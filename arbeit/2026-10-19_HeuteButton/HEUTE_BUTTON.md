# Knopf „Heute“ im Dashboard (19.10.2026)

Für Josias, Desktop-App „Tischbuchung“. Grundlage: **Export 19.10. 10:35** (`TischbuchungHeutebutton_20261019103505.zip`). Erzeugt und maschinell geprüft mit `werkzeuge/heute_button.py` (0 Fehler, Mutationstest 5 von 5 erkannt). **Nicht unabhängig geprüft, in Studio nicht getestet.** Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Ein neuer Knopf `btnHeuteDatum` („Heute“) in `conDashboard`, rechts neben dem Datum.** Sonst ändert sich **keine** bestehende Property.
- **Ein Klick setzt das Ansichtsdatum auf heute.** Dadurch stellen sich alle Ansichten um, die am Ansichtsdatum hängen (belegt, maschinell gesucht):
  - die Liste „My personal desk“,
  - der Grundriss (Farben und Kürzel),
  - der Text „Heute“ über dem Datum,
  - das vorgeschlagene Datum im Buchungsdialog und im Panel „Tisch buchen“ (`dpDatum.DefaultDate`, `dpDatumTischePanel.DefaultDate`).
- **Er lädt den Grundriss mit derselben Zeile wie die Datumsauswahl** (`dpAnsichtsDatum.OnChange`, zeichengleich). Es gibt also keine neue Abfrageart und keinen Schreibzugriff.
- **Er ist nur zu sehen, wenn nicht heute gewählt ist.** Dann steht nie „Heute“ doppelt da.
- **Er ist grau und gesperrt, solange geladen wird oder der Buchungsdialog, ein Verwalten-Dialog oder die Check-in-Frage offen ist.** Der Grund: Das Datum im offenen Buchungsdialog hängt am Ansichtsdatum und würde sonst mitten im Buchen springen (belegt: `dpDatum.DefaultDate` liest `varAnsichtsDatum`).
- **Design:** Markenblau `#171496` wie die Tab-Knöpfe, weiße Schrift (Kontrast 13,3 : 1, gerechnet), halbfett, runde Ecken 10, Höhe 32 mittig zur Datumszeile.

## 1. Neues Steuerelement anlegen
1. In der Strukturansicht **`conDashboard`** markieren.
2. Einfügen → **Schaltfläche** (klassisch) → umbenennen in **`btnHeuteDatum`**.
3. Prüfen: `btnHeuteDatum` liegt **in** `conDashboard`.
4. Die Properties unten setzen. Jede Property wird **ganz** ersetzt. Properties, die nicht in der Liste stehen, bleiben auf Standard.

## 2. Properties von `btnHeuteDatum`

| Property | Wert (deutsche Schreibweise) |
|---|---|
| `Text` | `"Heute"` |
| `X` | `Image4.X + Image4.Width + 5` |
| `Y` | `dpAnsichtsDatum.Y + (dpAnsichtsDatum.Height - Self.Height) / 2` |
| `Width` | `90` |
| `Height` | `32` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `12` |
| `FontWeight` | `FontWeight.Semibold` |
| `Fill` | `ColorValue("#171496")` |
| `Color` | `RGBA(255; 255; 255; 1)` |
| `HoverFill` | `ColorFade(Self.Fill; -20%)` |
| `HoverColor` | `RGBA(255; 255; 255; 1)` |
| `PressedFill` | `ColorFade(Self.Fill; -30%)` |
| `PressedColor` | `RGBA(255; 255; 255; 1)` |
| `BorderThickness` | `0` |
| `DisabledFill` | `ColorFade(ColorValue("#171496"); 50%)` |
| `DisabledColor` | `RGBA(255; 255; 255; 1)` |
| `RadiusTopLeft` | `10` |
| `RadiusTopRight` | `10` |
| `RadiusBottomLeft` | `10` |
| `RadiusBottomRight` | `10` |
| `AccessibleLabel` | `"Datum auf heute zurücksetzen"` |

#### `btnHeuteDatum.Visible`

```
varAnsichtsDatum <> Date(Year(Coalesce(varJetztTakt; Now())); Month(Coalesce(varJetztTakt; Now())); Day(Coalesce(varJetztTakt; Now())))
```

#### `btnHeuteDatum.DisplayMode`

```
If(!varIsLoading && !varZeigeDialog && !varZeigeVerwalten && !varZeigeCheckin; DisplayMode.Edit; DisplayMode.Disabled)
```

#### `btnHeuteDatum.OnSelect`

```
If(
  !varIsLoading && !varZeigeDialog && !varZeigeVerwalten && !varZeigeCheckin;
  Set(varAnsichtsDatum; Today());;
  Reset(dpAnsichtsDatum);;
  Set(varZeigeDetails; false);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())))
)
```

Was `OnSelect` tut, Zeile für Zeile:
1. Nur wenn nicht geladen wird und kein Dialog offen ist (dieselbe Bedingung wie `DisplayMode`).
2. `varAnsichtsDatum` = heute.
3. `Reset(dpAnsichtsDatum)`: Der Kalender zeigt beim nächsten Öffnen heute. `dpAnsichtsDatum.DefaultDate` ist nicht gesetzt, also gilt der Standard „heute“ (belegt).
4. Ein offenes Details-Popup einer Kachel schließen, weil es sonst den alten Tag zeigt.
5. Grundriss laden: genau die Zeilen aus `dpAnsichtsDatum.OnChange` (maschinell verglichen), mit Stempel für die Grundriss-Sperre.

**`Visible`** rechnet mit dem Takt `varJetztTakt` statt mit `Today()`. Der Grund: `Today()` wird in Anzeigeformeln nicht von selbst neu berechnet (Regel aus dem Projekt). So stimmt die Anzeige auch nach Mitternacht.

## 3. Test (Zeitachse)
| ✓ | Schritt | Erwartung |
|---|---|---|
| ☐ | 1 App neu öffnen (Datum ist heute) | Kein Knopf „Heute“ zu sehen |
| ☐ | 2 Über das Datum einen Tag in drei Monaten wählen | Text zeigt das Datum, blauer Knopf „Heute“ rechts daneben. Grundriss und Liste zeigen diesen Tag |
| ☐ | 3 „Heute“ tippen | Text „Heute“, Knopf verschwindet. Grundriss und Liste zeigen heute. Das Datum erneut öffnen: Der Kalender steht auf heute |
| ☐ | 4 Wieder einen fernen Tag wählen, dann eine **freie** Kachel antippen (Buchungsdialog offen) | Knopf grau, Tippen tut nichts. Dialog abbrechen: Knopf wieder blau |
| ☐ | 5 Ferner Tag, **belegte** Kachel antippen (Details-Popup), dann „Heute“ | Popup schließt, alles zeigt heute |
| ☐ | 6 Nach Schritt 5 „Tisch Buchen“ öffnen | Datum im Panel ist heute |
| ☐ | 7 Optional Monitor: in Schritt 3 die Abfragen zählen | 1 Abfrage auf `Tischbuchungen` für den Grundriss, dazu die Liste „My personal desk“. Bei 2 Grundriss-Abfragen siehe U1 |

## 4. Rückfall
`btnHeuteDatum` löschen. Es wurde keine andere Property geändert.

## 5. UNSICHER
| Nr | Was | Prüfen / Folge |
|---|---|---|
| U1 | Ob `Reset(dpAnsichtsDatum)` auch `dpAnsichtsDatum.OnChange` auslöst | Test 7. Wenn ja, lädt der Grundriss einmal doppelt (eine Abfrage mehr, nur bei diesem Klick). Das Ergebnis ist trotzdem richtig |
| U2 | `Image4.Width` ist im Export nicht gesetzt (Standardbreite). Der Knopf steht 5 rechts davon | Test 2. Sitzt er zu weit rechts, `X` auf eine feste Zahl setzen (z. B. `175`) |
| U3 | Hover- und Druckfarbe sind wie bei den Tab-Knöpfen abgedunkelt | Sichtprüfung |

## 6. Hinweise zum Export 19.10. (belegt, maschinell)
- Gegenüber dem 13.10. ist nur neu: `Container2_1` in `galAlleTischbuchungen` (runde Karten), die Radien von `btnEincheckenHeute` und `Rectangle4_2.Fill` = transparent.
- **Nachtrag 5 und Nachtrag 6 sind weiterhin nicht drin.** Alle 21 bzw. 25 Vorher-Fassungen passen noch, die Blöcke gelten unverändert. Die Storno-Bestätigung (N1–N3) und die gesperrte Check-in-Karte bei „Verfallen“ (R1) fehlen also in der App, die seit 14.10. live ist.
- Die gelben Dreiecke im Bildschirmfoto sind Hinweise der App-Prüfung in Studio, keine Fehler. Die App-Prüfung meldet 94 Hinweise und 0 Fehler, wie am 13.10. (belegt, `AppCheckerResult.sarif`). Darunter fehlt bei `dpAnsichtsDatum`, `galTischbuchungenHeute` und `Icon1_1` die Barrierefreiheits-Beschriftung (`AccessibleLabel`), das passt zur Lage der Dreiecke (geschlussfolgert).

## Anhang: Maschinelle Prüfung
```
Knopf btnHeuteDatum: 25 Properties, 1 neues Steuerelement in conDashboard. Grundlage: Export 19.10. 10:35.
varAnsichtsDatum lesen (stellen sich mit um): Circle1.BorderStyle, Circle1.Fill, Icon1.OnSelect, Icon1_1.OnSelect, Image6.OnSelect, Label1.Text, Label16.Text, Rectangle1.Fill, btnEinchecken.OnSelect, btnGrundrissAktualisieren.OnSelect, btnHitArea.OnSelect, btnHitArea_1.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnStornieren.OnSelect, btnStornierenKlein.OnSelect, btnStornieren_1.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect, ddStockwerk.OnChange, dpDatum.DefaultDate, dpDatumTischePanel.DefaultDate, galTischbuchungenHeute.Items, icoAktualisierenGrundriss.OnSelect
varAnsichtsDatum/dpAnsichtsDatum schreiben bisher: App.OnStart, Timer1.OnTimerEnd, dpAnsichtsDatum.OnChange
dpAnsichtsDatum.DefaultDate nicht gesetzt (Standard Today()) -> Reset(dpAnsichtsDatum) zeigt heute
Lage: Y 33.5–65.5 (lblMyPersonalDesk ab 75), X = Image4.X + Image4.Width + 5 = 85 + Image4.Width + 5 (Image4.Width im Export Standard, nicht gesetzt)
Kontrast Weiß auf Fill (23, 20, 150): 13.3:1
Textbreite „Heute“ bei Größe 12 halbfett ca. 45 (geschätzt) < 90
Prüfung: 0 Fehler
```
