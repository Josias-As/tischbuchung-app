# Selbstprüfung meiner Arbeit (Paket K v2, Analyse, Paket L), 08.10.2026

Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**, **Einschätzung**.

## 1. Kurzfassung
- **Ein wichtiger Fehler war übersehen (jetzt behoben):** Datum und Zeiten im Buchungsdialog bleiben vom letzten Öffnen stehen, was eine **stille Buchung am falschen Tag** möglich macht (F-L11, belegt am Export). Neu ist **L13** (2 Properties). Mit Paket K v2 ist L13 **Pflicht**, sonst führen alte Uhrzeiten von heute zur verwirrenden Meldung „Vergangenheit“.
- **Zu optimistisch war ich beim Go-Live.** K v2 und L zusammen sind **137 Properties**, die von Hand einzufügen und zu testen sind. Dazu schreibt K v2 alle acht Schreibstellen neu. Neuer Code bringt eigene Fehler, und dass ich F-L11 erst jetzt gefunden habe, zeigt, dass es weitere unentdeckte geben kann. **Empfehlung: vor dem Go-Live nur die 40 Muss-Properties** (Abschnitt 4), den Rest danach.
- **Einige Aussagen waren zu stark gekennzeichnet oder unvollständig.** Die Korrekturen stehen in Abschnitt 2. An meinen Kernurteilen ändert sich nichts.
- **Nichts davon ist in Studio getestet.** Das ist die größte verbleibende Lücke, und die kann nur Josias schließen. Die wichtigsten offenen Laufzeitfragen stehen in Abschnitt 5.

## 2. Was falsch oder zu stark eingeschätzt war
| # | Wo | Was ich gesagt habe | Richtig ist | Folge |
|---|---|---|---|---|
| 1 | Analyse, Abschnitt 2 | „Alles **belegt** am Export“ | Der Doppelklick-Fehler ist in der **Handy-App gemessen**. Für die Desktop-App ist er **geschlussfolgert** (gleiches Muster, gleiche Einstellungen). Die Häufigkeiten in der Tabelle sind **Einschätzung** | Urteil bleibt, Kennzeichnung korrigiert |
| 2 | Analyse, Abschnitt 6 | Go-Live mit Paket K „~65–75 %“ | Diese Zahlen waren Bauchgefühl und haben den Aufwand nicht eingerechnet: 55 Properties für K, dazu jetzt 82 für L, rund 4 Arbeitstage. **Neue Einschätzung:** nur Muss-Teil (40) eingefügt und getestet: ~60–70 %. Alles (137) vor dem 14.10.: eher schlechter, weil die Testzeit fehlt | Muss/Soll/Später-Liste (Abschnitt 4) |
| 3 | Analyse, Abschnitt 5 | „Lizenz 0 €“ | Nur, wenn alle Nutzer eine M365-Lizenz mit Power-Apps-Nutzungsrecht haben (in Business- und E-Plänen üblich, geschlussfolgert). App und Flows nutzen nur Standard-Konnektoren | Bei Michael bestätigen lassen |
| 4 | Analyse, Abschnitt 3 | Mitbestimmung nach § 87 BetrVG | Gilt nur, **wenn es bei Technoform einen Betriebsrat gibt** (weiß ich nicht). Datenschutz (Information der Beschäftigten, Löschfrist) gilt unabhängig davon | Frage an Michael/Datenschutz bleibt die wichtigste organisatorische |
| 5 | Analyse, Abschnitt 5 | Wartung „erheblicher Teil der Lizenz“ | Konkreter, mit **Annahme**: 10 Std/Monat × 12 × ~20 €/Std (Werkstudent) ≈ **2.400 €/Jahr**, also rund ein Viertel von 10.000 €. Die Ersparnis bleibt deutlich. Das eigentliche Risiko ist, dass nach dir niemand mehr da ist, nicht die Kosten | Urteil „Bus-Faktor 1“ bleibt das stärkste Gegenargument |
| 6 | Paket L, F-L2 | Reihenfolge der Dashboard-Liste „= ID“ | **geschlussfolgert** (SharePoint liefert ohne Sortierung üblicherweise nach ID), nicht belegt | L2 sortiert ohnehin explizit |
| 7 | Analyse, Abschnitt 3 und Paket L, P2 | „Aufräum-Flow löscht nach 7 Tagen“ | Steht so in den Übergaben (`ENTWURF_MEHRFACHAUSWAHL.md`). **Den Flow selbst habe ich nicht gesehen** | Vor P2 den Flow ansehen |
| 8 | Analyse | „Die Handy-App ist sauberer gebaut“ | Gilt für die Schreibwege (gelesen), nicht für alles. Die Handy-App habe ich nicht vollständig geprüft. Bestätigt habe ich jetzt: Ihre Startliste endet korrekt um 21:30 (belegt) | – |
| 9 | Paket K v2 | 24 Plus-/Minus-Properties „~50 Abfragen pro Schreibvorgang“ | Die ~50 (Trace 4) enthalten auch `btn5Std`/`btn9Std`, nicht nur die Dauer-Knöpfe. Die Größenordnung stimmt | – |

## 3. Was gefehlt hat und jetzt ergänzt ist
1. **F-L11 / L13:** Buchungsdialog und Panel setzen Datum, Zeiten und Wiederholen-bis beim Öffnen zurück. Im Panel stehen die Resets **nach** dem Leeren der Zeit-Vorgaben, damit die Startliste auf den frischen Standard geht. Der P1-Plan ist mit denselben Resets angepasst.
2. **Priorisierung** (Abschnitt 4): Bisher stand alles gleichrangig nebeneinander.
3. **Bestandsdaten prüfen** (Abschnitt 6): Der veröffentlichte Stand kann schon kaputte Buchungen erzeugt haben (Ende 00:00, über 22:00, über Mitternacht).
4. **Zeitumstellung** (25.10.2026, 29.03.2027): `Datum + Uhrzeit` wird in der App als Zeitspanne ab Mitternacht gerechnet. Am Umstellungstag selbst könnte eine Buchung deshalb um eine Stunde verschoben sein (geschlussfolgert, UNSICHER). Beide Tage sind **Sonntage**, und für Sa/So gibt es keine Wochentag-Schalter. Das Risiko ist sehr klein. Gilt genauso für die Handy-App.
5. **Zweite unabhängige Prüfung** von L10–L13, P1 und dem Gesamtstand nach K + L: Ergebnis in `pruefung_paket_l_2.md`.

## 4. Einfügereihenfolge nach Priorität (K v2: 55, L: 82, zusammen 137)
| Stufe | Schritte | Properties | Warum |
|---|---|---|---|
| **Muss vor Go-Live** | K: 0, A1–A10, B1, B2, C2 · L: L1, L13 | **40** | Doppelbuchungen (Doppelklick, B0, keine Serverprüfung), rohe Fehler beim Stornieren, falsche Meldungen, Buchung mit Ende vor Beginn, Buchung am falschen Tag |
| Soll vor Go-Live, wenn Zeit | K: C1, C3, C4, C5, D1–D4 · L: L3, L4, L9 | 52 | Tischauswahl nur frei (größte erwartete Beschwerde, aber mit offenen Fragen U-C1/U-V3), unlesbare Knöpfe, aktiver Tab, deutsche Texte |
| Nach Go-Live | L: L2, L5–L8, L10–L12 | 45 | Optik und Stimmigkeit |

**Mein Rat:** Muss-Teil am 08./09.10. einfügen und mit dem Testbogen testen. Am 12./13.10. drei bis fünf Kollegen testen lassen. C1 (Tischauswahl) nur, wenn die Muss-Tests bis dahin grün sind.

## 5. Was weiterhin offen ist (kann ich nicht klären)
- **Nichts ist in Studio getestet.** Die wichtigsten Laufzeitfragen:
  - **U-C1:** Behält die Tischliste die Auswahl, wenn sich die Zeit ändert?
  - **U-V3:** Wird die Abfrage der Tischliste delegiert?
  - **U-B1:** Wird `SerienID` beim Sammel-Patch geschrieben?
  - **Reset:** Setzt `Reset(ddStart)` direkt nach `Reset(dpDatum)` wirklich auf den neuen Standard? (L13-Test)
  - **Doppelklick:** Hält die Zweifach-Sperre in der Desktop-App?
- **Unbekannt:** die Nutzung von GoBright bei Technoform, ob es einen Betriebsrat gibt, die Berechtigungen der Liste, ob die Handy-App zum Go-Live gehört, ob es eine Nachfolge gibt.
- **Messdaten:** Die Trace-Auswertung stammt von Claude Code (06./07.10.). Ich habe die Rohdateien nicht selbst nachgerechnet. Nach Paket K wäre ein neuer Trace der Beweis für die weggefallenen Abfragen.
- **Die Handy-App** habe ich nicht gegen alle neuen Befunde geprüft, nur gegen F-L1 (dort kein Fehler).

## 6. Bestandsdaten prüfen (einmalig, vor dem Go-Live)
Der veröffentlichte Stand konnte Buchungen mit Ende vor Beginn, über 22:00 oder über Mitternacht erzeugen (F-L1 sowie BD-03/F13 ohne Grenze beim Verlängern). So findest du sie, ohne etwas zu ändern: In Studio eine **leere Galerie** vorübergehend auf `Screen1` legen, `Items`:
```
Filter(Tischbuchungen; Endzeit <= Startzeit || Day(Endzeit) <> Day(Startzeit) || Hour(Endzeit) * 60 + Minute(Endzeit) > 22 * 60)
```
Die Delegierungswarnung ist hier egal: Die Liste hat ~250 Zeilen, weniger als das Limit von 1.000. Gefundene Zeilen in SharePoint korrigieren oder löschen, danach die Galerie wieder löschen. (Formel von Hand geschrieben, nicht aus dem Export erzeugt. Prüfe die App-Prüfung danach.)
