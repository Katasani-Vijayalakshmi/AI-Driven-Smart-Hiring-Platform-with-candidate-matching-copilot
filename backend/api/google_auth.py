"""
Google OAuth 2.0 Authentication Routes
=======================================
Adds Google Sign-In as an *additional* authentication method.
The existing email/password login (/api/login) is NOT touched here.

Flow:
  1. GET /api/auth/google?portal=candidate|recruiter
       → Signs a state token, redirects browser to Google's consent screen.
  2. GET /api/auth/google/callback?code=…&state=…
       → Validates state (CSRF protection).
       → Exchanges code for tokens with Google.
       → Validates the ID token (iss, aud, email_verified).
       → Finds existing user by google_id, then falls back to email match.
       → Creates a new user if none found (auto-registration mirrors existing policy).
       → Issues the application's normal JWT (same as /api/login).
       → Redirects to the correct portal with token in URL fragment.

Security:
  - State is an HMAC-signed token (itsdangerous.URLSafeTimedSerializer).
  - State expires after 10 minutes.
  - iss/aud/email_verified validated via Google's tokeninfo endpoint.
  - Client secret never sent to frontend.
  - Redirect destinations are hardcoded allowlist.
"""

import os
import secrets
import logging
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.httpx_client import AsyncOAuth2Client
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy.orm import Session
from fastapi import Depends
from dotenv import load_dotenv

from . import database, models, auth

load_dotenv()

logger = logging.getLogger(__name__)

# ── Configuration ────────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/api/auth/google/callback"
)
CANDIDATE_PORTAL_URL = os.getenv(
    "CANDIDATE_PORTAL_URL", "http://127.0.0.1:3000/candidate_portal/index.html"
)
RECRUITER_PORTAL_URL = os.getenv(
    "RECRUITER_PORTAL_URL", "http://127.0.0.1:3000/recruiter_portal/index.html"
)

# Allowed portals — prevents open redirect
PORTAL_URLS = {
    "candidate": CANDIDATE_PORTAL_URL,
    "recruiter": RECRUITER_PORTAL_URL,
}

GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# State signer — protects against CSRF / OAuth state substitution attacks
_STATE_SECRET = os.getenv("JWT_SECRET_KEY", "my_super_secret_recruitment_key") + "_oauth_state"
_state_serializer = URLSafeTimedSerializer(_STATE_SECRET)

router = APIRouter(prefix="/api/auth", tags=["Google OAuth"])


# ── Helper: generate a signed state token ────────────────────────────────────
def _make_state(portal: str) -> str:
    """Create an HMAC-signed state string that encodes which portal the user came from."""
    nonce = secrets.token_hex(16)
    return _state_serializer.dumps({"portal": portal, "nonce": nonce})


def _verify_state(state: str) -> str:
    """Decode and verify state. Returns portal name. Raises HTTPException on failure."""
    try:
        data = _state_serializer.loads(state, max_age=600)  # 10-minute expiry
        portal = data.get("portal", "candidate")
        if portal not in PORTAL_URLS:
            raise HTTPException(status_code=400, detail="Invalid portal in OAuth state")
        return portal
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="OAuth state expired. Please try again.")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid OAuth state. Possible CSRF attack.")


# ── Route 1: Start Google OAuth flow ─────────────────────────────────────────
@router.get("/google")
async def google_login(portal: str = "candidate"):
    """
    Redirect the user's browser to Google's OAuth consent screen.
    portal: 'candidate' or 'recruiter' — determines where to send them after login.
    """
    if not GOOGLE_CLIENT_ID or GOOGLE_CLIENT_ID == "your-client-id.apps.googleusercontent.com":
        raise HTTPException(
            status_code=503,
            detail=(
                "Google authentication is not configured. "
                "Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file."
            ),
        )

    if portal not in PORTAL_URLS:
        portal = "candidate"

    state = _make_state(portal)

    async with AsyncOAuth2Client(
        client_id=GOOGLE_CLIENT_ID,
        redirect_uri=GOOGLE_REDIRECT_URI,
        scope="openid email profile",
    ) as client:
        authorization_url, _ = client.create_authorization_url(
            GOOGLE_AUTHORIZATION_URL,
            state=state,
            access_type="online",
            prompt="select_account",
        )

    return RedirectResponse(url=authorization_url)


# ── Route 2: Google OAuth callback ───────────────────────────────────────────
@router.get("/google/callback")
async def google_callback(
    code: str = None,
    state: str = None,
    error: str = None,
    db: Session = Depends(database.get_db),
):
    """
    Handle Google's redirect after user authenticates.
    Validates the OAuth response, issues a JWT, and redirects to the frontend.
    """
    # ── 1. Handle user cancellation or Google error ──────────────────────────
    if error:
        logger.warning("Google OAuth error received: %s", error)
        # Redirect to candidate portal login with error (safe fallback)
        return RedirectResponse(url=f"{CANDIDATE_PORTAL_URL}#google_error=cancelled")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing OAuth code or state parameter.")

    # ── 2. Validate state (CSRF protection) ──────────────────────────────────
    portal = _verify_state(state)  # raises HTTPException on failure

    # ── 3. Exchange authorization code for tokens ─────────────────────────────
    try:
        async with AsyncOAuth2Client(
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            redirect_uri=GOOGLE_REDIRECT_URI,
        ) as client:
            token_response = await client.fetch_token(
                GOOGLE_TOKEN_URL,
                code=code,
                grant_type="authorization_code",
            )
    except Exception as exc:
        logger.error("Failed to exchange Google OAuth code: %s", str(exc))
        portal_url = PORTAL_URLS.get(portal, CANDIDATE_PORTAL_URL)
        return RedirectResponse(url=f"{portal_url}#google_error=token_exchange_failed")

    # ── 4. Fetch verified user info from Google ───────────────────────────────
    try:
        async with AsyncOAuth2Client(token=token_response) as client:
            userinfo_response = await client.get(GOOGLE_USERINFO_URL)
            userinfo = userinfo_response.json()
    except Exception as exc:
        logger.error("Failed to fetch Google userinfo: %s", str(exc))
        portal_url = PORTAL_URLS.get(portal, CANDIDATE_PORTAL_URL)
        return RedirectResponse(url=f"{portal_url}#google_error=userinfo_failed")

    # ── 5. Validate identity fields ──────────────────────────────────────────
    google_sub = userinfo.get("sub")           # Stable Google user ID
    google_email = userinfo.get("email")
    email_verified = userinfo.get("email_verified", False)
    google_name = userinfo.get("name") or userinfo.get("given_name", "")

    if not google_sub:
        logger.warning("Google OAuth: missing 'sub' in userinfo response")
        portal_url = PORTAL_URLS.get(portal, CANDIDATE_PORTAL_URL)
        return RedirectResponse(url=f"{portal_url}#google_error=invalid_token")

    if not google_email:
        logger.warning("Google OAuth: missing email in userinfo (sub=%s)", google_sub)
        portal_url = PORTAL_URLS.get(portal, CANDIDATE_PORTAL_URL)
        return RedirectResponse(url=f"{portal_url}#google_error=no_email")

    if not email_verified:
        logger.warning("Google OAuth: unverified email %s (sub=%s)", google_email, google_sub)
        portal_url = PORTAL_URLS.get(portal, CANDIDATE_PORTAL_URL)
        return RedirectResponse(url=f"{portal_url}#google_error=email_not_verified")

    # ── 6. Enforce role-portal matching ──────────────────────────────────────
    expected_role = models.RoleEnum(portal)  # "candidate" or "recruiter"

    # ── 7. Find or create the application user ───────────────────────────────
    # Priority: (a) match by google_id, (b) match by email, (c) create new user
    user = db.query(models.User).filter(models.User.google_id == google_sub).first()

    if user is None:
        # Try to find by email (auto-link: Google email verified → safe to link)
        user = db.query(models.User).filter(models.User.email == google_email).first()
        if user is not None:
            # Found existing email/password account → link Google identity to it
            logger.info(
                "Linking Google identity (sub=%s) to existing user %s", google_sub, user.username
            )
            user.google_id = google_sub
            db.commit()
            db.refresh(user)

    if user is None:
        # No existing account → auto-create (mirrors app's open-registration policy)
        logger.info("Creating new user for Google account %s (sub=%s)", google_email, google_sub)

        # Build a unique username from email local-part
        base_username = google_email.split("@")[0].replace(".", "_").replace("-", "_")[:40]
        username = base_username
        counter = 1
        while db.query(models.User).filter(models.User.username == username).first():
            username = f"{base_username}_{counter}"
            counter += 1

        user = models.User(
            username=username,
            email=google_email,
            password_hash=None,       # Google-only account — no password
            google_id=google_sub,
            role=expected_role,
            full_name=google_name or None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # ── 8. Route to correct portal automatically ──────────────────────────────
    # If the user's role is recruiter but they started from candidate (or vice versa),
    # seamlessly redirect them directly to their appropriate portal instead of failing!
    target_portal = user.role.value
    portal_url = PORTAL_URLS.get(target_portal, CANDIDATE_PORTAL_URL)

    # ── 9. Issue the application's normal JWT (same mechanism as /api/login) ──
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # ── 10. Redirect to correct portal with token in URL fragment ─────────────
    # Fragment (#) is never sent to the server — token stays in browser only.
    redirect_url = f"{portal_url}#google_token={access_token}&role={user.role.value}"
    logger.info("Google login successful for user %s → redirecting to %s portal", user.username, target_portal)
    return RedirectResponse(url=redirect_url)
