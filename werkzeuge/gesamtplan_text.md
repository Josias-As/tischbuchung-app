@@ kopf
# GESAMTPLAN Tischbuchung: alle Änderungen Schritt für Schritt
**Stand 08.10.2026 · Basis: veröffentlichter Export vom 07.10. (enthält L2) · ersetzt das Einfügen von Paket K v2 und Paket L einzeln: Jede Property steht hier genau einmal in ihrer Endfassung · maschinell erzeugt und geprüft (`werkzeuge/gesamtplan.py`, Anhang B) · Go-Live 14.10.2026, harter Umstieg (GoBright-Vertrag endet)**

Kennzeichnung: **belegt** (im Export nachgesehen) · **gemessen** (Monitor/Test) · **geschlussfolgert** · **UNSICHER** (mit Test).

@@ kurzfassung
## 0. Kurzfassung
- **Was das ist:** ein fertiger Plan zum Abarbeiten, Schritt für Schritt. Jeder Schritt sagt, welches Problem er löst, wie, was genau einzufügen ist (vollständige Formel, deutsche Schreibweise) und wie du testest. Du arbeitest ihn mit einem anderen Chat durch, der Startprompt steht in `START_PROMPT_fuer_Chat.md`.
- **Umfang:** 26 App-Schritte (253 Properties, 7 neue Steuerelemente), dazu Vorbereitung in SharePoint, ein Power-Automate-Flow, die Rechte, 2 Properties in der Handy-App, Test mit Kollegen und Go-Live-Checkliste.
- **Reihenfolge = Wichtigkeit.** Phase 1 (Schritte G1–G7) ist das Fundament gegen Doppelbuchungen, falsche Tage und rohe Fehler. **Ohne Phase 1 nicht live gehen.** Danach Freigabe-Flow und Timer (Phase 2), Tischauswahl (Phase 3), Grundriss-Erweiterungen (Phase 4), Optik (Phase 5), Raumcode ruhig (Phase 6), Barrierefreiheit (Phase 7), Handy-App (Phase 8), Test und Go-Live (Phase 9).
- **Zeitbedarf (Einschätzung):** Phase 0–2 ein Tag, Phase 3–5 ein Tag, Phase 6–9 ein Tag, plus Kollegentest. Das passt in deine 3–4 Tage, wenn nichts Größeres schiefgeht. Wenn es knapp wird: Phase 5 und 7 nach dem Go-Live.
- **Deine Entscheidungen aus dem Interview** sind eingebaut: harter Umstieg, automatische Freigabe nach 30 Min (nur löschen), Start ab 06:00, Serien Mo–Fr, Namen sichtbar, Raumcode bleibt (wird nur ruhiggestellt), Liste „nur eigene Elemente bearbeiten“, Tische sperren nur durch dich, Big Table für alle über den Grundriss.
- **Was ich für dich entschieden habe** (du hattest „wie du es für sinnvoll hältst“ gesagt), steht in Abschnitt 2.
- **Ehrlich:** Nichts davon ist in Studio getestet. Alles ist aus dem Export erzeugt und maschinell geprüft. Paket K v2 und L wurden je zweimal unabhängig geprüft, die Ergänzungen aus dem Interview (06:00, Gesperrt, Storno-Bestätigung, Timer, „Andere Zeit buchen“, Raumcode ruhig, Barrierefreiheit, Handy) noch **nicht**. Die offenen Laufzeitfragen stehen im Abschnitt UNSICHER.

@@ nutzung
## 1. So arbeitest du den Plan ab
1. **Ein Schritt nach dem anderen.** Bei jedem Schritt: Steuerelement in der Strukturansicht suchen (Ort steht dabei), Property im Formelfeld wählen, **ganze Property ersetzen** (alles markieren, einfügen), Enter.
2. **Nach jedem Schritt:** App-Prüfung (oben rechts das Stethoskop-Symbol): neue **Formelfehler** (rot)? Dann stoppen und im Chat melden (Schritt, Property, Fehlertext). Warnungen (gelb) notieren, nicht stoppen.
3. **Testen:** Test unter dem Schritt durchführen, im Testbogen (Abschnitt 13) abhaken.
4. **Speichern** nach jedem Schritt (Strg+S). Veröffentlichen erst am Ende einer Phase.
5. **Rückfall:** Jede Originalformel steht im Anhang A. Ganze Property wieder ersetzen. Neue Properties: leeren bzw. Standard. Neue Steuerelemente: löschen.
6. **Neue Steuerelemente** (G4, G8, G14): Anleitung steht beim Schritt. **Name exakt so** vergeben (Doppelklick auf den Namen in der Strukturansicht), sonst passen die Formeln nicht.
7. **`Items.Value`** (G9) ist kein Formelfeld: rechts im Eigenschaftenbereich „Wert“ auswählen.
8. **Deutsche Schreibweise:** Alle Blöcke sind schon deutsch (`;` trennt, `;;` verkettet). Nichts umschreiben.

@@ entscheidungen
## 2. Entscheidungen, die im Plan stecken
| # | Thema | Entscheidung | Wer |
|---|---|---|---|
| E1 | Verlängern über 22:00 | abgelehnt, Plus-Knopf wird grau | Claude (Regel der Handy-App) |
| E2 | Zwei Tische zur selben Zeit | verhindert | Claude (Handy-Regel V6) |
| E3 | Einchecken | ab 30 Min vor Beginn bis Ende. Auschecken jederzeit | Claude (Handy V2) |
| E4 | Buchen in der Vergangenheit | gesperrt (vor der laufenden halben Stunde) | Claude |
| E5 | Big Table | in der Panel-Liste nicht, im Grundriss für alle buchbar | Josias |
| E6 | 5 Std / 9 Std an anderen Tagen | ab 08:00 | Claude |
| E7 | Mehrfachauswahl, Serien | bleiben | Claude |
| E8 | Frühester Start | 06:00. Der **Vorschlag** an anderen Tagen bleibt 08:00, damit niemand aus Versehen um 06:00 bucht | Josias / Claude |
| E9 | Automatische Freigabe | 30 Min nach Beginn ohne Check-in wird gelöscht, keine Mail | Josias |
| E10 | Storno | mit Rückfrage „Wirklich stornieren?“ (Handy V8) | Claude |
| E11 | Handy-App | am 14.10. mit den Kollegen mit Firmenhandy teilen. Deren GoBright-App fällt auch weg, und am Handy kann man einchecken, was mit der Freigabe wichtig wird | Claude |
| E12 | Raumcode | bleibt im Code, fragt aber beim Start nichts mehr ab (36 Abfragen weniger) | Josias (behalten) / Claude (ruhigstellen) |
| E13 | Tisch-Anzeigen von GoBright | werden am 14.10. abgeschaltet bzw. zeigen nichts mehr (Abschnitt 12) | Josias / Claude |

@@ phase0
## 3. Phase 0: Vorbereitung (zuerst, ohne App-Formeln)
### G0.1 Sicherung
- In Studio: **Datei → Speichern unter → Diesen Computer** (`.msapp`). Name z. B. `Tischbuchung_vor_Gesamtplan_2026-10-08.msapp`.
- Die aktuelle **Versionsnummer** im Versionsverlauf notieren (Rückfall: „Wiederherstellen“).
- **Prüfe, dass seit dem Export vom 07.10. nichts geändert wurde.** Wenn doch, schick mir einen neuen Export. Der Plan ist gegen den 07.10. erzeugt, und ganze Properties würden spätere Änderungen überschreiben.

### G0.2 Bestandsdaten prüfen (kaputte Buchungen finden)
**Problem:** Der veröffentlichte Stand kann Buchungen mit Ende vor Beginn (Start 22:00, F-L1), über 22:00 oder über Mitternacht (Verlängern ohne Grenze) erzeugt haben. Solche Zeilen stören Prüfungen und Anzeigen.
**So findest du sie:** Vorübergehend eine leere **vertikale Galerie** auf `Screen1` einfügen, `Items`:
```
Filter(Tischbuchungen; Endzeit <= Startzeit || Day(Endzeit) <> Day(Startzeit) || Hour(Endzeit) * 60 + Minute(Endzeit) > 22 * 60)
```
Die Delegierungswarnung ist hier egal (~250 Zeilen, Limit 1.000). Die Galerie zeigt die betroffenen Buchungen (Titel-Feld der Galerie auf `ThisItem.Tisch.Value & " " & Text(ThisItem.Startzeit; "dd.mm. hh:mm") & "–" & Text(ThisItem.Endzeit; "dd.mm. hh:mm")` stellen). Diese Zeilen in der SharePoint-Liste korrigieren oder löschen, **danach die Galerie wieder löschen**.

### G0.3 Spalte „Gesperrt“ in der Liste `Tische`
**Warum:** Damit du Tische sperren kannst (Reparatur, Umbau), ohne den Code zu ändern (Plan P4). Mehrere Schritte (G6, G7, G9, G13, G14) lesen diese Spalte. **Sie muss vor G6 existieren.**
1. SharePoint → Liste **Tische** → **+ Spalte hinzufügen → Ja/Nein**. Name genau **`Gesperrt`**, Standardwert **Nein**. Speichern.
2. In Studio: links **Daten** → bei **Tische** auf **…** → **Aktualisieren**. Ohne das kennt die App die Spalte nicht, und die Formeln werden rot.
3. Sperren: In der Liste beim Tisch `Gesperrt = Ja`. Entsperren: `Nein`. Den Big Table **nicht** sperren (alle dürfen ihn über den Grundriss buchen).

### G0.4 Mail an Michael (heute)
Vorschlag zum Kopieren:
> Hallo Michael,
> am 14.10. löst unsere eigene Tischbuchungs-App GoBright ab. Dazu brauche ich bitte kurz deine Hilfe:
> 1. **Datenschutz/Betriebsrat:** Die App zeigt im Grundriss Initialen und im Popup den Namen der Person, die einen Tisch gebucht hat (wie GoBright). Müssen wir das mit dem Datenschutz oder Betriebsrat abstimmen?
> 2. **Mitbesitzer:** Ich möchte dich als Mitbesitzer der App „Tischbuchung“, der SharePoint-Listen `Tischbuchungen` und `Tische` und der Flows eintragen, damit du im Notfall eingreifen kannst. Ist das okay?
> 3. **Lizenzen:** Haben alle Nutzer eine M365-Lizenz mit Power-Apps-Nutzungsrecht? (Die App nutzt nur Standard-Konnektoren.)
> 4. **GoBright-Hardware:** Die Tischanzeigen und das Gateway hängen an der GoBright-Cloud und funktionieren nach Vertragsende vermutlich nicht mehr. Sollen wir sie ausstecken bzw. abbauen?
> Danke! Josias

@@ phase 1
## 4. Phase 1: Fundament (Pflicht vor dem Go-Live)
Diese sieben Schritte schließen alle Wege zu Doppelbuchungen, Buchungen am falschen Tag und rohen Fehlermeldungen. Sie gehören zusammen. **Teste erst nach G7 alles zusammen**, einzelne Kurztests stehen trotzdem bei jedem Schritt.

@@ G1
**Problem:** Die neue Doppelklick-Sperre und die Verlängern-Grenzen brauchen Startwerte.
**Lösung:** Drei Zeilen ganz am **Anfang** von `App.OnStart` (`varSperreBis`, `varVerlGrenze`, `varVerlGrenzeTab`). Die L2-Ladezeile bleibt die letzte Anweisung. Die Sperre funktioniert auch ohne diese Zeilen (sie fängt ein leeres `varSperreBis` ab), aber so sind die Typen eindeutig.
**Test:** App-Prüfung ohne Fehler. In der Strukturansicht bei **App** auf **…** → **OnStart ausführen** (Studio führt OnStart nach dem Einfügen nicht von selbst aus). Vorschau: Der Grundriss lädt wie bisher.

@@ G2
**Problem (belegt):** (1) **Befund B0:** Der Verwalten-Dialog im Buchungen-Tab merkt sich die Buchung in `varSelectedBuchungTab`, seine sechs Dauer-Knöpfe prüfen aber `varSelectedBuchung`, also die zuletzt im Dashboard angeklickte Buchung. Ein Knopf kann grün sein, obwohl hinter **dieser** Buchung jemand gebucht hat → stille Doppelbuchung. (2) Jeder der 9 Dauer-Knöpfe fragt in `DisplayMode` und `Fill` selbst SharePoint ab, zusammen 18 Abfragen, auch bei geschlossenem Dialog (gemessen: ~50 Abfragen pro Schreibvorgang mit den Panel-Knöpfen). (3) Im Tab blieb die zuletzt gewählte Dauer stehen. (4) Verlängern über 22:00 war möglich.
**Lösung:** Beim Klick auf „Verwalten“ wird **einmal** die **Grenze** berechnet: der Beginn der nächsten Buchung am selben Tisch nach meinem Ende, höchstens 22:00 am Buchungstag. Dafür gibt es eine delegierbare Abfrage `First(Sort(Filter(…)))`, die Werte stehen in globalen Variablen. Die Knöpfe vergleichen nur noch `Ende + Dauer > Grenze`. Das ist dieselbe Bedingung wie vorher (logisch umgeformt, zweimal unabhängig geprüft), plus 22:00. Jeder Dialog hat seine eigene Grenze (`varVerlGrenze` Dashboard, `varVerlGrenzeTab` Tab), der Tab liest jetzt seine eigene Buchung. Beim Öffnen wird die Dauer geleert.
**Test:** Dashboard → Verwalten einer heutigen Buchung, die um 20:30 endet: +1 grün, +2 und +3 grau. **B0-Test:** Im Dashboard Buchung A verwalten und schließen. Im Tab Buchung B verwalten, hinter der direkt jemand gebucht hat → +1 ist grau. Tab: −1/−2/−3 je nach Länge grau.

@@ G3
**Problem (belegt):** Verlängern prüfte die Belegung nur beim Einfärben, nicht beim Speichern. Zwischen Öffnen und Klick konnte jemand buchen. Doppelklick verlängerte doppelt (in der Handy-App gemessen: aus +1 wurden +2). Fehler wurden verschluckt, Dauer `0` nach Stockwerkwechsel schrieb „+0“.
**Lösung:** Erprobtes Muster aus der Handy-App: **Zweifach-Sperre** (`varIsLoading` + 2 Sekunden `varSperreBis`) → Buchung **frisch** laden → Prüfungen mit eigener Meldung (keine Dauer, gelöscht, wäre leer, über 22:00, inzwischen belegt) → `Patch` in `IfError` → **Nachlese**: Ist das neue Ende wirklich angekommen? → ehrliche Meldung → Liste und Grundriss neu laden. Der Knopf ist erst bedienbar, wenn eine Dauer gewählt ist. Nach „inzwischen belegt“ werden die Plus-Knöpfe grau.
**Test:** +1 Std → „Buchung geändert, neues Ende hh:mm Uhr.“. **Doppelklick** → nur einmal verlängert. Zwei Browser-Tabs: In Tab 2 direkt dahinter buchen, in Tab 1 verlängern → „inzwischen belegt“. Im Tab −1 Std → verkürzt.

@@ G4
**Problem (belegt):** Stornieren im Dashboard löschte den Stand vom Öffnen des Dialogs (`Remove(…; varSelectedBuchung)`) ohne Fehlerbehandlung. War die Buchung inzwischen weg, kam die rohe englische Meldung **„Item Not Found“** (euer gemeldeter Fehler vom 30.09.). Es gab keine Rückfrage, ein Fehlklick löschte sofort, und Doppelklick war nicht gesperrt.
**Lösung:** (1) Die drei Storno-Knöpfe (Dashboard, Tab, Mehrfach) **fragen nur noch**: Sie merken sich, woher die Frage kommt (`varStornoQuelle`), und öffnen den neuen Dialog `conStornoFrage`. (2) „Ja, stornieren“ führt je nach Herkunft die sichere Storno-Formel aus: Sperre → frisch laden → `Remove` in `IfError` → Nachlese (ist sie wirklich weg?) → Meldung → neu laden. Für das Mehrfach-Stornieren bleibt deine bewährte Formel, nur mit Sperre.
**Neues Steuerelement anlegen (4 Stück), dann alle Properties unten setzen:**
1. In der Strukturansicht `Screen1` wählen → **Einfügen → Layout → Container** → umbenennen in **`conStornoFrage`**. Er muss direkt unter `Screen1` liegen, nicht in einem anderen Container.
2. `conStornoFrage` wählen → **Einfügen → Textbeschriftung** → **`lblStornoFrage`**.
3. `conStornoFrage` wählen → **Einfügen → Schaltfläche** (klassisch) → **`btnStornoNein`**, noch einmal → **`btnStornoJa`**.
4. Liegt `conStornoFrage` in der Strukturansicht **über** `conLadeOverlay`, ist das in Ordnung (der Dialog schließt sich vor dem Laden).
**Test:** Dashboard → Verwalten → Stornieren → Rückfrage → „Nein“ → nichts passiert. Noch einmal → „Ja, stornieren“ → „Buchung storniert.“. Zwei Tabs: In Tab 2 stornieren, in Tab 1 stornieren → „Diese Buchung gibt es nicht mehr…“ (kein „Item Not Found“). Tab „Buchungen“ und Mehrfachauswahl genauso. Die Rückfrage nennt bei der Mehrfachauswahl die Anzahl.

@@ G5
**Problem (belegt):** Einchecken ging für jeden Tag und zu jeder Zeit (z. B. übermorgen), ohne Fehlerbehandlung. Mit der automatischen Freigabe ist Check-in jetzt wichtig und muss zuverlässig sein.
**Lösung:** Sperre → frisch laden → **Fenster ab 30 Min vor Beginn bis Ende** (wie in der Handy-App) → `Patch` in `IfError` → Nachlese → Meldung „Eingecheckt.“/„Ausgecheckt.“. Auschecken bleibt jederzeit möglich.
**Test:** Buchung, die in einer Stunde beginnt → Einchecken → Meldung „erst ab 30 Minuten vor Beginn“. Laufende Buchung → „Eingecheckt.“, Kachel rot.

@@ G6
**Problem (belegt):** Die beiden Speichern-Knöpfe (Buchungsdialog aus dem Grundriss und Panel „Tisch buchen“) waren verschieden gebaut. Der Dialog nutzt den Sammel-Patch, das Panel eine alte Schleife. Keiner prüfte, ob die Person zur selben Zeit schon einen Tisch hat. Beide erlaubten Buchungen in der Vergangenheit. Die Kollisionsabfrage lud **alle** Buchungen des Tisches (Datenzeilenlimit). Meldungen zählten lokal statt nachzulesen, und „auf 2 Wochen begrenzt“ verdrängte die Kollisionsmeldung. Nach einem Fehler schloss der Dialog und die Eingaben waren weg. Doppelklick buchte doppelt.
**Lösung:** **Ein** Ablauf für beide Knöpfe:
1. Sperre setzen.
2. Werte zum Klickzeitpunkt in Variablen übernehmen.
3. Termine berechnen (Serie mit Kappung auf 14 Tage, Wochentage Mo–Fr).
4. Prüfungen mit je eigener Meldung: Tisch gewählt? Ende nach Beginn? Wochentag gewählt? Bis-Datum vor dem Start? Tisch **gesperrt** (neu)? Vergangenheit?
5. **Eine** delegierbare Abfrage „Tisch belegt im Zeitraum“ und **eine** „ich habe schon einen Tisch“.
6. Je Termin entscheiden: frei, Tisch belegt oder „ich belegt“.
7. **Sammel-Patch** der freien Termine mit gemeinsamer **`SerienID`** (die Spalte gibt es, sie war nie befüllt).
8. `Refresh` und **Nachlese:** Wie viele sind wirklich angekommen? Hat jemand in derselben Sekunde mit kleinerer ID gebucht?
9. **Eine** Meldung mit allem. Bei Erfolg kommt dazu der Hinweis **„Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben.“**
10. Nur wenn etwas gebucht wurde: Dialog schließen und Eingaben leeren.

**Test:** Einzelbuchung → „Gebucht: OG Desk 5, 09.10., 09:00 bis 10:00 Uhr. Bitte bis 30 Minuten …“. In SharePoint hat die neue Zeile eine `SerienID`. Serie Mo–Fr über 2 Wochen mit einem belegten Tag → „9 von 10 Terminen gebucht … 1× war der Tisch schon belegt.“. Zur selben Zeit schon anderswo gebucht → „Du hast in dieser Zeit schon einen Tisch gebucht.“. Gesperrter Tisch → Meldung. Datum gestern → „Vergangenheit“. **Doppelklick** → eine Buchung.

@@ G7
**Problem (belegt):**
1. Datum, Start, Ende und „Wiederholen bis“ im Buchungsdialog blieben vom letzten Öffnen stehen. Wer im Dialog „morgen“ wählte und abbrach, sah beim nächsten Tisch wieder „morgen“, obwohl der Grundriss heute zeigt.
2. Die Startliste rechnete mit `Now()`. Das wird in solchen Formeln nicht von selbst neu berechnet, deshalb wurde die Startzeit nach Stunden alt.
3. Die Startliste bot **22:00** an. Dann war die Endliste leer, und die Buchung wurde mit **Ende 00:00 vor dem Beginn** gespeichert.
4. Der früheste Start war 08:00 (an anderen Tagen).
5. Gesperrte Tische ließen sich im Grundriss öffnen.

**Lösung:**
- Beim Öffnen (Kachel bzw. „Tisch buchen“) wird der Zeitpunkt in `varDialogJetzt`/`varPanelJetzt` gemerkt, und alle Eingaben werden mit `Reset` zurückgesetzt. Die Startliste und der Startvorschlag rechnen mit diesem Zeitpunkt statt mit `Now()`.
- Die Startliste endet um **21:30** (wie in der Handy-App) und beginnt um **06:00**. Heute beginnt sie bei der nächsten halben Stunde, aber nicht vor 06:00. Der **Vorschlag** an anderen Tagen bleibt 08:00.
- Eine gesperrte Kachel meldet „Dieser Tisch ist zurzeit gesperrt.“

**Test:**
1. Grundriss → freie Kachel → im Dialog „morgen 14:00“ einstellen → Abbrechen. Andere Kachel → heute, nächste halbe Stunde.
2. Dialog um 10:05 öffnen (Start 10:30), schließen, nach 11:00 erneut öffnen → Start 11:30.
3. Datum morgen → Liste ab 06:00, vorgeschlagen 08:00, letzte Startzeit 21:30.
4. Panel „Tisch buchen“ genauso.
5. Einen Tisch in SharePoint sperren → Kachel antippen → Meldung.

@@ phase 2
## 5. Phase 2: Automatische Freigabe, Aktualisieren, Rechte
@@ GF
### G-F Flow „Tischbuchung – Freigabe ohne Check-in“ (Power Automate)
**Problem:** Einchecken hatte bisher keine Folge. Nicht genutzte Tische blieben belegt. GoBright gab sie frei, und so hast du es entschieden (30 Min, nur löschen).
**Lösung:** Ein geplanter Flow unter deinem Konto, alle 5 Minuten:
1. make.powerautomate.com → **Erstellen → Geplanter Cloud-Flow**. Name **`Tischbuchung – Freigabe ohne Check-in`**. Wiederholen alle **5 Minuten**.
2. **Neuer Schritt → SharePoint → Elemente abrufen.** Website: die Site `IMSKonzept`, Liste: **Tischbuchungen**.
   - **Filterabfrage** (Spaltennamen sind die **internen** Namen, `Checkedin` mit kleinem i, belegt):
   ```
   Checkedin eq 0 and Startzeit le '@{formatDateTime(addMinutes(utcNow(), -30), 'yyyy-MM-ddTHH:mm:ssZ')}' and Endzeit gt '@{formatDateTime(utcNow(), 'yyyy-MM-ddTHH:mm:ssZ')}'
   ```
   - Die Ausdrücke `@{…}` über **Ausdruck** einfügen oder genau so in das Feld tippen. Die Zeiten sind UTC, SharePoint speichert UTC: Das passt.
   - Höchstanzahl: **100**.
3. **Neuer Schritt → Auf alle anwenden** (Ausgabe `value` von „Elemente abrufen“) → darin **SharePoint → Element löschen**: Site und Liste wie oben, ID = **ID** aus „Elemente abrufen“.
4. Speichern und **Testen → Manuell**.

**Was er tut:** Er löscht nur Buchungen, die **gerade laufen** (Ende in der Zukunft), seit mindestens 30 Minuten begonnen haben und **nicht eingecheckt** sind. Vergangene Buchungen fasst er nicht an, das macht weiter dein Aufräum-Flow.

**Test:**
1. Buchung mit Start vor 40 Minuten und Ende in 2 Stunden anlegen, **nicht** einchecken → Flow manuell starten → die Buchung ist weg.
2. Dasselbe **mit** Check-in → bleibt.
3. Buchung, die vor 10 Minuten begann → bleibt.

**UNSICHER:** ob `Checkedin eq 0` für Ja/Nein-Spalten im Flow passt. Falls der Flow nichts findet, `Checkedin eq false` versuchen und melden. Die Spalten `Startzeit`/`Endzeit` müssen die internen Namen sein. Prüfen in den Listeneinstellungen: Spalte anklicken, am Ende der Adresse steht `Field=…`.
**Ablauf für Nutzer:** Ab dem Go-Live **innerhalb von 30 Minuten nach Beginn einchecken** (Dashboard „Einchecken“ oder Handy-App). Das muss in die Kurzanleitung und die Go-Live-Mail.
**Aufwand:** etwa 20 Min. **Rückfall:** Flow ausschalten.

@@ G8
**Problem (belegt):** Die App hatte keinen Timer. Bei offener App blieb der Grundriss veraltet. Mit der automatischen Freigabe verschwinden jetzt laufend Buchungen, die App zeigt sie aber weiter als belegt. Über Mitternacht blieb das Ansichtsdatum auf gestern.
**Lösung:** Ein unsichtbarer Timer `tmrAktualisieren`, alle 5 Minuten. Er lädt Liste und Grundriss neu und wechselt nach Mitternacht auf heute. **Er tut nichts, solange ein Dialog oder das Panel offen ist oder gerade gespeichert wird**, damit Eingaben nicht verspringen. Er zeigt keine Warnmeldung (alle 5 Minuten eine gelbe Meldung bei kurzem Netzausfall wäre lästig). Kosten: pro offener App etwa 25 Abfragen alle 5 Minuten, weit unter dem SharePoint-Limit (geschlussfolgert).
**Neues Steuerelement anlegen:** `Screen1` wählen → **Einfügen → Eingabe → Timer** → umbenennen in **`tmrAktualisieren`** → Properties setzen.
**Test:** App offen lassen. In einem zweiten Tab eine Buchung anlegen. Nach spätestens 5 Minuten erscheint sie im Grundriss. Mit offenem Dialog passiert nichts.

@@ GR
### G-R Rechte: „nur eigene Elemente bearbeiten“
**Problem:** Damit die App schreiben kann, dürfen alle Nutzer die Liste bearbeiten, also auch im Browser direkt **fremde** Buchungen ändern oder löschen, an allen Regeln vorbei.
**Lösung:** SharePoint → Liste **Tischbuchungen** → Zahnrad → **Listeneinstellungen** → **Erweiterte Einstellungen** → **Elementbasierte Berechtigungen**:
- Lesezugriff: **Alle Elemente lesen**.
- Erstellen und Bearbeiten: **Nur eigene Elemente erstellen und bearbeiten**.
- Speichern.

„Eigene“ heißt **„Erstellt von“**. Das passt, weil die App unter dem Konto des Nutzers schreibt. Du als Listenbesitzer (und Michael als Mitbesitzer) dürft weiterhin alles. Deshalb laufen deine beiden Flows weiter.
**Test (wichtig):**
1. Ein Kollege ohne Besitzerrechte storniert in der App seine Buchung → geht.
2. Derselbe Kollege öffnet die Liste im Browser und versucht, **deine** Buchung zu bearbeiten → nicht erlaubt.
3. Freigabe-Flow und Aufräum-Flow einmal manuell laufen lassen → löschen weiter.

**Wann:** nach dem Freigabe-Flow, vor dem Kollegentest.

@@ phase 3
## 6. Phase 3: Tischauswahl und Panel

@@ G9
**Problem (belegt):** Die Tischauswahl im Panel zeigte alle 34 Tische unsortiert, auch belegte und den Big Table. Ob ein Tisch frei ist, erfuhr man erst über graue Knöpfe oder beim Speichern. Das wäre wohl die häufigste Beschwerde gewesen. Beim erneuten Öffnen blieb der zuletzt gewählte Tisch stehen.
**Lösung:**
- Die Liste rechnet mit denselben Terminen wie Speichern. Sie holt **eine** Abfrage „Buchungen an den betroffenen Tagen“, die Grenzen stehen direkt als Steuerelement-Ausdrücke im Filter (laut Messung in der Handy-App die delegierbare Form).
- Danach zeigt sie nur Tische, die an mindestens einem Termin frei sind, ohne Big Table und ohne gesperrte Tische.
- Sortierung: ganz freie zuerst, dann das Stockwerk aus dem Grundriss, dann nach Nummer. Bei Serien steht dabei „(an 2 von 10 Tagen belegt)“.
- Kein Tisch ist vorausgewählt. Speichern ist ohne Tisch grau (G6). Bei geschlossenem Panel fragt die Liste nichts ab.

**Hinweis:** `Items.Value` → rechts „Wert“ auf **Anzeige** stellen.
**Test:**
1. Panel öffnen: kein Tisch gewählt, Speichern grau.
2. Morgen 09:00–10:00: belegte Tische und der Big Table fehlen, das Stockwerk des Grundrisses steht zuerst, `OG Desk 2` vor `OG Desk 10`.
3. Wiederholen Mo–Fr: Tische mit „(an x von y Tagen belegt)“ stehen hinten.
4. **Zeit ändern, nachdem ein Tisch gewählt war → notieren, ob die Auswahl bleibt oder leer wird** (UNSICHER U-C1, beides ist sicher, weil Speichern den gewählten Tisch prüft und nennt).
5. App-Prüfung: Steht eine Warnung an `Startzeit`/`Endzeit` in `ddTischePanel.Items`? → melden (U-V3).

@@ G10
**Problem (belegt):** „5 Std“/„9 Std“ rechneten an anderen Tagen ab der aktuellen Uhrzeit (sinnlos) und waren ohne gewählten Tisch gesperrt. Mit „erst Zeit, dann Tisch“ ist das falsch herum. Bei geschlossenem Panel fragten sie trotzdem ab. `CountRows(Filter(…))` erzeugte Delegierungswarnungen.
**Lösung:** Heute ab der nächsten halben Stunde (nicht vor 06:00), an anderen Tagen ab 08:00. Ohne Tisch bedienbar, mit Tisch nur, wenn er frei ist (`LookUp(…).ID`, delegierbar). Bei geschlossenem Panel keine Abfrage. Farbe und Bedienbarkeit rechnen mit dem Öffnungszeitpunkt.
**Test:** Morgen → „5 Std“ → 08:00–13:00. Heute nach 17:00 → „5 Std“ grau. Tisch gewählt, der in den nächsten 5 Std belegt ist → grau.

@@ G11
**Problem (belegt):** Text und Farbe des Hinweises „*Zu weit gewählt“ im Panel rechneten mit dem Datum des **Buchungsdialogs** (`dpDatum`) statt des Panels.
**Lösung:** beide auf `dpDatumTischePanel`.
**Test:** Panel → Wiederholen → Bis-Datum 3 Wochen später → roter Hinweis.

@@ G12
**Problem (belegt):** (1) Ein Stockwerkwechsel setzte die Dauer auf `0` statt leer (BD-12). (2) Die vier Aktualisieren-Stellen meldeten „Aktualisiert.“ auch dann, wenn das Laden scheiterte, und überdeckten die Warnung (BD-10). (3) Im Panel stand „schließen“ doppelt im Code (BD-25).
**Lösung:** leer statt `0`. „Aktualisiert.“ nur bei Erfolg. Doppelte Zeile weg.
**Test:** Aktualisieren → „Aktualisiert.“. WLAN aus → nur die gelbe Warnung.

@@ phase 4
## 7. Phase 4: Grundriss und Dashboard

@@ G13
**Problem:** Gesperrte Tische (G0.3) sahen im Grundriss aus wie freie.
**Lösung:** Gesperrte Kachel grau `#A6A6A6`, Kreis weiß. Das Antippen meldet „gesperrt“ (G7).
**Test:** Tisch in SharePoint sperren → in Studio Daten **Tische** aktualisieren bzw. App neu starten → Kachel grau.

@@ G14
**Problem (belegt):** Ist ein Tisch zu **irgendeiner** Zeit des Tages belegt (bei anderen Tagen) oder gerade belegt (heute), öffnet die Kachel nur das Details-Popup. Die freien Stunden des Tisches waren über den Grundriss nicht buchbar. Und im Buchungsdialog sah man nicht, wann der Tisch belegt ist.
**Lösung:**
- Ins Details-Popup kommt ein Knopf **„Andere Zeit buchen“**. Er öffnet den normalen Buchungsdialog für diesen Tisch, mit denselben frischen Eingaben wie G7.
- Im Buchungsdialog steht neu **„Belegt: 08:00–10:00, 14:00–17:00“** bzw. „An diesem Tag noch frei.“, aus den schon geladenen Grundriss-Daten (keine neue Abfrage). Die Zeile verschwindet, wenn im Dialog ein anderes Datum gewählt wird.
- Das Popup wird 46 px höher. Speichern prüft wie immer am Server (G6).

**Neue Steuerelemente anlegen:**
1. `conDetailsPopup` wählen → **Einfügen → Schaltfläche** (klassisch) → **`btnAndereZeit`**.
2. `conBuchungDialog` wählen → **Einfügen → Textbeschriftung** → **`lblBelegtHeute`**.

**Test:** Tisch heute 08:00–10:00 buchen (oder einen belegten wählen) → Kachel → Popup → „Andere Zeit buchen“ → Dialog zeigt „Belegt: 08:00–10:00“ → 13:00–17:00 buchen → klappt.

@@ G15
**Problem (belegt):** Das Popup zeigte immer „Besetzt“ in Rot, auch wenn die Kachel orange ist (gebucht, nicht eingecheckt).
**Lösung:** „Eingecheckt“ rot oder „Gebucht“ orange, wie die Kachel.
**Test:** Orange Kachel → „Gebucht“. Rote Kachel → „Eingecheckt“.

@@ G16
**Problem (belegt/geschlussfolgert):** „Meine Tischbuchungen“ im Dashboard war nicht nach Uhrzeit sortiert. Der Check-in-Dialog berechnet seine Position aus der Reihenfolge.
**Lösung:** Nach Startzeit sortieren. Die Position des Check-in-Dialogs rechnet mit derselben Reihenfolge.
**Test:** Erst eine Buchung für 14:00, dann eine für 08:00 anlegen → 08:00 steht oben. Einchecken bei der unteren → Dialog auf Höhe der richtigen Zeile.

@@ phase 5
## 8. Phase 5: Einheitliche Optik
Die App wirkte wie aus zwei Apps zusammengesetzt (belegt): Der Buchungsdialog nutzt das Standard-Graublau von Power Apps, das Panel das Markenblau. Speichern war mal grün, mal blau. Stornieren sah aus wie Speichern. Gedrückte Knöpfe waren unlesbar. Der aktive Tab war unsichtbar. Deutsch und Englisch waren gemischt. Diese Schritte ändern **nur Aussehen und Texte**, kein Verhalten.

@@ G17
**Problem (belegt):** Bei 7 Knöpfen ist die Schrift im gedrückten Zustand unsichtbar (schwarz auf schwarz bzw. grün auf grün).
**Lösung:** Gedrückt dunkelgrau mit weißer Schrift.
**Test:** Knöpfe gedrückt halten: Die Schrift bleibt lesbar.

@@ G18
**Problem (belegt):** Beide Tabs haben immer dieselbe Farbe.
**Lösung:** Aktiver Tab dunkelblau, inaktiver hellblau (35 %, Kontrast ok).
**Test:** Tabs wechseln.

@@ G19
**Problem (belegt):** Die Profilfarbe wurde bei jedem Start zufällig gewählt.
**Lösung:** Die Farbe ergibt sich aus der E-Mail-Adresse und ist damit immer gleich. `varProfilFarbe` in OnStart bleibt ungenutzt stehen (harmlos).
**Test:** Zweimal starten: gleiche Farbe.

@@ G20
**Problem (belegt):** Im Buchungsdialog sind die Schalter, Pfeile und Kalender graublau, Speichern ist grün. Im Panel ist alles markenblau, die Schalter grün.
**Lösung:** Der Dialog sieht aus wie das Panel: Schalter grün, Pfeile und Kalender blau, Speichern blau, Auswahlmodus blau.
**Test:** Kachel → Dialog sieht aus wie das Panel.

@@ G21
**Problem:** Stornieren (gefährlich) sah aus wie Speichern (blau) und steht im Tab direkt daneben.
**Lösung:** Stornieren rot.
**Test:** Verwalten-Dialoge ansehen.

@@ G22
**Problem (belegt):** Englische und uneinheitliche Texte: „My personal desk“, „Tisch Buchen“, „+1Std“, „-2std“, „Tisch OG Desk 5“, „---“, „-Keine Einträge-“, verschiedene Titelformen.
**Lösung:** Einheitlich deutsch: „Meine Tischbuchungen“, „Tisch buchen“, „+1 Std“, „−1 Std“, Titel „Verwalten: OG Desk 5“ bzw. nur der Tischname, leere Listen „Keine Buchungen“.
**Test:** Texte durchsehen. Werden „+1 Std“ und ähnliche Texte abgeschnitten, bei diesen Knöpfen `Size` um 1 verkleinern (UNSICHER).

@@ G23
**Problem (belegt):** Auswahlbalken, markierte Listenzeilen, Pfeil-Hover und Trennlinien sind graublau statt blau. Beim Hover springt ein blauer Pfeil auf Graublau.
**Lösung:** alles Markenblau. Pfeil beim Hover dunkler blau.
**Test:** Liste öffnen, Zeile markieren, über den Pfeil fahren.

@@ G24
**Problem (belegt):** Fünf unsichtbare Klickflächen dunkeln beim Hover verschieden stark ab (4–20 %).
**Lösung:** einheitlich 10 %.
**Test:** über Kachel, Einchecken, Verwalten-Pfeile und Logo fahren.

@@ phase 6
## 9. Phase 6: Raumcode ruhigstellen (bleibt erhalten)
@@ G25
**Problem (gemessen/belegt):** Der ausgeblendete Raumcode fragt beim App-Start trotzdem ab (36 Abfragen, darunter die langsamsten). Du willst ihn behalten.
**Lösung:** Der Code bleibt vollständig erhalten. Er wird nur hinter eine Bedingung gestellt: Er rechnet erst, wenn das Raum-Panel bzw. die Raumbestätigung offen ist (`varZeigeRaumBuchungForm`/`varZeigeRaumBestätigung`). Die Raum-Galerien sind dann leer, also rechnen auch ihre Knöpfe und Labels nicht.
**Zurückholen:** jeweils die äußere Bedingung entfernen (Original in Anhang A).
**Test:** App starten: unverändert. Optional mit dem Monitor: keine Abfragen mehr auf `Raumbuchungen` und `Räume` beim Start.

@@ phase 7
## 10. Phase 7: Barrierefreiheit
@@ G26
**Problem (belegt):** 37 Steuerelemente ohne Beschriftung für Screenreader (App-Prüfung).
**Lösung:** `AccessibleLabel` mit kurzem deutschem Text. Das ändert nichts Sichtbares.
**Test:** App-Prüfung: Die Einträge „Fehlende Beschriftung“ verschwinden.

@@ phase 8
## 11. Phase 8: Handy-App
@@ GH
**Problem:**
- Die Handy-App startet heute an anderen Tagen um 08:00. Laut deiner Entscheidung soll ab 06:00 gebucht werden können.
- Eine **Auswahl-Vorgabe** fehlte, die Liste nahm einfach den ersten Eintrag. Mit 06:00 als erstem Eintrag würde an anderen Tagen 06:00 vorgeschlagen.

**Lösung:** Startliste ab 06:00 (heute ab der laufenden halben Stunde, nicht vor 06:00). Neue Vorgabe: heute die erste mögliche Zeit, an anderen Tagen **08:00**.
**Wo:** App **„Tischbuchung Handy“** in Studio öffnen (nicht die Desktop-App!). Steuerelement `ddStart`.
**Test:** Handy-Vorschau → morgen → Start 08:00 vorgeschlagen, Liste ab 06:00. Heute vor 06:00 öffnen (oder Datum heute) → erster Eintrag.
**Teilen (E11):** Danach veröffentlichen und **teilen** mit den Kollegen mit Firmenhandy: Datei → Teilen → Namen eingeben, **ohne** Mitbesitzer-Recht. Die App erscheint dann in **Power Apps Mobile**, die die Kollegen aus dem App Store installieren und sich mit dem Firmenkonto anmelden.
**UNSICHER:** Die Handy-App nutzt `Now()` in der Startliste und hat keinen Timer. Bleibt sie stundenlang offen, veraltet die Liste. Abhilfe: Datum kurz wechseln oder die App neu öffnen. Ein dauerhafter Fix (wie G7) gehört in ein eigenes kleines Handy-Paket.

@@ phase 9
## 12. Phase 9: Test, Go-Live, Betrieb
### G-T Test mit 3–5 Kollegen (vor dem 14.10.)
1. **Vorher:** alle Phasen bis mindestens 4 eingefügt, veröffentlicht, Flow an, Rechte gesetzt.
2. **Ablauf (60–90 Min):** Jeder Kollege bucht nach Kurzanleitung:
   - eine Einzelbuchung über den Grundriss,
   - eine Serie Mo–Fr über das Panel,
   - einmal verlängern, einmal stornieren (mit Rückfrage), einmal einchecken.
3. **Gezielt:**
   - Zwei Kollegen buchen gleichzeitig denselben Tisch zur selben Zeit (einer bekommt „belegt“ oder die rote Gleichzeitig-Meldung).
   - Einer bucht und checkt **nicht** ein → nach 30 Minuten weg.
   - Einer versucht, im Browser eine fremde Buchung zu ändern → verboten.
4. **Notieren:** jede Meldung, die verwirrt, und jeder Fehlertext (Foto). Dauer gefühlt ok?
5. **Danach:** Export und Monitor-Trace an mich, ich werte aus.

### G-G Go-Live-Checkliste (13./14.10.)
- [ ] Alle Phasen 1–4 eingefügt, App-Prüfung ohne Formelfehler, veröffentlicht
- [ ] Flow „Freigabe ohne Check-in“ an, Aufräum-Flow an
- [ ] Rechte „nur eigene Elemente“ gesetzt und getestet
- [ ] Bestandsdaten geprüft (G0.2)
- [ ] App mit allen 30 Nutzern geteilt (Datei → Teilen, ggf. über eine Gruppe), Handy-App mit den Firmenhandy-Kollegen
- [ ] Michael ist Mitbesitzer von App, Listen und Flows, Betriebshandbuch übergeben
- [ ] Kurzanleitung (1 Seite) und Go-Live-Mail verschickt. Inhalt: Link zur App, „innerhalb von 30 Minuten nach Beginn einchecken“, Teams-Chat für Fehler
- [ ] GoBright-Tischanzeigen: Umgang geklärt (Abschnitt 12a)
- [ ] `.msapp`-Sicherung des Go-Live-Stands

### G-Z Rückfall (ohne GoBright)
Da GoBright am 14.10. endet, gibt es keinen Weg zurück dorthin. Rückfall heißt: **auf die letzte funktionierende Version der eigenen App**.
1. **Ein Schritt macht Probleme:** Original aus Anhang A einfügen, veröffentlichen.
2. **Ganze Phase:** Studio → **Versionsverlauf** → Version vor der Phase **wiederherstellen** → veröffentlichen.
3. **App komplett kaputt:** gesicherte `.msapp` (G0.1) importieren bzw. Version wiederherstellen.
4. **Flow löscht Falsches:** Flow ausschalten. Gelöschte Buchungen liegen 93 Tage im **Papierkorb** der SharePoint-Site (wiederherstellbar).
5. **Notbetrieb:** Buchungen direkt in der SharePoint-Liste `Tischbuchungen` anlegen (Tisch, Start, Ende, Person). Die App zeigt sie an.

### 12a. GoBright-Tischanzeigen und Gateway
**Recherche (belegt, Herstellerseiten, abgerufen 08.10.):** Das Gateway muss mit der GoBright-Plattform verbunden sein. Die Tischanzeigen („GoBright Connect“) brauchen eine **Lizenz pro Tisch**. Die GoBright-API ist ein Cloud-Dienst der Plattform. Lokal bietet das Gateway nur eine Aktivierungsseite (Port 8080), keine Steuerschnittstelle. Eine Anbindung an deine App ohne GoBright-Vertrag ist damit **nach allem, was öffentlich bekannt ist, nicht möglich**.
**Empfehlung:**
1. Mit dem Vertragsende **Anzeigen und Gateway ausschalten** bzw. ausstecken, damit sie keinen falschen Status zeigen (ein grünes Licht an einem gebuchten Tisch wäre schlimmer als gar keins).
2. Wer es genau wissen will: eine Mail an support@gobright.com mit der Frage, ob Gateway und Anzeigen ohne Plattform-Lizenz ansteuerbar sind.
3. **Ersatz für später:** **QR-Code am Tisch**, der die Handy-App mit diesem Tisch öffnet und einchecken lässt (Power Apps `Param("tisch")`). Das braucht ein kleines Handy-Paket, ist aber günstig und zuverlässig.

Quellen: [GoBright Connect](https://gobright.com/products/desk-booking-system/connect/), [Produktblatt Connect (PDF)](https://gobright.com/wp-content/uploads/2023/09/GoBright-Downloads-GoBright-Connect-Product-Information.pdf), [Gateway konfigurieren](https://support.gobright.com/hc/en-us/articles/360010138740-Configure-a-Gateway-Device), [API-Erweiterung](https://gobright.com/new-features-and-innovation/api-extension-to-extract-data-from-gobright/), [Gateway-Setup (Partner)](https://ascentae.magentrixcloud.com/articles/knowledgebase/GoBright-Gateway-Setup-10-5-2023).

@@ spaeter
## 13. Bewusst nicht im Plan (mit Grund)
| Vorhaben | Warum nicht jetzt | Nächster Schritt |
|---|---|---|
| Outlook-Einladung (P5) | braucht ein Funktionspostfach und Klärung mit Michael, zwei Flows und eine Spalte `KalenderID` | nach Michaels Antwort eigenes Paket |
| Koordinaten aus der Liste (P7) | Positionen sind von dir final bestätigt, ein Umzug in die Liste birgt Verschiebungsrisiko | nach dem Go-Live mit Screenshots |
| Eigene Umgebung/Lösung (P8) | IT-Thema | mit Michael |
| QR-Check-in am Tisch | Handy-Paket | nach dem Go-Live |
| Buchungen-Tab „manchmal leer“ | Ursache unbekannt | beim nächsten Auftreten Monitor-Trace aufnehmen |
| Mehrfach-Verlängern, Alternativtische | eigene Konzepte | bei Bedarf |
| Hover-Richtung vereinheitlichen, Grautöne, Farbtabelle | nur Optik, viele Properties | später in einem Zug |
| Tab-Reihenfolge (19 Hinweise der App-Prüfung) | geringe Wirkung | später |

@@ unsicher
## 14. UNSICHER (mit Test)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U-C1 | Behält die Tischauswahl die Auswahl, wenn sich die Zeit ändert? | Tisch neu wählen (lästig, nicht gefährlich) | G9 Test 4 |
| U-V3 | Wird die Abfrage der Tischliste delegiert? | Bei sehr vielen Buchungen zeigt die Liste einen belegten Tisch als frei, Speichern prüft trotzdem richtig | App-Prüfung nach G9 |
| U-B1 | `SerienID` wird beim Sammel-Patch geschrieben | falsche Meldung „nicht angekommen“ (keine Doppelbuchung) | G6 Test |
| U-R1 | `Reset` direkt nach `Set(varDialogJetzt; Now())` liefert die neue Startzeit | alte Startzeit | G7 Test 2 |
| U-F1 | Flow-Filter `Checkedin eq 0` | Flow findet nichts oder alles | G-F Test |
| U-S1 | Sperre gegen Doppelklick in der Desktop-App (in der Handy-App gemessen) | doppelte Aktion | Doppelklick-Tests G3, G6 |
| U-T1 | Timer mit `Refresh` alle 5 Min stört nicht | Flackern in Listen | G8 Test, Kollegentest |
| U-G1 | Spalte `Gesperrt` ist ohne „Daten aktualisieren“ unbekannt | rote Formeln in G6/G7/G9/G13/G14 | G0.3 Schritt 2 |
| U-H1 | Handy-Vorgabe „08:00“ greift (Default-Text passt zur Liste) | Vorschlag 06:00 | Phase 8 Test |
| U-Z1 | Zeitumstellung 25.10. (Sonntag) | Buchungen am Sonntag selbst eine Stunde verschoben | sehr selten, keine Aktion |

@@ testbogen
## 15. Testbogen
| ☐ | Schritt | Ergebnis | Notiz |
|---|---|---|---|
| ☐ | G0.1–G0.4 Vorbereitung | | |
| ☐ | G1 OnStart | | |
| ☐ | G2 Verwalten (inkl. B0-Test) | | |
| ☐ | G3 Verlängern (inkl. Doppelklick, zwei Tabs) | | |
| ☐ | G4 Stornieren mit Rückfrage (alle drei Wege) | | |
| ☐ | G5 Einchecken (Fenster) | | |
| ☐ | G6 Speichern (Einzel, Serie, Person, gesperrt, Vergangenheit, Doppelklick, SerienID) | | |
| ☐ | G7 Frische Eingaben, 06:00, 21:30, gesperrte Kachel | | |
| ☐ | G-F Flow Freigabe | | |
| ☐ | G8 Timer | | |
| ☐ | G-R Rechte | | |
| ☐ | G9–G12 Panel | | |
| ☐ | G13–G16 Grundriss/Dashboard | | |
| ☐ | G17–G24 Optik | | |
| ☐ | G25 Raumcode ruhig | | |
| ☐ | G26 Barrierefreiheit | | |
| ☐ | Phase 8 Handy-App, geteilt | | |
| ☐ | G-T Kollegentest | | |
| ☐ | App-Prüfung: vorher 134 Einträge, nachher ___ (erwartet deutlich weniger: ~47 Delegations- und 37 Beschriftungs-Hinweise fallen weg) | | |
