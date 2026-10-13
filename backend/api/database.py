import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Prefer the configured DATABASE_URL when present; fall back to SQLite so the app
# can run locally without needing a MySQL server installed in the environment.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hcl.db")

engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # Production MySQL/PostgreSQL connection pooling for 100+ concurrent users
    engine_kwargs["pool_size"] = 15
    engine_kwargs["max_overflow"] = 25
    engine_kwargs["pool_timeout"] = 30

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
