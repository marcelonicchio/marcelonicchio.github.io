#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO_HOSTS = ("youtube.com", "youtu.be")
SKIP_FILES = {"404.html", "index.html", "pt/index.html", "en/index.html"}
ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.I)
HREF_RE = re.compile(r"\bhref=(['\"])(.*?)\1", re.I | re.S)
CLASS_RE = re.compile(r"\bclass=(['\"])(.*?)\1", re.I | re.S)
EVIDENCE_LINKS_RE = re.compile(
    r'<div\s+class="(?P<classes>[^"]*\bevidence-links\b[^"]*)">(?P<body>.*?)</div>',
    re.I | re.S,
)

GLOBAL_CSS = r'''
/* Global video & media standard — 2026-09-14 */
:where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill{
  display:inline-flex;align-items:center;justify-content:center;gap:7px;
  min-height:38px;padding:7px 12px;
  border:1px solid rgba(243,239,231,.48);border-radius:999px;
  background:rgba(243,239,231,.065);color:rgba(243,239,231,.96)!important;
  font-size:.82rem;font-weight:760;text-decoration:none!important;line-height:1.15;
  white-space:normal;box-shadow:inset 0 1px 0 rgba(255,255,255,.055);
  transition:background .16s ease,color .16s ease,border-color .16s ease,transform .16s ease,box-shadow .16s ease
}
:where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill:hover,
:where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill:focus-visible{
  opacity:1;background:#f1dfa3;color:#101011!important;border-color:#f6e7ae;
  transform:translateY(-1px);box-shadow:0 5px 16px rgba(241,223,163,.14)
}
:where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill:focus-visible{
  outline:2px solid #f6e7ae;outline-offset:3px
}
.video-library--compact{margin:24px 0 10px;padding:13px 14px 14px}
.video-library--compact .video-library__head{margin-bottom:12px}
.video-library--compact .video-library__actions{justify-content:flex-start}
.record-media-block{
  display:block;margin:28px 0 32px;padding:14px 16px 16px;
  border:1px solid rgba(255,255,255,.14);border-radius:14px;
  background:linear-gradient(180deg,rgba(255,255,255,.032),rgba(255,255,255,.014));
  box-shadow:inset 3px 0 0 rgba(211,164,160,.46)
}
.record-media-block__head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:11px;border-bottom:1px solid rgba(255,255,255,.09)}
.record-media-block__head span{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--text);font-weight:800}
.record-media-block__head strong{margin:0;font-size:.78rem;color:#c7c2b9;font-weight:680}
.record-media-block__links{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-start;margin-top:13px}
@media(max-width:580px){
  :where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill{min-height:40px;padding:8px 11px;font-size:.84rem}
  .video-library--compact{padding:13px;margin:22px 0 10px}
  .record-media-block{padding:13px 13px 14px;margin:24px 0 28px}
  .record-media-block__head{align-items:flex-start;flex-direction:column;gap:2px}
  .record-media-block__head span,.record-media-block__head strong{font-size:.8rem}
}
@media(prefers-reduced-motion:reduce){
  :where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill{transition:none}
  :where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill:hover,
  :where(.evidence-links,.record-media-block__links,.page-tools,.root-video-actions) a.video-pill:focus-visible{transform:none}
}
'''


def is_video(href: str) -> bool:
    h = href.lower()
    return any(host in h for host in VIDEO_HOSTS) and "/@" not in h


def add_video_class(tag: str) -> str:
    href_m = HREF_RE.search(tag)
    if not href_m or not is_video(href_m.group(2)):
        return tag
    cls_m = CLASS_RE.search(tag)
    if cls_m:
        classes = cls_m.group(2).split()
        if "presence-link" in classes or "root-milestone" in classes or "video-pill" in classes:
            return tag
        classes.append("video-pill")
        replacement = f'class={cls_m.group(1)}{" ".join(classes)}{cls_m.group(1)}'
        return tag[: cls_m.start()] + replacement + tag[cls_m.end() :]
    return tag[:-1] + ' class="video-pill">'


def lang_for(path: Path) -> str:
    s = path.as_posix()
    if s.startswith("en/") or "/en/" in s or s.startswith("content/entries/en/"):
        return "en"
    return "pt"


def group_multi_video_evidence(text: str, lang: str) -> tuple[str, int]:
    grouped = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal grouped
        body = m.group("body")
        if "<div" in body.lower():
            return m.group(0)
        anchors = ANCHOR_RE.findall(body)
        if len(anchors) < 2:
            return m.group(0)
        hrefs = []
        for tag in anchors:
            hm = HREF_RE.search(tag)
            if not hm:
                return m.group(0)
            hrefs.append(hm.group(2))
        if not all(is_video(h) for h in hrefs):
            return m.group(0)
        grouped += 1
        label = "Videos &amp; Media" if lang == "en" else "Vídeos &amp; Mídia"
        return (
            '<div class="video-library video-library--compact">\n'
            f'  <div class="video-library__head"><strong>{label} · {len(anchors)}</strong></div>\n'
            f'  <div class="video-library__actions">{body.strip()}</div>\n'
            '</div>'
        )

    return EVIDENCE_LINKS_RE.sub(repl, text), grouped


def process_file(path: Path) -> tuple[bool, int, int]:
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_FILES:
        return False, 0, 0
    text = path.read_text(encoding="utf-8")
    original = text
    video_count = 0

    def anchor_repl(m: re.Match[str]) -> str:
        nonlocal video_count
        tag = m.group(0)
        hm = HREF_RE.search(tag)
        if hm and is_video(hm.group(2)):
            cm = CLASS_RE.search(tag)
            classes = cm.group(2).split() if cm else []
            if "presence-link" not in classes and "root-milestone" not in classes:
                video_count += 1
        return add_video_class(tag)

    text = ANCHOR_RE.sub(anchor_repl, text)
    text, grouped = group_multi_video_evidence(text, lang_for(path))

    if lang_for(path) == "pt":
        text = text.replace("<span>Vídeos preservados</span><strong>Assista ao programa</strong>", "<span>Vídeos &amp; Mídia · 4</span><strong>Assista ao programa</strong>")
    else:
        text = text.replace("<span>Preserved videos</span><strong>Watch the program</strong>", "<span>Videos &amp; Media · 4</span><strong>Watch the program</strong>")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True, video_count, grouped
    return False, video_count, grouped


def update_css() -> bool:
    path = ROOT / "styles.css"
    css = path.read_text(encoding="utf-8")
    original = css
    css = re.sub(
        r"\n/\* High-contrast video action buttons \*/.*?(?=\n/\*[^\n]*\*/)",
        "\n",
        css,
        flags=re.S,
    )
    marker = "/* Global video & media standard — 2026-09-14 */"
    if marker not in css:
        css = css.rstrip() + "\n\n" + GLOBAL_CSS.strip() + "\n"
    if css != original:
        path.write_text(css, encoding="utf-8")
        return True
    return False


def check() -> int:
    errors: list[str] = []
    total = 0
    for path in list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.inc")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for tag in ANCHOR_RE.findall(text):
            hm = HREF_RE.search(tag)
            if not hm or not is_video(hm.group(2)):
                continue
            cm = CLASS_RE.search(tag)
            classes = cm.group(2).split() if cm else []
            if "presence-link" in classes or "root-milestone" in classes:
                continue
            total += 1
            if "video-pill" not in classes:
                errors.append(f"{rel}: video link missing video-pill: {hm.group(2)}")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    if "High-contrast video action buttons" in css:
        errors.append("styles.css: legacy high-contrast YouTube rule still present")
    if "Global video & media standard — 2026-09-14" not in css:
        errors.append("styles.css: global video standard missing")
    if errors:
        print("Global video standard check failed:")
        for e in errors:
            print(" -", e)
        return 1
    print(f"Global video standard OK: {total} content video anchors use video-pill.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    changed_files = 0
    links = 0
    groups = 0
    for path in list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.inc")):
        if ".git" in path.parts:
            continue
        changed, count, grouped = process_file(path)
        changed_files += int(changed)
        links += count
        groups += grouped
    css_changed = update_css()
    print(f"Applied global video standard: {links} content video anchors scanned; {groups} multi-video groups promoted; {changed_files} markup files changed; css_changed={css_changed}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
