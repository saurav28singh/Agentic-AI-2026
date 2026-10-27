/* external form links, read from config.js */
(function () {
  var cfg = window.AAIW_LINKS || {};
  var nodes = document.querySelectorAll('[data-link]');
  for (var i = 0; i < nodes.length; i++) {
    (function (el) {
      var currentHref = (el.getAttribute('href') || '').trim();
      var key = el.getAttribute('data-link');
      var url = (cfg[key] || '').trim();
      if (!url && (currentHref.startsWith('http://') || currentHref.startsWith('https://'))) {
        url = currentHref;
      }
      if (url) {
        el.setAttribute('href', url);
        el.setAttribute('target', '_blank');
        el.setAttribute('rel', 'noopener noreferrer');
        el.removeAttribute('aria-disabled');
        el.classList.remove('is-pending');
      } else {
        el.setAttribute('href', '#');
        el.setAttribute('aria-disabled', 'true');
        el.classList.add('is-pending');
        el.addEventListener('click', function (e) { e.preventDefault(); });
      }
    })(nodes[i]);
  }
  var mail = (cfg.contact || '').trim();
  var slots = document.querySelectorAll('[data-contact]');
  for (var j = 0; j < slots.length; j++) {
    if (mail) {
      slots[j].textContent = mail;
      slots[j].classList.remove('tba');
    }
  }
})();

/* reliable navigation for external form links inside Streamlit iframe */
(function () {
  function setupExternalLinks() {
    var formLinks = document.querySelectorAll('.take a.btn-go[href*="forms.gle"], a.btn[href*="forms.gle"]');
    for (var i = 0; i < formLinks.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function (e) {
          if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey) {
            return;
          }
          var url = btn.getAttribute('href');
          if (url && (url.startsWith('https://forms.gle/') || url.startsWith('http'))) {
            e.preventDefault();
            try {
              if (window.top && window.top !== window) {
                window.top.open(url, '_blank', 'noopener,noreferrer');
                return;
              }
            } catch (err) {}
            window.open(url, '_blank', 'noopener,noreferrer');
          }
        });
      })(formLinks[i]);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupExternalLinks);
  } else {
    setupExternalLinks();
  }
})();

/* the facts list bends toward the pointer, and settles as it leaves */
(function () {
  var list = document.querySelector('.facts');
  if (!list) return;
  var reduced = false, fine = true;
  try {
    reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  } catch (e) {}
  if (reduced || !fine) return;

  var rows = [].slice.call(list.querySelectorAll('.fact'));
  var LIFT = 9, SPREAD = 74;
  var pending = false, pointerY = 0, inside = false;

  function paint() {
    pending = false;
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i].getBoundingClientRect();
      var d = (r.top + r.height / 2) - pointerY;
      var k = d / SPREAD;
      var lift = inside ? -LIFT * Math.exp(-k * k) : 0;
      rows[i].style.transform = lift ? 'translate3d(0,' + lift.toFixed(2) + 'px,0)' : '';
    }
  }
  function queue() {
    if (!pending) { pending = true; requestAnimationFrame(paint); }
  }

  list.addEventListener('pointermove', function (e) {
    inside = true; pointerY = e.clientY; queue();
  });
  list.addEventListener('pointerleave', function () {
    inside = false; queue();
  });
})();

/* the title leans toward the pointer, a little */
(function () {
  var hero = document.querySelector('.hero');
  if (!hero) return;
  var reduced = false, fine = true;
  try {
    reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  } catch (e) {}
  if (reduced || !fine) return;
  var h1 = hero.querySelector('h1');
  if (!h1) return;
  hero.addEventListener('pointermove', function (e) {
    var r = hero.getBoundingClientRect();
    var x = (e.clientX - r.left) / r.width - 0.5;
    var y = (e.clientY - r.top) / r.height - 0.5;
    hero.classList.add('tilting');
    h1.style.setProperty('--ty', (x * 7).toFixed(2) + 'deg');
    h1.style.setProperty('--tx', (-y * 5).toFixed(2) + 'deg');
  });
  hero.addEventListener('pointerleave', function () {
    hero.classList.remove('tilting');
    h1.style.setProperty('--ty', '0deg');
    h1.style.setProperty('--tx', '0deg');
  });
})();

/* theme toggle — our own class, so the host's attribute cannot override it */
(function () {
  var btn = document.getElementById('themeBtn');
  if (!btn) return;
  var root = document.documentElement;
  function current() {
    if (root.classList.contains('t-dark')) return 'dark';
    if (root.classList.contains('t-light')) return 'light';
    var attr = root.getAttribute('data-theme');
    if (attr === 'dark' || attr === 'light') return attr;
    try {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    } catch (e) { return 'light'; }
  }
  btn.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    root.classList.remove('t-dark', 't-light');
    root.classList.add('t-' + next);
    try { localStorage.setItem('aaiw-theme', next); } catch (e) {}
  });
})();

/* the illustrative run on the home page */
(function () {
  var svg = document.querySelector('.orch');
  var logEl = document.getElementById('demoLog');
  var stateEl = document.getElementById('demoState');
  var replay = document.getElementById('demoReplay');
  if (!svg || !logEl || !stateEl) return;

  var stats = {
    attempt: document.getElementById('stAttempt'),
    calls: document.getElementById('stCalls'),
    tokens: document.getElementById('stTokens'),
    cost: document.getElementById('stCost'),
    time: document.getElementById('stTime')
  };
  var reduced = false;
  try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  // node, edges to light, log line, tone, added calls, added tokens, added seconds, run state
  var steps = [
    ['n-orch', ['f-goal'], 'orchestrator', 'plan: retrieve \u2192 draft \u2192 verify', '', 0, 900, 1.4, 'running', 1],
    ['n-ret', ['f-o2r'], 'retriever', 'arXiv + PubMed + bioRxiv \u00b7 38 hits', '', 4, 12400, 9.2, 'running', 1],
    ['n-rea', ['f-r2rea'], 'reasoner', 'drafts 6 paragraphs, 20 claims', '', 0, 9800, 7.5, 'running', 1],
    ['n-ver', ['f-rea2v'], 'verifier', 're-reads every cited source', '', 1, 5200, 6.1, 'running', 1],
    ['n-ver!', [], 'verifier', '2 claims unsupported, attempt 1 failed', 'warn', 0, 0, 0.4, 'failed', 1],
    ['n-orch', ['f-revise'], 'orchestrator', 'keep the 18 that held, send 2 round again', 'warn', 0, 900, 1.2, 'running', 2],
    ['n-ret', ['f-o2r'], 'retriever', 'narrower query \u00b7 1 new source', '', 3, 6100, 5.8, 'running', 2],
    ['n-rea', ['f-r2rea'], 'reasoner', 'rewrites the two paragraphs', '', 0, 4300, 4.3, 'running', 2],
    ['n-ver!', ['f-rea2v'], 'verifier', '1 claim still unsupported, attempt 2 failed', 'warn', 1, 3100, 3.6, 'failed', 2],
    ['n-orch', ['f-revise'], 'orchestrator', 'one more lap, then drop what has no source', 'warn', 0, 700, 1.1, 'running', 3],
    ['n-ret', ['f-o2r'], 'retriever', 'nothing further to find', '', 2, 2400, 3.1, 'running', 3],
    ['n-rea', ['f-r2rea'], 'reasoner', 'drops the unsupported claim', '', 0, 2900, 2.9, 'running', 3],
    ['n-ver+', ['f-rea2v'], 'verifier', 'all 19 claims match their source', 'good', 1, 2200, 2.4, 'running', 3],
    ['n-ans+', ['f-v2a'], 'orchestrator', 'releases the answer with its trace', 'good', 0, 0, 0.6, 'passed', 3]
  ];

  var timer = null, idx = 0, calls = 0, tokens = 0, secs = 0;

  var stack = document.querySelector('.orch-stack');

  function clearMarks() {
    var boxes = svg.querySelectorAll('.box');
    for (var i = 0; i < boxes.length; i++) { boxes[i].classList.remove('on', 'fail', 'pass'); }
    var flows = svg.querySelectorAll('.flow');
    for (var j = 0; j < flows.length; j++) { flows[j].classList.remove('on'); }
    if (stack) {
      var rows = stack.querySelectorAll('li');
      for (var k = 0; k < rows.length; k++) { rows[k].classList.remove('on', 'fail', 'pass'); }
    }
  }

  function bump(el, text) {
    if (!el) return;
    el.textContent = text;
    el.classList.add('bump');
    setTimeout(function () { el.classList.remove('bump'); }, 420);
  }

  function addLog(who, msg, tone) {
    var li = document.createElement('li');
    if (tone) li.className = tone;
    li.innerHTML = '<b></b><span></span>';
    li.querySelector('b').textContent = who;
    li.querySelector('span').textContent = msg;
    logEl.appendChild(li);
    while (logEl.children.length > 4) { logEl.removeChild(logEl.firstChild); }
  }

  function run(step) {
    var id = step[0], mark = '';
    if (id.slice(-1) === '!') { mark = 'fail'; id = id.slice(0, -1); }
    else if (id.slice(-1) === '+') { mark = 'pass'; id = id.slice(0, -1); }
    clearMarks();
    var node = document.getElementById(id);
    if (node) node.classList.add(mark || 'on');
    var row = document.getElementById('m-' + id.slice(2));
    if (row) row.classList.add(mark || 'on');
    for (var i = 0; i < step[1].length; i++) {
      var f = document.getElementById(step[1][i]);
      if (f) f.classList.add('on');
    }
    addLog(step[2], step[3], step[4]);
    calls += step[5];
    tokens += step[6];
    secs += step[7];
    bump(stats.calls, String(calls));
    bump(stats.tokens, (tokens / 1000).toFixed(1) + 'k');
    bump(stats.cost, '$' + (tokens * 0.0000065).toFixed(2));
    bump(stats.time, secs.toFixed(1) + 's');
    bump(stats.attempt, step[9] + ' of 3');
    stateEl.textContent = step[8];
    stateEl.className = 'run-state ' + (step[8] === 'running' ? '' : step[8]);
  }

  function stop() { clearTimeout(timer); timer = null; }

  function play() {
    stop();
    idx = 0; calls = 0; tokens = 0; secs = 0;
    logEl.innerHTML = '';
    function next() {
      if (idx >= steps.length) {
        timer = setTimeout(play, 7000);
        return;
      }
      run(steps[idx]);
      var wait = steps[idx][8] === 'failed' ? 2100 : 1500;
      idx++;
      timer = setTimeout(next, wait);
    }
    next();
  }

  if (replay) replay.addEventListener('click', play);
  if (reduced) return;

  try {
    var io2 = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) { if (!timer) play(); }
        else { stop(); }
      }
    }, { threshold: 0.12 });
    io2.observe(svg.closest('section') || svg);
  } catch (e) { play(); }

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { stop(); }
  });
})();

/* Agentic AI Workshop 2026 — mobile menu + speaker ring */
(function () {
  var btn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    function setMenuState(open) {
      nav.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
      var txt = btn.querySelector('.menu-btn-text');
      if (txt) {
        txt.textContent = open ? 'Close' : 'Menu';
      }
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = !nav.classList.contains('open');
      setMenuState(willOpen);
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' || e.target.closest('a')) {
        setMenuState(false);
      }
    });

    document.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !nav.contains(e.target) && !btn.contains(e.target)) {
        setMenuState(false);
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        setMenuState(false);
        btn.focus();
      }
    });
  }
})();

(function () {
  var people = [
    ['Prof. Surya Ganguli', 'Associate Professor of Applied Physics', 'Stanford University', '', 'Academia'],
    ['Prof. Manik Varma', 'Technical Fellow & Corporate Vice President', 'Microsoft Research India', '', 'Industry'],
    ['Dr. Nanda Kishore Kambhatla', 'Head of Lab', 'Adobe Research, India', 'Enterprise', 'Industry'],
    ['Dr. Balaji Vasan Srinivasan', 'Principal Scientist', 'Adobe Research, India', 'Enterprise', 'Industry'],
    ['Dr. Prashant Warier', 'Co-Founder & Chief Executive Officer', 'Qure.ai', 'Healthcare', 'Industry'],
    ['Dr. Arijit Patra', 'Senior Principal Scientist', 'UCB Pharma', 'Healthcare', 'Industry'],
    ['Dr. Nitish Naik', 'Professor of Cardiology', 'AIIMS, New Delhi', 'Healthcare', 'Academia'],
    ['Prof. Karthik Raman', 'Professor, Data Science and AI, and Biotechnology', 'IIT Madras', 'Scientific Discovery', 'Academia'],
    ['Prof. Raghunathan Rengaswamy', 'Professor, Data Science and AI, and Chemical Engineering', 'IIT Madras', '', 'Academia'],
    ['Dr. Deepak N. Subramani', 'Associate Professor, Computational and Data Sciences', 'IISc Bangalore', 'Scientific Discovery', 'Academia'],
    ['Prof. Ashutosh Modi', 'Associate Professor, Computer Science and Engineering', 'IIT Kanpur', '', 'Academia']
  ];
  var orbit = document.getElementById('orbit');
  var name = document.getElementById('orbName');
  var role = document.getElementById('orbRole');
  var org = document.getElementById('orbOrg');
  var tags = document.getElementById('orbTags');
  if (!orbit || !name) return;
  var faces = orbit.querySelectorAll('.face');

  function show(i) {
    var p = people[i];
    if (!p) return;
    name.textContent = p[0];
    role.textContent = p[1];
    org.textContent = p[2];
    var html = '';
    if (p[3]) { html += '<span class="track">' + p[3] + '</span>'; }
    html += '<span>' + p[4] + '</span>';
    tags.innerHTML = html;
    for (var k = 0; k < faces.length; k++) {
      faces[k].setAttribute('aria-current', String(k === i));
    }
  }

  var cur = 0, timer = null;
  function step() { cur = (cur + 1) % people.length; show(cur); }
  function start() { if (!timer) { timer = setInterval(step, 2800); } }
  function stop() { clearInterval(timer); timer = null; }

  for (var k = 0; k < faces.length; k++) {
    (function (btn, i) {
      btn.addEventListener('mouseenter', function () { cur = i; show(i); });
      btn.addEventListener('focus', function () { cur = i; show(i); });
      btn.addEventListener('click', function () { cur = i; show(i); });
    })(faces[k], parseInt(faces[k].getAttribute('data-i'), 10));
  }
  orbit.addEventListener('mouseenter', stop);
  orbit.addEventListener('mouseleave', start);
  orbit.addEventListener('focusin', stop);
  orbit.addEventListener('focusout', start);
  orbit.addEventListener('touchstart', stop, { passive: true });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { stop(); } else { start(); }
  });
  show(0);
  start();
})();
