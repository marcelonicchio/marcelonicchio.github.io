#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
GALLERIES = ROOT / "data/galleries.json"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def optimize_thread(source_rel: str, output_rel: str, max_width: int = 1100, max_bytes: int = 280_000) -> tuple[int, int, int]:
    source = ROOT / source_rel
    output = ROOT / output_rel
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        if im.mode == "RGBA":
            base = Image.new("RGB", im.size, "white")
            base.paste(im, mask=im.getchannel("A"))
            im = base
        if im.width > max_width:
            h = max(1, round(im.height * max_width / im.width))
            im = im.resize((max_width, h), Image.Resampling.LANCZOS)

        quality = 84
        while True:
            im.save(output, "WEBP", quality=quality, method=6)
            size = output.stat().st_size
            if size <= max_bytes or quality <= 58:
                break
            quality -= 4
        while output.stat().st_size > max_bytes and im.width > 760:
            nw = max(760, round(im.width * 0.9))
            nh = max(1, round(im.height * nw / im.width))
            im = im.resize((nw, nh), Image.Resampling.LANCZOS)
            im.save(output, "WEBP", quality=quality, method=6)
        return im.width, im.height, output.stat().st_size


def thread_figure(*, marker: str, source_rel: str, web_rel: str, width: int, height: int,
                  alt: str, caption: str, open_label: str, aria: str) -> str:
    return f'''<!-- thread-media:{marker}:start -->
<figure class="thread-media thread-media--linked">
<a aria-label="{esc(aria)}" href="/{esc(source_rel)}" rel="noopener noreferrer" target="_blank">
<img alt="{esc(alt)}" decoding="async" height="{height}" loading="lazy" src="/{esc(web_rel)}" width="{width}"/>
</a>
<figcaption><strong>{esc(caption)}</strong><a class="thread-media-open" href="/{esc(source_rel)}" rel="noopener noreferrer" target="_blank">{esc(open_label)}</a></figcaption>
</figure>
<!-- thread-media:{marker}:end -->'''


def insert_after_first_paragraph(text: str, block: str, marker: str) -> str:
    if f"<!-- thread-media:{marker}:start -->" in text:
        return text
    match = re.search(r"</p>", text, flags=re.I)
    if not match:
        raise RuntimeError(f"No paragraph found for thread media {marker}")
    return text[:match.end()] + "\n" + block + text[match.end():]


def add_gallery_placeholder(text: str, gid: str) -> str:
    if f"<!-- gallery:{gid}" in text or f'data-gallery="{gid}"' in text:
        return text
    return text.rstrip() + f"\n<!-- gallery:{gid} -->\n"


def update_fragment(path_rel: str, *, figure: str | None = None, marker: str | None = None, gid: str) -> None:
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    if figure and marker:
        text = insert_after_first_paragraph(text, figure, marker)
    text = add_gallery_placeholder(text, gid)
    path.write_text(text, encoding="utf-8")


def section_pattern(section_id: str) -> re.Pattern[str]:
    escaped = re.escape(section_id)
    return re.compile(rf'(<section\b(?=[^>]*\bid=["\']{escaped}["\'])[^>]*>)(.*?)(</section>)', re.S | re.I)


def update_section(path_rel: str, section_id: str, *, figure: str | None = None, marker: str | None = None, gid: str) -> None:
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    pat = section_pattern(section_id)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{path_rel} #{section_id}: expected one section, got {len(matches)}")
    m = matches[0]
    inner = m.group(2)
    if figure and marker:
        inner = insert_after_first_paragraph(inner, figure, marker)
    if f"<!-- gallery:{gid}" not in inner and f'data-gallery="{gid}"' not in inner:
        inner = inner.rstrip() + f"\n<!-- gallery:{gid} -->\n"
    updated = text[:m.start()] + m.group(1) + inner + m.group(3) + text[m.end():]
    path.write_text(updated, encoding="utf-8")


def item(i: int | str, source: str, pt: str, en: str) -> dict:
    return {"id": f"{int(i):02d}" if isinstance(i, int) or str(i).isdigit() else str(i), "source": source, "caption": {"pt": pt, "en": en}}


def numbered_items(sources: Iterable[str], pt_base: str, en_base: str) -> list[dict]:
    return [item(i, source, f"{pt_base} {i}.", f"{en_base} {i}.") for i, source in enumerate(sources, 1)]


def upsert_gallery(data: dict, gallery: dict) -> None:
    galleries = data.setdefault("galleries", [])
    for idx, existing in enumerate(galleries):
        if existing.get("id") == gallery["id"]:
            galleries[idx] = gallery
            return
    galleries.append(gallery)


def main() -> int:
    # Web-friendly editorial Thread images. Masters remain untouched in assets/archive.
    thread_specs = {
        "best-kenshoo": (
            "assets/archive/internet/best-kenshoo/best00_thread_palestra01.png",
            "assets/media/thread/best-kenshoo-workshop.webp",
        ),
        "psinet": (
            "assets/archive/internet/psinet/PSINet00_Thread-Psinet-STI_Sede-Alphaville.jpg",
            "assets/media/thread/psinet-alphaville.webp",
        ),
        "prateleira-cultural": (
            "assets/archive/communication/prateleira-cultural/prateleiracultural_thread_marcelo-nicchio.jpg",
            "assets/media/thread/prateleira-cultural.webp",
        ),
    }
    dims = {}
    for key, (source, output) in thread_specs.items():
        dims[key] = optimize_thread(source, output)
        print(f"thread {key}: {dims[key][0]}x{dims[key][1]} {dims[key][2]} bytes")

    bw, bh, _ = dims["best-kenshoo"]
    best_pt = thread_figure(
        marker="best-kenshoo", source_rel=thread_specs["best-kenshoo"][0], web_rel=thread_specs["best-kenshoo"][1], width=bw, height=bh,
        alt="Registro do workshop do E-Commerce Brasil durante o ciclo BEST/Kenshoo.",
        caption="Workshop do E-Commerce Brasil durante o ciclo BEST/Kenshoo, 2014.",
        open_label="Abrir imagem original ↗", aria="Abrir a fotografia original do workshop BEST/Kenshoo"
    )
    best_en = thread_figure(
        marker="best-kenshoo", source_rel=thread_specs["best-kenshoo"][0], web_rel=thread_specs["best-kenshoo"][1], width=bw, height=bh,
        alt="Record of the E-Commerce Brasil workshop during the BEST/Kenshoo period.",
        caption="E-Commerce Brasil workshop during the BEST/Kenshoo period, 2014.",
        open_label="Open original image ↗", aria="Open the original BEST/Kenshoo workshop photo"
    )

    pw, ph, _ = dims["psinet"]
    psinet_pt = thread_figure(
        marker="psinet", source_rel=thread_specs["psinet"][0], web_rel=thread_specs["psinet"][1], width=pw, height=ph,
        alt="Registro da sede PSINet/STI em Alphaville.", caption="Sede da PSINet/STI em Alphaville, c. 2000.",
        open_label="Abrir imagem original ↗", aria="Abrir a fotografia original da PSINet em Alphaville"
    )
    psinet_en = thread_figure(
        marker="psinet", source_rel=thread_specs["psinet"][0], web_rel=thread_specs["psinet"][1], width=pw, height=ph,
        alt="Record of the PSINet/STI office in Alphaville.", caption="PSINet/STI office in Alphaville, c. 2000.",
        open_label="Open original image ↗", aria="Open the original PSINet Alphaville photo"
    )

    sw, sh, _ = dims["prateleira-cultural"]
    prateleira_pt = thread_figure(
        marker="prateleira-cultural", source_rel=thread_specs["prateleira-cultural"][0], web_rel=thread_specs["prateleira-cultural"][1], width=sw, height=sh,
        alt="Marcelo Nicchio no período da coluna Prateleira Cultural na Revista Sinal Verde.",
        caption="Marcelo Nicchio no período da coluna Prateleira Cultural, Revista Sinal Verde.",
        open_label="Abrir imagem original ↗", aria="Abrir a fotografia original da Prateleira Cultural"
    )
    prateleira_en = thread_figure(
        marker="prateleira-cultural", source_rel=thread_specs["prateleira-cultural"][0], web_rel=thread_specs["prateleira-cultural"][1], width=sw, height=sh,
        alt="Marcelo Nicchio during the Prateleira Cultural column period at Revista Sinal Verde.",
        caption="Marcelo Nicchio during the Prateleira Cultural column period at Revista Sinal Verde.",
        open_label="Open original image ↗", aria="Open the original Prateleira Cultural photo"
    )

    # Fragment-backed entries: edit their neutral sources, then sync_entries propagates them.
    update_fragment("content/entries/pt/internet-best.inc", figure=best_pt, marker="best-kenshoo", gid="best-kenshoo")
    update_fragment("content/entries/en/internet-best.inc", figure=best_en, marker="best-kenshoo", gid="best-kenshoo")
    update_fragment("content/entries/pt/communication-folha.inc", gid="folha-orfaos-do-rock")
    update_fragment("content/entries/en/communication-folha.inc", gid="folha-orfaos-do-rock")

    # Vertical-backed entries: Full Biography remains generated downstream.
    update_section("pt/internet/index.html", "psinet", figure=psinet_pt, marker="psinet", gid="psinet")
    update_section("en/internet/index.html", "psinet", figure=psinet_en, marker="psinet", gid="psinet")
    update_section("pt/internet/index.html", "petlove", gid="petlove")
    update_section("en/internet/index.html", "petlove", gid="petlove")
    update_section("pt/comunicacao/index.html", "sinal-verde", figure=prateleira_pt, marker="prateleira-cultural", gid="prateleira-cultural")
    update_section("en/communication/index.html", "sinal-verde", figure=prateleira_en, marker="prateleira-cultural", gid="prateleira-cultural")

    data = json.loads(GALLERIES.read_text(encoding="utf-8"))
    data["updated"] = "2026-09-01"

    best_sources = [
        "best00_palestra02_tratamento-ia.jpg",
        "best00_palestra03_tratamento-_ia.jpg",
        "best00_palestra04_tratamento-ia.jpg",
        "best00_palestra05_tratamento-ia.jpg",
        "best00_palestra06_tratamento-ia_.jpg",
        "best01-cartao.jpg",
        "best02-escritorio01.jpg",
        "best03-escritorio02.jpg",
        "best04-escritorio03-ia.jpg",
        "best05-clientes.JPG",
        "best06-claudio-coelho_chap-chap_marcelo-nicchio_roger-lopes.JPG",
    ]
    best_items = []
    for i, source in enumerate(best_sources, 1):
        if i <= 5:
            pt, en = "Registro do workshop com tratamento por IA.", "Workshop record with AI treatment."
        elif i == 6:
            pt, en = "Cartão profissional do período BEST/Kenshoo.", "Professional card from the BEST/Kenshoo period."
        elif i in (7, 8):
            pt, en = "Registro do escritório da BEST.", "Record of the BEST office."
        elif i == 9:
            pt, en = "Registro do escritório com tratamento por IA.", "Office record with AI treatment."
        elif i == 10:
            pt, en = "Registro visual de clientes da operação.", "Visual record of operation clients."
        else:
            pt, en = "Claudio Coelho, Chap Chap, Marcelo Nicchio e Roger Lopes.", "Claudio Coelho, Chap Chap, Marcelo Nicchio and Roger Lopes."
        best_items.append(item(i, source, pt, en))

    folha_sources = [
        "folhateen - 23-04-2000 - Reportagem - Órfãos do Rock Pag 1de2 (1-2) - 300dpi.jpg",
        "folhateen - 23-04-2000 - Reportagem - Órfãos do Rock Pag 1de2 (2-2) - 300dpi.jpg",
        "folhateen - 23-04-2000 - Reportagem - Órfãos do Rock Pag 2de2 - 300dpi.jpg",
    ]
    folha_items = [
        item(1, folha_sources[0], "Folhateen — primeira página da matéria ‘Órfãos do Rock’, scan 1.", "Folhateen — first page of the ‘Órfãos do Rock’ article, scan 1."),
        item(2, folha_sources[1], "Folhateen — primeira página da matéria ‘Órfãos do Rock’, scan 2.", "Folhateen — first page of the ‘Órfãos do Rock’ article, scan 2."),
        item(3, folha_sources[2], "Folhateen — segunda página da matéria ‘Órfãos do Rock’.", "Folhateen — second page of the ‘Órfãos do Rock’ article."),
    ]

    petlove_sources = [f"petlove{i:02d}.jpg" for i in range(1, 12)]
    psinet_sources = [f"PSINet{i:02d}.jpg" for i in range(1, 6)]

    prateleira_sources = [
        "sinalverde01.jpg", "sinalverde02-novo.jpg", "sinalverde03-novo.jpg", "sinalverde04.jpg", "sinalverde05.jpg", "sinalverde06.jpg", "sinalverde07.jpg",
        "sinalverde08-01novo.jpg", "sinalverde08-02novo.jpg", "sinalverde09.jpg", "sinalverde10.jpg", "sinalverde11.jpg", "sinalverde12.jpg", "sinalverde13.jpg",
        "sinalverde14.jpg", "sinalverde15.jpg", "sinalverde16.jpg", "sinalverde17.jpg", "sinalverde18.jpg", "sinalverde19.jpg", "sinalverde20.jpg", "sinalverde21.jpg",
        "sinalverde22.jpg", "sinalverde23.jpg",
    ]
    prateleira_items = []
    column_labels = ["01", "02", "03", "04", "05", "06", "07", "08 — parte 1", "08 — parte 2", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
    for i, (source, label) in enumerate(zip(prateleira_sources, column_labels), 1):
        en_label = label.replace("parte", "part")
        prateleira_items.append(item(i, source, f"Prateleira Cultural — coluna {label}.", f"Prateleira Cultural — column {en_label}."))

    upsert_gallery(data, {
        "id": "best-kenshoo",
        "sourceRoot": "assets/archive/internet/best-kenshoo",
        "targets": {"pt": ["content/entries/pt/internet-best.inc"], "en": ["content/entries/en/internet-best.inc"]},
        "title": {"pt": "Fotos e registros", "en": "Photos and records"},
        "items": best_items,
    })
    upsert_gallery(data, {
        "id": "folha-orfaos-do-rock",
        "sourceRoot": "assets/archive/communication/folha-orfaos-do-rock",
        "targets": {"pt": ["content/entries/pt/communication-folha.inc"], "en": ["content/entries/en/communication-folha.inc"]},
        "title": {"pt": "Scans da matéria", "en": "Article scans"},
        "items": folha_items,
    })
    upsert_gallery(data, {
        "id": "petlove",
        "sourceRoot": "assets/archive/internet/petlove",
        "targets": {"pt": ["pt/internet/index.html"], "en": ["en/internet/index.html"]},
        "title": {"pt": "Fotos", "en": "Photos"},
        "items": numbered_items(petlove_sources, "Registro fotográfico do período na Petlove", "Photographic record from the Petlove period"),
    })
    upsert_gallery(data, {
        "id": "psinet",
        "sourceRoot": "assets/archive/internet/psinet",
        "targets": {"pt": ["pt/internet/index.html"], "en": ["en/internet/index.html"]},
        "title": {"pt": "Fotos", "en": "Photos"},
        "items": numbered_items(psinet_sources, "Registro fotográfico do período na PSINet", "Photographic record from the PSINet period"),
    })
    upsert_gallery(data, {
        "id": "prateleira-cultural",
        "sourceRoot": "assets/archive/communication/prateleira-cultural",
        "targets": {"pt": ["pt/comunicacao/index.html"], "en": ["en/communication/index.html"]},
        "title": {"pt": "Páginas digitalizadas", "en": "Digitized pages"},
        "items": prateleira_items,
    })

    GALLERIES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Registered five gallery batches and three Thread images.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
