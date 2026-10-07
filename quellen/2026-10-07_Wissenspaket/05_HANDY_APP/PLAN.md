# PLAN.md — Aufbau der Handy-App

**Kurzfassung:** Eine neue Canvas-App im Phone-Format, ein einziger Screen mit drei Bereichen, die über eine Variable umgeschaltet werden, Tab-Leiste unten. Das Gerüst ist ein vertikaler Auto-Layout-Container (Header fix, Inhalt flexibel, Tab-Leiste fix); Dialoge und Lade-Overlay liegen direkt im Screen, nicht im Container. Etwa 45 Steuerelemente gegenüber 186 in der Desktop-App. Gebaut wird in der Reihenfolge Lesen → Einchecken → Verwalten → Buchen, weil Schreiben die meiste Sorgfalt braucht. Diese Datei wird fortgeschrieben, sobald sich etwas ändert.

---

## 1. Architektur

**Neue App, keine Kopie.** Begründung in `ENTSCHEIDUNGEN.md` E-01.

| | |
|---|---|
| Name | `Tischbuchung Handy` |
| Format | Phone, Hochformat |
| Designgröße | 640 × 1136 (Power Apps verdoppelt im Phone-Format das Koordinatensystem) |
| Scale to fit | **aus** |
| Ausrichtung sperren | **an** (Hochformat) |
| Seitenverhältnis sperren | aus (folgt automatisch) |
| Datenquellen | `Tischbuchungen`, `Tische` — **nicht** `Räume`, **nicht** `Raumbuchungen` |
| Steuerelementtyp | klassisch, siehe E-03 unten |

**Folge aus dem verdoppelten Koordinatensystem:** Tippflächen mindestens 90 Einheiten hoch, Fließtext ab Größe 24, Überschriften 32 und mehr, Galerie-`TemplateHeight` um 140. Die 44–48 pt aus dem Auftrag entsprechen hier etwa 90–96 Einheiten.

### E-03 — Klassische Steuerelemente statt moderner (Fluent 2)

Die beiden Hintergrunddokumente widersprechen sich hier. Ich nehme **klassische** Steuerelemente:

- Die Formeln und Eigenschaftsnamen der Desktop-App lassen sich direkt übernehmen (`Fill`, `DisabledFill`, `PressedFill`, `Items.Value`). Bei modernen Steuerelementen heißen viele Eigenschaften anders, und ich müsste jedes Muster neu erfinden statt ein erprobtes zu benutzen.
- Josias pflegt die App allein und kennt ausschließlich klassische Steuerelemente aus der Desktop-App.
- Das Touch-Argument für moderne Steuerelemente löse ich über Größe und Abstand, nicht über den Steuerelementtyp.

Gegenargument, das ich anerkenne: Moderne Steuerelemente sehen auf dem Handy besser aus und sind für Touch gemacht. Das ist ein möglicher späterer Umbau, kein Thema für den ersten Stand.

---

## 2. Bildschirmaufbau

Ein Screen: `scrMobil`.

```
scrMobil
├── conRoot                      vertikaler Auto-Layout-Container, füllt den Screen
│   ├── conHeader                FillPortions 0, feste Höhe ~150
│   ├── conInhalt                FillPortions 1, scrollbar
│   │   ├── conHeute             Visible: varTab = "heute"
│   │   ├── conBuchen            Visible: varTab = "buchen"
│   │   └── conMeine             Visible: varTab = "meine"
│   └── conTabLeiste             FillPortions 0, feste Höhe ~160
├── conDlgHintergrund            direkt im Screen, halbtransparent, sperrt den Hintergrund
├── conDlgVerwalten              direkt im Screen
├── conDlgStorno                 direkt im Screen, Bestätigung
└── conLadeOverlay               direkt im Screen, oberste Ebene
```

**Warum Dialoge und Overlay nicht im Auto-Layout-Container liegen:** In einem Auto-Layout-Container werden `X` und `Y` der Kinder ignoriert, die Kinder werden gestapelt. Ein Dialog, der über allem liegen soll, muss direkt im Screen sitzen.

**Reihenfolge in der Strukturansicht:** Was weiter unten in der Liste steht, liegt visuell oben. `conLadeOverlay` steht deshalb ganz unten.

**Ein Screen statt drei:** Das entspricht dem Muster der Desktop-App (`varAktiverTab`), das Josias kennt. Es spart `Navigate`-Übergänge und die Schwierigkeiten mit `App.StartScreen`. Bei drei Bereichen ohne eigene Zustände ist das die einfachere Lösung.

---

## 3. Die drei Bereiche

### „Heute" (Startansicht)

| Element | Zweck |
|---|---|
| `lblHeuteTitel` | „Heute" plus Datum |
| `galHeute` | eigene Buchungen von heute, die noch nicht vorbei sind |
| in der Galerie: `recKarte`, `lblTisch`, `lblZeit`, `lblStatus`, `btnEinchecken`, `btnVerwaltenHeute` | die Karte |
| `conHeuteLeer` | Hinweis plus Knopf „Tisch buchen", wenn nichts da ist (A11) |

Status auf der Karte nach `ENTSCHEIDUNGEN.md` E-A09: eingecheckt grün „Eingecheckt", sonst orange „Einchecken". Der Einchecken-Knopf ist nur im Zeitfenster V2 aktiv (ab 30 Minuten vor Start bis Ende).

### „Buchen"

Reihenfolge **Datum → Uhrzeit → Tisch** (A12).

| Element | Zweck |
|---|---|
| `dpDatum` | Datum, Standard heute, kein Datum in der Vergangenheit |
| `ddStart`, `ddEnde` | 30-Minuten-Raster, Ende bis 22:00 |
| `btnBis17` | Schnellwahl „bis 17:00" (V9, ohne die teuren Abfragen der Desktop-Knöpfe) |
| `ddTisch` | **nur Tische, die im gewählten Zeitraum frei sind**, ohne „Big Table" |
| `lblKeinTischFrei` | wenn die Liste leer ist |
| `lblZusammenfassung` | „OG Desk 5 · Mi 08.10. · 08:00–17:00" (A13) |
| `btnBuchen` | der einzige schreibende Knopf dieses Bereichs |

### „Meine Buchungen"

| Element | Zweck |
|---|---|
| `galMeine` | alle eigenen kommenden Buchungen, chronologisch, mit Wochentag |
| in der Galerie: `recKarteM`, `lblTischM`, `lblTagM`, `lblZeitM`, `btnVerwaltenM` | die Karte |
| `conMeineLeer` | Leerzustand |

### Dialoge

`conDlgVerwalten`: zeigt die gewählte Buchung und bietet „+1 Std", „+2 Std", „Jetzt beenden", „Stornieren", „Schließen".
`conDlgStorno`: Bestätigung mit „Ja, stornieren" und „Abbrechen" (V8).

---

## 4. Variablen

Alle in `App.OnStart` typgerecht vorbelegt, keine mit `Blank()`.

| Variable | Typ | Startwert | Zweck |
|---|---|---|---|
| `varTab` | Text | `"heute"` | aktiver Bereich |
| `varIsLoading` | Wahrheitswert | `false` | Lade-Overlay |
| `varBuchung` | Datensatz `Tischbuchungen` | `Defaults(Tischbuchungen)` | die im Dialog gewählte Buchung |
| `varBuchungID` | Zahl | `0` | 0 heißt „nichts gewählt"; eindeutiger als eine Prüfung auf dem Datensatz |
| `varZeigeVerwalten` | Wahrheitswert | `false` | Dialog sichtbar |
| `varZeigeStorno` | Wahrheitswert | `false` | Bestätigung sichtbar |
| `varNeuLaden` | Zahl | `0` | Zähler, der die Galerien zum Neurechnen zwingt |

**Keine Variable trägt zwei Datensatztypen.** `varBuchung` ist immer eine Zeile aus `Tischbuchungen`.

**Beim Bauen zu prüfen:** ob `Defaults(Tischbuchungen)` als typgerechter Leerwert funktioniert und was `.ID` dort liefert. Deshalb zusätzlich `varBuchungID` als eindeutiges Kennzeichen.

### Named Formulas (`App.Formulas`)

Werden bei Bedarf ausgewertet, nicht beim Start, und können keine `Set`-Variablen lesen.

| Name | Inhalt |
|---|---|
| `FarbeBlau`, `FarbeGruen`, `FarbeOrange`, `FarbeRot` | `#171496`, `#00A96B`, `#FFA500`, `#EB3951` |
| `MeineMail` | `User().Email` |
| `TagesEndeStunde` | `22` |

---

## 5. Die Formeln, auf die es ankommt

Hier steht die Absicht, nicht die endgültige Syntax. Jede Formel wird beim Bauen gegen das Studio geprüft (P1) und von einem Prüf-Subagenten angegriffen (P5). **Schreibweise unten: invariantes Format mit `,`** — im Studio wird daraus die deutsche Schreibweise mit `;`.

### 5.1 Freie Tische im gewählten Zeitraum (A12, D1)

Eine delegierbare Abfrage über **alle** Tische, danach lokal gegenrechnen:

```
With(
  { s: <Startzeitstempel>, e: <Endzeitstempel> },
  With(
    { belegt: Filter(Tischbuchungen, Startzeit < e && Endzeit > s) },
    Sort(
      Filter(Tische, Titel <> "Big Table" && IsBlank(LookUp(belegt, Tisch.Value = Titel))),
      Titel
    )
  )
)
```

- Die innere Abfrage hat **die Zeitgrenze im Filter** und keinen Tischfilter. Beides ist bei SharePoint delegierbar (`<`/`>` auf DateTime). Das ist der Beleg für D1 und A20.
- `IsBlank(LookUp(...))` und `<>` laufen auf `Tische`, nicht auf `Tischbuchungen`. `Tische` hat etwa 34 Zeilen, weit unter dem Datenzeilenlimit von 1000. Die Delegationswarnung, die Studio hier zeigen wird, ist damit **begründet unkritisch** (A05).
- „Big Table" wird über den Titel ausgeschlossen, weil die Liste keine Spalte hat, die Tische als nicht buchbar markiert (V7).

### 5.2 Der Buchen-Knopf (A14, A15, D2 bis D8)

Ablauf, jeder Schritt mit eigener deutscher Meldung:

1. `Set(varIsLoading, true)` als erste Anweisung
2. Plausibilität: Ende nach Start, Start nicht in der Vergangenheit, Ende nicht nach 22:00 (A15)
3. **Frisch prüfen, ob der Tisch im Zeitraum frei ist** — nicht gegen die Liste von vorhin, sondern mit einer neuen Abfrage (D2). Dasselbe Überschneidungsmuster wie oben, zusätzlich auf diesen Tisch gefiltert.
4. **Frisch prüfen, ob ich selbst zur selben Zeit woanders gebucht habe** (D5, V6): `Filter(Tischbuchungen, Person.Email = User().Email && Startzeit < e && Endzeit > s)` — beides delegierbar.
5. `IfError(Patch(Tischbuchungen, Defaults(Tischbuchungen), { … }), <Fehlerzweig>, <Erfolgszweig>)` mit `Tisch: {Id, Value}` und dem vollen Personenschema aus `APP_WISSEN.md`
6. **Nachlese** (D8, A27): frisch nachlesen, ob die Buchung wirklich dasteht. Die Erfolgsmeldung kommt aus dem Ergebnis dieser Nachlese, nicht aus einer lokalen Zählung.
7. Die Nachlese prüft zugleich, ob **mehr als eine** Buchung für diesen Tisch und Zeitraum existiert (D7, gleichzeitige Buchung). Wenn ja: ehrliche Meldung, keine automatische Rücknahme. Begründung in `FRAGEN_AN_JOSIAS.md` F-12.
8. Aufräumen **nur im Erfolgsfall** (Ü2)
9. `Set(varIsLoading, false)` auf **jedem** Pfad (A29)

**Doppeltipp (D3, A22):** `btnBuchen.DisplayMode` liest `varIsLoading`. Solange gespeichert wird, ist der Knopf gesperrt. Das fehlt in der Desktop-App an jedem Knopf.

### 5.3 Einchecken (A10)

- Knopf nur aktiv, wenn `Now() >= Startzeit - 30 Min` und `Now() <= Endzeit` (V2)
- Buchung **frisch** per `LookUp(Tischbuchungen, ID = varBuchungID)` holen, nicht aus der Variablen (D2, F6)
- Existiert sie nicht mehr: verständliche Meldung statt Netzwerkfehler
- Zeitfenster **zum Klickzeitpunkt** erneut prüfen
- `IfError(Patch(..., { CheckedIn: true }))` — fest auf `true`, nie umschalten, damit ein zweiter Tipp nicht auscheckt (V3)

### 5.4 Verlängern (A17) und „Jetzt beenden" (A18)

- Verlängern: `+1 Std` und `+2 Std` (V5). Beim Speichern **frisch** prüfen: Kollision nur gegen das **neue Stück** (`Startzeit < neueEndzeit && Endzeit > alteEndzeit`), damit die eigene Buchung sich nicht selbst blockiert, und `neueEndzeit` nicht nach 22:00.
- „Jetzt beenden": Endzeit auf `Now()` setzen (V4). Keine Kollisionsprüfung nötig, die Buchung wird nur kürzer. Prüfen, dass die neue Endzeit nach der Startzeit liegt.
- Beide arbeiten mit `varBuchungID` und einem frischen `LookUp`, nie mit einem gespeicherten Datensatz (D4, A23).

### 5.5 Stornieren (A19)

Bestätigungsdialog (V8), dann frisch per `LookUp` holen, `IfError(Remove(...))`, bei bereits gelöschtem Datensatz eine verständliche Meldung.

---

## 6. Reihenfolge des Baus

Lesen zuerst, Schreiben zuletzt. Nach jedem Punkt: kompilieren, zur Laufzeit in Handy-Größe testen, dokumentieren, committen.

| # | Schritt | Kriterien |
|---|---|---|
| 1 | App anlegen, Einstellungen, Datenquellen | A01, A03 |
| 2 | Gerüst: `conRoot`, Header, Tab-Leiste, Lade-Overlay | A06, A07 |
| 3 | „Meine Buchungen" (nur lesen) | A16 |
| 4 | „Heute" (nur lesen) | A08, A09, A11 |
| 5 | Einchecken (erste Schreiboperation) | A10, A25 |
| 6 | Verwalten-Dialog: Verlängern, Jetzt beenden, Stornieren | A17, A18, A19, A23 |
| 7 | „Buchen" mit Frei-Filter | A12, A13 |
| 8 | Buchen-Knopf mit vollem Doppelbuchungsschutz | A14, A15, A20 bis A22, A24, A26, A27 |
| 9 | Härten: Prüf-Subagent, Fehlerpfade, Meldungen | A28, A29, A30 |
| 10 | Übergabe: Anleitung, Abnahme, Testdaten aufräumen | A31, A32, A33 |

---

## 7. Wie ich baue

**Erster Weg:** Canvas Authoring MCP (`.pa.yaml` direkt schreiben, `compile_canvas` prüfen). Braucht .NET 10 SDK, das gerade installiert wird, und Co-Authoring **in der Handy-App** — nicht in der produktiven App, das wäre eine verbotene Änderung.

**Rückfallweg:** Power Apps Studio im Browser bedienen und Formeln über die Code-Ansicht einfügen. Langsamer, aber erprobt.

Ich entscheide nach dem Ausgang der Installation und schreibe das Ergebnis in `FORTSCHRITT.md`.

---

## 8. Was dieser Plan noch nicht entscheidet

- Die Regel bei gleichzeitiger Buchung (D7). Vorerst: ehrlich melden, nichts automatisch zurücknehmen. Vorschlag kommt, wenn der Buchen-Knopf steht (`FRAGEN_AN_JOSIAS.md` F-12).
- Ob die Quiet Desks als buchbar angeboten werden. Standard: ja, sie sind normale Tische.
- Das genaue Aussehen. Farben und Maße stehen fest, die Feinarbeit kommt beim Bauen.
