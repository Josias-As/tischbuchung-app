# „Für andere buchen“ + weicher Hinweis: Diagnose und Fragen (26.10.2026)

Grundlage: Desktop-Export **25.10. 20:09** (`quellen/2026-10-25_Desktop/`), Auftrag `quellen/2026-10-26_FuerAndere/Prompt_Analyse-Chat_Buchung_fuer_andere_2026-10-26.md`. Noch keine Formeln.

## 1. Diagnose (belegt aus dem Export)

**Eine Zählung „2 Buchungen“ gibt es im Export nicht.**
- Die heutige Regel heißt „**kein zweiter Tisch zur selben Zeit**“. Sie prüft Überschneidung mit eigenen Buchungen, nicht die Anzahl.
- Wer am selben Tag zu verschiedenen Zeiten bucht, kann beliebig viele Tische buchen.
- Zwei Aussagen im Auftrag stimmen deshalb nicht mit dem Export überein:
  - „Wer schon 2 Tische gebucht hat …“: Diese Prüfung gibt es nicht.
  - „Die Desktop-App prüft das nicht (zwei Tische gleichzeitig)“: Sie prüft es, siehe Tabelle.

| Wo | Was | Wirkung heute |
|---|---|---|
| `btnSpeichern.OnSelect` (Buchungsdialog aus dem Grundriss) und `btnSpeichernTischePanel.OnSelect` (Panel „Tisch buchen“) | `ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart))`, dann verfallene lokal raus (`RemoveIf`). Je Termin `Grund = "ich"`, wenn er eine eigene Buchung überschneidet | **harte Sperre je Termin:** Einzelbuchung „Du hast in dieser Zeit schon einen Tisch gebucht.“, bei einer Serie werden diese Termine still übersprungen („… hattest du zu der Zeit schon einen Tisch“) |
| `btnVerlängern.OnSelect` (Dashboard) und `btnVerlängern_1.OnSelect` (Tab) | `colVerlIch` mit derselben Bedingung für die Verlängerung | harte Sperre: „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“ |
| Handy-App (`btnBuchen`, `btnVerl1`, `btnVerl2`, Export 12.10.) | dieselbe Regel | harte Sperre |

**Speichernde Knöpfe:**
- Buchen: nur `btnSpeichern` und `btnSpeichernTischePanel`. Beide decken Einzel- und Serienbuchung ab (`varWiederholen`, 2-Wochen-Deckel). Sie speichern mit einem Sammel-Patch.
- Außerdem schreiben `btnEinchecken`, `btnVerlängern` und `btnVerlängern_1` (Patch) sowie `btnStornieren`, `btnStornieren_1` und `btnStornierenKlein` (Remove).
- Eine **„Mehrfachauswahl-Buchung“ gibt es nicht.** Die Mehrfachauswahl im Tab „Buchungen“ ist nur zum Stornieren da (`btnStornierenKlein`) und ist von der Änderung nicht betroffen.

**Hier steht heute der Buchende:**
- Details-Popup der Kachel: `lblPerson.Text = varSelectedBuchung.Person.DisplayName`. Das ist ein frisch gelesener ganzer Datensatz, Gastname ist dort ohne neue Abfrage lesbar.
- Kachel-Kürzel: `Label1.Text` aus `colGrundriss.Name`. Das kommt aus der Ladezeile `Name: B.Person.DisplayName`, die an **17 Stellen** zeichengleich steht.
- „My personal desk“ (`galTischbuchungenHeute`) und der Tab „Buchungen“ (`galAlleTischbuchungen`) zeigen nur eigene Buchungen (`Person.Email = User().Email`), aber ohne Namen. Gast-Buchungen erscheinen dort automatisch beim Buchenden. Die Verwalten-Dialoge zeigen keinen Namen.

**Weitere Befunde:**
- **Delegation:** `IsBlank(GastName)` ist im SharePoint-Filter nicht delegierbar. Deshalb bleibt der Server-Filter unverändert, Gast-Buchungen werden lokal per `RemoveIf` herausgenommen (gleiches Muster wie die Freigabe). Tagesgrenzen als benannte Formeln braucht es dafür nicht.
- **Spaltennamen im Export:** `Tisch`, `Person`, `Startzeit`, `Endzeit`, `CheckedIn`, `SerienID`, `Titel`, `Erstellt`. `GastName` kommt neu. Kein Konflikt.
- **Axel Krägelius / Norman Horn:** stehen nirgends im Export. Bekannt ist nur: NHN ist der Dienstleister der GoBright-Gateways, IT-Admin ist Michael (`CLAUDE.md`).
- **Nächtlicher Lösch-Flow:** ist nicht im Export. Laut Betriebshandbuch filtert er nur nach `Endzeit` (älter als 7 Tage). Eine neue optionale Textspalte ändert daran nichts (geschlussfolgert). **Prüfen:** nach dem Anlegen den nächsten Lauf im Ausführungsverlauf ansehen.
- **Handy-App ist mittelbar betroffen:** Gast-Buchungen gehören dem Buchenden (`Person`). Die Handy-App zählt sie als eigene. Wer am PC für einen Gast bucht, kann am Handy zur selben Zeit nichts für sich buchen und die Gast-Buchung dort nicht verlängern, wenn er zur selben Zeit selbst gebucht hat (geschlussfolgert aus der Handy-Regel).

## 2. Plan (vorläufig, nach deinen Antworten)
1. Du legst `GastName` an und aktualisierst die Datenquelle.
2. **Bedienelemente:**
   - Im Buchungsdialog `tglFuerAndere` und `txtGastName`, im Panel `tglFuerAnderePanel` und `txtGastNamePanel`. Es braucht zwei Paare, weil es zwei Speichern-Wege gibt.
   - Ein gemeinsamer Hinweisdialog direkt in `Screen1`: Vollbild-Hintergrund `btnFbHintergrund`, `conFbHinweis`, `lblFbHinweis`, `btnFbTrotzdem`, `btnFbAbbrechen`.
   - Alle neuen Variablen beginnen mit `varFb…`.
3. **Beide Speichern-Knöpfe:**
   - Gastname Pflicht, wenn der Schalter an ist.
   - Bei Gast-Buchung keine „ich“-Prüfung.
   - Eigene Prüfung ohne Gast-Buchungen.
   - Statt Sperre öffnet der Hinweisdialog. „Trotzdem buchen“ führt denselben Knopf noch einmal aus, mit `varFbTrotzdem`. Die Speicherlogik steht also nicht doppelt da.
   - Patch mit `GastName`. `IfError` und Nachlese sind schon da.
4. **Verlängern (beide):** Gast-Buchungen zählen nicht als „anderer Tisch“. Eine Gast-Buchung wird ohne diese Prüfung verlängert.
5. **Anzeige:** Gastname plus „gebucht von <Buchender>“ im Details-Popup, in „My personal desk“, im Tab „Buchungen“ und in beiden Verwalten-Dialogen. Altbestand (`GastName` leer) zeigt genau den heutigen Text.
6. **Zurücksetzen** beider Schalter und Textfelder beim Öffnen von Dialog und Panel und beim Schließen per Etage, Datum, Tab und Abbrechen.
7. Testbogen als Zeitachse, Rückfall je Property.

Geschätzt 25–35 Properties und 9 neue Steuerelemente, maschinell aus dem Export erzeugt.

## 3. Fragen (bitte gebündelt beantworten)
1. **Welche Regel soll weich werden?**
   - (A) Die vorhandene „kein zweiter Tisch zur selben Zeit“ wird zum Dialog „Trotzdem buchen / Abbrechen“. **Meine Empfehlung**, weil es sie gibt und sie beim Buchen und Verlängern greift.
   - (B) Eine **neue** Regel „ab 2 eigenen Buchungen am Tag“ mit Dialog. Die gibt es heute nicht, das wäre eine zusätzliche Hürde.
2. **Einchecken bei Gästen:** Ein Gast kann nicht einchecken, weil er kein Konto hat. Ohne Check-in wird jede Buchung nach 30 Min freigegeben, auch die des Gasts.
   - (a) Der Buchende checkt für den Gast ein, in seiner Liste. Kein Code nötig. **Meine Empfehlung**, solange Gäste selten sind.
   - (b) Gast-Buchungen gelten beim Speichern als eingecheckt (`CheckedIn = Ja`). Sie werden nie freigegeben, auch wenn der Gast nicht kommt.
   - (c) Gast-Buchungen von der Freigabe ausnehmen. Das ist ein großer Umbau: Ladezeile an 17 Stellen und alle Prüfungen.
3. **Grundriss:**
   - Gastname im Details-Popup: ohne Abfrage machbar, **empfohlen**.
   - Auf der Kachel die Gast-Kürzel statt der des Buchenden? Das braucht die Ladezeile an 17 Stellen. **Empfehlung: nein**, die Kachel zeigt weiter den Buchenden.
4. **Serien für Gäste:**
   - Dieselben Regeln (Mo–Fr, 2 Wochen, Tisch frei) und **keine** „ich“-Prüfung? **Empfehlung: ja.**
5. **Axel Krägelius / Norman Horn:**
   - In welchem Hinweistext sollen sie stehen, und wofür sind sie Ansprechpartner?
   - Für einen Buchungshinweis sind IT-Admins ungewöhnlich, fachlich bist eher du zuständig. Der Export gibt keinen Hinweis auf die beiden.
6. **Handy-App:** Ist dir die Folge oben recht (Gast-Buchungen blockieren am Handy den Buchenden zur selben Zeit), bis die Handy-App angepasst ist?
