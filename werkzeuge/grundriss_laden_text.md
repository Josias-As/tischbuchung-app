@@ kopf
# ÜBERGABE Tischbuchung: Grundriss-Ladeverhalten (Laden v1)
**v1 · 13.10.2026 · für Josias (Desktop-App „Tischbuchung“) · maschinell aus dem Export 13.10. 09:59 erzeugt und geprüft (`werkzeuge/grundriss_laden.py`) · unabhängig geprüft (Abschnitt 7) · in Studio nichts getestet**

Grundlage: Export `TischbuchungApp13.10.2026959_20261013075948.zip`. Er ist zeichengleich mit dem Analyse-Paket, und `props_de.json` = Export (maschinell geprüft). Kennzeichnung: **belegt** (Export/Dokument), **geschlussfolgert**, **UNSICHER** (mit Prüftest).

**Voraussetzung:** Jeder Block ersetzt die **ganze** Property. Wurde nach dem 13.10. 09:59 an `App.OnStart`, `App.Formulas`, `Gallery1.Items`, `ddTischePanel.Items` oder `ddStockwerk.SelectionColor` etwas gespeichert, wäre das weg. Dann erst einen neuen Export schicken und die Blöcke neu erzeugen lassen (Minuten).

@@ kurzfassung
## Kurzfassung
- **Plan von Claude Code: tragfähig, mit einer Änderung.** Statt `ClearCollect(colTische; Tische)` in `App.OnStart` lädt eine **benannte Formel** `TischeLokal` die Tische. Gründe:
  1. Die Ursache der 0/0-Kacheln ist, dass `App.OnStart` parallel zum Zeichnen läuft. Eine neue Sammlung in `App.OnStart` hätte wieder genau diese Abhängigkeit (geschlussfolgert).
  2. **Die App-Prüfung empfiehlt es selbst** (belegt, `AppCheckerResult.sarif`): 2× „Die Sammlung wird initialisiert, aber nie aktualisiert“ in `App.OnStart`. Das sind die zwei Positions-Sammlungen. Abhilfe laut Prüfung: benannte Formel in `App.Formulas`. `colTische` bekäme denselben Hinweis.
  3. Mit `colTische` müssten `TischNrOG/UG` (benannte Formeln) eine Sammlung lesen. Ob das zuverlässig neu berechnet, ist offen. `TischeLokal` liest wie heute die Liste.
  4. `App.OnStart` wird nur kürzer. Reihenfolge, Ladezeile und `varJetztTakt` am Ende bleiben unverändert.
- **Zwei Stufen, jede einzeln testbar und rücknehmbar:**
  - **Stufe 1 (L1 + L2), Wunsch 1 „keine Kacheln bei 0/0“:** Die Positionen werden benannte Formeln, mit denselben Namen und Werten 1:1. Die Kachel-Formeln bleiben unverändert.
  - **Stufe 2 (L3, dazu L4 als Kann), Wunsch 3 „OG↔UG sofort“:** Alle Tische werden **einmal** gelesen, danach lokal. Galerie, `TischNrOG/UG` und (L4) die Tischliste im Panel lesen daraus.
  - Wunsch 2 „Start im UG“ ist erledigt (belegt).
- **Umfang:** 5 Properties und `App.Formulas` zweimal (Stufe 1, dann Endfassung). Kein neues Steuerelement, keine neue Variable, kein Schreibzugriff.
  - Abfragen auf `Tische` (geschlussfolgert aus den Formeln):
    - **Beim Start:** heute bis zu 3 (Galerie, `TischNrUG`, Panel-Liste), danach 1.
    - **Beim ersten Wechsel aufs OG:** heute 1–2, danach 0.
  - Maschinell 0 Fehler, 6 von 6 Mutationen erkannt.
- **Unverändert (belegt):**
  - Positionen und Nummern (`Nr`, Galerie-Versatz). Die Reihenfolge bleibt die der Liste. Der neue UG Desk 14 ist Nr 19, also der letzte.
  - `Gesperrt` gilt wie heute ab App-Start. Beide Speichern-Knöpfe prüfen `Gesperrt` weiter **frisch am Server**.
- **Zeitpunkt:**
  - **K1** (`ddStockwerk.SelectionColor`, nur eine Farbe) kann heute rein.
  - **Stufe 1 und 2 nach dem Go-Live**, wie Claude Code empfiehlt. `App.Formulas` trägt den ganzen Grundriss, und der Gewinn ist etwa eine Sekunde beim Start. Am besten in einer ruhigen Stunde, mit Sicherung.
- **`Label3.Text` ist kein Fehler** (belegt). Das `"OG"` ist ein Vergleich mit `varSelectedTisch.Geschoss.Value`. Bei einem UG-Tisch steht „MMS Untergeschoss“ da.

@@ ursache
## 1. Ursache und Bewertung des Plans
**Warum stehen Kacheln kurz bei 0/0?** (geschlussfolgert, nicht gemessen)
- `usenonblockingonstartrule` ist an (belegt, `Properties.json`). Der Bildschirm wird also gezeichnet, während `App.OnStart` noch läuft.
- `Rectangle1.X` ist `LookUp(colTischPositionen…; Tisch = ThisItem.Titel).X * BasisSkalierung` (belegt). Solange die Sammlung leer ist, ergibt das leer → 0. Die Breite fällt dann auf „hoch“ zurück, weil `Ausrichtung` leer ≠ „Horizontal“ ist. Man sieht also hochkant stehende Kacheln oben links. Das passt zur Beobachtung.
- Benannte Formeln sind nie „noch nicht gesetzt“. Sie werden berechnet, sobald eine Kachel sie braucht. Microsoft empfiehlt sie genau dafür statt Sammlungen in `App.OnStart` (App-Prüfung, belegt; Microsoft-Seite „Große Apps“, Websuche).

**Warum ist der erste Wechsel OG↔UG langsam?** (geschlussfolgert)
- `Gallery1.Items = Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)` und `TischNrOG`/`TischNrUG` fragen je Geschoss am Server ab. Beim ersten Mal wird geladen, danach kommt das Ergebnis aus dem Zwischenspeicher.
- `ddStockwerk.OnChange` lädt außerdem `colGrundriss` neu (Ladezeile, belegt). Das bleibt so. Die Kacheln stehen sofort da, die Farben kommen mit der Antwort.

**Antworten auf die Fragen aus der Übergabe (Abschnitt 3):**

| Frage | Antwort |
|---|---|
| Plan tragfähig? | Ja. Positionen als benannte Formeln: ja. `colTische` ersetze ich durch die benannte Formel `TischeLokal`, Gründe in der Kurzfassung |
| Fallen bei benannten Formeln | (a) **Gleicher Name wie die alte Sammlung.** Zwischen L1 und L2 meldet Studio kurz „Name unbekannt“ an `Rectangle1`/`conDetailsPopup`. Das ist erwartet, nach L2 ist es weg (U2). (b) **Schreibgeschützt:** Niemand außer `App.OnStart` schreibt die Positionen (maschinell geprüft), also passt es. (c) **Abschlusszeichen:** jede Definition mit `;;` wie im Export, maschinell gezählt. (d) **Tabellenliteral:** gleiche Spalten und Werte, nur `Table(…)` statt `ClearCollect(…)`. `LookUp` darauf aus `Rectangle1.*` und `conDetailsPopup.*` funktioniert wie mit einer Sammlung (geschlussfolgert, Test 2/3) |
| Zwischenzustand beim Start | **Stufe 1:** Positionen sind immer da. Kacheln erscheinen, sobald `Tische` geantwortet hat, und gleich an der richtigen Stelle. **Stufe 2:** Bis `TischeLokal` geladen ist, ist die Galerie leer (keine Kachel statt falscher Kachel). Danach kommen Kacheln, `Nr` und Positionen **gleichzeitig**, weil Galerie und `TischNr` dieselbe Quelle haben. Fehler wirft das nicht (leerer `Filter`) |
| Schutz nötig (`Gallery1.Visible`)? | Nein. Eine leere Galerie zeigt nichts. Eine Sperre über `varJetztTakt` würde die Kacheln erst nach dem ganzen `App.OnStart` zeigen, also später. Nicht in v1 (U6) |
| Reihenfolge / `Nr` | Heute stammen `Nr` und Galerie aus zwei getrennten Server-Abfragen, beide ohne Sortierung, also nach ID. Künftig stammen beide aus **derselben** Tabelle und können nicht mehr auseinanderlaufen. Bleibt die Reihenfolge der Liste gleich (nach ID, geschlussfolgert), ändert sich keine Kachel um einen Pixel. Test 5 prüft das gegen Bildschirmfotos (U5) |
| Wirkung auf **Gesperrt** | Gleich wie heute: Stand beim App-Start (Betriebshandbuch). Ein frisch gesperrter Tisch ist bis zum Neustart grün. **Buchen geht trotzdem nicht**, weil `btnSpeichern`/`btnSpeichernTischePanel` frisch am Server prüfen (`LookUp(Tische; ID = varNeuTischID && Gesperrt = true)`, belegt). Test 8 |
| Typen | `varSelectedTisch` und `varDetailsTisch` werden nur aus `ThisItem` der Galerie oder mit `Blank()` gefüllt (belegt). Es gibt also nur einen Datensatz-Typ. Gelesen werden nur `ID`, `Titel`, `Geschoss`, `Gesperrt` (maschinell). Die liefert `TischeLokal` |
| Alternativen | (1) **Nur Positionen** = Stufe 1 allein. Löst 0/0, der erste Wechsel bleibt langsam. (2) **Nur `colTische`**, ohne benannte Positionen: löst 0/0 nicht sicher, weil die Positionen weiter von `App.OnStart` abhängen. (3) **`colTische` wie vorgeschlagen:** geht auch, aber mit neuer Start-Abhängigkeit, Prüfhinweis und offener Frage zu Formeln über Sammlungen. (4) **Später, Backlog:** echte Bild-Y-Werte in die Positionen, dann braucht `Rectangle1.Y` die Reihenfolge der Liste nicht mehr |
| Aufwand/Nutzen vor dem Go-Live | Nutzen klein (ca. 1 s beim Start, erster Wechsel sofort, kein Sprung). Risiko: `App.Formulas` und `App.OnStart` sind die zwei Properties, an denen der ganze Grundriss hängt. **Nach dem Go-Live**, ich stimme Claude Code zu. Ausnahme: K1 (nur eine Farbe) |

@@ einfuegen
## 2. Einfügen
1. **Sicherung:** Datei → Speichern unter → Diesen Computer (`.msapp`). Bildschirmfotos für Test 5 machen, **bevor** etwas geändert wird (siehe Test 0).
2. Reihenfolge: **K1** (jederzeit, auch heute) · **L1 → L2** direkt hintereinander, dann Tests 1–3 · **L3** (erst `App.Formulas`, dann `Gallery1.Items`), dann Tests 4–8 · **L4** (Kann), dann Test 9.
3. Nach jedem Schritt die App-Prüfung ansehen: keine roten Fehler. Ausnahme: zwischen L1 und L2 kurz Fehler an `Rectangle1`/`conDetailsPopup` (siehe L1).
4. `App.Formulas` liegt in Studio bei **App** → Property-Liste oben links → `Formulas`. Den ganzen Inhalt markieren (Strg+A) und ersetzen.
5. Erst nach Test 10 veröffentlichen.

@@ K1
**Befund 1 aus der Übergabe (belegt):** Die gewählte Zeile im Geschoss-Menü hat weiße Schrift auf Hellgrau `RGBA(196, 196, 203)`. Der Kontrast liegt bei **1,7 : 1** (gerechnet, WCAG verlangt 4,5 : 1). Mit `RGBA(32, 54, 71)`, dem Dunkelblau der App (`Gallery1.BorderColor`, `ddTischePanel.BorderColor`), sind es **7,2 : 1**.

**Test:** Geschoss-Menü öffnen. Die gewählte Zeile ist dunkel beschriftet und gut lesbar.
**Rückfall:** `RGBA(255; 255; 255; 1)`.

@@ L1
**Was:** Die zwei Blöcke `ClearCollect(colTischPositionen; …)` und `ClearCollect(colTischPositionenUG; …)` werden entfernt. Sonst ändert sich nichts: gleiche Reihenfolge, Ladezeile unverändert, `Set(varJetztTakt; Now())` bleibt die letzte Anweisung (maschinell geprüft).

**Erwartet:** Direkt danach zeigt die App-Prüfung Fehler an `Rectangle1.X/Y/Width/Height` und `conDetailsPopup.X/Y` („Name ist ungültig“), weil die Namen kurz fehlen. **Sofort mit L2 weitermachen**, nichts dazwischen speichern oder veröffentlichen.

**Rückfall:** Originalfassung aus Anhang A.

@@ L2
**Was:** Am Ende von `App.Formulas` kommen die zwei Positionstabellen dazu, gleiche Namen, Werte 1:1 aus `App.OnStart` (maschinell verglichen, 16 OG + 19 UG). Alles andere bleibt zeichengleich.

**Tests (nach L1 + L2):**
1. App-Prüfung: keine roten Fehler. Die zwei Hinweise „Die Sammlung wird initialisiert, aber nie aktualisiert“ (Leistung) sind weg.
2. **Speichern, Studio schließen und die App neu öffnen** (dann läuft `App.OnStart` wie beim Start). Beim Aufbau steht **keine Kachel oben links**. Die Kacheln stehen wie auf den Fotos aus Test 0 (UG, dann OG).
3. Eine freie Kachel antippen: Buchungsdialog mit Tischname und „… MMS Untergeschoss“. Schließen. Eine belegte Kachel antippen: Das Details-Fenster erscheint neben der Kachel.

**Rückfall:** `App.Formulas` aus Anhang A, dann `App.OnStart` aus Anhang A (in dieser Reihenfolge, dazwischen kurz Fehler).

@@ L3
**Was:**
- `App.Formulas` (Endfassung, Diff gegen Stufe 1): Neu ist `TischeLokal = ForAll(Tische As T; {ID: …; Titel: …; Geschoss: …; Gesperrt: …})`. `TischNrOG` und `TischNrUG` lesen daraus statt aus `Tische`. Sonst bleibt alles zeichengleich.
- `Gallery1.Items` liest aus `TischeLokal`.
- **Reihenfolge:** erst `App.Formulas`, dann `Gallery1.Items`.

**Tests (nach L3):**
4. App-Prüfung: keine roten Fehler, kein neuer Delegierungshinweis an `App.Formulas`. App neu öffnen (wie Test 2). Dann **sofort** auf OG wechseln: Die Kacheln stehen sofort da. Das Bild selbst kann beim allerersten Mal einen Moment brauchen (U4). Mehrmals hin und her wechseln.
5. **Positionen gegen die Fotos aus Test 0**, beide Geschosse und beide Fenstergrößen. Besonders UG Desk 13–18 und OG Desk 6–13 ansehen. Weicht eine Kachel um ein paar Pixel nach oben oder unten ab, ist die Reihenfolge anders (U5) → Rückfall Stufe 2, Foto an mich.
6. Im Grundriss das Datum auf morgen stellen: Die Farben ändern sich, die Positionen nicht.
7. Am Grundriss **UG Desk 14** für morgen 08:00–09:00 buchen. Die Kachel wird für morgen orange, die Buchung steht in der Liste. Danach stornieren.
8. **Gesperrt** (nur Josias, an einem Tisch ohne Buchungen, z. B. UG Desk 18):
   1. In SharePoint `Gesperrt` = Ja setzen. Die App bleibt offen.
   2. Die Kachel ist noch grün, wie heute. Antippen → Dialog → Speichern: Die App meldet, dass der Tisch gesperrt ist, und es entsteht keine Buchung.
   3. App neu öffnen: Die Kachel ist grau, Antippen meldet „gesperrt“.
   4. In SharePoint `Gesperrt` = Nein setzen, App neu öffnen.

**Rückfall Stufe 2:** `App.Formulas` = Block aus L2 (Stufe 1), dann `Gallery1.Items` = `Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)`.

@@ L4
**Was:** Die Tischliste im Panel („Tisch buchen“) liest `TischeLokal` statt `Tische`. Es ist genau ein Wort. Felder, Filter und Sortierung bleiben gleich.

**Warum Kann:** Die Formel wird auch bei geschlossenem Panel berechnet und liest heute beim Start alle Tische ein zweites Mal (geschlussfolgert, „unsichtbar ≠ nicht berechnet“). Mit L4 bleibt es bei der einen Abfrage. `Gesperrt` gilt auch hier ab App-Start, wie heute. Beim Speichern prüft die App frisch.

**Test:**
9. Panel öffnen, heute, eine freie Zeit: Die Liste zeigt alle buchbaren Tische, ohne Big Table und ohne gesperrte, gleiche Sortierung wie vorher (vor dem Einfügen ein Foto machen). Einen Tisch über das Panel buchen und wieder stornieren.

**Rückfall:** Original aus Anhang A (`Tische As Ti`).

@@ tests
## 4. Testbogen (Zeitachse)
| Zeit | Schritt | Test |
|---|---|---|
| vorher | **Test 0:** Sicherung `.msapp`. Bildschirmfotos des Grundrisses UG und OG im **Vollbild** und in einem **halb so breiten** Fenster. Dazu ein Foto der Panel-Tischliste (heute, eine freie Zeit). Optional Monitor starten (Studio → Erweiterte Tools → Monitor) und beim Start die Zeilen mit `Tische` zählen | Fotos liegen vor |
| K1 | Farbe | K1-Test |
| L1 + L2 | Positionen | Tests 1–3 |
| L3 | Tische lokal | Tests 4–8 |
| L4 | Panel-Liste | Test 9 |
| danach | **Test 10:** Monitor beim Start: `Tische` wird **einmal** abgefragt. Beim Wechsel aufs OG gibt es keine `Tische`-Abfrage. Dann veröffentlichen und im Browser mit Strg+F5 neu laden: keine Kachel oben links | Abfragen wie erwartet |
| danach | **Test 11:** Handy-Gegenprobe: am Handy einen Tisch buchen, am PC „Aktualisieren“. Die Kachel wird orange (Weg unverändert, nur zur Sicherheit) | wie vorher |

Gezählt wird beim Start, nicht beim Speichern. Testbuchungen danach stornieren. `Gesperrt` am Ende wieder auf Nein.

@@ rueckfall
## 5. Rückfall (gesamt)
- **Einzelschritte:** jeweils unter dem Schritt. Die Originale stehen in Anhang A.
- **Alles auf einmal:** make.powerapps.com → App → … → Details → **Versionen** → letzte Version vor der Änderung → **Wiederherstellen**. Oder die `.msapp`-Sicherung öffnen und veröffentlichen.
- Was nach dem Rückfall gilt: Die App verhält sich wie im Export 13.10. (0/0-Sprung beim Start, erster Wechsel lädt).

@@ unsicher
## 6. UNSICHER
| Nr | Was | Prüfen / Folge |
|---|---|---|
| U1 | `ForAll(Tische As T; {…})` in einer **benannten Formel**: Wird sie einmal geladen und dann wiederverwendet? Benannte Formeln mit `Tische` gibt es schon (`TischNrOG/UG`, belegt), mit `ForAll` noch nicht | Test 4 (App-Prüfung) und Test 10 (Monitor). Meldet Studio einen Fehler an `TischeLokal` oder fragt `Tische` öfter als einmal ab → Rückfall Stufe 2. Stufe 1 bleibt und löst 0/0 trotzdem |
| U2 | Benannte Formel mit demselben Namen wie die gerade entfernte Sammlung | Bleiben nach L2 Fehler an `Rectangle1`/`conDetailsPopup` stehen: speichern, Studio schließen und neu öffnen. Bleiben sie dann noch → Rückfall Stufe 1, mir die Fehlermeldung schicken |
| U3 | Ursache 0/0 ist geschlussfolgert, nicht gemessen | Test 2. Springen die Kacheln nach Stufe 1 weiter → Bildschirmvideo an mich. Möglich wäre dann noch `BasisSkalierung` beim Aufbau |
| U4 | Das OG-Bild (PNG, ca. 430 KB) ist beim Start unsichtbar und wird erst beim ersten Wechsel angezeigt. Ob der Browser es vorher lädt, steht nicht im Export | Test 4. Erscheinen die Kacheln sofort und das Bild kurz danach, liegt das am Bild, nicht an den Daten. Das lässt sich mit Formeln kaum ändern |
| U5 | `ForAll(Tische)` und `Filter(Tische; Geschoss…)` liefern dieselbe Reihenfolge (nach ID). Gestützt durch die REST-Reihenfolge vom 12.10. (nach ID, 35 Zeilen) | Test 5. Bei Abweichung verschiebt sich eine Kachel um ca. 1 Pixel je Platz in der Reihenfolge (geschlussfolgert aus `Rectangle1.Y`) |
| U6 | Kacheln können beim Start kurz **grün** sein, bevor `colGrundriss` geladen ist (Ladezeile am Ende von `App.OnStart`). Das ist heute schon so und wird nicht geändert | beobachten. Wenn es stört: später `Gallery1.Items` an `varJetztTakt` koppeln (zeigt Kacheln erst nach `App.OnStart`) |
| U7 | Scheitert das Laden von `Tische` (Netz), bleibt der Grundriss leer, ohne Meldung. Heute ist es ähnlich | App neu öffnen. Benannte Formeln dürfen kein `Notify` enthalten, deshalb gibt es keine Meldung |

@@ pruefung_unabh
## 7. Unabhängige Prüfung
PRUEFUNG_PLATZHALTER

@@ anhang_hinweis
Die Originale stammen aus dem Export 13.10. 09:59 (deutsche Schreibweise).
