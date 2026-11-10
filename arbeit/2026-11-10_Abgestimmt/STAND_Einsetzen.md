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
