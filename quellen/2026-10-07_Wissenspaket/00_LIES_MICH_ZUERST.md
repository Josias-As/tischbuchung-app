# Lies mich zuerst: Wegweiser durch das gesamte Wissenspaket (Stand 07.10.2026)

Dieses ZIP enthält **alles**, was Claude Code zur Tischbuchungs-App (Desktop und Handy) kennt. Es ist nach Zweck geordnet. Ältere Dokumente sind teils veraltet (z. B. `Title` statt `Titel`, Stand vor L2). **Im Zweifel gilt der Export vom 07.10.** (Ordner `01_AKTUELL/`).

## Lesereihenfolge
1. **`01_AKTUELL/00_UEBERGABE_an_Chat_PaketK_2026-10-07.md`**: aktuelle Übergabe (Josias’ Feedback an dich, Stand, Messdaten, Regeln, App-Fakten).
2. **`01_AKTUELL/02_GESAMTE_AUFGABEN_Tischbuchung_2026-10-07.md`**: **alle** Aufgaben, Wünsche, Befunde, offene Fragen mit Status und Priorität (Abschnitte A–K). Dein Hauptdokument für „was ist alles zu tun“.
3. **`01_AKTUELL/UEBERGABE_PaketK_v1.md`**: Paket K (Korrekturen zum Go-Live 14.10.), fertige Blöcke, Arbeitsgrundlage für den **aktuellen Auftrag**.
4. **`01_AKTUELL/01_PROMPT_fuer_den_Chat.md`**: Startprompt (Auftrag: Paket K unabhängig prüfen, `UEBERGABE_PaketK_v2.md` im Stil von L2 v0.3 zurückgeben).
5. Danach nach Bedarf die Ordner unten.

## Ordner
| Ordner | Inhalt | Wann lesen |
|---|---|---|
| `01_AKTUELL/` | aktuelle Übergabe, Gesamtaufgaben, Paket K, Prompt, Generator-Skripte (`exportiere_props.ps1`, `erzeuge_konzept.ps1`, `konzept_text.md`, `pruefe_formeln.ps1`), `props_de.json` (alle Formeln des veröffentlichten Stands), `FORTSCHRITT.md` (Verlauf der Sitzung), Stilvorlage `UEBERGABE_Grundriss_L2_v0.3_1.md` | immer |
| `02_EXPORT_UND_TRACES/` | Export-ZIP der Desktop-App vom 07.10. (Quelle der Wahrheit), Export-ZIP der Handy-App, Traces 3–5 (Serie vorher/nachher, Mehrfachstornierung) | zum Nachrechnen/Gegenprüfen |
| `03_DESKTOP_HINTERGRUND/` | `BEFUNDE_DESKTOP.md` (BD-01…27), `OFFENE_FUNDE.md`, `07_OFFENE_FRAGEN.md`, Entwürfe `ENTWURF_SPEICHERN.md` (K1–K5), `ENTWURF_MEHRFACHAUSWAHL.md`, verworfene Ansätze, `KORREKTUR*.md`, `INVENTAR.md`, `KONTEXT.md` (30.09., teils veraltet), `AUFGABE_*.md` (alte Aufgabenstellungen) | Herleitung, warum etwas so entschieden wurde |
| `04_UEBERGABE_2026-10-06/` | Vollanalyse des Quellcodes vom 06.10. (`01_APP_KOMPLETT`, `02_BUTTONS`, `03_VARIABLEN`, `04_DATENQUELLEN`, `05_STAND_DER_AENDERUNGEN`, `06_KONZEPT_MEHRFACHBUCHUNG`), `BRIEFING_Mehrfachspeichern.md`, `VERIFIKATION.md`, `LIESMICH` | Detailnachschlagen zu einzelnen Steuerelementen |
| `05_HANDY_APP/` | Plan, Entscheidungen, Fortschritt, Fragen, Testprotokoll/-daten, App-Wissen, Anleitung, Features, Hintergrundanalysen, YAML-Auszüge der Handy-App | nur für das Handy-Vorhaben (E-5) und den Rechercheauftrag |
| `06_RECHERCHE/` | `RECHERCHEAUFTRAG_AppStore_2026-10-07.md` (noch nicht ausgeführt) | für Aufgabe K |

## Die wichtigsten Fakten in fünf Sätzen
1. **L2 (Grundriss-Performance) ist eingebaut und veröffentlicht**: Serie 11 Termine ~4,7 s statt ~101 s (gemessen), Mehrfachstornierung 33 Buchungen ~9 s fehlerfrei.
2. **Go-Live der Desktop-App ist der 14.10.2026**; Josias fügt jede Formel selbst in Power Apps Studio ein (ganze Properties, deutsche Schreibweise, keine Kommentare), du bearbeitest nie die App.
3. **Paket K** (K1 stille Doppelbuchung, Doppelklick-Sperre, Verlängern prüft am Server, genauere Serienmeldungen) ist maschinell erzeugt und geprüft, aber **nicht eingefügt** und die **unabhängige Prüfung fehlt**.
4. Alle weiteren Aufgaben (BD-Befunde, Wünsche wie „nur freie Tische“, Vorprüfung mit Alternativtischen, L3/L4, Handy-App, Rechercheauftrag, Fachfragen 1–11) stehen mit Status in `02_GESAMTE_AUFGABEN…`.
5. Josias fand deine letzte Analyse sehr gut: behalte Stil (maschinell erzeugte vollständige Blöcke, belegt/gemessen/geschlussfolgert/UNSICHER, Tests, Rückfall, Originale im Anhang, unabhängige Prüfung).

## Bekannte Lücken dieses Pakets
- Was Josias nur in **anderen Chats** besprochen hat und nirgends als Datei liegt, kennt Claude Code nicht (ergänzen, wenn du es aus dem Projekt kennst).
- Screenshots der Handy-App und Medien (`MOBIL\screenshots`, `medien`) sind **nicht** enthalten (zu groß, nicht nötig).
- Der Stand der Handy-App stammt aus ihrem Fortschrittsprotokoll vom 06.10., nicht aus einer neuen Prüfung.
- Der Rechercheauftrag (Aufgabe K) wurde nicht ausgeführt.
