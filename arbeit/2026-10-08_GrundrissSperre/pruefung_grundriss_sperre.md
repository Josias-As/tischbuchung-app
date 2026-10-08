# Unabhängige Prüfung: Grundriss-Sperre (08.10.2026)

Ein Prüf-Agent hat den Endstand selbst nachgebaut: Export + G1 G2 G3 G6[N4] G7 G9–G13 G15–G20 G25 + F2.1 + `bloecke.json`. Das eigene Skript lag im Scratchpad, keine Repo-Datei wurde geändert.

**Urteil: keine kritischen, keine hohen, 3 mittlere und 7 niedrige Befunde. Alle sind eingearbeitet.**

| Nr | Befund (kurz) | Einarbeitung |
|---|---|---|
| M1 | `usenonblockingonstartrule: true` (belegt): Während OnStart ist `varGrundrissStand` leer, die Sperre blitzt bei jedem Start auf, und der Knopf ist schon bedienbar | `Set(varJetztTakt; Now())` steht am **Ende** von OnStart. Beide `Visible` beginnen mit `!IsBlank(varJetztTakt) && …`. Generator prüft das. Test 2 |
| M2 | Ohne Laden im Timer veralten `lblStatusHeute` (hängt an `varFreigabeGrenze`) und `galTischbuchungenHeute`. Die Abschaffung des automatischen Aktualisierens ist Josias' Entscheidung | **Anders gelöst als vorgeschlagen:** Neuer Schritt S3b. `lblStatusHeute.Text`/`.Color` rechnen mit `varJetztTakt`. Der Vorschlag war, `varFreigabeGrenze` bei jedem Tick zu setzen. Das hätte `ddTischePanel.Items` (`ForAll` über `Tische`) neu rechnen lassen, ob aus dem Zwischenspeicher, ist unbelegt. Die Entscheidung steht als eigener Abschnitt im Dokument, mit Folgen für die Dashboard-Listen. Der F2.1-Testpunkt „F8 Timer aktualisiert“ ist durch Test 8 ersetzt |
| M3 | Rückfall nicht ausführbar (Verweis auf F2.1 Anhang A falsch), kein Anhang mit Originalen, S4 allein zurücknehmen lässt S3 stehen | Anhang A enthält die F2.1-Fassungen aller 19 geänderten Properties mit Herkunft. Der Rückfall-Text ist korrigiert: „S4 nur zusammen mit S3, nie S3 allein“ |
| N1 | Die Erinnerung fragt auch bei laufenden und verfallenen Buchungen im veralteten `colGrundriss`, alle 5 Minuten bis zum Ende | Vorprüfung um `Startzeit > DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); …)` ergänzt. Nachteil wie im Befund genannt: Eine spät angelegte Buchung, deren Beginn schon über 30 Minuten zurückliegt, wird nicht erinnert. Der Text ist richtiggestellt |
| N2 | Notweg (F2.1 Anhang D) lädt ohne Stempel | Im Dokument vermerkt. Der Notweg ist nicht mehr nötig, weil F2 eingefügt ist. Die Folge wäre harmlos |
| N3 | Fläche ohne `AccessibleLabel`. Per Tastatur sind die Elemente darunter erreichbar | `AccessibleLabel` gesetzt. Die Tastatur ist als Grenze dokumentiert |
| N4 | Aufgeklappte `ddStockwerk`-Liste fälschlich als belegt markiert. S-U1 lässt sich stützen | Als geschlussfolgert umformuliert. S-U1 mit der transparenten `btnHitArea` (belegt) gestützt |
| N5 | In Studio verdeckt die Fläche die Kacheln | Abschnitt „Hinweise für Studio“ (Strukturansicht) |
| N6 | 2:00–2:15 statt „2 Minuten“, eine Abfrage um Mitternacht, Drosselung im Hintergrund-Tab | Text korrigiert, S-U3 neu, Test 9 |
| N7 | Fehlende Tests | Tests 2 (Start), 6 (offline), 8 (Erinnerung ≤ 15 s), 9 (Status „Verfallen“ ohne Tippen). Die Tests sind an die Halbstunden-Startliste angepasst |

**Vom Prüfer als in Ordnung bestätigt** (Auszug):
- Ladestellen vollständig: 17 Schreibstellen auf `colGrundriss` im Endstand, alle mit Stempel nur im Erfolgszweig. Die noch nicht eingefügten G-Schritte bringen keine weitere Ladestelle.
- Diffs: An den Ladestellen ist nur der Stempel geändert.
- Sichtbarkeitslogik einschließlich Fehlerfall und Tageswechsel.
- Timer: Takt vor dem Dialog-Gate, Drosselung korrekt, U11 entfällt.
- Ebenen belegt über ZIndex in `Controls/4.json`: `conGrundriss` hat 1, die Dialoge 3–14.
- Alle Properties der klassischen Schaltfläche existieren.

**Nach dem Einarbeiten:**
- Generator erneut gelaufen: 0 Fehler, 53 Properties.
- Zusätzlich geprüft: Takt am Ende von OnStart, Takt-Schutz in `Visible`, `varFreigabeGrenze` im Timer nur in der Erinnerung, Variante „streng“ (Anhang B) ohne Abfrage.
- S3b und Anhang B sind **nur maschinell geprüft**, nicht erneut unabhängig.
