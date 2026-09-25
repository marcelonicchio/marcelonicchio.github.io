#!/usr/bin/env python3
"""Audit the optional Spotify now-playing Home integration.

This audit protects architecture and privacy boundaries only. Spotify's official
full-logo asset is a launch-time branding requirement and is intentionally kept
outside this repository until the official asset is supplied.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://now.marcelonicchio.com/now-playing"
CUSTOM_DOMAIN = "now.marcelonicchio.com"

HOME = {
    "pt": ROOT / "pt" / "index.html",
    "en": ROOT / "en" / "index.html",
}
STATUS = {
    "pt": ROOT / "pt" / "spotify-status" / "index.html",
    "en": ROOT / "en" / "spotify-status" / "index.html",
}
WORKER = ROOT / "infra" / "spotify-now-playing" / "src" / "index.js"
WRANGLER = ROOT / "infra" / "spotify-now-playing" / "wrangler.jsonc"
CLIENT = ROOT / "assets" / "js" / "now-playing.js"
SITEMAP = ROOT / "sitemap.xml"
GITIGNORE = ROOT / ".gitignore"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    for path in [*HOME.values(), *STATUS.values(), WORKER, WRANGLER, CLIENT, SITEMAP, GITIGNORE]:
        require(path.exists(), f"missing required file: {path.relative_to(ROOT)}", errors)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    client = CLIENT.read_text(encoding="utf-8")
    worker = WORKER.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")
    config = json.loads(WRANGLER.read_text(encoding="utf-8"))

    for lang, path in HOME.items():
        html = path.read_text(encoding="utf-8")
        require('data-now-playing' in html, f"{lang} Home missing now-playing slot", errors)
        require(f'data-endpoint="{ENDPOINT}"' in html, f"{lang} Home uses unexpected endpoint", errors)
        require('hidden aria-live="polite"' in html, f"{lang} Home widget must be hidden by default", errors)
        require('/assets/js/now-playing.js?v=' in html, f"{lang} Home missing now-playing client", errors)
        require('<audio' not in _widget(html), f"{lang} Home now-playing widget must not embed Spotify audio", errors)

    for lang, path in STATUS.items():
        html = path.read_text(encoding="utf-8")
        require('<meta name="robots" content="noindex,follow">' in html,
                f"{lang} Spotify status page must remain noindex,follow", errors)
        require(str(path.relative_to(ROOT)).replace("index.html", "") not in sitemap,
                f"{lang} Spotify status page must not enter sitemap", errors)

    require('user-read-currently-playing' in worker,
            "Worker must request only the currently-playing read scope", errors)
    require('user-modify-playback-state' not in worker,
            "Worker must not request playback-control scope", errors)
    require('/v1/me/player/currently-playing' in worker,
            "Worker must use Spotify currently-playing endpoint", errors)
    require('invalid_grant' in worker and 'reauth_required' in worker,
            "Worker must handle six-month refresh-token expiration", errors)
    require('SPOTIFY_STATE' in worker,
            "Worker must persist OAuth tokens in the declared KV binding", errors)

    required = set(config.get("secrets", {}).get("required", []))
    expected = {"SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "ADMIN_KEY", "STATE_SECRET"}
    require(required == expected, "Worker required-secret declaration changed unexpectedly", errors)
    require(config.get("workers_dev") is False,
            "production Worker must not expose an extra workers.dev endpoint", errors)
    routes = config.get("routes", [])
    require(any(route.get("pattern") == CUSTOM_DOMAIN and route.get("custom_domain") is True for route in routes),
            "Worker custom domain is missing or incorrect", errors)
    kv = config.get("kv_namespaces", [])
    require(any(item.get("binding") == "SPOTIFY_STATE" for item in kv),
            "Worker KV binding SPOTIFY_STATE is missing", errors)

    require("document.visibilityState" in client,
            "Home client must pause polling when the page is not visible", errors)
    require("60_000" in client,
            "Home client polling interval changed from the one-minute baseline", errors)
    require("payload.status !== \"playing\"" in client,
            "Home client must hide paused/idle states rather than implying live playback", errors)
    require(".textContent =" in client,
            "Spotify metadata must be inserted as text, not trusted HTML", errors)

    require(".dev.vars" in gitignore and ".env" in gitignore,
            "local Worker secret files must be ignored by git", errors)

    secret_assignment = re.compile(
        r"(?:SPOTIFY_CLIENT_SECRET|ADMIN_KEY|STATE_SECRET)\s*=\s*['\"][^'\"]+['\"]"
    )
    for path in [WORKER, CLIENT, WRANGLER]:
        require(secret_assignment.search(path.read_text(encoding="utf-8")) is None,
                f"{path.relative_to(ROOT)} appears to contain a committed secret value", errors)

    if errors:
        print(f"Spotify now-playing audit failed with {len(errors)} error(s):")
        for error in errors:
            print(" -", error)
        return 1

    print("Spotify now-playing architecture OK: hidden live Home slot, read-only Worker, KV token storage, no public secrets, no Spotify audio proxy.")
    print("LAUNCH GATE: add Spotify's official full logo according to current branding guidelines before publishing the widget.")
    return 0


def _widget(html: str) -> str:
    match = re.search(r'<section class="now-playing-band".*?</section>', html, flags=re.S)
    return match.group(0) if match else ""


if __name__ == "__main__":
    raise SystemExit(main())
