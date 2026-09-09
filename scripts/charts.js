// ============================================================
//  AI RECRUITMENT COPILOT — CHARTS MODULE
// ============================================================

const Charts = (() => {

  // ── Pipeline Bar Chart ────────────────────────────────────
  function renderPipelineChart(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const maxH = 160;
    el.innerHTML = `
      <div class="pipeline-chart-wrap">
        ${MOCK.pipeline.map((p, i) => `
          <div class="pipeline-bar-group">
            <div class="pipeline-bar-val" style="font-size:11px">${p.count.toLocaleString()}</div>
            <div class="pipeline-bar" style="
              --bar-color: ${p.color};
              --bar-h: ${p.height}px;
              --bar-delay: ${i * 120}ms;
              background: ${p.color};
            "></div>
            <div class="pipeline-bar-label">${p.stage}</div>
          </div>
        `).join('')}
      </div>
    `;
  }

  // ── Donut / Gauge Chart ───────────────────────────────────
  function renderDonut(containerId, percent, color = '#6366f1', label = '') {
    const el = document.getElementById(containerId);
    if (!el) return;

    const r = 36;
    const circumference = 2 * Math.PI * r;
    const dashOffset = circumference * (1 - percent / 100);

    el.innerHTML = `
      <div class="score-ring-wrap" style="width:90px;height:90px">
        <svg width="90" height="90" viewBox="0 0 90 90">
          <circle cx="45" cy="45" r="${r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
          <circle cx="45" cy="45" r="${r}" fill="none" stroke="${color}" stroke-width="8"
            stroke-dasharray="${circumference}" stroke-dashoffset="${circumference}"
            stroke-linecap="round"
            style="transition: stroke-dashoffset 1.4s cubic-bezier(0.16,1,0.3,1);
                   --dash-offset:${dashOffset}"
            id="${containerId}-ring"/>
        </svg>
        <div class="score-ring-center">
          <div class="score-ring-value" style="color:${color};font-size:18px">${percent}%</div>
          ${label ? `<div class="score-ring-label">${label}</div>` : ''}
        </div>
      </div>
    `;

    // Animate after mount
    setTimeout(() => {
      const ring = document.getElementById(`${containerId}-ring`);
      if (ring) ring.style.strokeDashoffset = dashOffset;
    }, 100);
  }

  // ── Mini Sparkline ────────────────────────────────────────
  function renderSparkline(containerId, values, color = '#6366f1') {
    const el = document.getElementById(containerId);
    if (!el) return;

    const w = 80, h = 32;
    const max = Math.max(...values);
    const min = Math.min(...values);
    const range = max - min || 1;
    const pts = values.map((v, i) => {
      const x = (i / (values.length - 1)) * w;
      const y = h - ((v - min) / range) * h;
      return `${x},${y}`;
    }).join(' ');

    el.innerHTML = `
      <svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="overflow:visible">
        <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
        <circle cx="${pts.split(' ').pop().split(',')[0]}" cy="${pts.split(' ').pop().split(',')[1]}" r="3" fill="${color}"/>
      </svg>
    `;
  }

  // ── Horizontal bar (skill level) ──────────────────────────
  function renderSkillBar(containerId, percent, color) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = `
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:0%;background:${color || 'var(--grad-primary)'}"></div>
      </div>
    `;
    setTimeout(() => {
      const fill = el.querySelector('.progress-bar-fill');
      if (fill) fill.style.width = percent + '%';
    }, 100);
  }

  // ── Wave animation (voice module placeholder) ─────────────
  function renderWave(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const bars = Array.from({ length: 32 }, (_, i) => {
      const delay = (i * 0.05).toFixed(2);
      const h = 8 + Math.random() * 24;
      return `<div style="width:4px;height:${h}px;background:var(--grad-primary);border-radius:2px;
        animation: wave 0.8s ease-in-out infinite alternate;
        animation-delay:${delay}s"></div>`;
    }).join('');
    el.innerHTML = `<div style="display:flex;align-items:center;gap:3px;height:40px">${bars}</div>`;
  }

  return { renderPipelineChart, renderDonut, renderSparkline, renderSkillBar, renderWave };

})();
