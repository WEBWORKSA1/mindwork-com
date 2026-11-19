/* MindWork.com — quizzes and page-specific wiring (home, daily workout, dashboard, lead plan, support, contest) */
(function () {
  'use strict';
  const MW = window.MW, el = MW.el, P = (MW.page = {});

  /* ---------- quiz engine ---------- */
  MW.mountQuiz = function () {
    const box = document.getElementById('quiz'), src = document.getElementById('quiz-data'); if (!box || !src) return;
    const D = JSON.parse(src.textContent); let i = 0, right = 0, tally = {};
    function ask() {
      box.innerHTML = ''; const q = D.questions[i], opts = el('div', { class: 'opts' });
      box.append(el('p', { class: 'muted', style: 'margin:0', text: 'Question ' + (i + 1) + ' of ' + D.questions.length }), el('div', { class: 'meter', style: 'margin:8px 0 4px' }, el('i', { style: 'width:' + (i / D.questions.length * 100) + '%' })), el('p', { class: 'q', text: q.q }), opts);
      q.opts.forEach((o, k) => {
        const b = el('button', { class: 'opt', type: 'button', text: typeof o === 'string' ? o : o.t });
        b.addEventListener('click', () => {
          if (D.type === 'match') { Object.keys(o.s).forEach(key => { tally[key] = (tally[key] || 0) + o.s[key]; }); i++; return i < D.questions.length ? ask() : end(); }
          opts.querySelectorAll('button').forEach((x, n) => { x.disabled = true; if (n === q.a) x.classList.add('right'); });
          if (k === q.a) right++; else b.classList.add('wrong');
          box.append(el('p', { class: 'note why ' + (k === q.a ? 'focus' : 'learn') }, el('b', { text: k === q.a ? 'Correct. ' : 'Not this one. ' }), q.why));
          box.append(el('button', { class: 'btn', type: 'button', style: 'margin-top:14px', text: i + 1 < D.questions.length ? 'Next question' : 'See my result', onclick: () => { i++; i < D.questions.length ? ask() : end(); } }));
        });
        opts.append(b);
      });
    }
    function end() {
      box.innerHTML = ''; let r, head;
      if (D.type === 'match') { const top = Object.keys(D.results).sort((a, b) => (tally[b] || 0) - (tally[a] || 0))[0]; r = D.results[top]; head = r.title; }
      else { r = D.results.filter(x => right >= x.min).sort((a, b) => b.min - a.min)[0]; head = right + ' of ' + D.questions.length + ': ' + r.title; }
      box.append(el('h2', { text: head }), el('p', { text: r.text }));
      const row = el('div', { class: 'btn-row' });
      if (r.link) row.append(el('a', { class: 'btn', href: MW.root + r.link[0], text: r.link[1] }));
      row.append(el('button', { class: 'btn ghost', type: 'button', text: 'Take the quiz again', onclick: () => { i = 0; right = 0; tally = {}; ask(); } }));
      const sh = el('button', { class: 'btn ghost', type: 'button', text: 'Share my result' }); sh.addEventListener('click', () => MW.share(D.share.replace('{r}', D.type === 'match' ? r.title : right + '/' + D.questions.length), sh)); row.append(sh);
      box.append(row); box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    ask();
  };

  /* ---------- daily workout list (home + daily page) ---------- */
  function dailyList(ul) {
    if (!ul) return; const picks = MW.daily.picks(), st = MW.daily.state(); ul.innerHTML = '';
    picks.forEach((id, n) => {
      const m = MW.META[id], done = st.done.indexOf(id) >= 0;
      ul.append(el('li', {}, el('a', { class: 'tile' + (done ? ' done' : ''), 'data-p': 'train', href: MW.root + m.url + '?daily=1' }, el('b', { text: (n + 1) + '. ' + m.name }), el('span', { text: done ? 'Done today' : 'About ' + (id === 'math' || id === 'nback' ? 'one minute' : 'two minutes') }))));
    });
    return { picks: picks, done: st.done.length };
  }
  P.home = function () {
    const pad = document.getElementById('hero-pad'); if (pad && MW.heroPad) MW.heroPad(pad);
    dailyList(document.getElementById('daily-picks'));
    const s = MW.daily.streak(), out = document.getElementById('home-streak');
    if (out && s.count) out.textContent = 'Current streak: ' + s.count + (s.count === 1 ? ' day' : ' days');
  };
  P.daily = function () {
    const r = dailyList(document.getElementById('daily-picks')), s = MW.daily.streak(), status = document.getElementById('daily-status'), dots = document.getElementById('streak-dots');
    if (status) status.textContent = r.done >= r.picks.length ? 'Today’s workout is done. Streak: ' + s.count + (s.count === 1 ? ' day.' : ' days.') + ' A new set appears at midnight, your time.' : r.done + ' of ' + r.picks.length + ' done. Finish all three to extend your streak' + (s.count ? ' of ' + s.count + (s.count === 1 ? ' day.' : ' days.') : '.');
    if (dots) {
      dots.innerHTML = ''; const days = s.days || [];
      for (let k = 6; k >= 0; k--) { const d = new Date(); d.setDate(d.getDate() - k); const key = MW.today(d); dots.append(el('li', { class: days.indexOf(key) >= 0 ? 'on' : '', title: key, text: ['S', 'M', 'T', 'W', 'T', 'F', 'S'][d.getDay()] })); }
    }
    const best = document.getElementById('streak-best'); if (best) best.textContent = String(s.best || 0);
  };

  /* ---------- dashboard ---------- */
  P.dashboard = function () {
    const all = MW.scores(), tb = document.getElementById('score-rows'), c = MW.composite();
    MW.ORDER.forEach(id => {
      const m = MW.META[id], s = all[id], tr = el('tr', {}, el('td', {}, el('a', { href: MW.root + m.url, text: m.name })));
      if (s && s.best != null) { const p = MW.pct(id, s.best); tr.append(el('td', { class: 'num', text: s.best + ' ' + m.unit }), el('td', { class: 'num', text: s.last + ' ' + m.unit }), el('td', { class: 'num', text: String(s.n) }), el('td', { style: 'min-width:120px' }, el('div', { class: 'meter', title: p + ' of 100' }, el('i', { style: 'width:' + p + '%' })))); }
      else tr.append(el('td', { colspan: '4' }, el('a', { href: MW.root + m.url, text: 'Take this test' })));
      tb.append(tr);
    });
    document.getElementById('comp-score').textContent = c.score == null ? '–' : String(c.score);
    document.getElementById('comp-note').textContent = c.score == null ? 'Take any test to start your score.' : 'Based on your best result in ' + c.done + ' of ' + c.total + ' tests. Finish the rest for a steadier number.';
    const s = MW.daily.streak(); document.getElementById('dash-streak').textContent = String(s.count); document.getElementById('dash-streak-best').textContent = String(s.best || 0);
    const L = MW.get('timerlog', {}), fb = document.getElementById('focus-rows'); let total = 0;
    for (let k = 6; k >= 0; k--) { const d = new Date(); d.setDate(d.getDate() - k); const key = MW.today(d), v = L[key] || { n: 0, min: 0 }; total += v.min; fb.append(el('tr', {}, el('td', { text: d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }), el('td', { class: 'num', text: String(v.n) }), el('td', { class: 'num', text: v.min + ' min' }))); }
    document.getElementById('focus-total').textContent = (total / 60).toFixed(1) + ' hours of timed focus in the last 7 days';
    document.getElementById('export-btn').addEventListener('click', () => {
      const data = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.indexOf('mw.') === 0) data[k] = localStorage.getItem(k); }
      const a = el('a', { href: URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })), download: 'mindwork-data.json' }); document.body.append(a); a.click(); a.remove();
    });
    document.getElementById('reset-btn').addEventListener('click', () => {
      if (!window.confirm('Delete every score, streak and saved tool from this browser? This cannot be undone.')) return;
      const keys = []; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.indexOf('mw.') === 0 && k !== 'mw.consent' && k !== 'mw.theme') keys.push(k); }
      keys.forEach(k => localStorage.removeItem(k)); location.reload();
    });
  };

  /* ---------- lead plan unlock ---------- */
  P.start = function () {
    const lock = document.getElementById('plan-lock'), form = document.getElementById('lead-form'); if (!lock) return;
    const open = () => { lock.classList.add('open'); const b = document.getElementById('print-plan'); if (b) b.hidden = false; };
    if (MW.get('lead', false)) open();
    if (form) form.addEventListener('mw:sent', () => { MW.set('lead', true); open(); lock.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  };

  /* ---------- support ---------- */
  P.support = function () {
    const links = (MW.cfg.payLinks || {}), box = document.getElementById('pay-now');
    if (box && (links.oneTime || links.monthly)) {
      box.hidden = false;
      if (links.oneTime) box.append(el('a', { class: 'btn', href: links.oneTime, target: '_blank', rel: 'noopener', text: 'Give once, securely' }));
      if (links.monthly) box.append(el('a', { class: 'btn ghost', href: links.monthly, target: '_blank', rel: 'noopener', text: 'Give monthly' }));
    }
    const other = document.getElementById('amount-other'), radios = document.querySelectorAll('input[name="amount"]');
    if (other) other.addEventListener('input', () => { if (other.value) radios.forEach(r => { r.checked = false; }); });
    radios.forEach(r => r.addEventListener('change', () => { if (other) other.value = ''; }));
  };

  /* ---------- contest ---------- */
  P.contest = function () {
    const now = new Date(), id = MW.ORDER[(now.getFullYear() * 12 + now.getMonth()) % MW.ORDER.length], m = MW.META[id], end = new Date(now.getFullYear(), now.getMonth() + 1, 0), c = MW.cfg.contest || {};
    const set = (i, t) => { const n = document.getElementById(i); if (n) n.textContent = t; };
    set('c-month', now.toLocaleDateString(undefined, { month: 'long', year: 'numeric' })); set('c-test', m.name);
    set('c-rule', m.low ? 'Lowest ' + m.unit + ' wins' : 'Highest ' + m.unit + ' wins');
    set('c-close', c.closes || end.toLocaleDateString(undefined, { day: 'numeric', month: 'long', year: 'numeric' }));
    set('c-prize', c.prize || 'No prize is posted for this round yet. Entries are ranked for the hall of fame.');
    const a = document.getElementById('c-link'); if (a) { a.href = MW.root + m.url; a.textContent = 'Play the ' + m.name + ' test'; }
    const f = document.getElementById('c-test-field'); if (f) f.value = m.name;
    const s = MW.scores()[id], sc = document.getElementById('c-score'), cd = document.getElementById('c-code');
    if (s && s.best != null && sc && !sc.value) { sc.value = s.best + ' ' + m.unit; }
    if (s && s.last != null && cd && !cd.value) { cd.placeholder = 'Shown under your result, for example ' + MW.code(id, s.last); }
  };

  document.addEventListener('mw:ready', function () {
    const page = document.body.getAttribute('data-page'); if (page && P[page]) P[page]();
    const g = document.body.getAttribute('data-game'); if (g && MW.mountGame) MW.mountGame(g);
    const t = document.body.getAttribute('data-tool'); if (t && MW.mountTool) MW.mountTool(t);
    if (document.getElementById('quiz')) MW.mountQuiz();
  });
})();
