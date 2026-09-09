// ============================================================
//  AI RECRUITMENT COPILOT — RESUME UPLOAD & PARSING MODULE
// ============================================================

const Resume = (() => {

  let uploadedFiles = [];
  let parsingState  = { active: false, progress: 0, currentFile: null };

  // ── SVG Icons ─────────────────────────────────────────────
  const ICONS = {
    upload: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>`,
    file:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>`,
    check:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`,
    spin:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>`,
    x:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
  };

  // ── Mock parsed profiles ───────────────────────────────────
  const PARSED_PROFILES = [
    {
      name: 'Sarah Johnson', email: 'sarah.j@example.com', phone: '+1 (555) 123-4567',
      experience: '5 years', education: 'MS Computer Science', location: 'San Francisco, CA',
      skills: ['Python','Machine Learning','TensorFlow','Data Analysis','SQL','Project Management','NLP'],
    },
    {
      name: 'Michael Chen', email: 'michael.c@example.com', phone: '+1 (555) 987-6543',
      experience: '8 years', education: 'BS Computer Engineering', location: 'Austin, TX',
      skills: ['JavaScript','React','Node.js','PostgreSQL','Redis','TypeScript','GraphQL'],
    },
    {
      name: 'Emily Rodriguez', email: 'emily.r@example.com', phone: '+1 (555) 234-5678',
      experience: '4 years', education: 'MS Data Science', location: 'New York, NY',
      skills: ['Python','R','Statistics','Spark','Tableau','SQL','Scikit-learn'],
    },
  ];

  // ── Initialize ────────────────────────────────────────────
  function init() {
    renderDropzone();
    renderParsingPanel();
    renderRecentTable();
  }

  // ── Dropzone ──────────────────────────────────────────────
  function renderDropzone() {
    const container = document.getElementById('dropzone-container');
    if (!container) return;

    container.innerHTML = `
      <div class="dropzone" id="dropzone" ondragover="Resume.handleDragOver(event)" ondragleave="Resume.handleDragLeave(event)" ondrop="Resume.handleDrop(event)" onclick="document.getElementById('file-input').click()">
        <input type="file" id="file-input" accept=".pdf,.docx,.doc" multiple style="display:none" onchange="Resume.handleFileSelect(event)">
        <div class="dropzone-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:28px;height:28px;color:white"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg></div>
        <div class="dropzone-title">Drop resumes here</div>
        <div class="dropzone-sub">or click to browse your files</div>
        <button class="btn btn-primary" onclick="event.stopPropagation();document.getElementById('file-input').click()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
          Upload Files
        </button>
        <div class="dropzone-formats">
          <span class="format-chip">PDF</span>
          <span class="format-chip">DOCX</span>
          <span class="format-chip">DOC</span>
          <span style="font-size:var(--fs-xs);color:var(--txt-muted)">Max 10MB per file</span>
        </div>
      </div>
      <div class="uploaded-files-list" id="uploaded-files-list"></div>
    `;
  }

  // ── Drag & Drop ───────────────────────────────────────────
  function handleDragOver(e) {
    e.preventDefault();
    document.getElementById('dropzone').classList.add('drag-over');
  }

  function handleDragLeave(e) {
    document.getElementById('dropzone').classList.remove('drag-over');
  }

  function handleDrop(e) {
    e.preventDefault();
    document.getElementById('dropzone').classList.remove('drag-over');
    const files = Array.from(e.dataTransfer.files).filter(f => isValidFile(f));
    if (files.length) processFiles(files);
    else App.showToast('Only PDF and DOCX files are supported.', 'error');
  }

  function handleFileSelect(e) {
    const files = Array.from(e.target.files).filter(f => isValidFile(f));
    if (files.length) processFiles(files);
    e.target.value = '';
  }

  function isValidFile(f) {
    return /\.(pdf|docx|doc)$/i.test(f.name);
  }

  // ── File Processing ───────────────────────────────────────
  function processFiles(files) {
    files.forEach(file => {
      const id = 'file_' + Date.now() + Math.random().toString(36).slice(2);
      const fileObj = {
        id, name: file.name,
        size: formatSize(file.size || Math.random() * 2000000 + 500000),
        status: 'parsing',
        parsedData: null,
      };
      uploadedFiles.unshift(fileObj);
      addFileToUI(fileObj);
      simulateParsing(fileObj);
    });
    App.showToast(`${files.length} file${files.length > 1 ? 's' : ''} queued for parsing.`, 'info');
  }

  function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  }

  // ── Add file row ───────────────────────────────────────────
  function addFileToUI(fileObj) {
    const list = document.getElementById('uploaded-files-list');
    if (!list) return;
    const el = document.createElement('div');
    el.className = 'file-item';
    el.id = `file-item-${fileObj.id}`;
    el.innerHTML = `
      <div class="file-icon">${ICONS.file}</div>
      <div class="file-info">
        <div class="file-name">${fileObj.name}</div>
        <div class="file-meta">Uploaded just now · ${fileObj.size}</div>
      </div>
      <div class="file-status parsing" id="status-${fileObj.id}">
        <div class="spinner" style="width:14px;height:14px;border-top-color:var(--clr-amber)"></div>
        Parsing...
      </div>
    `;
    list.prepend(el);
  }

  // ── Simulate AI parsing ────────────────────────────────────
  function simulateParsing(fileObj) {
    const profileIdx = Math.floor(Math.random() * PARSED_PROFILES.length);
    const profile    = { ...PARSED_PROFILES[profileIdx], fileName: fileObj.name };
    fileObj.parsedData = profile;

    setTimeout(() => {
      const statusEl = document.getElementById(`status-${fileObj.id}`);
      if (statusEl) {
        statusEl.className = 'file-status done';
        statusEl.innerHTML = `${ICONS.check} Parsed`;
      }
      fileObj.status = 'done';
      updateParsingPanel(profile);
      updateRecentTable();
      animateProgressBars();
      App.showToast(`Resume parsed: <strong>${profile.name}</strong>`, 'success');
    }, 2500 + Math.random() * 1500);
  }

  // ── Parsing Progress Panel ─────────────────────────────────
  function renderParsingPanel() {
    const el = document.getElementById('parsing-panel');
    if (!el) return;

    const sample = PARSED_PROFILES[0];
    el.innerHTML = `
      <div class="card parsing-card" style="height:100%">
        <div class="card-header">
          <div>
            <div style="font-size:var(--fs-md);font-weight:700">Parsing Progress</div>
            <div style="font-size:var(--fs-xs);color:var(--txt-muted);margin-top:2px">Real-time extraction status</div>
          </div>
          <div class="badge badge-emerald">
            <div class="status-dot online" style="width:6px;height:6px"></div>
            Live
          </div>
        </div>
        <div class="card-body" style="display:flex;flex-direction:column;gap:var(--space-5)">

          <!-- Stat Row -->
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-4)">
            ${MOCK.stats.parsing.map(s => `
              <div style="text-align:center;padding:var(--space-4);background:rgba(99,102,241,0.06);border-radius:var(--radius-md);border:1px solid var(--clr-border)">
                <div style="font-size:var(--fs-xl);font-weight:800;color:var(--txt-primary);counter-anim" id="pstat-${s.id}">${s.value}</div>
                <div style="font-size:10px;color:var(--txt-muted);text-transform:uppercase;letter-spacing:.05em;margin-top:4px">${s.label}</div>
              </div>
            `).join('')}
          </div>

          <!-- Extraction Progress -->
          <div class="extraction-progress">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--space-3)">
              <div style="font-size:var(--fs-sm);font-weight:600;color:var(--txt-secondary)">Extraction Progress</div>
              <div style="font-size:var(--fs-sm);font-weight:700;color:var(--clr-indigo-light)" id="extraction-pct">95%</div>
            </div>
            <div class="progress-bar-wrap" style="height:10px">
              <div class="progress-bar-fill" id="main-progress-bar" style="width:0%"></div>
            </div>
          </div>

          <!-- Divider -->
          <div class="divider" style="margin:0"></div>

          <!-- Extracted Profile -->
          <div>
            <div style="font-size:var(--fs-xs);text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--txt-muted);margin-bottom:var(--space-3)">
              Extracted Information
            </div>
            <div class="extracted-profile" id="extracted-profile">
              <div class="profile-field"><div class="profile-field-label">Name</div><div class="profile-field-value">${sample.name}</div></div>
              <div class="profile-field"><div class="profile-field-label">Email</div><div class="profile-field-value">${sample.email}</div></div>
              <div class="profile-field"><div class="profile-field-label">Phone</div><div class="profile-field-value">${sample.phone}</div></div>
              <div class="profile-field"><div class="profile-field-label">Experience</div><div class="profile-field-value">${sample.experience}</div></div>
              <div class="profile-field"><div class="profile-field-label">Education</div><div class="profile-field-value">${sample.education}</div></div>
              <div class="profile-field"><div class="profile-field-label">Location</div><div class="profile-field-value">${sample.location}</div></div>
            </div>
          </div>

          <!-- Skills -->
          <div>
            <div style="font-size:var(--fs-xs);text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--txt-muted);margin-bottom:var(--space-3)">
              Skills
            </div>
            <div class="skills-list" id="extracted-skills">
              ${sample.skills.map((s, i) => `<span class="skill-tag${i % 3 === 1 ? ' cyan' : i % 3 === 2 ? ' purple' : ''}">${s}</span>`).join('')}
            </div>
          </div>

        </div>
      </div>
    `;

    // Animate bars on load
    setTimeout(animateProgressBars, 300);
  }

  function updateParsingPanel(profile) {
    const profileEl = document.getElementById('extracted-profile');
    const skillsEl  = document.getElementById('extracted-skills');
    if (!profileEl || !skillsEl) return;

    profileEl.innerHTML = `
      <div class="profile-field"><div class="profile-field-label">Name</div><div class="profile-field-value">${profile.name}</div></div>
      <div class="profile-field"><div class="profile-field-label">Email</div><div class="profile-field-value">${profile.email}</div></div>
      <div class="profile-field"><div class="profile-field-label">Phone</div><div class="profile-field-value">${profile.phone}</div></div>
      <div class="profile-field"><div class="profile-field-label">Experience</div><div class="profile-field-value">${profile.experience}</div></div>
      <div class="profile-field"><div class="profile-field-label">Education</div><div class="profile-field-value">${profile.education}</div></div>
      <div class="profile-field"><div class="profile-field-label">Location</div><div class="profile-field-value">${profile.location}</div></div>
    `;

    skillsEl.innerHTML = profile.skills.map((s, i) =>
      `<span class="skill-tag${i % 3 === 1 ? ' cyan' : i % 3 === 2 ? ' purple' : ''}">${s}</span>`
    ).join('');

    animateProgressBars();
  }

  function animateProgressBars() {
    const bar = document.getElementById('main-progress-bar');
    if (bar) {
      bar.style.width = '0%';
      setTimeout(() => { bar.style.width = '95%'; }, 50);
    }
  }

  // ── Recent candidates table ───────────────────────────────
  function renderRecentTable() {
    const el = document.getElementById('recent-candidates-table');
    if (!el) return;
    el.innerHTML = `
      <div class="card" style="margin-top:var(--space-6)">
        <div class="card-header">
          <div>
            <div style="font-size:var(--fs-md);font-weight:700">Recently Processed Candidates</div>
            <div style="font-size:var(--fs-xs);color:var(--txt-muted);margin-top:2px">Latest resume parsing results</div>
          </div>
          <button class="btn btn-secondary btn-sm" onclick="App.navigate('candidates')">View All</button>
        </div>
        <div class="card-body" style="padding:0">
          <table class="data-table" id="recent-table-body">
            <thead>
              <tr>
                <th>Candidate Name</th>
                <th>Email</th>
                <th>Experience</th>
                <th>Key Skills</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="recent-tbody">
              ${getRecentTableRows()}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  function getRecentTableRows() {
    return MOCK.candidates.slice(0, 5).map(c => `
      <tr onclick="App.openCandidateModal('${c.id}')" style="cursor:pointer">
        <td>
          <div style="display:flex;align-items:center;gap:var(--space-3)">
            <div class="avatar avatar-sm" style="background:${c.color}">${c.initials}</div>
            ${c.name}
          </div>
        </td>
        <td>${c.email}</td>
        <td>${c.experience}</td>
        <td>
          <div style="display:flex;gap:var(--space-1);flex-wrap:wrap">
            ${c.skills.slice(0,3).map(s => `<span class="skill-tag" style="font-size:10px;padding:2px 8px">${s}</span>`).join('')}
          </div>
        </td>
        <td><span class="badge ${c.status === 'Processed' ? 'badge-emerald' : 'badge-amber'}">${c.status}</span></td>
      </tr>
    `).join('');
  }

  function updateRecentTable() {
    const tbody = document.getElementById('recent-tbody');
    if (tbody) tbody.innerHTML = getRecentTableRows();
  }

  // ── Simulate a demo upload on first visit ─────────────────
  function runDemoUpload() {
    const demoFiles = [
      { name: 'Sarah_Johnson_Resume.pdf', size: 1200000 },
      { name: 'Michael_Chen_CV.docx',     size: 890000  },
    ];
    setTimeout(() => {
      demoFiles.forEach((f, i) => {
        setTimeout(() => {
          const fileObj = {
            id: 'demo_' + i,
            name: f.name,
            size: formatSize(f.size),
            status: 'parsing',
            parsedData: null,
          };
          uploadedFiles.unshift(fileObj);
          addFileToUI(fileObj);
          simulateParsing(fileObj);
        }, i * 600);
      });
    }, 800);
  }

  // ── Public API ────────────────────────────────────────────
  return { init, handleDragOver, handleDragLeave, handleDrop, handleFileSelect, runDemoUpload };

})();
