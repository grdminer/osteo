import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content
import pymupdf
from playwright.sync_api import sync_playwright

OUT = os.path.join(HERE, '..', 'pdf')
os.makedirs(OUT, exist_ok=True)
JOBS = [('Behandlungsvertrag', content.VERTRAG, 'Behandlungsvertrag Stand Oktober 2026.pdf'),
        ('Patientenaufnahmebogen', content.AUFNAHME, 'Patientenaufnahmebogen Stand Oktober 2026.pdf')]

PROBE = """() => {
  const pages=[...document.querySelectorAll('.page')];
  const over=pages.map((p,i)=>{ const pr=p.getBoundingClientRect(); const foot=p.querySelector('.foot').getBoundingClientRect();
     let maxB=0; p.querySelectorAll(':scope > *:not(.foot):not(.enso)').forEach(e=>{maxB=Math.max(maxB,e.getBoundingClientRect().bottom)});
     return {page:i+1, free_mm: Math.round((foot.top-maxB)/3.7795*10)/10}; });
  const fields=[...document.querySelectorAll('[data-n]')].map(e=>{ const p=e.closest('.page'); const pr=p.getBoundingClientRect(); const r=e.getBoundingClientRect();
     return {n:e.dataset.n, t:e.dataset.t, page:pages.indexOf(p), x:r.left-pr.left, y:r.top-pr.top, w:r.width, h:r.height}; });
  return {over, fields};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, fn in JOBS:
        hp = os.path.join(HERE, name + '.html'); open(hp, 'w').write(html)
        pg = b.new_page(viewport={'width': 794, 'height': 1123})
        pg.goto('file://' + hp); pg.wait_for_timeout(500)
        pg.emulate_media(media='print')
        info = pg.evaluate(PROBE)
        print(name, info['over'])
        raw = os.path.join(OUT, name + '_raw.pdf')
        pg.pdf(path=raw, format='A4', print_background=True, prefer_css_page_size=True)
        doc = pymupdf.open(raw)
        k = 0.75  # CSS px -> pt
        for fd in info['fields']:
            page = doc[fd['page']]
            r = pymupdf.Rect(fd['x']*k, fd['y']*k, (fd['x']+fd['w'])*k, (fd['y']+fd['h'])*k)
            w = pymupdf.Widget()
            w.field_name = fd['n']
            if fd['t'] == 'check':
                w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
                w.rect = r; w.field_value = False
                w.border_width = 0
            else:
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                if fd['t'] == 'multi':
                    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
                    w.rect = pymupdf.Rect(r.x0+3, r.y0+2, r.x1-3, r.y1-1); w.text_fontsize = 10
                else:
                    w.rect = pymupdf.Rect(r.x0, r.y0+3, r.x1, r.y1-1); w.text_fontsize = 10
                w.text_font = 'Helv'; w.border_width = 0
            w.text_color = (0.17, 0.14, 0.12)
            page.add_widget(w); k  # noqa
        doc.set_metadata({'title': f'{name} – Gunnar Götze', 'author': 'Gunnar Götze, Heilpraktiker und Physiotherapeut', 'subject': content.STAND})
        out = os.path.join(OUT, fn)
        doc.save(out, garbage=3, deflate=True); doc.close()
        print('saved', out, len(info['fields']), 'fields')
    b.close()
