@@ kopf
# Handy „Tisch zeigen“: alle Properties (12.10.2026)

Für den Handy-Chat. Grundlage ist der **echte Handy-Export 12.10. 12:05** („handy echt“). Jeder Diff rechnet gegen diesen Export. Erzeugt und geprüft mit `werkzeuge/handy_tisch_zeigen.py`, die Daten mit `werkzeuge/tisch_zeigen_v2.py`. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

@@ kurzfassung
## Kurzfassung
- **Achtung, Export verwechselt (belegt):** `handytischbuchungegrundrisseinbauen12.10.` enthält die **Desktop-App** „Tischbuchung“. Sie hat dieselbe App-ID und ist zeichengleich mit dem Desktop-Export 11:52. Der echte Handy-Export ist `handy echt 12.10.` (12:05). Gegen den rechnet dieses Dokument.
- **Stand Handy-Export (belegt):**
  - `lblTischH.Width` ist korrigiert (`Parent.Width - 360`).
  - **H8 ist nur zu drei Vierteln drin:** `tmrJetzt`, `ddDatum.Items` und `lblHeuteTitel.Text` ja, **`App.OnStart` nein**. Damit ist `varHeute` beim Start leer.
  - Folge: Beim ersten Timer-Takt, etwa 1 Minute nach dem Start, setzt die App `ddDatum` zurück und lädt die Listen neu. Wer in dieser Minute „Morgen“ gewählt hat, steht plötzlich auf „Heute“.
  - **T0 holt das nach.** Der Block ist zeichengleich mit H8, die Vorher-Fassung passt zum Export (maschinell geprüft).
- **Daten gegengeprüft (belegt):**
  - Ich habe alle 35 Tische aus dem Desktop-Export 11:52 und der REST-Reihenfolge unabhängig nachgerechnet. Ergebnis: **0 Abweichungen** zur `tabelle_handy_de.txt`.
  - Jedes Rechteck liegt in `handy_plan_OG/UG.jpg` auf seinem Tisch (Überlagerung, `pruef_overlay_*.png`).
  - Meine Tabelle vom Vormittag (`tabelle_hoch_de.txt`) war für OG 6–13 falsch, weil ich die falsche Reihenfolge angenommen hatte. Sie ist überholt.
- **Aufbau wie vorgeschlagen, mit drei Verbesserungen:**
  1. **Eine** benannte Formel `TischPlan` als Datensatz (`Farbe`, `Fuellung`, `Tische`).
     - Es gibt nur eine Formel, also braucht es **kein Trennzeichen**. Die Frage nach `;` oder `;;` (T-U2) entfällt.
     - Die Farbe ändert man **an einer Stelle**: `Farbe` und `Fuellung` in `App.Formulas`. Vorgabe ist Orange.
  2. Ein **Vollbild-Hintergrundknopf** `btnTischPlanHintergrund` hinter dem Plan.
     - Er fängt alle Klicks ab, damit darunter nichts bedienbar ist. Ein Container allein fängt keine Klicks.
     - Ein Tipp daneben schließt den Plan.
  3. Der Knopf ist in beiden Karten so gesetzt, dass er nichts überlappt. Dafür werden `lblZeitH` und `lblZeitM` etwas schmaler (maschinell geprüft bei Layoutbreite 640).
- **Aufklappen in der Karte: weiterhin nein.**
  - Die Karten haben feste Höhen (`TemplateSize` 300 und 260, belegt). Aufklappen hieße eine Galerie mit variabler Höhe und ein Bild je Karte.
  - Das Overlay rendert genau **ein** Bild, nur wenn es offen ist.
- **Umfang:** 6 Schritte, 123 Properties, 8 neue Steuerelemente. **0 SharePoint-Abfragen** durch das Feature (maschinell geprüft). Maschinell 0 Fehler, in Studio nichts getestet. Nicht unabhängig geprüft.

@@ vorbereitung
## 1. Vorbereitung (vor T1)
1. Sicherung: Datei → Speichern unter → Dieser Computer (`.msapp`).
2. **Bilder hochladen:** Medien → Hochladen → `handy_plan_OG.jpg` und `handy_plan_UG.jpg`. In der Medienliste müssen sie **`handy_plan_OG`** und **`handy_plan_UG`** heißen. Sonst bleibt `imgTischPlan.Image` rot.
3. Reihenfolge: T0 → T1 → T2 → T3 → T4 → T5. Nach jedem Schritt die App-Prüfung ansehen: keine roten Fehler.

@@ T0
Nur die Zeile `Set(varHeute; Today());;` kommt dazu. Der Rest ist der Export (Diff).

**Test:**
1. App neu öffnen (Vorschau neu starten).
2. Sofort im Tab „Buchen“ „Morgen“ wählen und 70 Sekunden warten. Die Auswahl bleibt auf „Morgen“.

@@ T1
**Einfügen:** `App` markieren → Property **`Formulas`** → den ganzen Block einfügen. Die Property ist im Export leer.
- Ist `Formulas` in Studio nicht auswählbar, die App-Einstellung „Benannte Formeln“ prüfen. In der Desktop-App laufen benannte Formeln mit denselben App-Einstellungen (belegt).

**Farbe ändern:** nur hier.
- `Farbe` ist der Rand.
- `Fuellung` ist dieselbe Farbe mit Transparenz: Der letzte Wert 0,3 heißt 30 % deckend, die Tischnummer bleibt lesbar.

**Test:** Die App-Prüfung zeigt an `App.Formulas` nichts Rotes.

@@ T2
**Neu anlegen:**
1. `galHeute` → Vorlage der ersten Karte → **`conKarteH`** markieren.
2. Einfügen → Schaltfläche (klassisch).
3. Umbenennen in **`btnTischZeigenH`**. Er muss **in** `conKarteH` liegen.

Lage: rechts neben der Uhrzeit, unter dem Status (Y 80–130). Die Knöpfe „Einchecken“ und „Verwalten“ beginnen bei Y 150. `lblZeitH` wird 190 schmaler: Platz für „hh:mm bis hh:mm“ bleibt (geschlussfolgert, Breite etwa 346 bei Layout 640).

@@ T3
**Neu anlegen:**
1. `galMeine` → Vorlage der ersten Karte → **`conKarteM`** markieren.
2. Einfügen → Schaltfläche (klassisch).
3. Umbenennen in **`btnTischZeigenM`**.

Lage: rechts unter „Verwalten“ (Y 176–224, Kartenhöhe 236). `lblZeitM` wird 10 schmaler, damit es den Knopf nicht berührt.

@@ T4
**Neu anlegen, Namen exakt so, in dieser Reihenfolge:**
1. `Screen1` markieren → Einfügen → Schaltfläche (klassisch) → **`btnTischPlanHintergrund`**.
2. `Screen1` markieren → Einfügen → Layout → **Container** → **`conTischPlan`**.
3. `conTischPlan` markieren → Einfügen → Textbeschriftung → **`lblTischPlanTitel`**.
4. `conTischPlan` markieren → Einfügen → Medien → Bild → **`imgTischPlan`**.
5. `conTischPlan` markieren → Einfügen → Formen → Rechteck → **`recTischMarke`**. Es muss in der Strukturansicht **über** `imgTischPlan` liegen.
6. `conTischPlan` markieren → Einfügen → Schaltfläche (klassisch) → **`btnTischPlanSchliessen`**.
7. **Ebenen:** `conLadeOverlay` markieren → Neu anordnen → **Ganz nach vorne**. Danach ist die Reihenfolge der `Screen1`-Kinder von unten nach oben:
   - `conRoot`, `tmrJetzt`, `conDlgHintergrund`, `conDlgVerwalten`, `conDlgStorno`
   - `btnTischPlanHintergrund`, `conTischPlan`
   - `conLadeOverlay`

**Warum diese Ebenen:**
- Der Plan liegt über den Dialogen. Er kann aber nie zusammen mit ihnen offen sein: Der Hintergrundknopf deckt alles ab, und die Tab-Knöpfe schließen beides (T5).
- Das Lade-Overlay bleibt ganz oben. „Aktualisieren“ schließt den Plan vorher (T5).

**Größe (geschlussfolgert, Layout 640 × 1136 hochkant, belegt):**
- Bildhöhe = Platz zwischen Titel und Schließen-Knopf, höchstens Breite × 2,5. Breite = Höhe ÷ 2,5.
- Bei 640 × 1136 ist das etwa 812 × 325. Ein Tisch ist dann etwa 27 × 45 bis 45 × 27 Einheiten groß.
- Auf kleineren und größeren Handys passt sich das an, weil alles über `Parent` rechnet. Die Anteile gelten genau, weil das Bild kein Rand hat (Seitenverhältnis 2,5 geprüft).

@@ T5
Nur `Set(varZeigeTisch; false);;` vorne. Der Rest ist der Export (maschinell geprüft).

@@ test
## 3. Testablauf
Vorher: T0–T5 eingefügt, Bilder hochgeladen, App-Prüfung ohne rote Fehler. Vorschau, dann am echten Handy.

| ✓ | Test | Erwartung |
|---|---|---|
| ☐ | 1 Eigene Buchungen anlegen, nacheinander (keine zwei Tische zur selben Zeit): **OG Desk 3**, **Quiet Desk 1**, **UG Desk 14**, **UG Desk 18**. **Big Table** am PC über den Grundriss buchen, weil die Handy-App ihn nicht anbietet | Alle stehen unter „Meine“ (und unter „Heute“, wenn heute) |
| ☐ | 2 Bei jeder Buchung **„Tisch zeigen“** | Plan des richtigen Geschosses, hochkant. Titel z. B. „OG Desk 3 · Obergeschoss“. Das orange Rechteck liegt **genau** auf dem Tisch mit der Nummer. Kein anderer Tisch ist markiert |
| ☐ | 3 Schließen über „Schließen“, über einen Tipp neben den Plan, über einen Tab-Knopf | Der Plan ist zu, die App ist normal bedienbar |
| ☐ | 4 OG-Buchung zeigen, schließen, dann UG-Buchung zeigen | Das Bild wechselt aufs UG, das Rechteck sitzt richtig. Kein Rest vom OG |
| ☐ | 5 Plan offen, auf „Aktualisieren“ tippen geht nicht, weil der Plan alles abdeckt. Nach dem Schließen „Aktualisieren“ | „Aktualisiert.“. Der Plan bleibt zu |
| ☐ | 6 Plan offen, auf „Verwalten“ einer Karte tippen geht nicht, weil der Hintergrund abdeckt | kein Verwalten-Dialog unter dem Plan |
| ☐ | 7 Karten ansehen | „Tisch zeigen“ überlappt weder Status, Uhrzeit noch Knöpfe. Die Uhrzeit ist vollständig lesbar |
| ☐ | 8 Kleines Handy (z. B. iPhone SE) und großes Handy | Der Plan passt ganz auf den Bildschirm, „Schließen“ ist sichtbar, das Rechteck sitzt |
| ☐ | 9 Monitor (optional): „Tisch zeigen“ und Schließen | **keine** `getRows` |
| ☐ | 10 T0: App neu öffnen, „Morgen“ wählen, 70 s warten | bleibt „Morgen“ |
| ☐ | 11 Testbuchungen stornieren, veröffentlichen, Sicherung | |

@@ unsicher
## 4. UNSICHER
| Nr | Was | Prüfen |
|---|---|---|
| H-U1 | Benannte Formel als Datensatz mit `Table` in der Handy-App (`App.Formulas` ist dort neu). Belegt nur für die Desktop-App | App-Prüfung nach T1. Wenn rot: dasselbe als `Set(varTischPlan; { … })` am Ende von `App.OnStart` und in den Formeln `TischPlan` durch `varTischPlan` ersetzen. Dann melden, ich erzeuge die Blöcke neu |
| H-U2 | Medienname nach dem Hochladen genau `handy_plan_OG`/`handy_plan_UG` | Test 2 |
| H-U3 | Tippen auf `btnTischPlanHintergrund` über den Galerien wird abgefangen (klassische Schaltfläche, Muster wie Desktop `btnHitArea`) | Test 6 |

@@ rueckfall
## 5. Rückfall
1. Die 8 neuen Steuerelemente löschen: `btnTischZeigenH`, `btnTischZeigenM`, `btnTischPlanHintergrund`, `conTischPlan` samt Inhalt.
2. `App.Formulas` leeren.
3. `lblZeitH.Width`, `lblZeitM.Width`, `btnTabHeute/Buchen/Meine.OnSelect` und `icoAktualisieren_1.OnSelect` auf Anhang A zurücksetzen.
4. Medien `handy_plan_OG`/`handy_plan_UG` löschen.
5. **T0 bleibt.** Es ist der fehlende Teil von H8 und unabhängig vom Feature.

@@ neu
## 6. Bei neuem Tisch oder Umbenennung
1. Tische in SharePoint ändern, dann in der Desktop-App die Positionen (`colTischPositionen`/`colTischPositionenUG`) anpassen. Der Desktop-Grundriss verschiebt sich sonst, siehe Hinweis 7.
2. Neuen Desktop-Export und die neue Reihenfolge der Liste `Tische` (REST) an den Handy-Chat. Sein Skript erzeugt Bilder und `tabelle_handy_de.txt` neu.
3. Gegenprüfung durch mich mit `werkzeuge/tisch_zeigen_v2.py`, dann nur zwei Dinge in der App ersetzen: den Teil `Tische:` in `App.Formulas` und die zwei Bilder (gleiche Namen hochladen, alte vorher löschen). Kein anderer Block ändert sich.

## 7. Zum Hinweis Desktop (Galerie-Versatz)
- Bestätigt (belegt, `Rectangle1.Y`): Der Versatz hängt an der ID-Reihenfolge in `Tische`. Ein neuer oder gelöschter Tisch verschiebt Kacheln im Desktop-Grundriss.
- Der Vorschlag ist richtig: echtes Bild-Y in die Positionstabellen und `Rectangle1.Y` vereinfachen. Das wird nach dem Go-Live bewertet und ist im Backlog vermerkt.
