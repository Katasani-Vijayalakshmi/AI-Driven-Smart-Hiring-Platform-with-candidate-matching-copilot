// ============================================================
//  AI RECRUITMENT COPILOT — JOB DESCRIPTION ANALYSIS MODULE
// ============================================================

const Jobs = (() => {

  let selectedJobId = MOCK.jobs[0].id;

  // ── Initialize ────────────────────────────────────────────
  function init() {
    renderJobList();
    renderAnalyzerPanel(selectedJobId);
  }

  // ── Job List ──────────────────────────────────────────────
  function renderJobList() {
    const el = document.getElementById('job-list');
    if (!el) return;

    el.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:var(--space-4)">
        ${MOCK.jobs.map(job => renderJobCard(job)).join('')}
      </div>
    `;
  }

  function renderJobCard(job) {
    const isSelected = job.id === selectedJobId;
    const daysLabel = job.postedDays === 1 ? '1 day ago' : `${job.postedDays} days ago`;
    return `
      <div class="card jd-card ${isSelected ? 'selected' : ''}" id="jd-card-${job.id}" onclick="Jobs.selectJob('${job.id}')">
        <div class="jd-card-header">
          <div style="flex:1;min-width:0">
            <div class="jd-role-name">${job.role}</div>
            <div class="jd-company">${job.company} · ${job.department}</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:flex-end;gap:var(--space-2);flex-shrink:0">
            <span class="badge badge-indigo">${job.level}</span>
            <span style="font-size:var(--fs-xs);color:var(--txt-muted)">${daysLabel}</span>
          </div>
        </div>
        <div class="jd-meta">
          ${metaChip(`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 1 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>`, job.location)}
          ${metaChip(`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`, job.type)}
          ${metaChip(`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`, job.salary)}
          ${metaChip(`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`, `${job.applicants} applicants`)}
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:var(--space-1)">
          ${job.requiredSkills.slice(0,5).map(s => `<span class="skill-tag" style="font-size:10px;padding:3px 9px">${s}</span>`).join('')}
          ${job.requiredSkills.length > 5 ? `<span class="skill-tag" style="font-size:10px;padding:3px 9px;background:rgba(255,255,255,0.04)">+${job.requiredSkills.length - 5} more</span>` : ''}
        </div>
      </div>
    `;
  }

  function metaChip(icon, label) {
    return `<div style="display:flex;align-items:center;gap:4px;font-size:var(--fs-xs);color:var(--txt-muted)">${icon} ${label}</div>`;
  }

  // ── Analyzer Panel ────────────────────────────────────────
  function selectJob(id) {
    selectedJobId = id;

    // Update card selection state
    document.querySelectorAll('.jd-card').forEach(c => c.classList.remove('selected'));
    const card = document.getElementById(`jd-card-${id}`);
    if (card) card.classList.add('selected');

    renderAnalyzerPanel(id);
  }

  function renderAnalyzerPanel(id) {
    const job = MOCK.jobs.find(j => j.id === id);
    if (!job) return;
    const el = document.getElementById('jd-analyzer');
    if (!el) return;

    el.innerHTML = `
      <div class="jd-analyzer-panel" style="height:100%">
        <!-- Header -->
        <div class="jd-analyzer-header">
          <div>
            <div style="font-size:var(--fs-md);font-weight:700">JD Analysis</div>
            <div style="font-size:var(--fs-xs);color:var(--txt-muted);margin-top:2px">${job.role}</div>
          </div>
          <div class="badge badge-cyan">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="10" height="10"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Analyzed
          </div>
        </div>

        <!-- Body -->
        <div style="padding:var(--space-5);display:flex;flex-direction:column;gap:var(--space-5)">

          <!-- Score Summary -->
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-3)">
            ${scoreBubble(job.requiredSkills.length, 'Skills Required', 'var(--clr-indigo-light)')}
            ${scoreBubble(job.mustHave.length, 'Must Have', 'var(--clr-cyan-light)')}
            ${scoreBubble(job.applicants, 'Applicants', 'var(--clr-purple-light)')}
          </div>

          <!-- Requirements breakdown -->
          <div>
            <div style="font-size:var(--fs-xs);text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--txt-muted);margin-bottom:var(--space-3)">Requirements Breakdown</div>
            <div class="req-list">
              <div class="req-item">
                <div class="req-dot must"></div>
                <div class="req-text">Must Have</div>
                <div class="req-count">${job.mustHave.length} items</div>
              </div>
              <div class="req-item">
                <div class="req-dot preferred"></div>
                <div class="req-text">Preferred</div>
                <div class="req-count">${job.preferred.length} items</div>
              </div>
              <div class="req-item">
                <div class="req-dot nice"></div>
                <div class="req-text">Nice to Have</div>
                <div class="req-count">${job.niceToHave.length} items</div>
              </div>
            </div>
          </div>

          <!-- Must Have -->
          <div>
            <div style="font-size:var(--fs-xs);text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--txt-muted);margin-bottom:var(--space-3)">Must Have</div>
            <div style="display:flex;flex-direction:column;gap:var(--space-2)">
              ${job.mustHave.map(r => `
                <div style="display:flex;align-items:center;gap:var(--space-2);padding:8px var(--space-3);background:rgba(99,102,241,0.06);border-radius:var(--radius-sm);border-left:3px solid var(--clr-indigo)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="var(--clr-indigo-light)" stroke-width="2.5" width="14" height="14"><polyline points="20 6 9 17 4 12"/></svg>
                  <span style="font-size:var(--fs-sm);color:var(--txt-secondary)">${r}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Preferred -->
          <div>
            <div style="font-size:var(--fs-xs);text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--txt-muted);margin-bottom:var(--space-3)">Preferred</div>
            <div style="display:flex;flex-direction:column;gap:var(--space-2)">
              ${job.preferred.map(r => `
                <div style="display:flex;align-items:center;gap:var(--space-2);padding:8px var(--space-3);background:rgba(6,182,212,0.05);border-radius:var(--radius-sm);border-left:3px solid var(--clr-cyan)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="var(--clr-cyan-light)" stroke-width="2.5" width="14" height="14"><polyline points="20 6 9 17 4 12"/></svg>
                  <span style="font-size:var(--fs-sm);color:var(--txt-secondary)">${r}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- AI Insight -->
          <div class="jd-ai-insight">
            <div class="ai-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 6v6l4 2"/><circle cx="19" cy="5" r="3" fill="var(--clr-indigo)" stroke="none"/></svg>
              AI Insight
            </div>
            ${job.aiInsight}
          </div>

          <!-- Required Skills -->
          <div>
            <div style="font-size:var(--fs-xs);text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--txt-muted);margin-bottom:var(--space-3)">Required Skills</div>
            <div style="display:flex;flex-wrap:wrap;gap:var(--space-2)">
              ${job.requiredSkills.map((s, i) =>
                `<span class="skill-tag${i % 3 === 1 ? ' cyan' : i % 3 === 2 ? ' purple' : ''}">${s}</span>`
              ).join('')}
            </div>
          </div>

          <!-- Actions -->
          <div style="display:flex;gap:var(--space-3);flex-wrap:wrap">
            <button class="btn btn-primary" style="flex:1" onclick="App.showToast('Matching engine launching in Part 2!','info')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              Match Candidates
            </button>
            <button class="btn btn-secondary btn-sm" onclick="App.showToast('Export coming soon!','info')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export
            </button>
          </div>

        </div>
      </div>
    `;
  }

  function scoreBubble(value, label, color) {
    return `
      <div style="text-align:center;padding:var(--space-4) var(--space-3);background:rgba(255,255,255,0.03);border:1px solid var(--clr-border);border-radius:var(--radius-md)">
        <div style="font-size:var(--fs-xl);font-weight:800;color:${color}">${value}</div>
        <div style="font-size:10px;color:var(--txt-muted);text-transform:uppercase;letter-spacing:.05em;margin-top:3px">${label}</div>
      </div>
    `;
  }

  // ── New Posting Form ──────────────────────────────────────
  function renderNewPostingForm() {
    // Handled inline in main app (modal)
  }

  return { init, selectJob };

})();
