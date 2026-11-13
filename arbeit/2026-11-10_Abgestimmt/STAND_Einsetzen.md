# Stand Einsetzen – 10.11.2026 (für die nächste Sitzung)

Reihenfolge laut EINSETZPLAN.md. Josias setzt alles selbst in Power Apps Studio ein, Claude liefert Blöcke einzeln ("ok next").

| Schritt | Stand |
|---|---|
| P0 Design | erledigt |
| P2 Stornieren (Nachtrag 5) | erledigt, plus Zusätze (siehe unten) |
| SharePoint-Spalte `GastName` | angelegt |
| **P1 Für andere buchen v2** | **in Arbeit** |
| P3 Nachtrag 6 v2 | offen |
| Testbogen Teil 0, A, B | offen |
| Veröffentlichen, Export an Claude zum Abgleich | offen |
| P4 Grundriss-Laden v2 | später, eigene Sitzung |

## P1 – Fortschritt (Quelle: P1_FuerAndere_v2/bloecke.json, UEBERGABE_FuerAndere_v2.md)
- S2 Hinweisdialog (btnFbHintergrund, conFbHinweis + 4 Kinder), S3 (tglFuerAndere, txtGastName), S4 neue Steuerelemente (tglFuerAnderePanel, txtGastNamePanel): als YAML per Strg+V, siehe `P1_FuerAndere_v2/yaml_paste/`. Josias hat Datei 1–3 erhalten und eingefügt (Rückmeldung zum Gelingen von Datei 2/3 und zu den Ebenen steht aus).
- S4 `btnSpeichernTischePanel.Y` = `(tglTagFr_1.Y + tglTagFr_1.Height + 20) + 40 + 20` – gegeben.
- S5 `btnSpeichern.OnSelect` und `btnSpeichernTischePanel.OnSelect` – gegeben (Josias fügt ein; Bestätigung steht aus).
- **Noch offen:** S6 btnVerlängern / btnVerlängern_1, S7 btnHitArea / btnTischHinzufügen, S8 19 Anzeige-Eigenschaften. Danach Ebenen auf Screen1: btnFbHintergrund, conFbHinweis, conLadeOverlay jeweils "Ganz nach vorne".

## Erkenntnisse
- YAML-Einfügen: `AccessibleLabel` ist bei Classic/Button@2.2.0 unbekannt (PA2108) → aus den YAML-Dateien entfernt (auch Toggle/TextInput vorsorglich).
- **UNSICHER:** `Classic/TextInput@2.3.2` ist in keinem Export belegt. Bei Fehler: Texteingabe von Hand anlegen, Werte aus yaml_paste/02 bzw. 03 übernehmen.
- Studio hängt beim Einfügen ggf. `_1` an Namen an → zurückbenennen (btnFbTrotzdem verweist auf btnFbAbbrechen).
- Performance der neuen OnSelect-Formeln: gleiche Zahl Netzwerkaufrufe (geschlussfolgert, nicht gemessen) → im Testbogen Teil A Einzel-/Mehrfachbuchung mit Stoppuhr messen.

## Zusätze von Josias in P2 (nicht im Plan, beim Export-Abgleich dem Analyse-Chat nennen)
- `btnStornieren.Size`, `btnStornieren_1.Size`, `btnStornierenKlein.Size` (12 bei offener Rückfrage, sonst 15)
- `btnSchließen4.OnSelect`, `btnSchließen4_1.OnSelect`, `btnSchließenKlein.OnSelect` setzen die Storno-Frage zurück

## Offene Nebenpunkte
- ddStockwerk.SelectionColor noch dunkel
- Repo ist öffentlich (empfohlen: wieder privat)
- Handy-App anpassen, Doku aktualisieren

## Stand 13.11.2026
- P1 S6–S8 und P3 R1–R3 eingefügt. btnNeuBuchenHeute war zuerst außerhalb der Galerie-Vorlage (18 Fehler „ThisItem“) → in die Vorlage verschoben. lblZeitHeute.Y war versehentlich mit der If-Formel von lblTischHeute.Y überschrieben → zurück auf `lblTischHeute.Y + lblTischHeute.Height`.
- Test mit Testknopf (varFreigabeMinuten = 1, Buchung am Handy ab laufender halber Stunde): „Neu buchen“ erscheint wie geplant.

### Änderung „Rebuchen“ (Wunsch Josias 13.11., NICHT im abgestimmten Plan)
- btnNeuBuchenHeute (Name bleibt) heißt jetzt „Rebuchen“, Stil wie btnHeuteDatum (weiß, blauer Rand 1, blaue Schrift, Radius 14, Höhe 28, Breite 100).
- OnSelect öffnet keinen Dialog mehr: prüft, ob der Tisch ab jetzt bis zum alten Ende frei ist (verfallene fremde Buchungen zählen nicht), legt eine neue Buchung mit **genau derselben Start- und Endzeit**, demselben Tisch, derselben SerienID und demselben GastName an und entfernt danach die alte verfallene Buchung. Die neue gilt 30 Min ab Buchungszeitpunkt (Erstellt) → einchecken.
- Belegung vor „jetzt“ wird nicht geprüft (geschlussfolgert: sonst würde Rebuchen an längst beendeten Fremdbuchungen scheitern).
- Visible unverändert (Rest bis mindestens zur nächsten halben Stunde).
- YAML: `P3_Nachtrag6_v2/yaml_paste/R2b_btnNeuBuchenHeute_Rebuchen.yaml`
- **Folgen:** P4 L5 entfällt (Rebuchen setzt varSelectedTisch nicht mehr, kein Typ-Konflikt; Tische bleibt für die frische Sperr-Prüfung). Testbogen Teil A Tests 9 und 10 anders: Rebuchen bucht sofort, kein Dialog. R3 (varEndeOverride-Reset) schadet nicht, ist aber nicht mehr nötig. Beim Export-Abgleich dem Analyse-Chat melden.
- Rebuchen Visible vereinfacht (Vorschlag 13.11.): statt „Ende nach der nächsten halben Stunde“ nur noch `ThisItem.Endzeit > Coalesce(varJetztTakt; Now())`, damit auch kurze Restbuchungen (z. B. 10:30–11:00) rebuchbar sind.

### Änderung „Tisch Buchen“-Knopf (Wunsch Josias 13.11., überschreibt P0)
- btnTischHinzufügen weiß mit blauer Schrift und blauem Rand (#171496), BorderThickness 2, Hover RGBA(23;20;150;0,08), Pressed RGBA(23;20;150;0,16), Disabled weiß / ColorFade 60 %. Size 15, Width 160 aus P0 bleiben.
- Rebuchen-Knopf heißt in der Aufschrift jetzt „Reaktivieren“ (Josias 13.11.), Y = `(Parent.TemplateHeight - Self.Height) / 2` (mittig in der Karte), Width 110.
- **P4 K1 vorgezogen (13.11.):** `ddStockwerk.SelectionColor = RGBA(32; 54; 71; 1)`. P4 hat damit nur noch L1–L4 (L5 entfällt).
- **P4 eingefügt (13.11.):** Vorher-Abgleich von App.OnStart, App.Formulas, Gallery1.Items, ddTischePanel.Items mit Josias' eingefügten Ist-Fassungen: alle 4 zeichengleich (maschinell). Dann L1, L2, L3 (Formulas + Gallery1.Items), L4 gegeben. L5 entfällt.
- **Damit sind P0–P4 vollständig gegeben.** Offen: Testbogen-Reste, Testknopf löschen + OnStart, veröffentlichen, P4 Test 10 (Strg+F5, keine Kachel oben links) und 11 (Handy-Gegenprobe), Export an Claude zum Abgleich.
