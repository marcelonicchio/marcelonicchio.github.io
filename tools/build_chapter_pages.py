#!/usr/bin/env python3
"""Generate selective Chapter Pages from neutral entry fragments and metadata.

Only entries with chapter_page.status=pilot are emitted. Candidate entries stay
unpublished until their source migration is deliberate.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from sync_analytics import load_measurement_id, render_block as analytics_block
from sync_presence import load_profiles, render_block as presence_block

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "entries.json"
TAGS = ROOT / "data" / "tags.json"
BASE = "https://marcelonicchio.github.io/"

DOMAIN = {
    "communication": {
        "pt": ("Comunicação & Cultura", "/pt/comunicacao/"),
        "en": ("Communication & Culture", "/en/communication/"),
    },
    "internet": {
        "pt": ("Internet & Performance", "/pt/internet/"),
        "en": ("Internet & Performance", "/en/internet/"),
    },
    "audiovisual": {
        "pt": ("Audiovisual", "/pt/audiovisual/"),
        "en": ("Audiovisual", "/en/audiovisual/"),
    },
    "music": {
        "pt": ("Música", "/pt/musica/"),
        "en": ("Music", "/en/music/"),
    },
}

OG_IMAGE = {
    "communication-folha": "/assets/media/thread/folhateen-cover-2001.webp",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(rel: str) -> str:
    directory = rel[:-10] if rel.endswith("index.html") else rel
    return BASE + directory.lstrip("/")


def nav(lang: str, counterpart: str) -> str:
    if lang == "pt":
        links = [
            ("/pt/biografia/", "Biografia"),
            ("/pt/musica/", "Música"),
            ("/pt/comunicacao/", "Comunicação"),
            ("/pt/internet/", "Internet & Performance"),
            ("/pt/audiovisual/", "Audiovisual"),
            ("/pt/ia-hai/", "IA/HAI"),
            ("/pt/arquivo/", "Arquivo"),
            (counterpart, "EN"),
        ]
        aria = "Voltar à página inicial e seleção de idioma"
    else:
        links = [
            ("/en/biography/", "Biography"),
            ("/en/music/", "Music"),
            ("/en/communication/", "Communication"),
            ("/en/internet/", "Internet & Performance"),
            ("/en/audiovisual/", "Audiovisual"),
            ("/en/ai-hai/", "AI/HAI"),
            ("/en/archive/", "Archive"),
            (counterpart, "PT"),
        ]
        aria = "Back to home and language selection"
    joined = "".join(f'<a href="{href}">{label}</a>' for href, label in links)
    return (
        f'<header class="site-header"><div class="wrap nav">'
        f'<a class="brand" href="/" aria-label="{aria}">Marcelo Nicchio</a>'
        f'<nav class="nav-links">{joined}</nav></div></header>'
    )


def tag_labels(taxonomy: dict[str, Any]) -> dict[str, dict[str, str]]:
    return {tag["id"]: tag["label"] for tag in taxonomy["tags"]}


def breadcrumbs(entry: dict[str, Any], lang: str, current_url: str) -> tuple[str, str]:
    domain_label, domain_path = DOMAIN[entry["domain"]][lang]
    home_label = "Início" if lang == "pt" else "Home"
    current = entry["title"][lang]
    home_path = "/pt/" if lang == "pt" else "/en/"
    visible = (
        '<nav class="entry-breadcrumbs" aria-label="Breadcrumb">'
        f'<a href="{home_path}">{html.escape(home_label)}</a><span>›</span>'
        f'<a href="{domain_path}">{html.escape(domain_label)}</a><span>›</span>'
        f'<span aria-current="page">{html.escape(current)}</span></nav>'
    )
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_label, "item": BASE + home_path.lstrip("/")},
            {"@type": "ListItem", "position": 2, "name": domain_label, "item": BASE + domain_path.lstrip("/")},
            {"@type": "ListItem", "position": 3, "name": current, "item": current_url},
        ],
    }
    schema = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'
    return visible, schema


def render(entry: dict[str, Any], lang: str, taxonomy: dict[str, Any], profiles: list[dict[str, Any]]) -> str:
    page = entry["chapter_page"]
    rel = page[f"{lang}_path"]
    other = "en" if lang == "pt" else "pt"
    other_rel = page[f"{other}_path"]
    url = canonical(rel)
    other_url = canonical(other_rel)
    title = entry["title"][lang]
    summary = entry["summary"][lang]
    meta_description = page.get("meta_description", {}).get(lang, summary)
    date = entry["date"][lang]
    source_rel = entry["source"][f"{lang}_path"]
    body = (ROOT / source_rel).read_text(encoding="utf-8").strip()
    domain_label, domain_path = DOMAIN[entry["domain"]][lang]
    labels = tag_labels(taxonomy)
    chips = "".join(
        f'<span class="entry-topic">{html.escape(labels[tag_id][lang])}</span>'
        for tag_id in entry.get("topic_ids", [])
    )
    crumb, crumb_schema = breadcrumbs(entry, lang, url)
    ga = analytics_block(load_measurement_id())
    presence = presence_block(profiles, lang == "pt")
    robots = page.get("indexing", "noindex,follow")
    html_lang = "pt-BR" if lang == "pt" else "en"
    hreflang_self = "pt-BR" if lang == "pt" else "en"
    hreflang_other = "en" if lang == "pt" else "pt-BR"
    back_bio = "/pt/biografia/" if lang == "pt" else "/en/biography/"
    bio_anchor = f"#bio-{entry['id']}"
    full_bio_label = "Ver na Biografia Completa" if lang == "pt" else "View in Full Biography"
    vertical_label = f"Voltar a {domain_label}" if lang == "pt" else f"Back to {domain_label}"
    eyebrow = f"Registro · {domain_label}" if lang == "pt" else f"Entry · {domain_label}"
    period_label = "Período" if lang == "pt" else "Period"
    topics_label = "Temas" if lang == "pt" else "Topics"
    og = ""
    if entry["id"] in OG_IMAGE:
        image_url = BASE.rstrip("/") + OG_IMAGE[entry["id"]]
        og = f'\n  <meta property="og:image" content="{image_url}">\n  <meta name="twitter:card" content="summary_large_image">'
    else:
        og = '\n  <meta name="twitter:card" content="summary">'

    return f'''<!doctype html>
<html lang="{html_lang}">
<head>
{ga}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)} — Marcelo Nicchio</title>
  <meta name="description" content="{html.escape(meta_description, quote=True)}">
  <meta name="robots" content="{html.escape(robots, quote=True)}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="{hreflang_self}" href="{url}">
  <link rel="alternate" hreflang="{hreflang_other}" href="{other_url}">
  <link rel="alternate" hreflang="x-default" href="{url if lang == 'pt' else other_url}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(meta_description, quote=True)}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">{og}
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/assets/chapter-page.css">
  {crumb_schema}
</head>
<body>
{nav(lang, '/' + other_rel[:-10])}
<main data-entry-id="{entry['id']}">
<section class="article-hero entry-page-hero"><div class="wrap">
{crumb}
<div class="eyebrow">{html.escape(eyebrow)}</div>
<h1>{html.escape(title)}</h1>
<p class="hero-lead">{html.escape(summary)}</p>
<div class="fact-strip"><div class="fact"><span>{period_label}</span><strong>{html.escape(date)}</strong></div></div>
<div class="entry-topic-row" aria-label="{topics_label}">{chips}</div>
</div></section>
<section class="section"><div class="wrap entry-page-shell"><article class="article-body entry-page-body">
{body}
<div class="page-tools"><a href="{domain_path}">{html.escape(vertical_label)}</a><a href="{back_bio}{bio_anchor}">{html.escape(full_bio_label)}</a></div>
</article></div></section>
</main>
<footer>
{presence}
<div class="wrap footer-grid"><span><a href="{domain_path}">← {html.escape(domain_label)}</a></span><span><a href="/{other_rel[:-10]}">{'English version' if lang == 'pt' else 'Versão em português'}</a></span></div>
</footer>
<script src="/assets/js/archive-lightbox.js" defer></script>
</body></html>
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated Chapter Pages are missing or stale")
    args = parser.parse_args()

    registry = load(REGISTRY)
    taxonomy = load(TAGS)
    profiles = load_profiles()
    changed: list[str] = []

    for entry in registry.get("entries", []):
        page = entry.get("chapter_page", {})
        if page.get("status") != "pilot":
            continue
        if entry.get("source", {}).get("kind") != "fragment":
            raise RuntimeError(f"{entry['id']}: pilot Chapter Page requires neutral fragment source")
        for lang in ("pt", "en"):
            rel = page[f"{lang}_path"]
            path = ROOT / rel
            output = render(entry, lang, taxonomy, profiles)
            if not path.exists() or path.read_text(encoding="utf-8") != output:
                changed.append(rel)
                if not args.check:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(output, encoding="utf-8")

    if args.check and changed:
        print("Chapter Page generation required:")
        for rel in changed:
            print(" -", rel)
        return 1

    if changed:
        print("Generated Chapter Pages:")
        for rel in changed:
            print(" -", rel)
    else:
        print("Chapter Pages already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
