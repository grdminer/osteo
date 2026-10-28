import os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content, changes
import pymupdf
from playwright.sync_api import sync_playwright

OUT = os.path.join(HERE, '..', 'pdf')
COL = {  # Markierung, Etikett
 'recht':   ((0.95, 0.66, 0.56), (0.60, 0.23, 0.15)),
 'neu':     ((0.74, 0.87, 0.64), (0.33, 0.44, 0.19)),
 'sprache': ((0.70, 0.82, 0.93), (0.24, 0.41, 0.60)),
}
HEX = {'recht': '#9a3b27', 'neu': '#55702f', 'sprache': '#3d6999'}
e = html.escape

def protocol_html(title, entries, vergleich='im Vergleich zur Fassung vom 01.01.2023'):
    used = []
    for c in entries:
        for q in c[8]:
            if q not in used: used.append(q)
    num = {q: i + 1 for i, q in enumerate(used)}
    cards = []
    for (cid, pg, anchor, kind, stelle, bisher, neu, grund, qs) in entries:
        refs = ', '.join(f'<a href="#q-{q}">[{num[q]}] {e(changes.Q[q][0])}</a>' for q in qs) or '–'
        cards.append(f'''<article class="card">
  <header><span class="id" style="background:{HEX[kind]}">{cid}</span><b>{e(stelle)}</b><span class="meta">Seite {pg}, {changes.KIND[kind]}</span></header>
  <dl><dt>Bisher</dt><dd class="old">{e(bisher)}</dd>
  <dt>Änderung</dt><dd>{e(neu)}</dd>
  <dt>Grund</dt><dd>{e(grund)}</dd>
  <dt>Fundstellen</dt><dd class="refs">{refs}</dd></dl></article>''')
    srcs = ''.join(f'<li id="q-{q}">{e(changes.Q[q][0])}<br><a href="{changes.Q[q][1]}">{e(changes.Q[q][1])}</a></li>' for q in used)
    legend = ''.join(f'<span class="chip"><i style="background:{HEX[k]}"></i>{v}</span>' for k, v in changes.KIND.items())
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><link rel="stylesheet" href="doc.css">
<style>
@page {{ size: A4; margin: 16mm 18mm 20mm 20mm; }}
body {{ font-size: 9pt; }}
h1 {{ font-size: 18pt; }}
.chip {{ display:inline-flex; align-items:center; gap:1.6mm; margin-right:5mm; font-size:8.6pt; }}
.chip i {{ width:3.2mm; height:3.2mm; border-radius:.6mm; display:inline-block; }}
.card {{ border-top: .6pt solid var(--line); padding: 3mm 0 2.5mm; break-inside: avoid; }}
.card header {{ display:flex; align-items:baseline; gap:2.5mm; margin-bottom:1.6mm; }}
.card .id {{ color:#fff; font-weight:700; font-size:8pt; padding:.5mm 1.6mm; border-radius:.8mm; }}
.card b {{ font-family:"Literata",serif; font-weight:500; font-size:10.2pt; }}
.card .meta {{ margin-left:auto; color:var(--muted); font-size:7.8pt; white-space:nowrap; }}
dl {{ display:grid; grid-template-columns: 21mm 1fr; column-gap:4mm; row-gap:1.2mm; margin:0; }}
dt {{ color:var(--muted); font-size:8pt; padding-top:.3mm; }}
dd {{ margin:0; }}
dd.old {{ color:var(--muted); font-style:italic; }}
a {{ color: var(--clay); text-decoration: none; }}
.refs a {{ white-space: normal; }}
ol.src {{ padding-left:5mm; font-size:8.4pt; }} ol.src li {{ margin-bottom:1.6mm; overflow-wrap:anywhere; }}
.warn {{ background: var(--wash); border-left:1.4pt solid var(--cinnabar); padding:3mm 4mm; margin:4mm 0 5mm; }}
</style></head><body>
<h1>Änderungsprotokoll</h1>
<p class="lead" style="max-width:none">{e(title)}, Fassung {content.STAND}, {vergleich}. Die Nummern entsprechen den Markierungen am Seitenrand; die Kommentare enthalten jeweils denselben Text.</p>
<p>{legend}</p>
<div class="warn">Die Begründungen beruhen auf den genannten Gesetzestexten und Quellen und ersetzen keine Rechtsberatung. Vor dem Einsatz sollte das Dokument von einer Fachperson für Medizinrecht geprüft werden.</div>
{''.join(cards)}
<h3 style="margin-top:6mm">Quellen</h3><ol class="src">{srcs}</ol>
</body></html>'''

def comment_text(c):
    cid, pg, anchor, kind, stelle, bisher, neu, grund, qs = c
    refs = '; '.join(f'{changes.Q[q][0]} ({changes.Q[q][1]})' for q in qs) or 'keine'
    return f'{cid} – {stelle} ({changes.KIND[kind]})\n\nBisher: {bisher}\n\nÄnderung: {neu}\n\nGrund: {grund}\n\nFundstellen: {refs}'

