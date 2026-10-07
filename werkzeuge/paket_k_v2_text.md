@@ kopf
# ÜBERGABE Tischbuchung: Paket K v2 (Korrektheit, Verlängern, Speichern, Tischauswahl)
**v2 · 07.10.2026 · Basis: veröffentlichter Export „Tischbuchung App 07.10.2026 verbesserung analyse“ (enthält L2) · alle 55 Properties maschinell aus diesem Export erzeugt und geprüft (`werkzeuge/paket_k_v2.py`, Anhang 2) · unabhängig geprüft, Befunde eingearbeitet (Abschnitt „Unabhängige Prüfung“) · ersetzt `UEBERGABE_PaketK_v1.md` · noch nichts davon eingefügt**

Kennzeichnung: **belegt** = im Export/Dokument nachgesehen · **gemessen** = Livemonitor oder Test · **geschlussfolgert** = abgeleitet, nicht getestet · **UNSICHER** = offen, mit Prüftest (Abschnitt UNSICHER).

@@ kurzfassung
## 0. Kurzfassung
- **v1 hatte einen echten Fehler.** Die Doppelklick-Sperre nur über `DisplayMode` hält nicht. Die Handy-App hat das am 06.10. gemessen: Ein Doppeltipp auf „+1 Std“ hat zweimal verlängert (belegt, `ENTSCHEIDUNGEN.md` E-07). v2 nutzt deshalb an allen 8 Schreibstellen die dort erprobte Zweifach-Sperre `If(!varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis); …)`. Folge: Nach jeder Speichern-, Verlängern-, Stornieren- oder Einchecken-Aktion reagiert 2 Sekunden lang **kein** Schreibknopf (still, ohne Meldung), und das Lade-Overlay erscheint jetzt auch beim Verlängern, Stornieren und Einchecken.
- **Eine Regel für beide Apps.** v2 übernimmt die Regeln, die du für die Handy-App schon bestätigt hast: nie über 22:00, kein Buchen in der Vergangenheit, keine zwei Tische zur selben Zeit, Einchecken ab 30 Minuten vor Beginn. Außerdem dasselbe Schreibmuster: frisch lesen, prüfen, `IfError`, nachlesen, ehrlich melden. Die Formeln sind dort schon in Betrieb (belegt).
- **Verwalten-Dialoge neu gedacht (Teil A).** Beim Öffnen wird **einmal** berechnet, bis wann die Buchung verlängert werden kann. Die 24 Plus-/Minus-Properties fragen danach **keine Daten mehr ab** (vorher je eine eigene Abfrage, auch bei geschlossenem Dialog, gemessen ~50 Abfragen pro Schreibvorgang). Befund B0 ist damit an der Wurzel weg: Der Tab liest seine eigene Buchung (statt der Ein-Zeilen-Lösung K1).
- **Speichern (Teil B):** Beide Speichern-Knöpfe laufen gleich, beide mit Sammel-Patch. Neu dabei: Kollisionsprüfung mit Zeitfenster, Prüfung „du hast schon einen Tisch“, **`SerienID` wird geschrieben und nachgelesen** (ehrliche Anzahl statt lokaler Zählung), Erkennung gleichzeitiger Buchungen, **eine** Meldung mit allem. Bei einem Fehler bleiben die Eingaben stehen.
- **Tischauswahl (Teil C):** Das Panel zeigt nur noch freie Tische, sortiert, ohne Big Table, das aktuelle Stockwerk zuerst. Bei Serien steht dabei, an wie vielen Tagen ein Tisch belegt ist. Beim Öffnen ist kein Tisch vorausgewählt. „5 Std“/„9 Std“ starten an anderen Tagen um 08:00.
- **Geprüft:** eigene maschinelle Prüfung (Anhang 2) und ein unabhängiger Prüf-Agent. Sein Urteil: „einfügebereit nach Korrekturen“, mit 1 Fehler, 3 Risiken und 12 Hinweisen. Alle sind eingearbeitet oder begründet offen (Abschnitt „Unabhängige Prüfung“).
- **Aufwand:** 22 Schritte, 55 Properties, jeder Schritt einzeln testbar. Die Teile A bis D sind voneinander unabhängig. Schritt 0 zuerst ist empfohlen, aber nicht zwingend.
- **Was nur du entscheiden kannst:** sieben Punkte in Abschnitt 2. Überall steht ein Vorschlag (meist die Regel der Handy-App). Wenn du nichts sagst, gilt der Vorschlag.

@@ behebt
{"0": "Voraussetzung für Sperre und Grenzen", "A1": "L3 (keine Abfragen im versteckten Dialog), 22:00 im Knopf sichtbar", "A2": "B0 (BD-02) an der Wurzel, alte Dauer blieb vorausgewählt", "A3": "~6 Abfragen je Welle weniger, 22:00 grau", "A4": "B0, ~6 Abfragen weniger", "A5": "B0, ~6 Abfragen weniger", "A6": "BD-03, BD-04, BD-12, BD-16, BD-09", "A7": "BD-03, BD-04, BD-12, BD-16, BD-09", "A8": "BD-05 „Item Not Found“", "A9": "BD-05 im Tab", "A10": "BD-15, Doppeltipp, Fehler wurde verschluckt", "B1": "BD-01, BD-04, BD-06, BD-07, BD-08, BD-09, BD-11, BD-19, B3, E-4", "B2": "wie B1, dazu Schleife → Sammel-Patch", "C1": "E-1 nur freie Tische, Frage 21", "C2": "Frage 21 (alte Auswahl)", "C3": "Frage 20, BD-27, Abfragen bei geschlossenem Panel", "C4": "wie C3", "C5": "BD-26", "D1": "BD-12", "D2": "BD-10 (U7)", "D3": "Doppeltipp bei Mehrfach-Stornieren", "D4": "BD-25"}

@@ entscheidungen
## 2. Entscheidungen (Vorschlag, du bestätigst oder widersprichst)
| # | Frage | Vorschlag in v2 | Warum | Falls du es anders willst |
|---|---|---|---|---|
| E1 | 22:00 beim Verlängern | **ablehnen**, Plus-Knopf wird grau, wenn er über 22:00 führen würde | Handy-App V5 „nie über 22:00“ (bestätigt), Panel endet schon um 22:00 (belegt) | In A1/A2 `22 * 60` durch `24 * 60` ersetzen und die 22:00-Prüfung in A6/A7 entfernen: Bescheid geben, ich erzeuge es neu |
| E2 | Zwei Tische zur selben Zeit für dieselbe Person (BD-06, Frage 5) | **verhindern** | Handy-App V6 „nein, wird verhindert“ | Prüfung `colNeuIch` in B1/B2 entfernen (eine Zeile, ich erzeuge es neu) |
| E3 | Einchecken-Zeitfenster (BD-15, Frage 8) | **ab 30 Min vor Beginn bis Ende**, Auschecken jederzeit | Handy-App V2. Am PC bleibt Auschecken möglich (der Knopf heißt heute schon so), die Handy-App kennt es nicht (V3) | Arm `!varCheckinBuchung.CheckedIn && (…)` in A10 entfernen |
| E4 | Buchen in der Vergangenheit (BD-19, Frage 7) | **sperren** (vor der laufenden halben Stunde) | Handy-App E-06/A15 | Arm `First(colNeuTermine).Start < varNeuJetzt` entfernen |
| E5 | Big Table in der Panel-Liste | **nicht in der Liste**, über den Grundriss weiter buchbar | Wunsch E-1 und Handy-App V7. Der Grundriss bleibt unverändert, damit nichts wegfällt | Filter `!("big table" in …)` in C1 entfernen |
| E6 | „5 Std“/„9 Std“ an einem anderen Tag | **ab 08:00** (wie die Startliste) | Heute: ab der aktuellen Uhrzeit, an einem anderen Tag sinnlos. Um 07:00 morgens wird der Start „07:00“ gesetzt, den die Liste nicht enthält (Frage 20) | in C3/C4 `8 * 60` anders wählen |
| E7 | Mehrfachauswahl und Serienbuchung | **beide drinlassen** | Mehrfach-Stornieren gemessen 33 Buchungen ~9 s ohne Fehler. Serie gemessen ~4,7 s. v2 sichert beide zusätzlich ab (D3, B1/B2) | `tglAuswahlModus.Visible = false` blendet die Mehrfachauswahl aus |

**K4.2 bleibt verworfen** (geprüft, Begründung aus v1 stimmt): Wer „Wiederholen“ anhakt und das Bis-Datum nicht anfasst, bekäme mit K4.2 still nur eine Buchung. v2 ergänzt eine fehlende Meldung: Liegt das Bis-Datum **vor** dem Startdatum, kommt jetzt „Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum“. Vorher konnte `Sequence` mit negativer Anzahl zu einem Fehler führen (geschlussfolgert).

@@ ablauf
## 3. Ablauf je Schritt (wie bei L2)
1. Vorher: **`.msapp` exportieren** (Datei → Speichern unter → Diesen Computer) und prüfen, dass seit dem Export vom 07.10. in Studio nichts geändert wurde. Wenn doch: neuen Export geben, dann erzeuge ich alles neu (`python3 -I werkzeuge/paket_k_v2.py`). Das Skript bricht ab, wenn ein Anker nicht mehr genau passt.
2. Steuerelement in der Strukturansicht wählen (der Ort steht bei jedem Block) → Property im Formelfeld → **ganze Property ersetzen** → Enter.
3. App-Prüfung (Baseline vor Paket: 134 Einträge, keine Formelfehler). Neue **Formelfehler** = sofort melden, nicht weitermachen. 47 der 134 Einträge sitzen auf Properties, die das Paket ersetzt (vor allem `CountRows`-Warnungen der Dauer-Knöpfe). Nach dem ganzen Paket also etwa **87 plus wenige neue** (möglich bei C1, siehe U-V3). Ist es viel mehr, wurde vermutlich ein Block nicht eingefügt.
4. Kurz testen (Test unter jedem Schritt), im Testbogen abhaken.
5. **Reihenfolge:** Schritt 0 zuerst, danach in Studio **„OnStart ausführen“** (Strukturansicht → App → … → OnStart ausführen), weil Studio OnStart nach dem Einfügen nicht von selbst neu ausführt. Danach A, B, C, D in beliebiger Reihenfolge. Innerhalb eines Schritts alle Properties einfügen, bevor du testest.
6. **Besonderheit `Items.Value` (C1):** Das ist kein Formelfeld. Rechts im Eigenschaftenbereich „Wert“ auf **Anzeige** stellen, nachdem `Items` ersetzt ist.

@@ teil 0
Legt drei Variablen mit Startwert an, ganz am **Anfang** von OnStart (nicht blockierendes OnStart: so früh wie möglich gesetzt). Die L2-Ladezeile bleibt die letzte Anweisung. Die Sperre funktioniert auch ohne Schritt 0 (`IsBlank(varSperreBis)` ist abgefangen). Schritt 0 macht nur die Typen eindeutig und ist deshalb empfohlen.

@@ test 0
**Test:** App-Prüfung ohne neue Fehler. **OnStart ausführen**, dann Vorschau: Grundriss lädt wie bisher.

@@ teil A
**Was sich ändert (belegt am Export):** Heute rechnet jeder Plus-/Minus-Knopf seine Farbe und Bedienbarkeit mit einer eigenen Abfrage `LookUp(Tischbuchungen; ID = varSelectedBuchung.ID)` plus einer Kollisionsabfrage. Das sind 24 Properties, und sie laufen auch bei geschlossenem Dialog. Im Tab lesen sie die falsche Variable (B0). **Neu:** Beim Klick auf „Verwalten“ wird einmal die **Grenze** berechnet. Das ist der Beginn der nächsten Buchung am selben Tisch nach meinem Ende, höchstens 22:00 am Buchungstag. Das ist eine einzige delegierbare Abfrage (`First(Sort(Filter(…)))`). Die Knöpfe vergleichen dann nur noch Zahlen. Das bewertet dasselbe wie heute: Ein Plus-Knopf ist gesperrt genau dann, wenn eine Buchung mit `Startzeit < neues Ende` und `Endzeit > altes Ende` existiert (geschlussfolgert, gleichwertig umgeformt). Dazu kommt die 22:00-Grenze.

**Richtig benannt:** Der Dialog `conVerwaltenDialog` wird **vom Dashboard** geöffnet (`galTischbuchungenHeute > btnVerwalten`), nicht vom Grundriss. Eine Kachel im Grundriss öffnet das Details-Popup (`btnHitArea` → `varZeigeDetails`), belegt. v1 nannte ihn „Grundriss-Dialog“, deshalb war der B3-Test dort nicht ausführbar.

**Weil sich die Daten ändern können, während der Dialog offen ist,** prüft der Speichern-Knopf (A6/A7) **beim Klick** noch einmal frisch am Server. Meldet er „inzwischen belegt“, wird die Grenze auf das alte Ende gesetzt, sodass alle Plus-Knöpfe grau werden. Verkürzen bleibt möglich. Wie in der Handy-App stehen die Werte dabei in globalen Variablen, weil die Handy-App nur so delegierbare Filter bekam (belegt, E-06 Punkt 2).

@@ test A1
**Test:** Dashboard → bei einer heutigen Buchung „Verwalten“: +1/+2/+3 Std sind grün, wenn dahinter frei ist. Ist ein Knopf grau, dann reicht er in eine Folgebuchung oder über 22:00. Monitor (optional): beim Öffnen genau 1 Abfrage auf `Tischbuchungen`.

@@ test A2
**Test:** Tab „Buchungen“ → Buchung A verwalten, +3 wählen, schließen. Buchung B verwalten: **keine** Dauer ist vorausgewählt (vorher blieb +3 stehen). Auswahlmodus an: Klick öffnet wie bisher den kleinen Dialog.

@@ test A3
**Test:** wie A1. Zusätzlich eine Buchung, die um 20:30 endet: +1 grün, +2 grau (würde 22:30).

@@ test A4
**Test (B0):** Im Dashboard Buchung A verwalten, schließen. Im Tab Buchung B verwalten, wobei hinter B direkt jemand gebucht hat: +1 ist **grau**. Vorher richtete sich die Farbe nach A.

@@ test A5
**Test:** Buchung 2 Std lang: −1 grün, −2 und −3 grau.

@@ A6
Ablauf, gleich wie in der Handy-App (`btnVerl1`): Sperre → Buchung frisch laden → keine Dauer (auch `0`, BD-12)? → gelöscht? → würde leer? → über 22:00? → Tisch inzwischen belegt? → speichern in `IfError` → **nachlesen**, ob das neue Ende angekommen ist → Meldung → immer: `Refresh`, Grundriss neu laden, Dauer leeren, Sperre 2 s, Ladeanzeige aus. Der Knopf ist erst bedienbar, wenn eine Dauer gewählt ist.

@@ test A6
**Test:** (1) +1 Std → „Buchung geändert, neues Ende hh:mm Uhr.“, Dialog zu, Dashboard-Karte und Kachel stimmen. (2) **Doppelklick** auf Verlängern → genau +1 Std. (3) Zwei Browser-Tabs: In Tab 2 direkt hinter die Buchung buchen, in Tab 1 (Dialog war schon offen, +1 grün) verlängern → „Der Tisch ist in dieser Zeit inzwischen belegt…“, danach sind die Plus-Knöpfe grau. (4) In Tab 2 die Buchung stornieren, in Tab 1 verlängern → „Diese Buchung gibt es nicht mehr…“, Dialog zu.

@@ A7
Wie A6, für den Tab (`varSelectedBuchungTab`, `varZeigeVerwaltenTab`). Verkürzen läuft über dieselbe Formel (negative Dauer). Weggefallen sind `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus; false)`: Der Tab-Dialog öffnet sich nur außerhalb des Auswahlmodus, dann ist die Auswahl leer. `varMehrfachAuswahlModus` liest niemand (BD-21, belegt).

@@ test A7
**Test:** wie A6 im Tab, dazu −1 Std → „neues Ende …“. Ein Doppelklick auf Speichern verkürzt nur einmal.

@@ A8
Behebt den gemeldeten Fehler „Item Not Found“ (BD-05, geschlussfolgert): Heute löscht der Knopf `Remove(Tischbuchungen; varSelectedBuchung)`, also den Stand vom Öffnen des Dialogs, ohne `IfError`. Neu: frisch laden, löschen in `IfError`, nachlesen.

@@ test A8
**Test:** Dashboard → Verwalten → Stornieren → „Buchung storniert.“, Karte weg, Kachel grün. Zwei-Tab-Test: In Tab 2 stornieren, in Tab 1 noch einmal stornieren → „Diese Buchung gibt es nicht mehr…“ (kein roher Fehler).

@@ test A9
**Test:** wie A8 im Tab.

@@ A10
Einchecken liest frisch, prüft das Fenster (E3), schreibt in `IfError` und liest nach. Die Grundriss-Ladezeile bleibt. Auschecken bleibt jederzeit möglich.

@@ test A10
**Test:** Heutige Buchung, die in mehr als 30 Minuten beginnt → „Einchecken ist erst ab 30 Minuten vor Beginn…“. Laufende Buchung → „Eingecheckt.“, Kachel rot. Noch einmal → „Ausgecheckt.“.

@@ teil B
**Ein Ablauf für beide Knöpfe** (der Buchungsdialog aus dem Grundriss und das Tische-Panel): Sperre → Werte zum Klickzeitpunkt in Variablen → Termine berechnen (wie bisher: Kappung auf Start + 14 Tage, Wochentage). Der unerreichbare Zweig „Taeglich“ entfällt (BD-24, `varWiederholenModus` wird nur auf „Wochentage“ gesetzt, belegt) → Plausibilität mit je eigener Meldung → **eine** Abfrage „Tisch belegt?“ und **eine** „ich schon gebucht?“, beide nur im Zeitraum der Serie (K4.1, delegierbar) → je Termin frei / Tisch belegt / ich belegt → **Sammel-Patch** der freien Termine mit gemeinsamer `SerienID` → `Refresh` → **Nachlese** (dieselbe Zeitraum-Abfrage; das `Refresh` davor stellt sicher, dass sie vom Server kommt und nicht aus dem Zwischenspeicher): Wie viele meiner Zeilen sind wirklich angekommen? Hat jemand mit kleinerer ID gleichzeitig denselben Tisch gebucht (Regel der Handy-App, nimmt nichts automatisch zurück)? → eine Meldung → nur wenn etwas gebucht wurde: Dialog schließen und Eingaben leeren (BD-11).

**Warum `SerienID` jetzt geschrieben wird:** Die Spalte gibt es schon (Text, filterbar, belegt in `DataSources.json`), sie war nur nie befüllt. So lässt sich nach dem Sammel-Patch exakt zählen, was angekommen ist (Frage 14), und eine Serie später gemeinsam finden (E-4). Der Aufräum-Flow wird nicht berührt (geschlussfolgert, er löscht nach Datum).

@@ test B1
**Test:** (1) Grundriss → freie Kachel → Buchen ohne Wiederholen → „Gebucht: OG Desk 5, 08.10., 09:00 bis 10:00 Uhr.“. In SharePoint (Listenansicht „Tischbuchungen“) hat die neue Zeile eine `SerienID`. (2) Serie Mo–Fr, 2 Wochen → „Gebucht: …, 10 Termine ab …“ oder, wenn Tage belegt sind, „8 von 10 Terminen gebucht (…). 2× war der Tisch schon belegt.“. (3) Bis-Datum 4 Wochen → Meldung endet mit „Die Wiederholung wurde auf 2 Wochen begrenzt.“. (4) Zur selben Zeit schon einen anderen Tisch gebucht → „Du hast in dieser Zeit schon einen Tisch gebucht.“, Dialog bleibt offen. (5) Datum gestern → „Diese Zeit liegt in der Vergangenheit…“. (6) **Doppelklick** auf Speichern → nur eine Buchung.

@@ test B2
**Test:** wie B1 über „Tisch Buchen“ im Dashboard. Zusätzlich: Ohne gewählten Tisch ist Speichern grau. Nach dem Speichern springt die Ansicht wie bisher auf das Dashboard.

@@ teil C
**Ablauf im Panel neu: erst Datum und Zeit, dann Tisch.** Die Tischliste rechnet mit denselben Terminen wie der Speichern-Knopf. Dafür holt sie **eine** Abfrage „alle Buchungen der betroffenen Tage“ (ganze Tage vom Startdatum bis zum letzten Serientag). Die Grenzen stehen direkt als Steuerelement-Ausdrücke im Filter, nicht als `With`-Werte, denn das ist laut Messung in der Handy-App die delegierbare Form (APP_WISSEN). Danach wird lokal minutengenau gerechnet. Die Liste zeigt nur Tische, die an **mindestens einem** Termin frei sind. Bei Serien steht dahinter z. B. „(an 2 von 10 Tagen belegt)“. Sortierung: ganz freie zuerst, dann das gerade gewählte Stockwerk, dann nach Nummer (Muster aus der Handy-App, `Desk 2` vor `Desk 10`). Bei geschlossenem Panel fragt die Liste `Tischbuchungen` nicht ab (`Tische` wird aus dem Zwischenspeicher gelesen). Die Liste berücksichtigt nur „Tisch belegt“, nicht „du hast zu der Zeit schon einen Tisch“. Das prüft erst Speichern (E2).

**Sicherheitsnetz (wichtig):** Ändert sich die Zeit, nachdem ein Tisch gewählt wurde, berechnet sich die Liste neu. Ob die klassische Auswahlliste den gewählten Tisch dann behält oder leert, ist UNSICHER (U-C1). Deshalb ist kein Tisch vorausgewählt (`Default` leer, `AllowEmptySelection` an), Speichern ist ohne Tisch grau, die Erfolgsmeldung nennt den Tisch, und Speichern prüft am Server noch einmal. Gebucht wird immer der Tisch, der beim Klick sichtbar gewählt ist. Ein unbemerkter Wechsel ist damit unwahrscheinlich, aber nicht bewiesen (UNSICHER, U-C1).

**Optional, nicht nötig:** Die Tischauswahl im Panel nach unten unter die Zeit ziehen (nur Y-Position), damit die Reihenfolge auf dem Bildschirm der Logik folgt.

@@ test C1
**Test:** (1) Panel öffnen: kein Tisch gewählt, Speichern grau. (2) Morgen 09:00–10:00 (heute beginnt die Startliste erst bei der nächsten halben Stunde): belegte Tische fehlen, Big Table fehlt, Stockwerk des Grundrisses zuerst, `OG Desk 2` vor `OG Desk 10`. (3) Wiederholen Mo–Fr: Tische mit Hinweis „(an x von y Tagen belegt)“ stehen hinten. (4) Zeit ändern, nachdem ein Tisch gewählt war: Wird die Auswahl geleert oder bleibt sie? → im Testbogen notieren (U-C1). (5) App-Prüfung: Warnung bei `ddTischePanel.Items` → **Wortlaut notieren** (U-V3). Eine Warnung an `Tische`/`ForAll` ist erwartet und harmlos. Eine Warnung an `Startzeit`/`Endzeit` heißt, dass die Abfrage nicht delegiert wird: dann melden.

@@ test C2
**Test:** Tisch wählen, Panel schließen (Pfeil „<“), wieder öffnen → kein Tisch gewählt, Datum = Ansichtsdatum.

@@ test C3
**Test:** Panel, Datum morgen → „5 Std“ grün; klicken → Start 08:00, Ende 13:00. Heute nach 17:00 → „5 Std“ grau. Mit gewähltem, ab jetzt belegtem Tisch → grau.

@@ test C4
**Test:** wie C3 mit 9 Std (morgen 08:00–17:00).

@@ test C5
**Test:** Panel → Wiederholen an → Bis-Datum 3 Wochen nach dem Panel-Datum → Text „*Zu weit gewählt …“. Der Text wird rot. Vorher lasen Text und Farbe das Datum aus dem Buchungsdialog, sodass sie sich widersprechen konnten.

@@ test D1
**Test:** Tab „Buchungen“ → Verwalten → +1 wählen, Dialog offen lassen. Tab Dashboard → Stockwerk wechseln → zurück zum Tab: Speichern ist grau (vorher war die Dauer `0`, und Speichern hätte „+0 Minuten“ geschrieben).

@@ test D2
**Test:** Aktualisieren (Dashboard, Buchungen, Kopfzeile, Profil) → „Aktualisiert.“. WLAN aus → **kein** „Aktualisiert.“, dafür die gelbe Warnung „… Bitte erneut auf Aktualisieren tippen.“ (Text leicht geändert). Ein zusätzliches Fehlerbanner von Power Apps ist möglich, weil `Refresh` selbst nicht abgefangen ist (UNSICHER).

@@ test D3
**Test:** Mehrfachauswahl, 2 Buchungen, Doppelklick auf Stornieren → „2 Buchungen storniert.“, keine zweite Meldung „gibt es nicht mehr“.

@@ test D4
**Test:** Panel öffnen und mit „<“ schließen wie bisher.

@@ rueckfall
## Rückfall
- **Ein Schritt:** Original aus Anhang 1 einfügen. Für Properties, die es vorher nicht gab: `DisplayMode` → `DisplayMode.Edit`, `AllowEmptySelection` → `false`, `Default` (ddTischePanel) → Formel leeren, `Items.Value` → wieder `Titel` wählen.
- **Teil A zurück:** A3 bis A5 brauchen die Grenze aus A1/A2. Deshalb Teil A **ganz** zurücknehmen oder ganz behalten. B, C, D sind davon unabhängig.
- **Teil B zurück:** B1/B2 einzeln möglich. Bereits geschriebene `SerienID`-Werte stören nicht.
- **Teil C zurück:** C1 (vier Properties) zusammen zurücknehmen, sonst passt `Items.Value` nicht zu `Items`.
- **Schritt 0** kann jederzeit zurück: Die Sperre fängt ein leeres `varSperreBis` ab.
- **Komplett:** `.msapp`-Export oder Versionsverlauf.

@@ unsicher
## UNSICHER (mit Prüftest)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U-V1 | ~~Leeres `varSperreBis`~~ **erledigt:** Die Sperre prüft `IsBlank(varSperreBis) \|\| Now() >= varSperreBis`. Unsicher war, ob `Now() >= Blank()` wahr ist (Prüfbefund R3) | – | – |
| U-V2 | Die 2-Sekunden-Sperre fängt den eingereihten Zweitklick auch in der **PC**-App (in der Handy-App gemessen, gleiche App-Einstellungen, belegt `Properties.json`) | Doppelte Buchung/Verlängerung bei Doppelklick | Doppelklick-Tests A6, A7, B1 (6), D3 |
| U-V3 | `ddTischePanel.Items`: `ForAll(Tische …)` ist nicht delegierbar (34 Zeilen, harmlos). Ob die Abfrage auf `Tischbuchungen` delegiert wird, ist UNSICHER. Die Grenzen stehen direkt im Filter (Form „ohne Warnung“ laut Handy-App), sind aber mit `If`/`Min`/`DateDiff` zusammengesetzt | Wird nicht delegiert: Die Liste rechnet nur mit den ersten 1.000 Zeilen der ganzen Liste und zeigt belegte Tische als frei. **Speichern prüft trotzdem richtig** | App-Prüfung nach C1: Warnung an `Startzeit`/`Endzeit` in `ddTischePanel.Items`? Dann melden, ich erzeuge eine einfachere Form |
| U-V4 | Datenzeilenlimit: Die App steht auf **1.000** (belegt, `Properties.json`). Bei einer 2-Wochen-Serie holt die Panel-Liste alle Buchungen aller Tische an 15 Tagen, das sind höchstens einige hundert (34 Tische × 15 Tage × wenige Buchungen pro Tag) | Erst bei sehr voller Belegung würde die Liste unvollständig, Speichern prüft trotzdem richtig | keiner nötig. Nur relevant, wenn U-V3 zutrifft |
| U-C1 | Behält die klassische Auswahlliste den gewählten Tisch, wenn sich `Items` neu berechnet? | Nutzer muss den Tisch nach einer Zeitänderung neu wählen (lästig, nicht gefährlich, siehe Sicherheitsnetz in Teil C) | C1-Test (4) |
| U-B1 | `SerienID` wird beim Sammel-Patch mitgeschrieben (Spalte vorhanden, read-write, belegt). Wenn nicht: Nachlese zählt 0 → Meldung „nicht angekommen“, obwohl gebucht ist | falsche rote Meldung. Ein erneuter Klick bucht **nicht** doppelt (Prüfung findet die eigene Buchung) | B1-Test (1): `SerienID` in der Liste gefüllt? |
| U-B2 | `Text(GUID())` liefert Text (App-Einstellung `useguiddatatypes` an, belegt) | rote Formel | App-Prüfung nach B1 |
| U-A1 | Gleichheit `Endzeit = varVerlEndeNeu` in der Nachlese (Muster aus der Handy-App) | falsche Meldung „nicht angekommen“ trotz Erfolg | A6-Test (1) |
| U-A2 | `First(Sort(Filter(…); Startzeit; SortOrder.Ascending))` ist delegierbar (Sort auf DateTime bei SharePoint) | Delegierungswarnung bei A1/A2 | App-Prüfung nach A1 |
| U-B3 | Ein Lesefehler (Netz weg) beim frischen `LookUp` gilt als „gibt es nicht mehr“ (A6–A10), eine gescheiterte Vorprüfung in B1/B2 als „alles frei“. So verhält sich auch die Handy-App. Die Nachlese meldet eine Doppelbuchung dann hinterher | seltene irreführende Meldung | hinnehmen (Prüfbefund H12) |
| U-A3 | Mehrarmiges `If` mit Anweisungsketten in den Zweigen bei `powerfxv1 = false`. In der Handy-App mit denselben Einstellungen in Betrieb (belegt) | rote Formel | App-Prüfung nach A6 |

@@ testbogen
## Testbogen (abhaken, Ergebnis kurz melden)
| | Schritt | Ergebnis | Notiz |
|---|---|---|---|
| ☐ | 0 OnStart | | |
| ☐ | A1–A5 Dauer-Knöpfe Dashboard/Tab (inkl. B0-Test A4) | | |
| ☐ | A6/A7 Verlängern (inkl. Doppelklick, Zwei-Tab) | | |
| ☐ | A8/A9 Stornieren (inkl. Zwei-Tab) | | |
| ☐ | A10 Einchecken (Fenster, Ein/Aus) | | |
| ☐ | B1 Buchungsdialog (Einzel, Serie, Kappung, Person, Vergangenheit, Doppelklick, SerienID) | | |
| ☐ | B2 Panel speichern | | |
| ☐ | C1 Tischliste (frei, sortiert, Big Table, Serienhinweis; U-C1 notieren) | | |
| ☐ | C2–C5 Panel öffnen, 5/9 Std, Hinweistext | | |
| ☐ | D1–D4 Kleinigkeiten | | |
| ☐ | App-Prüfung: Anzahl Einträge vorher 134, nachher ___ (erwartet etwa 87 plus wenige), neue Formelfehler ___ | | |
| ☐ | Monitor (optional): Serie 11 Termine über das Panel, nur diese Aktion | | erwartet deutlich unter 96 `getRows` (keine Abfragen der Dauer-Knöpfe mehr) |

@@ pruefung
## Unabhängige Prüfung
### a) Prüfung von Paket K v1 (Auftrag aus `01_PROMPT_fuer_den_Chat.md`, gegen den Export vom 07.10.)
| # | Frage | Ergebnis | Kennz. |
|---|---|---|---|
| 1 | Passen die Blöcke auf den veröffentlichten Stand? | Ja. Der Python-Leser liest alle 1.994 Properties genauso wie `props_de.json`. Die zehn Abweichungen sind nur Anführungszeichen-Reste des PowerShell-Lesers. L2-Ladezeile in B1, B3, C1, C2 vorhanden, Klammern ok. | belegt |
| 2a | B1/B3 Kollisionsprüfung gleichwertig zu den Plus-Knöpfen? | Ja, wortgleich. | belegt |
| 2b | `varIsLoading` auf jedem Pfad zurück? | Ja, die Zeilen stehen nach dem äußeren `With`. | belegt |
| 2c | Ungenannte Verhaltensänderung / Fehler | **(1)** Mit `varAusgewaehltePlusDauer = 0` (nach Stockwerkwechsel, BD-12) schreibt v1 dasselbe Ende und meldet „Buchung geändert“. **(2)** Im Tab bleibt die zuletzt gewählte Dauer stehen (`btnVerwalten_2` leert sie nicht, das Dashboard schon), v1 behebt das nicht. **(3)** B3-Test „über den Grundriss“ ist nicht ausführbar, der Dialog hängt am Dashboard. | belegt |
| 2d | `Date(…) + Time(22; 0; 0)` (U-K1) | Plausibel, aber unnötig: Die Handy-App rechnet `DateAdd(Startzeit; 22*60 − Minuten des Starts; Minutes)` und ist damit in Betrieb. v2 übernimmt das. | geschlussfolgert |
| 3 | Nebenwirkungen von A1 (K1) | Kein Typkonflikt: Alle Quellen von `varSelectedBuchung` sind Datensätze aus `Tischbuchungen` (Galerien, `LookUp`, `Patch`). Check-in, Details und `conCheckinDialog.Y` bleiben unberührt, weil A1 deren Sichtbarkeit auf falsch setzt. **Lücke:** Bleibt der Tab-Dialog offen, und man verwaltet inzwischen im Dashboard eine andere Buchung, zeigen die Tab-Knöpfe wieder die falsche Buchung. v2 löst B0 deshalb an der Wurzel (Tab liest `varSelectedBuchungTab`). | belegt / geschlussfolgert |
| 4 | K5: hält die DisplayMode-Sperre? | **Nein.** In der Handy-App am 06.10. gemessen: Doppeltipp verlängert zweimal trotz `DisplayMode`. U-K3 aus v1 war berechtigt, und der B2-Test hätte versagt. v2: Zweifach-Sperre wie in der Handy-App (E-07). | belegt (gemessen in der Handy-App) |
| 5 | K4.2 verwerfen? Test-Reihenfolge? | Begründung stimmt. Reihenfolge A vor B ok, nur der B3-Test war falsch (siehe 2c). | belegt |
| 6 | E1/E2/E3 mit den Messdaten | E1 ablehnen: passt (Handy V5). E2 drinlassen: passt (Trace 5 fehlerfrei; v2 sichert den Mehrfach-Knopf zusätzlich gegen Doppelklick ab). E3 drinlassen: passt (Trace 4, ~4,7 s). | gemessen / belegt |
| 7 | Fehlt etwas Wichtiges? | **Ja:** BD-05 („Item Not Found“), BD-06 (zwei Tische zur selben Zeit; die Handy-App verhindert es, die PC-App nicht), BD-19 (Vergangenheit), BD-15 (Check-in-Fenster), unterschiedliche Regeln PC/Handy, Tischauswahl (E-1, Frage 21). v2 baut alles davon ein. | belegt |

**Weitere Funde beim Lesen des ganzen Exports (v2 behebt sie):** `ddStockwerk.OnSelect` setzt die Dauer auf `0` (BD-12). Die vier Aktualisieren-Knöpfe überdecken die Grundriss-Warnung (BD-10). Das Panel liest im Hinweistext das falsche Datum (BD-26). Die Panel-Knöpfe 5/9 Std fragen auch bei geschlossenem Panel ab. `chkAuswahl.X` liest schon `btnVerwalten_2` (**BD-18 ist bereits erledigt**, belegt).

### b) Prüfung von v2
__PRUEFUNG_V2__

@@ spaeter
## Bewusst nicht in diesem Paket
| Vorhaben | Warum nicht jetzt |
|---|---|
| L4 Raumcode stilllegen (BD-22, −36 Abfragen beim Start), tote Variablen (BD-21) | Du musst bestätigen, dass Raumbuchung nicht gebraucht wird (Frage 11) |
| Bestätigung vor dem Stornieren (Handy V8) | braucht ein neues Steuerelement (Dialog), eigenes kleines Paket |
| Vorprüfung mit Alternativtischen für Serien (E-2) | mit C1 ist der größte Teil erreicht: Die Liste zeigt je Tisch, an wie vielen Tagen er belegt ist. Ersatztische je Konflikttag sind ein eigenes Konzept |
| Mehrfach-Verlängern (E-3) | acht Entwürfe verworfen, eigenes Konzept |
| Listen-Galerien (`galTischbuchungenHeute`, `galAlleTischbuchungen`) | fragen bei jedem `Refresh` neu ab (~24 Abfragen je Schreibvorgang). Das ist gewollt, sie zeigen die eigenen Buchungen |
| Buchungen-Tab „manchmal leer“ (D3 in der Gesamtliste, Frage 15) | Ursache nicht aus dem Code ableitbar, braucht einen Trace im Moment des Fehlers |
| Statusfarbe eingecheckt (BD-14) | Grundriss rot = „besetzt“ aus Sicht anderer, Dashboard grün = „du bist eingecheckt“. Beides ist begründbar, kein Fehler |
| `dpWiederholenBis_1.OnChange` ohne Wirkung (BD-23) | harmlos, beim Aufräumen mit L4 |

@@ regeln
## Regeln
Deutsche Schreibweise (`;` trennt, `;;` verkettet), keine Kommentare, immer die **ganze** Property ersetzen, ein Studio-Fenster, nach jedem Schritt App-Prüfung. Die zwei Speichern-, Verlängern- und Stornieren-Knöpfe sind **nicht** wortgleich: jeden einzeln einfügen. Neu erzeugen nach einem neuen Export: `python3 -I werkzeuge/paket_k_v2.py && python3 -I werkzeuge/doc_paket_k_v2.py`.
