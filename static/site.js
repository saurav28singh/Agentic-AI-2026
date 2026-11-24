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
            } catch (err) { }
            window.open(url, '_blank', 'noopener,noreferrer');
          }
        });
      })(formLinks[i]);
    }

    /* reliable mailto link handling on desktop, mobile, and inside Streamlit iframe */
    var mailtoLinks = document.querySelectorAll('a[href^="mailto:"]');
    for (var j = 0; j < mailtoLinks.length; j++) {
      (function (btn) {
        btn.addEventListener('click', function (e) {
          if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey) {
            return;
          }
          var url = btn.getAttribute('href');
          if (!url || !url.startsWith('mailto:')) {
            return;
          }
          try {
            if (window.top && window.top !== window) {
              e.preventDefault();
              window.top.location.href = url;
              return;
            }
          } catch (err) { }
          window.location.href = url;
        });
      })(mailtoLinks[j]);
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
  } catch (e) { }
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
  } catch (e) { }
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

/* permanent dark theme */
(function () {
  try { localStorage.removeItem('aaiw-theme'); } catch (e) { }
  document.documentElement.setAttribute('data-theme', 'dark');
  document.documentElement.classList.remove('t-light');
  document.documentElement.classList.add('t-dark');
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
  try { reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { }

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
    var backdrop = document.getElementById('navBackdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.id = 'navBackdrop';
      backdrop.className = 'nav-backdrop';
      backdrop.setAttribute('aria-hidden', 'true');
      document.body.appendChild(backdrop);
    }

    function setMenuState(open) {
      nav.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
      var txt = btn.querySelector('.menu-btn-text');
      if (txt) {
        txt.textContent = open ? 'Close' : 'Menu';
      }
      if (backdrop) {
        backdrop.classList.toggle('open', open);
      }
      document.body.classList.toggle('menu-open', open);
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = !nav.classList.contains('open');
      setMenuState(willOpen);
    });

    if (backdrop) {
      backdrop.addEventListener('click', function () {
        setMenuState(false);
      });
    }

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
  var carousel = document.getElementById('spkCarousel');
  if (!carousel) return;

  var track = document.getElementById('spkTrack');
  var viewport = document.getElementById('spkViewport');
  var prevBtn = document.getElementById('spkPrev');
  var nextBtn = document.getElementById('spkNext');
  var dotsContainer = document.getElementById('spkDots');
  var cards = track ? track.querySelectorAll('.spk-card') : [];
  var total = cards.length;
  if (!track || total === 0) return;

  var currentIndex = 0;
  var timer = null;
  var autoAdvanceInterval = 5500;
  var isHovered = false;
  var isFocused = false;

  function getVisibleCount() {
    var w = window.innerWidth;
    if (w <= 560) return 1;
    if (w <= 768) return 2;
    if (w <= 1024) return 3;
    if (w <= 1380) return 4;
    return 5;
  }

  function getCenterOffset(v) {
    return Math.floor(v / 2);
  }

  function getMaxIndex() {
    var v = getVisibleCount();
    return Math.max(0, total - v);
  }

  function updateActiveStates() {
    var v = getVisibleCount();
    var centerOffset = getCenterOffset(v);
    var centerIndex = Math.min(currentIndex + centerOffset, total - 1);

    for (var i = 0; i < total; i++) {
      if (i === centerIndex) {
        cards[i].classList.add('is-center');
        cards[i].setAttribute('aria-current', 'true');
      } else {
        cards[i].classList.remove('is-center');
        cards[i].removeAttribute('aria-current');
      }
    }

    if (dotsContainer) {
      var dots = dotsContainer.querySelectorAll('.spk-dot');
      for (var d = 0; d < dots.length; d++) {
        if (d === currentIndex) {
          dots[d].classList.add('is-active');
          dots[d].setAttribute('aria-selected', 'true');
        } else {
          dots[d].classList.remove('is-active');
          dots[d].setAttribute('aria-selected', 'false');
        }
      }
    }
  }

  function renderDots() {
    if (!dotsContainer) return;
    dotsContainer.innerHTML = '';
    var maxIdx = getMaxIndex();
    var numPositions = maxIdx + 1;

    for (var i = 0; i < numPositions; i++) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'spk-dot' + (i === currentIndex ? ' is-active' : '');
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Go to speaker slide ' + (i + 1));
      dot.setAttribute('aria-selected', String(i === currentIndex));
      (function (idx) {
        dot.addEventListener('click', function () {
          goTo(idx);
          restartTimer();
        });
      })(i);
      dotsContainer.appendChild(dot);
    }
  }

  function getStep() {
    if (!cards[0]) return 0;
    var cardRect = cards[0].getBoundingClientRect();
    var gap = parseFloat(window.getComputedStyle(track).gap) || 16;
    return cardRect.width + gap;
  }

  function updateTransform(animate) {
    if (animate === false) {
      track.style.transition = 'none';
    } else {
      track.style.transition = 'transform .45s cubic-bezier(.22, 1, .36, 1)';
    }
    var step = getStep();
    var offset = currentIndex * step;
    track.style.transform = 'translate3d(-' + offset + 'px, 0, 0)';
    if (animate === false) {
      // Force reflow and restore transition
      track.offsetHeight;
      track.style.transition = 'transform .45s cubic-bezier(.22, 1, .36, 1)';
    }
    updateActiveStates();
  }

  function goTo(index, animate) {
    var maxIdx = getMaxIndex();
    if (index < 0) {
      index = maxIdx;
    } else if (index > maxIdx) {
      index = 0;
    }
    currentIndex = index;
    updateTransform(animate);
  }

  function next() {
    goTo(currentIndex + 1);
  }

  function prev() {
    goTo(currentIndex - 1);
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', function () {
      prev();
      restartTimer();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      next();
      restartTimer();
    });
  }

  for (var k = 0; k < total; k++) {
    (function (idx) {
      cards[idx].addEventListener('click', function () {
        var v = getVisibleCount();
        var centerOffset = getCenterOffset(v);
        var targetIndex = idx - centerOffset;
        var maxIdx = getMaxIndex();
        targetIndex = Math.max(0, Math.min(targetIndex, maxIdx));
        goTo(targetIndex);
        restartTimer();
      });
    })(k);
  }

  if (viewport) {
    var startX = 0;
    var startY = 0;
    var currentX = 0;
    var currentY = 0;
    var isSwiping = false;
    var threshold = 35;

    viewport.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      startX = e.clientX;
      startY = e.clientY;
      currentX = e.clientX;
      currentY = e.clientY;
      isSwiping = true;
      stopTimer();
    }, { passive: true });

    window.addEventListener('pointermove', function (e) {
      if (!isSwiping) return;
      currentX = e.clientX;
      currentY = e.clientY;
    }, { passive: true });

    window.addEventListener('pointerup', function (e) {
      if (!isSwiping) return;
      isSwiping = false;
      var deltaX = currentX - startX;
      var deltaY = currentY - startY;
      if (Math.abs(deltaX) > threshold && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
        if (deltaX < 0) {
          next();
        } else {
          prev();
        }
      }
      startTimer();
    }, { passive: true });

    window.addEventListener('pointercancel', function () {
      if (isSwiping) {
        isSwiping = false;
        startTimer();
      }
    }, { passive: true });
  }

  carousel.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      prev();
      restartTimer();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      next();
      restartTimer();
    }
  });

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function startTimer() {
    if (timer || prefersReducedMotion()) return;
    timer = setInterval(function () {
      if (!isHovered && !isFocused && !document.hidden) {
        next();
      }
    }, autoAdvanceInterval);
  }

  function stopTimer() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  function restartTimer() {
    stopTimer();
    startTimer();
  }

  carousel.addEventListener('pointerenter', function () {
    isHovered = true;
    stopTimer();
  });
  carousel.addEventListener('pointerleave', function () {
    isHovered = false;
    startTimer();
  });
  carousel.addEventListener('focusin', function () {
    isFocused = true;
    stopTimer();
  });
  carousel.addEventListener('focusout', function () {
    isFocused = false;
    startTimer();
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      stopTimer();
    } else {
      startTimer();
    }
  });

  var resizeTimeout;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function () {
      var maxIdx = getMaxIndex();
      if (currentIndex > maxIdx) {
        currentIndex = maxIdx;
      }
      renderDots();
      updateTransform(false);
    }, 100);
  });

  renderDots();
  goTo(0, false);
  startTimer();
})();

/* Premium 3D Tech Robot pulling Pre-Event CTA button (Left to Right Sequence) */
(function () {
  var heroActions = document.getElementById('heroActions');
  var btn = document.getElementById('heroPreBtn');
  var stage = document.getElementById('heroCinematicStage');
  var bot = document.getElementById('heroTechBot');
  var tetherCanvas = document.getElementById('heroTetherCanvas');
  var tetherPath = document.getElementById('heroTetherPath');
  var legL = document.getElementById('botLegL');
  var legR = document.getElementById('botLegR');
  var armL = document.getElementById('botArmL');
  var armR = document.getElementById('botArmR');
  var head = document.getElementById('botHeadAssembly');

  if (!heroActions || !btn || !stage || !bot || !tetherCanvas || !tetherPath) return;

  var reduced = false;
  try {
    reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}

  if (reduced) {
    btn.style.transform = 'none';
    btn.style.opacity = '1';
    stage.style.display = 'none';
    btn.classList.add('hero-btn-settle-glow');
    return;
  }

  var animationTriggered = false;

  function initTechRobotSequence() {
    if (animationTriggered) return;
    animationTriggered = true;

    var isMobile = window.innerWidth <= 768;
    var btnWidth = btn.offsetWidth || (isMobile ? 290 : 390);
    var btnHeight = btn.offsetHeight || 48;
    var leadDist = isMobile ? 18 : 28;

    // Left-to-Right Geometry
    var btnStartX = isMobile ? -Math.min(220, window.innerWidth * 0.55) : -(btnWidth + 20);
    var robotStartX = isMobile ? -55 : -45;
    var robotDockX = btnWidth + leadDist;
    var robotDockY = isMobile ? -4 : 2;

    // Initial Positions
    btn.style.transform = 'translate3d(' + btnStartX.toFixed(1) + 'px, 0, 0)';
    btn.style.opacity = '0';

    bot.style.transform = 'translate3d(' + robotStartX.toFixed(1) + 'px, ' + robotDockY + 'px, 0) rotate(5deg)';
    bot.style.opacity = '1';

    tetherCanvas.style.opacity = '1';
    tetherCanvas.style.display = 'block';

    var startTime = null;
    var haulDuration = 1900;  // Phase 1: Enter & Pull to destination (0.0s - 1.9s)
    var dockDuration = 550;   // Phase 2: Settle micro-bounce & confident nod (1.9s - 2.45s)
    var exitDuration = 1150;  // Phase 3: Walk away off-screen to the right (2.45s - 3.6s)
    var totalDuration = haulDuration + dockDuration + exitDuration;

    function easeOutCubic(t) {
      return 1 - Math.pow(1 - t, 3);
    }

    function renderTetherLine(x1, y1, x2, y2, tension) {
      try {
        var midX = (x1 + x2) * 0.5;
        var midY = (y1 + y2) * 0.5 + tension;
        tetherPath.setAttribute('d', 'M ' + x1.toFixed(1) + ' ' + y1.toFixed(1) +
          ' Q ' + midX.toFixed(1) + ' ' + midY.toFixed(1) +
          ' ' + x2.toFixed(1) + ' ' + y2.toFixed(1));
      } catch (e) {}
    }

    function frame(timestamp) {
      if (!startTime) startTime = timestamp;
      var elapsed = timestamp - startTime;

      if (elapsed < haulDuration) {
        // ========== Phase 1: Enter from Left & Pull toward Right ==========
        var p = Math.min(1, elapsed / haulDuration);
        var eased = easeOutCubic(p);

        // Button moves from left to (0, 0) smoothly without rotation or deformation
        var curBtnX = (1 - eased) * btnStartX;
        var btnFade = Math.min(1, elapsed / 200);
        btn.style.opacity = btnFade.toFixed(2);
        btn.style.transform = 'translate3d(' + curBtnX.toFixed(1) + 'px, 0, 0)';

        // Robot walks naturally facing right, leading the button
        var curRobX = (1 - eased) * robotStartX + eased * robotDockX;
        var leanAngle = 5 + Math.sin(p * Math.PI * 7) * 1.2;
        var bobY = Math.abs(Math.sin(p * Math.PI * 7)) * 1.8;

        bot.style.transform = 'translate3d(' + curRobX.toFixed(1) + 'px, ' + (robotDockY - bobY).toFixed(1) + 'px, 0) rotate(' + leanAngle.toFixed(1) + 'deg)';

        // Leg stride cycle
        var stride = Math.sin(p * Math.PI * 8) * 20;
        if (legL) legL.style.transform = 'rotate(' + (-stride).toFixed(1) + 'deg)';
        if (legR) legR.style.transform = 'rotate(' + (stride).toFixed(1) + 'deg)';

        // Arms pulling backward holding tether
        if (armL) armL.style.transform = 'rotate(-16deg)';
        if (armR) armR.style.transform = 'rotate(-12deg)';

        // Micro-tether line
        var bX = curBtnX + btnWidth - 2;
        var bY = btnHeight * 0.5;
        var rX = curRobX + (20 / 100) * 68;
        var rY = robotDockY - bobY + (58 / 110) * 75;

        renderTetherLine(bX, bY, rX, rY, -1.5);
        requestAnimationFrame(frame);

      } else if (elapsed < haulDuration + dockDuration) {
        // ========== Phase 2: Settle Button, Tether Disconnects, Robot Nods ==========
        var sp = (elapsed - haulDuration) / dockDuration;

        // Button settles with subtle micro-bounce in exact spot
        var bounceScale = 1 + 0.016 * Math.sin(sp * Math.PI * 2) * Math.exp(-sp * 3.2);
        btn.style.opacity = '1';
        btn.style.transform = 'translate3d(0, 0, 0) scale(' + bounceScale.toFixed(4) + ')';
        btn.classList.add('hero-btn-settle-glow');

        // Tether unclips and fades out
        var tetherFade = Math.max(0, 1 - sp * 3.5);
        tetherCanvas.style.opacity = tetherFade.toFixed(2);

        // Robot plants feet, returns to upright posture
        var standTilt = Math.max(0, 5 * (1 - sp * 2));
        bot.style.transform = 'translate3d(' + robotDockX.toFixed(1) + 'px, ' + robotDockY.toFixed(1) + 'px, 0) rotate(' + standTilt.toFixed(1) + 'deg)';
        if (legL) legL.style.transform = 'rotate(0deg)';
        if (legR) legR.style.transform = 'rotate(0deg)';
        if (armL) armL.style.transform = 'rotate(-4deg)';
        if (armR) armR.style.transform = 'rotate(-4deg)';

        // Tiny confident head nod
        if (head && sp >= 0.15 && sp <= 0.85) {
          var nodP = (sp - 0.15) / 0.7;
          var nodAngle = Math.sin(nodP * Math.PI) * 4.5;
          head.style.transform = 'rotate(' + nodAngle.toFixed(1) + 'deg)';
        } else if (head) {
          head.style.transform = 'rotate(0deg)';
        }

        requestAnimationFrame(frame);

      } else if (elapsed < totalDuration) {
        // ========== Phase 3: Walk Away off-screen to the Right ==========
        btn.style.transform = '';
        tetherCanvas.style.display = 'none';

        var wp = (elapsed - (haulDuration + dockDuration)) / exitDuration;
        var easedW = wp * wp * (3 - 2 * wp); // smoothstep

        var exitX = Math.max(window.innerWidth * 0.85, 680);
        var curWalkX = robotDockX + (exitX - robotDockX) * easedW;
        var bobWalkY = Math.abs(Math.sin(wp * Math.PI * 9)) * 2;

        var robFade = wp > 0.65 ? Math.max(0, (1 - wp) / 0.35) : 1;
        bot.style.opacity = robFade.toFixed(2);
        bot.style.transform = 'translate3d(' + curWalkX.toFixed(1) + 'px, ' + (robotDockY - bobWalkY).toFixed(1) + 'px, 0)';

        // Walking stride cycle
        var walkStride = Math.sin(wp * Math.PI * 10) * 18;
        if (legL) legL.style.transform = 'rotate(' + (-walkStride).toFixed(1) + 'deg)';
        if (legR) legR.style.transform = 'rotate(' + (walkStride).toFixed(1) + 'deg)';

        // Natural arm counter-swing
        if (armL) armL.style.transform = 'rotate(' + (walkStride * 0.85).toFixed(1) + 'deg)';
        if (armR) armR.style.transform = 'rotate(' + (-walkStride * 0.85).toFixed(1) + 'deg)';

        requestAnimationFrame(frame);

      } else {
        // ========== Phase 4: Sequence Complete — Clean State ==========
        btn.style.transform = '';
        btn.style.opacity = '';
        btn.classList.add('hero-btn-settle-glow');

        // Stage completely hidden: No permanent robot
        stage.style.display = 'none';
      }
    }

    requestAnimationFrame(frame);
  }

  // Trigger once when hero actions element is visible
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        observer.disconnect();
        initTechRobotSequence();
      }
    }, { threshold: 0.1 });
    observer.observe(heroActions);
  } else {
    setTimeout(initTechRobotSequence, 120);
  }
})();
