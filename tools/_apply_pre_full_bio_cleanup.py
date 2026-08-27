from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected block: {label}")
    return text.replace(old, new, 1)


def replace_regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Expected exactly one match for {label}, got {count}")
    return updated


def patch_hai(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")

    if lang == "pt":
        note = '<div class="note"><strong>Escopo preciso.</strong> Este hub usa “Human–AI Interaction (HAI)” como descrição principal deste eixo. HCI aparece quando faz parte do enquadramento metodológico de um trabalho específico, mas a biografia não amplia artificialmente o escopo para sugerir uma agenda mais extensa do que a produção realmente publicada.</div>\n'
        text = replace_once(text, note, "", "PT HAI scope note")

        old_cycle = '<section id="ciclo" class="chapter"><h2>Um ciclo de pesquisa, não uma lista solta de papers</h2><p>A produção de 2025–2026 é apresentada como um arco específico. A série <strong>Melissa 1.0</strong> documenta e formaliza observações relacionais e arquiteturas de personas persistentes. O <strong>Punk Rock Orchestra v1</strong> reorganiza parte desse aprendizado em uma metodologia de triangulação epistemológica adversarial operada por um único pesquisador. O <strong>PRO v2</strong>, atualmente em desenvolvimento, foi concebido por Nicchio como a versão definitiva e o fechamento desse ciclo.</p><p>Isso não significa o fim da pesquisa independente. Significa apenas que não há, neste momento, uma agenda pública programada depois do PRO v2. O site não antecipa projetos, depósitos ou resultados editoriais que ainda não existem.</p></section>'
        new_cycle = '<section id="ciclo" class="chapter"><h2>Um ciclo de pesquisa</h2><p>A produção de 2025–2026 forma um arco específico. A série <strong>Melissa 1.0</strong> documenta e formaliza observações relacionais e arquiteturas de personas persistentes. O <strong>Punk Rock Orchestra v1</strong> reorganiza parte desse aprendizado em uma metodologia de triangulação epistemológica adversarial operada por um único pesquisador. O <strong>PRO v2</strong>, atualmente em desenvolvimento, foi concebido por Nicchio como a versão definitiva e o fechamento desse ciclo.</p></section>'
        text = replace_once(text, old_cycle, new_cycle, "PT HAI cycle")

        old_pro1 = '<p>Para o hub, essas versões não contam como “cinco publicações diferentes”. Elas são instâncias e registros do mesmo trabalho, distribuídos em ecossistemas distintos para preservação, visibilidade e acesso.</p>'
        new_pro1 = '<p>O trabalho possui registros e instâncias públicas em diferentes ecossistemas de pesquisa, preservação e acesso.</p>'
        text = replace_once(text, old_pro1, new_pro1, "PT PRO v1 registry wording")

        text = replace_regex_once(
            text,
            r'<section id="pro2" class="chapter"><h2>Punk Rock Orchestra v2 — fechamento do ciclo</h2>.*?</section>',
            '<section id="pro2" class="chapter"><h2>Punk Rock Orchestra v2 — fechamento do ciclo</h2><p>O <strong>PRO v2</strong> está em desenvolvimento e é tratado por Nicchio como a versão definitiva dessa pesquisa específica e o fechamento do ciclo iniciado com Melissa 1.0.</p></section>',
            "PT PRO v2 section",
        )
        text = replace_regex_once(
            text,
            r'<section id="rigor" class="chapter">.*?</section>\n',
            '',
            "PT rigor disclaimer",
        )
        text = replace_once(text, '<a href="#rigor">Rigor editorial</a>', '', "PT rigor aside link")
        text = replace_regex_once(text, r'<p class="aside-note">Este eixo é contemporâneo.*?</p>', '', "PT HAI aside disclaimer")
    else:
        note = '<div class="note"><strong>Precise scope.</strong> This hub uses “Human–AI Interaction (HAI)” as the primary description of this axis. HCI appears where it belongs to the methodological framing of a specific work, but the biography does not artificially expand the field beyond the published body of research.</div>\n'
        text = replace_once(text, note, "", "EN HAI scope note")

        old_cycle = '<section id="cycle" class="chapter"><h2>One research cycle, not a loose paper list</h2><p>The 2025–2026 body of work is presented as a specific arc. The <strong>Melissa 1.0</strong> series documents and formalizes relational observations and persistent persona architectures. <strong>Punk Rock Orchestra v1</strong> reorganizes part of that learning into a single-operator adversarial epistemic triangulation methodology. <strong>PRO v2</strong>, currently in development, is conceived by Nicchio as the definitive version and closure of that cycle.</p><p>This does not mean the end of independent research. It means there is currently no fixed public agenda after PRO v2. The site does not pre-announce projects, repository deposits or publication outcomes that do not yet exist.</p></section>'
        new_cycle = '<section id="cycle" class="chapter"><h2>A research cycle</h2><p>The 2025–2026 body of work forms a specific arc. The <strong>Melissa 1.0</strong> series documents and formalizes relational observations and persistent persona architectures. <strong>Punk Rock Orchestra v1</strong> reorganizes part of that learning into a single-operator adversarial epistemic triangulation methodology. <strong>PRO v2</strong>, currently in development, is conceived by Nicchio as the definitive version and closure of that cycle.</p></section>'
        text = replace_once(text, old_cycle, new_cycle, "EN HAI cycle")

        old_pro1 = '<p>For this hub, those copies do not count as “five separate publications.” They are instances and records of the same work, distributed across different ecosystems for preservation, discoverability and access.</p>'
        new_pro1 = '<p>The work has public records and instances across several research, preservation and access ecosystems.</p>'
        text = replace_once(text, old_pro1, new_pro1, "EN PRO v1 registry wording")

        text = replace_regex_once(
            text,
            r'<section id="pro2" class="chapter"><h2>Punk Rock Orchestra v2 — closing the cycle</h2>.*?</section>',
            '<section id="pro2" class="chapter"><h2>Punk Rock Orchestra v2 — closing the cycle</h2><p><strong>PRO v2</strong> is currently in development and is treated by Nicchio as the definitive version of this specific research and the closing work of the cycle begun with Melissa 1.0.</p></section>',
            "EN PRO v2 section",
        )
        text = replace_regex_once(
            text,
            r'<section id="rigor" class="chapter">.*?</section>\n',
            '',
            "EN rigor disclaimer",
        )
        text = replace_once(text, '<a href="#rigor">Editorial rigor</a>', '', "EN rigor aside link")
        text = replace_regex_once(text, r'<p class="aside-note">This axis is contemporary.*?</p>', '', "EN HAI aside disclaimer")

    path.write_text(text, encoding="utf-8")


def patch_music(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")

    if lang == "pt":
        coitado = '''<section id="coitado" class="chapter"><h2>Coitado do Próximo</h2><p>Em 1992, Marcelo Nicchio fundou o <strong>Coitado do Próximo</strong>, projeto autoral em que atuou como compositor e baterista. Desde o início, Nicchio e o vocalista formaram o núcleo do projeto, enquanto a banda atravessou diferentes formações ao longo dos anos. O grupo permaneceu continuamente ativo até seu encerramento oficial em 2003.</p><p>O primeiro show preservado em vídeo aconteceu ainda em 1992, no <strong>Barão Homem de Mello</strong>, colégio estadual em Santana, São Paulo. A partir de 1993 começaram as apresentações mais estruturadas no circuito de casas noturnas da cidade.</p><p>Em 1994 foi gravada a primeira demo-tape, com <em>Pegue o seu Celular</em> e <em>Mulher SP</em>. O áudio final e vídeos das sessões de gravação sobreviveram e aguardam publicação.</p><p>No mesmo ano, Nicchio foi entrevistado por <strong>Kid Vinil</strong> na 97FM Rock. O áudio dessa entrevista foi preservado diretamente da transmissão de rádio e também deverá integrar o arquivo público.</p></section>'''
        text = replace_regex_once(text, r'<section id="coitado" class="chapter">.*?</section>', coitado, "PT Coitado section")

        marker = '<div class="phase"><div class="phase-year">2003</div><div><h3>Encerramento</h3><p>O projeto foi encerrado após um período de desgaste interno.</p></div></div>'
        addition = '<div class="phase"><div class="phase-year">2001–2003</div><div><h3>Atividade contínua</h3><p>Depois da passagem pelo Programa do Jô, o Coitado do Próximo continuou ativo com shows e entrevistas até o encerramento oficial em 2003.</p></div></div>\n<div class="phase"><div class="phase-year">2003</div><div><h3>Encerramento</h3><p>Após uma trajetória contínua desde 1992, o projeto foi encerrado em 2003.</p></div></div>'
        text = replace_once(text, marker, addition, "PT 2001-2003 continuity phase")
    else:
        coitado = '''<section id="coitado" class="chapter"><h2>Coitado do Próximo</h2><p>In 1992, Marcelo Nicchio founded <strong>Coitado do Próximo</strong>, an original project in which he worked as composer and drummer. From the beginning, Nicchio and the vocalist formed the core of the project while the band moved through different lineups over the years. The group remained continuously active until its official end in 2003.</p><p>The first performance preserved on video took place in 1992 at <strong>Barão Homem de Mello</strong>, a state school in the Santana district of São Paulo. From 1993 onward, the band began playing more structured shows on the city's club circuit.</p><p>In 1994 it recorded its first demo tape with <em>Pegue o seu Celular</em> and <em>Mulher SP</em>. The final audio and footage from the recording sessions survive and await publication.</p><p>That same year Nicchio was interviewed by <strong>Kid Vinil</strong> on 97FM Rock. A direct recording of the radio broadcast has been preserved and is also expected to become part of the public archive.</p></section>'''
        text = replace_regex_once(text, r'<section id="coitado" class="chapter">.*?</section>', coitado, "EN Coitado section")

        marker = '<div class="phase"><div class="phase-year">2003</div><div><h3>End of the project</h3><p>The project ended after a period of internal strain.</p></div></div>'
        addition = '<div class="phase"><div class="phase-year">2001–2003</div><div><h3>Continuous activity</h3><p>After the Programa do Jô appearance, Coitado do Próximo remained active with shows and interviews until its official end in 2003.</p></div></div>\n<div class="phase"><div class="phase-year">2003</div><div><h3>End of the project</h3><p>After a continuous trajectory beginning in 1992, the project officially ended in 2003.</p></div></div>'
        text = replace_once(text, marker, addition, "EN 2001-2003 continuity phase")

    path.write_text(text, encoding="utf-8")


patch_hai(ROOT / "pt/ia-hai/index.html", "pt")
patch_hai(ROOT / "en/ai-hai/index.html", "en")
patch_music(ROOT / "pt/musica/index.html", "pt")
patch_music(ROOT / "en/music/index.html", "en")

# Self-clean: these bootstrap files must not remain in the final branch diff.
for rel in ["tools/_apply_pre_full_bio_cleanup.py", ".github/workflows/pre-full-bio-editorial-cleanup.yml"]:
    p = ROOT / rel
    if p.exists():
        p.unlink()

print("Pre-Full-Bio editorial cleanup applied.")
