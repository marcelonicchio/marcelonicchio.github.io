#!/usr/bin/env python3
"""Guard PRO v1's bilingual SoundCloud enhancement without touching Full Biography."""
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CSS = "/assets/research-podcast.css?v=20261010-v1"
JS = "/assets/js/research-podcast.js?v=20261010-v1"
PAGES = {
    "pt/ia-hai/index.html": "vertical",
    "en/ai-hai/index.html": "vertical",
    "pt/ia-hai/punk-rock-orchestra-pro-v1/index.html": "chapter",
    "en/ai-hai/punk-rock-orchestra-pro-v1/index.html": "chapter",
}


def check_page(relative_path: str, kind: str) -> None:
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    styles = [tag.get("href") for tag in soup.select('link[rel="stylesheet"]')]
    scripts = [tag.get("src") for tag in soup.select("script[src]")]
    assert styles.count(CSS) == 1, f"{relative_path}: missing or repeated podcast stylesheet"
    assert scripts.count(JS) == 1, f"{relative_path}: missing or repeated podcast script"
    assert 'data-entry-id="hai-pro1"' in html or 'id="pro1"' in html
    if kind == "vertical":
        target = soup.select_one("#pro1 > p.meta")
    else:
        target = soup.select_one('main[data-entry-id="hai-pro1"] article.entry-page-body > p.meta')
    assert target is not None, f"{relative_path}: podcast insertion anchor missing"


def main() -> int:
    for path, kind in PAGES.items():
        check_page(path, kind)

    code = (ROOT / "assets/js/research-podcast.js").read_text(encoding="utf-8")
    for required in (
        "https://soundcloud.com/marcelonicchio/a-ia-como-maquina-de-hesitar",
        "https://soundcloud.com/marcelonicchio/punk-rock-orchestra-one",
        'A IA como "Máquina de Hesitar" (PRO v1)',
        "Punk Rock Orchestra: One Researcher. Many AI Critics. No Easy Answers.",
        "show_artwork: 'true'",
        "auto_play: 'false'",
        "visual: 'false'",
    ):
        assert required in code, f"missing episode data or SoundCloud option: {required}"

    generator = (ROOT / "tools/build_chapter_pages.py").read_text(encoding="utf-8")
    assert 'entry["id"] == "hai-pro1"' in generator
    assert "{podcast_css}" in generator and "{podcast_js}" in generator
    for relative_path in ("pt/biografia/index.html", "en/biography/index.html"):
        html = (ROOT / relative_path).read_text(encoding="utf-8")
        assert JS not in html and CSS not in html, f"{relative_path}: podcast assets must remain chapter-only"
    print("PRO v1 SoundCloud integration OK: 4 chapter surfaces, 2 audios, no Biography leakage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
