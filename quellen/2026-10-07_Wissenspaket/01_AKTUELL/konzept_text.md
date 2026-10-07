# ÜBERGABE Tischbuchung: Paket K (Korrekturen zum Go-Live)
**v1 · 07.10.2026 · Basis: veröffentlichter Export „Tischbuchung App 07.10.2026 verbesserung analyse“ (erstellt {STAND}, enthält L2) · alle Formeln maschinell aus diesem Export erzeugt und geprüft (Anhang 2) · noch nichts davon eingefügt**

## 0. Kurzfassung
- **Teil A (klein, empfohlen vor dem Go-Live):** K1 stille Doppelbuchung im Tab + Doppelklick-Sperre beim Speichern. 1 Formel ersetzen, 2 Properties setzen. Ca. 10 Minuten.
- **Teil B (empfohlen, wenn A ok):** Verlängern prüft vor dem Schreiben am Server (Kollision, 22:00, gelöschte Buchung), meldet ehrlich, Doppelklick-Sperre. 2 Formeln ersetzen, 2 Properties setzen.
- **Teil C (optional, auch nach dem Go-Live):** Speichern lädt weniger Daten, Serienmeldungen nennen alles in einer Meldung, Panel erkennt Schreibfehler. 2 Formeln ersetzen.
- **Teil E (nur bei Bedarf):** Mehrfachauswahl ausblenden.
- Alles, was nicht in A–C/E steht, ist bewusst **nach** dem Go-Live (Abschnitt 9).

Ablauf je Schritt wie bei L2: Steuerelement.Property öffnen → **ganze Property ersetzen** → App-Prüfung → kurzer Test → Ergebnis melden. Jeder Block ist vollständig, deutsche Schreibweise, ohne Kommentare.

**Voraussetzung:** Seit dem Export (07.10.) wurde in Studio nichts mehr gespeichert. Sonst neuen Export erstellen, entpacken und `exportiere_props.ps1` + `erzeuge_konzept.ps1` neu laufen lassen (die Skripte brechen ab, wenn ein Anker nicht mehr genau passt). Vorher `.msapp` exportieren.

## 1. Übersicht
| Schritt | Steuerelement.Property | Was | Behebt | Impact | Risiko |
|---|---|---|---|---|---|
| A1 | `btnVerwalten_2.OnSelect` | +1 Zeile `Set(varSelectedBuchung; ThisItem)` | B0 stille Doppelbuchung beim Verlängern im Tab | hoch | niedrig |
| A2, A3 | `btnSpeichern.DisplayMode`, `btnSpeichernTischePanel.DisplayMode` | neu: gesperrt während `varIsLoading` | Doppelklick = doppelte Buchung | mittel | niedrig |
| B1 | `btnVerlängern_1.OnSelect` | neu: prüft am Server, meldet ehrlich | Kollision zwischen Anzeige und Klick, über 22:00, gelöschte Buchung, „gespeichert“ trotz Fehler | mittel–hoch | mittel |
| B2 | `btnVerlängern_1.DisplayMode` | neu: Doppelklick-Sperre | „+1 Std“ wird zu „+2 Std“ | mittel | niedrig |
| B3 | `btnVerlängern.OnSelect` | wie B1 im Grundriss | wie B1 | mittel–hoch | mittel |
| B4 | `btnVerlängern.DisplayMode` | wie B2 im Grundriss | wie B2 | mittel | niedrig |
| C1 | `btnSpeichern.OnSelect` | Zeitfenster in Kollisionsabfrage (K4.1) + eine Meldung mit Anzahl, Kollision, Kappung | B3 Kappungsmeldung verdrängt Kollisionsmeldung; weniger Daten | niedrig–mittel | niedrig |
| C2 | `btnSpeichernTischePanel.OnSelect` | K4.1 + `IfError` je Termin + Meldung wie C1 | B2 Fehler wird als „gespeichert“ gezählt | niedrig–mittel | niedrig |
| E2 | `tglAuswahlModus.Visible` | `false` (nur falls gewünscht) | Mehrfachauswahl zum Go-Live aus | – | niedrig |

Herkunft: K1–K5 stammen aus `ENTWURF_SPEICHERN.md` (Claude Code, vor L2). Hier sind sie an den **heutigen** Stand angepasst: L2-Ladezeile bleibt überall erhalten, `btnSpeichern` hat inzwischen den Sammel-Patch (deshalb C1 neu geschrieben), die Verlängern-Prüfung ist delegierbar und wortgleich mit der der Plus-Knöpfe.

**Bewusst verworfen: K4.2 (`<>` → `>` beim Serien-Enddatum).** Geprüft am Export: Wer „Wiederholen“ anhakt und das Bis-Datum vergisst (Standard = heute), bekommt heute „… Bitte Enddatum anpassen“. Mit K4.2 bekäme er still nur **eine** Buchung, obwohl er eine Serie wollte. Das wäre schlechter. Der Test im alten Entwurf war nicht stimmig (ohne gewählten Wochentag kommt auch danach „Bitte mindestens einen Wochentag auswählen“).

## 2. Entscheidungen (Vorschlag, du bestätigst)
- **E1 22:00-Grenze beim Verlängern: ablehnen** (Meldung, nichts ändern). Begründung: Das Tische-Panel behandelt 22:00 schon als Tagesende (`btn5Std`, `btn9Std`), die Handy-App erlaubt Verlängern bis 22:00. Verkürzen ist immer erlaubt, auch bei alten Buchungen über 22:00. Wenn du **keine** Grenze willst: B1/B3 nicht einfügen und Bescheid geben, dann wird die Variante ohne Grenze erzeugt.
- **E2 Mehrfachauswahl: drinlassen** (Trace mit 33 Stornierungen fehlerfrei). Nur wenn dein Zwei-Tab-Test scheitert: Schritt E2.
- **E3 Serienbuchung: drinlassen** (gemessen ~5 s statt ~101 s).

<<<BLOECKE>>>
## 7. Rückfall
- Einzelner Schritt: die Originalformel aus Anhang 1 einfügen (bei DisplayMode/Visible: `DisplayMode.Edit` bzw. `true`).
- Teil B zurück, Teil A behalten: geht, A und B sind unabhängig. B2/B4 vor B1/B3 zurücknehmen (sonst ist der Knopf nach einem Fehler gesperrt, siehe U-K2).
- Teil C zurück: Original aus Anhang 1 einfügen. A, B und C sind unabhängig voneinander (C ändert `OnSelect` der Speichern-Knöpfe, A nur deren `DisplayMode`).
- Komplett: `.msapp`-Export oder Versionsverlauf.

## 8. UNSICHER (mit Prüftest)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U-K1 | `Date(Year(x); Month(x); Day(x)) + Time(22; 0; 0)` ergibt 22:00 Ortszeit am Buchungstag. Das Muster `Datum + Time(22; 0; 0)` nutzt die App schon (`btn5Std`), `Date(...)` aus einer Buchung noch nicht | 22:00-Grenze greift zu früh/spät | B1-Test (3): 19:00–21:30, +1 Std → abgelehnt; 19:00–20:30, +1 Std → erlaubt |
| U-K2 | DisplayMode-Sperre: Hängt eine Formel unerwartet ab, bleibt `varIsLoading` wahr und der Knopf gesperrt | Knopf bleibt grau bis zum Neustart | Bei jedem Test prüfen, ob Overlay und Knopf danach wieder frei sind. Alle Wege setzen `varIsLoading` am Ende auf falsch |
| U-K3 | Ob die DisplayMode-Sperre einen sehr schnellen Doppelklick wirklich abfängt (Power Apps garantiert kein Neuzeichnen zwischen zwei Anweisungen) | Ein zweiter Klick kommt selten doch durch | A2- und B2-Test mehrmals. Restrisiko bleibt; die Serverprüfung in B1/B3 fängt es nicht ab, weil die eigene Buchung nicht als Kollision zählt |
| U-K4 | `IfError(Patch(...); "fehler"; "ok")` in `With` erkennt einen fehlgeschlagenen Patch. Muster aus `btnSpeichern`, dort läuft es, ein echter Fehler wurde aber nie ausgelöst | Fehler wird als Erfolg gemeldet (wie heute) | WLAN kurz aus, verlängern → erwartet rote Meldung |
| U-K5 | Mehrere geschachtelte `If` mit `Notify` und `Set` in den Zweigen bei `powerfxv1 = false`. Die App mischt das schon (z. B. `btnStornierenKlein`, L2-Ladezeile) | rote Formel beim Einfügen | App-Prüfung nach B1 |
| U-K6 | C2-Fehlerzweig nicht gezielt testbar | Fehlermeldung unerprobt | hinnehmen, Normalfall testen |
| U-K7 | C1/C2: Zeitfenster 16 Tage muss größer als die Serien-Kappung (Start + 14 Tage) bleiben | Kollision am letzten Serientag übersehen | Falls die Kappung je geändert wird: Zahl 16 mitändern |

## 9. Nach dem Go-Live (bewusst nicht in diesem Paket)
| Vorhaben | Warum später |
|---|---|
| L3 versteckte Dialoge nur rechnen, wenn offen | nach L2 kaum spürbar (~50 Abfragen pro Schreibwelle, Speichern ~5 s) |
| L4 Raumcode stilllegen + `App.OnStart` aufräumen | Start ~3 s, stört nicht; größere Änderung |
| Plus-Knöpfe ab 22:00 grau | B1/B3 lehnen schon ab; Komfort |
| Nur freie Tische im Panel (Muster aus der Handy-App) | Umbau von Panel und Speichern |
| Vorprüfung mit Alternativtischen, `SerienID`-Nachlese | großes Konzept |
| Panel-Speichern auf Sammel-Patch | Panel misst ~5 s, kein Bedarf |
| Spinner-Optik | kosmetisch, verworfen |
| Fund am Rande: `dpWiederholenBis_1.OnChange` rechnet ein `If` ohne `Set` (wirkungslos, harmlos) | Aufräumen bei L4 |

## 10. Regeln
Deutsche Schreibweise (`;` trennt, `;;` verkettet), keine Kommentare, immer die **ganze** Property ersetzen, ein Studio-Fenster, Schritte einzeln, nach jedem Schritt App-Prüfung. Die zwei Speichern-Knöpfe und die zwei Verlängern-Knöpfe sind **nicht** wortgleich: jeden einzeln einfügen.
