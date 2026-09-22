#!/usr/bin/env python3
"""Guard the recovered album audio archive and Meu Querido Diário artwork pairing."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "pt": {
        "mqd": ROOT / "content/entries/pt/music-album-1997.inc",
        "enta": ROOT / "content/entries/pt/music-album-1999-2000.inc",
    },
    "en": {
        "mqd": ROOT / "content/entries/en/music-album-1997.inc",
        "enta": ROOT / "content/entries/en/music-album-1999-2000.inc",
    },
}

MQD_COVER = "/assets/archive/music/coitado-do-proximo/1997-1998-meu-querido-diario/coitadodoproximo_00_cdmeuqueridodiario_1997.jpg"
MQD_STUDIO = "/assets/archive/music/coitado-do-proximo/1997-1998-meu-querido-diario/coitadodoproximo_00_estudioasas1997_300kb.jpg"


def local_path(url: str) -> Path:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        raise AssertionError(f"Audio source must be local: {url}")
    return ROOT / unquote(parsed.path).lstrip("/")


def audit_audio_block(soup: BeautifulSoup, expected_count: int, label: str) -> list[str]:
    block = soup.select_one(".album-audio-library")
    if block is None:
        raise AssertionError(f"{label}: album audio library missing")
    players = block.select("audio.audio-library__player")
    if len(players) != expected_count:
        raise AssertionError(f"{label}: expected {expected_count} players, found {len(players)}")

    sources: list[str] = []
    for index, player in enumerate(players, start=1):
        if player.get("preload") != "none":
            raise AssertionError(f"{label}: player {index} must use preload=none")
        source = player.find("source")
        if source is None or not source.get("src"):
            raise AssertionError(f"{label}: player {index} source missing")
        src = str(source["src"])
        if source.get("type") != "audio/mpeg":
            raise AssertionError(f"{label}: player {index} must declare audio/mpeg")
        path = local_path(src)
        if not path.exists() or not path.is_file():
            raise AssertionError(f"{label}: missing audio file {path.relative_to(ROOT)}")
        if path.suffix.lower() != ".mp3":
            raise AssertionError(f"{label}: non-MP3 source {path.relative_to(ROOT)}")
        sources.append(src)
    if len(set(sources)) != len(sources):
        raise AssertionError(f"{label}: duplicate audio source")
    return sources


def main() -> int:
    for lang, paths in TARGETS.items():
        mqd = BeautifulSoup(paths["mqd"].read_text(encoding="utf-8"), "html.parser")
        enta = BeautifulSoup(paths["enta"].read_text(encoding="utf-8"), "html.parser")

        pair = mqd.select_one("figure.thread-media--album-pair .thread-media-pair__images")
        if pair is None:
            raise AssertionError(f"{lang}: Meu Querido Diário album pair missing")
        images = [str(img.get("src", "")) for img in pair.find_all("img", recursive=True)]
        if images != [MQD_COVER, MQD_STUDIO]:
            raise AssertionError(f"{lang}: Meu Querido Diário pair must be cover + studio image in that order")

        audit_audio_block(mqd, 5, f"{lang}:Meu Querido Diário")
        audit_audio_block(enta, 9, f"{lang}:Eu Não Tô Nem Aí")

        bonus = enta.select(".album-audio-library__bonus")
        if len(bonus) != 1 or "Um Anjo do Céu" not in bonus[0].get_text(" ", strip=True):
            raise AssertionError(f"{lang}: live Um Anjo do Céu bonus track must be isolated")

        credits = enta.select_one(".album-credits")
        if credits is None:
            raise AssertionError(f"{lang}: Eu Não Tô Nem Aí credits missing")
        track_list = credits.find("ol")
        if track_list is None or len(track_list.find_all("li", recursive=False)) != 8:
            raise AssertionError(f"{lang}: Eu Não Tô Nem Aí official CD track list must contain 8 tracks")
        credits_text = credits.get_text(" ", strip=True)
        if "Ninguém Imaginava" not in credits_text or "Ciúmes" not in credits_text:
            raise AssertionError(f"{lang}: official CD track list must include Ninguém Imaginava and Ciúmes")

        combined = paths["mqd"].read_text(encoding="utf-8") + paths["enta"].read_text(encoding="utf-8")
        if "streaming" in combined.casefold():
            raise AssertionError(f"{lang}: album archive fragments must not discuss streaming availability")

    print("Music album audio archive OK: MQD cover pair + 5 recovered tracks; ENTA 8 CD tracks + 1 live bonus.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
