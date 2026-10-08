# Nachtrag 4 (08.10.): Nachlese ohne `Refresh`, bei jeder Buchung schneller

> Für den Chat, der Josias führt. Gilt für **G6** (Gesamtplan) und **F4** (Paket F). **Ersetzt Nachtrag 3** (enthält dessen Änderung schon). Im Vault ablegen.

## Kurzfassung
- **Was sich ändert:** Beide Speichern-Knöpfe kommen ganz **ohne** `Refresh(Tischbuchungen)` aus.
  - Nachtrag 3 hat das `Refresh` im Zweig „nichts gebucht“ entfernt.
  - Jetzt entfällt auch das `Refresh` vor der Nachlese. Das ist der Teil, der bei **jeder** Buchung läuft.
- **Warum es vorher nötig schien (H6):** Die Nachlese war **wortgleich** mit der Vorprüfung `colNeuBelegt`. Hätte Power Apps die gleiche Abfrage aus einem Zwischenspeicher beantwortet, hätte die Nachlese den Stand **vor** dem Patch gezeigt. Das `Refresh` sollte das verhindern.
- **Die Lösung:** Die Nachlese ist jetzt eine **eigene, bei jedem Klick eindeutige** Abfrage. Ihre untere Zeitgrenze `varNeuNachVon` liegt um die Sekunden seit Mitternacht (plus 1) vor dem Beginn. Damit ist die Abfrage-URL bei jedem Klick anders und kann nicht aus einem Zwischenspeicher kommen. Das ist dasselbe Prinzip wie die gemessene L2-Ladezeile, die dafür `Now()` nutzt.
- **Ausgewertet wird wie bisher:**
  - Eigene neue Zeilen werden über **`SerienID`** gezählt (`varNeuAnzahl`).
  - Gleichzeitige fremde Buchungen findet die **Überlappung** mit kleinerer ID (`varNeuKonflikt`).
  - Zusätzlich geholte Zeilen (Ende bis zu 24 Std. vor Beginn) überlappen nie mit den neuen Terminen und zählen daher nicht.
- **Warum nicht nur über `SerienID`?** Eine reine `SerienID`-Abfrage zählt die eigenen Zeilen, findet aber **keine** gleichzeitige fremde Buchung. Die Warnung „Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht“ wäre weg. Deshalb bleibt die Abfrage über Tisch und Zeit, nur eindeutig gemacht. Das sind 1 statt 2 Abfragen.

## Belege
| Was | Kennzeichnung | Quelle |
|---|---|---|
| Nach einem Patch zeigt die eigene Liste die neue Buchung **ohne** `Refresh` | **gemessen** in der Handy-App (gleiche App-Einstellungen, gleiche Liste) | `05_HANDY_APP/TESTPROTOKOLL.md`, Test TB-1: „Gebucht: UG Desk 17 … automatischer Wechsel zu „Meine“; dort am Ende „UG Desk 17 …““. `btnBuchen` hat kein `Refresh` |
| Nachlese mit einer **anders geformten** Abfrage als die Vorprüfung, ohne `Refresh` | **gemessen** in der Handy-App (TB-1 „Gebucht“, also Nachlese gefunden) | Handy `btnBuchen.OnSelect`: Vorprüfung `LookUp`, Nachlese `ClearCollect(colKollision; Filter(…))` |
| Eindeutige Abfrage-URL schließt den Zwischenspeicher aus | **belegt** als Prinzip in L2 (veröffentlicht, gemessen schnell) | `UEBERGABE_Grundriss_L2_v0.3_1.md`: „Durch `Now()` ist außerdem jede Abfrage-URL eindeutig …“ |
| Ob die Desktop-Galerien nach dem Sammel-Patch (Tabelle) genauso von selbst aktualisieren | **geschlussfolgert** aus der Handy-Messung (dort Einzel-Patch) | Test 2 unten |

## Wirkung auf die Abfragen (geschlussfolgert, im Monitor prüfbar)
Erfolgreiche Buchung, **vorher** (Gesamtplan bzw. Paket F):
1. Vorprüfung: 3 Abfragen (Tisch belegt, ich belegt, Tisch gesperrt).
2. Sammel-Patch.
3. `Refresh`: Neuabfrage aller an `Tischbuchungen` gebundenen Anzeigen, also 2 Galerien. Aus dem Panel bis zu **7**, weil das Panel zu diesem Zeitpunkt noch offen ist (Tischliste, Knöpfe 5/9 Std.).
4. Nachlese: 1.
5. Ladezeile: 1.

**Nachher:** Schritt 3 entfällt. **Ersparnis je Buchung: 2 Abfragen aus dem Grundriss-Dialog, bis zu 7 aus dem Panel.** Dazu kommt Nachtrag 3 (nur im Zweig „nichts gebucht“).
- Ob Power Apps nach dem Patch die beiden Galerien einmal selbst neu lädt, zeigt der Monitor. Laut Handy-Messung zeigen sie die neue Buchung. Das `Refresh` war dann eine **zweite** Welle.
- Die Nachlese holt bis zu einem Tag mehr Zeilen **eines** Tisches, also höchstens ein paar Zeilen mehr.

## So einfügen
- **G6** (noch nicht oder schon eingefügt, auch nach Nachtrag 3): die beiden G6-Blöcke unten, ganze Property ersetzen.
- **Paket F, Schritt F4:** die beiden F4-Blöcke unten statt der F4-Blöcke aus `UEBERGABE_PaketF.md` bzw. Nachtrag 3.

## Test
1. **Einzelbuchung** im Grundriss-Dialog → „Gebucht: …“. In SharePoint steht die Zeile.
2. **Liste ohne Aktualisieren:** Direkt danach steht die neue Buchung im Dashboard („My personal desk“, wenn heute) und im Tab „Buchungen“, **ohne** auf Aktualisieren zu tippen. Dasselbe aus dem Panel „Tisch buchen“.
3. **Serie** (Mo–Fr, 2 Wochen, ein Tag belegt) → „9 von 10 Terminen gebucht …“. Die Zählung kommt aus der Nachlese.
4. **Gleichzeitig:** zwei Browserfenster (zwei Konten oder Josias + Kollege), derselbe Tisch und dieselbe Zeit, möglichst gleichzeitig „Speichern“ → einer bekommt „Gebucht“, der andere „Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht …“.
5. **Zweimal hintereinander dieselbe Zeit:** buchen, stornieren, sofort dieselbe Zeit wieder buchen → „Gebucht“, **nicht** „nicht angekommen“. Das ist der Zwischenspeicher-Fall.
6. **Optional Monitor:** Speichern → nach dem Patch genau **eine** `getRows`-Anfrage der Nachlese mit `Endzeit gt …`. Diese Uhrzeit weicht von der Vorprüfung ab. Keine `Refresh`-Welle mehr.

**Wenn Test 2 scheitert** (neue Buchung erst nach Aktualisieren sichtbar): Das ist kein Datenfehler, nur die Anzeige. Rückfall auf Nachtrag 3 (Refresh vor der Nachlese) oder melden. Dann setzt Claude Code ein `Refresh` **nach** dem Schließen des Panels, also nur 2 statt 7 Abfragen.
**Wenn Test 1, 3 oder 5 „nicht angekommen“ zeigt, obwohl die Zeile in SharePoint steht:** sofort Rückfall auf Nachtrag 3 und melden.

## Rückfall
Die Blöcke aus **Nachtrag 3** (`arbeit/2026-10-08_Nachtrag3/NACHTRAG_3_Speichern_ohne_Refresh.md`) einsetzen: mit `Refresh` vor der Nachlese, ohne das im Zweig „nichts gebucht“. Ganz zurück: G6 aus `GESAMTPLAN.md` bzw. F4 aus `UEBERGABE_PaketF.md`.
