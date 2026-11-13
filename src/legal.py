#!/usr/bin/env python3
"""Render the legal pages in six languages, and 404.html, with the site chrome.

Sources: src/legal/<lang>/<page>.html (the document body) and src/legal/<lang>/meta.json (titles,
navigation and notices). English is the reference text; every language must have every page.
Output: legal/<page>.html (English) and <lang>/legal/<page>.html for the other five languages,
each linking to the same page in the other languages (hreflang).

The pages are drafts for legal review until the entity placeholders in [square brackets] are
filled; the notice at the top of every page says so.
"""
from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://nabo-app.org"
DEFAULT = "en"
LANGS = ["en", "sq", "fr", "it", "de", "es"]
NATIVE = {"en": "English", "sq": "Shqip", "fr": "Français", "it": "Italiano", "de": "Deutsch", "es": "Español"}
PAGES = ["terms", "privacy", "guidelines", "dpa", "subprocessors"]
NAV = [("terms", "nav_terms"), ("privacy", "nav_privacy"), ("guidelines", "nav_guidelines"), ("dpa", "nav_dpa"),
       ("subprocessors", "nav_subprocessors")]
CONTACT = "info@nabo-app.org"

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="author" content="Ervin Capi">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Nabo</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#F7F6F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1A17" media="(prefers-color-scheme: dark)">
{alternates}
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
<style>
.doc .table-wrap{{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:16px 0 8px}}
.doc table{{width:100%;border-collapse:collapse;font-size:15px}}
.doc th,.doc td{{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line, rgba(127,127,127,.25));color:var(--ink-2)}}
.doc thead th,.doc tbody th{{font-weight:600}}
.doc tbody th{{width:28%}}
.langs{{display:flex;flex-wrap:wrap;gap:6px 14px;margin:-20px 0 28px;font-size:14px}}
.doc .langs a{{text-decoration:none}}
.langs [aria-current]{{font-weight:600}}
</style>
<script>(function(){{try{{var t=localStorage.getItem('nabo-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
<body>
<header class="nav is-scrolled" id="nav">
  <div class="wrap">
    <a class="brand" href="{home}" aria-label="Nabo">
      <span class="mark" aria-hidden="true"><svg viewBox="0 0 64 64"><path d="M18 46V28l14-11 14 11v18H36V34h-8v12z" fill="currentColor"/></svg></span>
      Nabo
    </a>
    <nav class="nav-links" aria-label="Legal">
{nav}
    </nav>
    <div class="nav-right">
      <a class="btn btn-ghost btn-sm" href="{home}">{back}</a>
    </div>
  </div>
</header>
<main id="main">
"""

FOOT = """
</main>
<footer class="footer">
  <div class="wrap footer-bottom" style="margin-top:0;border-top:0;padding-top:0">
    <span>© 2026 Nabo · {rights}</span>
    <span><a href="mailto:{contact}">{contact}</a></span>
    <span>{made_by} <a href="https://www.linkedin.com/in/ervin-capi/" rel="author noopener" target="_blank">Ervin Capi</a></span>
  </div>
</footer>
<script src="{base}assets/site.js" defer></script>
</body>
</html>
"""

NOTICE = """<div class="notice"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg><span>{text}</span></div>"""


def page_path(lang: str, slug: str) -> str:
    """Path from the site root, e.g. legal/terms.html or sq/legal/terms.html."""
    return f"legal/{slug}.html" if lang == DEFAULT else f"{lang}/legal/{slug}.html"


def base_for(lang: str) -> str:
    """Relative path from a legal page back to the site root."""
    return "../" if lang == DEFAULT else "../../"


def load(lang: str) -> tuple[dict, dict[str, str]]:
    folder = ROOT / "src" / "legal" / lang
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    bodies = {slug: (folder / f"{slug}.html").read_text(encoding="utf-8") for slug in PAGES}
    return meta, bodies


def check(sources: dict[str, tuple[dict, dict[str, str]]]) -> None:
    """Every language has the English meta keys, every page, and the same structure as English."""
    en_meta, en_bodies = sources[DEFAULT]
    problems = []
    for lang in LANGS[1:]:
        meta, bodies = sources[lang]
        problems += [f"[{lang}] meta.json missing {key}" for key in en_meta if key not in meta]
        for group in ("titles", "descriptions"):
            problems += [f"[{lang}] meta.json {group} missing {slug}" for slug in PAGES if slug not in meta.get(group, {})]
        for slug in PAGES:
            for tag in ("<h2", "<li", "<tr", "<a "):
                have, want = bodies[slug].count(tag), en_bodies[slug].count(tag)
                if have != want:
                    problems.append(f"[{lang}] {slug}.html has {have} {tag}> (English {want})")
    if problems:
        sys.exit("\n".join(problems))


def wrap_tables(body: str) -> str:
    return body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")


def render(lang: str, slug: str, meta: dict, body: str) -> str:
    base = base_for(lang)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{other}" href="{SITE}/{page_path(other, slug)}">' for other in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/{page_path(DEFAULT, slug)}">'
    nav = "\n".join(
        f'      <a href="{other}.html"' + (' aria-current="page"' if other == slug else "") + f">{meta[key]}</a>"
        for other, key in NAV
    )
    langs = " ".join(
        f'<span aria-current="true">{NATIVE[other]}</span>' if other == lang
        else f'<a href="{base}{page_path(other, slug)}" hreflang="{other}" lang="{other}">{NATIVE[other]}</a>'
        for other in LANGS
    )
    html = HEAD.format(lang=lang, title=escape(meta["titles"][slug], quote=False),
                       description=escape(meta["descriptions"][slug]), robots="index,follow",
                       alternates=alternates, base=base, home="../", nav=nav, back=meta["back"])
    html += f"""<section class="doc"><div class="wrap">
<h1 class="display">{meta['titles'][slug]}</h1>
<p class="meta">{meta['updated']}</p>
<nav class="langs" aria-label="{escape(meta['languages'])}">{langs}</nav>
{NOTICE.format(text=meta['draft'])}
{wrap_tables(body)}
<h2>{meta['contact']}</h2>
<p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
</div></section>"""
    html += FOOT.format(base=base, rights=meta["rights"], contact=CONTACT, made_by=meta["made_by"])
    return html


def not_found(meta: dict) -> str:
    # Served for any path, so resolve assets from the site root — which is /nabo-site/ on the GitHub Pages preview.
    html = HEAD.format(lang=DEFAULT, title="Page not found", description="This page does not exist.", robots="noindex",
                       alternates="", base="", home="", nav="", back=meta["back"])
    html = html.replace(
        "<meta charset=\"utf-8\">",
        "<meta charset=\"utf-8\">\n<script>document.write('<base href=\"' + (location.pathname.indexOf('/nabo-site/') === 0 ? '/nabo-site/' : '/') + '\">');</script>",
        1,
    )
    html += """<section class="nf"><div class="wrap">
<span class="eyebrow">404</span>
<h1 class="display">Wrong <em>door.</em></h1>
<p class="lede" style="text-align:center">This page is not in the building. Try the entrance.</p>
<a class="btn btn-primary" href="/">Back to Nabo</a>
</div></section>"""
    html += FOOT.format(base="", rights=meta["rights"], contact=CONTACT, made_by=meta["made_by"])
    return html


def legal_urls() -> list[str]:
    return [f"{SITE}/{page_path(lang, slug)}" for slug in PAGES for lang in LANGS]


def main() -> None:
    sources = {lang: load(lang) for lang in LANGS}
    check(sources)
    for lang in LANGS:
        meta, bodies = sources[lang]
        for slug in PAGES:
            out = ROOT / page_path(lang, slug)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(render(lang, slug, meta, bodies[slug]), encoding="utf-8")
            print(f"wrote {out.relative_to(ROOT)}")
    (ROOT / "404.html").write_text(not_found(sources[DEFAULT][0]), encoding="utf-8")
    print("wrote 404.html")


if __name__ == "__main__":
    main()
