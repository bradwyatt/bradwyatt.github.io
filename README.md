# BradWyatt.github.io

Static personal website for GitHub Pages with three pages: Home, Resume, Projects.

## Quick Start

Start a local server from the repo root:

```bash
python3 -m http.server 8000
```

Then open:

- http://localhost:8000/
- http://localhost:8000/resume/
- http://localhost:8000/projects/

## Structure

- `index.html` — Home page
- `resume/index.html` — Resume page
- `projects/index.html` — Projects page
- `css/site.css` — Global styles
- `js/site.js` — Small UI behaviors

### Assets

- `assets/shared/` — Site-wide visuals (hero background, shared placeholders)
- `assets/home/` — Home page images (headshot)
- `assets/resume/` — Resume PDFs and images
- `assets/projects/` — Project media + downloads
  - `assets/projects/gifs/`
  - `assets/projects/videos/`

## Deploy

Push to `main` and GitHub Pages will serve the site at `https://bradwyatt.github.io/`.
