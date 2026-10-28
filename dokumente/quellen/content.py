# Inhalte der beiden Patientendokumente (Stand Oktober 2026)
import itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
ENSO = open(os.path.join(HERE, 'enso.txt')).read().split('\n')[0]
MOUNT = open(os.path.join(HERE, 'mount.txt')).read().split('\n')
STAND = 'Stand Oktober 2026'
BOOK = 'my.lemniscus.de/ot/24f0e28b-988a-4317-8907-98d3f3a59a79'

_c = itertools.count()
def f(name, cls='', t='text', h=None):
    st = f' style="height:{h}mm"' if h else ''
    extra = ' multi' if t == 'multi' else ''
    return f'<div class="f{extra} {cls}" data-n="{name}" data-t="{t}"{st}></div>'
def fld(label, name, cls='c3', t='text', h=None, opt=False):
    o = ' <em>freiwillig</em>' if opt else ''
    return f'<div class="fld {cls}"><label>{label}{o}</label>{f(name, t=t, h=h)}</div>'
def box(name):
    return f'<span class="box" data-n="{name}" data-t="check"></span>'
def chk(label, name):
    return f'<div class="chk">{box(name)}<span>{label}</span></div>'
def ph(t):
    return f'<span class="ph">{t}</span>'

def masthead():
    return f'''<svg class="enso" viewBox="40 40 520 520" aria-hidden="true"><path d="{ENSO}"/></svg>
<div class="masthead">
  <div class="brand"><div class="seal">GG</div><div><strong>Gunnar Götze</strong><span>Heilpraktiker und Physiotherapeut</span></div></div>
  <div class="contact"><b>Bahnhofstraße 62</b><br>15827 Blankenfelde-Mahlow, OT Dahlewitz<br>0159 01758367<br>osteopathie.goetze@gmail.com</div>
</div>'''
def runhead(title):
    return f'<div class="runhead"><div class="mini"><i>GG</i>Gunnar Götze</div><div>{title}</div></div>'
def foot(title, n, total):
    return f'''<div class="foot"><div class="meta"><span>{title}, {STAND}</span><span>Seite {n} von {total}</span></div>
<svg viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{MOUNT[0]}"/><path d="{MOUNT[1]}"/></svg></div>'''
def sec(no, title, body):
    return f'<div class="sec"><h2><span class="no">{no}</span>{title}</h2>{body}</div>'

def doc(title, pages):
    total = len(pages)
    out = []
    for i, body in enumerate(pages, 1):
        head = masthead() if i == 1 else runhead(title)
        out.append(f'<section class="page">{head}{body}{foot(title, i, total)}</section>')
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{title} – Gunnar Götze</title>
<link rel="stylesheet" href="doc.css"></head><body>{''.join(out)}</body></html>'''

def sign(prefix, who=('Unterschrift Patientin/Patient bzw. gesetzliche Vertretung',), date=True):
    cols = ' three' if len(who) == 2 else ''
    parts = [fld('Ort, Datum', f'{prefix}_datum', 'x')] if date else []
    parts += [fld(w, f'{prefix}_sig{i}', 'x') for i, w in enumerate(who)]
    return f'<div class="sign{cols}">{"".join(parts)}</div>'

# ---------------------------------------------------------------- Vertrag
V = 'Behandlungsvertrag'
v1 = f'''
<h1>Behandlungsvertrag</h1>
<p class="lead">Dieser Vertrag regelt, was Sie von meiner Behandlung erwarten können und was wir miteinander vereinbaren. Bitte lesen Sie ihn vor dem ersten Termin in Ruhe durch. Fragen beantworte ich Ihnen gern.</p>
<div class="panel" style="margin-top:0">
  <p class="small" style="margin-bottom:3mm">Zwischen Gunnar Götze, Heilpraktiker und Physiotherapeut, Bahnhofstraße 62, 15827 Blankenfelde-Mahlow, OT Dahlewitz (im Folgenden „Praxis“) und</p>
  <div class="grid">
    {fld('Name, Vorname', 'v_name', 'c4')}{fld('Geburtsdatum', 'v_geb', 'c2')}
    {fld('Anschrift', 'v_anschrift', 'c6')}
    {fld('Gesetzliche Vertretung (nur bei Minderjährigen oder Betreuung)', 'v_vertretung', 'c6')}
  </div>
  <p class="small" style="margin:3mm 0 0">(im Folgenden „Sie“) wird folgender Vertrag geschlossen.</p>
</div>
{sec('§ 1', 'Gegenstand der Behandlung', '''
<p>Die Praxis erbringt osteopathische und physiotherapeutische Behandlungen auf Grundlage der Heilpraktikererlaubnis. Geschuldet ist eine sorgfältige Behandlung nach den Regeln des Fachs, nicht ein bestimmter Erfolg. Ein Behandlungserfolg kann nicht versprochen werden.</p>
<p>Osteopathie gehört nicht zu den Leistungen der gesetzlichen Krankenversicherung. Für einige Beschwerden, etwa Rückenschmerzen, gibt es Hinweise auf eine Wirksamkeit; für viele andere ist sie wissenschaftlich nicht ausreichend belegt. Die Behandlung ersetzt keine ärztliche Untersuchung. Ernste Ursachen von Beschwerden sollten ärztlich abgeklärt werden.</p>
<p>Die Praxis kann einzelne Behandlungswünsche ablehnen, insbesondere wenn sie fachlich nicht vertretbar sind.</p>''')}
{sec('§ 2', 'Dauer einer Behandlung', '''
<p>Eine Behandlung dauert 50 Minuten. Sie kann im Einzelfall kürzer oder länger ausfallen; der Preis richtet sich nicht nach der genauen Dauer.</p>''')}
'''

v2 = f'''
{sec('§ 3', 'Kosten', f'''
<div class="note"><p><b>Information über die voraussichtlichen Kosten:</b> Eine Behandlung kostet 80 Euro, ab dem 1. Januar 2027 100 Euro. Die Abrechnung orientiert sich am Gebührenverzeichnis für Heilpraktiker (GebüH) bzw. an den Beihilfesätzen des Bundes.</p></div>
<p>Sie erhalten nach jeder Behandlung eine Rechnung und können bar oder per Überweisung zahlen.</p>
<p>Gesetzliche Krankenkassen übernehmen die Kosten in der Regel nicht. Manche zahlen freiwillig einen Zuschuss, meist nur mit einer ärztlichen Bescheinigung, die vor der Behandlung ausgestellt wurde. Private Krankenversicherungen, Zusatzversicherungen und Beihilfe erstatten je nach Tarif ganz, teilweise oder gar nicht. Bitte klären Sie das vorab mit Ihrer Versicherung. Ihre Zahlungspflicht besteht unabhängig davon, ob und in welcher Höhe Sie eine Erstattung erhalten.</p>''')}
{sec('§ 4', 'Termine und Absagen', f'''
<p>Vereinbarte Termine sind verbindlich, weil die Zeit für Sie reserviert ist. Wenn Sie einen Termin nicht wahrnehmen können, sagen Sie ihn bitte spätestens 24 Stunden vorher ab: telefonisch unter 0159 01758367, per E-Mail an osteopathie.goetze@gmail.com oder über die Online-Terminbuchung.</p>
<p>Bei einer späteren Absage oder wenn Sie nicht erscheinen, kann die Praxis ein Ausfallhonorar von 50 Prozent des Behandlungspreises berechnen. Das gilt nicht, wenn Sie den Ausfall nicht zu vertreten haben oder der Termin anderweitig vergeben werden konnte. Sie können außerdem nachweisen, dass der Praxis kein oder ein wesentlich geringerer Schaden entstanden ist.</p>
<p>Hausbesuche sind nur ausnahmsweise und nach Absprache möglich; einen Anspruch darauf gibt es nicht. Werden Sie bei einem vereinbarten Hausbesuch nicht angetroffen, kann der volle Behandlungspreis zuzüglich einer Anfahrtspauschale von 10 Euro berechnet werden. Auch hier gelten die Ausnahmen und die Nachweismöglichkeit aus dem vorigen Absatz.</p>''')}
{sec('§ 5', 'Ihre Mitwirkung', '''
<p>Bitte informieren Sie mich vor der Behandlung vollständig über bekannte Erkrankungen, Medikamente, eine Schwangerschaft und alles, was die Behandlung beeinflussen könnte. Dafür dient der Patientenaufnahmebogen. Teilen Sie mir Änderungen bitte unaufgefordert mit, ebenso Beschwerden, die während oder nach einer Behandlung auftreten.</p>''')}
{sec('§ 6', 'Aufklärung', '''
<p>Vor der ersten Behandlung bespreche ich mit Ihnen Ablauf, Nutzen, Risiken und Alternativen der geplanten Behandlung. Ergänzend erhalten Sie die schriftliche Aufklärung im Patientenaufnahmebogen. Von allen Unterlagen, die Sie unterschreiben, bekommen Sie eine Kopie. Sie können einzelne Techniken jederzeit ablehnen und Ihre Einwilligung widerrufen.</p>''')}
{sec('§ 7', 'Dokumentation und Akteneinsicht', '''
<p>Die Praxis führt über Ihre Behandlung eine Patientenakte und bewahrt sie zehn Jahre nach Abschluss der Behandlung auf. Sie können jederzeit Einsicht in Ihre vollständige Akte nehmen. Die erste Kopie erhalten Sie kostenlos; für weitere Kopien können die Kosten berechnet werden.</p>''')}
'''

v3 = f'''
{sec('§ 8', 'Vertraulichkeit und Datenschutz', '''
<p>Alle Angaben behandle ich vertraulich. Wie Ihre Daten verarbeitet werden, erläutert die Datenschutzinformation am Ende des Patientenaufnahmebogens. An Dritte, etwa Ihre Ärztin oder Ihren Arzt, gebe ich Informationen nur weiter, wenn Sie eingewilligt haben oder ein Gesetz dazu verpflichtet. Die Einwilligung können Sie unten auf dieser Seite erteilen.</p>''')}
{sec('§ 9', 'Kündigung', '''
<p>Sie können den Vertrag jederzeit ohne Frist kündigen. Die Praxis kann ebenfalls jederzeit kündigen, zu einem für Sie ungünstigen Zeitpunkt aber nur aus wichtigem Grund, etwa wenn für die Behandlung notwendige Angaben fehlen oder bewusst falsch gemacht wurden.</p>''')}
{sec('§ 10', 'Haftung', '''
<p>Die Praxis haftet nach den gesetzlichen Vorschriften. Für mitgebrachte Wertsachen und Kleidung haftet sie nur bei Vorsatz und grober Fahrlässigkeit.</p>''')}
{sec('§ 11', 'Schlussbestimmungen', '''
<p>Änderungen dieses Vertrags und Erklärungen wie eine Kündigung bedürfen der Textform; eine E-Mail genügt. Sollte eine Bestimmung unwirksam sein, bleibt der Vertrag im Übrigen wirksam.</p>''')}

<h3 style="margin-top:7mm">Unterschriften</h3>
<p>Ich habe den Vertrag gelesen und bin mit ihm einverstanden. Ich erhalte eine Kopie.</p>
{sign('v', ('Unterschrift Patientin/Patient bzw. gesetzliche Vertretung', 'Unterschrift Praxis'))}
<div class="panel" style="margin-top:9mm">
  <h3>Einwilligung in den Austausch mit Ihrer Ärztin oder Ihrem Arzt <span class="small" style="font-family:Karla;font-weight:400">(freiwillig)</span></h3>
  <p>Ich entbinde die Praxis gegenüber der unten genannten Ärztin bzw. dem unten genannten Arzt von der Schweigepflicht. Befunde und Informationen zur Behandlung dürfen ausgetauscht werden, soweit das für meine Behandlung sinnvoll ist.</p>
  <div class="grid" style="margin:3mm 0 1mm">{fld('Name und Anschrift der Ärztin oder des Arztes', 'v_arzt', 'c6')}</div>
  <p class="small">Diese Einwilligung ist freiwillig. Ohne sie wird Ihre Behandlung nicht schlechter. Sie können sie jederzeit mit Wirkung für die Zukunft widerrufen, eine E-Mail genügt.</p>
  {sign('v_ein')}
</div>
'''
VERTRAG = doc(V, [v1, v2, v3])

# ---------------------------------------------------------------- Aufnahmebogen
A = 'Patientenaufnahmebogen'
scale = ''.join(f'<div class="n">{box(f"a_schmerz_{i}")}<b>{i}</b></div>' for i in range(11))
a1 = f'''
<h1>Patientenaufnahmebogen</h1>
<p class="lead">Ihre Angaben helfen mir, Ihre Beschwerden zu verstehen und Risiken zu erkennen. Bitte füllen Sie den Bogen möglichst vollständig aus, am Computer oder von Hand. Was Sie nicht sicher wissen, besprechen wir gemeinsam. Felder mit dem Hinweis „freiwillig“ können Sie leer lassen.</p>
{sec('1', 'Persönliche Angaben', f'''
<div class="grid">
  {fld('Name', 'a_name')}{fld('Vorname', 'a_vorname')}
  {fld('Geburtsdatum', 'a_geb', 'c2')}{fld('Telefon', 'a_tel', 'c2')}{fld('E-Mail', 'a_mail', 'c2', opt=True)}
  {fld('Straße und Hausnummer', 'a_str')}{fld('PLZ und Ort', 'a_ort')}
  {fld('Behandelnde Ärztin oder behandelnder Arzt', 'a_arzt', opt=True)}{fld('Wie sind Sie auf die Praxis aufmerksam geworden?', 'a_empf', opt=True)}
</div>
<p class="small" style="margin:3.5mm 0 1mm">Krankenversicherung</p>
<div class="checks" style="grid-template-columns:repeat(4,1fr)">{chk('gesetzlich', 'a_kv_g')}{chk('privat', 'a_kv_p')}{chk('Beihilfe', 'a_kv_b')}{chk('Zusatzversicherung', 'a_kv_z')}</div>''')}
{sec('2', 'Ihre aktuellen Beschwerden', f'''
<div class="grid">
  {fld('Welche Beschwerden oder Schmerzen haben Sie? Bitte nennen Sie alle, nicht nur die, wegen der Sie kommen.', 'a_beschw', 'c6', 'multi', 21)}
  {fld('Seit wann bestehen sie?', 'a_seit', 'c2')}
  <div class="fld c4"><label>Wie stark sind sie im Moment? (0 = keine, 10 = stärkste vorstellbare)</label><div class="scale">{scale}</div></div>
  {fld('Wie fühlen sie sich an, und wann treten sie auf?', 'a_art', 'c6', 'multi', 14)}
  {fld('Was verstärkt oder lindert die Beschwerden?', 'a_faktor', 'c3', 'multi', 14)}
  {fld('Was haben Sie bisher unternommen? (z. B. Arzt, Physiotherapie, Übungen)', 'a_bisher', 'c3', 'multi', 14)}
</div>''')}
'''

warn = [
 ('Schmerzen in der Nacht oder in Ruhe, die sich durch Lagewechsel nicht bessern', 'w1'),
 ('Ungewollter Gewichtsverlust in den letzten Monaten', 'w2'),
 ('Fieber, Schüttelfrost oder ein allgemeines Krankheitsgefühl', 'w3'),
 ('Taubheit, Kribbeln oder Kraftverlust in Armen oder Beinen', 'w4'),
 ('Probleme beim Wasserlassen oder Stuhlgang, Taubheit im Gesäß- oder Genitalbereich', 'w5'),
 ('Plötzlicher Schwindel, Seh- oder Sprachstörungen, neuartige starke Kopf- oder Nackenschmerzen', 'w6'),
 ('Ein Unfall oder Sturz in den letzten Wochen', 'w7'),
]
rows = ''.join(f'<tr><td>{t}</td><td class="o"><span>{box("a_"+n+"_ja")}ja</span></td><td class="o"><span>{box("a_"+n+"_nein")}nein</span></td></tr>' for t, n in warn)
organ = ['Hören, Schmecken, Riechen, Sehen', 'Schilddrüse', 'Herz', 'Lunge', 'Leber und Galle', 'Verdauung (Magen, Darm)', 'Nieren und Blase', 'Urogenitaltrakt']
a2 = f'''
{sec('3', 'Wichtige Warnzeichen', f'''
<p>Bitte kreuzen Sie an, ob eines dieser Zeichen derzeit bei Ihnen auftritt. Wenn ja, sprechen Sie mich bitte vor der Behandlung darauf an. Manchmal ist zuerst eine ärztliche Abklärung nötig.</p>
<table class="yn">{rows}</table>''')}
{sec('4', 'Schwangerschaft', f'''
<div class="checks" style="grid-template-columns:auto auto auto 1fr;align-items:center">{chk('nein', 'a_ss_nein')}{chk('nicht sicher', 'a_ss_unsicher')}{chk('ja, in der Woche', 'a_ss_ja')}<div style="width:22mm">{f('a_ss_woche')}</div></div>''')}
{sec('5', 'Medikamente und Allergien', f'''
<div class="grid">
  {fld('Welche Medikamente nehmen Sie regelmäßig ein?', 'a_med', 'c6', 'multi', 21)}
</div>
<div class="checks two" style="margin-top:2.5mm">{chk('Ich nehme blutverdünnende Medikamente (z. B. Marcumar, ASS, Xarelto, Eliquis).', 'a_blutv')}{chk('Ich nehme dauerhaft Kortison ein.', 'a_kortison')}</div>
<div class="grid">{fld('Bekannte Allergien oder Unverträglichkeiten', 'a_allerg', 'c6')}</div>''')}
{sec('6', 'Beschwerden an Organen', f'''
<p>Bitte kreuzen Sie an, wo Sie Beschwerden haben, auch wenn keine Diagnose vorliegt.</p>
<div class="checks">{''.join(chk(o, f'a_org{i}') for i, o in enumerate(organ))}</div>
<div class="grid">{fld('Bitte näher beschreiben', 'a_org_text', 'c6', 'multi', 14)}</div>''')}
'''

vor = ['Diabetes Typ 1', 'Diabetes Typ 2', 'Bluthochdruck', 'Vorhofflimmern', 'Angina pectoris oder Herzinfarkt', 'Herzschrittmacher oder Implantate',
 'Durchblutungsstörungen', 'Gefäßerkrankung (z. B. Aneurysma)', 'Krampfadern', 'Schlaganfall', 'Erhöhte Blutfettwerte', 'Gicht (erhöhte Harnsäure)',
 'Schilddrüsenerkrankung', 'Lebererkrankung', 'Nierenerkrankung', 'Erkrankung des Verdauungstrakts', 'Verdauungsprobleme', 'Nahrungsmittelunverträglichkeit',
 'Krebserkrankung', 'Osteoporose', 'Rheuma', 'Bandscheibenvorfall', 'Atemwegserkrankung', 'Allergien', 'Medikamentenunverträglichkeit',
 'Epilepsie', 'Neurologische Erkrankung', 'Psychische Erkrankung', 'Infektionskrankheit (z. B. HIV, Hepatitis)']
fam = ['Bluthochdruck', 'Diabetes', 'Fettstoffwechselstörung', 'Herzinfarkt', 'Krebs', 'Schlaganfall']
a3 = f'''
{sec('7', 'Vorerkrankungen', f'''
<div class="checks">{''.join(chk(o, f'a_vor{i}') for i, o in enumerate(vor))}</div>
<div class="grid">{fld('Sonstige Erkrankungen', 'a_vor_sonst', 'c6')}</div>''')}
{sec('8', 'Unfälle und Operationen', f'<div class="grid">{fld("Was und wann?", "a_ops", "c6", "multi", 21)}</div>')}
{sec('9', 'Erkrankungen in der Familie', f'''
<div class="checks">{''.join(chk(o, f'a_fam{i}') for i, o in enumerate(fam))}</div>''')}
{sec('10', 'Was Sie mir noch mitteilen möchten', f'<div class="grid">{fld("", "a_sonst", "c6", "multi", 21)}</div>')}
<p style="margin-top:5mm">Ich habe die Fragen nach bestem Wissen beantwortet.</p>
{sign('a')}
'''

a4 = f'''
<div class="compact"><h1 style="font-size:17pt">Aufklärung und Einwilligung</h1>
<p class="lead" style="margin-bottom:4mm">Vor der ersten Behandlung sprechen wir ausführlich über Ihre Beschwerden und die geplante Behandlung. Diese Seite fasst das Gespräch zusammen, sie ersetzt es nicht.</p>
<div class="cols2">
<div><h3 style="margin-top:0">Was in der Behandlung geschieht</h3>
<p>Je nach Befund setze ich unter anderem folgende Techniken ein {ph('Liste prüfen')}:</p>
<p><b>Mobilisation:</b> Gelenke werden sanft und wiederholt bewegt, um ihre Beweglichkeit zu verbessern.</p>
<p><b>Muskel-Energie-Technik:</b> Sie spannen einen Muskel leicht gegen meinen Widerstand an, danach wird das Gelenk weiter bewegt.</p>
<p><b>Strain-Counterstrain:</b> Ein Körperbereich wird in eine entlastende Position gebracht und dort gehalten, bis die Spannung nachlässt.</p>
<p><b>Weichteiltechniken (Release):</b> Muskeln und Bindegewebe werden mit Druck und Dehnung gelockert.</p>
<p><b>Manipulation:</b> ein kurzer, schneller Impuls mit kleinem Bewegungsausmaß an einem Gelenk, oft mit hörbarem Knacken.</p></div>
<div><h3 style="margin-top:0">Mögliche Nebenwirkungen und Risiken</h3>
<p>Nach einer Behandlung können die Beschwerden vorübergehend zunehmen. Auch Muskelkater-ähnliche Beschwerden oder Müdigkeit sind möglich.</p>
<p>Bei einer vorgeschädigten Bandscheibe oder einem bisher unbemerkten Bandscheibenvorfall können akute Beschwerden auftreten.</p>
<p>Sehr selten kann es bei Manipulationen an der Halswirbelsäule zu einer Verletzung der Halsgefäße (Wirbelarterie oder Halsschlagader) kommen. Dabei können sich Blutgerinnsel bilden, die einen Schlaganfall auslösen. Das Risiko ist bei vorgeschädigten Gefäßen erhöht.</p>
<p>Ein erhöhtes Risiko besteht auch bei blutverdünnenden Medikamenten, Gefäßerkrankungen, Bandscheibenschäden mit Nervenausfällen, Osteoporose und nach Knochenbrüchen. Dann wäge ich besonders sorgfältig ab und verzichte gegebenenfalls auf Manipulationen.</p></div>
<div><h3>Alternativen</h3>
<p>Je nach Beschwerden kommen auch eine ärztliche Behandlung, Physiotherapie auf ärztliche Verordnung, ein eigenes Übungsprogramm oder Abwarten in Frage. Wir besprechen, was in Ihrem Fall sinnvoll ist.</p></div>
<div><h3>Wissenschaftliche Einordnung</h3>
<p>Für Rückenschmerzen gibt es Hinweise auf eine Wirksamkeit osteopathischer Behandlung. Für viele andere Beschwerden ist sie nicht ausreichend belegt. Mehr dazu finden Sie auf meiner Website.</p></div>
</div>
<div class="panel">
  <h3>Ihre Einwilligung</h3>
  <div class="grid" style="margin-bottom:3mm">{fld('Aufklärungsgespräch mit Gunnar Götze am', 'e_gespraech', 'c2')}</div>
  <div class="checks" style="grid-template-columns:1fr;row-gap:2.2mm">
    {chk('Ich wurde mündlich aufgeklärt und hatte Gelegenheit, alle meine Fragen zu stellen.', 'e_1')}
    {chk('Ich willige in die besprochene Behandlung ein. Ich weiß, dass ich meine Einwilligung jederzeit widerrufen und einzelne Techniken ablehnen kann.', 'e_2')}
    {chk('Ich wünsche keine Manipulation mit Impuls an der Halswirbelsäule. <span class="small">(freiwillig)</span>', 'e_3')}
    {chk('Ich habe eine Kopie dieses Bogens erhalten.', 'e_4')}
  </div>
  {sign('e', ('Unterschrift Patientin/Patient bzw. gesetzliche Vertretung', 'Unterschrift Therapeut'))}
</div></div>
'''

a5 = f'''
<h1 style="font-size:17pt">Datenschutzinformation</h1>
<p class="lead">Nach Art. 13 der Datenschutz-Grundverordnung (DSGVO) informiere ich Sie darüber, wie ich mit Ihren Daten umgehe.</p>
<div class="cols2">
<div><h3 style="margin-top:0">Verantwortlich</h3>
<p>Gunnar Götze, Bahnhofstraße 62, 15827 Blankenfelde-Mahlow, Telefon 0159 01758367, osteopathie.goetze@gmail.com</p></div>
<div><h3>Wofür ich Ihre Daten verarbeite</h3>
<p>Für Ihre Behandlung, die vorgeschriebene Dokumentation, die Abrechnung und die Organisation Ihrer Termine. Dazu gehören auch Gesundheitsdaten.</p></div>
<div><h3>Rechtsgrundlagen</h3>
<p>Der Behandlungsvertrag (Art. 6 Abs. 1 lit. b DSGVO), gesetzliche Dokumentations- und Aufbewahrungspflichten (Art. 6 Abs. 1 lit. c DSGVO) und die Gesundheitsversorgung (Art. 9 Abs. 2 lit. h DSGVO). Für den Austausch mit Ihrer Ärztin oder Ihrem Arzt ist Ihre Einwilligung die Grundlage (Art. 6 Abs. 1 lit. a und Art. 9 Abs. 2 lit. a DSGVO).</p></div>
<div><h3>Wer Ihre Daten erhält</h3>
<p>Ich gebe Ihre Daten nur weiter, wenn Sie eingewilligt haben oder ich gesetzlich dazu verpflichtet bin. Rechnungen für eine Erstattung reichen Sie selbst bei Ihrer Versicherung ein.</p>
<p>Für einzelne Aufgaben nutze ich Dienstleister, die Daten in meinem Auftrag verarbeiten: für die Online-Terminbuchung lemniscus {ph('Anbieter und Anschrift ergänzen')}, für E-Mails Gmail von Google {ph('prüfen')}. Bitte senden Sie mir ausführliche Gesundheitsdaten möglichst nicht per E-Mail, da E-Mails in der Regel nicht Ende-zu-Ende-verschlüsselt sind.</p></div>
<div><h3>Wie lange ich Ihre Daten speichere</h3>
<p>Ihre Patientenakte bewahre ich zehn Jahre nach Abschluss der Behandlung auf, weil das Gesetz es verlangt (§ 630f BGB). Rechnungen bewahre ich so lange auf, wie es das Steuerrecht vorschreibt. Danach werden die Daten gelöscht.</p></div>
<div><h3>Ihre Rechte</h3>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung (soweit keine Aufbewahrungspflicht besteht), Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch (Art. 15 bis 21 DSGVO). Eine Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen.</p>
<p>Sie können sich außerdem bei der Aufsichtsbehörde beschweren: Die Landesbeauftragte für den Datenschutz und für das Recht auf Akteneinsicht Brandenburg, Stahnsdorfer Damm 77, 14532 Kleinmachnow.</p></div>
<div><h3>Müssen Sie Angaben machen?</h3>
<p>Die Angaben im Aufnahmebogen sind freiwillig, für eine sichere Behandlung aber notwendig. Ohne sie kann ich Sie unter Umständen nicht behandeln.</p></div>
</div>
'''
AUFNAHME = doc(A, [a1, a2, a3, a4, a5])
