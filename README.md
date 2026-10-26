# Agentic AI Workshop 2026 — website

The website for the Agentic AI Workshop 2026, organised by the Indian Institute
of Technology Delhi and the Yardi School of Artificial Intelligence (ScAI).

**15–16 December 2026 · IIT Delhi, Hauz Khas, New Delhi**

Ten pages of plain HTML, CSS and JavaScript. No framework, no build step, no
dependencies. Open `static/index.html` in a browser and it works.

---

## 1. The one file you need to edit

Paste your Google Form URLs into **`static/config.js`**:

```js
window.AAIW_LINKS = {
  register: "https://forms.gle/your-registration-form",
  poster:   "https://forms.gle/your-poster-form",
  kiosk:    "https://forms.gle/your-kiosk-form",
  contact:  "agentic-ai@iitd.ac.in"
};
```

Save, refresh, done. Nothing else needs changing and there is nothing to rebuild.

| Key | Buttons it fills |
| --- | --- |
| `register` | "Register to attend" — hero, Three ways in, Registration page |
| `poster` | "Submit a poster" — Three ways in, Registration → Posters |
| `kiosk` | "Request a kiosk" — Three ways in, Partners & sponsors |
| `contact` | The committee e-mail shown in the footer and on Partners/Organisers |

While a value is left empty, that button renders greyed out and reads
"opens soon", and clicking does nothing. No dead links, no 404s.

### Making the Google Forms send an acknowledgement

The site promises registrants an instant copy of their responses. To honour it,
in each form: **Settings → Responses → Collect email addresses: Verified**, then
**Send responders a copy of their response: Always**.

---

## 2. Deploying

### GitHub Pages (recommended)

This is a static site, which is exactly what Pages is for. A workflow is already
included at `.github/workflows/pages.yml`.

1. Push this repository to GitHub.
2. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
3. Push to `main`. The workflow publishes `static/` and prints the URL.

You get `https://<user>.github.io/<repo>/`, free, with HTTPS. To use a custom
domain such as `agenticai.iitd.ac.in`, add it under Settings → Pages and create
the matching DNS record.

### Streamlit Community Cloud

Included because you asked for it, with one caveat below.

1. Push to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), **New app**, pick this
   repository and `streamlit_app.py`.
3. Deploy. You get `https://<app-name>.streamlit.app`.

`.streamlit/config.toml` turns on static file serving, so `static/` is published
at `/app/static/`, and `streamlit_app.py` embeds `index.html` full-bleed.

**The caveat:** Streamlit is built for Python data apps, not static sites. The
whole site lives inside one iframe, so the browser URL never changes as you move
between pages, visitors cannot link to the Speakers page directly, the back
button does not follow page changes, and search engines index almost none of it.
Free Streamlit apps also sleep when idle and take a few seconds to wake.

For a conference site people will link to and share, GitHub Pages is the better
host. Any plain web server works too: copy `static/` to it and you are done.

### Anywhere else

Netlify, Vercel, Cloudflare Pages or an institutional server: publish `static/`
as the document root. No build command.

---

## 3. Layout

```
├── static/                 the website — this folder is what gets deployed
│   ├── index.html          home
│   ├── about.html          what agentic AI is, and the worked example trace
│   ├── programme.html      the two-day schedule
│   ├── speakers.html       the eleven speakers, with space for biographies
│   ├── tutorials.html      tutorials and live demos
│   ├── venue.html          route map, travel, accommodation
│   ├── register.html       how registration works, fees, posters, FAQ
│   ├── partners.html       sponsorship tiers and kiosks
│   ├── organisers.html     faculty and student organisers
│   ├── config.js           ← your form links go here
│   ├── site.js             theme toggle, speaker ring, run demo, menu
│   ├── styles.css          one stylesheet for every page
│   └── photos/             speaker portraits, campus, crests, card images
├── build_site.py           regenerates static/*.html from one source
├── streamlit_app.py        Streamlit host wrapper
├── requirements.txt        streamlit
└── .github/workflows/      GitHub Pages deployment
```

### Editing content

Two ways, and you can mix them:

- **Direct.** Open the HTML file and edit it. It is ordinary markup.
- **Via the generator.** `build_site.py` holds the header, footer, navigation and
  page content in one place and writes all ten pages, so shared furniture stays
  consistent. Run `python3 build_site.py` and it rewrites `static/*.html`.
  It overwrites those files, so if you have hand-edited a page, port the change
  into the script first.

### Adding speaker biographies

In `build_site.py`, find the `SPK` list on the speakers page. Each entry is
`(photo, name, designation, affiliation, track, sector)`. Replace
`Biography to follow.` in the generated block with real text, or edit
`static/speakers.html` directly. Portraits are 520×520 WebP in `static/photos/`,
named after the speaker.

### Filling in the schedule

`DAY1` and `DAY2` in `build_site.py` are lists of
`(time, session, type, room, speaker, style)`. Replace "Invited talk" and
"Speaker to be announced" as sessions confirm, then rebuild.

---

## 4. How it behaves

- **Light and dark themes.** Follows the device setting; the header toggle
  overrides it and the choice is remembered. The campus photo and the three card
  images each have a day and a night version that swap with the theme.
- **Responsive.** Checked at 360, 390, 768, 1024 and 1440px. On phones the
  orchestration diagram becomes a vertical pipeline instead of scrolling
  sideways.
- **Motion.** The speaker ring rotates, the run demo plays, cards tilt and the
  facts list bends toward the cursor. All of it stops under
  `prefers-reduced-motion`.
- **No tracking.** No analytics, no cookies, no third-party requests except
  Google Fonts.

---

## 5. Credits and licensing

Before this goes public, settle two things:

- **Speaker portraits** in `static/photos/` were supplied for this site. Confirm
  each speaker is happy to appear.
- **The three card images** (attend, poster, exhibit) are AI-generated, and the
  company names and logos in them are fictional. Swap them for real photographs
  from a past event if you have them.

The IIT Delhi crest belongs to the institute; use follows institute policy.
