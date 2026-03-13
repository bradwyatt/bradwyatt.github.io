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

### View on iPhone

Run a local server on your Mac bound to your LAN IP, then open that IP from your iPhone on the same Wi-Fi.

From the repo root:

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Then find your Mac's local IP:

```bash
ipconfig getifaddr en0
```

If that returns something like `192.168.1.42`, open this on your iPhone:

```text
http://192.168.1.42:8000
```

Use `http`, not `https`. Your iPhone and Mac must be on the same Wi-Fi network.

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
