# INVENTAR.md — Quellcode-Inventar der App „Tischbuchung"

**Erstellt:** 01.10.2026
**Quelle:** `Tischbuchung_2026-09-30_Analyse_20260930124236 (1).zip` → `Microsoft.PowerApps/apps/1516988942138200528/Ncd7bb48d-…-document.msapp` → `./src`
**Verifiziert:** `displayName: "Tischbuchung"` in `1516988942138200528.json`. Das ist die richtige App.
**Umfang des Quellcodes:** `Src/App.pa.yaml` (139 Zeilen), `Src/Screen1.pa.yaml` (4.323 Zeilen), `References/DataSources.json`, `AppCheckerResult.sarif`.

> **Hinweis zur Schreibweise in allen ORIGINAL-Zitaten:** Der YAML-Export steht in invarianter Locale, also mit **Komma** als Argumenttrenner. Im deutschen Studio siehst du dort **Semikolon**. Das ist kein Unterschied in der Formel, nur in der Darstellung. Alle Zitate unten sind wortgetreu aus dem Export, also mit Komma.

---

## Vorab: drei Funde, die alles andere betreffen

**A. Die Spalte heißt `Titel`, nicht `Title`.**
`References/DataSources.json`: Liste `Tische`, interner Name `Title`, **Anzeigename `Titel`**. Die App arbeitet durchgehend mit Anzeigenamen. Im Quellcode: 79 Treffer für `.Titel`, **null** für `.Title`.
→ Regel 6 in `KONTEXT.md` („Interner Spaltenname ist immer `Title`, nie `Titel`") beschreibt den internen Namen richtig, ist als Formel-Regel aber **irreführend**. In jeder Power-Fx-Formel dieser App ist `Titel` korrekt.

**B. Die Check-in-Spalte ist eindeutig geklärt — kein `UNSICHER`.**
Interner Name: `Checkedin` (kleines i). Anzeigename: `CheckedIn` (großes I). Die App benutzt durchgehend `CheckedIn`, also den Anzeigenamen, und das ist korrekt. Für Power Automate oder REST ist dagegen `Checkedin` zu verwenden.

**C. Es gibt eine Spalte `SerienID` in `Tischbuchungen` — die App benutzt sie nirgends.**
`SerienID`, Typ `string`, read-write, filterbar mit `eq` und `startswith`. Null Treffer im gesamten Quellcode. In `KONTEXT.md` kommt sie nicht vor. Das ist für die Serienbuchung und für die Mehrfachauswahl die wichtigste ungenutzte Ressource im Datenmodell.

---

## 1. MASTER-BEDINGUNG

**Befund: sechs Steuerelement-Properties, aber zwölf `LookUp(Tischbuchungen; …)`-Vorkommen.** Alle in der Galerie-Vorlage `Screen1.conGrundriss.Gallery1`.

`Gallery1.Items` (Zeile 55):
```
=Filter(Tische, Geschoss.Value = varAusgewaehltesStockwerk)
```

### 1.1 `Gallery1.Rectangle1.Fill` — Datei `Src/Screen1.pa.yaml`, Zeile 66–85
```
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
    ColorValue("#00A96B"),
    If(
      relevanteBuchung.CheckedIn,
      ColorValue("#EB3951"),
      ColorValue("#FFA500")
    )
  )
)
```

### 1.2 `Gallery1.Circle1.BorderColor` — Zeile 149–153
```
=With(
  { relevanteBuchung: LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)) },
  If(IsBlank(relevanteBuchung), Color.Transparent, Color.Black)
)
```
**Abweichung zu allen anderen fünf Stellen:** Hier fehlt der `If(varAnsichtsDatum = Today(); …)`-Zweig. Diese Property prüft **immer** gegen `Now()`, egal welches Datum angezeigt wird. Beim Blättern auf einen anderen Tag zeigt der Kreisrand also die Lage von heute.

### 1.3 `Gallery1.Circle1.BorderStyle` — Zeile 154–168 (drei LookUps)
```
=With(
  {
    istBesetzt:
      If(
        varAnsichtsDatum = Today(),
        !IsBlank(LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Now() >= Startzeit && Now() <= Endzeit)),
        !IsBlank(LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)))
      ),
    istAusstehend:
      varAnsichtsDatum = Today() &&
      !IsBlank(LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit > Now() && Startzeit <= DateAdd(Now(), 60, TimeUnit.Minutes)))
  },
  If(istBesetzt Or istAusstehend, BorderStyle.Solid, BorderStyle.None)
)
```
**Achtung:** `istBesetzt` benutzt hier das Fenster `Now() >= Startzeit && Now() <= Endzeit` — ein **anderes** Zeitfenster als die anderen fünf Stellen (`Endzeit >= Now() && Startzeit <= Now()+30min`). Zwei verschiedene Definitionen von „besetzt" in derselben Kachel.

### 1.4 `Gallery1.Circle1.Fill` — Zeile 170–181
```
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(IsBlank(relevanteBuchung), ColorValue("#4DC398"), Color.White)
)
```

### 1.5 `Gallery1.Label1.Text` — Zeile 212–228
```
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
    "",
    Upper(Left(First(Split(relevanteBuchung.Person.DisplayName, " ")).Value, 1) &
          Left(Last(Split(relevanteBuchung.Person.DisplayName, " ")).Value, 1))
  )
)
```

### 1.6 `Gallery1.btnHitArea.OnSelect` — Zeile 245–277
```
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
      Set(varSelectedTisch, ThisItem);
      Set(varZeigeDialog, true);
      Set(varZeigeDetails, false);
      Set(varZeigeCheckin, false);
      Set(varZeigeVerwalten, false);
      Set(varWiederholen, false);
      Set(varWiederholenModus, "Wochentage");
      Set(varTagMo, false);
      Set(varTagDi, false);
      Set(varTagMi, false);
      Set(varTagDo, false);
      Set(varTagFr, false);
      Set(varTagSa, false);
      Set(varTagSo, false),
      Set(varDetailsTisch, ThisItem); Set(varSelectedBuchung, relevanteBuchung);
      Set(varZeigeDetails, true);
      Set(varZeigeDialog, false);
      Set(varZeigeCheckin, false);
      Set(varZeigeVerwalten, false)
  )
)
```

### Antwort auf die Frage „sind es sechs?"

**Es sind genau sechs Properties — die Notiz stimmt in der Zahl.** Sie stimmt aber **nicht in der Liste**: `KONTEXT.md` §4.2 nennt `btnEincheckenHeute.Visible` als sechste Stelle. Dieses Steuerelement (`conDashboard.galTischbuchungenHeute.btnEincheckenHeute`, Zeile 460) hat **gar keine `Visible`-Property** und enthält keine Master-Bedingung. Die tatsächliche sechste Stelle ist `btnHitArea.OnSelect`.

**Last pro Rendervorgang:** `Gallery1` zeigt im OG 16 Tische (13 `OG Desk` + 3 `Quiet Desk`), im UG 18. Pro Zeile werden ausgewertet: Rectangle1.Fill (1) + Circle1.BorderColor (1) + Circle1.BorderStyle (2) + Circle1.Fill (1) + Label1.Text (1) = **6 `LookUp` pro Tisch**. `btnHitArea.OnSelect` kommt nur beim Klick dazu. Macht **96 `LookUp`-Auswertungen im OG, 108 im UG** bei jedem Neuaufbau des Grundrisses.

---

## 2. REFRESH

**Neun Vorkommen, alle `Refresh(Tischbuchungen)`. Keines davon steht in einer `ForAll`-Schleife.**

| # | Zeile | Steuerelement | Property | In `ForAll`? |
|---|---|---|---|---|
| 1 | 781 | `conDashboard.Icon1_1` | `OnSelect` | nein |
| 2 | 1048 | `conTischBuchungenPanel.btnSpeichernTischePanel` | `OnSelect` | **nein** — steht nach der schließenden Klammer der `ForAll` |
| 3 | 2816 | `conBuchungDialog.btnSpeichern` | `OnSelect` | **nein** — ebenso nach der `ForAll` |
| 4 | 3667 | `conBuchungen.conVerwaltenDialog_1.btnStornieren_1` | `OnSelect` | nein |
| 5 | 3699 | `conBuchungen.conVerwaltenDialog_1.btnVerlängern_1` | `OnSelect` | nein |
| 6 | 4080 | `conBuchungen.conVerwaltenKlein.btnStornierenKlein` | `OnSelect` | **nein** — direkt nach `ForAll(colAusgewaehlteBuchungen; Remove(…))` |
| 7 | 4174 | `conBuchungen.Icon1` | `OnSelect` | nein |
| 8 | 4202 | `conHeader.Image6` | `OnSelect` | nein |
| 9 | 4294 | `conHeader.btnHitArea_1` | `OnSelect` | nein |

### Deine Hauptvermutung ist widerlegt

`KONTEXT.md` §4.3 und `AUFGABE_INVENTAR.md` Punkt 2 nennen „`Refresh` in einer `ForAll`" als Hauptverdacht für die langsame Serienbuchung. **Das ist im Quellcode nicht der Fall.** Jedes `Refresh` steht genau einmal am Ende seines Vorgangs — das ist bereits die korrekte Form.

**Die echte Ursache steht eine Zeile höher:** die `ForAll`-Schleife selbst führt pro Durchlauf einen eigenen `Patch` bzw. `Remove` aus. Bei 10 Wiederholungen sind das 10 einzelne HTTP-Aufrufe gegen SharePoint, nacheinander. Genau das erzeugt das von dir beobachtete unregelmäßige Muster (Durchlauf 6 und 7 langsam, Rest schnell) — das ist Drosselung auf Einzelaufrufen, nicht ein wiederholtes Nachladen.

Microsofts eigene App-Prüfung bestätigt das: **`app-ForAllWithMutation`, drei Treffer**, exakt an diesen drei Stellen:
- `Screen1.conBuchungen.conVerwaltenKlein.btnStornierenKlein.OnSelect`
- `Screen1.conTischBuchungenPanel.btnSpeichernTischePanel.OnSelect`
- `Screen1.conBuchungDialog.btnSpeichern.OnSelect`

Die drei relevanten Schleifen:

**Zeile 4079** (`btnStornierenKlein.OnSelect`) — Mehrfach-Storno:
```
ForAll(colAusgewaehlteBuchungen, Remove(Tischbuchungen, ThisRecord));
```

**Zeile 1003–1027** (`btnSpeichernTischePanel.OnSelect`) und **Zeile 2771–2795** (`btnSpeichern.OnSelect`) — Serienbuchung, wortgleich bis auf die Steuerelementnamen:
```
ergebnisse:
  ForAll(
    datumsListe As Eintrag,
    If(
      CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0)))) = 0,
      With(
        {
          neuerEintrag: Patch(Tischbuchungen, Defaults(Tischbuchungen), {
            Tisch: {Id: ddTischePanel.Selected.ID, Value: ddTischePanel.Selected.Titel},
            Startzeit: Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0),
            Endzeit: Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0),
            Person: {
              Claims: "i:0#.f|membership|" & Lower(User().Email),
              Department: "",
              DisplayName: User().FullName,
              Email: User().Email,
              JobTitle: "",
              Picture: ""
            }
          })
        },
        "gespeichert"
      ),
      "übersprungen"
    )
  )
```

---

## 3. DELEGATION

Quelle ist hier nicht meine Einschätzung allein, sondern `AppCheckerResult.sarif` — das von Power Apps selbst beim Veröffentlichen gespeicherte Prüfergebnis. **136 Befunde insgesamt, davon 56 Delegationswarnungen.**

| Regel | Anzahl |
|---|---|
| `app-SuggestRemoteExecutionHint` | 32 |
| `app-SuggestRemoteExecutionHint-OpNotSupportedByService` | 14 |
| `app-SuggestRemoteExecutionHint-OpNotSupportedByColumn` | 10 |
| `acc-AccessibleLabelNeeded` | 37 |
| `acc-TabIndexShouldBeDefinedForInteractiveControl` | 19 |
| `app-UnusedVariables` | 10 |
| `acc-FocusBorderShouldBeVisible` | 7 |
| `app-ForAllWithMutation` | 3 |
| `app-CollectingReadOnlyTable` | 2 |
| `acc-ReadableScreenNameNeeded` | 1 |
| `app-ScreenHasManyControls` | 1 |

### Die 56 Delegationswarnungen nach Fundort

**Verlängern-Buttons — je 4 Warnungen, `Tisch.Value` ist der Auslöser (`OpNotSupportedByColumn`):**

| Steuerelement | Properties |
|---|---|
| `conVerwaltenDialog.btnPlus1Std` | `DisplayMode`, `Fill` |
| `conVerwaltenDialog.btnPlus2Std` | `DisplayMode`, `Fill` |
| `conVerwaltenDialog.btnPlus3Std` | `DisplayMode`, `Fill` |
| `conBuchungen.conVerwaltenDialog_1.btnPlus1Std_1` | `DisplayMode`, `Fill` |
| `conBuchungen.conVerwaltenDialog_1.btnPlus2Std_1` | `DisplayMode`, `Fill` |

Das sind 10 Properties × 4 = 40 Warnungen. Wortlaut des Auslösers: `aktuelleBuchung.Tisch.Value`.

**Weitere, je 1 Warnung wegen `CountRows` (`OpNotSupportedByService`):**

| Steuerelement | Property | Datenquelle |
|---|---|---|
| `conTischBuchungenPanel.btn5Std` | `DisplayMode`, `Fill` | Tischbuchungen |
| `conTischBuchungenPanel.btn9Std` | `DisplayMode`, `Fill` | Tischbuchungen |
| `conBuchungen.conVerwaltenDialog_1.btnPlus3Std_1` | `DisplayMode`, `Fill` | Tischbuchungen |
| `conRaumBuchungenPanel.galRäume` | `Items` (3 Warnungen) | Raumbuchungen — **toter Code** |
| `conRaumBuchungenPanel.galRäume.btnSlot1` | `DisplayMode`, `Fill` | Raumbuchungen — **toter Code** |
| `conRaumBuchungenPanel.galRäume.btnSlot2` | `DisplayMode` | Raumbuchungen — **toter Code** |
| `conRaumBuchungenPanel.galRäume.btnSlot3` | `DisplayMode` | Raumbuchungen — **toter Code** |
| `conRaumBuchungenPanel.galRäume.btnSlot4` | `DisplayMode` | Raumbuchungen — **toter Code** |
| `conRaumBestätigen.recBuchungDavor1` | `Visible` | Raumbuchungen — **toter Code** |
| `conRaumBestätigen.recBuchungDanach1` | `Visible` | Raumbuchungen — **toter Code** |

**Zehn der 56 Warnungen hängen an totem Raumbuchungs-Code.** Das Löschen der Raum-Container entfernt sie ersatzlos — das ist der billigste Teil der Delegationsarbeit.

### Die wichtigste Abweichung in diesem Abschnitt

**Die Master-Bedingung aus Abschnitt 1 wird von der App-Prüfung nicht beanstandet.** Keine einzige der 56 Warnungen betrifft `Gallery1.Rectangle1.Fill`, `Circle1.*`, `Label1.Text` oder `btnHitArea.OnSelect`.

`KONTEXT.md` §4.1 nennt genau diese Formel „das Hauptproblem" und begründet das damit, dass `Tisch.Value`, `Now()` und `DateAdd()` nicht delegierbar seien. Die Prüfung sieht das anders: `Tisch.Value` wird bei den Plus-Buttons sehr wohl als `OpNotSupportedByColumn` gemeldet, in der Galerie-Vorlage aber nicht.

`UNSICHER:` **Warum die Prüfung die Galerie-Vorlage auslässt, kann ich aus dem Quellcode nicht belegen.** Zwei plausible Erklärungen: entweder prüft die App-Prüfung Ausdrücke im Galerie-Vorlagenkontext (`ThisItem`) grundsätzlich nicht auf Delegation, oder sie bewertet `LookUp` anders als `Filter`/`CountRows`. Das solltest du im Studio gegenprüfen: **Steht neben `Rectangle1.Fill` ein gelbes Warndreieck oder nicht?** Davon hängt ab, ob die Delegationsarbeit in Schritt 2 überhaupt an dieser Stelle ansetzen muss.

**Unabhängig von der Delegationsfrage bleibt der Befund aus Abschnitt 1 bestehen:** 96 bis 108 `LookUp`-Auswertungen pro Grundriss-Rendervorgang sind auch dann teuer, wenn jede einzelne delegiert. Eine Tages-Collection `colBuchungenTag` ersetzt sie durch einen Zugriff. Das ist der belastbare Teil des Arguments.

### Alle `Filter(`/`LookUp(` auf `Tischbuchungen`, vollständig

| Zeile | Ort | Ausdruck (gekürzt auf den Kern) | Einschätzung |
|---|---|---|---|
| 72, 73 | `Rectangle1.Fill` | `LookUp(…Tisch.Value…Now()…)` | nicht beanstandet, aber 1× pro Galeriezeile |
| 151 | `Circle1.BorderColor` | `LookUp(…Tisch.Value…Now()…)` | dito |
| 160, 161, 165 | `Circle1.BorderStyle` | 3× `LookUp(…Tisch.Value…)` | dito, dreifach |
| 176, 177 | `Circle1.Fill` | `LookUp(…Tisch.Value…)` | dito |
| 218, 219 | `Label1.Text` | `LookUp(…Tisch.Value…)` | dito |
| 251, 252 | `btnHitArea.OnSelect` | `LookUp(…Tisch.Value…)` | nur bei Klick |
| 364–367 | `galTischbuchungenHeute.Items` | `Filter(Tischbuchungen, Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days) && (varAnsichtsDatum <> Today() \|\| Endzeit >= Now()))` | nicht beanstandet; `Person.Email` und der `\|\|`-Teil sind die Risikokandidaten |
| 966 | `btnSpeichernTischePanel.OnSelect` | `Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel)` | **holt alle Buchungen dieses Tisches, ohne Datumsgrenze** |
| 1226, 1251 | `btn5Std.DisplayMode`, `.Fill` | `CountRows(Filter(…))` | **beanstandet**, `CountRows` |
| 1311, 1336 | `btn9Std.DisplayMode`, `.Fill` | `CountRows(Filter(…))` | **beanstandet**, `CountRows` |
| 2734 | `btnSpeichern.OnSelect` | `Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)` | **ohne Datumsgrenze** |
| 3296, 3307 | `btnPlus1Std.DisplayMode`, `.Fill` | `CountRows(Filter(…Tisch.Value…))` | **beanstandet**, `Tisch.Value` |
| 3345, 3356 | `btnPlus2Std.*` | dito | **beanstandet** |
| 3394, 3406 | `btnPlus3Std.*` | dito | **beanstandet** |
| 3456 | `galAlleTischbuchungen.Items` | `Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now())` | nicht beanstandet; **kein Datumsfenster** — holt alle künftigen Buchungen des Nutzers |
| 3745, 3756 | `btnPlus1Std_1.*` | dito | **beanstandet** |
| 3794, 3805 | `btnPlus2Std_1.*` | dito | **beanstandet** |
| 3843, 3850 | `btnPlus3Std_1.*` | dito | **beanstandet** |

**Zu Bug 3 („Buchungen-Tab zeigt manchmal keine Einträge"):** `galAlleTischbuchungen.Items` filtert auf `Person.Email = User().Email && Endzeit >= Now()` **ohne Datumsobergrenze**. Wenn `Person.Email` nicht delegiert, holt Power Apps die ersten 2000 Zeilen und filtert lokal — fällt die eigene Buchung aus diesem Fenster, ist sie unsichtbar. Das passt exakt zum gemeldeten Verhalten. `UNSICHER:` Ob `Person.Email` hier delegiert, sagt mir die App-Prüfung nicht; sie meldet diese Zeile nicht, aber sie meldet die Galerie-Vorlagen auch sonst nicht. **Im Studio prüfen: steht neben `galAlleTischbuchungen.Items` ein Warndreieck?**

---

## 4. CHECK-IN-SPALTE

**`CheckedIn` (großes I): 7 Treffer. `Checkedin` (kleines i): keine Treffer.** Die Schreibweise in der App ist einheitlich.

| Zeile | Steuerelement | Property | Formel |
|---|---|---|---|
| 80 | `conGrundriss.Gallery1.Rectangle1` | `Fill` | `relevanteBuchung.CheckedIn,` |
| 444 | `conDashboard.galTischbuchungenHeute.lblStatusHeute` | `Color` | `=If(ThisItem.CheckedIn, ColorValue("#00A96B"), ColorValue("#FFA500"))` |
| 447 | `conDashboard.galTischbuchungenHeute.lblStatusHeute` | `Text` | `=If(ThisItem.CheckedIn, "Eingecheckt", "Einchecken")` |
| 3046 | `conCheckinDialog.btnEinchecken` | `Fill` | `=If(varSelectedBuchung.CheckedIn, ColorValue("#EB3951"), ColorValue("#00a96b"))` |
| 3054 | `conCheckinDialog.btnEinchecken` | `OnSelect` | `Set(varSelectedBuchung, Patch(Tischbuchungen, aktuelleBuchung, {CheckedIn: !aktuelleBuchung.CheckedIn}))` |
| 3058 | `conCheckinDialog.btnEinchecken` | `PressedColor` | `=If(varSelectedBuchung.CheckedIn, ColorValue("#EB3951"), ColorValue("#00a96b"))` |
| 3061 | `conCheckinDialog.btnEinchecken` | `Text` | `=If(varSelectedBuchung.CheckedIn, "Auschecken", "Einchecken")` |

**Beleg aus `References/DataSources.json`:**
```
"Checkedin": { "title": "CheckedIn", "type": "boolean", "x-ms-permission": "read-write",
               "x-ms-capabilities": { "filterFunctions": ["eq"] }, "default": false }
```
Interner Name `Checkedin`, Anzeigename `CheckedIn`. Power Apps arbeitet in dieser App mit Anzeigenamen (siehe auch `Titel` statt `Title`), also ist `CheckedIn` in jeder Formel **richtig**. Kein latenter Bug. Für Power Automate, REST oder Spaltenformatierung gilt dagegen `Checkedin`.

**Zu Bug 5 („Einchecken dauert manchmal lange"):** Der Grund steht nicht im `Patch`, sondern in seiner Umgebung. `btnEinchecken.OnSelect` macht zuerst `LookUp(Tischbuchungen, ID = varSelectedBuchung.ID)` (ein Serverzugriff), dann den `Patch` (zweiter Zugriff). Danach rendert die Galerie `galTischbuchungenHeute` neu, und falls der Grundriss sichtbar ist, laufen dessen 96 `LookUp`s erneut. Der kleine Statusupdate zieht also einen vollständigen Neuaufbau nach sich.

---

## 5. TOTER CODE

### 5.1 Raumbuchungen — vollständig unerreichbar

**Beweiskette:** Der gesamte Raum-Zweig hängt an `varZeigeRaumBuchungForm`. Diese Variable wird an genau einer Stelle auf `true` gesetzt:

- Zeile 698, `conDashboard.btnRaumHinzufügen.OnSelect`: `=Set(varZeigeRaumBuchungForm, true)`
- Zeile 704, **`conDashboard.btnRaumHinzufügen.Visible`: `=false`**

Der einzige Einstieg ist unsichtbar. **Der komplette Raum-Zweig ist unerreichbar.**

| Fund | Ort | Was ihn noch referenziert |
|---|---|---|
| `conRaumBuchungenPanel` (Container, Zeile 1379) | Screen1 | `Visible: =varZeigeRaumBuchungForm` — nie `true` |
| `conRaumBestätigen` (Container, Zeile 2248) | Screen1 | `Visible: =varZeigeRaumBestätigung` — nur aus `galRäume.btnSlot1–4.OnSelect`, die im toten Panel liegen |
| `conDashboard.galRaumbuchungenHeute` (Zeile 506) | conDashboard | `Visible: =false` (Zeile 513) |
| `conDashboard.lblRaumLeer` (Zeile 635) | conDashboard | `Visible: =false` (Zeile 642) |
| `conDashboard.lblMyMeetings` (Zeile 656) | conDashboard | `Visible: =false` (Zeile 663) |
| `conDashboard.btnRaumHinzufügen` (Zeile 687) | conDashboard | `Visible: =false` (Zeile 704) |
| `varZeigeRaumBuchungForm` | App.OnStart Z. 45 | `conDashboard.Visible` (Z. 351, als `!varZeigeRaumBuchungForm`), `conRaumBuchungenPanel.Visible` (Z. 1385), Setzer Z. 698/1470/2316 |
| `varAusgewähltRaum` | App.OnStart Z. 46 | nur innerhalb `conRaumBuchungenPanel` und `conRaumBestätigen` |
| `varAusgewählteStartzeit` | App.OnStart Z. 47 | dito |
| `varAusgewählteEndzeit` | App.OnStart Z. 48 | dito |
| `varZeigeRaumBestätigung` | App.OnStart Z. 49 | dito |
| `varZeigeRaumInfo` | App.OnStart Z. 61 | **nichts** — von der App-Prüfung als `app-UnusedVariables` gemeldet |
| `varZeigeRaumVerwalten` | App.OnStart Z. 62 | nur `Set(varZeigeRaumVerwalten, false)` in `btnTabBuchungen.OnSelect` (Z. 4240) — also nur ein Schreibzugriff, nie gelesen. Ebenfalls als `app-UnusedVariables` gemeldet |

**Steuerelementzahl im toten Raum-Zweig:** `conRaumBuchungenPanel` 25 (inkl. Container), `conRaumBestätigen` 14 (inkl. Container), `galRaumbuchungenHeute` samt Kindern 9, dazu `lblRaumLeer`, `lblMyMeetings`, `btnRaumHinzufügen` = **51 von 186 Steuerelementen, also 27 %.**

Die Datenquellen `Räume` und `Raumbuchungen` sind in `References/DataSources.json` weiterhin verbunden.

### 5.2 Zoom und Pan

| Fund | App.OnStart | Screen1 | Status |
|---|---|---|---|
| `varZoom` | Z. 77, `Set(varZoom, 1)` | **2 Treffer**: `Circle1.Height` (Z. 187) und `Circle1.Width` (Z. 194), jeweils `… * BasisSkalierung * varZoom` | **nicht tot.** Wird gelesen, ist aber immer 1 und wird nie geändert. `KONTEXT.md` hat recht: nicht entfernt. Entfernen bedeutet: beide Properties anpassen, dann `Set` löschen. |
| `varPanX` | Z. 78 | **keine Treffer** | **tot.** Von der App-Prüfung als `app-UnusedVariables` bestätigt. Gefahrlos löschbar. |
| `varPanY` | Z. 79 | **keine Treffer** | **tot.** Dito. |

### 5.3 Die amtliche Liste der ungenutzten Variablen

Aus `AppCheckerResult.sarif`, Regel `app-UnusedVariables` — das ist Microsofts eigener Befund, nicht meine Schätzung:

```
App.varZeigeVerlaengern
App.varWiederholenBis
App.varZeigeRaumInfo
App.varZeigeRaumVerwalten
App.varPanX
App.varPanY
App.varWiederholenBisGewaehlt
App.varStockwerkDropdownOffen
App.varMehrfachAuswahlModus
App.varSpinnerWinkel
```

Zehn Variablen. Zwei davon (`varZeigeVerlaengern`, `varStockwerkDropdownOffen`) stehen **nicht** auf der Verdachtsliste in `KONTEXT.md` — die sind neu.

Genauer hingesehen:
- `varZeigeVerlaengern`: in Screen1 2 Treffer, beide nur `Set(…, false)` (Z. 330 `ddStockwerk.OnSelect`, Z. 4245 `btnTabBuchungen.OnSelect`). Nie gelesen.
- `varStockwerkDropdownOffen`: in Screen1 nur `Set` in `ddStockwerk.OnChange` und `.OnSelect`. Nie gelesen.
- `varWiederholenBis`: nur `Set` in `dpWiederholenBis.OnSelect` und `dpWiederholenBis_1.OnSelect`. Nie gelesen — die Formeln lesen stattdessen direkt `dpWiederholenBis.SelectedDate`.
- `varWiederholenBisGewaehlt`: nur `Set(…, true)` in `dpWiederholenBis.OnChange`. Nie gelesen.
- `varMehrfachAuswahlModus`: nur `Set(…, false)` in `btnVerlängern_1.OnSelect` (Z. 3703). Nie gelesen. **Die Frage aus `KONTEXT.md` ist damit beantwortet: von den zwei Variablen für denselben Zweck wird nur `varAuswahlModusAktiv` wirklich benutzt.**

### 5.4 Weitere Auffälligkeiten in `App.OnStart`

- **`varZeigeTischBuchungForm` wird in `App.OnStart` nie initialisiert**, aber in Screen1 sechsmal verwendet, darunter als `conDashboard.Visible` (Z. 351) und `conTischBuchungenPanel.Visible` (Z. 797). Beim Start ist sie `Blank()`, was als `false` wirkt — es funktioniert, ist aber die einzige Oberflächen-Zustandsvariable ohne Initialisierung.
- **`varDetailsTisch` wird ebenfalls nie initialisiert**, aber in `conDetailsPopup.X` und `.Y` gelesen (Z. 3098, 3100).
- `app-CollectingReadOnlyTable`, **2 Treffer, beide in `App.OnStart`** — das sind die zwei `ClearCollect`-Aufrufe mit den hartcodierten Koordinaten.

---

## 6. APP.FORMULAS

Vollständiger Inhalt, `Src/App.pa.yaml` Zeile 11–35, unverändert zitiert:

```
BasisBreite = 1920;
BasisHoehe = 1080;
BasisSkalierung = Min(conGrundriss.Width / BasisBreite, conGrundriss.Height / BasisHoehe);
BasisKachelbreiteQuer = 101;
BasisKachelhoeheQuer = 60;
BasisKachelbreiteHoch = 60;
BasisKachelhoeheHoch = 101;
BasisKreisgroesse = 39;
btnAbstand = 6;
btnBreite = Min(80, Max(44, (conVerwaltenDialog_1.Width - 5*btnAbstand - 40) / 6));
BasisKachelbreiteHochUG = 52;
BasisKachelhoeheHochUG = 89;
BasisKachelbreiteQuerUG = 89;
BasisKachelhoeheQuerUG = 52;
BasisKreisgroesseUG = 34;
BasisSchriftgroesseUG = 12;
// Josias 2026-09-28: eigene Breite fuer Big Table UG, deutlich breiter als Standardtisch, Hoehe bleibt Basishoehe horizontal
BasisKachelbreiteBigTableUG = 220;

// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
TischNrOG = With({src: Filter(Tische, Geschoss.Value = "OG")}, ForAll(Sequence(CountRows(src)), {Titel: Index(src, Value).Titel, Nr: Value}));
TischNrUG = With({src: Filter(Tische, Geschoss.Value = "UG")}, ForAll(Sequence(CountRows(src)), {Titel: Index(src, Value).Titel, Nr: Value}));
// Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
BasisSkalierungReferenz = Min(881 / BasisBreite, 678 / BasisHoehe);
```

**19 Named Formulas.**

### Zwei Befunde dazu

**1. `//`-Kommentare stehen in `App.Formulas` und die App ist veröffentlicht.**
Drei Stück (Zeile 28, 31, 34), dazu zwei weitere in `Screen1.Rectangle1.Height` (Z. 94) und `.Width` (Z. 114) sowie zwei in `Rectangle1.Y` (Z. 134–135). Insgesamt sieben `//`-Kommentare im produktiven Code.
→ Die Regel „Keine Kommentare in Power Fx, ein `//` erzeugt app-weite Fehler" aus `KONTEXT.md` §6 trifft für diese App **nicht zu**. Ich halte mich trotzdem daran und liefere kommentarfrei, aber du solltest wissen, dass die Regel so nicht stimmt.

**2. `TischNrOG` und `TischNrUG` enthalten je ein `Filter(Tische, …)` plus `CountRows` plus `ForAll`.**
Named Formulas werden bei jeder Auswertung neu berechnet und nicht zwischengespeichert. `BasisSkalierung` hängt an `conGrundriss.Width`/`.Height` — ändert sich die Fenstergröße, wird alles neu berechnet. `TischNrOG` wird in `Rectangle1.Y` **pro Galeriezeile** ausgewertet. Das ist 16 bis 18 Mal pro Render ein `Filter` über `Tische` plus `ForAll` über eine Sequenz. `UNSICHER:` Ob Power Apps das intern dedupliziert, kann ich aus dem Quellcode nicht belegen.

---

## 7. SPINNER

### Die Bestandsaufnahme

| Element | Fundstelle | Befund |
|---|---|---|
| `conLadeOverlay` | `Screen1`, Zeile 4304 | `Fill: =RGBA(0, 0, 0, 0.4)`, `Visible: =varIsLoading`, volle Bildschirmgröße. Genau ein Kind. |
| `imgSpinner` | Zeile 4313 | `Image: ='Spinner@1x-1.0s-201px-201px'` (eine animierte GIF-Datei, `Assets/Images/3fa86700-….gif`, 88 KB), `DisplayMode: =DisplayMode.Disabled`, 80×80, mittig |
| `varIsLoading` | App.OnStart Z. 137 | 17 Treffer in Screen1 |
| `varSpinnerWinkel` | App.OnStart Z. 138 | **null Treffer in Screen1.** Tot. Von der App-Prüfung bestätigt. |
| **Timer-Steuerelement** | — | **Existiert nirgends.** Null Treffer auf `Timer` im gesamten Quellcode. |

`varIsLoading` wird in diesen Paaren gesetzt (`true` am Anfang, `false` am Ende desselben `OnSelect`):

| Zeilen | Steuerelement |
|---|---|
| 780 / 782 | `conDashboard.Icon1_1` |
| 960 / 1069 | `conTischBuchungenPanel.btnSpeichernTischePanel` |
| 2728 / 2827 | `conBuchungDialog.btnSpeichern` |
| 3662 / 3671 | `conVerwaltenDialog_1.btnStornieren_1` |
| 4075 / 4087 | `conVerwaltenKlein.btnStornierenKlein` |
| 4173 / 4175 | `conBuchungen.Icon1` |
| 4201 / 4203 | `conHeader.Image6` |
| 4293 / 4295 | `conHeader.btnHitArea_1` |

### Die Ursache des doppelten Ladesymbols — gefunden

**`Screen1.Properties`, Zeile 13:**
```
LoadingSpinner: =LoadingSpinner.Data
```
Zusätzlich Zeile 14: `LoadingSpinnerColor: =RGBA(100, 118, 132, 1)`.

Das ist der **eingebaute Lade-Spinner des Screens**. Power Apps zeigt ihn automatisch an, solange eine Datenquelle des Screens lädt. Er ist unabhängig von `varIsLoading` und von `conLadeOverlay`.

**Damit laufen zwei voneinander unabhängige Ladeanzeigen parallel:**
1. der eingebaute Screen-Spinner (`LoadingSpinner.Data`), ausgelöst vom Datenladen selbst,
2. das selbstgebaute `conLadeOverlay` mit `imgSpinner`, gesteuert von `varIsLoading`.

Sie erscheinen zu verschiedenen Zeitpunkten und an verschiedenen Stellen — genau das gemeldete Symptom. Eine der beiden muss weg. Die naheliegende Lösung ist `Screen1.LoadingSpinner` auf `LoadingSpinner.None` zu setzen, weil `conLadeOverlay` den Bildschirm sperrt und damit zusätzlich Doppelklicks verhindert. Der Vollständigkeit halber: `varSpinnerWinkel` kann ersatzlos gelöscht werden, es gibt keinen Timer, der sie hochzählen würde.

---

## 8. MEHRFACHAUSWAHL

### Der wichtigste Befund dieses Abschnitts

**Es gibt kein Mehrfach-Speichern.** Die Mehrfachauswahl kennt genau eine Sammelaktion: **Stornieren**. Punkt 2.c der `AUFGABE_UMBAU.md` („Mehrfachauswahl Speichern") hat im Quellcode keine Entsprechung.

Der Button, der im Mehrfach-Dialog „Speichern" heißt (`btnVerlängern_1`, Zeile 3679), gehört zu `conVerwaltenDialog_1` und arbeitet auf **`varSelectedBuchungTab`**, also auf genau einer Buchung. Er leert danach `colAusgewaehlteBuchungen` mit, was irreführend aussieht, aber keine Mehrfachoperation ist.

### Die beteiligten Steuerelemente, vollständig

**`conBuchungen.tglAuswahlModus`** — Schalter „Auswahlmodus", Zeile 4127
```
DisplayMode: =If(galAlleTischbuchungen.AllItemsCount <= 1, DisplayMode.Disabled, DisplayMode.Edit)
OnChange: |-
  =Set(varAuswahlModusAktiv, tglAuswahlModus.Value);
  If(
    !tglAuswahlModus.Value,
    Clear(colAusgewaehlteBuchungen);
    Set(varZeigeVerwaltenKlein, false);
    Set(varGeklickteBuchungKlein, Blank())
  );
  Set(varGalleryNeuAufbauen, varGalleryNeuAufbauen + 1);
  If(
    tglAuswahlModus.Value,
    Set(varZeigeVerwaltenTab, false)
  )
TrueFill: =RGBA(100, 118, 132, 1)
X: =galAlleTischbuchungen.X + galAlleTischbuchungen.Width - Self.Width
Y: =52
```

**`conBuchungen.chkAlleAuswählen`** — „alle markieren", Zeile 4149
```
Default: =CountRows(colAusgewaehlteBuchungen) > 0 && CountRows(colAusgewaehlteBuchungen) = galAlleTischbuchungen.AllItemsCount
OnCheck: =ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)
OnUncheck: =Clear(colAusgewaehlteBuchungen)
Visible: =varAuswahlModusAktiv
```

**`conBuchungen.galAlleTischbuchungen.chkAuswahl`** — Haken pro Zeile, Zeile 3574
```
Default: =!IsBlank(LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
OnCheck: =Collect(colAusgewaehlteBuchungen, ThisItem)
OnUncheck: =Remove(colAusgewaehlteBuchungen, LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
Visible: =varAuswahlModusAktiv
X: =btnVerwalten_2.X - btnVerwalten.Width - 10
```
**Fehler in `X`:** verweist auf `btnVerwalten.Width` — das ist der Button in `conDashboard.galTischbuchungenHeute`, nicht `btnVerwalten_2` in dieser Galerie. Ein übersehener Name beim Kopieren. Fällt nicht auf, weil beide 50 breit sind.

**`conBuchungen.galAlleTischbuchungen.btnVerwalten_2.OnSelect`** — Zeile 3556
```
=If(
  varAuswahlModusAktiv,
  Set(varGeklickteBuchungKlein, ThisItem);
  Set(varZeigeVerwaltenKlein, true),
  Set(varSelectedBuchungTab, ThisItem);
  Set(varZeigeVerwaltenTab, true);
  Set(varZeigeCheckin, false);
  Set(varZeigeDetails, false);
  Set(varZeigeDialog, false)
)
```

**`conBuchungen.galAlleTischbuchungen.Items`** — Zeile 3452
```
=With(
  { erzwingeNeuaufbau: varGalleryNeuAufbauen },
  SortByColumns(
    Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()),
    "Startzeit",
    SortOrder.Ascending
  )
)
```
`erzwingeNeuaufbau` wird deklariert und **nie verwendet** — der einzige Zweck ist, die Formel von `varGalleryNeuAufbauen` abhängig zu machen, damit das Hochzählen in `tglAuswahlModus.OnChange` einen vollständigen Neuaufbau erzwingt. Das funktioniert, kostet aber jedes Mal eine komplette Neuabfrage der Datenquelle.

### Der Nullpunkt: `btnStornierenKlein.OnSelect` — Zeile 4074–4087

```
=Set(varIsLoading, true);
If(
  CountRows(colAusgewaehlteBuchungen) = 0,
  Notify("Keine Buchungen ausgewählt.", NotificationType.Warning),
  ForAll(colAusgewaehlteBuchungen, Remove(Tischbuchungen, ThisRecord));
  Refresh(Tischbuchungen);
  Notify("Buchungen storniert.", NotificationType.Success)
);
Clear(colAusgewaehlteBuchungen);
Set(varGeklickteBuchungKlein, Blank());
Set(varZeigeVerwaltenKlein, false);
Set(varAuswahlModusAktiv, false);
Set(varIsLoading, false); Reset(tglAuswahlModus)
```

**Das ist die Formel, um die es in `AUFGABE_SCHLEIFE.md` geht.** Drei harte Mängel:
1. `ForAll(… Remove(…))` erzeugt N einzelne Löschaufrufe statt einen. Von der App-Prüfung als `app-ForAllWithMutation` gemeldet.
2. Kein `IfError`. Schlägt ein `Remove` fehl, sieht der Nutzer den rohen Connector-Fehler — und die Erfolgsmeldung erscheint **trotzdem**, weil `Notify("Buchungen storniert.")` unbedingt nach der Schleife steht.
3. `ThisRecord` stammt aus `colAusgewaehlteBuchungen`, einer lokalen Kopie, die beim Anhaken erstellt wurde. Ist die Buchung inzwischen serverseitig weg, wirft `Remove` „Item Not Found" — **das ist Bug 4.**

**Die übrigen Mehrfachauswahl-Steuerelemente:**

`conVerwaltenKlein` (Container, Z. 4013): `Visible: =varZeigeVerwaltenKlein`, 400×150.
`lblVerwaltenKleinTitel` (Z. 4046):
```
=varGeklickteBuchungKlein.Tisch.Value &
If(
  CountRows(colAusgewaehlteBuchungen) > 1,
  " +" & (CountRows(colAusgewaehlteBuchungen) - 1) & " weitere",
  ""
)
```
`btnSchließenKlein.OnSelect` (Z. 4106):
```
=Set(varZeigeVerwaltenKlein, false);
Set(varGeklickteBuchungKlein, Blank());
Clear(colAusgewaehlteBuchungen);
Set(varAuswahlModusAktiv, false); Reset(tglAuswahlModus)
```

### Der Einzel-Storno zum Vergleich

**`conVerwaltenDialog.btnStornieren.OnSelect`** (Z. 3225) — der ältere der beiden:
```
=Remove(Tischbuchungen, varSelectedBuchung); Set(varZeigeVerwalten, false)
```
Kein `IfError`, kein `Refresh`, keine Meldung, `Remove` direkt auf einer Variablen statt auf frischem `LookUp`. Das ist die riskanteste Schreiboperation der App.

**`conBuchungen.conVerwaltenDialog_1.btnStornieren_1.OnSelect`** (Z. 3661) — der neuere:
```
=Set(varIsLoading, true);
If(
  IsBlank(varSelectedBuchungTab),
  Notify("Keine Buchung ausgewählt.", NotificationType.Warning),
  Remove(Tischbuchungen, varSelectedBuchungTab);
  Refresh(Tischbuchungen);
  Notify("Buchung storniert.", NotificationType.Success)
);
Set(varZeigeVerwaltenTab, false);
Set(varIsLoading, false)
```

---

## 9. FARBEN

### `ColorValue`-Literale

| Farbe | Anzahl | Verwendung |
|---|---|---|
| `#00A96B` | 44 | Grün „frei"/„eingecheckt"/„bestätigt". **Achtung:** zusätzlich 5× als `#00a96b` kleingeschrieben (Z. 1106, 1118, 1130, 1142, 1154 — die `tglTag*_1.TrueFill`; sowie Z. 2830, 3046, 3058). Power Fx ist hier unempfindlich, aber die Suche nach Fundstellen nicht. |
| `#EB3951` | 38 | Rot „besetzt"/„Konflikt". Ebenfalls einmal klein als `#eb3951` (Z. 2354, `recNeueBuchung.Fill`). |
| `#171496` | 11 | Technoform-Blau. Primärbuttons: `btnTabDashboard.Fill`, `btnTabBuchungen.Fill`, `btnStornieren.Fill`, `btnVerlängern.Fill`, `btnStornieren_1.Fill`, `btnVerlängern_1.Fill`, `btnStornierenKlein.Fill`, `btnSpeichernTischePanel.Fill`, `btnSpeichernRaumPanel.Fill`, `Rectangle2.Fill`, `Label16.Color` |
| `#FFA500` | 10 | Orange „gebucht, nicht eingecheckt" |
| `#f7f7f7` | 6 | Containerhintergrund: `conDashboard`, `conTischBuchungenPanel`, `conRaumBuchungenPanel`, `conRaumBestätigen`, `conBuchungen`, `conHeader` |
| `#F0F0F0` | 3 | `Rectangle4.Fill`, `Rectangle4_1.Fill`, `Rectangle7.Fill` |
| `#D0D0D0` | 2 | `btnRaumHinzufügen.Fill`, `btnTischHinzufügen.Fill` |
| `#4DC398` | 1 | `Circle1.Fill`, hellgrün bei freiem Tisch |
| `#8CAFF4`, `#82C7B3`, `#EFA897`, `#B59EDC`, `#82CCC5`, `#F5C295`, `#A1AADB`, `#A1B1BA` | je 1 | `App.OnStart` Z. 63–76, die acht Avatarfarben in `varProfilFarbe` |

### `RGBA`-Literale (die zwanzig häufigsten)

| Wert | Anzahl | Rolle |
|---|---|---|
| `RGBA(32, 54, 71, 1)` | 132 | Standard-`BorderColor`, fast überall, meist unsichtbar |
| `RGBA(255, 255, 255, 1)` | 121 | Weiß, `Color` und `HoverColor` von Buttons |
| `RGBA(166, 166, 166, 1)` | 45 | `DisabledBorderColor`, Standardwert |
| `RGBA(100, 118, 132, 1)` | 44 | Graublau: Trennlinien, `SelectionFill`, `ChevronBackground` |
| `RGBA(0, 0, 0, 1)` | 10 | Schwarz |
| `RGBA(205, 209, 213, 1)` | 7 | `HoverFill` der Dropdowns |
| `RGBA(50, 49, 48, 1)` | 6 | Textfarbe |
| `RGBA(0, 0, 0, 0)` | 6 | transparent, `ddStockwerk` |
| `RGBA(241, 241, 241, 1)` | 5 | Raum-Panel-Hintergrund (toter Code) |
| `RGBA(0, 0, 0, 0.2)` | 5 | `HoverFill` |
| `RGBA(234, 234, 236, 1)` | 3 | `conVerwaltenDialog_1`, `conVerwaltenKlein`, `Rectangle4_2` |
| `RGBA(0, 0, 0, 0.04)` | 2 | `HoverFill` |
| `RGBA(0, 0, 0, 0.08)` | 1 | `btnHitArea_1.HoverFill` |
| `RGBA(0, 0, 0, 0.4)` | 1 | **`conLadeOverlay.Fill`** |
| `RGBA(220, 220, 220, 1)` | 1 | `dpDatumRaum.IconBackground` |
| `RGBA(150, 150, 150, 1)` | 1 | `btnAbbrechenTischePanel.Fill` |
| `RGBA(23, 20, 150, 0.08)` | 1 | `ddStockwerk.HoverFill` — das ist `#171496` mit 8 % Deckung, aber als RGBA geschrieben |
| `RGBA(0, 0, 0, 0.15)` | 1 | `btnHitArea.HoverFill` |
| `RGBA(233, 233, 235, 1)` | 1 | **`Screen1.Fill`** |
| `RGBA(120, 120, 120, 1)` | 1 | `lblDatumLabel.Color` |

**Beobachtung:** `RGBA(32, 54, 71, 1)` steht 132-mal als `BorderColor` an Steuerelementen, deren `BorderThickness` null ist. Das ist der von Power Apps gesetzte Standardwert, kein gestalterischer Entschluss. Für die Farbarbeit sind nur die vier Statusfarben (`#00A96B`, `#4DC398`, `#FFA500`, `#EB3951`), das Markenblau `#171496` und die drei Grautöne relevant.

---

## 10. UMFANG

**186 Steuerelemente auf einem einzigen Screen.** Die App-Prüfung meldet dazu `app-ScreenHasManyControls`.

| Container | Nachkommen | Anteil | Status |
|---|---|---|---|
| `conBuchungen` | 33 | 18 % | aktiv (enthält `conVerwaltenDialog_1` 12 und `conVerwaltenKlein` 5) |
| `conDashboard` | 30 | 16 % | aktiv, **davon 12 tot** (Raum-Teil) |
| `conRaumBuchungenPanel` | 24 | 13 % | **vollständig tot** |
| `conBuchungDialog` | 19 | 10 % | aktiv |
| `conTischBuchungenPanel` | 17 | 9 % | aktiv |
| `conRaumBestätigen` | 13 | 7 % | **vollständig tot** |
| `conGrundriss` | 10 | 5 % | aktiv (davon 4 in der Galerie-Vorlage) |
| `conVerwaltenDialog` | 8 | 4 % | aktiv |
| `conDetailsPopup` | 7 | 4 % | aktiv |
| `conCheckinDialog` | 6 | 3 % | aktiv |
| `conHeader` | 6 | 3 % | aktiv |
| `conLadeOverlay` | 1 | 1 % | aktiv |
| 12 Container selbst | 12 | 6 % | — |

**Löschbar ohne Funktionsverlust: 51 Steuerelemente (27 %).**
`conRaumBuchungenPanel` samt 24 Kindern (25), `conRaumBestätigen` samt 13 Kindern (14), `galRaumbuchungenHeute` samt 8 Kindern (9), `lblRaumLeer`, `lblMyMeetings`, `btnRaumHinzufügen` (3).

### Zur Frage „welche Steuerelemente werden nirgends referenziert"

Diese Frage führt in die Irre, deshalb beantworte ich sie in zwei Teilen.

**Teil 1 — Steuerelemente, deren Name in keiner anderen Formel vorkommt: 93 von 186.** Das ist aber **kein Hinweis auf Totes**. Eine Beschriftung, die Text anzeigt, ist nützlich, auch wenn kein anderes Steuerelement ihre Position oder Breite referenziert. Die Liste wäre hier nur Rauschen.

**Teil 2 — Steuerelemente, die tatsächlich nie sichtbar werden.** Das ist die nützliche Liste, und sie ist identisch mit dem toten Raum-Zweig aus Abschnitt 5.1, plus:

| Steuerelement | Zeile | Warum nie sichtbar |
|---|---|---|
| `conDashboard.lblTischLeer` | 626 | `Visible: =galTischbuchungenHeute.AllItemsCount = 0` — erreichbar, aber `conBuchungen.lblTischLeer_1` (Z. 4118) hat **dieselbe Bedingung auf dieselbe Galerie**, obwohl es im Buchungen-Tab sitzt und dort `galAlleTischbuchungen` gemeint sein müsste. Das ist ein Fehler: Der Hinweis „-Keine Einträge-" im Buchungen-Tab richtet sich nach der Dashboard-Galerie. |

`UNSICHER:` Ob `lblTischLeer_1.Visible` absichtlich auf `galTischbuchungenHeute` zeigt, kann ich nicht entscheiden. Falls nicht, müsste dort `galAlleTischbuchungen.AllItemsCount = 0` stehen.

---

## 11. ABWEICHUNGEN ZU KONTEXT.md

Abschnitt 2 von `KONTEXT.md` stammt aus der App „App". Hier steht, wo „Tischbuchung" davon abweicht.

### 11.1 Container

**Die Liste der zwölf Container stimmt vollständig.** Alle zwölf Namen existieren so. Abweichungen:

| Punkt | `KONTEXT.md` | Quellcode |
|---|---|---|
| Reihenfolge | `conLadeOverlay`, `conHeader`, `conBuchungen`, `conVerwaltenDialog`, `conDetailsPopup`, `conCheckinDialog`, `conBuchungDialog`, `conRaumBestätigen`, `conRaumBuchungenPanel`, `conTischBuchungenPanel`, `conDashboard`, `conGrundriss` | `conGrundriss`, `conDashboard`, `conTischBuchungenPanel`, `conRaumBuchungenPanel`, `conRaumBestätigen`, `conBuchungDialog`, `conCheckinDialog`, `conDetailsPopup`, `conVerwaltenDialog`, `conBuchungen`, `conHeader`, `conLadeOverlay` — **exakt umgekehrt** |
| Nicht erwähnt | — | `conBuchungen.conVerwaltenDialog_1` (12 Steuerelemente) und `conBuchungen.conVerwaltenKlein` (5). Zwei weitere Verwalten-Dialoge, die es neben `conVerwaltenDialog` gibt. |
| `conDetailsPopup` | „laut Doku unvollständig befüllt" | Trifft zu: `lblStatus.Text` ist die Konstante `"Besetzt"`, nicht aus der Buchung abgeleitet. |

### 11.2 `App.OnStart`

| Punkt | `KONTEXT.md` | Quellcode |
|---|---|---|
| Anzahl `Set(` | „rund 60" | **48** |
| `ClearCollect` | 2 | 2 ✓ |
| `colTischPositionen` | „OG, 13 Einträge" | **16 Einträge** — 13 `OG Desk` **plus 3 `Quiet Desk`** (`Quiet Desk 1–3`). Die Quiet Desks fehlen in der Notiz völlig. |
| `colTischPositionenUG` | „17 Einträge + Big Table" | **18 Einträge** ✓ (17 `UG Desk` + `Big Table`) |
| `varWiederholenBis = Today() + 14` | ✓ | ✓ (Z. 59) |
| `varAnsichtsDatum = Today()` | ✓ | ✓ (Z. 105) |
| `varAusgewaehltesStockwerk = "OG"` | ✓ | ✓ (Z. 106) |
| `varAktiverTab = "dashboard"` | ✓ | ✓ (Z. 44) |
| `varGalleryNeuAufbauen = 0` | ✓ | ✓ (Z. 114) |
| `varIsLoading = false` | ✓ | ✓ (Z. 137) |
| `varSpinnerWinkel = 0` | ✓ | ✓ (Z. 138) |
| `colAusgewaehlteBuchungen` per `Clear()` | ✓ | ✓ (Z. 110) |
| **In der Notiz nicht erwähnt** | — | `varSelectedBuchungTab` (Z. 100) |
| **In der Notiz erwähnt, in `OnStart` nicht vorhanden** | `varZeigeTischBuchungForm` ist dort gar nicht gelistet, wird aber gebraucht | wird **nie initialisiert**, obwohl 6× verwendet |
| **Dito** | `varDetailsTisch` fehlt in beiden | wird nie initialisiert, aber in `conDetailsPopup.X`/`.Y` gelesen |
| `varProfilFarbe` mit `RandBetween(1; 8)` | „vermutlich unbeabsichtigt" | **Bestätigt, Z. 63–76.** Acht Pastellfarben, bei jedem Start zufällig. |

### 11.3 Toter Code

| Variable | `KONTEXT.md` | Quellcode |
|---|---|---|
| `varZeigeRaumBuchungForm` | tot | **nicht tot** — wird in `conDashboard.Visible` gelesen |
| `varAusgewähltRaum` | tot | wird gelesen, aber nur im unerreichbaren Raum-Zweig |
| `varAusgewählteStartzeit` / `-Endzeit` | tot | dito |
| `varZeigeRaumBestätigung` | tot | dito |
| `varZeigeRaumInfo` | tot | **tot ✓**, amtlich bestätigt |
| `varZeigeRaumVerwalten` | tot | **tot ✓**, amtlich bestätigt |
| `varZoom` | „nicht entfernt" | ✓ richtig, **und wird aktiv gelesen** in `Circle1.Height`/`.Width` |
| `varPanX` / `varPanY` | „nicht entfernt" | ✓ richtig, **und wirklich tot** — null Leser |
| **Nicht in der Notiz** | — | `varZeigeVerlaengern`, `varStockwerkDropdownOffen`, `varWiederholenBis`, `varWiederholenBisGewaehlt`, `varMehrfachAuswahlModus` sind ebenfalls tot |

### 11.4 Datenmodell (Abschnitt 3 von `KONTEXT.md`, laut `KORREKTUR.md` eigentlich gültig — ist es nicht)

| Angabe | `KONTEXT.md` | `References/DataSources.json` |
|---|---|---|
| `Tische` Titelspalte | `Title` | intern `Title`, **Anzeigename `Titel`** — die App nutzt `Titel` |
| `Tische.Standort` | existiert | **existiert nicht.** Die Spalte heißt **`Geschoss`** und ist eine Auswahlspalte (`Geschoss.Value`, Werte `"OG"`/`"UG"`) |
| `Tische.Aktiv` | existiert | **existiert nicht.** Kein Feld dieses Namens in der Liste. |
| `Tische.Ausrichtung` (Choice) | ✓ | ✓ — **und zusätzlich `Ausrichtung2`**, ebenfalls eine Auswahlspalte. Beide werden von der App **nicht benutzt**. |
| `Tische.X`, `.Y` | „existieren, werden nicht benutzt" | ✓ bestätigt, Typ `number`, null Treffer im Quellcode |
| `Tischbuchungen.Tisch` | Lookup → `Tische.Title` | ✓ Lookup, mit `Tisch#Id` und `Tisch.Value` |
| `Tischbuchungen` Check-in | „Schreibweise ungeklärt" | **geklärt:** intern `Checkedin`, Anzeigename `CheckedIn` |
| **Nicht in der Notiz** | — | **`Tischbuchungen.SerienID`**, Typ `string`, read-write, filterbar mit `eq` und `startswith`. **Von der App nie benutzt.** |
| `Tischbuchungen.Raum` | — | existiert nicht in `Tischbuchungen` (nur in `Raumbuchungen`) |

**Folge für `AUFGABE_UMBAU.md` Punkt 5:** Das dort vorgeschlagene Muster `Filter(Tische As T; T.Aktiv && T.Standort = varAusgewaehltesStockwerk; …)` ist **zweifach falsch** — `Aktiv` gibt es nicht, und `Standort` heißt `Geschoss` und braucht `.Value`. Korrekt wäre `Filter(Tische As T; T.Geschoss.Value = varAusgewaehltesStockwerk; …)`. Das ist nicht Teil dieses Laufs, aber du solltest es wissen, bevor du Punkt 5 angehst.

### 11.5 Technische Kernprobleme (Abschnitt 4 von `KONTEXT.md`)

| Behauptung | Befund |
|---|---|
| §4.1 „Master-Bedingung ist das Hauptproblem, nicht delegierbar" | **Von der App-Prüfung nicht bestätigt.** Keine der 56 Delegationswarnungen trifft die Galerie-Vorlage. Siehe Abschnitt 3, inkl. `UNSICHER`. |
| §4.2 „sechs Stellen, darunter `btnEincheckenHeute.Visible`" | Zahl ✓, **Liste falsch**: `btnEincheckenHeute` hat keine `Visible`-Property. Die sechste Stelle ist `btnHitArea.OnSelect`. |
| §4.3 „`Refresh` in einer `ForAll` ist die Ursache" | **Widerlegt.** Neun `Refresh`, keines in einer Schleife. Die Ursache sind die N Einzelschreibvorgänge in der `ForAll` selbst. |
| §4.4 „Doppelbuchung möglich, Read-then-Write" | **Bestätigt.** `btnSpeichern.OnSelect` Z. 2774: `CountRows(Filter(bestehendeBuchungenTisch; …)) = 0` und erst danach `Patch`. `bestehendeBuchungenTisch` wird im äußeren `With` **einmal** gelesen (Z. 2734) und dann für alle Schleifendurchläufe wiederverwendet — innerhalb einer Serienbuchung kollidieren die eigenen neuen Einträge also nicht einmal miteinander. |
| §4.5 „`IfError` kommt nirgends vor" | **Bestätigt.** Null Treffer im gesamten Quellcode. |

### 11.6 Power-Fx-Regeln (Abschnitt 6 von `KONTEXT.md`)

| Regel | Befund |
|---|---|
| „Keine Kommentare in Power Fx" | **Widerlegt.** Sieben `//`-Kommentare im veröffentlichten Code, davon drei in `App.Formulas`. |
| „Interner Spaltenname ist immer `Title`, nie `Titel`" | **Irreführend.** Intern stimmt es, in Formeln gilt `Titel`. |
| „Personenfeld: immer das volle Schema mit `'@odata.type'`" | **In der App nicht eingehalten.** Beide `Patch` auf `Tischbuchungen` (Z. 1013–1020 und Z. 2781–2788) schreiben `Person` **ohne** `'@odata.type'`. Nur der tote `Patch` auf `Raumbuchungen` (Z. 2306) hat es. Es funktioniert offenbar trotzdem. |
| „`Patch` immer auf frischem `LookUp(…; ID = …)`" | **Mehrheitlich eingehalten**, mit einer Ausnahme: `btnStornieren.OnSelect` (Z. 3225) ruft `Remove(Tischbuchungen; varSelectedBuchung)` direkt auf der Variablen auf. |
| „`Fill` wird ignoriert bei `DisplayMode = Disabled`" | Relevant: alle sechs Plus-Buttons und `btn5Std`/`btn9Std` setzen `DisplayMode` **und** `Fill` auf dieselbe Bedingung. Bei `Disabled` greift `DisabledFill`, nicht `Fill` — die aufwendige `Fill`-Formel ist in genau dem Fall wirkungslos, für den sie gebaut wurde, und kostet trotzdem einen Datenzugriff. |

---

## FAZIT

Am meisten überrascht hat mich, dass **deine Hauptvermutung falsch ist**: Es steht kein einziges `Refresh` in einer `ForAll` — die neun Vorkommen sind alle korrekt platziert, und die Serienbuchung ist langsam, weil die Schleife N einzelne `Patch`-Aufrufe absetzt, was Microsofts eigene App-Prüfung dreimal als `app-ForAllWithMutation` meldet. Die zweite Überraschung ist, dass die App-Prüfung **die Master-Bedingung überhaupt nicht beanstandet**, obwohl `KONTEXT.md` sie zum Hauptproblem erklärt: alle 56 Delegationswarnungen hängen an `CountRows(Filter(…))` in den Verlängern- und Dauer-Buttons, und 10 davon an totem Raumcode. Der Grundriss bleibt trotzdem teuer, nur aus einem anderen Grund — 96 bis 108 `LookUp`-Auswertungen pro Render, die eine Tages-Collection auf einen Zugriff zusammenzieht. Den Bug „doppeltes Ladesymbol" habe ich gefunden: `Screen1.LoadingSpinner = LoadingSpinner.Data` lässt den eingebauten Spinner neben deinem selbstgebauten `conLadeOverlay` laufen, und ein Timer für `varSpinnerWinkel` existiert nirgends.

Das größte Problem sehe ich woanders, und es steht auf keiner deiner Listen: **das Datenmodell und der Code haben sich auseinanderentwickelt, ohne dass es jemandem auffällt.** `Tische.Aktiv` gibt es nicht, `Standort` heißt `Geschoss`, `Ausrichtung` existiert zweimal und wird nie benutzt, `X` und `Y` liegen in SharePoint **und** hartcodiert in `App.OnStart`, und `Tischbuchungen.SerienID` wartet ungenutzt — eine Spalte, die genau das Problem lösen würde, an dem die Serienbuchung krankt. Dazu 51 von 186 Steuerelementen in einem Raum-Zweig, der über einen unsichtbaren Button erreicht werden müsste. Jede Formel, die du nach `KONTEXT.md` statt nach dem Quellcode schreibst, ist falsch, und SharePoint sagt dir das nicht.

Zwei Punkte verdienen echte Sorge statt Aufräumarbeit: `btnStornieren.OnSelect` ist eine einzeilige Löschoperation ohne Prüfung, ohne Fehlerbehandlung und ohne Rückmeldung, und die Kollisionsprüfung der Serienbuchung liest den Bestand **einmal vor** der Schleife und entscheidet dann für alle Termine auf diesem Stand. Beides geht lange gut und dann plötzlich nicht mehr.

---

## Offene Fragen an Josias

1. **Steht im Studio ein gelbes Warndreieck neben `Gallery1.Rectangle1.Fill`?** Davon hängt ab, ob die Delegationsarbeit dort ansetzen muss oder ob die 96 `LookUp`s „nur" ein Mengenproblem sind.
2. **Steht ein Warndreieck neben `galAlleTischbuchungen.Items`?** Das entscheidet über Bug 3.
3. **Soll `lblTischLeer_1.Visible` auf `galAlleTischbuchungen` zeigen statt auf `galTischbuchungenHeute`?** Sieht nach einem Kopierfehler aus.
4. **Wofür war `Tischbuchungen.SerienID` gedacht?** Wenn die Spalte frei ist, löst sie die Serienbuchung elegant.
5. **Wofür ist `Tische.Ausrichtung2`?** Zwei Auswahlspalten gleichen Namens, beide ungenutzt.
6. **Soll der eingebaute Screen-Spinner weg oder dein `conLadeOverlay`?** Einer von beiden muss gehen.
