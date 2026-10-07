# APP_WISSEN.md — Was ich über die Desktop-App weiß

**Kurzfassung:** Diese Datei ist mein Gedächtnis. Alles hier stammt aus dem Quellcode des Exports vom 06.10.2026 (Appstand 05.10.2026), nicht aus älterer Dokumentation. Sie enthält die Datenquellen mit internen Spaltennamen, die Schreibschemata für Person und Nachschlagefeld, die Status- und Kollisionslogik, die wiederverwendbaren Formeln und die Fallen, die mich sonst Zeit kosten. Was ich nicht belegen kann, steht als UNSICHER da. Wenn mein Kontext komprimiert wurde, lese ich diese Datei zuerst.

**Quelle für alles hier:** `C:\tischbuchung_work\UEBERGABE_2026-10-06\src\Src\App.pa.yaml` und `Screen1.pa.yaml`. Zeilenangaben beziehen sich auf `Screen1.pa.yaml`, sofern nicht anders vermerkt. Die vollständige Dokumentation liegt in `C:\tischbuchung_work\UEBERGABE_2026-10-06\` (01 bis 07 plus VERIFIKATION).

---

## 1. Umgebung und Identität

| | |
|---|---|
| Produktive App | „Tischbuchung", ID `d247d18b-d36f-4a44-975a-7839695b2f12` |
| Klone, nicht anfassen | „App", „App – Kopie" |
| Umgebung | Personal Productivity (Standardumgebung des Tenants) |
| SharePoint-Site | `https://technoformgroup.sharepoint.com/sites/IMSKonzept` |
| Verbindung | `shared_sharepointonline`, Standard-Tarif (kein Premium) |
| Go-Live Desktop | 14.10.2026 |

**Wichtig:** Die App-ID `d247d18b-…` kommt in **keinem** Exportpaket vor. Ein Exportpaket enthält die Portal-App-ID nicht. Die IDs im Paket sind andere: `3d782261-…` (Manifest-Ressource), `1516988942138200528` (Ordner), `e61d887c-84cf-4e0b-839c-79dbc3c333f8` (`Id`/`FileID` in `Properties.json`). Wer prüfen will, ob er die richtige App exportiert hat, prüft Name, Umgebung, Ersteller und Inhalt — nicht die ID.

**App-Einstellungen der Desktop-App** (aus `src/Properties.json`):
- `DocumentLayoutWidth: 1366`, `DocumentLayoutHeight: 768`, `DocumentLayoutOrientation: "landscape"`
- `DocumentLayoutScaleToFit: false`, `DocumentLayoutLockOrientation: false`
- `primaryFormFactor: Tablet` (aus der App-JSON des Pakets)
- `DefaultConnectedDataSourceMaxGetRowsCount: 1000` ← **das ist das Datenzeilenlimit**, nicht 2000. Das Briefing sagte 2000, der Export sagt 1000. Es gilt der Export.
- `powerfxv1: false`
- `usedisplaynamemetadata: true` ← deshalb funktionieren Anzeigenamen wie `Titel` und `CheckedIn` in Formeln
- `ParserErrorCount: 1`, `BindingErrorCount: 0`

---

## 2. Datenquellen und Spalten

Vier SharePoint-Listen sind verbunden. Die Handy-App braucht nur `Tischbuchungen` und `Tische`. `Räume` und `Raumbuchungen` gehören zu totem Code.

### `Tischbuchungen` (Tabellen-ID `76791681-4416-481c-81a7-9dd8c2f1bded`)

| interner Name | Anzeigename | Typ | Hinweis |
|---|---|---|---|
| `ID` | ID | integer, schreibgeschützt | Delegation: **nur `=`**, kein `<>` |
| `Title` | **`Titel`** | string | Anzeigename benutzen |
| `Tisch` | Tisch | object `{Id, Value, @odata.type}` | Nachschlagefeld auf `Tische` |
| `Tisch#Id` | Tisch Id | integer, schreibgeschützt | Begleitspalte, nicht direkt benutzen |
| `Startzeit` | Startzeit | date-time | |
| `Endzeit` | Endzeit | date-time | |
| `SerienID` | SerienID | string | existiert, wird in der Desktop-App **nirgends** benutzt |
| `Checkedin` | **`CheckedIn`** | boolean | interner Name mit kleinem i, Anzeigename mit großem I. **Die App schreibt `CheckedIn`.** Flows müssen `Checkedin` nehmen. |
| `Person` | Person | object | Personenfeld, Unterfelder `Claims`, `DisplayName`, `Email`, `Picture`, `Department`, `JobTitle`, `@odata.type` |
| `Person#Claims` | Person Claims | string, schreibgeschützt | Begleitspalte |

### `Tische` (Tabellen-ID `2616c57d-887d-4d28-8188-6736c3ac21e9`)

| interner Name | Anzeigename | Typ | Hinweis |
|---|---|---|---|
| `ID` | ID | integer, schreibgeschützt | |
| `Title` | **`Titel`** | string | der Tischname, z. B. „OG Desk 5" |
| `Geschoss` | Geschoss | object `{Id, Value, @odata.type}` | Werte `"OG"` / `"UG"`. Lesen über `Geschoss.Value`. |
| `Geschoss#Id` | Geschoss Id | integer, schreibgeschützt | |
| `Ausrichtung`, `Ausrichtung2` | | object `{Id, Value, @odata.type}` | von der App **nicht** gelesen |
| `X`, `Y` | | number | von der App **nicht** gelesen (Koordinaten stehen fest im Code) |

**Es gibt kein `Aktiv` und kein `Standort`.** Es gibt keine Spalte, die einen Tisch als „nicht buchbar" markiert — „Big Table" muss über den Titel ausgeschlossen werden.

**UNSICHER:** Ob `Geschoss` technisch eine Auswahl (Choice) oder ein Nachschlagefeld (Lookup) ist, lässt sich aus dem Export nicht entscheiden; beide erscheinen im SharePoint-Konnektor als `{Id, Value}` mit `@odata.type`. Für reines Lesen (`Geschoss.Value`) ist das egal. Die Handy-App schreibt `Geschoss` nicht.

**BELEGT (06.10.2026, 16:15):** `Tische` hat **34 Zeilen** — 16 im OG (OG Desk 1–13, Quiet Desk 1–3), 18 im UG (UG Desk 1–17, „Big Table"). Gemessen über `colTische` im Variablenbereich des Studios und über die Tischauswahl der Handy-App. Der Titel lautet exakt „Big Table".

### Die drei Namensfallen in einem Satz

`Titel` statt `Title` (Anzeigename), `CheckedIn` statt `Checkedin` (Anzeigename), `Geschoss` statt `Standort`, und `Aktiv` gibt es nicht.

---

## 3. Schreibschemata (wortgetreu aus dem Quellcode)

### Personenfeld

So schreibt die Desktop-App es in `btnSpeichern` (Z. 2780) und `btnSpeichernTischePanel` (Z. 1013), **ohne** `@odata.type`:

```
Person: {
  Claims: "i:0#.f|membership|" & Lower(User().Email),
  Department: "",
  DisplayName: User().FullName,
  Email: User().Email,
  JobTitle: "",
  Picture: ""
}
```

**Die einzige Stelle mit `@odata.type`** ist `btnSpeichernRaumPanel` im toten Raumcode (Z. 2305):

```
Person: {
  '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
  Claims: "i:0#.f|membership|" & Lower(User().Email),
  DisplayName: User().FullName,
  Email: User().Email,
  JobTitle: "",
  Department: "",
  Picture: ""
}
```

**Offen (Ü6):** Ob die Variante ohne `@odata.type` beim Schreiben über `Patch(Quelle; Tabelle; Tabelle)` zuverlässig funktioniert, ist ungemessen. Bei `Patch(Quelle; Defaults(Quelle); {…})` ist sie in der Desktop-App im Einsatz. **Für die Handy-App:** Ich schreibe mit `Patch(Tischbuchungen; Defaults(Tischbuchungen); {…})`, einen Datensatz auf einmal — das ist der in dieser App belegte Weg. Danach immer P4-Nachlese.

### Nachschlagefeld Tisch

```
Tisch: {Id: <Tische-ID>, Value: <Tische-Titel>}
```

Belegt in Z. 2777 (`{Id: varSelectedTisch.ID, Value: varSelectedTisch.Titel}`) und Z. 1010 (`{Id: ddTischePanel.Selected.ID, Value: ddTischePanel.Selected.Titel}`).

---

## 4. Geteilte Regeln (müssen in Handy- und Desktop-App gleich sein)

### Überschneidung zweier Zeiträume

```
Startzeit < neuesEnde && Endzeit > neuerStart
```

Belegt: `btnSpeichern` Z. 2772, `btnSpeichernTischePanel` Z. 1006, alle Plus-Knöpfe. Berührende Grenzen (Ende A = Start B) sind **keine** Überschneidung. Delegierbar (`<`/`>` auf DateTime).

### Status eines Tisches „jetzt" (Grundriss `Rectangle1.Fill`, Z. 66)

```
relevanteBuchung:
  If(
    varAnsichtsDatum = Today(),
    LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
    LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
  )
```

Farbe danach: `IsBlank(relevanteBuchung)` → grün `#00A96B`; sonst `relevanteBuchung.CheckedIn` → rot `#EB3951`; sonst orange `#FFA500`.

**Das ist ein Tisch-Status mit drei Ausgängen.** Eine Buchungskarte in der Handy-App kann nie „frei" sein. Siehe `ENTSCHEIDUNGEN.md`, E-A09.

### Status auf der Desktop-Dashboard-Karte (`lblStatusHeute`, Z. 440)

```
Text:  =If(ThisItem.CheckedIn, "Eingecheckt", "Einchecken")
Color: =If(ThisItem.CheckedIn, ColorValue("#00A96B"), ColorValue("#FFA500"))
```

**Achtung, das widerspricht dem Grundriss:** Hier ist eingecheckt **grün**, im Grundriss ist eingecheckt **rot**. Beide Logiken existieren nebeneinander in der Desktop-App. Notiert in `BEFUNDE_DESKTOP.md`.

### Zeiten

- Tagesende **22:00**: `minutenEnde: 22 * 60` in `ddStart.Items` (Z. 2657) und `ddStartTischePanel.Items` (Z. 873)
- Raster **30 Minuten**: `Sequence(…)` mit `Value * 30` in allen Zeit-Dropdowns
- Startzeit heute: auf 30 Minuten aufgerundet ab jetzt — `30 * RoundUp(minutenJetzt / 30, 0)`; an anderen Tagen ab `8 * 60`
- Standard-Endzeit: Start + 30 Minuten (`ddEnde.Default`, Z. 2683)
- Keine eigene Zeitzonenkorrektur. Power Apps rechnet beim `Patch` lokal nach UTC um.

### Farben

| Zweck | Wert |
|---|---|
| Technoform-Blau (Leitfarbe) | `#171496` |
| frei / Erfolg | `#00A96B` |
| fällig / Warnung | `#FFA500` |
| belegt / eingecheckt / Fehler | `#EB3951` |
| Schrift | `Font.'Open Sans'` |

---

## 5. Delegation bei SharePoint (Microsoft Learn, belegt)

| Was | delegierbar |
|---|---|
| `=` auf Text, Nachschlage-`Value`, Zahl, DateTime | ja |
| `<`, `<=`, `>`, `>=` auf DateTime | ja |
| Vergleiche auf Zahl | ja, **auf `ID` nur `=`** |
| `IsBlank` im Filterprädikat | **nein** |
| `Not` / `!` | **nein** |
| Personenspalte | nur `Email` und `DisplayName` |
| `Today()` | wird als Konstante gesendet, blockiert nicht |

**Geschlussfolgert, nicht in der Doku belegt:** `CountRows(Filter(…))` schickt den inneren Filter an den Server und zählt lokal.

### Gemessen: Womit man `ID = …` vergleicht, entscheidet über die Delegierbarkeit

**BELEGT** am 06.10.2026 an der Handy-App, Studio-App-Prüfung.

Diese Form erzeugt **zwei Delegierungswarnungen**:

```powerfx
With(
  { frisch: LookUp(Tischbuchungen, ID = ThisItem.ID) },
  ... LookUp(Tischbuchungen, ID = frisch.ID) ...
)
```

Wortlaut der Warnung: „Der hervorgehobene Teil dieser Formel funktioniert möglicherweise nicht ordnungsgemäß mit der Spalte ‚frisch.ID' in großen Datasets."

Diese Form erzeugt **keine Warnung**:

```powerfx
Set(varBuchungID, ThisItem.ID);
With(
  { frisch: LookUp(Tischbuchungen, ID = varBuchungID) },
  ... LookUp(Tischbuchungen, ID = varBuchungID) ...
)
```

### Gemessen: `CountRows` ist bei SharePoint nicht delegierbar

**BELEGT** am 06.10.2026, Wortlaut der Studio-App-Prüfung:

> „Der Vorgang ‚CountRows' wird durch diesen Connector nicht unterstützt."

Das gilt **unabhängig davon, wie delegierbar der innere `Filter` ist.** Die Form `CountRows(Filter(Tischbuchungen, …)) > 0` erzeugt immer eine Delegationswarnung.

**Ersatz für die Frage „gibt es mindestens einen Treffer?":**

```powerfx
!IsBlank(LookUp(Tischbuchungen, <Prädikat>).ID)
```

`LookUp` wird an den Server delegiert und liefert höchstens einen Datensatz; `IsBlank` läuft danach lokal auf diesem einen Datensatz. Das ist etwas anderes als `IsBlank` **im** Filterprädikat, was tatsächlich nicht delegierbar ist (die frühere Behauptung im Briefing, Abschnitt 12, hat diese beiden Fälle vermischt). **Nach dem Ersatz verschwand die Warnung vollständig.**

**Das erklärt die 56 Delegationswarnungen der Desktop-App:** Sie stehen laut Briefing alle auf `CountRows(Filter(...))` in den Verlängern- und Dauer-Knöpfen. Siehe `BEFUNDE_DESKTOP.md` BD-27.

**Regel:** Die rechte Seite eines Filterprädikats muss ein Wert sein, den Power Apps vor dem Absenden auflösen kann — eine globale Variable, ein Steuerelementwert, eine Konstante. Ein Feld aus einem `With`-Local, das selbst aus einem `LookUp` auf dieselbe Datenquelle stammt, kann es nicht. Deshalb die ID **vorher** in eine einfache Variable legen. Genau das macht die Desktop-App schon (`LookUp(Tischbuchungen; ID = varSelectedBuchung.ID)`), nur ohne dass dort jemand den Grund notiert hätte.

**Datenzeilenlimit: 1000** (Export). Was darüber hinausgeht, fällt stillschweigend weg — das ist der Grund für D1.

---

## 6. Wiederverwendbare Formelbausteine

### Eigene kommende Buchungen (Desktop `galAlleTischbuchungen.Items`, Z. 3464)

```
SortByColumns(
  Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()),
  "Startzeit",
  SortOrder.Ascending
)
```

Beide Bedingungen sind delegierbar. **Trotzdem zeigt Studio hier ein Delegationsdreieck** — Ursache ungeklärt (verdächtig: `SortByColumns` auf gefilterter Tabelle). Für die Handy-App beobachten.

### Eigene Buchungen eines Tages (Desktop `galTischbuchungenHeute.Items`, Z. 363)

```
Filter(
  Tischbuchungen,
  Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
)
```

### Zeitliste im 30-Minuten-Raster (Desktop `ddStart.Items`, Z. 2646)

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) },
  With(
    {
      minutenStart: If(dpDatum.SelectedDate = Today(), 30 * RoundUp(minutenJetzt / 30, 0), 8 * 60),
      minutenEnde: 22 * 60
    },
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30, 0) + 1, 0),
      With({ m: minutenStart + Value * 30 }, { Value: Text(Time(RoundDown(m / 60, 0), Mod(m, 60), 0), "hh:mm") })
    )
  )
)
```

### Datum und Uhrzeit zu einem Zeitstempel verbinden (Desktop Z. 2731)

```
dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value, 2)), Value(Mid(ddStart.Selected.Value, 4, 2)), 0)
```

### Initialen des Nutzers (Desktop `lblInitialen`, Z. 4309)

```
With(
  { teile: Split(User().FullName, " ") },
  Upper(Left(First(teile).Value, 1) & Left(Last(teile).Value, 1))
)
```

### Freie Tische in einem Zeitraum (für die Handy-App neu, Muster)

Eine delegierbare Abfrage über **alle** Tische, dann lokal gegenrechnen. `Tische` ist klein (ca. 34):

```
Filter(Tischbuchungen, Startzeit < <ende> && Endzeit > <start>)
```

Kein `Tisch.Value`-Filter, damit alle Tische kommen. Die Zeitgrenzen vorher in Variablen legen, nicht als Ausdruck ins Prädikat.

---

## 7. Fallen aus der Desktop-App (alle belegt)

| # | Falle | Fundstelle |
|---|---|---|
| F1 | Kollisionsabfrage **ohne Zeitgrenze**: `Filter(Tischbuchungen, Tisch.Value = …)` lädt alles bis zum Datenzeilenlimit | Z. 2734 und Z. 966, **beide** Speichern-Knöpfe |
| F2 | **B0:** Der Verwalten-Dialog im Buchungen-Tab speichert `varSelectedBuchungTab`, aber zwölf Plus-/Minus-Properties lesen `varSelectedBuchung` | Z. 3753 bis 3996 |
| F3 | Verlängern prüft **nur beim Färben**, nicht beim Speichern | `btnVerlängern` Z. 3256, `btnVerlängern_1` Z. 3702 |
| F4 | **Kein Knopf** der App hat eine `DisplayMode`-Sperre gegen Doppelklick | per Skript geprüft, 0 Treffer bei den vier Speichern-/Verlängern-Knöpfen |
| F5 | Aufräumblock läuft **unbedingt**, auch nach Fehlern: Dialog schließt, Eingaben weg | Z. 2828 ff., Z. 1048 ff. |
| F6 | `Remove(Tischbuchungen, varSelectedBuchung)` auf einer **Variablen** statt frischem `LookUp` | `btnStornieren` Z. 3237 |
| F7 | Meldung „Wiederholung auf 2 Wochen begrenzt" **verdrängt** Kollisions- und Erfolgsmeldung | Z. 2810, Z. 1032 |
| F8 | Zahlen in Meldungen kommen aus **lokalen Collections**, nicht aus einer Nachlese | Z. 2805 |
| F9 | `Screen1.LoadingSpinner = LoadingSpinner.Data` **neben** dem eigenen Overlay `conLadeOverlay` → doppelter Spinner | Z. 13 und Z. 4341 |
| F10 | `ddStockwerk.OnSelect` setzt `varAusgewaehltePlusDauer` auf **`0`**, überall sonst `Blank()`. `IsBlank(0)` ist falsch → Null-Verlängerung möglich | Z. 333 |
| F11 | `chkAlleAuswählen` markiert nur `galAlleTischbuchungen.AllItems`, also die **geladene** Teilmenge | Z. 4195 |
| F12 | Ein- und Auschecken ohne Zeitfenster, auch für künftige Tage | `btnEincheckenHeute` Z. 472, `btnEinchecken` Z. 3063 |
| F13 | Verlängern kennt **keine 22:00-Grenze** — eine Buchung kann in den Folgetag reichen | `btnPlus1Std` bis `btnPlus3Std` |
| F14 | Zwei Status-Logiken nebeneinander: eingecheckt ist im Grundriss **rot**, auf der Dashboard-Karte **grün** | Z. 80 gegen Z. 444 |

---

## 8. Power-Fx-Regeln in diesem Projekt

- **Zwei Schreibweisen:** In `.pa.yaml` steht das invariante Format (`,` trennt Argumente, `;` verkettet Anweisungen, `.` ist Dezimaltrenner, jede Formel beginnt mit `=`). Josias' Studio läuft auf Deutsch (`;` trennt, `;;` verkettet, `,` ist Dezimaltrenner). **Nie verwechseln.** Formeln für Josias zum Einfügen immer in deutscher Schreibweise.
- Keine Kommentare in Formeln (`//` erzeugt app-weite Fehler). *Anmerkung: In `App.Formulas` der Desktop-App stehen trotzdem `//`-Kommentare, dort funktioniert es.*
- `With()`-Felder werden gleichzeitig ausgewertet; Abhängiges braucht verschachtelte `With`.
- Eine Variable nie mit zwei verschiedenen Datensatztypen füllen (Typ wird app-weit aus allen `Set` abgeleitet).
- `Set(var; false)` setzt eine Checkbox nicht zurück, dafür `Reset(control)`.
- `varIsLoading` auf **jedem** Pfad zurücksetzen, auch nach Fehlern.
- `Navigate` in `App.OnStart` ist abgekündigt; Startbildschirm über `App.StartScreen`.
- Mehrarmiges `If(bed1; erg1; bed2; erg2; …)` kommt in der Desktop-App **nirgends** vor und ist bei `powerfxv1 = false` ungeprüft. Im Zweifel verschachtelte zweiarmige `If`.
- Änderungen an Josias immer als **vollständige** Ersatzformel für die ganze Property, nie als Teilstück.

---

## 8a. Wie ich in Power Apps Studio baue (wichtig nach einer Kontext-Kompaktierung)

**Steuerelemente lassen sich als YAML in die Zwischenablage legen und mit Strg+V ins Studio einfügen.** Das ist der schnelle Weg und ersetzt das Zusammenklicken. Geprüft und bestätigt am 06.10.2026.

So geht es:
1. YAML in PowerShell erzeugen und mit `Set-Clipboard -Value $yaml` in die Zwischenablage legen
2. Im Studio in der Strukturansicht das **Elternelement** auswählen (Screen oder Container)
3. Strg+V

Die exakte Syntax, von Studio selbst erzeugt (Kontextmenü eines Steuerelements → **Ansichtscode**):

```yaml
- conRoot:
    Control: GroupContainer@1.5.0
    Variant: AutoLayout
    Properties:
      LayoutAlignItems: =LayoutAlignItems.Stretch
      LayoutDirection: =LayoutDirection.Vertical
      PaddingBottom: =0
      X: =0
      Y: =0
      Width: =Parent.Width
      Height: =Parent.Height
    Children:
      - conHeader:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            LayoutDirection: =LayoutDirection.Horizontal
            FillPortions: =0
            Height: =150
```

Bestätigte Eigenschaften für Auto-Layout-Container: `Variant: AutoLayout`, `LayoutDirection` (`.Vertical`/`.Horizontal`), `LayoutAlignItems` (`.Stretch`/`.Center`), `FillPortions` (0 = feste Größe, 1 = füllt den Rest), `Padding…`.

**Zwei Schreibweisen, nicht verwechseln:**
- **In der YAML-Zwischenablage:** invariantes Format, Komma trennt Argumente (`RGBA(247, 247, 247, 1)`)
- **In der Formelleiste des Studios:** deutsche Schreibweise, `;` trennt Argumente, `;;` verkettet (`Set(varTab; "heute");; Set(varIsLoading; false)`)

Beides funktioniert nebeneinander; Studio rechnet die YAML beim Einfügen um.

### Das Koordinatensystem der Handy-App ist verdoppelt (gemessen)

**BELEGT** am 06.10.2026 mit einem Diagnose-Label in der Geräteemulation iPhone 390 × 844:

```
App 780 x 1688  |  Screen 780 x 1688  |  varTab: heute
```

**Eine App-Einheit ist ein halbes CSS-Pixel.** Daraus folgt für alle Maße und Schriftgrößen in dieser App:

| Was | Zielwert am Gerät | Wert in der App |
|---|---|---|
| Tippfläche (Auftrag: 44 bis 48 pt) | 44 bis 48 px | **88 bis 96** |
| Fließtext | 12 bis 14 px | **24 bis 28** |
| Überschrift | 16 bis 18 px | **32 bis 36** |
| kleine Nebenzeile | 11 bis 12 px | **22 bis 24** |
| Kopfzeile hoch | ca. 85 px | **170** |
| Tab-Leiste hoch | ca. 90 px | **180** |

Wer hier mit den gewohnten Zahlen aus einer Desktop-App arbeitet (Schriftgröße 15, Knopfhöhe 40), bekommt eine Oberfläche in halber Größe. Das ist mir beim ersten Durchgang genau so passiert.

**Vier Fallen beim YAML-Einfügen, alle selbst erlebt:**

1. **`: ` (Doppelpunkt plus Leerzeichen) in einer Formel bricht die YAML-Syntax.** Betrifft jedes `With({name: ...})`. Fehlermeldung: `PA1001 … YamlInvalidSyntax; Reason: While scanning a plain scalar value, found invalid mapping`. Lösung: Blockwert verwenden.
   ```yaml
   Text: |-
     =With(
       { teile: Split(User().FullName, " ") },
       Upper(Left(First(teile).Value, 1))
     )
   ```
   Ein `:` **ohne** folgendes Leerzeichen ist unkritisch, deshalb geht `="data:image/png;base64,…"` ohne Blockwert.

2. **`LayoutMinWidth` muss gesetzt werden, sonst gilt 560.** Ein Label in einem Auto-Layout-Container hat standardmäßig `Mindestbreite 560`. Bei `FillPortions: =1` schrumpft es trotzdem nicht unter 560 und drückt alle Geschwister aus dem Bild. Immer `LayoutMinWidth: =0` und `LayoutMinHeight: =0` mitgeben.

3. **`Rectangle@2.3.0` hat keine Radius-Eigenschaften.** `RadiusTopLeft` und Verwandte gibt es nur an `GroupContainer@1.5.0` und `Classic/Button@2.2.0`. Fehlermeldung: `PA2108 : Unknown property 'RadiusBottomLeft' for control type 'Rectangle@2.3.0'`. Für eine abgerundete Fläche einen `GroupContainer` nehmen.

4. **Eingefügte Steuerelemente landen am Ende der Geschwisterliste.** In einem vertikalen Auto-Layout-Container heißt das: unten. Danach über Kontextmenü → **Neu anordnen** → *Ganz nach oben verschieben* an die richtige Stelle bringen.

**Kleine Fallen im Studio:**
- Der Menüweg „Erstellen" legt immer eine **Tablet**-App an. Phone-Format nur über `canvas/?action=new-blank&form-factor=phone`
- Der Dialog „Speichern unter" hat einen Bereich **„Vorhandene ersetzen"** mit allen Apps der Umgebung. Vor dem Klick prüfen, dass **nichts** ausgewählt ist, sonst wird eine fremde App überschrieben
- Beim Einfügen eines Containers über das Menü entsteht ein überzähliges `Container1`, das danach gelöscht werden muss

## 9. Was die Desktop-App an Struktur hat (zur Orientierung)

186 Steuerelemente, 1985 gesetzte Properties, **ein** Screen (`Screen1`), 14 `GroupContainer` mit `Variant: ManualLayout`, 5 Galerien, 50 globale Variablen, 5 Collections, 20 Named Formulas, keine Kontextvariablen, kein Timer, keine Komponenten.

Container auf oberster Ebene: `conGrundriss`, `conDashboard`, `conTischBuchungenPanel`, `conRaumBuchungenPanel` (tot), `conRaumBestätigen` (tot), `conBuchungDialog`, `conCheckinDialog`, `conDetailsPopup`, `conVerwaltenDialog`, `conBuchungen`, `conHeader`, `conLadeOverlay`.

Die Handy-App übernimmt davon **keine** Steuerelemente, nur die Logik.

---

## 9. Funde aus dem Bau von „Buchen" (06.10.2026, alle BELEGT durch die App-Prüfung)

**Klassisches Dropdown:** `Control: Classic/DropDown@2.3.1`, die Anzeigespalte heißt im YAML `Items.Value: =Value`. Ermittelt, indem ich ein Dropdown über das Menü eingefügt und mit Strg+C in die Zwischenablage kopiert habe — **so lässt sich jede Steuerelementversion zuverlässig herausfinden.** Kein `AllItems` am klassischen Dropdown; „leer" erkennt man an `IsBlank(dd.Selected.Value)`.

**Delegation, drei weitere Regeln:**

| Form | Ergebnis |
|---|---|
| `With({s: DateAdd(dd.Selected.Tag, …)}, Filter(Tischbuchungen, Startzeit < e && Endzeit > s))` | **Warnung** an `Startzeit`/`Endzeit` — auch wenn das Local nur aus Steuerelementwerten berechnet ist |
| `Filter(Tischbuchungen, Startzeit < DateAdd(ddDatum.Selected.Tag, ddEnde.Selected.Min, TimeUnit.Minutes) && …)` | **keine Warnung** — der Ausdruck direkt im Prädikat wird vor dem Absenden aufgelöst |
| `LookUp(Tischbuchungen, … && ID < varBuchungID)` | **Warnung** an `ID`: an der ID-Spalte ist nur `=` delegierbar |
| `LookUp(Tischbuchungen, … && Startzeit = varBuchStart && …)` | **Warnung** am `LookUp` (Gleichheit auf Datum/Uhrzeit) |

**Muster dafür:** eine delegierbare Abfrage mit Zeitgrenze in eine Sammlung (`ClearCollect(colKollision, Filter(…))`), Feinprüfung lokal. Die Sammlung ist klein (Zeilen eines Tisches in einem Zeitraum).

**Studio-Vorschau führt `OnStart` nicht neu aus.** Neue Sammlungen aus `OnStart` sind in der Vorschau leer, bis man in der Strukturansicht `App` → Kontextmenü → **„OnStart ausführen"** wählt.

**YAML:** Eine Formel, die mit `="` beginnt und `): "` enthält, muss ebenfalls als Blockwert `|-` geschrieben werden. Sonst: „Mit dem eingefügten Code stimmt etwas nicht."

**Unabhängige Nachlese:** Lesend über die SharePoint-REST-Schnittstelle im angemeldeten Browser, siehe `TESTPROTOKOLL.md` „Nachlese-Methode". Höchste Buchungs-ID vor meinen Tests: 495.