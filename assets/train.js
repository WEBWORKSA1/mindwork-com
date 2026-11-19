/* MindWork.com — the nine tests. Each test is G[id](stage, done, opts) and calls done(value, extraRows, flags). */
(function () {
  'use strict';
  const MW = window.MW, el = MW.el, G = {};

  const BANDS = {
    reaction: [[200, 'Exceptional', 'Faster than most people manage with a mouse or touchscreen. See if it holds over a few runs.'], [250, 'Fast', 'Quicker than the usual range for a simple click test.'], [300, 'Typical', 'Inside the usual range for a visual reaction test on everyday hardware.'], [400, 'On the slow side', 'Screen lag, a touchpad or a tired afternoon can each add 30 to 80 ms. Try again with a mouse.'], [Infinity, 'Slow run', 'This usually reflects distraction or fatigue, not ability. Run it again when you are alert.']],
    number: [[12, 'Exceptional', 'Well beyond ordinary digit span. You are almost certainly chunking the digits.'], [9, 'Strong', 'Above the classic seven-plus-or-minus-two range.'], [6, 'Typical', 'Inside the classic range reported for adult digit span.'], [0, 'Below the usual range', 'Group the digits in threes or fours, say them in rhythm, then try again.']],
    sequence: [[13, 'Exceptional', 'Long spatial sequences like this usually mean you are turning tiles into a route or a shape.'], [9, 'Strong', 'Comfortably above where most first runs end.'], [5, 'Typical', 'Most first attempts end between five and eight steps.'], [0, 'Early exit', 'One slip ends the run. Trace the tiles as a path (corner, middle, corner) and go again.']],
    visual: [[13, 'Exceptional', 'You are holding large patterns as whole shapes, which is exactly the skill this test rewards.'], [10, 'Strong', 'Above where most runs end.'], [6, 'Typical', 'A normal result. Patterns get hard fast once the grid grows.'], [0, 'Early exit', 'Look for shapes (an L, a diagonal, a block) instead of single tiles.']],
    stroop: [[40, 'Minimal interference', 'The clashing words barely slowed you. Check your matching-trial time: a slow, careful pace also shrinks this number.'], [130, 'Typical interference', 'A clear, ordinary Stroop effect. Reading is automatic, so the word gets in the way of the colour.'], [Infinity, 'Strong interference', 'The words slowed you a lot on this run. Fatigue and divided attention both inflate this number.']],
    nback: [[85, 'Exceptional', 'Near-perfect updating at 2-back. Try the 3-back practice round.'], [65, 'Strong', 'You are tracking most targets with few false alarms.'], [35, 'Typical', 'A solid early result. Most people find 2-back hard at the start.'], [0, 'Finding your feet', 'Say each letter under your breath and compare it with the one two steps back.']],
    math: [[30, 'Exceptional', 'About two seconds per answer, including typing.'], [20, 'Fast', 'Quick recall with few stalls.'], [10, 'Typical', 'A normal pace. Times tables are usually where the seconds go.'], [0, 'Warm-up pace', 'Skip faster when a sum stalls you. Speed comes back quickly with a few runs.']],
    verbal: [[60, 'Exceptional', 'You are keeping dozens of words apart from their look-alikes.'], [35, 'Strong', 'Well past where most runs end.'], [15, 'Typical', 'A normal result. Errors pile up once thirty or so words are in play.'], [0, 'Early exit', 'Give each new word a quick picture in your head before you answer.']],
    schulte: [[25, 'Exceptional', 'About a second per number. You are finding targets with peripheral vision.'], [35, 'Fast', 'Quicker than most first attempts.'], [50, 'Typical', 'A normal time for a five-by-five table.'], [Infinity, 'Slow run', 'Fix your eyes on the centre tile and let the numbers come to you.']]
  };
  const INTRO = {
    reaction: ['Reaction time', 'The pad turns green after a random delay. Click, tap or press Space as fast as you can. Five trials, averaged.'],
    number: ['Number memory', 'A number appears for a few seconds. Type it back. Each correct answer adds a digit.'],
    sequence: ['Sequence memory', 'Tiles light up in order. Repeat the order. Each round adds one step; one mistake ends the run.'],
    visual: ['Visual memory', 'Some tiles flash. Click the same tiles from memory. Three misses in a round costs one of your three lives.'],
    stroop: ['Stroop test', 'A colour word appears in coloured ink. Choose the ink colour, not the word. 24 trials; use the buttons or keys 1 to 4.'],
    nback: ['2-back', 'Letters appear one at a time. Press Match whenever the letter is the same as the one two steps earlier.'],
    math: ['Mental math sprint', 'Answer as many sums as you can in 60 seconds. The next sum appears the instant your answer is right.'],
    verbal: ['Verbal memory', 'Words appear one at a time. Say whether you have already seen each word in this round. Three lives.'],
    schulte: ['Schulte table', 'Click the numbers 1 to 25 in order as fast as you can. The clock starts when the grid appears.']
  };
  const WORDS = 'anchor,basket,candle,desert,engine,forest,garden,harbor,island,jacket,kettle,ladder,market,needle,orange,pencil,quartz,ribbon,saddle,tunnel,umpire,valley,window,yogurt,zipper,bridge,copper,dragon,empire,falcon,glacier,hammer,insect,jungle,kernel,lantern,magnet,napkin,oyster,pillow,rocket,silver,temple,violin,walnut,canyon,marble,pepper,thread,velvet,bucket,camera,dinner,fabric,guitar,helmet,journal,kitten,lemon,mirror,number,office,planet,rabbit,school,ticket,vessel,winter,branch,cotton,dollar,flower,goblet,hunter,lizard,meadow,parcel,stream,turtle,wallet,button,castle,donkey,feather,gravel,hollow,jigsaw,locket,mitten,pebble,quiver,shovel,trophy,wizard,blanket,compass,dolphin,lantern,mustard,pumpkin,sparrow,whistle,biscuit,chimney,diamond,harvest,leather,penguin,sandals,trumpet'.split(',');

  function band(id, v) { const b = BANDS[id], low = MW.META[id].low; for (let i = 0; i < b.length; i++) { if (low ? v < b[i][0] : v >= b[i][0]) return b[i]; } return b[b.length - 1]; }
  function hud(a, b) { return el('div', { class: 'hud' }, el('span', { text: a }), el('span', { text: b })); }
  function kbtn(label, key, fn) { const b = el('button', { class: 'btn ghost', type: 'button' }, label, el('span', { class: 'kbd', text: key })); b.addEventListener('click', fn); return b; }
  const mean = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0;
  const lives = n => 'Lives ' + '●'.repeat(Math.max(0, n)) + '○'.repeat(3 - Math.max(0, n));

  /* 1 reaction time */
  G.reaction = function (stage, done, opts) {
    const trials = (opts && opts.trials) || 5, times = []; let t0 = 0, timer = null, state = 'idle';
    const big = el('div', { class: 'big' }), msg = el('div', { class: 'msg' }), sub = el('div', { class: 'sub' }), tr = el('div', { class: 'trials' });
    const pad = el('div', { class: 'pad', role: 'button', tabindex: '0', 'aria-live': 'polite' }, big, msg, sub, tr);
    stage.appendChild(pad);
    function set(s, b, m, u) { state = s; pad.setAttribute('data-s', s); big.textContent = b || ''; msg.textContent = m || ''; sub.textContent = u || ''; tr.textContent = times.length ? times.length + ' of ' + trials + ' trials: ' + times.join(', ') + ' ms' : ''; }
    function arm() { set('wait', '', 'Wait for green', 'Click the moment the colour changes.'); timer = setTimeout(function () { t0 = performance.now(); set('go', '', 'Click now', ''); }, 1500 + Math.random() * 3000); }
    function hit(e) {
      if (e && e.target && e.target.closest && e.target.closest('a,button')) return;
      if (state === 'idle' || state === 'shown' || state === 'early') return arm();
      if (state === 'wait') { clearTimeout(timer); return set('early', '', 'Too soon', 'Click to run that trial again.'); }
      if (state === 'go') {
        times.push(Math.round(performance.now() - t0));
        if (times.length >= trials) {
          off(); const avg = Math.round(mean(times));
          set('done', String(avg), 'ms average', '');
          done(avg, [['Trials', times.join(', ') + ' ms'], ['Fastest', Math.min.apply(null, times) + ' ms']]);
        } else set('shown', String(times[times.length - 1]), 'ms', 'Click to start trial ' + (times.length + 1) + '.');
      }
    }
    function key(e) { if ((e.code === 'Space' || e.code === 'Enter') && !/INPUT|TEXTAREA|SELECT|BUTTON|A/.test(e.target.tagName)) { e.preventDefault(); hit(); } }
    function off() { pad.removeEventListener('pointerdown', hit); document.removeEventListener('keydown', key); }
    pad.addEventListener('pointerdown', hit); document.addEventListener('keydown', key);
    set('idle', '', 'Click to start', 'When the pad turns green, click as fast as you can. ' + trials + ' trials.');
  };

  /* 2 number memory */
  G.number = function (stage, done) {
    let L = 3;
    function show() {
      stage.innerHTML = ''; let n = '';
      for (let i = 0; i < L; i++) n += String(i === 0 ? 1 + Math.floor(Math.random() * 9) : Math.floor(Math.random() * 10));
      const ms = 900 + L * 550, r = el('div', { class: 'readout', text: n }), fill = el('i'), bar = el('div', { class: 'bar' }, fill);
      if (L > 9) r.style.fontSize = 'clamp(1.7rem,6.5vw,3.4rem)';
      stage.append(hud('Level ' + (L - 2), L + ' digits'), r, bar);
      fill.style.transition = 'width ' + ms + 'ms linear';
      requestAnimationFrame(() => requestAnimationFrame(() => { fill.style.width = '0%'; }));
      setTimeout(() => ask(n), ms);
    }
    function ask(n) {
      stage.innerHTML = '';
      const inp = el('input', { type: 'text', inputmode: 'numeric', autocomplete: 'off', 'aria-label': 'Type the number you saw' });
      const form = el('form', {}, el('p', { class: 'muted', text: 'What was the number?' }), inp, el('div', { class: 'btn-row', style: 'justify-content:center;margin-top:14px' }, el('button', { class: 'btn', type: 'submit', text: 'Check answer' })));
      form.addEventListener('submit', function (e) {
        e.preventDefault(); const a = inp.value.replace(/\D/g, ''); if (!a) return;
        if (a === n) { L++; stage.innerHTML = ''; stage.append(el('h3', { text: 'Correct' }), el('p', { class: 'muted', text: 'Next: ' + L + ' digits' })); setTimeout(show, 800); }
        else {
          stage.innerHTML = '';
          stage.append(el('h3', { text: 'Not quite' }), el('p', {}, 'The number was ', el('b', { text: n })), el('p', {}, 'You typed ', el('b', { text: a })));
          done(L - 1, [['Missed at', L + ' digits']]);
        }
      });
      stage.append(hud('Level ' + (L - 2), L + ' digits'), form); inp.focus();
    }
    show();
  };

  /* 3 sequence memory */
  G.sequence = function (stage, done) {
    const seq = [], cells = []; let pos = 0, lock = true;
    stage.innerHTML = ''; const h = hud('Level 1', ''), g = el('div', { class: 'grid-g', style: 'grid-template-columns:repeat(3,1fr)' }), tip = el('p', { class: 'muted', text: 'Watch the pattern.' });
    for (let i = 0; i < 9; i++) { const c = el('button', { class: 'cell', type: 'button', 'aria-label': 'Tile ' + (i + 1) }); c.addEventListener('click', () => press(i)); cells.push(c); g.appendChild(c); }
    stage.append(h, g, tip);
    function next() {
      seq.push(Math.floor(Math.random() * 9)); pos = 0; lock = true; h.firstChild.textContent = 'Level ' + seq.length; tip.textContent = 'Watch the pattern.'; let i = 0;
      (function step() { if (i >= seq.length) { lock = false; tip.textContent = 'Your turn. Repeat it.'; return; } const c = cells[seq[i]]; c.classList.add('lit'); setTimeout(() => { c.classList.remove('lit'); i++; setTimeout(step, 180); }, 420); })();
    }
    function press(i) {
      if (lock) return; const c = cells[i];
      if (i === seq[pos]) { c.classList.add('ok'); setTimeout(() => c.classList.remove('ok'), 160); pos++; if (pos === seq.length) { lock = true; setTimeout(next, 650); } }
      else { lock = true; c.classList.add('bad'); cells[seq[pos]].classList.add('lit'); tip.textContent = 'Wrong tile. The lit tile was next.'; done(seq.length - 1, [['Missed at', 'step ' + (pos + 1) + ' of ' + seq.length]]); }
    }
    setTimeout(next, 600);
  };

  /* 4 visual memory */
  G.visual = function (stage, done) {
    let n = 3, left = 3, lock = true, target = new Set(), found = 0, miss = 0, cells = [];
    stage.innerHTML = ''; const h = hud('', ''), g = el('div', { class: 'grid-g' }), tip = el('p', { class: 'muted' }); stage.append(h, g, tip);
    const size = () => (n < 5 ? 3 : n < 8 ? 4 : n < 12 ? 5 : n < 17 ? 6 : 7);
    const head = () => { h.firstChild.textContent = n + ' tiles'; h.lastChild.textContent = lives(left); };
    function round() {
      lock = true; found = 0; miss = 0; const s = size(); g.innerHTML = ''; g.style.gridTemplateColumns = 'repeat(' + s + ',1fr)'; cells = [];
      const idx = MW.shuffle(Array.from({ length: s * s }, (_, i) => i)).slice(0, n); target = new Set(idx);
      for (let i = 0; i < s * s; i++) { const c = el('button', { class: 'cell', type: 'button', 'aria-label': 'Tile ' + (i + 1) }); c.addEventListener('click', () => press(i, c)); cells.push(c); g.appendChild(c); }
      head(); tip.textContent = 'Memorise the lit tiles.'; idx.forEach(i => cells[i].classList.add('lit'));
      setTimeout(() => { idx.forEach(i => cells[i].classList.remove('lit')); lock = false; tip.textContent = 'Click the ' + n + ' tiles that were lit.'; }, 1100 + n * 90);
    }
    function press(i, c) {
      if (lock || c.classList.contains('ok') || c.classList.contains('bad')) return;
      if (target.has(i)) { c.classList.add('ok'); found++; if (found === n) { lock = true; n++; setTimeout(round, 600); } return; }
      c.classList.add('bad'); miss++;
      if (miss >= 3) {
        lock = true; left--; head(); target.forEach(t => { if (!cells[t].classList.contains('ok')) cells[t].classList.add('lit'); });
        if (left <= 0) { tip.textContent = 'Out of lives.'; done(n - 1, [['Reached', n + ' tiles']]); }
        else { tip.textContent = 'Three misses: one life lost. Same level again.'; setTimeout(round, 1500); }
      }
    }
    round();
  };

  /* 5 stroop */
  G.stroop = function (stage, done) {
    const C = [['Red', '#E5484D'], ['Blue', '#2F6BFF'], ['Green', '#1FA971'], ['Yellow', '#D9A400']];
    let trials = []; for (let i = 0; i < 12; i++) { const w = i % 4; trials.push([w, w]); trials.push([w, (w + 1 + Math.floor(Math.random() * 3)) % 4]); }
    trials = MW.shuffle(trials); let t = 0, t0 = 0, open = false; const rec = [];
    stage.innerHTML = ''; const h = hud('', ''), word = el('div', { class: 'stroop-word', text: '+' }), keys = el('div', { class: 'keys' });
    C.forEach((c, i) => keys.appendChild(kbtn(c[0], String(i + 1), () => answer(i))));
    stage.append(h, el('p', { class: 'muted', text: 'Pick the colour of the ink, not the word.' }), word, keys);
    function show() {
      if (t >= trials.length) return end();
      h.firstChild.textContent = 'Trial ' + (t + 1) + ' of ' + trials.length; word.textContent = '+'; word.style.color = 'inherit'; open = false;
      setTimeout(() => { word.textContent = C[trials[t][0]][0].toUpperCase(); word.style.color = C[trials[t][1]][1]; t0 = performance.now(); open = true; }, 450);
    }
    function answer(i) { if (!open) return; open = false; rec.push({ cong: trials[t][0] === trials[t][1], ok: i === trials[t][1], rt: performance.now() - t0 }); t++; show(); }
    function key(e) { const i = ['1', '2', '3', '4'].indexOf(e.key); if (i >= 0) answer(i); }
    function end() {
      document.removeEventListener('keydown', key);
      const c = rec.filter(r => r.cong && r.ok).map(r => r.rt), ic = rec.filter(r => !r.cong && r.ok).map(r => r.rt), acc = Math.round(rec.filter(r => r.ok).length / rec.length * 100);
      const inter = Math.max(0, Math.round(mean(ic) - mean(c)));
      word.textContent = 'Done'; word.style.color = 'inherit'; keys.remove();
      const extra = [['Matching trials', Math.round(mean(c)) + ' ms'], ['Clashing trials', Math.round(mean(ic)) + ' ms'], ['Accuracy', acc + '%']];
      if (acc < 75 || !c.length || !ic.length) done(inter, extra, { nosave: true, label: 'Accuracy too low to score', note: 'Below 75% correct, the speed difference stops meaning much. Slow down slightly and run it again.' });
      else done(inter, extra);
    }
    document.addEventListener('keydown', key); show();
  };

  /* 6 n-back */
  G.nback = function (stage, done, opts) {
    const N = (opts && opts.n) || 2, L = 'BCDFGHJKLMNPQRSTVWXZ', len = 20 + N, seq = [];
    for (let i = 0; i < len; i++) { if (i >= N && Math.random() < 0.32) seq.push(seq[i - N]); else { let c; do { c = L[Math.floor(Math.random() * L.length)]; } while (i >= N && c === seq[i - N]); seq.push(c); } }
    let i = -1, pressed = false, hits = 0, miss = 0, fa = 0;
    stage.innerHTML = ''; const h = hud('', N + '-back'), letter = el('div', { class: 'readout', text: '' }), fb = el('p', { class: 'muted', html: '&nbsp;' });
    const btn = kbtn('Match', 'Space', press); btn.className = 'btn';
    stage.append(h, letter, fb, btn);
    const isT = k => k >= N && seq[k] === seq[k - N];
    function tick() {
      if (i >= N) { if (isT(i)) { if (pressed) hits++; else miss++; } else if (pressed) fa++; }
      i++; if (i >= len) return end();
      pressed = false; h.firstChild.textContent = (i + 1) + ' of ' + len; letter.textContent = seq[i]; letter.style.opacity = 1; fb.innerHTML = '&nbsp;';
      setTimeout(() => { letter.style.opacity = 0.12; }, 1500); setTimeout(tick, 2200);
    }
    function press() { if (i < 0 || pressed || i >= len) return; pressed = true; fb.textContent = i < N ? 'Too early to match' : (isT(i) ? 'Match' : 'No match'); }
    function key(e) { if (e.code === 'Space' || e.key === 'm' || e.key === 'M') { e.preventDefault(); press(); } }
    function end() {
      document.removeEventListener('keydown', key); btn.remove(); letter.textContent = 'Done'; letter.style.opacity = 1; fb.innerHTML = '&nbsp;';
      const T = hits + miss, NT = len - N - T, v = Math.max(0, Math.round((hits / Math.max(1, T) - fa / Math.max(1, NT)) * 100));
      const extra = [['Hits', hits + ' of ' + T], ['False alarms', String(fa)], ['Level', N + '-back']];
      if (N !== 2) done(v, extra, { nosave: true, label: N + '-back practice round', note: 'Only the 2-back is saved to your dashboard, so scores stay comparable.' }); else done(v, extra);
    }
    document.addEventListener('keydown', key); setTimeout(tick, 700);
  };

  /* 7 mental math */
  G.math = function (stage, done) {
    let correct = 0, skipped = 0, ans = 0, left = 60;
    stage.innerHTML = ''; const h = hud('0 correct', '60 s'), q = el('div', { class: 'readout', text: '' }), inp = el('input', { type: 'text', inputmode: 'numeric', autocomplete: 'off', 'aria-label': 'Your answer' });
    const skip = el('button', { class: 'btn ghost small', type: 'button', text: 'Skip this sum' });
    stage.append(h, q, el('div', { style: 'margin:16px 0 12px' }, inp), skip);
    const r = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
    function gen() {
      const lvl = Math.min(3, Math.floor(correct / 6)), op = ['+', '−', '×'][r(0, 2)]; let a, b;
      if (op === '×') { a = r(2, 6 + lvl * 2); b = r(2, 9 + lvl); ans = a * b; } else if (op === '+') { a = r(5, 30 + lvl * 25); b = r(5, 30 + lvl * 25); ans = a + b; } else { a = r(10, 40 + lvl * 25); b = r(2, a); ans = a - b; }
      q.textContent = a + ' ' + op + ' ' + b; inp.value = ''; inp.focus();
    }
    inp.addEventListener('input', () => { if (inp.value.trim() !== '' && parseInt(inp.value.replace(/[^\d]/g, ''), 10) === ans) { correct++; h.firstChild.textContent = correct + ' correct'; gen(); } });
    skip.addEventListener('click', () => { skipped++; gen(); });
    const iv = setInterval(() => {
      left--; h.lastChild.textContent = left + ' s';
      if (left <= 0) { clearInterval(iv); inp.disabled = true; skip.remove(); q.textContent = 'Time'; done(correct, [['Skipped', String(skipped)], ['Pace', (correct ? (60 / correct).toFixed(1) : '–') + ' s per answer']]); }
    }, 1000);
    gen();
  };

  /* 8 verbal memory */
  G.verbal = function (stage, done) {
    const pool = MW.shuffle(Array.from(new Set(WORDS))), seen = []; let score = 0, left = 3, cur = '', isSeen = false, p = 0;
    stage.innerHTML = ''; const h = hud('Score 0', ''), w = el('div', { class: 'readout', text: '', style: 'font-stretch:100%;font-size:clamp(2.2rem,8vw,4rem)' }), keys = el('div', { class: 'keys' });
    keys.append(kbtn('Seen', 'S', () => ans(true)), kbtn('New', 'N', () => ans(false)));
    stage.append(h, w, el('p', { class: 'muted', text: 'Have you seen this word in this round?' }), keys);
    function next() {
      h.firstChild.textContent = 'Score ' + score; h.lastChild.textContent = lives(left);
      if (left <= 0) return end();
      isSeen = (seen.length > 1 && Math.random() < 0.45) || p >= pool.length;
      if (isSeen) { let c; do { c = seen[Math.floor(Math.random() * seen.length)]; } while (c === cur && seen.length > 1); cur = c; } else cur = pool[p++];
      w.textContent = cur;
    }
    function ans(a) { if (left <= 0) return; if (a === isSeen) score++; else left--; if (!isSeen) seen.push(cur); next(); }
    function key(e) { if (e.key === 's' || e.key === 'S') ans(true); else if (e.key === 'n' || e.key === 'N') ans(false); }
    function end() { document.removeEventListener('keydown', key); keys.remove(); w.textContent = 'Out of lives'; done(score, [['Words in play', String(seen.length)]]); }
    document.addEventListener('keydown', key); next();
  };

  /* 9 schulte table */
  G.schulte = function (stage, done) {
    const nums = MW.shuffle(Array.from({ length: 25 }, (_, i) => i + 1)); let next = 1, errors = 0;
    stage.innerHTML = ''; const h = hud('Find 1', '0.0 s'), g = el('div', { class: 'grid-g', style: 'grid-template-columns:repeat(5,1fr);width:min(400px,100%)' });
    const t0 = performance.now(), iv = setInterval(() => { h.lastChild.textContent = ((performance.now() - t0) / 1000).toFixed(1) + ' s'; }, 100);
    nums.forEach(n => {
      const c = el('button', { class: 'cell', type: 'button', text: String(n) });
      c.addEventListener('click', () => {
        if (n !== next) { errors++; c.classList.add('bad'); setTimeout(() => c.classList.remove('bad'), 220); return; }
        c.classList.add('gone'); c.disabled = true; next++;
        if (next > 25) { clearInterval(iv); const s = Math.round((performance.now() - t0) / 100) / 10; h.lastChild.textContent = s.toFixed(1) + ' s'; h.firstChild.textContent = 'Done'; done(s, [['Wrong clicks', String(errors)]]); }
        else h.firstChild.textContent = 'Find ' + next;
      });
      g.appendChild(c);
    });
    stage.append(h, g, el('p', { class: 'muted', text: 'Keep your eyes on the centre and find the numbers with your peripheral vision.' }));
  };

  /* ---------- page wiring ---------- */
  MW.mountGame = function (id) {
    const stage = document.getElementById('stage'), result = document.getElementById('result'), m = MW.META[id];
    let opts = {};
    function intro() {
      stage.innerHTML = ''; result.hidden = true;
      stage.append(el('h3', { text: INTRO[id][0] }), el('p', { class: 'muted', style: 'max-width:34em', text: INTRO[id][1] }));
      if (id === 'nback') {
        const sel = el('select', { 'aria-label': 'Level', style: 'font:inherit;padding:8px 10px;margin-bottom:14px;border-radius:6px' }, el('option', { value: '1', text: '1-back (practice)' }), el('option', { value: '2', text: '2-back (scored)', selected: '' }), el('option', { value: '3', text: '3-back (practice)' }));
        sel.addEventListener('change', () => { opts.n = parseInt(sel.value, 10); }); stage.append(sel);
      }
      const s = MW.scores()[id];
      stage.append(el('button', { class: 'btn', type: 'button', text: 'Start the test', onclick: start }));
      if (s && s.best != null) stage.append(el('p', { class: 'muted', style: 'margin-top:12px', text: 'Your best: ' + s.best + ' ' + m.unit + ' over ' + s.n + (s.n === 1 ? ' attempt' : ' attempts') }));
    }
    function start() { stage.innerHTML = ''; result.hidden = true; G[id](stage, finish, opts); stage.scrollIntoView({ block: 'nearest' }); }
    function finish(v, extra, flags) {
      flags = flags || {}; const b = band(id, v), saved = flags.nosave ? null : MW.save(id, v);
      result.hidden = false; result.innerHTML = '';
      result.append(el('div', { class: 'score' }, String(v), el('small', { text: m.unit })));
      const right = el('div', {}, el('p', { class: 'band', text: flags.label || b[1] + (saved && saved.isBest ? '. New personal best' : '') }), el('p', { class: 'muted', style: 'margin:0', text: flags.note || b[2] }));
      const dl = el('dl');
      const rows = (extra || []).slice();
      if (saved) { rows.push(['Personal best', saved.best + ' ' + m.unit], ['Attempts', String(saved.n)], ['Result code', MW.code(id, v)]); }
      rows.forEach(r => dl.append(el('div', {}, el('dt', { text: r[0] }), el('dd', { text: r[1] }))));
      right.append(dl); result.append(right);
      const nextId = MW.ORDER[(MW.ORDER.indexOf(id) + 1) % MW.ORDER.length], row = el('div', { class: 'btn-row' });
      row.append(el('button', { class: 'btn', type: 'button', text: 'Run it again', onclick: start }));
      if (MW.daily.picks().indexOf(id) >= 0) row.append(el('a', { class: 'btn ghost', href: MW.root + 'daily.html', text: 'Back to today’s workout' }));
      row.append(el('a', { class: 'btn ghost', href: MW.root + MW.META[nextId].url, text: 'Next test: ' + MW.META[nextId].name }));
      const sh = el('button', { class: 'btn ghost', type: 'button', text: 'Share this result' });
      sh.addEventListener('click', () => MW.share('I scored ' + v + ' ' + m.unit + ' on the ' + m.name + ' test at MindWork.com.', sh));
      row.append(sh, el('a', { href: MW.root + 'dashboard.html', text: 'See all your scores' }));
      result.append(row); result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    intro();
  };

  MW.heroPad = function (box) {
    function run() {
      box.innerHTML = '';
      G.reaction(box, function (avg) {
        const sub = box.querySelector('.sub'); sub.textContent = '';
        sub.append('A three-trial warm-up. ', el('a', { href: MW.root + 'train/reaction-time.html', style: 'color:#fff;font-weight:700', text: 'Take the full test to save a score' }), '.', el('br'));
        sub.append(el('button', { class: 'btn small', type: 'button', style: 'margin-top:12px;background:#fff;color:#14213D;border-color:#fff', text: 'Run the warm-up again', onclick: run }));
      }, { trials: 3 });
    }
    run();
  };
  MW.G = G;
})();
