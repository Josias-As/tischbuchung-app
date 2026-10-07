# 06 — Konzept: Vorprüfung mit Alternativtischen

**Kurzfassung:** Heute speichert die Serienbuchung sofort, überspringt belegte Tage still und meldet am Ende nur eine Zahl. Gewünscht ist: erst prüfen, dann bei Konflikten ein Fenster mit Alternativtischen je Konflikttag anbieten, nicht buchbare Tage verwerfen lassen und erst dann speichern freigeben. Diese Datei beschreibt das Konzept und nennt die **technischen Anker im vorhandenen Quellcode** — welche Steuerelemente, Variablen und Collections betroffen sind, wo die Prüfung andocken muss und welche Fallen gelten. **Fertige Formeln stehen hier bewusst nicht**; die schreibt der nächste Claude.

---

## 1. Der gewünschte Ablauf (Vorgabe von Josias, 06.10.2026)

1. Der Nutzer wählt wie heute Tisch, Datum, Uhrzeit und Wiederholung.
2. **Zuerst kommt eine Prüfung**, nicht das Speichern. Der Knopf heißt zum Beispiel „Verfügbarkeit prüfen". Er ermittelt alle Termine der Serie und prüft für jeden Termin, ob der gewählte Tisch zu dieser Uhrzeit frei ist.
3. **Alles frei:** Der Speichern-Knopf wird freigegeben.
4. **Nicht alles frei:** Ein Fenster geht auf. Es nennt jeden Konflikttag („Am Mi 14.10. ist OG Desk 5 von 08:00 bis 12:00 schon belegt") und bietet für genau diesen Tag und diese Uhrzeit die **Alternativtische an, die dann frei sind**. Der Nutzer kann pro Tag einen Alternativtisch wählen.
5. Im Fenster gibt es einen Knopf **„Nicht buchbare Tage verwerfen"**. Er entfernt alle Konflikttage, für die keine Alternative gewählt wurde.
6. **Erst dann kann gespeichert werden:** Speichern ist gesperrt, bis jeder Konflikttag entweder einen Alternativtisch hat oder verworfen ist.
7. Ein Abbrechen-Knopf schließt das Fenster ohne Speichern.

### Entscheidungen von Josias (gelten als Vorgabe)

1. **Reihenfolge der Alternativtische:** zuerst freie Tische im **selben Geschoss**, sortiert nach Nähe zum gewünschten Tisch (Abstand aus den Koordinaten in `colTischPositionen` / `colTischPositionenUG`). Danach freie Tische im **anderen Geschoss**, sichtbar abgesetzt (zum Beispiel „UG – anderes Geschoss").
2. **Ein Ersatztisch für alle Konflikttage:** Es gibt einen Knopf „Diesen Ersatztisch für alle Konflikttage". Als Vorschlag erscheint der Tisch, der an den meisten Konflikttagen frei ist. Pro Tag bleibt eine abweichende Wahl möglich.
3. **„Big Table" wird nicht als Alternative angeboten.**
4. **Tage ohne jeden freien Tisch** zeigen „kein Tisch frei" und können nur verworfen werden.
5. **Eine Serie darf über mehrere Tische laufen.** Alle Termine einer Serie bekommen dieselbe `SerienID`, egal an welchem Tisch. Daraus folgt:
   - Die `SerienID` darf nirgends an den Tisch gekoppelt werden. Eine Nachlese nach dem Speichern filtert auf `SerienID` und Person, **nicht** zusätzlich auf den Tisch (sonst werden Termine am Ersatztisch als „nicht gespeichert" gemeldet).
   - Die Prüfung lädt die Belegung **aller** Tische im Serienzeitraum, nicht nur des gewählten Tisches.
   - Beim Speichern wird jeder Termin mit **seinem** Tisch erneut geprüft, das Ergebnis wird pro Tag gemeldet.
   - Spätere Funktionen wie „ganze Serie stornieren" müssen mit gemischten Tischen umgehen können.

---

## 2. Die technischen Anker im Quellcode

### 2.1 Beide Speichern-Wege

Die Prüfung muss an **zwei** Stellen andocken. Sie sind im Rechenteil wortgleich, im Aufräumteil nicht (Ü8).

| | Grundriss-Dialog | Tische-Panel |
|---|---|---|
| Container | `conBuchungDialog` (Z. 2535) | `conTischBuchungenPanel` (Z. 787) |
| Speichern-Knopf | `btnSpeichern` (Z. 2716) | `btnSpeichernTischePanel` (Z. 948) |
| Stand | Sammel-`Patch` mit `IfError` | alter `ForAll`-mit-`Patch`, ohne `IfError` |
| Tischquelle | `varSelectedTisch.ID` / `.Titel` | `ddTischePanel.Selected.ID` / `.Titel` |
| Datum | `dpDatum` | `dpDatumTischePanel` |
| Start / Ende | `ddStart` / `ddEnde` | `ddStartTischePanel` / `ddEndTischePanel` |
| Wiederholen-bis | `dpWiederholenBis` | `dpWiederholenBis_1` |
| Wiederholen-Haken | `chkWiederholen` (hat `Default`) | `chkWiederholenPanel` (kein `Default`, braucht `Reset`) |
| Wochentags-Schalter | `tglTagMo` … `tglTagFr` (mit `Default`) | `tglTagMo_1` … `tglTagFr_1` (ohne `Default`) |
| Aufräumblock | 12 Anweisungen (Z. 2828–2839) | 22 Anweisungen (Z. 1048–1069) |

**Geteilte Variablen beider Wege:** `varWiederholen`, `varWiederholenModus`, `varTagMo` bis `varTagSo`, `varIsLoading`. Eine Prüf-Collection, die beide Wege benutzen, muss daher entweder geteilt werden **oder** zwei Namen bekommen — mit einem geteilten Namen kann ein in einem Dialog erzeugtes Prüfergebnis im anderen Dialog weiterleben.

### 2.2 Geschoss und Tischpositionen

- `Tische.Geschoss` ist ein **Nachschlagefeld** mit den Unterfeldern `Id` und `Value` (`04_DATENQUELLEN.md`). Im Code steht überall `Geschoss.Value`.
- `varAusgewaehltesStockwerk` enthält `"OG"` oder `"UG"` (gesetzt in `App.OnStart` und `ddStockwerk.OnChange`).
- `Gallery1.Items: =Filter(Tische, Geschoss.Value = varAusgewaehltesStockwerk)` — nur dieses Geschoss. **Für die Alternativensuche reicht das nicht**, sie braucht beide Geschosse.
- Die Koordinaten für die Nähe-Sortierung stehen **nicht** in SharePoint, sondern fest einprogrammiert in `App.OnStart`:
  - `colTischPositionen` — 16 OG-Tische, Spalten `Tisch` (Text, entspricht `Tische.Titel`), `X`, `Y`, `Ausrichtung`
  - `colTischPositionenUG` — 18 UG-Tische, gleiche Spalten; enthält `{Tisch: "Big Table", X: 1254, Y: 630, Ausrichtung: "BigTable"}`
  - Die Liste `Tische` hat zwar eigene Spalten `X`, `Y`, `Ausrichtung`, `Ausrichtung2` — die App liest sie nicht.
- **„Big Table" ausschließen** geht damit über den Titel (`Tisch <> "Big Table"` bzw. `Titel <> "Big Table"`), nicht über ein Kennzeichen in der Liste. Es gibt keine Spalte, die „buchbar" markiert.
- **Der Abstand** lässt sich aus den Koordinaten derselben Collection rechnen. Innerhalb eines Geschosses sind die Koordinaten vergleichbar; zwischen OG und UG sind sie es nicht (zwei verschiedene Grundrissbilder). Das passt zur Vorgabe: Nähe nur im selben Geschoss sortieren, das andere Geschoss abgesetzt anhängen.
- Die drei „Quiet Desk"-Tische werden im Grundriss schmaler gezeichnet (`- If(StartsWith(ThisItem.Titel, "Quiet Desk"), 10, 0)`), sind aber normal buchbar. **Offene Frage:** ob sie als Alternative angeboten werden sollen (siehe `07_OFFENE_FRAGEN.md`).

### 2.3 Wie heute geprüft wird und warum das nicht reicht

Heute, in beiden Speichern-Knöpfen:

```powerfx
bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)
```

und je Termin:

```powerfx
CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0)))) = 0
```

Drei Punkte:
- Die Abfrage hat **keine Zeitgrenze** und lädt alle Buchungen des Tisches bis zum Datenzeilenlimit (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`). Das ist K4.1, nicht eingebaut.
- Sie lädt nur **einen** Tisch. Die Alternativensuche braucht alle.
- Das Überlappungsmuster `Startzeit < neuEnde && Endzeit > neuStart` ist das richtige und sollte übernommen werden. Es ist nach der Delegationstabelle delegierbar (`<`/`>` auf DateTime).

### 2.4 Die eine delegierbare Abfrage für den ganzen Zeitraum

Vorgabe aus der Aufgabe: Belegung **einmal** laden, dann lokal rechnen. Dafür zwei Datumsgrenzen vorher in Variablen legen (sonst steht der Ausdruck im Prädikat und bricht die Delegation):

```text
Startzeit < zeitraumEnde && Endzeit > zeitraumBeginn
```

Das ist nach der Doku delegierbar. Kein `Tisch.Value`-Filter, damit alle Tische kommen. Die Liste `Tische` ist klein (34 Einträge laut `colTischPositionen` plus `colTischPositionenUG`; die tatsächliche Zeilenzahl in SharePoint ist nicht geprüft, **UNSICHER**), die kann komplett geladen werden.

**Nicht benutzen:** `IsBlank` im Prädikat, `!`/`Not`, `ID <>`, Personenfelder außer `Email`/`DisplayName` — alle nicht delegierbar (`04_DATENQUELLEN.md`).

### 2.5 Eigene Buchungen sind kein fremder Konflikt

`Tischbuchungen.Person` ist eine Personenspalte; `Person.Email` ist delegierbar. Eine geladene Belegungstabelle enthält also auch die eigenen Buchungen. Zwei Fälle, die auseinandergehalten werden müssen:
- **Eigene Buchung am gewünschten Tisch zur gewünschten Zeit:** der Termin ist bereits gebucht, nicht „belegt". Der Tag gehört in eine eigene Kategorie („schon gebucht"), nicht in die Konfliktliste.
- **Eigene Buchung an einem anderen Tisch zur selben Zeit:** der Nutzer hätte zwei Tische zugleich. Fachliche Entscheidung, siehe `07_OFFENE_FRAGEN.md`.

Das ist zugleich die Lehre aus dem verworfenen Entwurf 2A: Nach einem Teilausfall fand der Neuversuch die eigenen bereits geschriebenen Zeilen und meldete sie als fremde Kollision.

### 2.6 Die `SerienID`

`Tischbuchungen.SerienID` ist eine Textspalte, les-, schreib- und filterbar, und wird **in der ganzen App nicht benutzt**. Sie ist die Zutat für die Nachlese nach dem Speichern (Ü1).

Zwei Fallen aus dem Verwurfsprotokoll:
- `Set(varSerienID; GUID())` erzeugt einen Typkonflikt zu `Set(varSerienID; "")` in `OnStart`. Richtig ist `Text(GUID())`.
- Die `SerienID` darf nicht in einer globalen Variablen zwischengelagert werden, die ein zweiter Klick überschreibt (Ü7). Sie gehört in einen `With`-Local des Knopfes oder in eine Collection-Spalte.

### 2.7 Lade-Overlay und Doppelklick

- `conLadeOverlay` (Z. 4341) ist bildschirmfüllend und hängt an `varIsLoading`. `varIsLoading` muss auf **jedem** Pfad zurückgesetzt werden, auch im Fehler- und im Abbruchzweig (Falle aus 1B/2C: Dort landete `Set(varIsLoading; false)` im Erfolgszweig, die App blieb bis zum Neustart gesperrt).
- Kein Knopf der App hat heute eine `DisplayMode`-Sperre gegen Doppelklick (K5 nicht eingebaut, Ü4). Der neue Prüf-Knopf und der neue Speichern-Knopf brauchen sie.
- `Screen1.LoadingSpinner = LoadingSpinner.Data` (Z. 13) zeigt zusätzlich den eingebauten Spinner. Doppelte Anzeige, bekannt.

---

## 3. Skizze der Bausteine

Keine Formeln, nur die Teile und was sie halten müssen.

### 3.1 Collections

| Name (Vorschlag) | Inhalt | gefüllt von | gelesen von |
|---|---|---|---|
| `colBelegung` | alle Buchungen im Serienzeitraum, alle Tische; Spalten mindestens `ID`, `Tisch.Value`, `Startzeit`, `Endzeit`, `Person.Email` | Prüf-Knopf, **eine** delegierbare Abfrage | die lokale Konfliktrechnung |
| `colSerienTermine` | ein Satz je Termin: `Datum`, `Startzeit`, `Endzeit`, `TischTitel`, `TischId`, `Status` (`frei` / `konflikt` / `ersetzt` / `verworfen` / `schonGebucht`) | Prüf-Knopf; der Nutzer ändert `TischTitel`/`Status` über die Auswahl | Konfliktliste, Speichern-Freigabe, Speichern |
| `colAlternativen` | je Konflikttag die freien Tische: `Datum`, `TischTitel`, `Geschoss`, `Abstand`, `Rang` | Prüf-Knopf (lokal aus `colBelegung`, `Tische`, `colTischPositionen*`) | die Auswahlgalerie im Fenster |
| `colErgebnis` | nach dem Speichern: je Termin `Datum`, `TischTitel`, `Status` aus dem **tatsächlichen** Schreibergebnis | Speichern-Knopf (Nachlese über `SerienID` + Person) | die Ergebnisanzeige |

Die bestehenden Collections (`colAusgewaehlteBuchungen`, `colStornoFrisch`, `colStornoZiele`, `colTischPositionen`, `colTischPositionenUG`) bleiben unberührt. Namen dürfen sich nicht überschneiden.

### 3.2 Variablen

| Name (Vorschlag) | Zweck |
|---|---|
| `varPruefungGueltig` | `true` nur zwischen erfolgreicher Prüfung und der nächsten Eingabeänderung. Steuert `DisplayMode` des Speichern-Knopfes. |
| `varZeigeKonflikte` | `Visible` des neuen Konflikt-Containers |
| `varErsatzVorschlag` | der Tisch für „Diesen Ersatztisch für alle Konflikttage" |

**Wichtig:** `varPruefungGueltig` muss von **jedem** Steuerelement auf `false` gesetzt werden, das die Eingabe ändert. Das sind pro Weg: Datum, Start, Ende, Wiederholen-Haken, Wiederholen-bis, die fünf Wochentags-Schalter und die Tischwahl. Im Tische-Panel zusätzlich `btn5Std` und `btn9Std`, die über `varStartOverridePanel`/`varEndeOverridePanel` die Zeiten ändern. Im Grundriss zusätzlich `btnHitArea` (Tischwechsel über `varSelectedTisch`) und `ddStockwerk.OnSelect` (setzt `varSelectedTisch` auf `Blank()`). Das sind je Weg etwa zehn bis zwölf Steuerelemente — wird eines vergessen, kann mit veraltetem Prüfergebnis gespeichert werden.

### 3.3 Steuerelemente

Pro Weg (also zweimal, siehe Ü8):
- **„Verfügbarkeit prüfen"**: neuer Knopf im Dialog. `DisplayMode` gegen Doppelklick (`varIsLoading`).
- **Speichern**: der vorhandene Knopf (`btnSpeichern` bzw. `btnSpeichernTischePanel`) bekommt eine `DisplayMode`-Formel, die `varPruefungGueltig` und `varIsLoading` liest, und eine neue `OnSelect`-Formel mit der zweiten Prüfung.

Einmal, gemeinsam nutzbar:
- **Konflikt-Container** (wie `conVerwaltenKlein` aufgebaut: `GroupContainer@1.5.0`, `Variant: ManualLayout`, `Visible` an einer Variablen, abgerundete Ecken mit `RadiusTopLeft` usw.).
- **Galerie der Konflikttage** mit `Items: =Filter(colSerienTermine; Status = "konflikt")` (sinngemäß). Je Zeile: Datum, Uhrzeit, Hinweistext, ein Dropdown oder eine Untergalerie mit den Alternativen dieses Tages.
- **Knopf „Diesen Ersatztisch für alle Konflikttage"**.
- **Knopf „Nicht buchbare Tage verwerfen"**.
- **Knopf „Abbrechen"**.

**Achtung bei Galerien:** `galAlleTischbuchungen.AllItems` liefert nur die geladenen Zeilen (Fehler A.3, nicht behoben). Für Entscheidungen „alle Konflikte haben eine Alternative" darf nicht `AllItems` gezählt werden, sondern die Collection selbst.

### 3.4 Der Ablauf im Speichern-Knopf

1. `Set(varIsLoading; true)` als Erstes, `DisplayMode` sperrt den Knopf.
2. Belegung für den Serienzeitraum **erneut** laden (eine delegierbare Abfrage, siehe 2.4). Zwischen Prüfung und Speichern können Minuten liegen.
3. Jeden Termin aus `colSerienTermine` mit **seinem** Tisch erneut prüfen (Serien dürfen über mehrere Tische laufen).
4. Eine `SerienID` erzeugen (`Text(GUID())`, in einem `With`-Local) und in **jeden** Datensatz schreiben.
5. Schreiben. Ob ein Sammel-`Patch` oder ein `Patch` je Zeile besser ist, ist offen (siehe Abschnitt 4).
6. **Nachlese:** `Filter(Tischbuchungen; SerienID = … && Person.Email = User().Email)` — ohne Tischfilter. Daraus `colErgebnis` je Tag füllen.
7. Ergebnis **pro Tag zeigen**, nicht als Zahl melden. Der Dialog bleibt bei Fehlern offen.
8. `Set(varIsLoading; false)` auf jedem Pfad.

---

## 4. Die Fallen, die gelten

### Aus `BRIEFING_Mehrfachspeichern.md` (Ü1 bis Ü8)

| | Falle | Was das Konzept dagegen tut |
|---|---|---|
| **Ü1** | Teilerfolg wird als Totalausfall gemeldet; die Zahl tatsächlich geschriebener Zeilen wird nie ermittelt | Nachlese über `SerienID` und Person, Ergebnis **pro Tag** aus `colErgebnis`, keine gezählte Gesamtmeldung |
| **Ü2** | Der Aufräumblock läuft unbedingt, auch im Fehlerfall | Nur im Erfolgszweig aufräumen; `varIsLoading` auf **jedem** Pfad zurücksetzen |
| **Ü3** | Ein gelöschter Datensatz bekommt eine falsche Begründung | Statuswerte unterscheiden `konflikt`, `schonGebucht`, `verworfen`, `fehler` |
| **Ü4** | Doppelklick erzeugt zwei widersprüchliche Meldungen | `DisplayMode` an Prüf- und Speichern-Knopf; heute hat **kein** Knopf der App eine solche Sperre |
| **Ü5** | Sammelaufruf spart gegen SharePoint vermutlich keine Aufrufe (nicht gemessen) | Die Prüfung macht **eine** Abfrage statt vieler — das ist der sichere Gewinn. Beim Schreiben bleibt die Frage offen, siehe unten |
| **Ü6** | `Collect` aus Satzliteralen verliert die Spaltentypen; `Person` und `Tisch` brauchen eventuell `'@odata.type'` | Vor dem Bau klären. Der einzige Beleg in dieser App: `btnSpeichernRaumPanel` (toter Raumcode) schreibt `'@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser"` mit, die Tischbuchungs-Knöpfe nicht |
| **Ü7** | Zustand in globalen Variablen macht Knöpfe mehrfachaufruf-unsicher | `SerienID` in einen `With`-Local; die Collections werden zu Beginn jedes Laufs geleert |
| **Ü8** | Die zwei Speichern-Knöpfe sind im Rechenteil gleich, im Aufräumteil nicht | Jede Änderung zweimal einbauen, Mapping-Tabelle in 2.1 benutzen, nie die ganze Formel kopieren |

### Aus `VERWORFEN_SPEICHERN.md` und dem Verwurfsprotokoll

- **Nicht zerlegen in Löschen und Neuanlegen** (1D): In einem System ohne Transaktionen ist das immer ein Rückschritt; die ID ändert sich, `CheckedIn` geht verloren.
- **Die Serie bleibt eine Zeile je Termin** (2D): Eine Wiederholungsregel in einer Zeile ist nicht delegierbar; Einzel-Storno und Check-in wären nicht mehr möglich. Die Serie wird über die `SerienID` zusammengehalten.
- **Kein stilles Sicherheitsnetz** (2B): Eine Rücknahme-Automatik („niedrigste ID gewinnt") kann gültige Buchungen löschen und rechtfertigt eine Erfolgsmeldung, die sonst niemand gegeben hätte. Lieber ehrlich melden, was offen blieb.
- **Keine Zielzeit statt Delta** (1C): gilt für das Verlängern, nicht für dieses Konzept, aber dieselbe Lehre: Unterschiede zwischen Zeilen nicht plätten.
- **Alles-oder-nichts nicht versprechen** (2C): Der Schreibvorgang ist nicht atomar. Der Name darf keine Atomizität behaupten, die es nicht gibt.

### Aus den Regeln des Projekts

- Deutsche Locale in Studio: `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet.
- Keine Kommentare in Power Fx.
- `With()`-Felder werden gleichzeitig ausgewertet; abhängige Werte brauchen verschachtelte `With` (so macht es der heutige Code mit `effektivesBisRoh` → `effektivesBis` → `anzahlTage` → `alleDatumsWerte` → `datumsListe`).
- Nachschlagefeld immer `{Id: …; Value: …}`, Personenfeld mit vollem Schema.
- `Patch` auf frisch gelesenem `LookUp(…; ID = …)`, nicht auf eine Variable.
- Eine Variable nie mit zwei Record-Typen befüllen.
- `Set(var; false)` setzt eine Checkbox nicht zurück: zusätzlich `Reset(control)`. Im Tische-Panel gilt das für `chkWiederholenPanel` und die fünf Toggles, im Buchungsdialog nicht (die haben `Default`).
- Mehrarmiges `If(bed1; erg1; bed2; erg2; …)` kommt im heutigen Quellcode **nirgends** vor. `powerfxv1` ist `False`. Ob die Form hier akzeptiert wird, ist ungeprüft; im Zweifel verschachtelte zweiarmige `If`.
- Änderungen immer als **vollständige** Ersatzformel für die ganze Property liefern, nie als Teilstück (es gab schon einen Einfügeunfall).

---

## 5. Was vor dem Bau gemessen oder entschieden werden muss

1. **Monitor-Messung** (entscheidet Ü5): Serie mit 1, 5 und 14 Tagen speichern, im Power-Apps-Monitor die Schreibaufrufe zählen, Dauer je Eintrag, Status (429?), nacheinander oder gleichzeitig. Einmal mit dem heutigen Sammel-`Patch` in `btnSpeichern`, einmal mit dem `ForAll`-`Patch` in `btnSpeichernTischePanel` — die beiden Knöpfe sind gerade der perfekte A/B-Vergleich.
2. **Schreibt der Sammel-`Patch` `Person` und `Tisch` korrekt?** Eine Serienbuchung speichern und prüfen, ob die Einträge unter „Meine Buchungen" auftauchen (die Ansichten filtern auf `Person.Email = User().Email`). Wenn nicht: `'@odata.type'` ergänzen wie im Raumcode.
3. **Die fachlichen Fragen aus `07_OFFENE_FRAGEN.md`**, vor allem: Gilt die Vorprüfung auch für die Einzelbuchung, und was zeigt das Fenster über fremde Buchungen.

## 6. Reihenfolge des Einbaus (Vorschlag)

1. `btnSpeichernTischePanel` auf den Stand von `btnSpeichern` bringen (Sammel-`Patch` mit `IfError`), damit beide Wege gleich sind. Vorher Monitor messen.
2. K4.1 und K4.2 in beiden Knöpfen (Zeitgrenze, `>` statt `<>`) — kleine, unabhängige Korrekturen, die die Prüfung ohnehin braucht.
3. K5 (`DisplayMode` mit `varIsLoading`) an beiden Speichern-Knöpfen.
4. `SerienID` schreiben und die Nachlese einbauen, noch ohne Alternativen-Fenster. Damit ist Ü1 gelöst und die Meldung ehrlich.
5. Prüf-Knopf und `varPruefungGueltig` einbauen, zunächst ohne Alternativen: Speichern bleibt gesperrt, bis geprüft wurde.
6. Das Alternativen-Fenster. Erst hier wird es umfangreich.

K1 (eine Zeile, behebt Befund B0) und A.4 sind von diesem Konzept unabhängig und sollten vorher erledigt werden, weil sie den einzigen belegten stillen Doppelbuchungsweg schließen.
