/* MindWork.com — shared behaviour: storage, scores, daily picks, forms, consent, ads, video embeds */
(function () {
  'use strict';
  var CFG = window.MW_CONFIG || {};
  var root = document.documentElement.getAttribute('data-root') || '';
  var MW = (window.MW = { root: root, cfg: CFG });

  /* ---------- storage ---------- */
  MW.get = function (k, d) { try { var v = localStorage.getItem('mw.' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } };
  MW.set = function (k, v) { try { localStorage.setItem('mw.' + k, JSON.stringify(v)); } catch (e) {} };
  MW.today = function (d) { d = d || new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); };
  MW.el = function (tag, attrs) {
    var n = document.createElement(tag), i, k;
    for (k in attrs || {}) {
      if (k === 'text') n.textContent = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else if (k.slice(0, 2) === 'on') n.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== false && attrs[k] != null) n.setAttribute(k, attrs[k]);
    }
    for (i = 2; i < arguments.length; i++) { var c = arguments[i]; if (c == null) continue; n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); }
    return n;
  };
  MW.rng = function (seed) { var a = seed >>> 0; return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  MW.shuffle = function (arr, rnd) { rnd = rnd || Math.random; var a = arr.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; };

  /* ---------- tests: metadata shared by results, dashboard, daily workout ---------- */
  MW.META = {
    reaction: { name: 'Reaction time', unit: 'ms', low: true, worst: 450, best: 180, url: 'train/reaction-time.html' },
    number: { name: 'Number memory', unit: 'digits', worst: 3, best: 13, url: 'train/number-memory.html' },
    sequence: { name: 'Sequence memory', unit: 'steps', worst: 2, best: 14, url: 'train/sequence-memory.html' },
    visual: { name: 'Visual memory', unit: 'tiles', worst: 3, best: 14, url: 'train/visual-memory.html' },
    stroop: { name: 'Stroop test', unit: 'ms', low: true, worst: 300, best: 0, url: 'train/stroop-test.html' },
    nback: { name: '2-back', unit: 'pts', worst: 0, best: 100, url: 'train/n-back.html' },
    math: { name: 'Mental math', unit: 'correct', worst: 0, best: 35, url: 'train/mental-math.html' },
    verbal: { name: 'Verbal memory', unit: 'words', worst: 0, best: 60, url: 'train/verbal-memory.html' },
    schulte: { name: 'Schulte table', unit: 's', low: true, worst: 70, best: 18, url: 'train/schulte-table.html' }
  };
  MW.ORDER = ['reaction', 'number', 'sequence', 'visual', 'stroop', 'nback', 'math', 'verbal', 'schulte'];
  MW.pct = function (id, v) { var m = MW.META[id]; var p = (v - m.worst) / (m.best - m.worst) * 100; return Math.max(0, Math.min(100, Math.round(p))); };
  MW.scores = function () { return MW.get('scores', {}); };
  MW.save = function (id, v) {
    var all = MW.scores(), s = all[id] || { n: 0, hist: [] }, m = MW.META[id];
    var better = s.best == null || (m.low ? v < s.best : v > s.best);
    s.n += 1; s.last = v; if (better) s.best = v;
    s.hist.push([Date.now(), v]); if (s.hist.length > 40) s.hist.shift();
    all[id] = s; MW.set('scores', all);
    MW.daily.mark(id);
    return { best: s.best, isBest: better && s.n > 1, n: s.n, first: s.n === 1 };
  };
  MW.composite = function () {
    var all = MW.scores(), sum = 0, n = 0;
    MW.ORDER.forEach(function (id) { if (all[id] && all[id].best != null) { sum += MW.pct(id, all[id].best); n++; } });
    return { score: n ? Math.round(sum / n) : null, done: n, total: MW.ORDER.length };
  };
  MW.code = function (id, v) {
    var day = Math.floor(Date.now() / 864e5), i = MW.ORDER.indexOf(id), s = Math.round(v * 10);
    var chk = (s * 7 + day * 13 + (i + 1) * 31) % 1295;
    return (id.slice(0, 2) + s.toString(36) + '-' + day.toString(36) + '-' + chk.toString(36)).toUpperCase();
  };
  MW.share = function (text, btn) {
    var url = location.href.split('?')[0].split('#')[0];
    if (navigator.share) { navigator.share({ text: text, url: url }).catch(function () {}); return; }
    var done = function () { if (btn) { var t = btn.textContent; btn.textContent = 'Copied to clipboard'; setTimeout(function () { btn.textContent = t; }, 1800); } };
    if (navigator.clipboard) navigator.clipboard.writeText(text + ' ' + url).then(done, function () {});
  };

  /* ---------- daily workout + streak ---------- */
  MW.daily = {
    picks: function (dateStr) {
      dateStr = dateStr || MW.today();
      var seed = parseInt(dateStr.replace(/-/g, ''), 10);
      return MW.shuffle(MW.ORDER, MW.rng(seed)).slice(0, 3);
    },
    state: function () { var s = MW.get('daily', {}); if (s.date !== MW.today()) s = { date: MW.today(), done: [] }; return s; },
    mark: function (id) {
      var s = MW.daily.state(), picks = MW.daily.picks();
      if (picks.indexOf(id) < 0 || s.done.indexOf(id) >= 0) return;
      s.done.push(id); MW.set('daily', s);
      if (s.done.length === picks.length) {
        var st = MW.get('streak', { count: 0, best: 0, days: [] });
        if (st.last !== s.date) {
          var y = new Date(); y.setDate(y.getDate() - 1);
          st.count = st.last === MW.today(y) ? st.count + 1 : 1;
          st.best = Math.max(st.best || 0, st.count); st.last = s.date;
          st.days = (st.days || []).concat(s.date).slice(-60);
          MW.set('streak', st);
        }
      }
    },
    streak: function () {
      var st = MW.get('streak', { count: 0, best: 0, days: [] });
      var y = new Date(); y.setDate(y.getDate() - 1);
      if (st.last !== MW.today() && st.last !== MW.today(y)) st.count = 0;
      return st;
    }
  };

  /* ---------- forms: every form on the site posts to one inbox through a relay ---------- */
  var K = [124,119,110,100,98,102,101,102,110,39,80,112,124,106,123,96,61,110,123,99];
  function inbox() {
    if (CFG.formToken) return CFG.formToken;
    return K.map(function (c, i) { return String.fromCharCode(c ^ (11 + (i * 7) % 13)); }).join('');
  }
  MW.send = function (data) {
    return fetch('https://formsubmit.co/ajax/' + encodeURIComponent(inbox()), {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data)
    }).then(function (r) { if (!r.ok) throw new Error('relay ' + r.status); return r.json().catch(function () { return {}; }); });
  };
  function wireForm(form) {
    var status = form.querySelector('.form-status') || form.appendChild(MW.el('p', { class: 'form-status', role: 'status', 'aria-live': 'polite' }));
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var fd = new FormData(form), data = {}, btn = form.querySelector('button[type=submit]');
      fd.forEach(function (v, k) { data[k] = data[k] ? data[k] + ', ' + v : v; });
      if (data._honey) return;
      delete data._honey;
      data._subject = '[MindWork.com] ' + (form.getAttribute('data-subject') || 'Website form');
      data._template = 'table'; data._captcha = 'false';
      data.form = form.getAttribute('data-form') || 'form';
      data.page = location.pathname;
      status.className = 'form-status'; status.textContent = 'Sending…';
      if (btn) btn.disabled = true;
      MW.send(data).then(function () {
        status.className = 'form-status ok';
        status.textContent = form.getAttribute('data-done') || 'Sent. We reply by email.';
        form.reset();
        if (form.getAttribute('data-unlock')) MW.set('lead', true);
        if (form.getAttribute('data-next')) { status.appendChild(document.createTextNode(' ')); status.appendChild(MW.el('a', { href: MW.root + form.getAttribute('data-next'), text: 'Open the full plan' })); }
        form.dispatchEvent(new CustomEvent('mw:sent', { detail: data }));
      }).catch(function () {
        status.className = 'form-status err';
        status.innerHTML = 'That didn’t send. Check your connection and try again, or <a href="https://web.works/contact" target="_blank" rel="noopener">use the contact page</a>.';
      }).then(function () { if (btn) btn.disabled = false; });
    });
  }

  /* ---------- consent + ads ---------- */
  function consent() {
    var box = document.getElementById('consent');
    if (!box || CFG.consent === 'google' || MW.get('consent', null)) return;
    box.classList.add('show');
    box.addEventListener('click', function (e) {
      var v = e.target.getAttribute('data-consent');
      if (!v) return;
      MW.set('consent', v); box.classList.remove('show');
    });
  }
  function ads() {
    var slots = CFG.adSlots || {};
    document.querySelectorAll('.ad[data-ad]').forEach(function (box) {
      var id = slots[box.getAttribute('data-ad')];
      if (!id || !CFG.adClient) return;
      var ins = MW.el('ins', { class: 'adsbygoogle', style: 'display:block', 'data-ad-client': CFG.adClient, 'data-ad-slot': id, 'data-ad-format': 'auto', 'data-full-width-responsive': 'true' });
      box.appendChild(ins); box.classList.add('on');
      try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
    });
  }

  /* ---------- small UI ---------- */
  function theme() {
    var btn = document.getElementById('theme-btn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      document.documentElement.setAttribute('data-theme', dark ? 'light' : 'dark');
      MW.set('theme', dark ? 'light' : 'dark');
      btn.setAttribute('aria-pressed', String(!dark));
    });
  }
  function menu() {
    var b = document.getElementById('menu-btn'), n = document.getElementById('nav');
    if (b && n) b.addEventListener('click', function () { var o = n.classList.toggle('open'); b.setAttribute('aria-expanded', String(o)); });
  }
  function videos() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('button[data-yt]') : null;
      if (!b) return;
      var id = b.getAttribute('data-yt');
      var f = MW.el('iframe', { src: 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0', title: b.getAttribute('aria-label') || 'Video', allow: 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share', allowfullscreen: '', loading: 'lazy' });
      b.parentNode.replaceChild(f, b);
    });
  }
  function leadbar() {
    var bar = document.getElementById('leadbar');
    if (!bar || MW.get('lead', false) || MW.get('leadbar-x', 0) > Date.now() - 6048e5) return;
    var shown = false, show = function () { if (shown) return; shown = true; bar.classList.add('show'); };
    setTimeout(show, 30000);
    window.addEventListener('scroll', function () { if (window.scrollY > document.body.scrollHeight * 0.4) show(); }, { passive: true });
    bar.querySelector('.x').addEventListener('click', function () { bar.classList.remove('show'); MW.set('leadbar-x', Date.now()); });
  }
  function filters() {
    document.querySelectorAll('[data-filter-group]').forEach(function (group) {
      var target = document.querySelector(group.getAttribute('data-filter-group'));
      var q = document.querySelector(group.getAttribute('data-search') || '#none');
      var cat = 'all';
      function apply() {
        var term = q ? q.value.trim().toLowerCase() : '';
        target.querySelectorAll('[data-cat]').forEach(function (li) {
          var ok = (cat === 'all' || li.getAttribute('data-cat') === cat) && (!term || li.textContent.toLowerCase().indexOf(term) >= 0);
          li.hidden = !ok;
        });
      }
      group.addEventListener('click', function (e) {
        var b = e.target.closest('button[data-cat-btn]'); if (!b) return;
        cat = b.getAttribute('data-cat-btn');
        group.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        apply();
      });
      if (q) q.addEventListener('input', apply);
    });
  }
  function marks() {
    /* mark tiles the visitor has already done; fill "best" labels */
    var all = MW.scores();
    document.querySelectorAll('[data-test]').forEach(function (t) {
      var s = all[t.getAttribute('data-test')], m = MW.META[t.getAttribute('data-test')];
      if (s && s.best != null && m) { var em = t.querySelector('em'); if (em) em.textContent = 'Your best: ' + s.best + ' ' + m.unit; }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    theme(); menu(); consent(); ads(); videos(); leadbar(); filters(); marks();
    document.querySelectorAll('form.mw-form').forEach(wireForm);
    document.querySelectorAll('[data-year]').forEach(function (n) { n.textContent = new Date().getFullYear(); });
    document.dispatchEvent(new Event('mw:ready'));
  });
})();
