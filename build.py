#!/usr/bin/env python3
"""Render nabo.al from src/template.html and i18n/<lang>.json.

    python3 build.py            # writes index.html (en) and <lang>/index.html, sitemap.xml

English lives at the root; every other language in its own folder so each page has a
stable URL, a real <html lang>, and hreflang alternates. The build is strict: a key
missing from any language file fails the build instead of leaking a placeholder.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
SITE = "https://nabo-app.org"
DEFAULT = "en"
LANGS = ["en", "sq", "fr", "it", "de", "es"]
NATIVE = {"en": "English", "sq": "Shqip", "fr": "Français", "it": "Italiano", "de": "Deutsch", "es": "Español"}
OG_LOCALE = {"en": "en_GB", "sq": "sq_AL", "fr": "fr_FR", "it": "it_IT", "de": "de_DE", "es": "es_ES"}
PLACEHOLDER = re.compile(r"{{(\w+)}}")


def url_for(lang: str) -> str:
    return f"{SITE}/" if lang == DEFAULT else f"{SITE}/{lang}/"


def render(template: str, values: dict[str, str], lang: str) -> str:
    missing: set[str] = set()

    def sub(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in values:
            return values[key]
        missing.add(key)
        return match.group(0)

    out = PLACEHOLDER.sub(sub, template)
    if missing:
        sys.exit(f"[{lang}] missing keys: {', '.join(sorted(missing))}")
    return out


def main() -> None:
    template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    strings = {lang: json.loads((ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8")) for lang in LANGS}

    # Every language must carry exactly the English key set.
    en_keys = set(strings[DEFAULT])
    for lang in LANGS[1:]:
        extra = set(strings[lang]) - en_keys
        lacking = en_keys - set(strings[lang])
        if extra or lacking:
            sys.exit(f"[{lang}] extra: {sorted(extra)} missing: {sorted(lacking)}")

    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{lang}" href="{url_for(lang)}">' for lang in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{url_for(DEFAULT)}">'

    for lang in LANGS:
        base = "" if lang == DEFAULT else "../"
        menu = "\n".join(
            f'          <a href="{base}{"" if other == DEFAULT else other + "/"}" hreflang="{other}" lang="{other}"'
            f'{" aria-current=\"true\"" if other == lang else ""}>{NATIVE[other]}<small>{other.upper()}</small></a>'
            for other in LANGS
        )
        values = dict(strings[lang])
        values.update(
            lang=lang,
            base=base,
            home_path="",
            canonical=url_for(lang),
            alternates=alternates,
            lang_menu=menu,
            lang_short=lang.upper(),
            og_locale=OG_LOCALE[lang],
            mail_subject=quote(values["mail_subject_raw"]),
        )
        html = render(template, values, lang)
        out = ROOT / "index.html" if lang == DEFAULT else ROOT / lang / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")

    today = date.today().isoformat()
    # Every legal page in every language (rendered by src/legal.py).
    legal = [f"legal/{p}.html" if lang == DEFAULT else f"{lang}/legal/{p}.html"
             for p in ("terms", "privacy", "guidelines", "dpa", "subprocessors") for lang in LANGS]
    urls = [url_for(lang) for lang in LANGS] + [f"{SITE}/{path}" for path in legal]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>")
    sitemap.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
