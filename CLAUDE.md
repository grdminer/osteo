# Projekt: Website und Patientendokumente Praxis Gunnar Götze

Neue Website für die Privatpraxis von Gunnar Götze, Heilpraktiker und Physiotherapeut (Osteopathie), Bahnhofstraße 62, 15827 Blankenfelde-Mahlow, OT Dahlewitz. Sie ersetzt die alte Strato-Baukasten-Seite unter www.osteopathie-götze.de. Dazu gehören neu gestaltete Patientendokumente als PDF.

Antworten und alle Inhalte auf Deutsch. Patienten werden mit „Sie“ angesprochen, sachlich und ohne Werbesprache.

## Stand (Oktober 2026)

Die Website läuft als Vorschau auf GitHub Pages (https://grdminer.github.io/osteo/) mit `noindex` und einer Vorschau-Leiste. Geplant ist der Umzug auf ein Strato-Webhosting-Paket mit SFTP; der Strato-Homepage-Baukasten erlaubt keine eigenen HTML-Dateien. Gestrichelte Kästen mit „Offen:“ auf den Seiten markieren Punkte, die Gunnar noch klären muss.

Fakten: Preis 80 Euro pro Behandlung, ab 1. Januar 2027 100 Euro (noch offen: gilt das auch für Physiotherapie?). Eine Behandlung dauert 50 Minuten. Reine Privatpraxis. Termine meist zwischen 10 und 18 Uhr, flexibel. Online-Buchung: https://my.lemniscus.de/ot/24f0e28b-988a-4317-8907-98d3f3a59a79 (war Ende Oktober 2026 noch nicht freigeschaltet). Telefon 0159 01758367, E-Mail osteopathie.goetze@gmail.com. Gunnar ist offenbar Mitglied der hpO (Berufsvereinigung für heilkundlich praktizierte Osteopathie e. V.).

## Aufbau

Statische Website ohne Build-Schritt im Wurzelverzeichnis: `index.html` (Startseite mit Hinweis-Banner zur Honoraranpassung), `aktuelles.html` (Neuigkeiten), die Wissensseiten `osteopathie.html`, `physiotherapie.html`, `heilkunde.html`, `tai-chi-qigong.html` sowie `impressum.html` und `datenschutz.html`. Gemeinsame Gestaltung in `assets/style.css`; Schriften Literata und Karla liegen lokal unter `assets/fonts/` (keine Google Fonts, aus Datenschutzgründen). Bilder in `assets/img/`, Download-PDFs für die Website in `assets/docs/`. Nach Änderungen an `style.css` die Versionsnummer `?v=` in allen HTML-Dateien erhöhen, damit Browser die neue Datei laden.

Patientendokumente unter `dokumente/`: Die Texte stehen in `dokumente/quellen/content.py` (Behandlungsvertrag, Patientenaufnahmebogen) und `build_patinfo.py` (Patienteninformation Honorar 2027), die Änderungsvermerke der Prüffassungen in `changes.py` bzw. in `build_patinfo.py`. Erzeugt werden die PDFs mit:

```
pip install playwright pymupdf
python -m playwright install chromium
cd dokumente/quellen
python build.py          # saubere Fassungen, ausfüllbar (Formularfelder)
python build_review.py   # Prüffassungen mit Kommentaren und Änderungsprotokoll
python build_patinfo.py  # Patienteninformation, sauber und Prüffassung
```

Ergebnisse landen in `dokumente/pdf/`. Prüffassungen sind per `.gitignore` vom öffentlichen Repository ausgeschlossen. Nach Änderungen an der Patienteninformation die saubere Fassung nach `assets/docs/patienteninformation-honorar-2027.pdf` kopieren. `build.py` meldet pro Seite den freien Platz in mm; negative Werte bedeuten, dass Inhalt über den Seitenfuß läuft.

## Gestaltung

Erdige Farben (Reispapier `#ebe3d5`, Umbra `#2c241f`, gebrannte Erde `#87552f`, Olivgrün `#6d6b3f`, Lehm `#cdb896`, Siegelrot `#9a3b27` nur für das GG-Siegel). Leichte asiatische Note: rotes Namenssiegel „GG“, ein Ensō, der beim Laden gemalt wird, danach ein Blütenzweig (Blüten-Hartriegel), der langsam von rechts nach links wächst, und Tuschberge vor dem Kontaktbereich. Alle Grafiken und Symbole sind selbst gezeichnete SVGs; keine fremden Bilder ohne geklärte Rechte verwenden. Die Patientendokumente nutzen dieselben Elemente dezent (Siegel, blasser Ensō, Bergsilhouette im Fuß) und sind druckfreundlich weiß.

## Inhaltliche Grundsätze

Wirkaussagen nur mit belastbaren Quellen (Cochrane, systematische Übersichten, RCTs) und vollständiger Fundstelle; Grenzen der Evidenz offen benennen, nichts beschönigen. Für Heilpraktiker gilt das Heilmittelwerbegesetz (keine irreführenden Wirkungsversprechen, kein garantierter Erfolg, Studien nur mit Verfasser, Jahr und Fundstelle). Die Patientendokumente berücksichtigen das Patientenrechtegesetz (§§ 630a ff. BGB) und das AGB-Recht (§§ 305 ff. BGB). Rechtliche Texte sind Entwürfe und sollen vor dem Einsatz von einer Fachperson für Medizinrecht geprüft werden.

## Offene Punkte

Gunnar muss klären: ob die 100 Euro auch für Physiotherapie gelten; die Technikliste im Aufnahmebogen (Aufklärung) und ob er kraniosakral oder viszeral arbeitet (Osteopathie-Seite); seine Behandlungsschwerpunkte auf der Startseite; ob er selbst Qigong oder Tai Chi anbietet; den Absatz in seinem Namen auf der Heilkunde-Seite und die Dauer seiner Osteopathie-Ausbildung; die zuständige Aufsichtsbehörde im Impressum (Gesundheitsamt Potsdam oder Teltow-Fläming) und ob dort die Privatanschrift stehen muss; ob die hpO-Mitgliedschaft für Kassenzuschüsse genügt; Anbieter und Auftragsverarbeitung bei lemniscus und die Nutzung von Gmail; ob es Mitarbeiter gibt (dann Datenschutzinformation ergänzen); die Auswahl der Warnzeichen im Aufnahmebogen.

## Vor dem Livegang bei Strato

Offene Punkte klären und die Kästen entfernen; Vorschau-Leiste, `noindex` in allen Seiten und die Sperre in `robots.txt` entfernen; Datenschutzerklärung von GitHub auf Strato als Hoster umstellen und Auftragsverarbeitungsvertrag mit Strato abschließen; `.htaccess` mit 301-Weiterleitungen der alten Adressen (/Startseite/, /Die-Praxis/, /Downloads-Anleitungen-Infos/, /Ihr-Weg-zu-uns/, /Impressum-und-Datenschutzerklaerung/) und https-Umleitung anlegen; Dateien per SFTP ins Hauptverzeichnis des Webspace laden, Domain zuweisen, SSL aktivieren; den Baukasten erst kündigen, wenn die neue Seite läuft. Den Banner zur Honoraranpassung im Frühjahr 2027 wieder entfernen.
