#!/usr/bin/env python3
"""Check Melissa's extensible SoundCloud catalog on both languages and Chapter Pages."""
import json
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/melissa-podcasts.json"
CSS = "/assets/melissa-podcast.css?v=20261010-v1"
BASE_CSS = "/assets/research-podcast.css?v=20261010-v1"
JS = "/assets/js/melissa-podcast.js?v=20261010-v2"
PAGES = {
    "pt/ia-hai/index.html": "vertical",
    "en/ai-hai/index.html": "vertical",
    "pt/ia-hai/melissa-1-0/index.html": "chapter",
    "en/ai-hai/melissa-1-0/index.html": "chapter",
}


def check_catalog() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["entry_id"] == "hai-melissa"
    episodes = data["episodes"]
    assert episodes, "at least one published audio required"
    ids = set()
    for ep in episodes:
        assert ep["id"] and ep["id"] not in ids
        ids.add(ep["id"])
        assert ep["language"] in ("pt", "en")
        assert isinstance(ep["title"], str) and ep["title"].strip()
        parsed = urlparse(ep["soundcloud_url"])
        assert parsed.scheme == "https" and parsed.netloc in {"soundcloud.com", "www.soundcloud.com"}
        assert len([p for p in parsed.path.split("/") if p]) >= 2
    # Future curations may add or remove tracks without changing the implementation.


def check_html(path: str, kind: str) -> None:
    soup = BeautifulSoup((ROOT / path).read_text(encoding="utf-8"), "html.parser")
    styles = [x.get("href") for x in soup.select('link[rel="stylesheet"]')]
    scripts = [x.get("src") for x in soup.select("script[src]")]
    for css in (BASE_CSS, CSS):
        assert styles.count(css) == 1, f"{path}: expected exactly one {css}"
    assert scripts.count(JS) == 1, f"{path}: Melissa script missing or duplicated"
    anchor = (
        soup.select_one("#melissa > figure.melissa-selfportrait") if kind == "vertical"
        else soup.select_one('main[data-entry-id="hai-melissa"] article.entry-page-body > figure.melissa-selfportrait')
    )
    assert anchor is not None, f"{path}: insertion anchor missing"
    assert anchor.find("img") is not None, f"{path}: portrait image missing"
    assert anchor.find("figcaption") is not None, f"{path}: portrait caption missing"
    assert anchor.find_previous_sibling("p", class_="meta") is not None, f"{path}: portrait must follow date"


def main() -> int:
    check_catalog()
    for path, kind in PAGES.items():
        check_html(path, kind)
    generator = (ROOT / "tools/build_chapter_pages.py").read_text(encoding="utf-8")
    assert 'entry["id"] == "hai-melissa"' in generator
    assert 'melissa-podcast.css?v=20261010-v1' in generator
    assert 'melissa-podcast.js?v=20261010-v2' in generator
    code = (ROOT / "assets/js/melissa-podcast.js").read_text(encoding="utf-8")
    for token in ('/data/melissa-podcasts.json', "show_artwork: 'true'", "auto_play: 'false'", "visual: 'false'", "soundcloud_url"):
        assert token in code, f"missing client behavior {token}"
    for path in ("pt/biografia/index.html", "en/biography/index.html"):
        html = (ROOT / path).read_text(encoding="utf-8")
        assert JS not in html and CSS not in html, f"{path}: leaked standalone audio player to biography"
    print("Melissa podcast library OK: extensible catalog, 4 target pages, no biography leakage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
