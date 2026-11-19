/* MindWork.com — the six focus tools. Everything is stored in this browser only. */
(function () {
  'use strict';
  const MW = window.MW, el = MW.el, T = {};
  let actx = null;
  const audio = () => { if (!actx) { const A = window.AudioContext || window.webkitAudioContext; if (A) actx = new A(); } if (actx && actx.state === 'suspended') actx.resume(); return actx; };
  function beep() {
    const c = audio(); if (!c) return;
    [0, 0.28, 0.56].forEach((d, i) => { const o = c.createOscillator(), g = c.createGain(); o.frequency.value = i === 2 ? 880 : 660; o.connect(g); g.connect(c.destination); g.gain.setValueAtTime(0.0001, c.currentTime + d); g.gain.exponentialRampToValueAtTime(0.25, c.currentTime + d + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime + d + 0.22); o.start(c.currentTime + d); o.stop(c.currentTime + d + 0.25); });
  }
  const fmt = s => ('0' + Math.floor(s / 60)).slice(-2) + ':' + ('0' + (s % 60)).slice(-2);
  const num = (v, d, lo, hi) => { v = parseFloat(v); if (isNaN(v)) v = d; return Math.max(lo, Math.min(hi, v)); };

  /* 1 focus timer */
  T.timer = function (box) {
    const S = MW.get('timer', { focus: 25, short: 5, long: 15, every: 4, sound: true, tasks: [], active: -1, count: 0 });
    let mode = 'focus', left = S.focus * 60, endAt = 0, iv = null; const title = document.title;
    const face = el('div', { class: 'timer-face', role: 'timer', 'aria-live': 'off' }), modes = el('div', { class: 'chips', style: 'justify-content:center' });
    const names = { focus: 'Focus', short: 'Short break', long: 'Long break' }, mbtn = {};
    Object.keys(names).forEach(k => { mbtn[k] = el('button', { class: 'chip', type: 'button', text: names[k], onclick: () => setMode(k) }); modes.append(mbtn[k]); });
    const go = el('button', { class: 'btn', type: 'button', text: 'Start focus', onclick: toggle });
    const controls = el('div', { class: 'controls' }, go, el('button', { class: 'btn ghost', type: 'button', text: 'Reset', onclick: () => setMode(mode) }), el('button', { class: 'btn ghost', type: 'button', text: 'Skip to next', onclick: () => finish(true) }));
    const stat = el('p', { class: 'muted', style: 'text-align:center;margin:6px 0 0' });
    const list = el('ul', { class: 'tasklist' }), inp = el('input', { type: 'text', placeholder: 'What are you working on?', 'aria-label': 'New task', maxlength: '120' });
    const add = el('form', { class: 'inline-add' }, inp, el('button', { class: 'btn small', type: 'submit', text: 'Add task' }));
    add.addEventListener('submit', e => { e.preventDefault(); const t = inp.value.trim(); if (!t) return; S.tasks.push({ t: t, n: 0, done: false }); if (S.active < 0) S.active = S.tasks.length - 1; inp.value = ''; save(); tasks(); });
    const set = el('details', { style: 'margin-top:16px' }, el('summary', { text: 'Change the timer lengths' }));
    const grid = el('div', { class: 'form', style: 'margin-top:12px' }), row = el('div', { class: 'row' });
    [['focus', 'Focus minutes', 1, 180], ['short', 'Short break minutes', 1, 60], ['long', 'Long break minutes', 1, 90], ['every', 'Long break after this many sessions', 2, 12]].forEach(f => {
      const i = el('input', { type: 'number', min: f[2], max: f[3], value: S[f[0]] }); i.addEventListener('change', () => { S[f[0]] = num(i.value, S[f[0]], f[2], f[3]); i.value = S[f[0]]; save(); if (!iv) setMode(mode); });
      row.append(el('label', {}, f[1], i));
    });
    const snd = el('input', { type: 'checkbox' }); snd.checked = !!S.sound; snd.addEventListener('change', () => { S.sound = snd.checked; save(); });
    grid.append(row, el('label', { class: 'check' }, snd, 'Play three beeps when a timer ends')); set.append(grid);
    box.append(modes, face, controls, stat, add, list, set);
    function save() { MW.set('timer', S); }
    function log() { const L = MW.get('timerlog', {}), d = MW.today(); L[d] = L[d] || { n: 0, min: 0 }; L[d].n++; L[d].min += S.focus; MW.set('timerlog', L); }
    function stats() { const L = MW.get('timerlog', {})[MW.today()] || { n: 0, min: 0 }; stat.textContent = 'Today: ' + L.n + (L.n === 1 ? ' focus session, ' : ' focus sessions, ') + L.min + ' minutes'; }
    function draw() { face.textContent = fmt(left); document.title = iv ? fmt(left) + ' ' + names[mode] : title; go.textContent = iv ? 'Pause' : (mode === 'focus' ? 'Start focus' : 'Start break'); Object.keys(mbtn).forEach(k => mbtn[k].setAttribute('aria-pressed', String(k === mode))); }
    function setMode(k) { stop(); mode = k; left = S[k] * 60; draw(); }
    function stop() { if (iv) { clearInterval(iv); iv = null; } }
    function toggle() { if (iv) { stop(); draw(); return; } audio(); endAt = Date.now() + left * 1000; iv = setInterval(tick, 250); draw(); }
    function tick() { left = Math.max(0, Math.round((endAt - Date.now()) / 1000)); draw(); if (left <= 0) finish(false); }
    function finish(skipped) {
      stop();
      if (mode === 'focus' && !skipped) { S.count++; log(); if (S.tasks[S.active]) S.tasks[S.active].n++; save(); tasks(); }
      if (!skipped && S.sound) beep();
      setMode(mode === 'focus' ? (S.count > 0 && S.count % S.every === 0 ? 'long' : 'short') : 'focus'); stats();
    }
    function tasks() {
      list.innerHTML = '';
      S.tasks.forEach((t, i) => {
        const cb = el('input', { type: 'checkbox', 'aria-label': 'Mark done: ' + t.t }); cb.checked = t.done;
        cb.addEventListener('change', () => { t.done = cb.checked; save(); tasks(); });
        const li = el('li', { class: (i === S.active ? 'active ' : '') + (t.done ? 'done' : '') }, cb, el('span', { text: t.t, title: 'Work on this task', onclick: () => { S.active = i; save(); tasks(); } }), el('small', { class: 'muted', text: t.n + (t.n === 1 ? ' session' : ' sessions') }), el('button', { class: 'x', type: 'button', 'aria-label': 'Delete task', text: '×', onclick: () => { S.tasks.splice(i, 1); if (S.active >= S.tasks.length) S.active = S.tasks.length - 1; save(); tasks(); } }));
        list.append(li);
      });
    }
    draw(); stats(); tasks();
  };

  /* 2 breathing pacer */
  T.breathe = function (box) {
    const P = { box: ['Box 4-4-4-4', [4, 4, 4, 4]], long: ['Long exhale 4-6', [4, 0, 6, 0]], even: ['Even 5-5', [5, 0, 5, 0]], slow: ['4-7-8', [4, 7, 8, 0]] }, words = ['Breathe in', 'Hold', 'Breathe out', 'Hold'];
    let pat = MW.get('breath', 'box'), mins = 3, timer = null, endAt = 0; if (!P[pat]) pat = 'box';
    const chips = el('div', { class: 'chips', style: 'justify-content:center' }), disc = el('i'), label = el('b', { text: 'Ready' }), ring = el('div', { class: 'breath' }, disc, label);
    Object.keys(P).forEach(k => chips.append(el('button', { class: 'chip', type: 'button', text: P[k][0], 'aria-pressed': String(k === pat), onclick: e => { pat = k; MW.set('breath', k); chips.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === e.target))); if (timer) { stop(); start(); } } })));
    const len = el('select', { 'aria-label': 'Session length', style: 'font:inherit;padding:10px;border-radius:6px' }, el('option', { value: '1', text: '1 minute' }), el('option', { value: '3', text: '3 minutes', selected: '' }), el('option', { value: '5', text: '5 minutes' }), el('option', { value: '10', text: '10 minutes' }));
    len.addEventListener('change', () => { mins = parseInt(len.value, 10); });
    const go = el('button', { class: 'btn', type: 'button', text: 'Start breathing', onclick: () => (timer ? stop() : start()) }), clock = el('p', { class: 'muted', style: 'text-align:center;margin:8px 0 0', html: '&nbsp;' });
    box.append(chips, ring, el('div', { class: 'controls' }, len, go), clock);
    function start() { endAt = Date.now() + mins * 60000; go.textContent = 'Stop'; phase(0); }
    function stop() { clearTimeout(timer); timer = null; go.textContent = 'Start breathing'; label.textContent = 'Ready'; disc.style.transitionDuration = '600ms'; disc.style.transform = 'scale(.35)'; clock.innerHTML = '&nbsp;'; }
    function phase(i) {
      const secs = P[pat][1][i];
      if (Date.now() >= endAt && i === 0) { stop(); label.textContent = 'Done'; return; }
      if (!secs) return phase((i + 1) % 4);
      label.textContent = words[i]; clock.textContent = fmt(Math.max(0, Math.round((endAt - Date.now()) / 1000))) + ' left';
      if (i === 0 || i === 2) { disc.style.transitionDuration = secs * 1000 + 'ms'; disc.style.transform = i === 0 ? 'scale(1)' : 'scale(.35)'; }
      timer = setTimeout(() => phase((i + 1) % 4), secs * 1000);
    }
  };

  /* 3 noise mixer */
  T.noise = function (box) {
    const defs = [['brown', 'Brown noise'], ['pink', 'Pink noise'], ['white', 'White noise'], ['rain', 'Rain'], ['hum', 'Low hum']], vol = MW.get('noise', { brown: 40, pink: 0, white: 0, rain: 0, hum: 0 }), gains = {};
    let on = false, built = false, master = null, offTimer = null;
    const go = el('button', { class: 'btn', type: 'button', text: 'Play sound', onclick: toggle }), sleep = el('select', { 'aria-label': 'Stop after', style: 'font:inherit;padding:10px;border-radius:6px' }, el('option', { value: '0', text: 'Play until I stop it' }), el('option', { value: '15', text: 'Stop after 15 minutes' }), el('option', { value: '30', text: 'Stop after 30 minutes' }), el('option', { value: '60', text: 'Stop after 60 minutes' }));
    sleep.addEventListener('change', arm);
    const mix = el('div', { class: 'mixer' });
    defs.forEach(d => {
      const out = el('span', { class: 'muted', text: vol[d[0]] + '%' }), r = el('input', { type: 'range', min: '0', max: '100', value: vol[d[0]], 'aria-label': d[1] + ' volume' });
      r.addEventListener('input', () => { vol[d[0]] = parseInt(r.value, 10); out.textContent = r.value + '%'; MW.set('noise', vol); if (gains[d[0]]) gains[d[0]].gain.value = vol[d[0]] / 100; });
      mix.append(el('label', {}, d[1], r, out));
    });
    box.append(el('div', { class: 'controls' }, go, sleep), mix);
    function buffer(c, type) {
      const n = 2 * c.sampleRate, b = c.createBuffer(1, n, c.sampleRate), d = b.getChannelData(0); let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0, last = 0;
      for (let i = 0; i < n; i++) {
        const w = Math.random() * 2 - 1;
        if (type === 'white') d[i] = w * 0.35;
        else if (type === 'pink') { b0 = 0.99886 * b0 + w * 0.0555179; b1 = 0.99332 * b1 + w * 0.0750759; b2 = 0.969 * b2 + w * 0.153852; b3 = 0.8665 * b3 + w * 0.3104856; b4 = 0.55 * b4 + w * 0.5329522; b5 = -0.7616 * b5 - w * 0.016898; d[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362) * 0.11; b6 = w * 0.115926; }
        else { last = (last + 0.02 * w) / 1.02; d[i] = last * 3.5; }
      }
      return b;
    }
    function build() {
      const c = audio(); if (!c) return false; master = c.createGain(); master.gain.value = 0; master.connect(c.destination);
      const bufs = { white: buffer(c, 'white'), pink: buffer(c, 'pink'), brown: buffer(c, 'brown') };
      defs.forEach(d => {
        const k = d[0], src = c.createBufferSource(), g = c.createGain(); src.buffer = bufs[k === 'rain' ? 'white' : k === 'hum' ? 'brown' : k]; src.loop = true; g.gain.value = vol[k] / 100; let node = src;
        if (k === 'rain') { const hp = c.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 1800; const lp = c.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 7500; src.connect(hp); hp.connect(lp); node = lp; }
        if (k === 'hum') { const lp = c.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 140; src.connect(lp); node = lp; }
        node.connect(g); g.connect(master); src.start(); gains[k] = g;
      });
      built = true; return true;
    }
    function toggle() {
      if (!built && !build()) { go.textContent = 'Audio is not supported in this browser'; go.disabled = true; return; }
      on = !on; audio(); master.gain.setTargetAtTime(on ? 0.9 : 0, actx.currentTime, 0.15); go.textContent = on ? 'Stop sound' : 'Play sound'; arm();
    }
    function arm() { clearTimeout(offTimer); const m = parseInt(sleep.value, 10); if (on && m) offTimer = setTimeout(() => { if (on) toggle(); }, m * 60000); }
  };

  /* 4 eisenhower matrix */
  T.matrix = function (box) {
    const Q = [['1', 'Do today', 'Urgent and important'], ['2', 'Schedule it', 'Important, not urgent'], ['3', 'Hand off or batch', 'Urgent, not important'], ['4', 'Drop it', 'Neither']];
    let items = MW.get('matrix', []);
    const inp = el('input', { type: 'text', placeholder: 'Add a task', 'aria-label': 'Task', maxlength: '140' }), sel = el('select', { 'aria-label': 'Quadrant', style: 'font:inherit;padding:10px;border-radius:6px' });
    Q.forEach(q => sel.append(el('option', { value: q[0], text: q[1] })));
    const add = el('form', { class: 'inline-add', style: 'margin:0 0 14px' }, inp, sel, el('button', { class: 'btn small', type: 'submit', text: 'Add task' }));
    add.addEventListener('submit', e => { e.preventDefault(); const t = inp.value.trim(); if (!t) return; items.push({ t: t, q: sel.value }); inp.value = ''; save(); });
    const grid = el('div', { class: 'quad' }), foot = el('div', { class: 'btn-row', style: 'margin-top:14px' }, el('button', { class: 'btn ghost small', type: 'button', text: 'Print the matrix', onclick: () => window.print() }), el('button', { class: 'btn ghost small', type: 'button', text: 'Clear every task', onclick: () => { if (items.length && window.confirm('Remove every task from the matrix?')) { items = []; save(); } } }));
    box.append(add, grid, foot);
    function save() { MW.set('matrix', items); draw(); }
    function draw() {
      grid.innerHTML = '';
      Q.forEach(q => {
        const ul = el('ul');
        items.forEach((it, i) => {
          if (it.q !== q[0]) return;
          const mv = el('select', { 'aria-label': 'Move task' }); Q.forEach(o => { const op = el('option', { value: o[0], text: o[1] }); if (o[0] === it.q) op.selected = true; mv.append(op); });
          mv.addEventListener('change', () => { it.q = mv.value; save(); });
          ul.append(el('li', {}, el('span', { text: it.t }), mv, el('button', { class: 'x', type: 'button', 'aria-label': 'Delete task', text: '×', onclick: () => { items.splice(i, 1); save(); } })));
        });
        if (!ul.children.length) ul.append(el('li', { class: 'muted', style: 'border-style:dashed', text: 'Nothing here yet' }));
        grid.append(el('section', { 'data-q': q[0] }, el('h4', { text: q[1] }), el('small', { text: q[2] }), ul));
      });
    }
    draw();
  };

  /* 5 decision matrix */
  T.decide = function (box) {
    const blank = () => ({ options: ['Option A', 'Option B'], criteria: [{ name: 'Impact', w: 5 }, { name: 'Cost', w: 3 }, { name: 'Speed', w: 2 }], scores: [[5, 5, 5], [5, 5, 5]] });
    let S = MW.get('decide', null) || blank();
    const wrap = el('div', { class: 'table-scroll' }), verdict = el('p', { class: 'note focus', style: 'margin-top:14px' });
    const bar = el('div', { class: 'btn-row', style: 'margin-top:12px' },
      el('button', { class: 'btn small', type: 'button', text: 'Add an option', onclick: () => { S.options.push('Option ' + String.fromCharCode(65 + S.options.length % 26)); S.scores.push(S.criteria.map(() => 5)); save(); } }),
      el('button', { class: 'btn small', type: 'button', text: 'Add a criterion', onclick: () => { S.criteria.push({ name: 'Criterion ' + (S.criteria.length + 1), w: 3 }); S.scores.forEach(r => r.push(5)); save(); } }),
      el('button', { class: 'btn ghost small', type: 'button', text: 'Start over', onclick: () => { S = blank(); save(); } }));
    box.append(wrap, verdict, bar);
    function save() { MW.set('decide', S); draw(); }
    function totals() { const sw = S.criteria.reduce((a, c) => a + c.w, 0) || 1; return S.scores.map(r => r.reduce((a, v, j) => a + v * S.criteria[j].w, 0) / sw); }
    function draw() {
      const tot = totals(), max = Math.max.apply(null, tot), table = el('table', { class: 'dm' }), hr = el('tr', {}, el('th', { text: 'Option' }));
      S.criteria.forEach((c, j) => {
        const n = el('input', { type: 'text', value: c.name, 'aria-label': 'Criterion name' }), w = el('input', { type: 'number', min: '1', max: '10', value: c.w, 'aria-label': 'Weight for ' + c.name, title: 'Weight, 1 to 10' });
        n.addEventListener('change', () => { c.name = n.value.trim() || c.name; save(); }); w.addEventListener('change', () => { c.w = num(w.value, c.w, 1, 10); save(); });
        hr.append(el('th', {}, n, el('div', { style: 'display:flex;gap:6px;align-items:center;margin-top:4px;font-weight:400;font-size:.82rem' }, 'Weight', w, S.criteria.length > 1 ? el('button', { class: 'x', type: 'button', 'aria-label': 'Remove criterion ' + c.name, text: '×', onclick: () => { S.criteria.splice(j, 1); S.scores.forEach(r => r.splice(j, 1)); save(); } }) : null)));
      });
      hr.append(el('th', { class: 'num', text: 'Weighted score' })); table.append(el('thead', {}, hr));
      const tb = el('tbody');
      S.options.forEach((o, i) => {
        const name = el('input', { type: 'text', value: o, 'aria-label': 'Option name' }); name.addEventListener('change', () => { S.options[i] = name.value.trim() || o; save(); });
        const tr = el('tr', { class: tot[i] === max && S.options.length > 1 ? 'win' : '' }, el('td', {}, el('div', { style: 'display:flex;gap:4px' }, name, S.options.length > 1 ? el('button', { class: 'x', type: 'button', 'aria-label': 'Remove ' + o, text: '×', onclick: () => { S.options.splice(i, 1); S.scores.splice(i, 1); save(); } }) : null)));
        S.criteria.forEach((c, j) => { const v = el('input', { type: 'number', min: '1', max: '10', value: S.scores[i][j], 'aria-label': o + ' score for ' + c.name }); v.addEventListener('change', () => { S.scores[i][j] = num(v.value, 5, 1, 10); save(); }); tr.append(el('td', {}, v)); });
        tr.append(el('td', { class: 'num total', text: tot[i].toFixed(2) })); tb.append(tr);
      });
      table.append(tb); wrap.innerHTML = ''; wrap.append(table);
      const order = tot.map((t, i) => [t, S.options[i]]).sort((a, b) => b[0] - a[0]);
      if (order.length < 2) verdict.textContent = 'Add a second option to compare.';
      else { const gap = order[0][0] - order[1][0]; verdict.textContent = gap < 0.5 ? order[0][1] + ' and ' + order[1][1] + ' are within ' + gap.toFixed(2) + ' points. Treat that as a tie and decide on the criterion you weighted highest.' : order[0][1] + ' leads ' + order[1][1] + ' by ' + gap.toFixed(2) + ' points out of 10. Change one weight and see whether the lead survives before you commit.'; }
    }
    draw();
  };

  /* 6 time-block planner */
  T.blocks = function (box) {
    const kinds = [['deep', 'Deep work'], ['shallow', 'Shallow work'], ['meet', 'Meetings'], ['break', 'Break'], ['', 'Erase']];
    const all = MW.get('blocks', {}), day = MW.today(); let S = all[day] || { from: 8, to: 18, slots: {} }, brush = 'deep';
    const legend = el('div', { class: 'legend' }), label = el('input', { type: 'text', placeholder: 'Label for the blocks you paint (optional)', 'aria-label': 'Block label', maxlength: '60', style: 'font:inherit;padding:8px 10px;border:1.5px solid var(--ink-2);border-radius:6px;flex:1;min-width:200px;background:var(--surface);color:var(--ink)' });
    kinds.forEach(k => legend.append(el('button', { class: 'chip', type: 'button', text: k[1], 'aria-pressed': String(k[0] === brush), onclick: e => { brush = k[0]; legend.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === e.target))); } })));
    const hours = (v, id) => { const s = el('select', { 'aria-label': id, style: 'font:inherit;padding:8px;border-radius:6px' }); for (let h = 5; h <= 23; h++) { const o = el('option', { value: h, text: ('0' + h).slice(-2) + ':00' }); if (h === v) o.selected = true; s.append(o); } return s; };
    const from = hours(S.from, 'Day starts'), to = hours(S.to, 'Day ends');
    from.addEventListener('change', () => { S.from = Math.min(parseInt(from.value, 10), S.to - 1); from.value = S.from; save(); }); to.addEventListener('change', () => { S.to = Math.max(parseInt(to.value, 10), S.from + 1); to.value = S.to; save(); });
    const grid = el('div', { class: 'blocks' }), sum = el('p', { class: 'note focus', style: 'margin-top:14px' });
    box.append(el('div', { class: 'btn-row', style: 'margin-bottom:10px' }, 'Day runs from', from, 'to', to), legend, el('div', { class: 'btn-row', style: 'margin-top:10px' }, label), grid, sum,
      el('div', { class: 'btn-row no-print', style: 'margin-top:12px' }, el('button', { class: 'btn small', type: 'button', text: 'Print today’s plan', onclick: () => window.print() }), el('button', { class: 'btn ghost small', type: 'button', text: 'Clear the day', onclick: () => { S.slots = {}; save(); } })));
    function save() { all[day] = S; const keys = Object.keys(all).sort(); while (keys.length > 14) delete all[keys.shift()]; MW.set('blocks', all); draw(); }
    function draw() {
      grid.innerHTML = ''; const tally = {};
      for (let m = S.from * 60; m < S.to * 60; m += 30) {
        const key = String(m), slot = S.slots[key], t = ('0' + Math.floor(m / 60)).slice(-2) + ':' + (m % 60 ? '30' : '00'), name = slot ? (slot.l || (kinds.find(k => k[0] === slot.k) || ['', ''])[1]) : '';
        if (slot) tally[slot.k] = (tally[slot.k] || 0) + 0.5;
        const b = el('button', { type: 'button', 'data-k': slot ? slot.k : '', text: name, 'aria-label': t + (name ? ': ' + name : ': empty') });
        b.addEventListener('click', () => { if (!brush) delete S.slots[key]; else S.slots[key] = { k: brush, l: label.value.trim() }; save(); });
        grid.append(el('time', { text: t }), b);
      }
      const parts = kinds.filter(k => k[0] && tally[k[0]]).map(k => tally[k[0]] + ' h ' + k[1].toLowerCase());
      sum.textContent = parts.length ? 'Planned: ' + parts.join(', ') + '.' + ((tally.deep || 0) > 4 ? ' More than four hours of deep work in a day is rare. Protect the first two blocks and treat the rest as a bonus.' : '') : 'Pick a block type, then click half-hour slots to paint your day. Start with one or two deep-work blocks.';
    }
    draw();
  };

  MW.mountTool = function (id) { const box = document.getElementById('tool'); if (box && T[id]) T[id](box); };
})();
