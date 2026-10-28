import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content, changes
from content import ph, masthead, foot
import review_lib as R
import pymupdf
from playwright.sync_api import sync_playwright

T = 'Patienteninformation Honorar 2027'
body = f'''
<h1>Neues Honorar ab 1.&nbsp;Januar&nbsp;2027</h1>
<div class="price">
  <div class="amount">100&nbsp;€</div>
  <div><p><b>pro Behandlung ab dem 1.&nbsp;Januar&nbsp;2027</b>, bisher 80&nbsp;Euro.</p>
  <p>Das gilt für Erst- und Folgebehandlungen. Eine Behandlung dauert 50 Minuten.</p></div>
</div>
<p class="salut">Liebe Patientinnen, liebe Patienten,</p>
<p>zum 1.&nbsp;Januar 2027 passe ich mein Honorar an. Die Kosten für den Praxisbetrieb, für Praxisbedarf und Energie sind in den vergangenen Jahren deutlich gestiegen. Mit dem neuen Honorar kann ich mir weiterhin die volle Behandlungszeit für Ihre Befundung und Behandlung nehmen, mich regelmäßig fort- und weiterbilden und die Praxis so führen, wie Sie es kennen.</p>
<h3>Erstattung durch Ihre Versicherung</h3>
<p>Die Abrechnung erfolgt weiterhin in Anlehnung an das Gebührenverzeichnis für Heilpraktiker (GebüH). Ob und in welcher Höhe Sie Kosten erstattet bekommen, hängt von Ihrer Versicherung ab. Private Kranken- und Zusatzversicherungen erstatten je nach Tarif. Die Beihilfe erstattet Heilpraktikerleistungen nur bis zu festgelegten Höchstbeträgen. Einige gesetzliche Krankenkassen zahlen einen Zuschuss, meist nur mit einer ärztlichen Bescheinigung, die vor der Behandlung ausgestellt wurde. Es kann daher ein Eigenanteil entstehen. Bitte erkundigen Sie sich direkt bei Ihrer Versicherung.</p>
<h3>Fragen</h3>
<p>Bei Fragen zum Honorar oder zur Erstattung sprechen Sie mich gern an, in der Praxis, unter 0159&nbsp;01758367 oder per E-Mail an osteopathie.goetze@gmail.com. Vielen Dank für Ihr Vertrauen.</p>
<div class="closing">
  <p>Mit besten Grüßen</p>
  <p class="name">Gunnar Götze</p>
  <p class="small">Heilpraktiker und Physiotherapeut</p>
</div>
<div class="member"><img src="hpo.jpg" alt=""><span>Mitglied der hpO – Berufsvereinigung für heilkundlich praktizierte Osteopathie e.&nbsp;V.</span></div>
'''
css = '''<style>
.price { display:flex; gap:7mm; align-items:center; background:var(--wash); border-left:1.6pt solid var(--clay); padding:5mm 6mm; margin:4mm 0 8mm; border-radius:0 1.5mm 1.5mm 0; max-width:150mm; }
.price .amount { font-family:"Literata",serif; font-size:30pt; color:var(--clay); line-height:1; white-space:nowrap; }
.price p { margin:0 0 1mm; font-size:10.4pt; } .price p:last-child { margin:0; color:var(--muted); font-size:9.6pt; }
.page p { font-size:10.4pt; line-height:1.55; max-width:150mm; margin-bottom:3mm; }
.page h3 { font-size:11.5pt; margin:6mm 0 1.6mm; }
.salut { margin-top:2mm; }
.closing { margin-top:8mm; } .closing p { margin:0; } .closing .name { font-family:"Literata",serif; font-size:13pt; margin-top:6mm; }
.member { position:absolute; left:20mm; right:18mm; bottom:24mm; display:flex; align-items:center; gap:4mm; border-top:.6pt solid var(--line); padding-top:4mm; font-size:8.2pt; color:var(--muted); }
.member img { height:9mm; width:auto; }
.page:first-child .lead { max-width:122mm; }
.enso { top:auto; bottom:38mm; right:22mm; width:42mm; height:42mm; opacity:.09; }
</style>'''
html = content.doc(T, [body]).replace('<link rel="stylesheet" href="doc.css">', '<link rel="stylesheet" href="doc.css">' + css)
html = html.replace(f'<span>Seite 1 von 1</span>', '<span></span>')

# Änderungsvermerke: (id, Seite, Fundtext, Art, Stelle, bisher, Änderung, Grund, Quellen)
changes.Q['zbb'] = ('Zentrale Bezügestelle Brandenburg: Informationsblatt Heilpraktikerleistungen, Stand 01.01.2026', 'https://zbb.brandenburg.de/sixcms/media.php/9/Informationsblatt%20Heilpraktikerleistungen%20Stand%2001_26.pdf')
changes.Q['hwg3'] = ('§ 3 HWG – Irreführende Werbung', 'https://lxgesetze.de/hwg/3')
E = [
 ('P1', 1, 'Gunnar Götze', 'sprache', 'Briefkopf',
  'Altes Logo; Kopfzeile „Physiotherapeut / Gunnar Götze / Heilpraktiker“; „15827 Dahlewitz“, „01590-1758367“.',
  'Briefkopf wie Website und neue Formulare (Siegel, Name, Berufsbezeichnung); Anschrift mit Gemeinde und Ortsteil; E-Mail ergänzt.',
  'Einheitlicher Auftritt und vollständige Kontaktdaten.', []),
 ('P2', 1, 'pro Behandlung ab dem', 'recht', 'Preisangabe',
  '„Neue Behandlungshonorare ab 1. Januar 2027: 100 € pro osteopathischer Behandlung“; der bisherige Preis wird nicht genannt.',
  'Hervorgehobener Kasten mit neuem und bisherigem Preis (bisher 80 Euro), Geltung für Erst- und Folgebehandlungen und Behandlungsdauer. Bitte klären: Gelten die 100 Euro auch für physiotherapeutische Behandlungen? Im Original steht „osteopathische Behandlung“; im Kasten steht jetzt allgemein „Behandlung“.',
  'Patienten sollen die Änderung nachvollziehen können. Über die voraussichtlichen Kosten ist vor der Behandlung in Textform zu informieren; der Brief erfüllt das für 2027, wenn er rechtzeitig vor dem ersten Termin im neuen Jahr ausgehändigt wird. Der Preis muss dann auch in den Behandlungsvertrag übernommen werden.',
  ['bgb630c']),
 ('P3', 1, 'passe ich mein Honorar an', 'sprache', 'Begründung',
  'Einleitungsabsatz, Abschnitt „Warum diese Anpassung notwendig ist“ und Aufzählung mit drei Punkten; Preis und Datum dreimal, Dank zweimal genannt.',
  'Begründung in einem Absatz zusammengefasst, Wiederholungen entfernt; der Brief passt auf eine Seite.',
  'Lesbarkeit; die eigentliche Information steht so am Anfang.', []),
 ('P4', 1, 'mich regelmäßig fort- und weiterbilden', 'recht', 'Werbeaussagen',
  '„… individuelle osteopathische Behandlung auf hohem Niveau …“, „Kontinuierliche Fort- und Weiterbildungen auf aktuellstem wissenschaftlichem und therapeutischem Stand“, „Ausreichend Behandlungszeit … zu garantieren (ohne Fließband-Taktung)“.',
  'Ersetzt durch überprüfbare Aussagen: volle Behandlungszeit, regelmäßige Fort- und Weiterbildung. „Garantieren“ und „ohne Fließband-Taktung“ gestrichen.',
  'Für Heilpraktiker gilt das Heilmittelwerbegesetz; irreführende Aussagen über Behandlungen sind unzulässig, und Qualitätsbehauptungen müssen im Streitfall belegt werden. „Garantieren“ klingt im Gesundheitsbereich nach einem Versprechen; die Spitze gegen andere Praxen ist unnötig.',
  ['hwg3']),
 ('P5', 1, 'Erstattung durch Ihre Versicherung', 'neu', 'Erstattung',
  '„Hinweis für privat Versicherte und Zusatzversicherte: … Ob und in welcher Höhe Ihre private Krankenversicherung oder Zusatzversicherung die Kosten erstattet, hängt von Ihrem Tarif ab.“',
  'Ergänzt um Beihilfe (Höchstbeträge), Zuschüsse gesetzlicher Krankenkassen (ärztliche Bescheinigung) und den Hinweis auf einen möglichen Eigenanteil.',
  'Heilpraktikerleistungen sind in der Beihilfe nur bis zu den Höchstbeträgen der Anlage 2 BBhV beihilfefähig. Kassenzuschüsse setzen meist eine vorherige ärztliche Bescheinigung voraus, z. B. bei der TK. Ob 100 Euro über den Beihilfe-Höchstbeträgen liegen, wurde nicht nachgerechnet.',
  ['zbb', 'tk']),
 ('P6', 1, 'Bei Fragen zum Honorar', 'sprache', 'Fragen und Gruß',
  '„Vielen Dank für Ihr Vertrauen“ als Überschrift, danach „Vielen Dank für Ihr Verständnis und Ihr Vertrauen. Bei Fragen … sprechen Sie mich gerne persönlich an.“',
  'Kontaktwege (Telefon, E-Mail) genannt; Dank einmal; Gruß mit Berufsbezeichnung.', 'Lesbarkeit, vollständige Kontaktdaten.', []),
 ('P7', 1, 'Mitglied der hpO', 'sprache', 'Verbandslogo',
  'hpO-Logo ohne Text am Seitenende.',
  'Logo mit erklärendem Text „Mitglied der hpO …“.',
  'Ohne Text ist das Logo für Patienten nicht verständlich. Bitte prüfen, ob die Mitgliedschaft aktuell ist und das Logo so verwendet werden darf.', []),
]

OUT = os.path.join(HERE, '..', 'pdf')
with sync_playwright() as p:
    b = p.chromium.launch()
    hp = os.path.join(HERE, 'patinfo.html'); open(hp, 'w').write(html)
    pg = b.new_page(viewport={'width': 794, 'height': 1123}); pg.goto('file://' + hp); pg.wait_for_timeout(500)
    info = pg.evaluate("""()=>{const p=document.querySelector('.page');const m=document.querySelector('.member').getBoundingClientRect();
      let maxB=0; p.querySelectorAll(':scope > *:not(.foot):not(.enso):not(.member)').forEach(e=>{maxB=Math.max(maxB,e.getBoundingClientRect().bottom)});
      return {pages:document.querySelectorAll('.page').length, free_mm:Math.round((m.top-maxB)/3.7795*10)/10}}""")
    print(info)
    clean = os.path.join(OUT, f'{T}.pdf')
    pg.pdf(path=clean, format='A4', print_background=True, prefer_css_page_size=True)
    d = pymupdf.open(clean); d.set_metadata({'title': 'Neues Honorar ab 1. Januar 2027 – Gunnar Götze', 'author': 'Gunnar Götze', 'subject': content.STAND}); d.saveIncr(); d.close()
    # Prüffassung
    hp2 = os.path.join(HERE, 'protokoll_patinfo.html')
    open(hp2, 'w').write(R.protocol_html('Patienteninformation zur Honoraranpassung 2027', E, 'im Vergleich zur Word-Datei „PatInfo Preiserhöhung.docx“ vom 13.10.2026'))
    pg2 = b.new_page(); pg2.goto('file://' + hp2); pg2.wait_for_timeout(400)
    prot = os.path.join(OUT, 'protokoll_patinfo.pdf')
    pg2.pdf(path=prot, format='A4', print_background=True, prefer_css_page_size=True, display_header_footer=True, header_template='<span></span>',
            footer_template='<div style="width:100%;font-family:Arial;font-size:8.5px;color:#6a5d51;padding:0 18mm 0 20mm;display:flex;justify-content:space-between"><span>Änderungsprotokoll Patienteninformation</span><span>Seite <span class="pageNumber"></span> von <span class="totalPages"></span></span></div>')
    doc = pymupdf.open(clean); W = doc[0].rect.width; missing = []
    page = doc[0]
    for c in E:
        cid, pno, anchor, kind = c[:4]
        hits = page.search_for(anchor, quads=True)
        if not hits: missing.append(cid); continue
        q = hits[1] if (cid == 'P1' and len(hits) > 1) else hits[0]
        r = q.rect; hl, lab = R.COL[kind]
        a = page.add_highlight_annot(q); a.set_colors(stroke=hl); a.set_opacity(0.55)
        a.set_info(title=f'Prüfhinweis {cid}', content=R.comment_text(c)); a.update()
        x0 = W - 15 * 2.835 if r.x0 > W / 2 else 3.5 * 2.835
        ft = page.add_freetext_annot(pymupdf.Rect(x0, r.y0 - 1, x0 + 11 * 2.835, r.y0 + 10.5), cid, fontsize=7.5, fontname='hebo', text_color=(1, 1, 1), fill_color=lab, align=1)
        ft.set_info(title=f'Prüfhinweis {cid}', content=cid); ft.update()
    bt = page.add_freetext_annot(pymupdf.Rect(20 * 2.835, 4 * 2.835, W - 18 * 2.835, 9.5 * 2.835),
        'Prüffassung mit Änderungsvermerken – nicht an Patientinnen und Patienten ausgeben. Änderungsprotokoll ab Seite 2.',
        fontsize=7, fontname='helv', text_color=(0.60, 0.23, 0.15), fill_color=(0.98, 0.94, 0.90), align=1); bt.update()
    doc.insert_pdf(pymupdf.open(prot))
    doc.set_metadata({'title': 'Patienteninformation Honorar 2027 – Prüffassung mit Änderungsvermerken', 'author': 'Gunnar Götze', 'subject': content.STAND})
    rev = os.path.join(OUT, f'{T} – Prüffassung mit Änderungsvermerken.pdf')
    doc.save(rev, garbage=3, deflate=True)
    print('review pages', len(doc), 'missing', missing)
    b.close()
