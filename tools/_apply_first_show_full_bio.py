from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.youtube.com/watch?v=7yjYTV1L0b0"

replacements = {
    "pt/musica/index.html": (
        '<p>O primeiro show preservado em vídeo aconteceu ainda em 1992, no <strong>Barão Homem de Mello</strong>, colégio estadual em Santana, São Paulo. A partir de 1993 começaram as apresentações mais estruturadas no circuito de casas noturnas da cidade.</p>',
        '<p>O primeiro show preservado em vídeo aconteceu em <strong>5 de julho de 1992</strong>, na <strong>Escola Estadual “Barão Homem de Mello”</strong>, na Rua Alfredo Pujol, 1555, em Santana, São Paulo (SP). A marcação de data e hora da própria câmera confirma a data do registro. A partir de 1993 começaram as apresentações mais estruturadas no circuito de casas noturnas da cidade.</p><div class="evidence-links inline-links"><a href="' + URL + '" target="_blank" rel="noopener noreferrer">1º show — abertura · 5 jul. 1992 ↗</a></div>'
    ),
    "en/music/index.html": (
        '<p>The first performance preserved on video took place in 1992 at <strong>Barão Homem de Mello</strong>, a state school in the Santana district of São Paulo. From 1993 onward, the band began playing more structured shows on the city\'s club circuit.</p>',
        '<p>The first performance preserved on video took place on <strong>July 5, 1992</strong>, at <strong>Escola Estadual “Barão Homem de Mello”</strong>, Rua Alfredo Pujol, 1555, in Santana, São Paulo. The camera\'s own date-and-time stamp confirms the date of the recording. From 1993 onward, the band began playing more structured shows on the city\'s club circuit.</p><div class="evidence-links inline-links"><a href="' + URL + '" target="_blank" rel="noopener noreferrer">First show — opening · Jul. 5, 1992 ↗</a></div>'
    ),
}

for rel, (old, new) in replacements.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if new not in text:
        if old not in text:
            raise SystemExit(f"Expected source paragraph not found in {rel}")
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")

manifest_path = ROOT / "data/full_biography.json"
data = json.loads(manifest_path.read_text(encoding="utf-8"))
for entry in data["entries"]:
    if entry["id"] == "music-coitado-1992":
        entry["date"] = "5 jul. 1992"
        entry["date_en"] = "Jul. 5, 1992"
        break
else:
    raise SystemExit("music-coitado-1992 not found in manifest")
manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

subprocess.run([sys.executable, str(ROOT / "tools/sync_full_biography.py")], cwd=ROOT, check=True)

for rel in ["tools/_apply_first_show_full_bio.py", ".github/workflows/apply-first-show-full-bio.yml"]:
    path = ROOT / rel
    if path.exists():
        path.unlink()

print("Exact first-show date propagated to Music and Full Biography PT/EN.")
