# ENTSCHEIDUNGEN.md — Architektur- und Fachentscheidungen

**Kurzfassung:** Jede Entscheidung steht hier mit den Optionen, die ich hatte, meiner Wahl, dem Grund und, sobald ein Prüf-Subagent sie angegriffen hat, seinem Fazit. Bisher stehen zwei Entscheidungen fest: Die Handy-App wird eine **neue App**, keine Kopie, und das mehrdeutige Abnahmekriterium A09 wird so ausgelegt, dass die Statusfarbe der Buchungskarte dem Check-in-Zustand folgt. Beides ist unten begründet. Entscheidungen, die eigentlich Josias treffen müsste, stehen zusätzlich in `FRAGEN_AN_JOSIAS.md`.

---

## E-01 — Neue App statt Kopie der Desktop-App

**Optionen laut Auftrag Abschnitt 3:** neue Canvas-App, Kopie der bestehenden App („Speichern unter") und abspecken, oder ein anderer Weg.

**Wahl: neue Canvas-App.**

**Grund.** Die Desktop-App ist nach Maß für Tablet gebaut, und zwar auf eine Weise, die sich nicht abspecken lässt:
- `primaryFormFactor: Tablet`, Designgröße 1366 × 768, Querformat
- 14 der 14 `GroupContainer` haben `Variant: ManualLayout`, also absolute Kindpositionen
- 176 `X`- und 174 `Y`-Properties mit absoluten Koordinaten, viele davon verketten sich (`btnPlus2Std.X = btnPlus1Std.X + btnPlus1Std.Width + 10`)
- Der Grundriss hängt an fest einprogrammierten Pixelkoordinaten (`colTischPositionen`, `colTischPositionenUG`) und einer Referenzskalierung (`BasisSkalierungReferenz`)

Von 186 Steuerelementen braucht die Handy-App etwa 15. Eine Kopie bedeutet: 171 Steuerelemente löschen, wobei jede Löschung die Koordinatenketten der verbleibenden bricht, und zusätzlich den toten Raumcode (21 Steuerelemente mit Verhaltensformel) und Befund B0 mitschleppen. Das ist mehr Arbeit als ein Neubau und erzeugt genau die Fehlerkaskaden, vor denen Abschnitt 5.2 warnt.

Hinzu kommt: Beim Neubau kann ich für das Layout responsive Container verwenden statt `ManualLayout`. Das ist am Handy die Voraussetzung dafür, dass 390 × 844 und 360 × 800 beide ohne horizontales Scrollen funktionieren (A03).

**Was ich aus der Desktop-App übernehme:** die Logik, nicht die Steuerelemente. Überschneidungsformel, Schreibschemata für Person und Tisch, Farbwerte, 22:00-Grenze, 30-Minuten-Raster. Alles steht in `APP_WISSEN.md` unter „Geteilte Regeln".

**Prüferfazit:** steht aus.

---

## E-A09 — Auslegung des Abnahmekriteriums A09

**Das Kriterium lautet:** „Status je Karte stimmt mit der Grundriss-Logik der Desktop-App überein (gleiche Buchung, gleicher Zeitpunkt, gleiches Ergebnis)."

**Das Problem.** In der Desktop-App gibt es **zwei verschiedene** Statuslogiken, und sie widersprechen sich.

*Grundriss* (`Gallery1.Rectangle1.Fill`, Z. 66 bis 85) ist ein **Tisch**-Status mit drei Ausgängen:

| Lage | Farbe |
|---|---|
| keine Buchung im Fenster „jetzt bis +30 Min" | grün `#00A96B` |
| Buchung vorhanden und `CheckedIn` | rot `#EB3951` |
| Buchung vorhanden, nicht eingecheckt | orange `#FFA500` |

*Dashboard-Karte* (`lblStatusHeute`, Z. 440 bis 449) ist ein **Buchungs**-Status mit zwei Ausgängen:

| Lage | Text | Farbe |
|---|---|---|
| `CheckedIn` | „Eingecheckt" | grün `#00A96B` |
| nicht eingecheckt | „Einchecken" | orange `#FFA500` |

**Eingecheckt ist im Grundriss rot und auf der Karte grün.** Beide Logiken stehen gleichzeitig in der App.

Die Handy-App zeigt Karten für die eigenen Buchungen. Eine solche Karte kann niemals „frei" sein — die Buchung existiert ja. Der dritte Ausgang des Grundrisses ist dort also unerreichbar, und eine wörtliche Übernahme der Grundriss-Logik ist nicht möglich.

**Meine Auslegung:**
- **Farbe und Text folgen dem Check-in-Zustand**, wie auf der Dashboard-Karte: eingecheckt grün „Eingecheckt", sonst orange. Grün bedeutet am Handy „alles erledigt", und das ist die Lesart, die ein Nutzer auf einer Karte erwartet.
- **Das 30-Minuten-Fenster des Grundrisses bleibt erhalten**, aber an der Stelle, an der es gehört: Es entscheidet, ob der Einchecken-Tipp aktiv ist (Vorgabe V2 sagt dasselbe: ab 30 Minuten vor Start bis Ende).
- **Der Vergleichstest zu A09** prüft deshalb das, was wirklich vergleichbar ist: Für dieselbe Buchung zum selben Zeitpunkt muss der Check-in-Zustand in beiden Apps gleich sein, und das Zeitfenster, in dem Einchecken möglich ist, muss dieselben Grenzen haben wie das Fenster, in dem der Grundriss die Buchung als „relevant" ansieht.

**Warum nicht die Grundriss-Farben übernehmen:** Dann wäre eine eingecheckte eigene Buchung am Handy rot. Rot heißt in dieser App sonst „belegt" oder „Fehler". Ein Nutzer, der gerade erfolgreich eingecheckt hat, bekäme ein Warnsignal. Das wäre eine Verschlechterung ohne Gegenwert.

**Das ist eine Abweichung vom Wortlaut des Kriteriums**, deshalb steht sie als Frage in `FRAGEN_AN_JOSIAS.md` (F-02). Bis Josias entscheidet, gilt die Auslegung oben.

**Prüferfazit:** steht aus.

---

## E-02 — Schreibweg für neue Buchungen

**Optionen:** `Patch(Tischbuchungen; Defaults(Tischbuchungen); {…})` für einen Datensatz, oder der Sammel-`Patch` mit Tabelle, den die Desktop-App seit dem 05.10. in `btnSpeichern` benutzt.

**Wahl: `Patch` mit `Defaults` für genau einen Datensatz.**

**Grund.** Die Handy-App legt immer nur eine Buchung an (keine Serienbuchung, Abschnitt 2.4). Der Sammel-`Patch` bringt hier keinen Vorteil und trägt ein ungeklärtes Risiko: Ob er `Person` und `Tisch` korrekt schreibt, ist in diesem Projekt ausdrücklich offen (Ü6, Briefing Frage 2) und ungemessen. Der Weg über `Defaults` ist der in der Desktop-App seit Monaten belegte; `Defaults()` bringt die Spaltentypen mit, die ein Satzliteral allein verliert.

**Prüferfazit:** steht aus.

---

## E-04 — A03 ist in Power Apps nicht vollständig erfüllbar: Zielkonflikt zwischen „Scale to fit aus" und „Ausrichtung gesperrt"

**Das Kriterium lautet:** „Hochformat, *Scale to fit* aus, Ausrichtung gesperrt; die App füllt in der Geräteemulation 390 × 844 und 360 × 800 die Breite ohne horizontales Scrollen."

**Der Befund.** In den App-Einstellungen unter „Anzeige" gibt es ein Feld **App-Layout** mit genau zwei Werten:

| Wert | Bedeutung | Ausrichtung | Seitenverhältnis sperren | Ausrichtung sperren |
|---|---|---|---|---|
| **Fest** | „Es wird durch Vergrößern und Verkleinern an den Bildschirm angepasst" — das **ist** Scale to fit | wählbar | wählbar | wählbar |
| **Dynamisch** | „Es passt sich automatisch an die Bildschirmgröße an" — Scale to fit **aus** | ausgegraut | ausgegraut, steht auf Aus | **ausgegraut, steht auf Aus** |

Die drei Schalter „Ausrichtung", „Seitenverhältnis sperren" und „Ausrichtung sperren" gehören zum festen Layout. Sobald das Layout dynamisch ist, sind sie deaktiviert — in einer dynamischen App gibt es nichts zu sperren, weil sich das Layout ohnehin an jede Größe anpasst.

**Damit schließen sich „Scale to fit aus" und „Ausrichtung gesperrt" gegenseitig aus.** Beides zugleich ist in einer Canvas-App nicht einstellbar.

**Meine Wahl: App-Layout „Dynamisch", Ausrichtungssperre nicht gesetzt.**

**Grund.** Der eigentliche Zweck von A03 steht im zweiten Halbsatz: Die App soll bei 390 × 844 **und** 360 × 800 die Breite füllen, ohne horizontal zu scrollen. Das leistet nur das dynamische Layout. Mit festem Layout würde die App auf eine Designgröße gezeichnet und auf jedem anderen Gerät proportional skaliert — bei zwei verschiedenen Seitenverhältnissen entstehen dann Ränder oder Verzerrung. Die Formulierung „Scale to fit aus" im Kriterium zeigt, dass genau das vermieden werden soll.

**Was ich stattdessen tue, damit das Querformat nicht hässlich wird:** Das Layout ist über einen vertikalen Auto-Layout-Container aufgebaut und bleibt auch im Querformat benutzbar; es wird dann nur gestaucht und scrollbar. Niemand wird daran gehindert, das Handy zu drehen, aber nichts bricht dabei.

**Belegt** durch die Einstellungsseite der App am 06.10.2026, Screenshot `screenshots\A03_anzeige_dynamisch_ausrichtung_gesperrt_deaktiviert.jpg`.

**Das ist eine Abweichung vom Wortlaut des Kriteriums**, deshalb steht sie als Frage in `FRAGEN_AN_JOSIAS.md` (F-13). In `FEATURES.json` bleibt A03 so lange auf `false`, bis die beiden Emulationstests mit Screenshots vorliegen; die Teilabweichung ist dort im Beleg vermerkt.

---

## E-05 — Eingaben im Bereich „Buchen"

**Datum als Auswahlliste statt Kalender.** `ddDatum` bietet heute und die nächsten 59 Tage an. *Grund:* Vergangene Tage sind gar nicht erst wählbar (A15 „Vergangenheit" wird schon in der Eingabe verhindert), die Liste ist am Handy mit einem Daumen bedienbar, und sie verhält sich in allen Browsern gleich. Der klassische Datumswähler öffnet einen kleinen Kalender, der bei verdoppeltem Koordinatensystem schwer zu treffen ist. *Grenze:* weiter als 60 Tage im Voraus kann man am Handy nicht buchen; am Desktop schon. **UNGETESTET**, ob jemand das braucht → J3.

**Start heute ab der laufenden halben Stunde, nicht ab der nächsten.** Die Desktop-App rundet auf (`RoundUp`): Um 16:21 ist dort 16:30 die früheste Startzeit. Am Handy bucht man typischerweise „jetzt, hier". Deshalb rundet die Handy-App ab: um 16:21 ist 16:00 wählbar. Der Buchen-Knopf lehnt nur Startzeiten ab, die **vor** der laufenden halben Stunde liegen. *Folge:* Eine Handy-Buchung kann bis zu 29 Minuten in der Vergangenheit beginnen. Das ist harmlos (die Überschneidungsprüfung arbeitet mit denselben Zeiten), weicht aber von der Desktop-App ab.

**Ende mit 17:00 vorbelegt statt Schnellwahlknopf (V9).** Liegt der Start vor 17:00, steht „Bis" auf 17:00, sonst auf Start + 30 Minuten. Das deckt den häufigsten Fall „bis Feierabend" ohne einen weiteren Knopf und ohne jede zusätzliche Abfrage — die Desktop-Schnellwahlknöpfe kosten je zwei `CountRows` (BD-27).

**An anderen Tagen ab 08:00**, wie in der Desktop-App.

---

## E-06 — Der Buchen-Knopf: Prüfreihenfolge und Doppelbuchungsschutz

Vollständige Formel in `yaml\conBuchen.yaml` (`btnBuchen.OnSelect`). Ablauf:

1. `varIsLoading` an → Knopf und alle Auswahllisten gesperrt, Lade-Overlay über allem (D3).
2. Alle Werte **zum Klickzeitpunkt** in globale Variablen (`varBuchStart`, `varBuchEnde`, `varTischName`, `varTischID`). Globale Variablen, weil nur sie im Filterprädikat delegierbar aufgelöst werden.
3. Plausibilität (A15): Pflichtangaben, Ende nach Beginn, nicht vor der laufenden halben Stunde, nicht nach 22:00. Jede mit eigener deutscher Meldung.
4. **D1/D2:** frische Abfrage `LookUp(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart)`. Die Tischliste kann veraltet sein; diese Abfrage nicht.
5. **D5:** `LookUp(Tischbuchungen, Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart)` → „Du hast in dieser Zeit schon einen Tisch gebucht."
6. `Patch(Tischbuchungen, Defaults(Tischbuchungen), {Tisch: {Id, Value}, Startzeit, Endzeit, Person: {Claims, Department, DisplayName, Email, JobTitle, Picture}})` in `IfError` (E-02, Schema aus `APP_WISSEN.md` Abschnitt 3).
7. **D8 Nachlese:** `ClearCollect(colKollision, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart))`. Darin muss die eigene Zeile mit genau dieser Person, Start- und Endzeit stehen. Fehlt sie: „Die Buchung ist nicht angekommen."
8. **D7:** Steht in `colKollision` eine Zeile mit **kleinerer ID** als die eigene, hat jemand anderes zwischen Schritt 4 und Schritt 6 denselben Tisch gebucht. Die App meldet das deutlich als Fehler und bittet, die eigene Buchung zu stornieren. **Sie nimmt nichts automatisch zurück** (F-12).
9. Erst jetzt „Gebucht: …" und Wechsel zu „Heute" bzw. „Meine".
10. `varNeuLaden` hochzählen, `varIsLoading` aus — auf jedem Pfad, weil beides **nach** dem gesamten `If` steht (A29).

**Warum Schritt 7 und 8 eine einzige Abfrage sind:** Die naheliegende Form `LookUp(…, ID < varBuchungID)` ist beim SharePoint-Konnektor nicht delegierbar (an `ID` nur `=`), ebenso die Gleichheit auf `Startzeit`. Die Studio-Prüfung hat beides als Delegierungswarnung gemeldet. Eine delegierbare Abfrage mit Zeitgrenze holt die wenigen Zeilen dieses Tisches im Zeitraum, der Rest läuft lokal. Das ist zugleich schneller.

**Ehrliche Bewertung von D7.** Der Schutz **erkennt** eine gleichzeitige Doppelbuchung, er **verhindert** sie nicht. SharePoint kennt keine Transaktionen, und eine Canvas-App kann nicht sperren. Das Zeitfenster zwischen Schritt 4 und 6 ist ein bis zwei Sekunden. Wer in dieser Lücke als Zweiter schreibt, bekommt eine rote Meldung; wer als Erster geschrieben hat, merkt nichts und behält seinen Tisch (die Regel „niedrigere ID gewinnt"). Für den Zweiten gibt es zwei Lücken: Er könnte die Meldung übersehen, und die Desktop-App des Ersten zeigt die Doppelbuchung nicht an. Eine automatische Rücknahme würde die erste Lücke schließen, hat aber im Projekt schon einmal Schaden angerichtet (Entwurf 2B). **Entscheidung bei Josias (F-12).**

**Was der Erste nicht prüft:** Bucht jemand **nach** mir denselben Tisch über die Desktop-App, erkennt nur die Desktop-App das — und deren Kollisionsprüfung hat Befund BD-01 (keine Zeitgrenze). Das liegt außerhalb der Handy-App.

---

## E-07 — Sperre gegen eingereihte Zweit-Tipps (D3)

**Befund (BELEGT, 06.10.2026 16:31):** `DisplayMode: If(varIsLoading, Disabled, Edit)` allein schützt nicht. Ein schneller zweiter Tipp wird eingereiht und läuft nach dem ersten. Gemessen: Doppeltipp auf „+1 Std" hat zweimal verlängert.

**Lösung:** Jeder schreibende Handler beginnt mit `If(!varIsLoading && Now() >= varSperreBis, …` und setzt am Ende `varSperreBis = DateAdd(Now(), 2, TimeUnit.Seconds)`. Zwei Schichten: `varIsLoading` fängt einen gleichzeitig laufenden zweiten Aufruf, `varSperreBis` den eingereihten, der erst nach dem Ende des ersten startet.

**Warum zwei Sekunden:** Ein eingereihter Tipp startet Millisekunden nach dem Ende des ersten. Zwei Sekunden reichen mit großem Abstand und sind kurz genug, dass niemand eine bewusst wiederholte Aktion als blockiert empfindet. Ein Tipp in der Sperrzeit tut nichts und meldet nichts — das ist beim Doppeltipp genau richtig; der Nutzer sieht ja die Meldung des ersten.

**Verworfen:** eine Prüfung „Dialog noch offen?" je Knopf. Hätte beim Buchen nicht gegriffen (der Bereich bleibt sichtbar, bis umgeschaltet wird) und wäre je Knopf verschieden gewesen.

---

## Verworfene Ansätze

Noch keine. Hier landet alles, was dreimal gescheitert ist, damit es niemand erneut versucht.
