# nabo.al

Marketing site for **Nabo**, the private community app for one apartment building. Static HTML, no framework, no build dependencies beyond Python 3.

Live: https://ervincapi.github.io/nabo-site/ (GitHub Pages) · production domain `nabo.al`

## Structure

| Path | What |
|---|---|
| `src/template.html` | The one page, with `{{key}}` placeholders |
| `i18n/<lang>.json` | Copy in `en`, `sq`, `fr`, `it`, `de`, `es` (same key set, checked at build) |
| `build.py` | Renders `index.html` (English) and `<lang>/index.html`, plus `sitemap.xml` |
| `src/legal.py` | Renders `legal/*.html` (terms, privacy, guidelines) and `404.html` |
| `src/render_og.swift` | Renders `assets/og.png` (1200×630) for link previews |
| `assets/` | `style.css`, `site.js`, icons (derived from the app icon), OG image |

## Build

```bash
python3 build.py          # pages + sitemap
python3 src/legal.py      # legal pages + 404
swift src/render_og.swift assets/og.png   # only when the OG artwork changes (macOS)
python3 -m http.server 4173              # preview at http://localhost:4173
```

Rendered output is committed, so the repository deploys as-is from GitHub Pages or any static host.

## Design

Paper `#F7F6F2`, ink `#141413`, one green `#1E6B5C`, the house mark from the app icon and the splash screen's floor-plan grid. Fraunces for display type, Inter for text. Light and dark themes follow the system and can be pinned from the footer. Every animation respects `prefers-reduced-motion`.

## Editing copy

Change `i18n/en.json`, mirror the key in the other five files, run `python3 build.py`. The build fails if any language is missing a key, so nothing ships half-translated.

## Domain

When `nabo.al` points at Pages, add a `CNAME` file containing `nabo.al` and enable "Enforce HTTPS" in the repository's Pages settings. The AASA file, magic-link and join landing pages stay in the app repository's `web/` folder and should be served from the same host.
