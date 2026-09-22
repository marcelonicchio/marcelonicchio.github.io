#!/usr/bin/env python3
"""Audit the two Coitado do Próximo album audio archives."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

CASES = {
    "pt": {
        "vertical": ROOT / "pt" / "musica" / "index.html",
        "mqd_page": ROOT / "pt" / "musica" / "meu-querido-diario" / "index.html",
        "enta_page": ROOT / "pt" / "musica" / "eu-nao-to-nem-ai" / "index.html",
        "audio_id": "audio-preservado",
        "mqd_teaser": "/pt/musica/meu-querido-diario/#audio-preservado",
        "enta_teaser": "/pt/musica/eu-nao-to-nem-ai/#audio-preservado",
        "bonus": "Bônus · Um Anjo do Céu",
    },
    "en": {
        "vertical": ROOT / "en" / "music" / "index.html",
        "mqd_page": ROOT / "en" / "music" / "meu-querido-diario" / "index.html",
        "enta_page": ROOT / "en" / "music" / "eu-nao-to-nem-ai" / "index.html",
        "audio_id": "preserved-audio",
        "mqd_teaser": "/en/music/meu-querido-diario/#preserved-audio",
        "enta_teaser": "/en/music/eu-nao-to-nem-ai/#preserved-audio",
        "bonus": "Bonus · Um Anjo do Céu",
    },
}

COVER = "/assets/archive/music/coitado-do-proximo/1997-1998-meu-querido-diario/coitadodoproximo_00_cdmeuqueridodiario_1997.jpg"
STUDIO = "/assets/archive/music/coitado-do-proximo/1997-1998-meu-querido-diario/coitadodoproximo_00_estudioasas1997_300kb.jpg"


def soup(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def assert_audio_sources(container, expected: int, label: str) -> None:
    players = container.select("audio.audio-library__player")
    if len(players) != expected:
        raise AssertionError(f"{label}: expected {expected} audio players, found {len(players)}")
    for player in players:
        if player.get("preload") != "none":
            raise AssertionError(f"{label}: every player must use preload=none")
        source = player.find("source")
        if source is None or source.get("type") != "audio/mpeg":
            raise AssertionError(f"{label}: player missing audio/mpeg source")
        src = source.get("src", "")
        disk = ROOT / unquote(src).lstrip("/")
        if not disk.is_file():
            raise AssertionError(f"{label}: missing MP3 referenced by player: {src}")


def main() -> int:
    if not (ROOT / COVER.lstrip("/")).is_file():
        raise AssertionError("Meu Querido Diário original cover is missing")
    if not (ROOT / STUDIO.lstrip("/")).is_file():
        raise AssertionError("Meu Querido Diário Estúdio Asas image is missing")

    for lang, cfg in CASES.items():
        vertical = soup(cfg["vertical"])

        mqd = vertical.select_one("#music-album-1997")
        if mqd is None:
            raise AssertionError(f"{lang}: Meu Querido Diário vertical entry missing")
        if mqd.find("audio") is not None:
            raise AssertionError(f"{lang}: vertical must stay compact; MQD players belong on standalone page")
        pair = mqd.select_one("figure.thread-media--album-pair")
        if pair is None:
            raise AssertionError(f"{lang}: MQD cover/studio pair missing")
        pair_srcs = {img.get("src") for img in pair.find_all("img")}
        if {COVER, STUDIO} - pair_srcs:
            raise AssertionError(f"{lang}: MQD pair must contain both original cover and studio image")
        if mqd.find("a", href=cfg["mqd_teaser"]) is None:
            raise AssertionError(f"{lang}: MQD standalone audio teaser missing")

        enta = vertical.select_one("#music-album-1999-2000")
        if enta is None:
            raise AssertionError(f"{lang}: Eu Não Tô Nem Aí vertical entry missing")
        if enta.find("audio") is not None:
            raise AssertionError(f"{lang}: vertical must stay compact; second-album players belong on standalone page")
        if enta.find("a", href=cfg["enta_teaser"]) is None:
            raise AssertionError(f"{lang}: Eu Não Tô Nem Aí standalone audio teaser missing")
        credits = enta.select_one(".album-credits")
        tracklist = credits.find("ol") if credits else None
        if tracklist is None or len(tracklist.find_all("li", recursive=False)) != 8:
            raise AssertionError(f"{lang}: Eu Não Tô Nem Aí must expose exactly 8 official CD tracks")
        names = tracklist.get_text(" ", strip=True)
        for required in ("Ninguém Imaginava", "Ciúmes"):
            if required not in names:
                raise AssertionError(f"{lang}: official CD track missing: {required}")

        mqd_page = soup(cfg["mqd_page"])
        mqd_audio = mqd_page.find(id=cfg["audio_id"])
        if mqd_audio is None:
            raise AssertionError(f"{lang}: MQD standalone audio archive missing")
        assert_audio_sources(mqd_audio, 5, f"{lang}: MQD")

        enta_page = soup(cfg["enta_page"])
        enta_audio = enta_page.find(id=cfg["audio_id"])
        if enta_audio is None:
            raise AssertionError(f"{lang}: Eu Não Tô Nem Aí standalone audio archive missing")
        assert_audio_sources(enta_audio, 9, f"{lang}: ENTA")
        groups = enta_audio.select(".video-library__group")
        if len(groups) != 9:
            raise AssertionError(f"{lang}: expected 9 audio groups including bonus")
        bonus = enta_audio.select_one(".album-audio-library__bonus")
        if bonus is None or cfg["bonus"] not in bonus.get_text(" ", strip=True):
            raise AssertionError(f"{lang}: Um Anjo do Céu must be visibly separated as the live bonus")
        if len(enta_audio.select(".album-audio-library__bonus")) != 1:
            raise AssertionError(f"{lang}: exactly one track may be marked as album bonus")

        for page, label in ((mqd_page, "MQD"), (enta_page, "ENTA")):
            if "streaming" in page.get_text(" ", strip=True).lower():
                raise AssertionError(f"{lang}: {label} album page should not discuss streaming; that belongs to its own post")

    print("Album audio archive OK: compact verticals, paired MQD artwork, 5 recovered MQD tracks, 8 official ENTA tracks + one live bonus.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
