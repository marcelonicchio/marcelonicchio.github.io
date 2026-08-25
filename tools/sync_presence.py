#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRESENCE = ROOT / "data" / "presence.json"
PERSON = ROOT / "data" / "person.json"
STYLES = ROOT / "styles.css"
SPRITE = "/assets/brand/social-sprite.svg"
START = "<!-- presence:start -->"
END = "<!-- presence:end -->"
CSS_START = "/* presence-footer:start */"
CSS_END = "/* presence-footer:end */"


def load_profiles():
    data = json.loads(PRESENCE.read_text(encoding="utf-8"))
    return data["profiles"]


def is_pt(text: str) -> bool:
    m = re.search(r'<html\s+[^>]*lang=["\']([^"\']+)', text, flags=re.I)
    return bool(m and m.group(1).lower().startswith("pt"))


def render_block(profiles, pt: bool) -> str:
    heading = "Presença online" if pt else "Online presence"
    sub = "Perfis, pesquisa, redes e arquivo" if pt else "Profiles, research, networks and archive"
    aria = "Perfis externos de Marcelo Nicchio" if pt else "Marcelo Nicchio external profiles"
    new_tab = "abre em nova aba" if pt else "opens in a new tab"
    links = []
    for p in profiles:
        label = p["label"]
        url = p["url"]
        ident = p["id"]
        safe_label = html.escape(label, quote=True)
        safe_url = html.escape(url, quote=True)
        links.append(
            f'        <a class="presence-link" href="{safe_url}" target="_blank" rel="noopener noreferrer" '
            f'data-label="{safe_label}" title="{safe_label}" aria-label="{safe_label} — {new_tab}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="{SPRITE}#{ident}"></use></svg></a>'
        )
    joined = "\n".join(links)
    return (
        f"{START}\n"
        f'  <div class="wrap presence-panel">\n'
        f'    <div class="presence-head"><strong>{heading}</strong><span>{sub}</span></div>\n'
        f'    <nav class="presence-links" aria-label="{aria}">\n{joined}\n    </nav>\n'
        f"  </div>\n"
        f"{END}"
    )


def sync_html(profiles):
    changed = []
    same_as = [p["url"] for p in profiles if p.get("sameAs")]
    same_as_json = json.dumps(same_as, ensure_ascii=False, separators=(",", ":"))
    block_re = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        block = render_block(profiles, is_pt(text))
        if START in text:
            text = block_re.sub(block, text)
        else:
            footer = re.search(r"<footer(?:\s[^>]*)?>", text, flags=re.I)
            if footer:
                pos = footer.end()
                text = text[:pos] + "\n" + block + text[pos:]
            else:
                text = re.sub(r"</body>", f"<footer>\n{block}\n</footer>\n</body>", text, count=1, flags=re.I)

        # Keep Person sameAs arrays synchronized wherever the current page already declares one.
        text = re.sub(r'("sameAs"\s*:\s*)\[[^\]]*\]', lambda m: m.group(1) + same_as_json, text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())
    return changed


def sync_person(profiles):
    person = json.loads(PERSON.read_text(encoding="utf-8"))
    new_same_as = [p["url"] for p in profiles if p.get("sameAs")]
    if person.get("sameAs") == new_same_as:
        return False
    person["sameAs"] = new_same_as
    PERSON.write_text(json.dumps(person, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def sync_styles():
    css = STYLES.read_text(encoding="utf-8")
    block = r'''
/* presence-footer:start */
.presence-panel{margin-bottom:30px;padding:18px 20px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.028),rgba(255,255,255,.012));display:grid;grid-template-columns:minmax(170px,.46fr) minmax(0,1.54fr);gap:24px;align-items:center}
.presence-head strong{display:block;color:var(--text);font-size:.78rem;letter-spacing:.12em;text-transform:uppercase}
.presence-head span{display:block;margin-top:3px;color:var(--muted);font-size:.75rem}
.presence-links{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end;align-items:center}
.presence-link{position:relative;display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;min-width:42px;border:1px solid var(--line);border-radius:11px;background:rgba(255,255,255,.018);color:var(--soft);text-decoration:none;transition:border-color .18s ease,background .18s ease,color .18s ease,transform .18s ease}
.presence-link svg{display:block;width:20px;height:20px;fill:currentColor}
.presence-link:hover,.presence-link:focus-visible{opacity:1;color:var(--text);border-color:rgba(211,164,160,.6);background:rgba(155,47,47,.10);transform:translateY(-2px)}
.presence-link:focus-visible{outline:2px solid var(--accent-soft);outline-offset:3px}
.presence-link::after{content:attr(data-label);position:absolute;left:50%;bottom:calc(100% + 9px);z-index:30;transform:translate(-50%,4px);padding:5px 8px;border:1px solid var(--line);border-radius:7px;background:#171719;color:var(--text);font-size:.7rem;font-weight:700;line-height:1;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .14s ease,transform .14s ease;box-shadow:0 8px 22px rgba(0,0,0,.3)}
.presence-link:hover::after,.presence-link:focus-visible::after{opacity:1;transform:translate(-50%,0)}
@media(max-width:820px){.presence-panel{grid-template-columns:1fr;gap:14px}.presence-links{justify-content:flex-start}}
@media(max-width:580px){.presence-panel{padding:16px}.presence-links{gap:7px}.presence-link{width:40px;height:40px;min-width:40px}.presence-link svg{width:19px;height:19px}}
@media(pointer:coarse){.presence-link::after{display:none}.presence-link{min-height:44px}}
@media(prefers-reduced-motion:reduce){.presence-link{transition:none}.presence-link:hover,.presence-link:focus-visible{transform:none}}
@media(forced-colors:active){.presence-panel,.presence-link{border-color:CanvasText}}
/* presence-footer:end */
'''.strip()
    pattern = re.compile(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), re.S)
    if CSS_START in css:
        new_css = pattern.sub(block, css)
    else:
        new_css = css.rstrip() + "\n\n" + block + "\n"
    if new_css == css:
        return False
    STYLES.write_text(new_css, encoding="utf-8")
    return True


def main():
    profiles = load_profiles()
    html_changed = sync_html(profiles)
    person_changed = sync_person(profiles)
    styles_changed = sync_styles()
    print(f"Presence sync: {len(html_changed)} HTML file(s) changed.")
    if person_changed:
        print("Updated data/person.json sameAs.")
    if styles_changed:
        print("Updated styles.css presence component.")
    for path in html_changed:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
