// ============================================================
//  AI RECRUITMENT COPILOT — APPLICATION CORE (Router + State)
// ============================================================

const App = (() => {

  // ── State ─────────────────────────────────────────────────
  let currentPage = 'dashboard';
  let toastTimer  = null;

  // ── SVG Icon Library ─────────────────────────────────────
  const I = {
    dashboard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`,
    upload:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`,
    users:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
    briefcase: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="12"/></svg>`,
    chart:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
    interview: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
    settings:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>`,
    bell:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`,
    search:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`,
    download:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
    plus:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
    x:         `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
    check:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`,
    alert:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
    info:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
    mail:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>`,
    phone:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.53 2 2 0 0 1 3.58 1.35h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.1a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>`,
    loc:       `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 1 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`,
    grad:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>`,
    brain:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.46 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.46 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>`,
    star:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
    refresh:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>`,
    filter:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>`,
  };

  // ── Navigation Config ──────────────────────────────────────
  const navItems = [
    { id: 'dashboard',   label: 'Dashboard',       icon: 'dashboard',  badge: null },
    { id: 'resume',      label: 'Resume Upload',    icon: 'upload',     badge: 'M1' },
    { id: 'candidates',  label: 'Candidates',       icon: 'users',      badge: null },
    { id: 'jobs',        label: 'Job Postings',     icon: 'briefcase',  badge: null },
    { id: 'analytics',   label: 'Analytics',        icon: 'chart',      badge: null },
    { id: 'interview',   label: 'Interview Assist', icon: 'interview',  badge: 'M3' },
    { id: 'settings',    label: 'Settings',         icon: 'settings',   badge: null },
  ];

  // ── Sidebar ───────────────────────────────────────────────
  function renderSidebar() {
    const el = document.getElementById('sidebar');
    if (!el) return;
    el.innerHTML = `
      <!-- Logo -->
      <div class="sidebar-logo">
        <div class="logo-mark">RC</div>
        <div class="logo-text">
          <strong>Recruitment</strong>
          <span>Copilot AI · Part 1</span>
        </div>
      </div>

      <!-- Milestone Pill -->
      <div class="milestone-pill">
        <div class="milestone-pill-label">Current Milestone</div>
        <div class="milestone-pill-name">📄 Resume Parsing & Profiling</div>
        <div class="milestone-pill-bar">
          <div class="milestone-pill-fill" style="width:33%"></div>
        </div>
        <div style="font-size:10px;color:var(--txt-muted)">Part 1 of 3 · Weeks 1–3</div>
      </div>

      <!-- Nav -->
      <div class="sidebar-section">
        <div class="sidebar-section-label">Navigation</div>
        ${navItems.map((n, i) => `
          <div class="nav-item ${n.id === currentPage ? 'active' : ''}"
               id="nav-${n.id}"
               style="--nav-i:${i}"
               onclick="App.navigate('${n.id}')">
            ${I[n.icon]}
            <span>${n.label}</span>
            ${n.badge ? `<span class="nav-badge">${n.badge}</span>` : ''}
          </div>
        `).join('')}
      </div>

      <!-- Footer -->
      <div class="sidebar-footer">
        <div class="user-widget">
          <div class="avatar avatar-sm" style="background:linear-gradient(135deg,#6366f1,#a855f7)">JR</div>
          <div class="user-info">
            <div class="user-name">Jamie Recruiter</div>
            <div class="user-role">Senior HR Manager</div>
          </div>
          <div style="color:var(--txt-muted);width:16px;height:16px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
          </div>
        </div>
      </div>
    `;
  }

  // ── Top Bar ───────────────────────────────────────────────
  function renderTopBar() {
    const pageLabels = {
      dashboard:  'Dashboard',
      resume:     'Resume Upload',
      candidates: 'Candidates',
      jobs:       'Job Postings',
      analytics:  'Analytics',
      interview:  'Interview Assistant',
      settings:   'Settings',
    };
    const el = document.getElementById('top-bar');
    if (!el) return;
    el.innerHTML = `
      <div class="top-bar-breadcrumb">
        <span>AI Copilot</span>
        <span>›</span>
        <span class="current">${pageLabels[currentPage] || 'Page'}</span>
      </div>
      <div class="top-bar-search">
        <svg class="top-bar-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" placeholder="Search candidates, jobs…" id="global-search" oninput="App.handleSearch(this.value)">
      </div>
      <div class="top-bar-actions">
        <div class="top-bar-icon-btn" data-tooltip="Notifications" onclick="App.showToast('No new notifications','info')">
          ${I.bell}
          <div class="notif-dot"></div>
        </div>
        <div class="top-bar-icon-btn" data-tooltip="Refresh" onclick="App.refreshPage()">
          ${I.refresh}
        </div>
        <button class="btn btn-primary btn-sm" onclick="App.showNewPostingModal()">
          ${I.plus}
          New Job Posting
        </button>
        <button class="btn btn-ghost btn-sm" onclick="App.showToast('Export started…','info')">
          ${I.download}
          Export
        </button>
      </div>
    `;
  }

  // ── Pages ─────────────────────────────────────────────────
  function renderDashboard() {
    const el = document.getElementById('page-dashboard');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <!-- Header -->
        <div class="section-header">
          <div>
            <h1 class="grad-text">AI Recruitment Copilot</h1>
            <p class="section-subtitle">Automate candidate screening and improve hiring efficiency with AI</p>
          </div>
          <div style="display:flex;gap:var(--space-3)">
            <button class="btn btn-ghost btn-sm" onclick="App.showToast('Export report…','info')">${I.download} Export</button>
            <button class="btn btn-primary" onclick="App.showNewPostingModal()">${I.plus} New Job Posting</button>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid-stats">
          ${MOCK.stats.dashboard.map(s => `
            <div class="card stat-card" style="--stat-accent:${s.accent}">
              <div class="stat-label">${s.label}</div>
              <div class="stat-value" id="stat-${s.id}">0</div>
              <div class="stat-delta up">${I.check} ${s.delta} from last month</div>
            </div>
          `).join('')}
        </div>

        <!-- Main Grid -->
        <div class="dashboard-grid">
          <!-- Left: Pipeline + Recent -->
          <div style="display:flex;flex-direction:column;gap:var(--space-6)">
            <!-- Pipeline Chart -->
            <div class="card">
              <div class="card-header">
                <div>
                  <div style="font-size:var(--fs-md);font-weight:700">Recruitment Pipeline</div>
                  <div style="font-size:var(--fs-xs);color:var(--txt-muted);margin-top:2px">Current hiring funnel overview</div>
                </div>
                <div style="display:flex;gap:var(--space-2)">
                  <button class="btn btn-ghost btn-sm">${I.filter} Filter</button>
                </div>
              </div>
              <div class="card-body">
                <div id="pipeline-chart"></div>
              </div>
            </div>

            <!-- Quick Actions -->
            <div class="card">
              <div class="card-header">
                <div style="font-size:var(--fs-md);font-weight:700">Quick Actions</div>
              </div>
              <div class="card-body">
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-4)">
                  ${quickAction('Parse Resumes', 'upload', 'rgba(99,102,241,0.12)', 'var(--clr-indigo-light)', "App.navigate('resume')")}
                  ${quickAction('Browse Candidates', 'users', 'rgba(6,182,212,0.12)', 'var(--clr-cyan-light)', "App.navigate('candidates')")}
                  ${quickAction('Post a Job', 'briefcase', 'rgba(168,85,247,0.12)', 'var(--clr-purple-light)', "App.showNewPostingModal()")}
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Activity Feed -->
          <div class="card" style="height:fit-content">
            <div class="card-header">
              <div>
                <div style="font-size:var(--fs-md);font-weight:700">Recent Activity</div>
                <div style="font-size:var(--fs-xs);color:var(--txt-muted);margin-top:2px">Live system events</div>
              </div>
              <div class="badge badge-emerald">
                <div class="status-dot online" style="width:6px;height:6px"></div>
                Live
              </div>
            </div>
            <div class="card-body">
              <div class="activity-feed">
                ${MOCK.activities.map(a => renderActivityItem(a)).join('')}
              </div>
            </div>
          </div>
        </div>

        <!-- Part 1 Milestone Banner -->
        <div style="margin-top:var(--space-6)">
          <div class="card" style="background:linear-gradient(135deg,rgba(99,102,241,0.1) 0%,rgba(6,182,212,0.06) 100%)">
            <div class="card-body" style="display:flex;align-items:center;gap:var(--space-6)">
              <div style="width:56px;height:56px;border-radius:var(--radius-xl);background:var(--grad-primary);display:flex;align-items:center;justify-content:center;flex-shrink:0;animation:float 3s ease-in-out infinite;box-shadow:0 8px 24px rgba(99,102,241,0.35)">
                ${I.brain.replace('viewBox', 'width="24" height="24" viewBox')}
              </div>
              <div style="flex:1">
                <div style="font-size:var(--fs-lg);font-weight:700;margin-bottom:var(--space-1)">🎯 Part 1: Resume Parsing & Job Analysis <span class="badge badge-cyan" style="vertical-align:middle;margin-left:8px">Weeks 1–3</span></div>
                <div style="font-size:var(--fs-sm);color:var(--txt-secondary)">Currently active: Resume upload, candidate profiling, and job description analysis. Parts 2 and 3 unlock candidate matching, interview simulation, and full analytics dashboard.</div>
              </div>
              <div style="display:flex;gap:var(--space-3);flex-shrink:0">
                <button class="btn btn-primary" onclick="App.navigate('resume')">${I.upload} Start Parsing</button>
                <button class="btn btn-secondary" onclick="App.navigate('jobs')">${I.briefcase} View Jobs</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    `;

    // Animate stats count-up
    MOCK.stats.dashboard.forEach(s => {
      const el2 = document.getElementById(`stat-${s.id}`);
      if (el2) {
        if (typeof s.value === 'number') {
          animateCountUp(el2, s.value, 1200);
        } else {
          setTimeout(() => { el2.textContent = s.value; el2.style.animation = 'bounceIn 0.5s'; }, 400);
        }
      }
    });

    // Render pipeline chart
    setTimeout(() => Charts.renderPipelineChart('pipeline-chart'), 100);
  }

  function quickAction(label, icon, bg, color, onclick) {
    return `
      <div onclick="${onclick}" style="display:flex;flex-direction:column;align-items:center;gap:var(--space-3);padding:var(--space-5);background:${bg};border-radius:var(--radius-lg);border:1px solid rgba(255,255,255,0.06);cursor:pointer;transition:all var(--dur-base) var(--ease-out);text-align:center" class="quick-action-card">
        <div style="width:44px;height:44px;border-radius:var(--radius-md);background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;color:${color}">
          ${I[icon]}
        </div>
        <div style="font-size:var(--fs-sm);font-weight:600;color:var(--txt-primary)">${label}</div>
      </div>
    `;
  }

  function renderActivityItem(a) {
    const iconSvg = { upload: I.upload, user: I.users, job: I.briefcase, match: I.star, alert: I.alert }[a.icon] || I.info;
    return `
      <div class="activity-item">
        <div class="activity-icon" style="background:${a.color}">${iconSvg}</div>
        <div class="activity-content">
          <div class="activity-text">${a.text}</div>
          <div class="activity-time">${a.time}</div>
        </div>
      </div>
    `;
  }

  function renderResumePage() {
    const el = document.getElementById('page-resume');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <div class="section-header">
          <div>
            <h1>Resume Parsing <span class="grad-text">&amp; Candidate Profiling</span></h1>
            <p class="section-subtitle">Upload and process resumes to create structured candidate profiles</p>
          </div>
          <div class="badge badge-indigo" style="font-size:var(--fs-sm);padding:8px 16px">Milestone 1</div>
        </div>

        <div class="grid-2">
          <!-- Upload Panel -->
          <div style="display:flex;flex-direction:column;gap:var(--space-5)">
            <div class="card">
              <div class="card-header">
                <div>
                  <div style="font-size:var(--fs-md);font-weight:700">Upload Resume</div>
                  <div style="font-size:var(--fs-xs);color:var(--txt-muted);margin-top:2px">Supports PDF, DOCX, DOC formats</div>
                </div>
                <button class="btn btn-ghost btn-sm" onclick="Resume.runDemoUpload()">
                  ${I.star} Run Demo
                </button>
              </div>
              <div class="card-body">
                <div id="dropzone-container"></div>
              </div>
            </div>
          </div>

          <!-- Parsing Panel -->
          <div id="parsing-panel"></div>
        </div>

        <!-- Recent Table -->
        <div id="recent-candidates-table"></div>
      </div>
    `;
    Resume.init();
  }

  function renderCandidatesPage() {
    const el = document.getElementById('page-candidates');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <div class="section-header">
          <div>
            <h1>Candidate <span class="grad-text">Profiles</span></h1>
            <p class="section-subtitle">${MOCK.candidates.length} candidates parsed and profiled</p>
          </div>
          <div style="display:flex;gap:var(--space-3)">
            <button class="btn btn-ghost btn-sm">${I.filter} Filter</button>
            <button class="btn btn-primary btn-sm" onclick="App.navigate('resume')">${I.plus} Add Candidate</button>
          </div>
        </div>

        <!-- Search & Filter Bar -->
        <div class="card" style="margin-bottom:var(--space-5)">
          <div class="card-body" style="padding:var(--space-4) var(--space-6);display:flex;align-items:center;gap:var(--space-4)">
            <div style="position:relative;flex:1;max-width:340px">
              ${I.search.replace('viewBox', 'style="position:absolute;left:12px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:var(--txt-muted);pointer-events:none" viewBox')}
              <input class="form-control" type="text" placeholder="Search by name, skill, location…" style="padding-left:38px;width:100%" id="cand-search" oninput="App.filterCandidates(this.value)">
            </div>
            <select class="form-control" style="width:160px" id="cand-sort" onchange="App.sortCandidates(this.value)">
              <option value="score">Sort by Match %</option>
              <option value="name">Sort by Name</option>
              <option value="exp">Sort by Experience</option>
            </select>
            <div style="margin-left:auto;font-size:var(--fs-sm);color:var(--txt-muted)">
              Showing <strong style="color:var(--txt-primary)" id="cand-count">${MOCK.candidates.length}</strong> candidates
            </div>
          </div>
        </div>

        <!-- Candidates Grid -->
        <div class="grid-auto" id="candidates-grid">
          ${MOCK.candidates.map(c => renderCandidateCard(c)).join('')}
        </div>
      </div>
    `;
  }

  function renderCandidateCard(c) {
    return `
      <div class="card candidate-card" onclick="App.openCandidateModal('${c.id}')">
        <div class="candidate-card-header">
          <div class="avatar avatar-lg" style="background:${c.color}">${c.initials}</div>
          <div class="candidate-info">
            <div class="candidate-name">${c.name}</div>
            <div class="candidate-title">${c.title}</div>
            <div class="candidate-location">${I.loc.replace('viewBox', 'width="12" height="12" viewBox')} ${c.location}</div>
          </div>
          <div class="match-score ${c.scoreClass}">${c.score}%</div>
        </div>
        <div class="candidate-card-skills">
          ${c.skills.slice(0,5).map((s, i) => `<span class="skill-tag${c.skillColors && c.skillColors[i] ? ' ' + c.skillColors[i] : ''}">${s}</span>`).join('')}
        </div>
        <div class="candidate-card-footer">
          <div class="candidate-meta-chips">
            <div class="meta-chip">${I.briefcase.replace('viewBox', 'width="12" height="12" viewBox')} ${c.experience}</div>
            <div class="meta-chip">${I.grad.replace('viewBox', 'width="12" height="12" viewBox')} ${c.education.split('—')[0].trim()}</div>
          </div>
          <span class="badge ${c.status === 'Processed' ? 'badge-emerald' : 'badge-amber'}">${c.status}</span>
        </div>
      </div>
    `;
  }

  function renderJobsPage() {
    const el = document.getElementById('page-jobs');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <div class="section-header">
          <div>
            <h1>Job Postings <span class="grad-text">&amp; JD Analysis</span></h1>
            <p class="section-subtitle">Process job descriptions and extract structured requirements</p>
          </div>
          <button class="btn btn-primary" onclick="App.showNewPostingModal()">${I.plus} New Posting</button>
        </div>

        <div class="jd-grid">
          <!-- Job List -->
          <div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:var(--space-5)">
              <div style="font-size:var(--fs-md);font-weight:600;color:var(--txt-secondary)">${MOCK.jobs.length} Active Postings</div>
              <select class="form-control" style="width:160px" onchange="Jobs.sortJobs && Jobs.sortJobs(this.value)">
                <option>Newest First</option>
                <option>Most Applicants</option>
                <option>Salary High–Low</option>
              </select>
            </div>
            <div id="job-list"></div>
          </div>

          <!-- Analyzer Panel -->
          <div id="jd-analyzer"></div>
        </div>
      </div>
    `;
    Jobs.init();
  }

  function renderAnalyticsPage() {
    const el = document.getElementById('page-analytics');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <div class="section-header">
          <div>
            <h1>Recruitment <span class="grad-text">Analytics</span></h1>
            <p class="section-subtitle">Insights and metrics for smarter hiring decisions</p>
          </div>
          <span class="badge badge-amber">Coming in Part 3</span>
        </div>
        <div class="card">
          <div class="card-body">
            <div class="coming-soon-block">
              <div class="coming-soon-icon">${I.chart.replace('viewBox', 'width="36" height="36" viewBox')}</div>
              <h2 class="coming-soon-title">Analytics <span class="grad-text">Dashboard</span></h2>
              <p class="coming-soon-desc">Full recruitment analytics, candidate funnel visualization, hiring metrics, and AI-generated reports will be available in Part 3 (Weeks 7–9).</p>
              <div class="coming-soon-badges">
                <span class="badge badge-indigo">Candidate Funnel</span>
                <span class="badge badge-cyan">Time-to-Hire</span>
                <span class="badge badge-purple">Skill Heatmap</span>
                <span class="badge badge-emerald">AI Reports</span>
                <span class="badge badge-amber">Voice Screening</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderInterviewPage() {
    const el = document.getElementById('page-interview');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <div class="section-header">
          <div>
            <h1>Interview <span class="grad-text">Assistant</span></h1>
            <p class="section-subtitle">AI-powered interview simulation and screening</p>
          </div>
          <span class="badge badge-purple">Coming in Part 2</span>
        </div>
        <div class="card">
          <div class="card-body">
            <div class="coming-soon-block">
              <div class="coming-soon-icon">${I.interview.replace('viewBox', 'width="36" height="36" viewBox')}</div>
              <h2 class="coming-soon-title">Interview <span class="grad-text">Simulation</span></h2>
              <p class="coming-soon-desc">Generate role-specific interview questions, conduct AI-powered mock interviews, and analyze candidate responses. Voice screening module included in Part 3.</p>
              <div class="coming-soon-badges">
                <span class="badge badge-indigo">Question Generator</span>
                <span class="badge badge-cyan">AI Simulation</span>
                <span class="badge badge-purple">Response Analysis</span>
                <span class="badge badge-emerald">ATS Integration</span>
                <span class="badge badge-amber">Voice Screening</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderSettingsPage() {
    const el = document.getElementById('page-settings');
    if (!el) return;
    el.innerHTML = `
      <div class="page-wrapper">
        <div class="section-header">
          <div>
            <h1>System <span class="grad-text">Settings</span></h1>
            <p class="section-subtitle">Configure integrations, preferences, and deployment options</p>
          </div>
        </div>
        <div class="grid-2">
          ${settingsSection('AI Model Configuration', 'brain', [
            { label: 'LLM Model', type: 'select', options: ['GPT-4o', 'Claude 3.5 Sonnet', 'Gemini 1.5 Pro'] },
            { label: 'Embedding Model', type: 'select', options: ['text-embedding-3-large', 'OpenAI Ada 002'] },
            { label: 'Confidence Threshold', type: 'range', value: '75' },
          ])}
          ${settingsSection('ATS Integration', 'briefcase', [
            { label: 'ATS Provider', type: 'select', options: ['Greenhouse', 'Lever', 'Workday', 'Custom API'] },
            { label: 'API Endpoint', type: 'text', placeholder: 'https://api.greenhouse.io/v1' },
            { label: 'API Key', type: 'password', placeholder: '••••••••••••••••' },
          ])}
          ${settingsSection('Resume Parsing', 'upload', [
            { label: 'Parser Engine', type: 'select', options: ['Spacy NLP', 'NLTK', 'Hugging Face'] },
            { label: 'Max Resume Size', type: 'select', options: ['5 MB', '10 MB', '20 MB'] },
            { label: 'Auto-profile Creation', type: 'toggle', checked: true },
          ])}
          ${settingsSection('Notifications', 'bell', [
            { label: 'Email Alerts', type: 'toggle', checked: true },
            { label: 'Slack Integration', type: 'toggle', checked: false },
            { label: 'Daily Summary', type: 'toggle', checked: true },
          ])}
        </div>
      </div>
    `;
  }

  function settingsSection(title, icon, fields) {
    const fieldHTML = fields.map(f => {
      if (f.type === 'select') {
        return `<div class="form-group"><label class="form-label">${f.label}</label>
          <select class="form-control">${f.options.map(o => `<option>${o}</option>`).join('')}</select></div>`;
      }
      if (f.type === 'toggle') {
        return `<div style="display:flex;align-items:center;justify-content:space-between;padding:var(--space-3) 0;border-bottom:1px solid var(--clr-border)">
          <div style="font-size:var(--fs-sm);color:var(--txt-secondary)">${f.label}</div>
          <div onclick="this.classList.toggle('on')" style="width:40px;height:22px;border-radius:11px;background:${f.checked ? 'var(--clr-indigo)' : 'rgba(255,255,255,0.1)'};cursor:pointer;position:relative;transition:background .2s" ${f.checked ? 'class="on"' : ''}>
            <div style="width:16px;height:16px;border-radius:50%;background:white;position:absolute;top:3px;left:${f.checked ? '21px' : '3px'};transition:left .2s"></div>
          </div>
        </div>`;
      }
      return `<div class="form-group"><label class="form-label">${f.label}</label>
        <input class="form-control" type="${f.type || 'text'}" placeholder="${f.placeholder || ''}" value="${f.value || ''}"></div>`;
    }).join('');

    return `
      <div class="card">
        <div class="card-header">
          <div style="display:flex;align-items:center;gap:var(--space-3)">
            <div style="width:34px;height:34px;border-radius:var(--radius-md);background:rgba(99,102,241,0.12);display:flex;align-items:center;justify-content:center;color:var(--clr-indigo-light)">${I[icon]}</div>
            <div style="font-size:var(--fs-md);font-weight:700">${title}</div>
          </div>
        </div>
        <div class="card-body" style="display:flex;flex-direction:column;gap:var(--space-4)">
          ${fieldHTML}
          <button class="btn btn-primary btn-sm" onclick="App.showToast('Settings saved!','success')">${I.check} Save Changes</button>
        </div>
      </div>
    `;
  }

  // ── Candidate Modal ───────────────────────────────────────
  function openCandidateModal(id) {
    const c = MOCK.candidates.find(x => x.id === id);
    if (!c) return;
    const modal = document.getElementById('candidate-modal');
    const body  = document.getElementById('candidate-modal-body');
    if (!body || !modal) return;

    body.innerHTML = `
      <!-- Hero -->
      <div class="profile-modal-hero">
        <div class="profile-modal-avatar" style="background:${c.color}">${c.initials}</div>
        <div class="profile-modal-info">
          <div class="profile-modal-name">${c.name}</div>
          <div style="font-size:var(--fs-md);color:var(--txt-secondary)">${c.title}</div>
          <div class="profile-modal-meta">
            <div class="profile-modal-meta-item">${I.mail.replace('viewBox','width="14" height="14" viewBox')} ${c.email}</div>
            <div class="profile-modal-meta-item">${I.phone.replace('viewBox','width="14" height="14" viewBox')} ${c.phone}</div>
            <div class="profile-modal-meta-item">${I.loc.replace('viewBox','width="14" height="14" viewBox')} ${c.location}</div>
            <div class="profile-modal-meta-item">${I.briefcase.replace('viewBox','width="14" height="14" viewBox')} ${c.experience}</div>
          </div>
        </div>
        <div style="text-align:center;flex-shrink:0">
          <div class="match-score ${c.scoreClass}" style="width:70px;height:70px;font-size:var(--fs-lg)">${c.score}%</div>
          <div style="font-size:10px;color:var(--txt-muted);margin-top:6px">AI Match</div>
        </div>
      </div>

      <!-- Modal Body -->
      <div class="modal-body" style="display:flex;flex-direction:column;gap:var(--space-6)">

        <!-- Summary -->
        <div>
          <div class="profile-section-title">Professional Summary</div>
          <div class="jd-ai-insight" style="margin-top:var(--space-2)">${c.summary}</div>
        </div>

        <!-- Skills & Certifications row -->
        <div class="grid-2" style="gap:var(--space-5)">
          <div>
            <div class="profile-section-title">Skills</div>
            <div class="skills-list">
              ${c.skills.map((s, i) => `<span class="skill-tag${c.skillColors && c.skillColors[i] ? ' ' + c.skillColors[i] : ''}">${s}</span>`).join('')}
            </div>
          </div>
          <div>
            <div class="profile-section-title">Certifications</div>
            <div style="display:flex;flex-direction:column;gap:var(--space-2)">
              ${c.certifications.map(cert => `
                <div style="display:flex;align-items:center;gap:var(--space-2);font-size:var(--fs-sm);color:var(--txt-secondary)">
                  ${I.check.replace('viewBox','width="14" height="14" viewBox').replace('stroke="currentColor"','stroke="var(--clr-success)"')} ${cert}
                </div>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Experience -->
        <div>
          <div class="profile-section-title">Work Experience</div>
          <div style="margin-top:var(--space-3)">
            ${c.experience_list.map((e, i, arr) => `
              <div class="exp-item">
                <div class="exp-timeline">
                  <div class="exp-dot"></div>
                  ${i < arr.length - 1 ? '<div class="exp-line"></div>' : ''}
                </div>
                <div class="exp-content">
                  <div class="exp-role">${e.role}</div>
                  <div class="exp-company">${e.company}</div>
                  <div class="exp-period">${e.period}</div>
                  <div class="exp-desc">${e.desc}</div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Actions -->
        <div style="display:flex;gap:var(--space-3);padding-top:var(--space-4);border-top:1px solid var(--clr-border)">
          <button class="btn btn-primary" onclick="App.showToast('Scheduling interview for ${c.name}…','success')">${I.interview.replace('viewBox','width="16" height="16" viewBox')} Schedule Interview</button>
          <button class="btn btn-secondary" onclick="App.showToast('Match analysis launching in Part 2!','info')">${I.star.replace('viewBox','width="16" height="16" viewBox')} Match to Job</button>
          <button class="btn btn-ghost" onclick="App.showToast('Export ready!','info')" style="margin-left:auto">${I.download.replace('viewBox','width="16" height="16" viewBox')} Export Profile</button>
        </div>
      </div>
    `;

    modal.classList.add('active');
  }

  function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('active');
  }

  // ── New Job Posting Modal ──────────────────────────────────
  function showNewPostingModal() {
    const modal = document.getElementById('new-job-modal');
    if (modal) modal.classList.add('active');
  }

  // ── Navigation ────────────────────────────────────────────
  function navigate(page) {
    currentPage = page;

    // Update nav
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const navEl = document.getElementById(`nav-${page}`);
    if (navEl) navEl.classList.add('active');

    // Show page
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const pageEl = document.getElementById(`page-${page}`);
    if (pageEl) {
      pageEl.classList.add('active');
      // Re-render dynamic pages
      const renderers = {
        dashboard:  renderDashboard,
        resume:     renderResumePage,
        candidates: renderCandidatesPage,
        jobs:       renderJobsPage,
        analytics:  renderAnalyticsPage,
        interview:  renderInterviewPage,
        settings:   renderSettingsPage,
      };
      if (renderers[page]) renderers[page]();
    }

    renderTopBar();
  }

  // ── Search ────────────────────────────────────────────────
  function handleSearch(val) {
    if (currentPage === 'candidates') filterCandidates(val);
  }

  function filterCandidates(val) {
    const q = val.toLowerCase();
    const grid = document.getElementById('candidates-grid');
    const count = document.getElementById('cand-count');
    if (!grid) return;
    const filtered = q
      ? MOCK.candidates.filter(c =>
          c.name.toLowerCase().includes(q) ||
          c.title.toLowerCase().includes(q) ||
          c.skills.some(s => s.toLowerCase().includes(q)) ||
          c.location.toLowerCase().includes(q)
        )
      : MOCK.candidates;
    grid.innerHTML = filtered.map(c => renderCandidateCard(c)).join('');
    if (count) count.textContent = filtered.length;
  }

  function sortCandidates(by) {
    const sorted = [...MOCK.candidates].sort((a, b) => {
      if (by === 'score') return b.score - a.score;
      if (by === 'name') return a.name.localeCompare(b.name);
      if (by === 'exp') return parseInt(b.experience) - parseInt(a.experience);
      return 0;
    });
    const grid = document.getElementById('candidates-grid');
    if (grid) grid.innerHTML = sorted.map(c => renderCandidateCard(c)).join('');
  }

  function refreshPage() {
    navigate(currentPage);
    showToast('Page refreshed', 'success');
  }

  // ── Toast Notifications ───────────────────────────────────
  function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const id = 'toast_' + Date.now();
    const icons = { success: I.check, error: I.x, info: I.info };
    const colors = { success: 'var(--clr-success)', error: 'var(--clr-danger)', info: 'var(--clr-indigo-light)' };

    const el = document.createElement('div');
    el.id = id;
    el.className = `toast ${type}`;
    el.innerHTML = `
      <div style="color:${colors[type]};flex-shrink:0">${icons[type]}</div>
      <div style="flex:1;font-size:var(--fs-sm)">${message}</div>
      <div onclick="this.closest('.toast').remove()" style="color:var(--txt-muted);cursor:pointer;flex-shrink:0">${I.x}</div>
    `;
    container.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateX(40px)'; setTimeout(() => el.remove(), 300); }, 4000);
  }

  // ── Count-up Animation ────────────────────────────────────
  function animateCountUp(el, target, duration) {
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(eased * target).toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString();
    };
    setTimeout(() => requestAnimationFrame(step), 200);
  }

  // ── Init ──────────────────────────────────────────────────
  function init() {
    renderSidebar();
    navigate('dashboard');

    // Hover effect for quick action cards
    document.addEventListener('mouseover', e => {
      const card = e.target.closest('.quick-action-card');
      if (card) card.style.transform = 'translateY(-3px)';
    });
    document.addEventListener('mouseout', e => {
      const card = e.target.closest('.quick-action-card');
      if (card) card.style.transform = '';
    });
  }

  return { init, navigate, openCandidateModal, closeModal, showNewPostingModal, showToast, handleSearch, filterCandidates, sortCandidates, refreshPage };

})();
