# Designprüfung der neuen Features (10.11.2026)

Grundlage: **Export 10.11. 08:13** („echt“, `Tischbuchung_echt_10.11.26_20261110081319.zip`). Er ist **zeichengleich mit dem Export vom 25.10.** (alle 2.109 Properties, kein Unterschied, App-Prüfung 94 Hinweise ohne Fehler). In der App ist also noch **keines** der Pakete eingefügt (kein `GastName`, kein `varFb…`).

Geprüft ist nur das **Design**, nicht die Funktion. Kennzeichnung: **belegt** (Export, mit Wert), **gerechnet**, **geschlussfolgert**, **UNSICHER**.

**Wichtig zu den Bildern:** Sie sind **Skizzen aus den Maßen**, keine Studio-Screenshots. Schrift ist Liberation Sans statt Open Sans (Breiten weichen um einige Prozent ab), Formelwerte habe ich von Hand aufgelöst. Orange Rahmen = neu. Erzeugt mit `werkzeuge/design_skizzen.py`.

## Kurzfassung
- **Urteil:** Die neuen Features passen ins Schema, **seit Fassung 2**. Die erste Fassung (26.10.) wich an sieben Stellen ab: Knopfgröße und -rand, Eckenradius, Overlay-Stärke, fehlender Schatten und Titel im Hinweis, Eingabefelder ohne App-Stil, Schalterhöhe, „Neu buchen“ mit eigenem Stil. Das ist behoben, und zwar **systematisch**: Der Generator nimmt den Stil jetzt von vorhandenen Steuerelementen der App und rät ihn nicht mehr (Tabelle in Abschnitt 2).
- **Zwei Befunde in der App selbst**, nicht in den Paketen:
  1. `btnHeuteDatum` (bei dir eingefügt): Beim Drücken ist die Schrift fast unsichtbar. 1 Property, Fix unten.
  2. „Tisch Buchen“ (`btnTischHinzufügen`): weiße Schrift auf Hellgrau `#D0D0D0`, Kontrast **1,5 : 1**. Das ist der Hauptknopf im Dashboard. Nicht Teil der Pakete, Entscheidung bei dir (Abschnitt 4).
- **Drei Designfragen an dich** (Abschnitt 5). Ich habe jeweils eine Vorgabe gewählt, die zur App passt.
- **Noch nicht geprüft, wie gewünscht:** Funktion und Abstimmung der Pakete untereinander. Die neu erzeugten Fassungen (Für andere buchen v2, Nachtrag 6 v2) liegen schon bereit, siehe Abschnitt 6.

## 1. Das Schema der App (belegt, Export 10.11.)

| Bereich | Regel der App | Beleg |
|---|---|---|
| Schrift | überall `Font.'Open Sans'` (131 von 131 geprüften Steuerelementen) | Export |
| Knöpfe | Größe **15**, **Semibold**, Eckenradius **10**, Rand **2**, Höhe **40**. Von 47 Knöpfen folgen 30 genau diesem Muster. Die übrigen 17 sind 8 unsichtbare Klickflächen (Kacheln, Karten), 3 im stillgelegten Raumcode und 6 sichtbare Ausnahmen (siehe nächste Zeile) | Export, gezählt |
| Hauptknopf | Füllung **`#171496`**, weiße Schrift, Hover `ColorFade(Self.Fill; -20%)`, Rand `ColorFade(Self.Fill; -15%)` | `btnSpeichern`, `btnVerlängern`, `btnStornieren` u. a. |
| Zweitknopf | Füllung **Schwarz**, weiße Schrift, Hover `ColorFade(Self.Fill; 30%)` | `btnAbbrechen`, `btnSchließen4`, 5 Stück |
| Sichtbare Ausnahmen | „Tisch Buchen“ Größe 11 und grau; `btnSchließen2` und `btnEinchecken` Größe 14; Schließen-„x“ 20 × 20; Overlay-Knöpfe 30–32 hoch (`btnGrundrissAktualisieren` 30, `btnHeuteDatum` 32) | Export |
| Dialoge | Weiß (Dashboard, Panel, Tab-Karten `#f7f7f7`), Radius **16**, `DropShadow.Light` (8 von 8 Containern) | Export |
| Eingaben | Weiß, Rand **Navy `RGBA(32,54,71,1)`**, Dicke **2**, Höhe **40**, Größe 13 | `ddStart`, `dpDatum`, `ddTischePanel` |
| Umschalter | Größe 13, Höhe 28, `TrueFill` **Grün `#00A96B`** | `tglTagMo`, `tglTagMo_1` |
| Überschrift im Panel | Größe **17**, **Bold** | `lblTischeBuchenPanel` |
| Ladeanzeige | Schwarz **40 %** über dem ganzen Bildschirm | `conLadeOverlay.Fill` |
| Palette | Grün `#00A96B` (47×), Rot `#EB3951` (37×), Blau `#171496` (34×), Orange `#FFA500` (11×), Hellgrau `#f7f7f7`, Navy für Ränder (134×) | Export |
| Raster | Eingabereihen im Buchungsdialog bei Y 60 · 122 · 186 (Abstand 62–64), Panel im 60er-Abstand | Export |

Die Palette-Zahlen kommen aus der Häufigkeit der Farbwerte in allen Formeln. Grün trägt weiterhin mehrere Bedeutungen (frei, eingecheckt, Umschalter „an“). Das ist ein bestehender Befund aus dem Stil-Audit vom 08.10. und hier nicht neu.

## 2. Konformität der neuen Steuerelemente

„v1“ = Fassung vom 26.10. (nur Prüfung am Papier), „v2“ = jetzt. Der Stil in v2 stammt **direkt aus den Referenz-Steuerelementen** (der Generator liest ihn aus dem Export und prüft ihn).

| Neues Element | Referenz in der App | v1 | v2 |
|---|---|---|---|
| `btnFbTrotzdem` (Hauptknopf im Hinweis) | `btnSpeichern` | Größe 13, ohne Semibold, Radius 4, ohne Rand | alle 19 Stil-Properties von `btnSpeichern`: Größe 15, Semibold, Radius 10, Rand 2, Hover/Pressed wie dort |
| `btnFbAbbrechen` (Zweitknopf) | `btnAbbrechen` | wie oben | alle Stil-Properties von `btnAbbrechen` (Schwarz) |
| `conFbHinweis` (Dialog) | `conDetailsPopup` | Weiß, Radius 16, **kein Schatten** | Weiß, Radius 16, `DropShadow.Light` |
| `lblFbTitel` (neu in v2) | `lblTischeBuchenPanel` | fehlte (Dialog ohne Titel) | „Zur selben Zeit schon gebucht“, Größe 17, Bold |
| `btnFbHintergrund` (Abdunkelung) | `conLadeOverlay` | Schwarz 35 % | **Schwarz 40 %**, wie die Ladeanzeige |
| `txtGastName`, `txtGastNamePanel` | `ddStart` | Rand ja, Füllung/Dicke/Schriftfarbe fehlten | Füllung Weiß, Navy-Rand Dicke 2, Höhe 40, Größe 13 |
| `tglFuerAndere`, `…Panel` | `tglTagMo` | Höhe 40 (die Wochentage sind 28) | Höhe **28**, in der 40er-Reihe mittig (+6), Größe 13, Grün wie die Wochentage |
| `btnNeuBuchenHeute` (Nachtrag 6) | `btnSpeichern` | Radius 8, ohne Rand, Größe 11 | Stil von `btnSpeichern` (Radius 10, Rand 2, Semibold), Größe 12, Höhe 32 wie `btnHeuteDatum` |

**Gerechnet (Kontrast, WCAG AA verlangt 4,5 : 1 für Text):**

| Paar | Verhältnis | Wo |
|---|---|---|
| Weiß auf `#171496` | 13,3 : 1 | „Trotzdem“, „Neu buchen“ |
| Weiß auf Schwarz | 21 : 1 | „Abbrechen“ |
| Hinweistext `RGBA(50,49,48)` auf Weiß | 13,0 : 1 | Hinweisdialog |
| Weiß auf `#00A96B` (Schalter an) | 3,0 : 1 | Schalter, nur die Fläche, Text steht daneben in Schwarz → unkritisch |

## 3. Wie sich die Features im Dialog einfügen (Skizzen)

| Ansicht | Skizze | Befund |
|---|---|---|
| Buchungsdialog, „Für mich“ | [`1_buchungsdialog_aus.png`](design/1_buchungsdialog_aus.png) | Nur der kleine Schalter in der mittleren Spalte. Der Dialog sieht fast aus wie heute. |
| Buchungsdialog, „Für andere“ | [`1_buchungsdialog_an.png`](design/1_buchungsdialog_an.png) | Schalter in der Reihe von „Beginn“, Namensfeld in der Reihe von „Ende“. Die mittlere Spalte war frei (Bild bis X 245, Eingaben ab X 448). **Passt ins Raster, kein Umbau des Dialogs.** |
| Panel „Tisch buchen“ | [`2_panel.png`](design/2_panel.png) | Neue Zeile unter den Wochentagen, rechtsbündig mit „Speichern“ (Kante X 430). „Speichern“ rückt um 60 nach unten (Unterkante 631 von 678). Bei ausgeschaltetem „Wiederholen“ steht die Zeile weit unter der Auswahl. Das war bei „Speichern“ schon immer so (Y fest 531). |
| Hinweisdialog | [`3_hinweisdialog.png`](design/3_hinweisdialog.png) | Gleiche Sprache wie die Dialoge der App: weiß, rund, Schatten, Titel, zwei Knöpfe schwarz/blau. Abdunkelung wie die Ladeanzeige. |
| Popup der Kachel, ohne und mit Gast | [`4_popup_heute.png`](design/4_popup_heute.png) · [`4_popup_gast.png`](design/4_popup_gast.png) | Mit Gast zwei Zeilen („Name“ / „gebucht von …“, Größe 11), die Zeitzeile rückt nach unten. Bleibt innerhalb der linken Hälfte, das Bild rechts bleibt frei. |
| Dashboard-Karten | [`5_dashboard_karten.png`](design/5_dashboard_karten.png) | Mit Gast steht „für Name“ unter der Zeit, der Tischtitel rückt dafür um 6 nach oben, damit unten 8 Rand bleiben. „Neu buchen“ ersetzt das Status-Wort und liegt 10 links vom Verwalten-Symbol. |

**Altbestand:** Jede geänderte Anzeige enthält die alte Formel zeichengleich im Zweig „kein Gastname“. Buchungen ohne `GastName` sehen aus wie heute (maschinell geprüft).

**Bekannte Grenzen des Designs** (UNSICHER, nur am echten Bildschirm zu sehen):
- **Lange Gastnamen** ab etwa 15 Zeichen werden im Popup und im Dashboard-Verwalten abgeschnitten. Die Liste zeigt sie ganz.
- Breiten sind mit der Schätzung je Zeichenart in Pixeln gerechnet, Open Sans kann einige Prozent abweichen. Prüfen mit dem längsten Namen deiner Kollegen.

## 4. Befunde in der bestehenden App

| Nr | Befund | Beleg | Vorschlag | Muss? |
|---|---|---|---|---|
| D1 | **`btnHeuteDatum`, gedrückt:** Schrift (`PressedColor` = Blau mit 16 % Deckkraft) auf blauer `PressedFill` → fast unsichtbar, solange man drückt | Export | `btnHeuteDatum.PressedColor` = `RGBA(255; 255; 255; 1)` | nein, 1 Property |
| D2 | **„Tisch Buchen“ (`btnTischHinzufügen`):** weiße Schrift auf `#D0D0D0`, Kontrast 1,5 : 1, Größe 11. Das ist der Hauptknopf des Dashboards und der unscheinbarste | Export, gerechnet | `Fill` auf `#171496`, `Size` 15, Breite so, dass der Text passt. Hover/Pressed wie die anderen Hauptknöpfe | Entscheidung bei dir |
| D3 | Status-Wörter auf der Karte: Orange `#FFA500` auf Weiß 2,0 : 1, Grün 3,0 : 1 | gerechnet | keine Änderung vorgeschlagen, gehört zum Farbcode (Orange/Grün/Rot) | nein |
| D4 | Auswahlbalken der Dropdowns in Graublau `RGBA(100,118,132)` (31 Vorkommen) statt Markenblau | Export | bereits im Stil-Audit vom 08.10., nicht Teil dieser Pakete | nein |

D1 behebe ich nicht still, sondern lege es als eigenen Block in den Einsetzplan (Abschnitt 6). D2 setze ich nur auf dein Wort um.

## 5. Drei Designfragen

1. **Schalterfarbe:** Der Umschalter „Für andere“ ist **grün**, wie die Wochentage-Schalter im selben Dialog. Alternative: Markenblau `#171496`. **Meine Vorgabe: grün**, weil die App Schalter überall so zeigt.
2. **Hinweistitel und -text:** „Zur selben Zeit schon gebucht“ und der Fließtext aus der Übergabe. Anpassen kannst du beides in `lblFbTitel.Text` und `lblFbHinweis.Text`. Die Kontaktzeile (Axel Krägelius / Norman Horn) ist noch ungeklärt.
3. **Gast-Anzeige:** „für Name“ in derselben Farbe und Schrift wie die Zeit, ohne Hervorhebung. Alternative: in Markenblau, damit Gast-Buchungen in der Liste sofort auffallen. **Meine Vorgabe: neutral**, weil die App sonst nur Statuswörter einfärbt.

## 6. Was sich geändert hat und wo es liegt

- **Für andere buchen v2:** 179 Properties (19 ersetzt, 6 bisher Standard, 154 an 10 neuen Steuerelementen), maschinell 0 Fehler. Generator `werkzeuge/fuer_andere_v2.py`, Ergebnis `arbeit/2026-11-10_Abgestimmt/P1_FuerAndere_v2/bloecke.json`. Das **Dokument zur Fassung 2** (Einfügeanleitung, Tests) erzeuge ich im nächsten Schritt zusammen mit der Abstimmung. Fassung 1 bleibt unverändert in `arbeit/2026-10-26_FuerAndere/`.
- **Nachtrag 6 v2** (auf Nachtrag 5 und Für andere buchen v2 aufgebaut, Knopfstil aus `btnSpeichern`): 32 Properties, 0 Fehler, `arbeit/2026-11-10_Abgestimmt/P3_Nachtrag6_v2/bloecke.json`.
- **Gegenüber der ersten Fassung von Für andere buchen:** +40 Properties durch den Stil (Knöpfe, Eingaben, Dialog, Titel), +2 für die Kartenposition bei Gästen, +1 Steuerelement (`lblFbTitel`). Mehr Properties, aber alle sind Stil-Werte aus der App.
- **Noch offen:** Funktionsprüfung, Reihenfolge, gemeinsamer Testbogen, Dokumente zu Für andere buchen v2 und Nachtrag 6 v2.
