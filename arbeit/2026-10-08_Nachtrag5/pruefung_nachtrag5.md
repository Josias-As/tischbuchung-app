# Prüfbericht Nachtrag 5 (Desktop) und H8 (Handy), 08.10.2026

Grundlage: `A.lade_desktop_fertig()` / `A.lade_handy_fertig()`. Eigene Skripte in `scratchpad/pruef_n5/`. Im Repo wurde nichts geändert.

## Kurzfassung
- **Die Formeln sind in Ordnung.** Ich habe keinen kritischen Fehler gefunden und keinen Weg, auf dem eine fremde oder nicht erfragte Buchung gelöscht wird. `varIsLoading` bleibt nirgends hängen.
- **Das Problem ist der Testbogen.**
  - Ein **hoher** Befund: Nach Test 12 läuft der Testmodus weiter. Test 14 („Muss“) meldet dann fälschlich „`Erstellt` leer → nicht veröffentlichen“.
  - Drei **mittlere** Befunde: Test 4 (5 Std), Test 6 (Einchecken zu früh) und Tests 6/8/9 parallel zur Wartezeit lassen sich so nicht ausführen bzw. erwarten Falsches.
- Bei N7 gibt es ein **mittleres UNSICHERES** Risiko: Beim Neuaufbau der Liste können Einträge in der Auswahl doppelt vorkommen. Dann stimmen die Zahlen in den Meldungen nicht. Es wird trotzdem nichts Falsches gelöscht.
- H8 ist korrekt: keine Endlosschleife, und der Start mit nicht blockierendem OnStart läuft sauber. Es bleiben nur niedrige Punkte.

## Was ich nachgeprüft habe (ohne Befund)
- **Blöcke und Diffs:** Die 18 Blöcke im Dokument sind zeichengleich mit `bloecke.json`. Jeder `vorher_de` ist gleich dem Export. Rückübersetzung und Klammern sind ok.
- **Bestätigungszweig:** Ich habe den Zweig selbst ausgeschnitten und zurückgerückt. Er ist bei allen 3 Knöpfen **identisch mit dem Export**. Der Frage-Zweig hat weder Abfrage noch Schreiben noch `varIsLoading`. Die Frage wird vor `Remove` zurückgesetzt (belegt).
- **Schreibstellen:** `Remove(Tischbuchungen…)` gibt es nur in den 3 Storno-Knöpfen (belegt).
- **Dialoge öffnen:** Nur `btnVerwalten` und `btnVerwalten_2` öffnen die Verwalten-Dialoge, beide setzen mit N3 zurück. `btnHitArea`, `ddStockwerk`, `btnEincheckenHeute` und `btnTabBuchungen` schließen `conVerwaltenDialog`. `varSelectedBuchung(Tab)` ändert sich bei offenem Dialog nur über die Nachlese nach dem Verlängern, und die hat dieselbe ID (belegt).
- **Die Bestätigung löscht immer genau die erfragte ID:**
  - Einzel-Storno: Die Bedingung ist `varStornoFrageID = varSelectedBuchung.ID`, gelöscht wird `varSelectedBuchung.ID`.
  - Mehrfach-Storno: Gelöscht wird `colStornoZiele` = frisch gelesen ∩ Auswahl, und die Auswahl muss textgleich mit der Frage sein.
  - „Alle auswählen“ und jede Änderung an den Haken ändern den Text, die App fragt dann neu.
  - Gleiche Auswahl in anderer Reihenfolge gibt einen anderen Text. Die App fragt dann einmal mehr, das ist sicher.
- **Typen:**
  - `varStornoFrageID` bekommt nur Zahlen (`0`, `.ID`), `varStornoFrageAuswahl` nur Text (`""`, `Concat`).
  - Solange sie leer sind: `Blank > 0` ist falsch und `Blank <> "…"` ist wahr. Dann wird gefragt und nicht gelöscht, der Knopf zeigt „Stornieren“.
  - Beide Namen gibt es im Export noch nicht (belegt).
- **Steuerelemente:** Alle referenzierten Steuerelemente gibt es in der jeweiligen App (`galTischbuchungenHeute`, `recZeitleisteBg`, `ddDatum` usw.). Die übrigen Treffer sind Spalten- und `As`-Namen.
- **N4:** Ich habe das Soll aus G (gemeldet) + F2.1 F1–F7 + S1–S4 selbst gegen den Export verglichen. Die Abweichungen sind genau S3b, F5 (`btn5Std.Fill`) und G25 (`recBuchungDanach1.Visible`). Dazu kommen G23 (Josias' Farben) und S4 (Standardwerte und Optik). Das Dokument stimmt (belegt).
- **N5:** `conRaumBestätigen.Visible = varZeigeRaumBestätigung` und `recBuchungDavor1.Visible` beginnt mit `varZeigeRaumBestätigung &&`. `Danach1` bekommt das mit N4. Die Rechtecke sind also unsichtbar, wenn die Raumbestätigung geschlossen ist (belegt). Danach steht jede Raum-Abfrage außerhalb von Verhaltensformeln hinter `varZeigeRaumBestätigung` oder `varZeigeRaumBuchungForm`. `galRäume.Items` ist geschützt, `App.OnStart` hat keine (belegt).
- **N6:**
  - Woher die Daten kommen: `galTischbuchungenHeute.Items` ist `Filter(Tischbuchungen…)` mit vollen Datensätzen, nur eigene Buchungen (E-Mail), nur am Ansichtstag. `CheckedIn` und `Erstellt` liest `lblStatusHeute` in der Galerie, die Spalten werden also mitgeladen (belegt).
  - Bedingung: Der Vorfilter `!CheckedIn && (Startzeit > G || Erstellt > G)` ist genau die Negation von `RemoveIf(CheckedIn || (Startzeit <= G && Erstellt <= G))`, also gleichwertig zur Freigabe-Regel. Ein leeres `Erstellt` wird in beiden gleich behandelt (bekannt, vorgemerkt).
  - Erreichbarkeit: Der Timer liegt auf `Screen1`, `AllItems` ist von dort erreichbar. Der Timer fragt nur bei `varAktiverTab = "dashboard"` und `varAnsichtsDatum = Today()`.
- **N7:** `galAlleTischbuchungen` lesen nur Steuerelemente in `conBuchungen`: `chkAlleAuswählen`, `lblTischLeer_1`, `tglAuswahlModus`, `conVerwaltenDialog_1`, `Image3_2` (in der Galerie) und `lblÜberschriftBuchungen`. Breiten und Positionen lesen nur `.X`/`.Width`/`.Y`, nicht `Items`. `"buchungen"` ist genau der Wert aus `btnTabBuchungen` (belegt).
- **H8:**
  - Keine Schleife: Die Bedingung ist nach `Set(varHeute; Today())` falsch. `ddDatum`, `ddStart` und `ddEnde` haben kein `OnChange` (belegt).
  - Timer und OnStart: `tmrJetzt` hat `AutoStart`/`Repeat` = true und keine `Duration`, also den Standard von 60 s. OnStart setzt `varHeute` gleich nach `varJetzt`, also lange vor dem ersten Takt. `Coalesce` deckt die ersten Millisekunden ab (`usenonblockingonstartrule: true`, belegt).
  - Listen: `galHeute` und `galMeine` werden über `varNeuLaden` ganz neu berechnet, `Today()` und `Now()` sind dann neu (geschlussfolgert, Standardverhalten).
  - Zeitauswahl: `ddStart.Items`/`.Default` hängen an `ddDatum.Selected`. Nach dem Tageswechsel ist `Tag = Today()`, also gilt ab 06:00 bzw. ab der laufenden halben Stunde. `ddEnde` folgt `ddStart`.
- **Test 14 ist am Handy machbar:** `ddStart` beginnt bei der laufenden halben Stunde, und `btnBuchen` lehnt erst Zeiten vor der laufenden halben Stunde ab (belegt).

## Befunde

### B1 · hoch · geschlussfolgert (Studio-Standardverhalten)
**Stelle:** Testbogen Punkt 12 und 14 (auch 15).
**Fehlerweg:**
1. Test 12 löscht den Testknopf und prüft nur den **Text** von `App.OnStart`. `varFreigabeMinuten` bleibt in der laufenden Studio-Sitzung aber auf 1, bis OnStart neu läuft.
2. Test 14: Um hh:35 gilt `Erstellt` (hh:20) ≤ hh:34. Der Tisch ist frei.
3. Laut Bogen heißt das „`Erstellt` kommt leer an → nicht veröffentlichen“. Das ist ein Fehlalarm vor dem Go-Live.
4. Auch Test 15 (Einchecken) kann dann „Zu spät“ melden.

**Korrektur:** Test 12 ergänzen: „Danach `App` → `OnStart` ausführen (oder Studio-Vorschau neu laden). Kontrolle: Eine Buchung zur nächsten halben Stunde zeigt 2 Minuten nach Beginn noch ‚Einchecken‘, nicht ‚Verfallen‘.“

### B2 · mittel · belegt
**Stelle:** Testbogen Punkt 4 und Test N4 („F5“).
**Fehlerweg:**
1. `btn5Std.Fill` und `.DisplayMode` rechnen mit dem Fenster **nächste halbe Stunde ab dem Öffnen des Panels** (`varPanelJetzt`) + 5 Std. Der gewählte Beginn zählt nicht. `btn5Std.OnSelect` überschreibt den Beginn ebenfalls mit „ab jetzt“.
2. Test 4 läuft direkt nach Test 3, zwischen T+1 und T+30. Das Fenster beginnt dann bei T+30, und darin liegt deine **aktive** Buchung T+30–T+60.
3. Folge: „5 Std“ ist rot und gesperrt, nicht „bedienbar“.
4. Außerdem ist die Farbe für frei **hellgrün** (`ColorFade(#00A96B; 70%)`), nicht „blau“.

**Korrektur:**
- Test 4 **vor** Test 3 ausführen, zwischen T+1 und T+30. Panel neu öffnen, „heute“, Beginn nicht ändern, Tisch X wählen.
- Erwartung: X steht in der Liste, „5 Std“ ist hellgrün und bedienbar, solange bis 22:00 Platz ist.
- Im Test N4 ebenso „hellgrün“ schreiben und „die verfallene Buchung muss im Fenster nächste halbe Stunde + 5 Std liegen“.

### B3 · mittel · belegt
**Stelle:** Testbogen Punkt 6.
**Fehlerweg:**
- Eine Buchung „zur nächsten halben Stunde“ liegt am PC höchstens 30 Min in der Zukunft (`RoundUp`). „Mehr als 30 Min vorher“ und damit die Meldung „erst ab 30 Minuten vor Beginn“ sind so nicht erreichbar.
- Außerdem braucht „Zu spät“ eine **zweite**, nicht eingecheckte Buchung, weil die erste im Fenster eingecheckt wurde.

**Korrektur:**
- 6a: Buchung zur **übernächsten** halben Stunde, sofort „Einchecken“ → „erst ab 30 Minuten …“. Ab 30 Min vor Beginn → „Eingecheckt.“
- 6b: eigene Buchung B zur nächsten halben Stunde, Testmodus, ab Beginn + 1 Min „Einchecken“ → „Zu spät …“.

### B4 · mittel · belegt
**Stelle:** Testbogen Vorbereitung 4 („Tests 6–11 in der Wartezeit“) und Punkte 6, 8, 9.
**Fehlerweg:**
1. Die Tests 6, 8 und 9 legen je eine eigene Buchung „zur nächsten halben Stunde“ an. Während der Wartezeit ist das immer derselbe Zeitpunkt (T bzw. T+30 = Buchung aus Test 3).
2. `btnSpeichern` lehnt die zweite mit „Du hast in dieser Zeit schon einen Tisch gebucht.“ ab, solange die erste nicht verfallen ist.
3. Test 8: `Timer1` wählt die **früheste** offene eigene Buchung, und `varErinnerungAb` drosselt nach jedem Vorfilter-Treffer 5 Minuten.
4. Ist z. B. Buchung 3 schon erfragt (`varCheckinGefragtID`), erscheint für die neue Buchung keine Frage, oder erst nach bis zu 5 Min 15 s. Die Erwartung „nach höchstens 15 s“ stimmt dann nicht.

**Korrektur:**
- Die Tests 6–9 erst nach Test 5 ausführen und die Buchungen aus 2–5 vorher stornieren (oder nach Test 13).
- Tests 8 und 9 mit **derselben** Buchung (Frage erscheint → „Später“/schließen, nicht einchecken → ab Beginn + 1 Min „Verfallen“).
- Erwartung Test 8: „höchstens 15 s, wenn keine andere eigene, nicht eingecheckte Buchung in den nächsten 30 Min liegt, sonst bis 5 Min“.

### B5 · mittel · UNSICHER
**Stelle:** N7 `galAlleTischbuchungen.Items` zusammen mit `chkAuswahl.OnCheck = Collect(colAusgewaehlteBuchungen; ThisItem)` und `chkAlleAuswählen.Default`/`OnUncheck`.
**Fehlerweg:**
1. Mit N7 wird die Liste bei **jedem** Tab-Wechsel leer und neu aufgebaut. Bisher blieb sie stehen.
2. Löst ein `Default` = wahr beim Neuaufbau `OnCheck` aus (in Foren oft berichtet, nicht gemessen), stehen ausgewählte Buchungen doppelt in `colAusgewaehlteBuchungen`.
3. Folge: Der Knopf zeigt „Ja, 6 stornieren“ bei 3 Haken, und die Meldung lautet „3 von 6 … die übrigen waren bereits storniert“.
4. Umgekehrt: Ist „Alle auswählen“ gesetzt, kippt `chkAlleAuswählen.Default` beim Verlassen des Tabs auf falsch. Löst das `OnUncheck` aus, wird die Auswahl still geleert.
5. Es wird nie etwas Falsches gelöscht, weil `colStornoZiele` frisch gelesen wird. Falsch sind nur die Zahlen.

**Korrektur:**
- `chkAuswahl.OnCheck` = `If(IsBlank(LookUp(colAusgewaehlteBuchungen; ID = ThisItem.ID)); Collect(colAusgewaehlteBuchungen; ThisItem))`. Eine Property, wirkt in jedem Fall.
- Testschritt N7-4: Mehrfachauswahl, 2 von 3 anhaken, zum Dashboard und zurück. Der Knopf zeigt nach dem Antippen „Ja, 2 stornieren“, nicht 4.

### B6 · niedrig · belegt
**Stelle:** N1/N3, gemeinsame `varStornoFrageID` für Dashboard- und Tab-Dialog.
**Fehlerweg:**
1. Im Tab ist der Verwalten-Dialog für Buchung 5 offen (`varZeigeVerwaltenTab` bleibt beim Tabwechsel wahr).
2. Auf dem Dashboard wird dieselbe Buchung 5 geöffnet → „Stornieren“ (Frage) → Tab „Buchungen“.
3. `btnStornieren_1` zeigt sofort „Ja, stornieren“, ein Tipp löscht 5.
4. Ebenso bleibt die Frage nach „Verlängern“ im selben Dialog stehen.

Es ist immer dieselbe, schon erfragte Buchung, und der Knopf zeigt „Ja, stornieren“.
**Korrektur (optional):** `Set(varStornoFrageID; 0);;` an den Anfang von `btnTabBuchungen.OnSelect` und `btnTabDashboard.OnSelect`.

### B7 · niedrig · UNSICHER
**Stelle:** Frage-Zweig in N1/N2.
**Fehlerweg:** Zuerst wird `varStornoFrageID` bzw. `varStornoFrageAuswahl` gesetzt, **danach** die 1-s-Sperre. Wertet Power Apps einen zweiten Klick zwischen beiden `Set` aus (E-07 zeigt, dass Klicks sich überholen können), wäre die Frage schon gesetzt, die Sperre aber noch nicht. Dann würde der zweite Klick bestätigen.
**Korrektur:** Reihenfolge tauschen, `Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;` als erste Anweisung im Frage-Zweig. Den Generator-Test („Frage-Zweig mit 1-s-Sperre“) entsprechend anpassen.

### B8 · niedrig · belegt
**Stelle:** Texte v4.
**Fehlerweg:**
- Kurzanleitung: „Listen … im Tab ‚Buchungen‘ aktualisieren sich nicht von selbst“. Mit N7 lädt der Tab bei jedem Öffnen neu. Im Betriebshandbuch fehlen bei „lädt nur beim Tippen (…)“ der Tab-Wechsel und das Antippen einer Kachel bzw. eines Verwalten-Dialogs.
- Stornieren: Ein zweiter Tipp innerhalb von 1 s wird **ohne Meldung** ignoriert, obwohl der Knopf schon „Ja, stornieren“ zeigt. Das kann verwirren.
- Notbetrieb: „verfällt 30 Min nach dem Anlegen“ gilt nur, wenn der Beginn vor dem Anlegen liegt.

**Korrektur:**
- „Die Liste im Tab ‚Buchungen‘ lädt beim Öffnen des Tabs neu, das Dashboard nach ‚Aktualisieren‘.“
- „… dann (kurz warten) ‚Ja, stornieren‘ tippen.“
- „… verfällt 30 Min nach Beginn bzw. nach dem Anlegen, je nachdem, was später ist.“

### B9 · niedrig · geschlussfolgert
**Stelle:** H8 `tmrJetzt.OnTimerEnd`, `Reset(ddDatum)`.
**Fehlerweg:** Der Reset um Mitternacht verwirft auch ein bewusst gewähltes späteres Datum. Wer gerade bucht, bucht dann ohne Hinweis für heute. Das ist selten (00:00, Formular offen). Ob die klassische Dropdown-Auswahl ohne Reset bei neuen `Items` stehen bliebe, ist UNSICHER.
**Korrektur:** So lassen (ein veraltetes „Heute“ ist das größere Risiko). Den Test aus der Abschlussanalyse §5 um die Erwartung ergänzen: „Nach dem Takt steht ‚Heute, <heutiges Datum>‘ ausgewählt und ‚Beginn‘ bei der laufenden halben Stunde.“

### B10 · niedrig · belegt
**Stelle:** H8 `App.OnStart` (ganze Property).
**Fehlerweg:** Der Block beruht auf dem Export 14:25. Der Handy-Chat arbeitet mit YAML-Quellen, die weiter sein können. Ersetzt man die ganze Property, gehen neuere OnStart-Änderungen verloren.
**Korrektur:** Vor dem Einfügen den Diff (`vorher_de`) mit Studio vergleichen. Weicht er ab, nur `Set(varHeute; Today());;` hinter `Set(varJetzt; Now());;` ergänzen und das dokumentieren.

### B11 · niedrig · belegt
**Stelle:** H8, Dokumentation.
**Fehlerweg:** H8 hat nur `handy_h8_bloecke.json`, kein Übergabedokument mit Diff, Rückfall und Test. Den Test gibt es nur in `ABSCHLUSSANALYSE.md` §5. Außerdem hängt `ddDatum.Items` weiter an `Hour(Now()) >= 22`, das sich nicht neu berechnet. Das ist harmlos, weil `ddStart` nach 21:30 leer ist.
**Korrektur:** In die Übergabe an den Handy-Chat Rückfall (alte Fassungen aus `vorher_de`) und Test (B9) aufnehmen.

## Offene Punkte für die Studio-Prüfung (UNSICHER, Dokument N-U1 bis N-U4 bestätigt)
- N-U1: Passt „Ja, stornieren“ in 136,7 px ohne Umbruch?
- N-U3: Blitzt die Liste bzw. „-Keine Buchungen-“ beim Öffnen des Tabs auf?
- N-U4: Sind `galTischbuchungenHeute.AllItems` im Timer gefüllt? Ich halte das für plausibel.
- Neu dazu: B5 (doppelte Auswahl nach Tabwechsel) und B7 (Reihenfolge der `Set` im Frage-Zweig).

---

## Einarbeitung (Claude Code, 08.10.)
| Befund | Einarbeitung |
|---|---|
| B1 Testmodus bleibt nach dem Löschen des Testknopfs | Test 16: „Dann **OnStart ausführen**“. Test 17 mit Kontrollbuchung (orange um hh:35, sonst läuft der Testmodus noch) |
| B2 `btn5Std` misst ab dem Panel-Beginn, Farbe hellgrün | Test 10 vor eigener Buchung am Tisch X, Beginn wie vorgeschlagen, Erwartung „hellgrün“ |
| B3 „zu früh“ mit der nächsten halben Stunde nicht erreichbar | Test 4 mit **E** ab T + 30. „Zu spät“ mit eigener Buchung **S** (Test 8) |
| B4 Tests kollidieren („zwei Tische“), Erinnerung gedrosselt | Testbogen neu mit Zeitachse N/T und getrennten Zeiten S, E, X, Y. Erinnerung (Test 3) mit der frühesten Buchung, einmal. Storno (Test 15) ohne die schon beendeten S/E |
| B5 doppelte Auswahl nach Tab-Wechsel (UNSICHER) | `chkAuswahl.OnCheck` idempotent (in N7), N-U5, Test N7 Schritt 4. N7 als „kein Muss“ gekennzeichnet |
| B6 gemeinsame Frage-ID über Tabs | `btnTabDashboard.OnSelect` und `btnTabBuchungen.OnSelect` setzen die Frage zurück (N3) |
| B7 Reihenfolge im Frage-Zweig | 1-s-Sperre ist die erste Anweisung, Generator prüft das |
| B8 Texte v4 | Tab lädt beim Öffnen, „kurz warten“, Notbetrieb „späterer Zeitpunkt aus Beginn und Anlegen“, Fall „Stornieren geht nicht“ |
| B9 `Reset(ddDatum)` um Mitternacht | so gelassen, im H8-Dokument unter „Bekannt und gewollt“, Test ergänzt |
| B10 `App.OnStart` ganz ersetzen | H8-Dokument: erst vergleichen, sonst nur die eine Zeile ergänzen |
| B11 H8 ohne Übergabe | `HANDY_H8_Tageswechsel.md` mit Blöcken, Test, Rückfall, Anhang |

Nach dem Einarbeiten: `nachtrag5.py` 0 Fehler (21 Properties), `handy_h8.py` 0 Fehler. Die Änderungen nach der Prüfung (N3-Tabwechsel, `chkAuswahl.OnCheck`, Reihenfolge im Frage-Zweig, Testbogen) sind **nur maschinell** geprüft.
