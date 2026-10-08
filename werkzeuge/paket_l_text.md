@@ kopf
# Weitere Fehler, Umbaupläne und Stil-Audit (Paket L)
**08.10.2026, nachts · Basis: veröffentlichter Export vom 07.10. · Paket L: 82 Properties, maschinell erzeugt und geprüft (`werkzeuge/paket_l.py`), ändert keine Property, die Paket K v2 ändert · Reihenfolge: erst Paket K v2, dann L · unabhängig geprüft, Befunde eingearbeitet**

Kennzeichnung: **belegt** (Export), **geschlussfolgert**, **UNSICHER**, **Einschätzung**.

## 0. Kurzfassung
- **Unabhängig geprüft** (`pruefung_paket_l.md`): Das Ergebnis waren 2 Fehler, 4 Risiken und 23 Hinweise. Eingearbeitet sind: Tab-Kontrast (L4), Titelbreite (L9: `lblTitel3` ohne Präfix), Outlook-Plan P5 neu, P3 mit Listen-Aktualisierung, P1-Datumsbedingung, P9 „nur eigene Elemente“, UTC-Hinweis bei P2 und die Zahlen im Stil-Audit. Danach wurde alles neu erzeugt und maschinell geprüft. **L10–L13 (25 Properties: Auswahl, Hover, Dialoghintergründe, Zurücksetzen) und die P1-Formeln kamen nach der Prüfung dazu. Sie sind maschinell geprüft, die zweite unabhängige Prüfung steht in `pruefung_paket_l_2.md`.**
- **Elf neue Befunde** (F-L1 bis F-L11), die Paket K v2 nicht abdeckt. Sieben davon behebt Paket L direkt, vier brauchen einen Umbau (P1, P3). **F-L11 (Datum bleibt stehen → Buchung am falschen Tag) wurde erst bei der Selbstprüfung gefunden und ist neben F-L1 der wichtigste.** Der wichtigste: Die Startliste bietet **22:00** an. Wählt man das, ist die Endliste leer, und die Buchung wird mit Ende **00:00 desselben Tages** gespeichert, also mit Ende vor Beginn (L1).
- **Die Oberfläche wirkt aus zwei Apps zusammengesetzt** (belegt). Der Buchungsdialog aus dem Grundriss nutzt das graublaue Standarddesign von Power Apps, das Tische-Panel das Markenblau `#171496`. „Speichern“ ist einmal grün, sonst blau. „Stornieren“ sieht aus wie „Speichern“. Bei sieben Knöpfen verschwindet beim Drücken die Schrift. Man sieht nicht, welcher Tab aktiv ist. Deutsch und Englisch sind gemischt.
- **Paket L** behebt das mit 82 kleinen Properties: nur Farben, Hover/Auswahl, Texte, Sortierung, eine Liste. Kein Schreibvorgang wird geändert. Risiko: niedrig.
- **Zehn größere Umbaupläne** (Abschnitt 3) sind durchdacht, aber nicht als Formel ausgearbeitet, weil sie neue Steuerelemente, Spalten oder Flows brauchen oder deine Entscheidung. Der wichtigste: **Im Grundriss kann man einen Tisch, der zu irgendeiner Zeit des Tages belegt ist, nicht für die freien Stunden buchen.**

## 1. Neue Fehler (nicht in Paket K v2)
| # | Fehler | Beleg | Folge | Lösung |
|---|---|---|---|---|
| F-L1 | Startliste endet bei **22:00**, die Endliste beginnt bei Start + 30 Min und endet 22:00 → Endliste leer → `Time(Value(""); …)` = 00:00 | `ddStart.Items`, `ddStartTischePanel.Items`: `Sequence(… + 1)`; `ddEnde.Items`: `Sequence(RoundDown((22*60 − start)/30))` | **Buchung 22:00–00:00 (Ende vor Beginn)** im veröffentlichten Stand (geschlussfolgert, nicht gemessen). Mit Paket K v2 kommt die Meldung „Ende muss nach Beginn liegen“. Fällt die leere Endliste allerdings auf ihren Standardwert „22:30“ zurück (UNSICHER), nähme K v2 sogar 22:00–22:30 an. Ab 21:31 ist 22:00 heute die **einzige** Startzeit | **L1** |
| F-L2 | Dashboard-Liste „My personal desk“ ist **nicht nach Uhrzeit sortiert** (Reihenfolge = ID = Buchungszeitpunkt) | `galTischbuchungenHeute.Items` ohne Sortierung | Wer erst nachmittags und dann vormittags bucht, sieht 14:00 vor 08:00 | **L2** (der Check-in-Dialog rechnet seine Position über dieselbe Reihenfolge und wird mit angepasst) |
| F-L3 | Gedrückter Knopf: **Schrift unsichtbar** (schwarz auf schwarz, grün auf grün) | `PressedColor = Self.Fill` bzw. `Color.Black` bei `PressedFill` gleicher Farbe: `btnSpeichern`, `btnAbbrechen`, `btnSchließen2/3/4/4_1`, `btnSchließenKlein` | Bei jedem Klick flackert der Knopf leer. Wirkt kaputt | **L3** |
| F-L4 | **Kein aktiver Tab erkennbar**: „Dashboard“ und „Buchungen“ haben immer dieselbe Farbe | `btnTabDashboard.Fill` = `btnTabBuchungen.Fill` = `#171496`, fest | Nutzer wissen nicht, wo sie sind | **L4** |
| F-L5 | **Profilfarbe zufällig bei jedem Start** | `App.OnStart`: `Set(varProfilFarbe; Switch(RandBetween(1; 8); …))` | Das eigene Initialen-Symbol wechselt jedes Mal die Farbe. Wirkt wie ein Fehler | **L5** (über `Circle2.Fill`, damit `App.OnStart` nicht mit Paket K kollidiert. `varProfilFarbe` wird danach nicht mehr gelesen und kann bei L4-Aufräumen weg) |
| F-L6 | Details-Popup zeigt immer **„Besetzt“ in Rot**, auch wenn nicht eingecheckt (Kachel ist dann orange) | `lblStatus.Text = "Besetzt"`, `Color = #EB3951` | Widerspricht der Kachelfarbe | **L6** |
| F-L7 | **App über Mitternacht offen**: `varAnsichtsDatum` bleibt auf gestern | wird nur in `App.OnStart` und `dpAnsichtsDatum.OnChange` gesetzt (belegt) | Wer die App morgens im alten Browser-Tab weiter benutzt, sieht gestern. Paket K verhindert immerhin Buchungen in der Vergangenheit | Plan P3 |
| F-L8 | **Grundriss: freie Restzeit eines belegten Tisches nicht buchbar** | `btnHitArea.OnSelect`: Ist irgendeine Buchung „relevant“, öffnet sich nur das Details-Popup. Heute: aktive Buchung oder Beginn in 30 Min. Anderer Tag: **irgendeine** Buchung an dem Tag | Tisch 08:00–10:00 gebucht → für 13:00–17:00 muss man ins Panel. Wer das nicht weiß, hält den Tisch für den ganzen Tag belegt | Plan P1 |
| F-L11 | **Eingaben bleiben vom letzten Öffnen stehen**: Datum, Start, Ende und Wiederholen-bis im Buchungsdialog (und Zeiten im Panel) werden beim Öffnen nicht zurückgesetzt | `Reset` gibt es im Export nur für Panel-Listen und -Schalter. `dpDatum`, `dpWiederholenBis(_1)` werden nirgends zurückgesetzt; `ddStart`/`ddEnde` nur bei Datumswechsel (belegt). `DefaultDate = varAnsichtsDatum` greift nur, wenn sich `varAnsichtsDatum` ändert (geschlussfolgert, Standardverhalten klassischer Steuerelemente) | **Stille Buchung am falschen Tag**: Wer im Dialog „morgen“ wählt, abbricht und eine andere Kachel anklickt, sieht wieder „morgen“, obwohl der Grundriss heute zeigt. Mit Paket K v2 kommt bei alten Uhrzeiten von heute die Meldung „Vergangenheit“, was ohne L13 verwirrt | **L13** (bei Paket K v2 Pflicht) |
| F-L10 | **Keine automatische Aktualisierung** (kein Timer in der App) | Steuerelement-Typen im Export: kein Timer (belegt) | Grundriss und Listen veralten, solange die App offen ist | Plan P3 |
| F-L9 | Heute ist eine Kachel **grün**, obwohl der Tisch ab 14:00 belegt ist. Der Buchungsdialog zeigt keine Belegung an | Kachelformel prüft nur „jetzt bis +30 Min“ (belegt) | Nutzer wählt 09:00–17:00 und bekommt „Tisch belegt“ ohne Hinweis, wann frei | Plan P1 |

## 2. Paket L (Formeln, nach Paket K v2 einfügen)
Ablauf wie bei Paket K: ganze Property ersetzen, App-Prüfung, kurzer Test. Alle Schritte sind unabhängig voneinander. **Rückfall:** Original aus Anhang. Die Texte (L9) sind Vorschläge. Wenn du andere Wörter willst, ändere nur den Text in Anführungszeichen.

@@ test L1
**Test:** Panel und Buchungsdialog, Datum heute nach 21:30 → keine Startzeit wählbar. Datum morgen → letzte Startzeit 21:30, Ende 22:00 wählbar.

@@ test L2
**Test:** Heute zwei Buchungen in umgekehrter Reihenfolge anlegen (erst 14:00, dann 08:00) → Dashboard zeigt 08:00 oben. „Einchecken“ bei der unteren → Dialog erscheint auf Höhe der richtigen Zeile.

@@ test L3
**Test:** Jeden dieser Knöpfe gedrückt halten: Schrift bleibt lesbar.

@@ test L4
**Test:** Tab wechseln: Der aktive Tab ist dunkelblau, der andere heller, aber gut lesbar. Die Aufhellung ist nach der Prüfung von 55 % auf 35 % gesenkt, damit die weiße Schrift auf dem inaktiven Tab genug Kontrast hat (etwa 5:1 statt 2,8:1).

@@ test L5
**Test:** App zweimal starten: Profilkreis hat dieselbe Farbe.

@@ test L6
**Test:** Grundriss → belegte Kachel (orange) → Popup „Gebucht“ orange. Eingecheckte Kachel (rot) → „Eingecheckt“ rot.

@@ test L7
**Test:** Grundriss → freie Kachel → Buchungsdialog sieht aus wie das Tische-Panel (blaue Pfeile und Kalender, grüne Wochentage, blauer Speichern-Knopf).

@@ test L8
**Test:** Verwalten-Dialoge: Stornieren ist rot, Speichern/Verlängern blau.

@@ test L9
**Test:** Texte durchsehen. Breite der Plus-/Minus-Knöpfe prüfen: „+1 Std“ ist ein Zeichen länger als „+1Std“ (UNSICHER, ob es abgeschnitten wird; falls ja, `Size` um 1 verkleinern).

@@ test L10
**Test:** Buchungen-Tab: Eine Zeile anklicken, der Auswahlbalken ist blau wie im Dashboard. Buchungsdialog, Check-in-Dialog und Details-Popup haben einen blauen Akzentbalken. Eine Auswahlliste öffnen: Die markierte Zeile ist blau. Über den Pfeil fahren: Er wird dunkler blau, nicht graublau.

@@ test L11
**Test:** Mit der Maus über Grundriss-Kachel, Einchecken-Fläche, Verwalten-Pfeil (Dashboard und Tab) und Logo fahren: Alle dunkeln gleich leicht ab.

@@ test L12
**Test:** Buchungen-Tab → Verwalten: Der Dialog ist weiß wie der Verwalten-Dialog im Dashboard. Der kleine Mehrfach-Dialog ebenso.

@@ test L13
**Test:** (1) Grundriss → freie Kachel → im Dialog Datum auf morgen und 14:00 stellen → Abbrechen. Andere freie Kachel → Dialog zeigt wieder das Grundriss-Datum und die nächste halbe Stunde. (2) Panel öffnen, 09:00–10:00 wählen, mit „<“ schließen, wieder öffnen → Zeiten stehen auf dem Standard. (3) Wiederholen-bis auf in 10 Tagen stellen, abbrechen, neu öffnen → Bis-Datum zurückgesetzt.

@@ plaene
## 3. Umbaupläne für größere Punkte (durchdacht, nicht als Formel)
Jeder Plan: Problem → Lösung → was du anlegen musst → Risiko → Aufwand (Einschätzung).

**P1 Grundriss: freie Zeiten belegter Tische buchen (F-L8, F-L9)**
- *Lösung:* Ins Details-Popup kommt ein Knopf **„Andere Zeit buchen“**. Er setzt `varSelectedTisch` auf den Tisch und öffnet den normalen Buchungsdialog (`varZeigeDialog`). Im Buchungsdialog steht eine Zeile **„Heute belegt: 08:00–10:00, 14:00–17:00“** aus `colGrundriss` (keine neue Abfrage). Die Zeile gilt nur, solange das Dialog-Datum dem Grundriss-Datum entspricht; bei einem anderen Datum blendet sie sich aus (`Visible: dpDatum.SelectedDate = varAnsichtsDatum`). Die Speichern-Prüfung aus Paket K v2 bleibt die letzte Instanz.
- *Anlegen:* einen Knopf `btnAndereZeit` im `conDetailsPopup` und ein Label `lblBelegtHeute` im `conBuchungDialog`.
- *Risiko:* niedrig. *Aufwand:* ~1 Std. Die Steuerelemente legst du an (Knopf im Popup, Label im Dialog unter dem Tischnamen).
- *Formeln (aus dem Export erzeugt, Klammern und Rückübersetzung geprüft; die beiden Steuerelemente sind neu):*
  - `btnAndereZeit.Text`: `"Andere Zeit buchen"`
  - `btnAndereZeit.OnSelect` (übernimmt den „frei“-Zweig aus `btnHitArea.OnSelect` in der Fassung nach L13, nur mit `varDetailsTisch` statt `ThisItem`; beide sind Datensätze aus `Tische`, also kein Typkonflikt):
```
Set(varSelectedTisch; varDetailsTisch);;
Reset(dpDatum);;
Reset(ddStart);;
Reset(ddEnde);;
Reset(dpWiederholenBis);;
Set(varZeigeDialog; true);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false)
```
  - `lblBelegtHeute.Text`:
```
With(
  { belegt: SortByColumns(Filter(colGrundriss; TischName = varSelectedTisch.Titel && Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)); "Startzeit"; SortOrder.Ascending) };
  If(IsEmpty(belegt); "An diesem Tag noch frei."; "Belegt: " & Concat(belegt; Text(Startzeit; "hh:mm") & "–" & Text(Endzeit; "hh:mm"); ", "))
)
```
  - `lblBelegtHeute.Visible`: `varZeigeDialog && dpDatum.SelectedDate = varAnsichtsDatum`
  - *Test:* Tisch heute 08:00–10:00 belegen. Grundriss-Kachel → Popup → „Andere Zeit buchen“ → Dialog zeigt „Belegt: 08:00–10:00“. 13:00–17:00 buchen → „Gebucht: …“. Datum im Dialog ändern → die Zeile verschwindet.


**P2 Check-in mit Folge oder ohne Check-in (größter fachlicher Punkt)**
- *Problem:* Einchecken bewirkt nichts. GoBright gibt nicht eingecheckte Tische frei.
- *Entscheidung nötig:* (a) **Automatische Freigabe:** Ein Power-Automate-Flow alle 15 Minuten löscht oder kürzt Buchungen von heute, die 30 Minuten nach Beginn nicht eingecheckt sind (Spalte intern `Checkedin`!). Dazu eine Mail an den Nutzer. Der Standard-Konnektor reicht (geschlussfolgert). **Achtung:** Der Flow sieht Datum/Uhrzeit in **UTC**. Vergleiche mit `utcNow()`, nicht mit Ortszeit. (b) **Check-in abschaffen** und die Knöpfe ausblenden: ehrlicher als eine Funktion ohne Wirkung.
- *Risiko (a):* Leute verlieren ihren Tisch, wenn sie den Check-in vergessen. Das braucht Kommunikation und wahrscheinlich die Zustimmung des Betriebsrats.
- *Aufwand:* (a) ~½ Tag, (b) 10 Min.

**P3 Automatisch aktualisieren und Tageswechsel (F-L7, F-L10)**
- *Problem (belegt):* Die App hat **keinen Timer**. Der Grundriss lädt nur bei einer Aktion neu, und `Now()` in den Kachelformeln wird nur dann neu berechnet. Bleibt die App offen, bleibt eine Kachel orange, obwohl die Buchung längst vorbei ist, und fremde neue Buchungen erscheinen nicht. Über Mitternacht bleibt `varAnsichtsDatum` auf gestern. GoBright aktualisiert live.
- *Lösung:* Josias fügt einen **Timer** `tmrAktualisieren` ein (irgendwo auf `Screen1`, `Visible = false`) mit `Duration = 300000` (5 Min), `Repeat = true`, `AutoStart = true` und `OnTimerEnd`:
```
If(
  !varIsLoading;
  If(
    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today();
    Set(varAnsichtsDatum; Today());;
    Reset(dpAnsichtsDatum)
  );;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; neu)))
)
```
  **Ergänzung nach Prüfung:** Damit auch die Listen im Dashboard und im Tab aktuell werden (sie lesen direkt aus SharePoint), als erste Anweisung im inneren Teil zusätzlich `Refresh(Tischbuchungen);;` einfügen. Das kostet pro Nutzer etwa 25 Abfragen alle 5 Minuten. Das ist vertretbar, aber spürbar mehr. Ohne diese Zeile wird nur der Grundriss aktuell.
  Das ist die L2-Ladezeile, nur ohne Warnmeldung (alle 5 Minuten eine gelbe Meldung bei kurzem Netzausfall wäre lästig), plus der Tageswechsel. Kosten: **eine** delegierte Abfrage pro Nutzer alle 5 Minuten, bei 30 Nutzern 6 Abfragen pro Minute, weit unter dem Limit (geschlussfolgert).
- *Nebenwirkung:* Wer bewusst einen **vergangenen** Tag ansieht, wird nach spätestens 5 Minuten auf heute zurückgesetzt (selten, akzeptabel).
- *Aufwand:* 10 Min. *Risiko:* niedrig. (Formel aus dem Export erzeugt, Klammern und Rückübersetzung geprüft. Der Timer-Name ist neu.)

**P4 Tisch sperren (Admin)**
- *Lösung:* In der Liste `Tische` eine Ja/Nein-Spalte **„Gesperrt“** anlegen. `Gallery1` zeigt gesperrte Tische grau und ohne Klick. Panel-Liste (C1) und Speichern filtern sie heraus. Gesperrt wird direkt in der SharePoint-Liste, nur Admins haben dort Schreibrechte auf `Tische`.
- *Aufwand:* ~1 Std.
- *Hinweis:* Das ist auch die saubere Lösung für den Big Table („gesperrt für Einzelbuchung“) statt der Namensprüfung.

**P5 Buchung im Outlook-Kalender** (nach Prüfung überarbeitet)
- *Problem mit der ersten Fassung (Prüfbefund):* Der SharePoint-Trigger „Element gelöscht“ liefert keine Spaltenwerte. `SerienID` gilt für eine ganze Serie, nicht für einen Termin. Außerdem würde der Aufräum-Flow sonst Kalendereinträge vergangener Buchungen mitlöschen.
- *Lösung:* Ein Flow „Wenn Element erstellt“ schickt mit dem Office-365-Outlook-Konnektor (Standard) eine **Einladung** aus einem Funktionspostfach an die Person (kein Schreibrecht auf fremde Kalender nötig). Die Ereignis-ID kommt in eine neue Spalte **`KalenderID`** der Buchung. Beim Stornieren ruft die App einen zweiten Flow mit dem Trigger „Power Apps (V2)“ auf und übergibt die `KalenderID`. Der Flow sagt die Einladung ab. Der Aufräum-Flow fasst Kalender **nicht** an.
- *Risiko:* mittel. Funktionspostfach und Besitzer der Flows mit Michael klären.
- *Aufwand:* 1–2 Tage.

**P6 Bestätigung vor dem Stornieren (Handy V8)**
- *Lösung:* Ein Container `conStornoFrage` mit „Wirklich stornieren?“, „Ja“ und „Nein“. Die drei Storno-Knöpfe setzen nur `varZeigeStornoFrage`, und „Ja“ führt die Storno-Formel aus Paket K v2 aus (mit einer Variablen, die sagt, welcher Dialog gefragt hat).
- *Aufwand:* 1 Std.

**P7 Grundriss-Koordinaten aus der Liste statt fest im Code**
- *Problem:* 34 Positionen stehen in `App.OnStart` (`colTischPositionen`, `…UG`). Die Spalten `X`/`Y` in `Tische` sind leer bzw. ungenutzt (belegt).
- *Lösung:* Positionen und Ausrichtung in die Liste übertragen und `Gallery1` direkt daraus lesen. Ein neuer Tisch braucht dann keinen Code mehr.
- *Risiko:* mittel, weil die Positionen von dir final bestätigt sind und nicht verrutschen dürfen. Deshalb nur mit einem Vorher/Nachher-Screenshot je Stockwerk.
- *Aufwand:* ½ Tag. **Nach** dem Go-Live.

**P8 Betrieb: Umgebung, Lösung, Vertretung**
- *Lösung:* Michael fragen nach (1) einer eigenen Umgebung (z. B. „Tischbuchung Prod“) und einer Lösung (Solution), damit die App nicht in „Personal Productivity“ an deinem Konto hängt, (2) einem **Mitbesitzer** der App und der Listen und (3) einer Test-Kopie der Listen.
- Zusätzlich die zwei Klone „App“ und „App – Kopie“ löschen oder eindeutig umbenennen.
- *Aufwand:* je nach IT 1–3 Tage, **wichtigster Punkt für die Zeit nach dir**.

**P9 Berechtigungen der Liste**
- *Lösung:* Prüfen, wer auf `Tischbuchungen` Schreibrechte hat. Für Power Apps sind „Bearbeiten“-Rechte nötig. Strenger geht es nur mit Flows unter einem Dienstkonto (Premium für den HTTP-Trigger aus der App? UNSICHER) oder Dataverse (Premium).
- *Einfachste Verschärfung (ohne Premium, Prüfbefund):* In den Listeneinstellungen → Erweiterte Einstellungen → **Elementbasierte Berechtigungen: „Bearbeiten: nur eigene Elemente“**. Die App bearbeitet ohnehin nur eigene Buchungen. Dann kann niemand fremde Buchungen ändern oder löschen, auch nicht am Browser vorbei. Achtung: „eigene“ heißt **„Erstellt von“**, nicht die Spalte `Person`. Das passt, weil die App unter dem Konto des Nutzers schreibt. Vorher testen, dass der Aufräum-Flow (läuft mit Besitzerrechten) weiter löscht. Ein Flow mit dem Trigger „Power Apps (V2)“ ist laut Prüfung kein Premium (geschlussfolgert).
- *Empfehlung:* Für den Start akzeptieren, aber **bewusst entscheiden und dokumentieren**. Versionsverlauf der Liste einschalten, damit Manipulationen nachvollziehbar sind.

**P10 Barrierefreiheit**
- *Problem:* 64 der 134 Einträge der App-Prüfung (belegt): 37 fehlende Beschriftungen (`AccessibleLabel`), 19 fehlende Tab-Reihenfolge, 7 unsichtbare Fokusrahmen, 1 Bildschirmname.
- *Lösung:* `AccessibleLabel` für alle Knöpfe ohne Text (Kachel-Klickfläche, Verwalten-Pfeile, Aktualisieren-Symbole) setzen und `TabIndex` vergeben.
- *Aufwand:* 1–2 Std., maschinell erzeugbar. **Nach** dem Go-Live, es sei denn, ihr habt Mitarbeitende mit Screenreader.

@@ stil
## 4. Stil-Audit: Was nicht einheitlich wirkt (belegt am Export)
**Farben im Einsatz** (Anzahl Vorkommen):

| Farbe | Wo | Bedeutung heute | Bewertung |
|---|---|---|---|
| `#171496` Markenblau (18×) | Tabs, Panel, Verwalten-Knöpfe | Hauptaktion | gut, aber nicht überall |
| `RGBA(100,118,132)` Graublau (36×) | Buchungsdialog (Pfeile, Kalender, Schalter), alle Auswahl-Markierungen in Listen, Auswahlmodus | **Power-Apps-Standarddesign**, übrig geblieben | **uneinheitlich**: zwei „Hauptfarben“ |
| `RGBA(32,54,71)` Dunkelblau-Grau (132×) | Texte, Rahmen | Schrift | ok |
| `#00A96B`/`#00a96b` Grün (44×) | frei, Erfolg, ausgewählte Dauer, Speichern im Dialog, Schalter im Panel, eingecheckt im Dashboard | **fünf Bedeutungen** | überladen |
| `#4DC398` helles Grün (1×) | Kreis einer freien Kachel | frei | ok |
| `#EB3951` Rot (38×) | belegt/eingecheckt im Grundriss, gesperrte Dauer-Knöpfe, „Besetzt“, Auschecken | „nicht möglich“ und „eingecheckt“ zugleich | widersprüchlich (BD-14) |
| `#FFA500` Orange (10×) | gebucht, nicht eingecheckt | | ok |
| Grautöne: `#F7F7F7`, `#F0F0F0`, `#D0D0D0`, `RGBA(241…)`, `RGBA(234…)`, `RGBA(233…)`, `RGBA(220…)`, `RGBA(205…)`, `RGBA(166…)`, `RGBA(120…)` | Hintergründe, Trennlinien, „Tisch Buchen“-Knopf | | **zehn Grautöne**, drei würden reichen |

**Knöpfe** (44):
- **Hauptaktion:** Blau mit Hover −20 % (9×; `btnAbbrechenTischePanel` „<“ ist ebenfalls blau, nicht schwarz). Im Buchungsdialog aber grün (`btnSpeichern`), im Raum-Panel mit graublauem Hover (toter Code).
- **Schließen/Abbrechen:** schwarz mit Hover **heller** (+30 %), während blaue Knöpfe beim Hover **dunkler** werden. Vier Beschriftungen: „Schließen“, „Abbrechen“, „x“, „<“.
- **Gedrückt:** drei verschiedene Muster. Blau wird invertiert (weißer Grund, blaue Schrift). Schwarz und grün werden unlesbar (F-L3). Ohne Angabe gilt der Standard. → L3 vereinheitlicht die kaputten.
- **Gesperrt:** rot verblasst 70 % (11×) bzw. 85 % (4×, nur toter Raumcode). Sonst grau (Standard).
- **Schriftgrößen:** Standard bei 38 Knöpfen, dazu 10, 11, 14, 25. „Tisch Buchen“ ist mit 11 kleiner als alles andere.
- **Stornieren** sieht aus wie Speichern (blau). Im Tab-Dialog stehen beide nebeneinander → Fehlklick-Gefahr. → L8 (rot).
- **Dauer-Knöpfe:** „+1Std“, „-2std“, „5 Std“ → L9.

**Eingabefelder:**
- Auswahllisten im Panel: blauer Pfeil, Hover −20 %. Im Buchungsdialog: graublauer Pfeil, Hover hellgrau. Stockwerk: kein Rahmen, eigener Hover. → L7 gleicht den Dialog an.
- Kalender: Panel blau, Dialog graublau, Dashboard ohne Symbol. → L7.
- Wochentag-Schalter: Panel grün, Dialog graublau → L7.

**Texte und Titel** (L9 deckt die meisten ab):
- Englisch: „My personal desk“, „My meetings“ (ausgeblendet), „Dashboard“ (kann bleiben, ist gängig).
- Titel in vier Formen: „Check-in: X“, „Tisch: X“, „Tisch X“, „Verwalten: Tisch X“, plus „Tisch “ vor einem Namen, der schon „OG Desk 5“ heißt („Tisch OG Desk 5“).
- Leere Listen: „---“ und „-Keine Einträge-“.
- „Tisch Buchen“ und „Raum Buchen“ mit großem B.
- Adresse „Matthäus-Merian-Strasse“ (ss) steht dreimal hart im Code.

**Vollständige Prüfung aller Zustände (Hover, Gedrückt, Auswahl, Gesperrt) über alle Steuerelement-Typen** (Tabelle im Anhang B, maschinell aus dem Export):

| Bereich | Befund (belegt) | Paket L |
|---|---|---|
| Auswahllisten: Pfeil-Hover | `ChevronHoverBackground` ist bei **allen 7** sichtbaren Listen graublau, auch wo der Pfeil blau ist. Beim Hover springt ein blauer Pfeil auf Graublau | L10 |
| Auswahllisten: markierte Zeile | `SelectionFill` ist bei allen 8 graublau | L10 (6 Listen, Raumcode ausgenommen) |
| Auswahllisten: Hover | Panel `ColorFade(Self.Fill; −20 %)`, Dialog hellgrau `RGBA(205,209,213)`, Stockwerk blau 8 % | durch L7 (Dialog wie Panel) teilweise |
| Listen-Auswahlbalken | Dashboard blau `#171496`, Buchungen-Tab graublau | L10 |
| Akzentbalken in Dialogen | `Rectangle5`, `Rectangle6`, `Rectangle6_1`, `Rectangle6_2` graublau | L10 |
| Unsichtbare Klickflächen (Kachel, Einchecken, Verwalten, Logo) | **fünf** verschiedene Hover-Stärken: 4 %, 8 %, 15 %, 20 %, 20 % | L11 (einheitlich 10 %) |
| Dialog-Hintergründe | Popups weiß, aber Tab-Verwalten und Mehrfach-Dialog grau `RGBA(234,234,236)` | L12 |
| Knöpfe gedrückt | siehe oben, 7 unlesbar | L3 |
| Knöpfe Hover | dunkel → heller (+30 %), blau → dunkler (−20 %), Dauer-Knöpfe −15 % | **nicht** in L. Gewollt kann „dunkle Knöpfe werden heller“ sein, es wirkt aber uneinheitlich. Vorschlag für später: überall `ColorFade(Self.Fill; −15 %)`, schwarze Knöpfe durch Dunkelgrau ersetzen |
| Gesperrte Knöpfe | Dauer-Knöpfe rot verblasst (`DisabledFill`), Speichern/Stornieren grau (Standard). Nach Paket K sind gesperrte Speichern-Knöpfe grau | bewusst so: rot = „geht nicht wegen Belegung“, grau = „gerade nicht bedienbar“ |
| Schalter (Toggle) | `TrueFill` 6× graublau, 5× grün, `FalseFill` überall Standard | L7 (Wochentage grün, Auswahlmodus blau) |
| Kontrollkästchen | alle 4 gleich (belegt) | ok |
| Kalender | Symbolhintergrund blau, graublau, transparent, hellgrau (Raum) | L7 |
| Symbole (Aktualisieren) | dunkel, ohne eigene Hover-Farbe | ok, siehe „Drei Stellen zum Aktualisieren“ |
| Schriftfarben | vier Dunkeltöne: `RGBA(32,54,71)` (Standard, 132×), `RGBA(50,49,48)` (4×), Schwarz, Grau `RGBA(120,120,120)` | später mit der Farbtabelle |
| Bilder | Bearbeiten-Symbol in beiden Listen mit Hover, Tisch-Symbole ohne (richtig, sie sind nicht klickbar) | ok |
| **Logo als Knopf** | Das **Technoform-Logo** in der Kopfzeile (`Image6`) ist der Aktualisieren-Knopf (belegt). Das errät niemand | Vorschlag: eigenes Aktualisieren-Symbol in die Kopfzeile, das Logo nur als Logo |
| Kalender-Trick im Dashboard | `dpAnsichtsDatum` hat transparenten Text und Rahmen und liegt über „Heute“/Datum (gewollt) | ok, aber ohne `AccessibleLabel` für Screenreader unsichtbar (P10) |

**Sonstiges:**
- **Drei Stellen zum Aktualisieren** (Symbol im Dashboard, Symbol im Buchungen-Tab, Symbol in der Kopfzeile mit eigener Klickfläche `btnHitArea_1`), alle mit derselben Formel (belegt). Eine in der Kopfzeile reicht. Mit dem Timer aus P3 braucht man sie fast nie.
- Die **Handy-App** nutzt schon das Markenblau `RGBA(23, 20, 150)` = `#171496` (belegt). L7 zieht die Desktop-App in dieselbe Richtung, damit beide Apps gleich aussehen.

**Bewusst nicht in Paket L (deine Entscheidung):**
- Farbe für **eingecheckt** (BD-14).
- Grautöne zusammenfassen: viele Properties, nur Optik, später in einem Zug.
- Schriftgrößen-Raster.
- Eine **Farbtabelle in `App.Formulas`** (`FarbeHaupt = ColorValue("#171496");` usw.), auf die alle Properties verweisen. Das ist der saubere Weg, aber er berührt über 200 Properties. Lohnt sich erst, wenn die App länger lebt.

@@ verbesserungen
## 5. Weitere Verbesserungsvorschläge (Einschätzung, nach Nutzen sortiert)
1. **Kurzanleitung** (1 Seite) und ein Teams-Kanal für Rückmeldungen zum Go-Live: größter Nutzen pro Minute.
2. **P2 entscheiden** (Check-in mit Folge oder weg).
3. **P1** (Restzeit im Grundriss buchen): vermeidet die häufigste Verwirrung nach der Tischliste.
4. **„Heute“-Knopf** neben dem Datum im Dashboard (zurück zum heutigen Tag mit einem Klick).
5. **„Wer sitzt wo“ ohne Namen** als Option, falls der Datenschutz Namen ablehnt: nur Farbe, keine Initialen, kein Name im Popup.
6. **Serie direkt im Buchungs-Tab sichtbar machen:** Termine mit derselben `SerienID` zusammen anzeigen und gemeinsam stornieren. Das geht erst, wenn Paket K die `SerienID` schreibt.
7. **Kennzahlen für die Geschäftsleitung** (Auslastung pro Woche) über einen Flow, der jede Nacht vor dem Löschen zählt. Der Aufräum-Flow löscht heute alles nach 7 Tagen, damit ist **jede Auswertung unmöglich**. Wenn Auslastung je gefragt ist: vorher zählen oder archivieren.
8. **Fehlermeldungen protokollieren:** `Trace()` an den `IfError`-Stellen, damit du im Livemonitor oder in App Insights siehst, was bei Nutzern schiefgeht, statt auf Screenshots zu warten.
9. **Raumcode löschen** (L4, BD-22): 21 Steuerelemente, 36 Abfragen beim Start und Verwechslungsgefahr beim Lesen.
10. **Handy-App** vor oder mit dem Go-Live teilen (sie ist im Test sauberer als die Desktop-App).
