import math
#!/usr/bin/env python3
"""Generate the Agentic AI Workshop 2026 site (one file per page)."""
import io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("programme.html", "Programme"),
    ("speakers.html", "Speakers"),
    ("tutorials.html", "Tutorials"),
    ("venue.html", "Venue"),
    ("organisers.html", "Organisers"),
]

EARLY_THEME = '<script>try{var t=localStorage.getItem("aaiw-theme");if(t){document.documentElement.classList.add("t-"+t);}}catch(e){}</script>'

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400'
         '&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">')


def header(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append('      <a href="%s"%s>%s</a>' % (href, cur, label))
    return """<header class="site-head">
  <div class="wrap head-in">
    <a class="mark" href="index.html" aria-label="IIT Delhi &middot; ScAI Home">
      <img class="crest crest-red" src="photos/iitd-crest-red.png" alt="IIT Delhi" width="160" height="160">
      <img class="crest crest-white" src="photos/iitd-crest-white.png" alt="IIT Delhi" width="160" height="160">
      <span class="mark-divider" aria-hidden="true"></span>
      <img class="scai-logo" src="photos/scai-logo.png" alt="Yardi School of Artificial Intelligence, Indian Institute of Technology Delhi" width="520" height="38">
    </a>
    <nav class="nav" id="nav" aria-label="Pages">
%s
      <div class="nav-mobile-cta">
        <a class="btn btn-sm" href="register.html">Register to attend</a>
      </div>
    </nav>
    <button class="theme-btn" id="themeBtn" type="button" aria-label="Switch between light and dark theme">
      <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2M12 19.5v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.5 12h2M19.5 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
    </button>
    <a class="btn btn-sm head-cta" href="register.html">Register</a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Toggle navigation menu">
      <span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span>
      <span class="menu-btn-text">Menu</span>
    </button>
  </div>
</header>""" % "\n".join(links)


FOOTER = """<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="crest crest-red foot-crest" src="photos/iitd-crest-red.png" alt="Indian Institute of Technology Delhi" width="160" height="160">
        <img class="crest crest-white foot-crest" src="photos/iitd-crest-white.png" alt="Indian Institute of Technology Delhi" width="160" height="160">
        <div class="brand">Agentic AI Workshop 2026</div>
        <p>Bringing together academia and industry through expert talks, panel discussions, tutorials, live demonstrations and a poster session.</p>
        <p class="mono" style="margin-top:16px;font-size:13px">15&ndash;16 December 2026<br>IIT Delhi, Hauz Khas, New Delhi</p>
      </div>
      <div>
        <h4>Programme</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="programme.html">Schedule</a></li>
          <li><a href="speakers.html">Speakers</a></li>
          <li><a href="tutorials.html">Tutorials &amp; demos</a></li>
        </ul>
      </div>
      <div>
        <h4>Visiting</h4>
        <ul>
          <li><a href="venue.html">Venue &amp; travel</a></li>
          <li><a href="register.html">Registration</a></li>
          <li><a href="organisers.html">Organisers</a></li>
        </ul>
      </div>
      <div>
        <h4>Get involved</h4>
        <ul>
          <li><a href="register.html">Register to attend</a></li>
          <li><a href="register.html#posters">Present a poster</a></li>
          <li><a href="partners.html">Partners &amp; sponsors</a></li>
        </ul>
      </div>
    </div>
    <div class="colophon">
      <span>&copy; 2026 IIT Delhi &middot; Yardi School of Artificial Intelligence</span>
      <span>Enquiries: <span class="tba" data-contact>agenticai.iitd@gmail.com</span></span>
    </div>
  </div>
</footer>
<script src="config.js"></script>
<script src="site.js?v=2"></script>"""


SPEAKERS = [
    ("ganguli", "Prof. Surya Ganguli"), ("manik", "Prof. Manik Varma"),
    ("nanda", "Dr. Nanda Kishore Kambhatla"), ("balaji", "Dr. Balaji Vasan Srinivasan"),
    ("prashant", "Dr. Prashant Warier"), ("patra", "Dr. Arijit Patra"),
    ("nitish", "Dr. Nitish Naik"), ("kartik", "Prof. Karthik Raman"),
    ("raghu", "Prof. Raghunathan Rengaswamy"), ("deepak", "Dr. Deepak N. Subramani"),
    ("ashutosh", "Prof. Ashutosh Modi"), ("aparna", "Aparna Taneja"),
    ("dinesh", "Dinesh Raghu"), ("nitendra", "Nitendra Rajput"),
]


def orbit_block(hint):
    orbs = []
    for i, (slug, name) in enumerate(SPEAKERS):
        a = round(i * 360.0 / len(SPEAKERS), 2)
        cur = ' aria-current="true"' if i == 0 else ""
        orbs.append(
            '              <div class="orb" style="--a:%sdeg"><button class="face" type="button" data-i="%d"%s>'
            '<span class="face-inner"><img src="photos/%s.webp" alt="%s" width="520" height="520"></span>'
            '</button></div>' % (a, i, cur, slug, name))
    return """        <div class="spk-feature">
          <div class="orbit" id="orbit">
            <div class="ring">
%s
            </div>
          </div>
          <div class="orbit-panel" aria-live="polite">
            <h3 id="orbName">Prof. Surya Ganguli</h3>
            <p class="role" id="orbRole">Associate Professor of Applied Physics</p>
            <p class="org" id="orbOrg">Stanford University</p>
            <p class="orbit-hint">%s</p>
          </div>
        </div>""" % ("\n".join(orbs), hint)


def band(eyebrow, heading, blurb, content, alt=False, bid=None):
    return """  <section class="band%s"%s>
    <div class="wrap band-grid">
      <div class="band-head">
        <p class="eyebrow">%s</p>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <div>
%s
      </div>
    </div>
  </section>""" % (" alt" if alt else "", ' id="%s"' % bid if bid else "", eyebrow, heading, blurb, content)


def page_head(crumb, eyebrow, title, lede):
    return """  <section class="page-head">
    <div class="wrap">
      <p class="crumb"><a href="index.html">Home</a> &rarr; %s</p>
      <p class="eyebrow" style="margin-top:16px">%s</p>
      <h1>%s</h1>
      <p class="lede">%s</p>
    </div>
  </section>""" % (crumb, eyebrow, title, lede)


# ---------------------------------------------------------------- schedule
DAY1 = [
    ("09:00 – 10:00", "Inauguration", "Session", "TBA", None, "flag"),
    ("10:00 – 10:30", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("10:30 – 11:00", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("11:00 – 11:30", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("11:30 – 11:45", "Tea break", "Break", "", None, "break"),
    ("11:45 – 12:15", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("12:15 – 12:45", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("12:45 – 13:15", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("13:15 – 15:00", "Lunch &amp; poster session", "Break", "", None, "break"),
    ("15:00 – 16:30", "Panel discussion 1", "Panel", "TBA", "Panelists to be announced", "flag"),
    ("16:30 – 17:00", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("17:00 – 17:30", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("17:30 – 18:00", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("18:00 – 19:30", "Panel discussion 2", "Panel", "TBA", "Five or six panelists, to be announced", "flag"),
    ("19:30 – 21:30", "Networking dinner", "Break", "", None, "break"),
]
DAY2 = [
    ("08:00 – 09:00", "Breakfast", "Break", "", None, "break"),
    ("09:00 – 09:30", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("09:30 – 10:00", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("10:00 – 10:30", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("10:30 – 11:00", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("11:00 – 11:30", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("11:30 – 11:45", "Tea break", "Break", "", None, "break"),
    ("11:45 – 12:15", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("12:15 – 12:45", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("12:45 – 13:15", "Invited talk", "Talk", "TBA", "Speaker to be announced", ""),
    ("13:15 – 14:30", "Tutorial or demo &middot; Track 1", "Tutorial", "TBA", "Instructors to be announced", ""),
    ("13:15 – 14:30", "Tutorial or demo &middot; Track 2", "Tutorial", "TBA", "Instructors to be announced", ""),
    ("13:15 – 14:30", "Tutorial or demo &middot; Track 3", "Tutorial", "TBA", "Instructors to be announced", ""),
    ("13:15 – 14:30", "Tutorial or demo &middot; Track 4", "Tutorial", "TBA", "Instructors to be announced", ""),
    ("13:15 – 14:30", "Tutorial or demo &middot; Track 5", "Tutorial", "TBA", "Instructors to be announced", ""),
]


def sched(rows):
    out = ['        <div class="sched">']
    for t, s, k, r, sub, cls in rows:
        c = " is-break" if cls == "break" else (" is-flag" if cls == "flag" else "")
        sub_html = "<small>%s</small>" % sub if sub else ""
        out.append('          <div class="sched-row%s"><div class="t">%s</div>'
                   '<div class="s">%s%s</div><div class="k">%s</div><div class="r">%s</div></div>'
                   % (c, t.replace("–", "&ndash;"), s, sub_html, k, r))
    out.append("        </div>")
    return "\n".join(out)


FORMATS = """        <div class="formats">
          <div><h4>Keynote</h4><p>Big-picture talks from leading voices in agentic AI.</p></div>
          <div><h4>Talk</h4><p>Research and industry talks on agents at work.</p></div>
          <div><h4>Panel</h4><p>Academia and industry on where agents are heading.</p></div>
          <div><h4>Tutorial</h4><p>Hands-on sessions where you build and run agents yourself. Bring a laptop.</p></div>
          <div><h4>Demo</h4><p>Live agents working on real problems, from labs and companies.</p></div>
        </div>"""

LOOP_BAND = """  <section class="band alt">
    <div class="wrap band-grid">
      <div class="band-head">
        <p class="eyebrow">What is an agentic system?</p>
        <h2>Plan, delegate, verify, repeat</h2>
        <p>An agentic system brings together specialized AI agents that collaborate, exchange information, and iteratively refine their outputs to accomplish complex tasks.</p>
      </div>
      <div>
        <div class="demo-bar">
          <span class="eyebrow">Illustrative run</span>
          <q>Which papers since 2024 report agents running wet-lab experiments?</q>
          <span class="run-state passed" id="demoState">passed</span>
          <button class="replay" id="demoReplay" type="button">Replay</button>
        </div>
        <ol class="orch-stack" aria-hidden="true">
          <li id="m-orch"><span class="st-dot"></span><span class="st-text"><b>Orchestrator</b><small>plan &middot; route &middot; retry</small></span></li>
          <li id="m-ret"><span class="st-dot"></span><span class="st-text"><b>Retriever</b><small>search &middot; rank</small></span></li>
          <li id="m-rea"><span class="st-dot"></span><span class="st-text"><b>Reasoner</b><small>decompose &middot; draft</small></span></li>
          <li id="m-ver"><span class="st-dot"></span><span class="st-text"><b>Verifier</b><small>check &middot; cite</small></span></li>
          <li id="m-ans"><span class="st-dot"></span><span class="st-text"><b>Answer</b><small>with its trace</small></span></li>
        </ol>
        <div class="orch-wrap">
            <svg class="orch" viewBox="0 0 680 460" role="img" aria-label="A loop: a goal enters the orchestrator, which sends work round retriever, reasoner and verifier. A verifier that passes releases the answer; one that fails sends the work back to the orchestrator for another lap.">
              <defs><marker id="ah" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0.5 0.8 L9.6 5 L0.5 9.2 Z" class="tick"/></marker><marker id="ah-on" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0.5 0.8 L9.6 5 L0.5 9.2 Z" class="tick-on"/></marker><marker id="ah-warn" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0.5 0.8 L9.6 5 L0.5 9.2 Z" class="tick-warn"/></marker></defs>
              <path class="wire dot" d="M340 92 V 154"/>
              <path class="wire dot" d="M300 216 V 258 H 215 V 300"/>
              <path class="wire dot" d="M380 216 V 272 H 420 V 300"/>
              <path class="wire dot" d="M80 221 V 394"/>
              <path class="wire dot" d="M215 364 V 394"/>
              <path class="wire dot" d="M500 364 V 394"/>
              <path class="wire" d="M150 42 H 258" marker-end="url(#ah)"/>
              <path class="flow" id="f-goal" d="M150 42 H 258" marker-end="url(#ah-on)"/>
              <path class="wire" d="M300 92 V 128 H 118 V 152" marker-end="url(#ah)"/>
              <path class="flow" id="f-o2r" d="M300 92 V 128 H 118 V 152" marker-end="url(#ah-on)"/>
              <path class="wire" d="M118 221 V 272 H 215 V 298" marker-end="url(#ah)"/>
              <path class="flow" id="f-r2rea" d="M118 221 V 272 H 215 V 298" marker-end="url(#ah-on)"/>
              <path class="wire" d="M291 334 H 379" marker-end="url(#ah)"/>
              <path class="flow" id="f-rea2v" d="M291 334 H 379" marker-end="url(#ah-on)"/>
              <path class="wire" d="M538 334 H 568 V 227" marker-end="url(#ah)"/>
              <path class="flow" id="f-v2a" d="M538 334 H 568 V 227" marker-end="url(#ah-on)"/>
              <path class="wire" d="M462 304 V 62 H 422" marker-end="url(#ah)"/>
              <path class="flow warn" id="f-revise" d="M462 304 V 62 H 422" marker-end="url(#ah-warn)"/>
              <rect class="box ghost" id="n-goal" x="20" y="20" width="130" height="44" rx="3"/>
              <text class="t" x="85" y="41" text-anchor="middle">Goal</text>
              <text class="sub" x="85" y="57" text-anchor="middle">from a person</text>
              <rect class="box" id="n-orch" x="265" y="32" width="150" height="60" rx="3"/>
              <text class="t" x="340" y="61" text-anchor="middle">Orchestrator</text>
              <text class="sub" x="340" y="77" text-anchor="middle">plan &#183; route</text>
              <rect class="box ghost" id="n-mem" x="270" y="156" width="140" height="60" rx="3"/>
              <text class="t" x="340" y="185" text-anchor="middle">Shared memory</text>
              <text class="sub" x="340" y="201" text-anchor="middle">state &#183; traces</text>
              <rect class="box" id="n-ret" x="43" y="155" width="150" height="62" rx="3"/>
              <text class="t" x="118" y="185" text-anchor="middle">Retriever</text>
              <text class="sub" x="118" y="201" text-anchor="middle">search &#183; rank</text>
              <rect class="box" id="n-rea" x="139" y="304" width="152" height="60" rx="3"/>
              <text class="t" x="215" y="333" text-anchor="middle">Reasoner</text>
              <text class="sub" x="215" y="349" text-anchor="middle">draft &#183; revise</text>
              <rect class="box" id="n-ver" x="386" y="304" width="152" height="60" rx="3"/>
              <text class="t" x="462" y="333" text-anchor="middle">Verifier</text>
              <text class="sub" x="462" y="349" text-anchor="middle">check &#183; cite</text>
              <rect class="box" id="n-ans" x="498" y="162" width="140" height="60" rx="3"/>
              <text class="t" x="568" y="191" text-anchor="middle">Answer</text>
              <text class="sub" x="568" y="207" text-anchor="middle">with its trace</text>
              <rect class="box ghost" x="40" y="394" width="600" height="38" rx="3"/>
              <text class="sub" x="340" y="418" text-anchor="middle">Tools &#183; web search &#183; databases &#183; code sandbox &#183; internal APIs</text>
              <text class="cap" x="474" y="140">fails &#8594; retry</text>
            </svg>
        </div>
        <div class="demo-foot">
          <ol class="demo-log" id="demoLog">
            <li><b>orchestrator</b><span>no source exists, so instruct drop</span></li>
            <li><b>reasoner</b><span>drops the unsupported claim</span></li>
            <li class="good"><b>verifier</b><span>all 19 claims match their source</span></li>
            <li class="good"><b>orchestrator</b><span>returns answer, citations and trace</span></li>
          </ol>
          <div class="demo-stats">
            <div><span class="k">Attempt</span><b id="stAttempt">3 of 3</b></div>
            <div><span class="k">Tool calls</span><b id="stCalls">10</b></div>
            <div><span class="k">Tokens</span><b id="stTokens">48.5k</b></div>
            <div><span class="k">Est. cost</span><b id="stCost">$0.32</b></div>
            <div><span class="k">Wall clock</span><b id="stTime">46.5s</b></div>
          </div>
        </div>
        <p class="demo-note">Two failed attempts, one success. Figures are illustrative, at roughly today's frontier-model rates. The retries are the cost, and the verifier is what you are buying.</p>
        <div class="prose" style="margin-top:30px">
          <p>A goal arrives and an <strong>orchestrator</strong> decides what the work actually is: which steps are needed, which specialist handles each one, what to do when one of them fails. Retrieval, reasoning and verification run as separate agents with separate prompts, separate tools and separate failure modes, writing to a <strong>shared memory</strong> the next step can read.</p>
          <p>The interesting edge is the return path. A verifier that rejects a draft sends it back with reasons, and the orchestrator re-plans rather than re-rolls. That is what separates an agentic pipeline from a long prompt: it can notice it was wrong and spend more compute instead of shipping the first plausible answer.</p>
          <p>It is also where the hard problems live. Every extra hop multiplies the ways a run can drift, tool calls have real consequences, and a trace nobody can audit is not a system anyone should deploy in a hospital or a lab. Reliability, evaluation and human oversight run through the whole programme.</p>
          <p class="note"><a href="#run-trace">Read the full step-by-step trace of this run &darr;</a></p>
        </div>
      </div>
    </div>
  </section>"""

VENUE_MAP_BAND = """  <section class="band">
    <div class="wrap band-grid">
      <div class="band-head">
        <p class="eyebrow">Route map</p>
        <h2>Every way in</h2>
        <p>Two metro lines, two stations and one airport, all within a short ride of the gate.</p>
      </div>
      <div>
        <div class="map-wrap">
          <div class="map-scroll-hint" aria-hidden="true"><span>&larr;</span> Swipe map to explore transit routes <span>&rarr;</span></div>
          <svg class="map" viewBox="0 0 860 520" role="img" aria-label="Transit-style map of routes to IIT Delhi from the airport, the railway stations and the Yellow and Magenta metro lines.">
            <g class="compass" transform="translate(792 76)">
              <circle cx="0" cy="0" r="18"/><path d="M0 -13 L5 3 L0 -1 L-5 3 Z" fill="currentColor" stroke="none" style="fill:var(--ink-soft)"/>
            </g>
            <text class="compass-n" x="792" y="46" text-anchor="middle">N</text>

            <path class="road" d="M80 440 L320 440 L360 400 L400 400"/>
            <path class="road-in" d="M80 440 L320 440 L360 400 L400 400"/>
            <path class="line express" d="M80 440 L80 160 L680 160"/>
            <path class="line magenta" d="M160 360 L240 280 L760 280"/>
            <path class="line yellow" d="M680 160 L560 280 L560 440"/>
            <path class="walk" d="M440 280 L400 320 L400 400"/>
            <path class="walk" d="M560 280 L480 360 L420 400"/>

            <circle class="stop" cx="80" cy="440" r="9"/>
            <text class="t" x="80" y="474" text-anchor="middle">IGI Airport</text>
            <text class="t sm" x="80" y="490" text-anchor="middle">T3 &#183; T1</text>

            <circle class="stop" cx="160" cy="360" r="8"/>
            <text class="t sm" x="178" y="356">T1 metro</text>

            <circle class="stop-x" cx="680" cy="160" r="11"/>
            <text class="t" x="680" y="134" text-anchor="middle">New Delhi station</text>
            <text class="t sm" x="680" y="118" text-anchor="middle">Yellow &#183; Express</text>

            <circle class="stop" cx="760" cy="280" r="9"/>
            <text class="t" x="760" y="254" text-anchor="middle">Nizamuddin</text>

            <circle class="stop-x" cx="560" cy="280" r="11"/>
            <text class="t" x="622" y="266">Hauz Khas</text>
            <text class="t sm" x="622" y="250">Yellow &#183; Magenta</text>

            <circle class="stop" cx="440" cy="280" r="9"/>
            <text class="t" x="424" y="250" text-anchor="end">IIT metro</text>
            <text class="t sm" x="424" y="234" text-anchor="end">Magenta</text>

            <circle class="stop" cx="560" cy="440" r="8"/>
            <text class="t sm" x="578" y="444">Saket</text>

            <circle class="venue-ring p1" cx="400" cy="400" r="26"/>
            <circle class="venue-ring p2" cx="400" cy="400" r="26"/>
            <circle class="venue" cx="400" cy="400" r="13"/>
            <text class="t tag" x="400" y="446" text-anchor="middle">You are here</text>
            <text class="t big" x="400" y="470" text-anchor="middle">IIT Delhi</text>
            <text class="t sm" x="400" y="488" text-anchor="middle">Hauz Khas &#183; the venue</text>

            <text class="t sm" x="200" y="424" text-anchor="middle">&#8776;15 km &#183; 30&#8211;60 min</text>
            <text class="t sm" x="96" y="300" transform="rotate(-90 96 300)" text-anchor="middle">Airport Express</text>
            <text class="t sm" x="300" y="306" text-anchor="middle">Magenta Line</text>
            <text class="t sm" x="640" y="214" transform="rotate(45 640 214)" text-anchor="middle">Yellow Line</text>
            <text class="t sm" x="462" y="348" transform="rotate(-38 462 348)">auto &#183; 5 min</text>
          </svg>
        </div>
        <div class="map-key">
          <b><i style="background:#E3A81F"></i>Yellow Line</b>
          <b><i style="background:#9B3D86"></i>Magenta Line</b>
          <b><i style="background:#D4633A"></i>Airport Express</b>
          <b><i style="background:var(--rule)"></i>Road in</b>
          <span>Schematic, not to scale</span>
        </div>
        <p class="note">Nearest stops are IIT (Magenta Line) and Hauz Khas (Yellow and Magenta Lines); both are a five-minute auto-rickshaw ride from the main gate on Sri Aurobindo Marg.</p>
      </div>
    </div>
  </section>"""

TRACE = """        <div class="trace-head">
          <p class="eyebrow">Worked example</p>
          <q>Which papers since 2024 report agents running wet-lab experiments?</q>
        </div>
        <ol class="trace">
          <li><span class="n">01</span><span class="who">orchestrator</span><span class="msg">Splits the question into <b>retrieve &rarr; draft &rarr; verify</b>, and sets the rule that every claim carries a citation.</span><span class="state run">planned</span></li>
          <li><span class="n">02</span><span class="who">retriever</span><span class="msg">Queries arXiv, PubMed and bioRxiv, de-duplicates and ranks what comes back.</span><span class="state ok">38 hits</span></li>
          <li><span class="n">03</span><span class="who">reasoner</span><span class="msg">Drafts a six-paragraph summary, each claim tagged to the source it came from.</span><span class="state ok">drafted</span></li>
          <li><span class="n">04</span><span class="who">verifier</span><span class="msg">Re-reads every cited paper against the claim made about it. Two claims are not supported by their source.</span><span class="state warn">2 failed</span></li>
          <li class="redo"><span class="n">05</span><span class="who">orchestrator</span><span class="msg">Keeps the eighteen claims that held. Re-queries only the two that did not, instead of starting again.</span><span class="state warn">revise</span></li>
          <li><span class="n">06</span><span class="who">retriever</span><span class="msg">Finds a genuine source for one claim. For the other there is nothing to find.</span><span class="state warn">1 of 2</span></li>
          <li><span class="n">07</span><span class="who">reasoner</span><span class="msg">Rewrites one paragraph and drops the claim that nothing supports.</span><span class="state ok">redrafted</span></li>
          <li><span class="n">08</span><span class="who">verifier</span><span class="msg">Every remaining claim now matches its source.</span><span class="state ok">passed</span></li>
          <li><span class="n">09</span><span class="who">orchestrator</span><span class="msg">Returns the summary, the citations, and a note saying what was dropped and why.</span><span class="state ok">done</span></li>
        </ol>"""

PARTICIPATE_BAND = """  <section class="band alt" id="take-part">
    <div class="wrap band-grid">
      <div class="band-head">
        <p class="eyebrow">Take part</p>
        <h2>Three ways in</h2>
        <p>Come and listen, bring your own research, or put what you are building in front of the room.</p>
      </div>
      <div>
        <div class="take-grid">
          <article class="take">
            <div class="take-body">
              <h3>Attend</h3>
              <p>Talks, panels, tutorials and live demos across two days. Free, with places confirmed by the committee.</p>
              <a class="btn btn-go" href="https://forms.gle/HHtuspnAUSAGpwxS9" target="_blank" rel="noopener noreferrer">Register to attend</a>
            </div>
          </article>
          <article class="take">
            <div class="take-body">
              <h3>Present a poster</h3>
              <p>arXiv preprints and papers under submission, on the broader theme of agentic AI.</p>
              <a class="btn btn-go" href="https://forms.gle/W6U7YbLqxAHPparc8" target="_blank" rel="noopener noreferrer">Submit a poster</a>
            </div>
          </article>
          <article class="take">
            <div class="take-body">
              <h3>Industry kiosk</h3>
              <p>A kiosk puts your products, prototypes and open roles in front of the room across both days.</p>
              <a class="btn btn-go" data-link="kiosk" href="partners.html">Request a kiosk</a>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>"""

SPONSOR_BAND = """  <section class="band sponsor-strip" id="sponsors">
    <div class="wrap sponsor-strip-in">
      <p class="sponsor-eyebrow"><i></i>Organising Industry Partner<i></i></p>
      <div class="sponsor-card"><img class="sponsor-logo" src="photos/infoorigin-logo.png" alt="InfoOrigin" width="1024" height="365" loading="lazy"></div>
      <p class="sponsor-note">Presented in partnership with <b>InfoOrigin</b> &middot; <a href="partners.html">Partners &amp; sponsors &rarr;</a></p>
    </div>
  </section>"""

HOME_FAQ = """  <section class="band" id="faq">
    <div class="wrap band-grid">
      <div class="band-head">
        <h2>FAQs</h2>
      </div>
      <div>
        <div class="faq">
          <details open><summary>Who can attend?</summary><p>Researchers, faculty, students, industry practitioners, startups and investors working on or around agentic AI. Places are limited, so every registration is reviewed and confirmed by the organising committee.</p></details>
          <details><summary>Is there a registration fee?</summary><p>No. Attendance is free. If any fees are introduced for particular categories, they will be announced on the <a href="register.html">registration page</a>.</p></details>
          <details><summary>Will I know my registration went through?</summary><p>Yes. Submitting the form sends you a copy of your responses immediately, and a separate e-mail from the committee confirms whether a place is available.</p></details>
          <details><summary>Can I present my work?</summary><p>The poster session is open to arXiv preprints and papers under submission on the broader theme of agentic AI. Answer &ldquo;Yes&rdquo; to the poster question when you register.</p></details>
          <details><summary>What should I bring to the tutorials?</summary><p>A laptop for most of them. Software and account prerequisites are published with each session once the <a href="tutorials.html">line-up</a> is final.</p></details>
          <details><summary>How do I get to campus?</summary><p>IIT Delhi is in Hauz Khas, South Delhi, about 15&nbsp;km from the airport and a short ride from the IIT and Hauz Khas metro stations. See <a href="venue.html">venue and travel</a>.</p></details>
        </div>
        <p class="note">More on fees, deadlines and accommodation in the <a href="register.html#faq">full FAQ</a>.</p>
      </div>
    </div>
  </section>"""

# ---------------------------------------------------------------- pages
pages = {}

pages["index.html"] = ("Agentic AI Workshop 2026", None, """  <section class="hero">
    <div class="hero-bg" aria-hidden="true"></div>
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <h1>Agentic&nbsp;AI<br>Workshop <em>2026</em></h1>
        <p class="hero-meta"><strong>15&ndash;16 December 2026</strong> <span class="hero-sep">|</span> <strong>Venue: IIT Delhi, Hauz Khas, New Delhi 110016</strong></p>
        <p class="hero-desc">Bringing together Academia and Industry leaders to explore Agentic AI innovations in Healthcare, Enterprise AI, and AI for Science.</p>
      </div>
      <div class="hero-panel">
        <div class="hero-panel-head">
          <p class="hero-eyebrow">PARTICIPATE</p>
          <h2>Three ways in</h2>
        </div>
        <div class="hero-cards">
          <div class="hero-card">
            <h3>Attend</h3>
            <p>Talks, panels, tutorials and live demos across two days. Free, with places confirmed by the committee.</p>
            <a class="hero-card-btn" href="https://forms.gle/HHtuspnAUSAGpwxS9" target="_blank" rel="noopener noreferrer">Register to attend &rarr;</a>
          </div>
          <div class="hero-card">
            <h3>Present a poster</h3>
            <p>arXiv preprints and papers under submission, on the broader theme of agentic AI.</p>
            <a class="hero-card-btn" href="https://forms.gle/W6U7YbLqxAHPparc8" target="_blank" rel="noopener noreferrer">Submit a poster &rarr;</a>
          </div>
          <div class="hero-card">
            <h3>Industry kiosk</h3>
            <p>A kiosk puts your products, prototypes and open roles in front of the room across both days.</p>
            <a class="hero-card-btn" href="partners.html">Request a kiosk &rarr;</a>
          </div>
        </div>
      </div>
    </div>
    <p class="hero-credit">IIT Delhi, Hauz Khas</p>
  </section>

""" + SPONSOR_BAND + "\n\n" + band("Speakers", "Eleven, and counting",
                "Eleven confirmed across universities, corporate research labs, hospitals and startups. More to come, and two panel discussions on the way.",
                orbit_block("The ring moves through all eleven speakers. Hover or tap any portrait to hold it there.")
                + '\n        <p class="note"><a href="speakers.html">Full profiles and the panel discussions &rarr;</a></p>')
+ "\n\n" + band("Themes", "Where agents earn their keep",
           "What can agents actually do for us? Talks, tutorials and demos are organised around three answers.",
           """        <div class="rows">
          <article class="row-item"><div class="num">01</div><div>
            <h3>Agentic AI in Healthcare</h3>
            <p>Agents that support clinicians and patients: triaging, summarising records, coordinating care and accelerating diagnostics, built to be safe, fair and accountable.</p>
          </div></article>
          <article class="row-item"><div class="num">02</div><div>
            <h3>Agentic AI for Scientific Discovery</h3>
            <p>AI scientists that read the literature, generate hypotheses, design and run experiments and analyse results, closing the loop from idea to insight.</p>
          </div></article>
          <article class="row-item"><div class="num">03</div><div>
            <h3>Agentic AI and Enterprise</h3>
            <p>From prototype to product: building, funding and scaling agentic AI ventures, and the business models that agents make possible.</p>
          </div></article>
        </div>
        <p class="note"><a href="about.html">Read how the three themes shape the programme &rarr;</a></p>""", bid="themes")
+ "\n\n" + band("Registration", "Save your seat",
                "Free, and it takes about two minutes. Every registration is reviewed by the organising committee.",
                """        <div class="reg-box">
          <div>
            <h3>Workshop registration</h3>
            <p>Free &middot; limited places &middot; open until seats are filled</p>
          </div>
          <a class="btn" href="register.html">How registration works</a>
        </div>
        <p class="note">Submitting the form sends you a copy of your responses straight away; the committee confirms your place by e-mail afterwards.</p>""", alt=True)
+ "\n\n" + HOME_FAQ)

pages["about.html"] = ("About the Workshop", "about.html",
    page_head("About", "About the workshop", "Why agentic AI, and why now?",
              "Where autonomous AI agents meet healthcare, science and entrepreneurship.")
    + "\n\n" + band("Why this workshop", "From answering to acting",
                    "The shift that makes this the right moment.",
                    """        <div class="prose">
          <p>AI systems are moving from answering questions to <strong>taking actions</strong>: planning multi-step tasks, using tools, collaborating with people and with other agents, and learning from feedback. The shift opens real opportunities and raises hard questions about reliability, safety and accountability.</p>
          <p>The Agentic AI Workshop 2026 brings researchers, practitioners, founders and investors to IIT Delhi to take stock of where agentic AI stands, where it is heading, and how it can create real impact in healthcare, scientific discovery and entrepreneurship.</p>
          <p><strong>Agentic AI</strong> describes systems that pursue goals with a degree of autonomy. Rather than producing a single response, an agent runs a loop, usually with a large language model as its reasoning engine, combined with memory, tool use and human oversight.</p>
          <ol class="loop">
            <li><div class="n">01</div><h4>Perceive</h4><p>Takes in the goal and its surroundings: requests, documents, sensor data, tool output.</p></li>
            <li><div class="n">02</div><h4>Reason</h4><p>Works out what the goal requires and what it still needs to know.</p></li>
            <li><div class="n">03</div><h4>Plan</h4><p>Breaks the goal into a sequence of steps it can carry out.</p></li>
            <li><div class="n">04</div><h4>Act</h4><p>Calls tools and APIs, writes to systems, or delegates to other agents.</p></li>
            <li><div class="n">05</div><h4>Reflect</h4><p>Checks the outcome against the goal and revises before trying again.</p></li>
          </ol>
        </div>""")
    + "\n\n" + LOOP_BAND
    + "\n\n" + band("A run, step by step", "What one task actually costs",
                    "An illustrative trace of a single question moving through the pipeline.",
                    '''%s''' % TRACE, bid="run-trace")
    + "\n\n" + band("Audience", "Who is in the room", "The room is deliberately mixed.",
                    """        <div class="cards">
          <div><h4>Researchers &amp; faculty</h4><p>Share and discover advances in agents, planning and multi-agent systems.</p></div>
          <div><h4>Students</h4><p>Learn hands-on in tutorials, meet mentors, and present a poster.</p></div>
          <div><h4>Industry practitioners</h4><p>See what works in production and connect with research teams.</p></div>
          <div><h4>Startups &amp; founders</h4><p>Showcase your product at the kiosks and meet collaborators.</p></div>
          <div><h4>Investors</h4><p>Spot emerging agentic AI ventures and the talent behind them.</p></div>
        </div>""", alt=True)
    + "\n\n" + band("Two days", "Six ways in",
                    "Six formats across 15 and 16 December.",
                    """        <div class="cards">
          <a href="speakers.html"><h4>Invited talks</h4><p>Keynotes and talks from leading academic and industry voices.</p></a>
          <a href="speakers.html#panels"><h4>Panel discussions</h4><p>Debates on the opportunities, risks and the road ahead.</p></a>
          <a href="tutorials.html"><h4>Tutorials</h4><p>Hands-on sessions on building and evaluating agents.</p></a>
          <a href="tutorials.html#demos"><h4>Live demos</h4><p>Agents in action, from research labs and companies.</p></a>
          <a href="partners.html"><h4>Industry kiosks</h4><p>Meet companies showcasing agentic technology.</p></a>
        </div>"""))

pages["programme.html"] = ("Programme", "programme.html",
    page_head("Programme", "Programme", "From the first gavel to the last demo",
              "Join us on 15&ndash;16 December 2026 at IIT Delhi for two days of insightful discussions, expert talks, and exploration of the future of Agentic AI.")
    + "\n\n" + band("Schedule", "Hour by hour",
                    "Session titles, rooms and speakers appear here as they are confirmed.",
                    '        <h3 class="day-title">Day 1 &middot; Tuesday, 15 December</h3>\n'
                    '        <p class="day-sub">09:00 &ndash; 21:30 IST</p>\n' + sched(DAY1)
                    + '\n        <h3 class="day-title">Day 2 &middot; Wednesday, 16 December</h3>\n'
                    '        <p class="day-sub">08:00 &ndash; 14:30 IST &middot; afternoon sessions to be announced</p>\n' + sched(DAY2)
                    + '\n        <p class="note">Five tutorial and demo tracks run in parallel on Day 2 from 13:15.</p>')
    + "\n\n" + band("Formats", "Six kinds of session", "Six kinds of session run across the two days.",
                    FORMATS.replace('<div class="formats">', '<div class="formats" style="border-top:0;padding-top:0;margin-top:0">'), alt=True)
    + "\n\n" + band("Kiosks", "Meet the companies building agents",
                    "Industry kiosks run alongside the sessions on both days.",
                    """        <div class="prose">
          <p>Kiosks give companies and startups a space to showcase agentic AI products, research prototypes and career opportunities to a highly engaged audience.</p>
        </div>
        <div class="soon" style="margin-top:22px">
          <h3>Exhibitor line-up coming soon</h3>
          <p>Participating companies and the agentic technology they showcase will be listed here.</p>
          <p style="margin-top:14px"><a class="btn btn-ghost btn-sm" href="partners.html">Exhibit with us</a></p>
        </div>""", bid="kiosks")
    + "\n\n" + band("Plan your visit", "Before you set off", "Everything needed for the trip.",
                    """        <div class="cards">
          <a href="venue.html"><h4>Venue &amp; travel</h4><p>Maps, directions from the airport and stations, and places to stay.</p></a>
          <a href="register.html"><h4>Registration</h4><p>Free, reviewed by the committee. Save your seat.</p></a>
          <a href="tutorials.html"><h4>Tutorials &amp; demos</h4><p>Levels, prerequisites and materials for the hands-on sessions.</p></a>
          <a href="speakers.html"><h4>Speakers</h4><p>Who is speaking, their talks and the panels.</p></a>
        </div>""", alt=True))

pages["speakers.html"] = ("Speakers & Panels", "speakers.html",
    page_head("Speakers", "Speakers", "Distinguished Speakers",
              "Fourteen researchers, practitioners and founders building agentic AI across universities, corporate research labs, hospitals and startups.")
    + "\n\n" + band("Profiles", "Who is speaking",
                    "Each profile fills in as speakers send their talk titles and biographies.",
                    '''        <div class="bios">
          <article class="bio">
            <div class="bio-photo"><img src="photos/ganguli.webp" alt="Prof. Surya Ganguli" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Prof. Surya Ganguli</h3>
              <p class="role">Associate Professor of Applied Physics</p>
              <p class="org">Stanford University</p>
              <p class="bio-copy">Bridges theoretical physics, neuroscience, and machine learning at Stanford. His research investigates the mathematical foundations of deep neural networks, neural dynamics, and scaling laws to understand biological and artificial intelligence.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/manik.webp" alt="Prof. Manik Varma" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Prof. Manik Varma</h3>
              <p class="role">Technical Fellow &amp; Corporate Vice President</p>
              <p class="org">Microsoft Research India</p>
              <p class="bio-copy">Technical Fellow at Microsoft Research India and Adjunct Professor at IIT Delhi. He pioneered extreme multi-label classification, developing scalable machine learning algorithms widely deployed in global web search and recommendation systems.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/nanda.webp" alt="Dr. Nanda Kishore Kambhatla" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dr. Nanda Kishore Kambhatla</h3>
              <p class="role">Head of Adobe Research Lab</p>
              <p class="org">Adobe Research, India</p>
              <p class="bio-copy">Heads Adobe Research India, driving research in natural language processing, conversational AI, and content intelligence. He previously led machine learning and dialogue systems initiatives at IBM Research for IBM Watson.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/balaji.webp" alt="Dr. Balaji Vasan Srinivasan" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dr. Balaji Vasan Srinivasan</h3>
              <p class="role">Principal Scientist</p>
              <p class="org">Adobe Research, India</p>
              <p class="bio-copy">Principal Scientist at Adobe Research India specializing in multimodal artificial intelligence, generative models, and computer vision. His work advances text-to-image synthesis, automated layout generation, and AI-assisted creative workflows.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/prashant.webp" alt="Dr. Prashant Warier" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dr. Prashant Warier</h3>
              <p class="role">Co-Founder &amp; Chief Executive Officer</p>
              <p class="org">Qure.ai</p>
              <p class="bio-copy">Co-Founder and CEO of Qure.ai and an IIT Delhi alumnus. He develops deep learning diagnostic algorithms for medical imaging, deploying automated screening solutions for tuberculosis, stroke, and lung cancer across over 100 countries.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/patra.webp" alt="Dr. Arijit Patra" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dr. Arijit Patra</h3>
              <p class="role">Senior Principal Scientist</p>
              <p class="org">UCB Pharma</p>
              <p class="bio-copy">Senior Principal Scientist at UCB Pharma and Rhodes Scholar from Oxford. He focuses on artificial intelligence for biomedical imaging, non-clinical drug safety workflows, and machine learning pipelines that accelerate therapeutic discovery.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/nitish.webp" alt="Dr. Nitish Naik" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dr. Nitish Naik</h3>
              <p class="role">Professor of Cardiology</p>
              <p class="org">AIIMS, New Delhi</p>
              <p class="bio-copy">Professor of Cardiology at AIIMS, New Delhi, and Padma Shri recipient. His work encompasses interventional cardiology, cardiovascular diagnostics, and the rigorous, clinically validated translation of artificial intelligence technologies into patient care.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/kartik.webp" alt="Prof. Karthik Raman" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Prof. Karthik Raman</h3>
              <p class="role">Professor, Data Science and AI, and Biotechnology</p>
              <p class="org">IIT Madras</p>
              <p class="bio-copy">Professor at IIT Madras across Data Science and Biotechnology, and coordinator of IBSE. His research integrates computational systems biology, metabolic modeling, and biological network analysis to investigate complex disease mechanisms.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/raghu.webp" alt="Prof. Raghunathan Rengaswamy" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Prof. Raghunathan Rengaswamy</h3>
              <p class="role">Professor, Data Science and AI, and Chemical Engineering</p>
              <p class="org">IIT Madras</p>
              <p class="bio-copy">Marti Mannariah Gurunath Chair Professor at IIT Madras. His research focuses on process systems engineering, fault detection and diagnosis, reinforcement learning, and combining first-principles physical models with data-driven analytics.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/deepak.webp" alt="Dr. Deepak N. Subramani" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dr. Deepak N. Subramani</h3>
              <p class="role">Associate Professor, Computational and Data Sciences</p>
              <p class="org">IISc Bangalore</p>
              <p class="bio-copy">Associate Professor at IISc Bangalore and MIT alumnus leading the QUEST Lab. His research focuses on physics-informed machine learning, autonomous robotic navigation, ocean forecasting, and Bayesian uncertainty quantification.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/ashutosh.webp" alt="Prof. Ashutosh Modi" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Prof. Ashutosh Modi</h3>
              <p class="role">Associate Professor, Computer Science and Engineering</p>
              <p class="org">IIT Kanpur</p>
              <p class="bio-copy">Associate Professor of Computer Science at IIT Kanpur. He specializes in natural language processing, affective computing, multimodal dialogue systems, and legal AI, developing models for machine comprehension and emotion recognition.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/aparna.webp" alt="Aparna Taneja" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Aparna Taneja</h3>
              <p class="role">Senior Research Scientist</p>
              <p class="org">Google DeepMind</p>
              <p class="bio-copy">Senior Research Scientist at Google DeepMind India. She leads research in artificial intelligence for social impact, developing restless multi-armed bandits and predictive machine learning models to improve maternal and public health.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/dinesh.webp" alt="Dinesh Raghu" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Dinesh Raghu</h3>
              <p class="role">Senior Researcher and Manager, Agentic AI</p>
              <p class="org">IBM</p>
              <p class="bio-copy">Senior Researcher and Manager in Agentic AI at IBM Research India. He leads research on autonomous agents, function calling in IBM Granite foundation models, multi-turn reasoning, and task-oriented conversational workflows.</p>
            </div>
          </article>
          <article class="bio">
            <div class="bio-photo"><img src="photos/nitendra.webp" alt="Nitendra Rajput" width="520" height="520" loading="lazy"></div>
            <div class="bio-text">
              <h3>Nitendra Rajput</h3>
              <p class="role">Vice President and Head of AI Garage Center</p>
              <p class="org">Mastercard</p>
              <p class="bio-copy">Vice President and Head of the AI Garage at Mastercard, and ACM Distinguished Scientist. He directs global AI research and deployment in financial security, fraud prevention, risk mitigation, and emerging agentic commerce.</p>
            </div>
          </article>
        </div>''')
    + "\n\n" + band("Panels", "Two arguments worth having",
                    "Academia and industry on where agents are heading.",
                    """        <div class="sched">
          <div class="sched-row is-flag"><div class="t">15:00 &ndash; 16:30</div><div class="s">Panel discussion 1<small>Panelists to be announced</small></div><div class="k">Panel</div><div class="r">TBA</div></div>
          <div class="sched-row is-flag"><div class="t">18:00 &ndash; 19:30</div><div class="s">Panel discussion 2<small>Five or six panelists, to be announced</small></div><div class="k">Panel</div><div class="r">TBA</div></div>
        </div>
        <p class="note">Both panels run on Tuesday, 15 December. See the full <a href="programme.html">programme</a>.</p>""",
                    alt=True, bid="panels"))

pages["tutorials.html"] = ("Tutorials & Demos", "tutorials.html",
    page_head("Tutorials &amp; demos", "Tutorials &amp; demos", "Hands on the keyboard",
              "Hands-on sessions on building and evaluating agents, plus live demos from research labs and companies. Check prerequisites before you arrive.")
    + "\n\n" + band("Tutorials", "Build one yourself",
                    "Five parallel tracks run on Day 2 from 13:15.",
                    """        <div class="soon">
          <h3>Tutorial line-up coming soon</h3>
          <p>Titles, instructors, prerequisites (laptop, software, accounts) and material links will be published here as sessions are confirmed.</p>
        </div>
        <p class="note">Most tutorials need a laptop. Prerequisites are listed with each session once the line-up is final, and registered attendees get them by e-mail beforehand.</p>""")
    + "\n\n" + band("Live demos", "Agents in action",
                    "Running systems, shown working on real problems.",
                    """        <div class="soon">
          <h3>Demo list coming soon</h3>
          <p>Teams and companies demonstrating agents live will be listed here.</p>
        </div>
        <p class="note">Showing something you have built? Write to the organisers, or mention it when you <a href="register.html">register</a>.</p>""",
                    alt=True, bid="demos"))

pages["venue.html"] = ("Venue & Travel", "venue.html",
    page_head("Venue &amp; travel", "Venue &amp; travel", "Getting to IIT Delhi",
              "Indian Institute of Technology Delhi, Hauz Khas, New Delhi 110016. The hall is to be announced and will be e-mailed to confirmed attendees.")
    + '\n\n  <div class="strip"><img src="photos/iitd-campus-wide.webp" alt="The main building at IIT Delhi, Hauz Khas" width="1400" height="820" loading="lazy"></div>'
    + "\n\n" + VENUE_MAP_BAND
    + "\n\n" + band("Routes", "Getting to campus",
                    "Travel times are approximate and depend heavily on traffic.",
                    """        <dl class="routes">
          <div class="route"><dt>From the airport</dt><dd>Indira Gandhi International (DEL) is about 15&nbsp;km away, roughly 30&ndash;60 minutes by taxi. Prepaid taxis and app cabs are at every terminal. The Magenta Line runs from Terminal 1 and the Airport Express from Terminal 3.</dd></div>
          <div class="route"><dt>From the stations</dt><dd>New Delhi and Hazrat Nizamuddin are 12&ndash;16&nbsp;km away, roughly 40&ndash;60 minutes by taxi. From New Delhi station the Yellow Line runs directly to Hauz Khas.</dd></div>
          <div class="route"><dt>By metro</dt><dd>Nearest stations are IIT (Magenta Line) and Hauz Khas (Yellow and Magenta Lines). From either, a short auto-rickshaw or cab ride reaches campus. The DMRC journey planner gives the best route.</dd></div>
          <div class="route"><dt>By road</dt><dd>The campus sits in Hauz Khas, South Delhi. App cabs and autos are widely available; allow extra time at peak hours. Visitor parking on campus is limited.</dd></div>
          <div class="route"><dt>Campus entry</dt><dd>IIT Delhi is a secured campus. Bring a valid government photo ID and the registration ID e-mailed to you. The exact hall, entry gate and visitor-pass details are posted here and e-mailed before the workshop.</dd></div>
        </dl>
        <p class="note"><a class="btn btn-ghost btn-sm" href="https://www.google.com/maps/search/?api=1&amp;query=Indian%20Institute%20of%20Technology%20Delhi%2C%20Hauz%20Khas%2C%20New%20Delhi" target="_blank" rel="noopener">Open in Google Maps</a></p>"""))

pages["register.html"] = ("Registration", "register.html",
    page_head("Registration", "Registration", "Save your seat",
              "Free to attend, and it takes about two minutes. Places are limited, so every registration is reviewed and confirmed by the organising committee.")
    + "\n\n" + band("How it works", "Three steps, two minutes", "One form covers attendance and the poster session.",
                    """        <div class="steps">
          <article class="step"><div>
            <h3>Fill in the registration form</h3>
            <p>Name, e-mail, institution and what you do, then your interests and logistics. The same form asks whether you want to present a poster, so one submission covers both.</p>
          </div></article>
          <article class="step"><div>
            <h3>You get an acknowledgement straight away</h3>
            <p>A copy of your responses arrives by e-mail the moment you submit, so you have a record of what you entered. If it does not appear within a few minutes, check your spam folder before writing to us.</p>
          </div></article>
          <article class="step"><div>
            <h3>The committee confirms your place</h3>
            <p>Registrations are reviewed in batches. You will hear by e-mail whether we can offer you a place, along with the hall, the schedule and campus entry instructions.</p>
          </div></article>
        </div>
        <div class="reg-box">
          <div>
            <h3>Workshop registration</h3>
            <p>Free &middot; limited places &middot; about two minutes</p>
          </div>
          <a class="btn" data-link="register" href="#">Open the registration form</a>
        </div>""")
    + "\n\n" + band("Who registers", "Who comes, and what it costs",
                    "Attendance is free; any fees would be announced here first.",
                    """        <dl class="routes">
          <div class="route"><dt>You are a&hellip;</dt><dd>Student &middot; Researcher or postdoc &middot; Faculty &middot; Industry practitioner &middot; Startup founder or team &middot; Investor &middot; Other</dd></div>
          <div class="route"><dt>Students</dt><dd class="tba">Fee to be announced</dd></div>
          <div class="route"><dt>Academia &amp; researchers</dt><dd class="tba">Fee to be announced</dd></div>
          <div class="route"><dt>Industry &amp; startups</dt><dd class="tba">Fee to be announced</dd></div>
          <div class="route"><dt>Workshop deadline</dt><dd class="tba">To be announced</dd></div>
        </dl>""", alt=True)
    + "\n\n" + band("Posters", "Bring your research",
                    "The poster session runs over lunch on Day 1.",
                    """        <div class="prose">
          <p>The poster session is open to arXiv preprints and papers currently under submission, on the broader theme of agentic AI. To present, answer &ldquo;Yes&rdquo; to the poster question in the registration form and give your title and abstract.</p>
        </div>
        <p style="margin-top:18px"><a class="btn" data-link="poster" href="#">Submit a poster</a></p>
        <p class="note">Posters are displayed during the lunch and poster session, 13:15&ndash;15:00 on Tuesday, 15 December.</p>""", bid="posters")
    + "\n\n" + band("FAQ", "Questions, answered", "Anything else, write to the organisers.",
                    """        <div class="faq">
          <details open><summary>Who can attend?</summary><p>Researchers, faculty, students, industry practitioners, startups and investors working on or around agentic AI. Places are limited, so registrations are reviewed and confirmed by the organising committee.</p></details>
          <details><summary>Is there a registration fee?</summary><p>Attendance is free. If any fees are introduced for particular categories, they will be announced on this page.</p></details>
          <details><summary>Will I know my registration went through?</summary><p>Yes. Submitting the form sends you a copy of your responses immediately. A separate e-mail from the committee confirms whether a place is available.</p></details>
          <details><summary>When will the detailed schedule be available?</summary><p>The draft schedule is already on the <a href="programme.html">programme page</a>. Session titles and speakers are filled in as they confirm, and registered attendees get the final version by e-mail.</p></details>
          <details><summary>What should I bring to the tutorials?</summary><p>A laptop for most of them. Software and account prerequisites are published with each tutorial once the line-up is final.</p></details>
          <details><summary>Will the talks be recorded?</summary><p>Selected slides and recordings may be shared on this site after the event, with each speaker's permission.</p></details>
          <details><summary>Is accommodation provided?</summary><p>Not unless announced otherwise. The <a href="venue.html">venue page</a> gives directions and campus entry details, and a limited number of guest-house rooms may be available on request.</p></details>
          <details><summary>How can my company exhibit or sponsor?</summary><p>See <a href="partners.html">partners and sponsors</a> for the tiers, or write to the organisers and we will talk it through.</p></details>
        </div>""", alt=True))

pages["partners.html"] = ("Partners & Sponsors", "partners.html",
    page_head("Partners", "Partners &amp; sponsors", "Put your work in front of the room",
              "Sponsors and exhibitors reach researchers and faculty, students, industry practitioners, startups and investors over two days on campus.")
    + "\n\n" + band("Tiers", "Four ways to put your name on it", "Each tier is priced on request. Choose one, or get in touch to talk it through.",
                    """        <div class="tiers">
          <article class="tier"><div>
            <h3>Title partner</h3>
            <p>Prominent branding across the venue and website, a speaking slot in the opening session, premium kiosk space, and a named session track.</p>
          </div><div class="price">On request</div></article>
          <article class="tier"><div>
            <h3>Platinum</h3>
            <p>Logo on the website, banners and schedule; kiosk space at the venue; access to student and research talent.</p>
          </div><div class="price">On request</div></article>
          <article class="tier"><div>
            <h3>Gold</h3>
            <p>Logo on the website and banners, with kiosk space in the shared zone.</p>
          </div><div class="price">On request</div></article>
          <article class="tier"><div>
            <h3>Academic &amp; community partners</h3>
            <p>Logo on the website and outreach to your community.</p>
          </div><div class="price">On request</div></article>
        </div>""")
    + "\n\n" + band("Kiosks", "Take a kiosk",
                    "A booth on both days, beside the sessions.",
                    """        <div class="prose">
          <p>An industry kiosk gives your team a space to show what you are building with agents: products, research prototypes and the roles you are hiring for. Kiosks run alongside the talks on both days, with traffic concentrated around the breaks and the poster session.</p>
        </div>
        <div class="sponsor-strip-in" style="align-items:flex-start;text-align:left;margin-top:22px;gap:16px">
          <div class="sponsor-card"><img class="sponsor-logo" src="photos/infoorigin-logo.png?v=2" alt="InfoOrigin" width="344" height="160" loading="lazy"></div>
          <p class="sponsor-note"><b>InfoOrigin</b> is the title sponsor of the Agentic AI Workshop 2026. Further partners and exhibitors will be listed here as agreements are signed.</p>
        </div>""", alt=True)
    + "\n\n" + band("Get in touch", "Become a partner",
                    "Tell us which tier fits and we will share what each one includes.",
                    """        <div class="reg-box">
          <div>
            <h3>Talk to the organising committee</h3>
            <p>Sponsorship, kiosks and academic partnerships are all handled by the committee.</p>
          </div>
          <a class="btn" data-link="kiosk" href="#">Request a kiosk</a>
        </div>"""))

pages["organisers.html"] = ("Organisers", "organisers.html",
    page_head("Organisers", "The team", "Organisers",
              "The Agentic AI Workshop 2026 is organised by the Yardi School of Artificial Intelligence (ScAI), IIT Delhi.</p>\n        <p>Our Industry Partner &mdash; Info Origin")
    + "\n\n" + band("The team", "The people running it",
                    "Faculty organisers, student organisers and volunteers.",
                    """        <div class="org-group">
          <h3>Faculty Organisers</h3>
          <div class="org-grid">
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/sandeep-kumar.jpg" alt="Prof. Sandeep Kumar" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Prof. Sandeep Kumar</h4>
                <p class="org-card-affil">IIT Delhi</p>
              </div>
            </article>
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/souvik-chakraborty.jpg" alt="Prof. Souvik Chakraborty" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Prof. Souvik Chakraborty</h4>
                <p class="org-card-affil">IIT Delhi</p>
              </div>
            </article>
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/tanmoy-chakraborty.jpg" alt="Prof. Tanmoy Chakraborty" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Prof. Tanmoy Chakraborty</h4>
                <p class="org-card-affil">IIT Delhi</p>
              </div>
            </article>
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/parag-singla.jpg" alt="Prof. Parag Singla" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Prof. Parag Singla</h4>
                <p class="org-card-affil">IIT Delhi</p>
              </div>
            </article>
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/mausam.jpg" alt="Prof. Mausam" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Prof. Mausam</h4>
                <p class="org-card-affil">IIT Delhi</p>
              </div>
            </article>
          </div>
        </div>
        <div class="org-group">
          <h3>Student Organisers</h3>
          <div class="org-grid">
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/abhishek-gupta.jpg" alt="Abhishek Gupta" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Abhishek Gupta</h4>
                <p class="org-card-role">PhD Scholar,</p>
                <p class="org-card-affil">Yardi School of AI,<br>IIT Delhi</p>
              </div>
            </article>
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/aditya-shahane.jpg" alt="Aditya Shahane" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Aditya Shahane</h4>
                <p class="org-card-role">PhD Scholar,</p>
                <p class="org-card-affil">Electrical Engineering,<br>IIT Delhi</p>
              </div>
            </article>
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/ajeet-singh.jpg" alt="Ajeet Kumar Singh" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Ajeet Kumar Singh</h4>
                <p class="org-card-role">PhD Scholar,</p>
                <p class="org-card-affil">School of Interdisciplinary<br>Research, IIT Delhi</p>
              </div>
            </article>
          </div>
        </div>
        <div class="org-group">
          <h3>Collaborating Partner</h3>
          <div class="org-grid">
            <article class="org-card organiser-card">
              <div class="org-card-photo">
                <img src="photos/anurag-tripathi.jpg" alt="Anurag Tripathi" width="76" height="76" loading="lazy">
              </div>
              <div class="org-card-info">
                <h4 class="org-card-name">Anurag Tripathi</h4>
                <p class="org-card-affil">Info Origin</p>
              </div>
            </article>
          </div>
        </div>
        <div class="org-group">
          <h3>Volunteers</h3>
          <div class="org-list">
            <div class="org"><b>Joining us soon</b><span>Want to help run the workshop? Write to the organisers.</span></div>
          </div>
        </div>""")
    + "\n\n" + band("Contact", "Reach the organisers",
                    "For speaking, sponsorship, volunteering or anything about attending.",
                    """        <div class="reg-box">
          <div>
            <h3>Contact the committee</h3>
            <p>For workshop-related queries, collaborations, and general enquiries, please contact the organising committee.</p>
          </div>
          <span class="tba" data-contact>agenticai.iitd@gmail.com</span>
        </div>""", alt=True))


def write_page(fname, title, current, body):
    head_html = header(current)
    if fname == "index.html":
        doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               '<meta name="claude:viewport-fit-sides" content="cover">\n'
               '<title>%s</title>\n%s\n'
               '<link rel="stylesheet" href="styles.css?v=2">\n%s\n</head>\n<body>\n\n%s\n\n<main>\n%s\n</main>\n\n%s\n</body>\n</html>\n'
               % (title, FONTS, EARLY_THEME, head_html, body, FOOTER))
    else:
        doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               '<title>%s &middot; Agentic AI Workshop 2026</title>\n%s\n'
               '<link rel="stylesheet" href="styles.css?v=2">\n%s\n</head>\n<body>\n\n%s\n\n<main>\n%s\n</main>\n\n%s\n</body>\n</html>\n'
               % (title, FONTS, EARLY_THEME, head_html, body, FOOTER))
    io.open(os.path.join(OUT, fname), "w", encoding="utf-8").write(doc)
    return len(doc)


if __name__ == '__main__':
    import sys
    if '--build' not in sys.argv:
        print("Safety guard: To regenerate static HTML files from build_site.py, run with '--build'.")
        sys.exit(0)
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for fname, (title, current, body) in pages.items():
        if fname == "index.html": continue
        n = write_page(fname, title, current, body)
        total += n
        print("%-20s %6d bytes" % (fname, n))
    print("total", total)
