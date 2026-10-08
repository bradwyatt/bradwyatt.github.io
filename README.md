# BradWyatt.github.io

Static personal website for GitHub Pages with Home, Resume, Projects, and four
unlisted OAuth application information pages.

## Quick Start

Start a local server from the repo root:

```bash
python3 -m http.server 8000
```

Then open:

- http://localhost:8000/
- http://localhost:8000/resume/
- http://localhost:8000/projects/
- http://localhost:8000/n8n-google-calendar/
- http://localhost:8000/n8n-google-calendar/privacy/
- http://localhost:8000/n8n-gmail/
- http://localhost:8000/n8n-gmail/privacy/

## Structure

- `index.html` — Home page
- `resume/index.html` — Resume page
- `projects/index.html` — Projects page
- `n8n-google-calendar/` — Google Calendar automation homepage and privacy policy
- `n8n-gmail/` — Gmail automation homepage and privacy policy
- `css/site.css` — Global styles
- `js/site.js` — Small UI behaviors

### Assets

- `assets/shared/` — Site-wide visuals (hero background, shared placeholders)
- `assets/home/` — Home page images (headshot)
- `assets/resume/` — Resume PDFs and images
- `assets/projects/` — Project media + downloads, organized in per-project folders

## Deploy

Push to `main` and GitHub Pages will serve the site at `https://bradwyatt.github.io/`.
