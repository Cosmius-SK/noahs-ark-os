// ==========================================
// app.js — Interactive logic for Noah's Ark OS
// ==========================================

/* ── Typewriter hero eyebrow ─────────────────────────────────────────────── */
(function() {
  const el = document.getElementById('heroEyebrow');
  if (!el) return;
  const text = 'Synthetic World Generation Engine';
  let i = 0;
  setTimeout(function tick() {
    el.textContent = text.slice(0, i) + (i < text.length ? '▌' : '');
    if (i <= text.length) { i++; setTimeout(tick, 55); }
  }, 400);
})();

/* ── Mobile nav ──────────────────────────────────────────────────────────── */
function closeDrawer() {
  document.getElementById('navDrawer').classList.remove('open');
}
document.getElementById('navMenuBtn').addEventListener('click', function() {
  document.getElementById('navDrawer').classList.toggle('open');
});
document.getElementById('navDrawer').addEventListener('click', function(e) {
  if (e.target === this) closeDrawer();
});

/* ── Nav scroll state + active section tracking ──────────────────────────── */
const nav = document.getElementById('mainNav');
const navLinks = document.querySelectorAll('.nav-links a[data-section]');
const sections = Array.from(document.querySelectorAll('section[id], div[id="statsBar"]'));

window.addEventListener('scroll', () => {
  // Scrolled style
  nav.classList.toggle('scrolled', window.scrollY > 60);

  // Active nav link
  const scrollMid = window.scrollY + window.innerHeight * 0.35;
  let active = null;
  for (const sec of sections) {
    if (sec.offsetTop <= scrollMid) active = sec.id;
  }
  navLinks.forEach(a => {
    a.classList.toggle('active', a.dataset.section === active);
  });
});

/* ── Reveal on scroll ────────────────────────────────────────────────────── */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const delay = e.target.style.getPropertyValue('--reveal-delay') || '0s';
      e.target.style.transitionDelay = delay;
      e.target.classList.add('visible');
      revealObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ── Stat counters ───────────────────────────────────────────────────────── */
function animateCounter(el, target, suffix) {
  let start = 0;
  const duration = 1400;
  const step = timestamp => {
    if (!step.startTime) step.startTime = timestamp;
    const progress = Math.min((timestamp - step.startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);
    el.textContent = current + suffix;
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target + suffix;
  };
  requestAnimationFrame(step);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const nums = e.target.querySelectorAll('[data-target]');
      nums.forEach(el => {
        animateCounter(el, parseInt(el.dataset.target), el.dataset.suffix || '');
      });
      statsObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.4 });

const statsBar = document.getElementById('statsBar');
if (statsBar) statsObserver.observe(statsBar);

/* ── World card expand ───────────────────────────────────────────────────── */
const worldLunar = document.getElementById('worldLunar');
const lunarDetail = document.getElementById('lunarDetail');
if (worldLunar && lunarDetail) {
  worldLunar.addEventListener('click', () => {
    const open = worldLunar.classList.toggle('expanded');
    lunarDetail.style.maxHeight = open ? lunarDetail.scrollHeight + 'px' : '0';
  });
}

/* ── Build tiles ─────────────────────────────────────────────────────────── */
const tevClass = { ok:"tev-ok", evolving:"tev-evolving", critical:"tev-critical" };
const tevLabel = { ok:"Stable", evolving:"Evolving", critical:"⚡ Critical" };

const tileGrid = document.getElementById('tileGrid');
if (tileGrid && typeof TILES !== 'undefined') {
  // Count badges
  const counts = { all: TILES.length, ok: 0, evolving: 0, critical: 0 };
  TILES.forEach(t => counts[t.status]++);
  ['all','ok','evolving','critical'].forEach(k => {
    const el = document.getElementById('fc-' + k);
    if (el) el.textContent = counts[k];
  });

  // Render tiles
  TILES.forEach(t => {
    const card = document.createElement('div');
    card.className = 'tile-card reveal';
    card.dataset.status = t.status;
    card.innerHTML = `
      <div class="tile-id">${t.id}</div>
      <div class="tile-name">${t.name}</div>
      <p class="tile-desc">${t.desc}</p>
      <span class="tile-tev ${tevClass[t.status]}">TEV ${t.tev} · ${tevLabel[t.status]}</span>
    `;
    tileGrid.appendChild(card);
    revealObserver.observe(card);
  });

  // Filter buttons
  document.querySelectorAll('#tileFilterBar .filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('#tileFilterBar .filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const filter = this.dataset.filter;
      document.querySelectorAll('.tile-card').forEach(card => {
        const show = filter === 'all' || card.dataset.status === filter;
        card.style.display = show ? '' : 'none';
      });
    });
  });
}

/* ── Build chapters timeline ─────────────────────────────────────────────── */
const timeline = document.getElementById('chaptersTimeline');
if (timeline && typeof CHAPTERS !== 'undefined') {
  CHAPTERS.forEach((ch, idx) => {
    const statusClass = { complete:'status-complete', active:'status-active', planned:'status-planned' }[ch.status];
    const statusLabel = { complete:'Complete', active:'In Progress', planned:'Planned' }[ch.status];

    const tagsHTML = ch.tags.map(t =>
      `<span class="tag ${t.style === 'teal' ? 'tag-teal' : t.style === 'gold' ? 'tag-gold' : ''}">${t.label}</span>`
    ).join('');

    const sprintsHTML = ch.sprints.length ? `
      <div class="chapter-sprints">
        ${ch.sprints.map(s => `
          <div class="sprint-block">
            <div class="sprint-id">${s.id}</div>
            <ul class="sprint-items">
              ${s.items.map(item => `<li>${item}</li>`).join('')}
            </ul>
          </div>
        `).join('')}
      </div>
    ` : '';

    const hasDetail = ch.sprints.length > 0;

    const item = document.createElement('div');
    item.className = 'chapter-item reveal';
    item.style.setProperty('--reveal-delay', `${idx * 0.07}s`);
    if (hasDetail) item.classList.add('has-detail');
    item.innerHTML = `
      <div class="chapter-dot"></div>
      <div class="chapter-header" ${hasDetail ? 'role="button" tabindex="0"' : ''}>
        <div class="chapter-meta">
          <span class="chapter-num">${ch.num}</span>
          <span class="chapter-status ${statusClass}">${statusLabel}</span>
          <span class="chapter-date">${ch.date}</span>
          ${hasDetail ? '<span class="chapter-toggle">+ Expand</span>' : ''}
        </div>
        <div class="chapter-title">${ch.title}</div>
        <p class="chapter-desc">${ch.desc}</p>
        <div class="chapter-tags">${tagsHTML}</div>
      </div>
      ${hasDetail ? `<div class="chapter-expandable">${sprintsHTML}</div>` : ''}
    `;

    if (hasDetail) {
      const header = item.querySelector('.chapter-header');
      const expandable = item.querySelector('.chapter-expandable');
      const toggle = item.querySelector('.chapter-toggle');
      let open = false;
      function toggleChapter() {
        open = !open;
        item.classList.toggle('open', open);
        expandable.style.maxHeight = open ? expandable.scrollHeight + 'px' : '0';
        if (toggle) toggle.textContent = open ? '− Collapse' : '+ Expand';
      }
      header.addEventListener('click', toggleChapter);
      header.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') toggleChapter(); });
    }

    timeline.appendChild(item);
    revealObserver.observe(item);
  });
}

/* ── Build version log ───────────────────────────────────────────────────── */
const versionTbody = document.getElementById('versionTbody');
if (versionTbody && typeof VERSIONS !== 'undefined') {
  function renderVersions(filter) {
    versionTbody.innerHTML = '';
    VERSIONS
      .filter(v => filter === 'all' || v.ch.startsWith(filter))
      .forEach((v, i) => {
        const tr = document.createElement('tr');
        tr.style.animationDelay = `${i * 0.03}s`;
        tr.className = 'vrow-appear';
        tr.innerHTML = `
          <td>${v.v}</td>
          <td>${v.date}</td>
          <td>${v.ch}</td>
          <td>
            <div class="vlog-desc">${v.title}</div>
            <div class="vlog-sub">${v.sub}</div>
          </td>
        `;
        versionTbody.appendChild(tr);
      });
  }

  renderVersions('all');

  document.querySelectorAll('#versionFilterBar .filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('#versionFilterBar .filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      renderVersions(this.dataset.vfilter);
    });
  });
}
