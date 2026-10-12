# Antwort an den Handy-Chat: Feature „Tisch zeigen“ (12.10.2026)

Grundlage:
- Desktop-Export 12.10. (`quellen/2026-10-12_Desktop/`, zeichengleich mit 08.10. 14:26) und Handy-Export 08.10. 14:25.
- Bilder und Tabelle erzeugt mit `werkzeuge/tisch_zeigen.py`.

Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Konzept passt.** Ein Bild, ein Hervorhebungs-Rechteck, Overlay von unten, keine Abfrage. Overlay statt Aufklappen in der Karte empfehle ich ebenfalls.
- **Wichtiger Befund (belegt, Bilder angesehen): Die Grundriss-Bilder der Desktop-App enthalten keine Tische.** Die Tische zeichnet die Desktop-App erst als Rechtecke darüber (`Gallery1 > Rectangle1`). Mit dem Originalbild und nur einem Rechteck sähe man am Handy keinen anderen Tisch.
- **Deshalb geliefert: 4 fertige Handy-Bilder mit eingezeichneten Tischen** (weiß, grauer Rand, Nummer).
  - Je Geschoss gibt es eine Fassung quer und eine hoch (90° gedreht).
  - Zugeschnitten auf das Gebäude, JPEG, 109–115 KB.
  - Dazu die Positionstabelle in **Anteilen 0–1** für beide Lagen. Es gibt also nur noch **ein** Rechteck für den eigenen Tisch.
- **Empfehlung: Hochformat-Bild.** Auf dem Handy (Layout 640 × 1136, hoch, belegt) wird ein Tisch damit etwa 2,5-mal so groß wie quer.
- **Schlüssel: Tischname**, wie in der Desktop-App. Begründung in Punkt 3.
- **Reihenfolge wie von dir vorgeschlagen:** erst umbenennen und die neuen Positionen festlegen. Danach `werkzeuge/tisch_zeigen.py` auf den neuen Desktop-Export laufen lassen, dann kommen neue Bilder und eine neue Tabelle. Das dauert Minuten.

## 1. Deine Fragen
**1) Positionstabellen, Maßstab** (belegt aus dem Desktop-Export)
- `colTischPositionen` (OG, 16 Tische) und `colTischPositionenUG` (UG, 18 Tische inkl. Big Table) in `App.OnStart`. Felder `Tisch`, `X`, `Y`, `Ausrichtung`.
- Die Werte sind **Pixel im Originalbild 1920 × 1080**:
  - Das Bild-Steuerelement ist `BasisBreite × BasisHoehe` = 1920 × 1080, mal `BasisSkalierung`, mit `ImagePosition.Fit`.
  - Die Bilder selbst sind 1920 × 1080.
- **Kachelmaße** (`App.Formulas`):

  | Geschoss | quer | hoch | Sonderfälle |
  |---|---|---|---|
  | OG | 101 × 60 | 60 × 101 | Quiet Desk −10 / −7 |
  | UG | 89 × 52 | 52 × 89 | Big Table 220 × 52 |

- **Achtung, Y-Versatz** (belegt, `Rectangle1.Y`):
  - Die Galerie verschiebt jede Zeile um 1 px (`TemplateSize` 1, `TemplatePadding` 0). Die Werte wurden mit diesem Versatz eingemessen.
  - Das echte Y im Bild ist `Y + (Nr − 1) / 0,4589` (`BasisSkalierungReferenz` = 881 / 1920). Dabei ist `Nr` die Reihenfolge in `Filter(Tische; Geschoss = …)`.
  - Ich habe angenommen, dass diese Reihenfolge der Tabelle entspricht (geschlussfolgert). Gestützt wird das durch das Bild: Ohne Versatz lägen UG 13, 15, 16, 17 und Q1 über der Außenwand, mit Versatz liegen sie im Raum.
  - **In den gelieferten Anteilen ist der Versatz schon eingerechnet.** Du musst nichts mehr umrechnen.
- **Anteile** in `tischplan_positionen.json` und als fertiges `Table(…)` in deutscher Schreibweise: `tabelle_hoch_de.txt` und `tabelle_quer_de.txt`.
  - Felder: `Tisch`, `Geschoss`, `X`, `Y`, `B`, `H`, alle als Anteil an Bildbreite bzw. Bildhöhe.
  - Zuschnitt: (60, 200)–(1860, 920) im Original. Bild quer 1800 × 720, hoch 720 × 1800.

**2) Bilddateien**
- In der Desktop-App liegen sie in den Ressourcen `grundriss_transparent (1)` (OG, `imgGrundrissOG.Image`) und `grundriss_UG_bearbeitet_PREVIEW (3)` (UG, `imgGrundrissUG.Image`). Beide PNG, 1920 × 1080, etwa 430 KB, transparent.
- **Für das Handy bitte nicht die Originale nehmen, sondern die gelieferten:**
  - `tischplan_OG_hoch.jpg`, `tischplan_UG_hoch.jpg` (empfohlen)
  - oder `…_quer.jpg`
  - In Studio: Medien → Hochladen. Der Name in der App ist dann z. B. `tischplan_OG_hoch`.

**3) Schlüssel Name oder ID**
- **Name**, aus drei Gründen:
  - Die Desktop-App schlüsselt Positionen über den Namen (belegt).
  - Die Nummern stehen im Bild.
  - Beim Umbenennen ändern sich ohnehin Bild und Tabelle, die ID bringt dann nichts.
- Die IDs der Tische kenne ich nicht, sie stehen nicht im Export.
- **Später besser für beide Apps:** Positionen als Spalten in der Liste `Tische` (`PosX`, `PosY`, `Ausrichtung`). Dann braucht ein Umbenennen oder ein neuer Tisch keine Codeänderung mehr. Das ist nach dem Go-Live zu prüfen, weil es auch die Desktop-App umbaut.

**4) Nur der eigene Tisch**
- Ja. Die anderen Tische sind im Bild neutral eingezeichnet, ohne Status.
- Es gibt keine Abfrage und keine 34 Steuerelemente.

**5) Feste Plätze (JA, SK) im Bild?**
- **Nein** (belegt, beide Bilder angesehen). Die Originalbilder enthalten gar keine Tische und keine Kürzel.
- In meinen Bildern stehen genau die 34 Tische aus den Positionstabellen: OG 1–13, Q1–Q3, UG 1–17 und Big Table.
- Gibt es in Wirklichkeit weitere feste Plätze, fehlen sie im Plan. Wenn Josias sie sehen will, sag mir Lage und Kürzel. Ich zeichne sie grau und ohne Nummer ein.

**6) Blöcke im gewohnten Stil**
- Ich erzeuge sie, sobald drei Dinge vorliegen:
  1. Josias' Entscheidungen: Overlay, Farbe, Hinweistext.
  2. Ein Handy-Export **nach H8**.
  3. Umbenennung und Positionen sind fertig.
- Bis dahin die Bausteine unten.

## 2. Bausteine (Vorschlag, geschlussfolgert, nicht in Studio getestet)
- **Tabelle:** Am besten als benannte Formel in `App.Formulas`:
  ```
  TischBild = <Inhalt von tabelle_hoch_de.txt>;
  ```
  - Sie wird erst berechnet, wenn sie gebraucht wird. `App.OnStart` (mit H8) bleibt unberührt, es gibt keine Sammlung beim Start.
  - Die Handy-App hat noch kein `App.Formulas` (belegt). Benannte Formeln laufen aber in der Desktop-App mit denselben App-Einstellungen (belegt).
  - Alternative: `ClearCollect(colTischBild; <Tabelle>)` am Ende von `App.OnStart`.
- **Knopf in der Karte** (`OnSelect`):
  ```
  Set(varTischBild; LookUp(TischBild; Tisch = ThisItem.Tisch.Value));; Set(varZeigeTisch; !IsBlank(varTischBild.Tisch))
  ```
  Ist der Tisch nicht in der Tabelle, öffnet sich nichts. Optional `Notify` ergänzen.
- **Bild** (`imgTischPlan`, im Overlay, `ImagePosition.Fit`):

  | Property | Formel |
  |---|---|
  | `Image` | `If(varTischBild.Geschoss = "OG"; tischplan_OG_hoch; tischplan_UG_hoch)` |
  | `Height` | `Min(Parent.Height - 140; (Parent.Width - 32) * 2,5)` |
  | `Width` | `Self.Height / 2,5` |
  | `X` | `(Parent.Width - Self.Width) / 2` |

  Seitenverhältnis 1800 / 720 = 2,5. So gibt es keinen weißen Rand, und die Anteile gelten genau.
- **Rechteck** (`recTischMarke`):

  | Property | Formel |
  |---|---|
  | `X` | `imgTischPlan.X + varTischBild.X * imgTischPlan.Width` |
  | `Y` | `imgTischPlan.Y + varTischBild.Y * imgTischPlan.Height` |
  | `Width` | `varTischBild.B * imgTischPlan.Width` |
  | `Height` | `varTischBild.H * imgTischPlan.Height` |
  | `Fill` | `Transparent` |
  | `BorderThickness` | `5` |
  | `BorderColor` | Josias' Farbe |

  Das Rechteck muss in der Strukturansicht über dem Bild liegen.
- **Größe am Handy:** Mit dem Hochformat-Bild ist ein Tisch etwa 30–55 Einheiten groß (geschlussfolgert aus 640 × 1136). Quer wären es etwa 12–20.
- **Hinweistext** (optional): `"Obergeschoss"`/`"Untergeschoss"` aus `varTischBild.Geschoss`. Eine Lage wie „hinten rechts“ müsste Josias je Tisch festlegen.

## 3. UNSICHER
| Nr | Was | Prüfen |
|---|---|---|
| T-U1 | Y-Versatz setzt voraus, dass die SharePoint-Reihenfolge der Tische der Tabellenreihenfolge entspricht | Josias vergleicht `tischplan_OG_quer.jpg` und `tischplan_UG_quer.jpg` mit dem Desktop-Grundriss. Die Tische müssen an denselben Stellen stehen. Abweichung → mir melden |
| T-U2 | Benannte Formel `TischBild` in der Handy-App, dazu das Schlusszeichen: Im Export (englisch) steht `;`, in der deutschen Studio-Anzeige vermutlich `;;` | App-Prüfung nach dem Einfügen. Meldet Studio einen Fehler am Ende, das andere Zeichen nehmen. Notfalls die Sammlung in `App.OnStart` |
| T-U3 | Beim Umbenennen ändern sich Namen, Positionen und vielleicht die Reihenfolge (neuer Tisch). Das Bild ist dann veraltet | nach dem Umbenennen neu erzeugen (Skript) |
