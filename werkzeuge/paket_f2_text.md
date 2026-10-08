@@ kopf
# Paket F, Fassung 2: Freigabe in der App, Stornieren direkt, Timer

Stand 08.10.2026 · erzeugt mit `werkzeuge/paket_f2.py` und `doc_paket_f2.py` · **ersetzt Paket F (Fassung 1), Nachtrag 3 und 4 sowie G4, G5 und G8** · Ausgangslage ist der **tatsächliche Stand im Studio** (siehe 1) · Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**

@@ kurzfassung
## 0. Kurzfassung (wo A bis E stehen)
- **A Stornieren ohne Rückfrage-Dialog (Schritt F2):**
  - Die drei Stornieren-Knöpfe stornieren direkt, ohne neues Steuerelement.
  - Jeder Knopf hat: Sperre, frisch gelesene Buchung, **nur eigene** (Vergleich `Lower(E-Mail)`), `IfError`, Nachlese, ehrliche Meldung, Ladezeile.
  - Mehrfach-Stornieren: gleich viele Abfragen wie heute (1 Abfrage, 1 Sammel-Remove, Refresh, Ladezeile), also **nicht langsamer** als die gemessenen 9 s für 33 Buchungen.
  - G4 entfällt ganz.
- **B Timer (Schritt F8):** Legt `tmrAktualisieren` an und **ersetzt G8**, ohne `varZeigeStornoFrage`. Mit Check-in-Erinnerung, die nur dann eine Abfrage macht, wenn du laut Grundriss gerade eine nicht eingecheckte Buchung hast. Eine reine G8-Fassung ohne Paket F steht in Anhang C.
- **C Paket F angepasst:** F1 bis F8 in der richtigen Einfügereihenfolge.
  - F4 enthält Nachtrag 4.
  - F7 enthält G5 (`btnEinchecken.DisplayMode`) und neu das **Auschecken mit zweitem Tippen**.
- **D Einfügeliste ohne Doppelarbeit (Abschnitt 2):** Jede Property kommt **genau einmal** vor. Zu jeder steht, was neu ist, und bei jedem Block ein **Diff gegen den Stand im Studio**.
- **E Vorab-Test „Erstellt“ (Abschnitt 3):** zwei Minuten, **vor** F1.
- **Umfang:** 8 Schritte, 37 Properties, 1 neues Steuerelement (`tmrAktualisieren`, das schon aus G8 vorgesehen war).
- **Geprüft:** maschinell 0 Fehler, unabhängig geprüft (Anhang B). In Studio nichts getestet.
- **Wenn die Zeit knapp wird:** **F1 + F2 zuerst.** Sie sind unabhängig vom Rest (sicheres Stornieren). F3 bis F8 sind die Freigabe. Sie funktionieren nur **zusammen** richtig, also entweder alle oder keine vor dem Go-Live.

@@ ausgangslage
## 1. Ausgangslage (nach Josias’ Angaben, nicht im Export prüfbar)
- **Eingefügt:** G1, G2, G3, G6 (Fassung Nachtrag 4), G7, G9, G10, G11, G12, G13, G15, G16, G17, G18, G19, G20, G25. G22 teilweise.
- **Nicht eingefügt:** G4, G5, G8, G14, G21, G23, G24, G26.
- **Phase 0:** erledigt bis auf die Mail an Michael.
- Die Diffs und Anhang A rechnen mit genau diesem Stand: Gesamtplan-Endfassung, wo eingefügt, sonst Export 07.10. **Keine Property dieses Pakets liegt in G22** (maschinell geprüft). Der unklare Stand dort spielt also keine Rolle.
- **Sieht ein Diff anders aus als das, was im Studio steht:** stoppen und melden. Dann stimmt die Ausgangslage nicht, z. B. wenn ein Schritt doch (nicht) eingefügt wurde.

@@ vorabtest
## 3. Vorab-Test „Erstellt“ (E), vor F1, etwa 2 Minuten
**Warum:** Paket F liest die SharePoint-Spalte „Erstellt“ (intern `Created`).
- Im Export steht sie mit dem Anzeigenamen „Erstellt“, lesbar und filterbar (**belegt**).
- Ob Studio den Namen `Erstellt` annimmt, ist **UNSICHER** (U1).
- Ob die Spalte in Collections mitkommt, ist ebenfalls **UNSICHER** (U7, explizite Spaltenauswahl).

**Test 1 (Name):**
1. Auf `Screen1` vorübergehend eine Textbeschriftung `lblTestErstellt` einfügen.
2. `Text`:
```
"Erstellt: " & Text(First(Tischbuchungen).Erstellt; "dd.mm.yyyy hh:mm")
```
- Erwartung: ein Datum, kein roter Fehler. Ein gelbes Delegations-Dreieck ist hier egal.

**Test 2 (Spalte in einer Collection):**
1. Vorübergehend eine Schaltfläche `btnTestErstellt` einfügen.
2. `OnSelect`:
```
ClearCollect(colTestErstellt; Filter(Tischbuchungen; Endzeit > DateAdd(Now(); -1; TimeUnit.Days)));; Notify(CountRows(colTestErstellt) & " Zeilen, Erstellt der ersten: " & Text(First(colTestErstellt).Erstellt; "dd.mm.yyyy hh:mm"); NotificationType.Information)
```
3. In der Vorschau klicken. Erwartung: „… Zeilen, Erstellt der ersten: 07.10.2026 …“ mit Datum.

**Danach beide Steuerelemente löschen.**

**Wenn Test 1 rot ist:**
1. Im Test `Erstellt` durch `Created` ersetzen.
2. Geht es dann, an Claude Code melden „Spalte heißt Created“. Paket F wird mit `Created` neu erzeugt (etwa 15 Minuten).
3. **Nicht** selbst in den Blöcken ersetzen: Ein Teil der Namen ist ein eigener Feldname und muss bleiben.

**Wenn Test 2 kein Datum zeigt** (leer): melden. Dann verliert nur „spät gebucht“ die Schonfrist (U7). Paket F kann trotzdem eingefügt werden.

@@ F1
**Was neu ist:**
- `Set(varFreigabeMinuten; 30)` (die eine Zahl zum Ändern), `varCheckinGefragtID` und `varAuscheckFrageID` vorbelegt.
- Vor der Ladezeile: Check-in-Frage beim Öffnen.
- Die Ladezeile lädt `Erstellt` mit und lässt verfallene Buchungen weg.

**Danach:** in der Strukturansicht `App` → … → **OnStart ausführen**.
**Test:** App-Prüfung ohne rote Fehler. Eigene Buchung „jetzt bis +1 Std“ (vorher angelegt, nicht eingecheckt) → OnStart ausführen → Check-in-Dialog erscheint.

@@ F2
**Was neu ist (A):**
- Alle drei Knöpfe stornieren **direkt**, wie heute, aber sicher:
  - Zweifach-Sperre gegen Doppelklick.
  - Buchung frisch per `LookUp` lesen.
  - **Nur eigene** (`Lower(varStornoBuchung.Person.Email) <> Lower(User().Email)` → „Nur eigene Buchungen können storniert werden.“).
  - `Remove` in `IfError`, danach nachlesen, ob die Zeile weg ist, und eine ehrliche Meldung.
  - Ladezeile mit Freigabe-Regel.
- `DisplayMode`: grau, solange gespeichert wird.
- **Warum es ohne Rückfrage sicher ist:** Der Fehler aus G4 entstand, weil **zwischen** Frage und „Ja“ eine Variable wechseln konnte. Ohne Rückfrage gibt es dieses Zeitfenster nicht. Die Buchung wird beim Klick gelesen.
- **Mehrfach-Stornieren:** gleicher Ablauf wie heute (eine Abfrage der eigenen Buchungen, **ein** `Remove` mit allen Zielen, `Refresh`, Ladezeile). Neu sind nur Sperre und Freigabe-Ladezeile. Gleiche Zahl an Abfragen (**geschlussfolgert** aus den Formeln, gemessen sind 33 in ca. 9 s mit dem heutigen Ablauf).

**Test:**
- Dashboard → Verwalten → Stornieren → „Buchung storniert.“, Zeile in SharePoint weg.
- Doppelklick → eine Meldung.
- Tab „Buchungen“ → Verwalten → Stornieren → ebenso.
- Mehrfachauswahl mit 5 Buchungen → „5 Buchungen storniert.“ (Zeit grob vergleichen).

@@ F3
**Was neu ist:**
- **Kachel-Klick:** holt die Buchungen des Tisches, entfernt verfallene, öffnet den Buchungsdialog, wenn nichts übrig ist.
- **Sechs reine Ladestellen** (Stockwerk, Datum, vier Aktualisieren-Symbole): `Set(varFreigabeGrenze; …)` davor, `Erstellt` mitladen, verfallene nicht in `colGrundriss`. Die Spalten von `colGrundriss` bleiben gleich (`DropColumns`).

**Test:** Testzeile in SharePoint anlegen (Beginn vor 1 Std, CheckedIn = Nein). Nach `varFreigabeMinuten` (Testmodus siehe Testbogen) → Aktualisieren → Kachel grün, Klick öffnet den Buchungsdialog.

@@ F4
**Was neu ist (gegenüber G6 aus Nachtrag 4):**
- `Set(varFreigabeGrenze; …)`.
- Nach den Vorprüfungen `RemoveIf(…verfallen…)`.
- In der Nachlese werden verfallene **fremde** Buchungen ignoriert.
- Die Erfolgsmeldung nennt die Minuten.
- Ladezeile mit Freigabe-Regel.
- **Nachtrag 4 bleibt** (kein Refresh).

**Test:** Auf einen Tisch mit verfallener Buchung buchen → „Gebucht …“, keine Warnung. Nachtrag-4-Test 2: die neue Buchung erscheint ohne Aktualisieren in der Liste.

@@ F5
**Was neu ist:**
- `btnTischHinzufügen`: setzt `varFreigabeGrenze` beim Öffnen.
- `ddTischePanel.Items`: jede Buchung bekommt `Aktiv`, gezählt werden nur aktive.
- 5/9-Std.-Knöpfe: gleiche Prüfung, nur aktive Buchungen.

**Test:** Panel, heute, Zeit der verfallenen Testbuchung → Tisch ohne „(an … belegt)“, 5 Std wählbar.

@@ F6
**Was neu ist:**
- Verwalten-Dialoge: die Grenze für die Dauer-Knöpfe ohne verfallene Buchungen. `varVerlNaechste` kommt jetzt aus einer Collection: Ein roter Zwischenfehler nach `btnVerwalten` verschwindet nach `btnVerwalten_2`.
- Verlängern: Kollision ohne verfallene. **Neu:** „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“
- Eigene verfallene Buchung: „Diese Buchung ist verfallen …“.

**Test:** +1 Std über eine verfallene fremde Buchung geht. Eigene Buchung in eine zweite eigene hinein verlängern → Meldung.

@@ F7
**Was neu ist (ersetzt G5):**
- Einchecken nur von 30 Min vor Beginn bis zur Frist. Davor und danach wird frisch geprüft, ob der Tisch schon an jemand anderen vergeben ist.
- **Auschecken nach Beginn mit zweitem Tippen (Frage 1):**
  - Erstes Tippen: Meldung „Zum Auschecken bitte noch einmal tippen …“, und der Knopf heißt „Wirklich auschecken?“.
  - Zweites Tippen: Ende = jetzt (nächste Minute).
  - Der erste Tipp schreibt nichts und liegt **vor** der Sperre. Deshalb wird das zweite Tippen nicht von der 2-Sekunden-Sperre geschluckt.
  - Beim Öffnen des Dialogs wird die Frage zurückgesetzt (`btnEincheckenHeute`).
  - Vor dem Beginn nimmt Auschecken wie bisher nur den Check-in zurück.
- `btnEinchecken.DisplayMode` aus G5.
- Dashboard-Status „Verfallen“ (grau).
- Meldungen versprechen nicht mehr „frei“, sondern „andere können den Tisch wieder buchen“ (Frage 2).

**Test:**
- Buchung in 1 Std → „erst ab 30 Minuten vor Beginn“.
- Laufende Buchung → „Eingecheckt.“.
- Auschecken → erstes Tippen: Meldung, Knopftext ändert sich. Zweites Tippen → „Ausgecheckt. Deine Buchung endet um …“.
- Dialog schließen und wieder öffnen → Knopf heißt wieder „Auschecken“.
- Verfallene Buchung → „Zu spät …“, Status grau.

@@ F8
**Was neu ist (ersetzt G8, B):**
- `tmrAktualisieren` neu anlegen (5 Properties).
- `OnTimerEnd`: alle 5 Min aktualisieren, wenn kein Dialog offen ist. Wie G8, aber **ohne** `varZeigeStornoFrage`.
- Ladezeile mit Freigabe-Regel.
- **Check-in-Erinnerung:**
  - Nur wenn das Dashboard für heute offen ist **und** der Grundriss (`colGrundriss`, lokal, ohne Abfrage) eine nicht eingecheckte Buchung unter deinem Namen zeigt, die in 30 Min beginnt oder läuft.
  - Erst dann **eine** Abfrage der eigenen Buchungen. Gefragt wird einmal je Buchung.

**Anlegen:** `Screen1` markieren → Einfügen → Eingabe → Timer → umbenennen in `tmrAktualisieren`.
**Test:** App 5 Min offen lassen, in einem zweiten Fenster eine Buchung ändern → spätestens nach 5 Min sichtbar. Eigene Buchung mit Beginn in 20 Min → Check-in-Dialog nach höchstens 5 Min, nur einmal.

@@ fragen
## 5. Antworten auf die Fragen
**1. Bestätigung beim Auschecken:** Ja, jetzt per **zweitem Tippen** auf denselben Knopf, ohne neues Steuerelement (F7). Begründung: Auschecken nach Beginn beendet die Buchung, und neu buchen geht erst ab der nächsten halben Stunde. Ein versehentlicher Klick kostet also den Tisch.

**2. „Sofort frei“:** Das ist korrigiert, in den App-Meldungen (F7) und in `KURZANLEITUNG_und_GoLive_Mail_v3.md` / `BETRIEBSHANDBUCH_Michael_v3.md`. Die Formulierung ist jetzt: „andere können den Tisch wieder buchen“. Der Grundriss zeigt das bei anderen nach dem nächsten Laden, spätestens nach 5 Minuten. Buchbar ist der Tisch ab der nächsten halben Stunde.

**3. Zusätzliche Abfragen** (**geschlussfolgert** aus den Formeln, im Monitor prüfbar):

| Stelle | zusätzlich | Häufigkeit |
|---|---|---|
| F1 App-Start | +1 (eigene anstehende Buchungen), +1 nur wenn eine gefunden wird | 1× je App-Start |
| F8 Timer, Erinnerung | **0**, solange laut Grundriss keine eigene, nicht eingecheckte Buchung ansteht. Sonst +1 (+1 beim Fragen), höchstens bis zum Check-in oder Verfall, also etwa 12 Ticks | alle 5 Min je offener App |
| F8 Timer, Grundlast (wie G8) | `Refresh` (2 Galerien) + Ladezeile (1) = 3 | alle 5 Min je offener App, nur ohne offenen Dialog |
| F3 Kachel-Klick | +1 nur bei belegtem Tisch (Datensatz für das Popup per ID) | je Klick |
| F6 Verlängern | +1 („zwei Tische“) | je Verlängern |
| F7 Einchecken | +2 (vorher und nachher: Tisch schon vergeben?) | je Check-in |
| F4 Speichern | −2 bis −7 (Nachtrag 4, kein Refresh) | **je Buchung** |
| F2 Stornieren | ±0 gegenüber heute | je Storno |

Bei 30 Nutzern und offener App sind das etwa 18 Abfragen pro Minute durch den Timer, fast alles Grundlast aus G8. Die Freigabe selbst kostet in der Anzeige **keine** Abfrage.

**4. Handy-App:** bestätigt. Die Handy-App wird erst geteilt, wenn die Regel aus `AUFTRAG_Handy_Freigabe.md` dort eingebaut und getestet ist. Sonst kann man in der Handy-App eine verfallene Buchung einchecken, deren Tisch schon neu vergeben ist.

**5. „Nur eigene Elemente“: zu korrigieren.**
- **Nicht** „Listen verwalten“ befreit von der Einstellung, sondern die Berechtigung **„Listenverhalten außer Kraft setzen“** (Override List Behaviors). Sie steckt standardmäßig in **Entwerfen** und **Vollzugriff**, **nicht** in **Bearbeiten**. „Bearbeiten“ enthält dagegen „Listen verwalten“ ([Microsoft Learn](https://learn.microsoft.com/en-nz/sharePoint/sites/user-permissions-and-permission-levels), **belegt**).
- **Folgen:**
  - Kollegen als **Mitglieder** (Bearbeiten) sind betroffen, so soll es sein.
  - Josias als **Besitzer** (Vollzugriff) ist nicht betroffen.
  - Michael ist nur dann nicht betroffen, wenn er **Websitebesitzer** (Vollzugriff) ist, „Mitbesitzer der App“ allein reicht dafür nicht.
  - Der **Aufräum-Flow** läuft mit der Verbindung dessen, der sie angelegt hat. Mit Josias’ Verbindung (Vollzugriff) ist er nicht betroffen.
- **Vorsicht** (**geschlussfolgert**, Community-Bericht [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/378127/sharepoint-list-permissions-read-only-for-all-item)): Bekommt jemand zusätzlich über eine andere Gruppe „Entwerfen“ oder „Vollzugriff“, sieht und ändert er wieder alles. Deshalb **nach dem Setzen mit einem Kollegen-Konto testen**: fremde Buchung in der Liste ändern geht nicht, eigene geht.
- **Was ein künftiger Flow beachten muss:**
  1. Seine Verbindung braucht Vollzugriff oder Entwerfen, sonst kann er nur selbst angelegte Zeilen ändern oder löschen.
  2. **Zeilen, die ein Flow anlegt, gehören dem Konto der Verbindung.** Legt ein Flow Buchungen für andere an (z. B. aus Outlook), können diese Personen sie in der App **nicht einchecken, verlängern oder stornieren**. Ohne Check-in verfallen sie. Ein solcher Flow muss `CheckedIn` setzen oder die Buchung über die App der Person anlegen lassen.
  3. Die Verbindung nicht an ein persönliches Konto binden, das wegfallen kann (Vertretung).

@@ testbogen
## 6. Testbogen

| ✓ | Test | Ergebnis |
|---|---|---|
| ☐ | E Vorab-Test 1 (Name) und 2 (Collection), Test-Steuerelemente gelöscht | |
| ☐ | F1 App-Prüfung ohne rote Fehler, OnStart ausgeführt, Check-in-Frage beim Start | |
| ☐ | F2 Stornieren Dashboard, Tab, Mehrfach (5 Stück, Zeit), Doppelklick | |
| ☐ | Testmodus: Testknopf `btnTestFreigabe` mit `Set(varFreigabeMinuten; 1)`, in der Vorschau drücken. **`App.OnStart` nicht ändern** | |
| ☐ | F3 verfallene Testzeile → Kachel grün, Klick → Buchungsdialog | |
| ☐ | F4 über verfallene Buchung buchen, neue Buchung ohne Aktualisieren in der Liste | |
| ☐ | F5 Panel-Liste und 5 Std | |
| ☐ | F6 Verlängern über verfallene Buchung, „zwei Tische“ | |
| ☐ | F7 Einchecken (zu früh, laufend, zu spät), Auschecken mit zweitem Tippen | |
| ☐ | F8 Timer aktualisiert, Erinnerung einmal | |
| ☐ | **Testknopf gelöscht**, in `App.OnStart` steht `Set(varFreigabeMinuten; 30)` | |
| ☐ | Veröffentlichen | |

@@ unsicher
## 7. UNSICHER
| Nr | Was | Test / Abhilfe |
|---|---|---|
| U1 | Name `Erstellt` in Studio | Vorab-Test 1 |
| U7 | `Erstellt` in Collections (explizite Spaltenauswahl) | Vorab-Test 2 |
| U8 | Die Timer-Vorprüfung vergleicht `colGrundriss.Name` (Anzeigename aus SharePoint) mit `User().FullName`. Weichen beide ab (Schreibweise im Profil), fragt der Timer nie, nur der App-Start fragt | Test F8. Fragt der Timer nicht, melden |
| U9 | Ob die Galerien nach `Remove` ohne `Refresh` aktualisieren, ist in der Handy-App gemessen (T-23). Hier bleibt `Refresh` beim Stornieren trotzdem drin. Grund: Der Tab „Buchungen“ hat einen bekannten Neuaufbau-Trick (`varGalleryNeuAufbauen`, Frage 15) | kein Test nötig |
| U3 | Geräteuhr | wie Paket F |

@@ anhangc
## Anhang C: G8 ohne Paket F (nur falls Paket F nicht eingefügt wird)
Wenn F3–F8 nicht vor dem Go-Live kommen, aber der Timer schon: `tmrAktualisieren` wie in F8 anlegen (`Duration`, `Repeat`, `AutoStart`, `Visible` wie dort) und `OnTimerEnd` so setzen. Das ist G8 ohne `varZeigeStornoFrage`. Später ersetzt F8 diese Property.
