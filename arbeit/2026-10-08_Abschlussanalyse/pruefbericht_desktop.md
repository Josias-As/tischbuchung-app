# Unabhängige Prüfung Desktop-App „Tischbuchung“, Stand `f` (Export 08.10. 14:26)

Geprüft wurden alle 2.071 Properties in `f`, der Vergleich mit `a` (07.10.) und mit dem Soll aus `soll.py`, `AppCheckerResult.sarif` (alt und neu), `Properties.json`, die Z-Reihenfolge in `Controls/4.json` und die Monitor-Traces 3–5 vom 07.10. Es wurde nichts im Repo geändert. Die Skripte liegen in `scratchpad/analyse_desktop/` (`h.py`, `vars.py`, `f_de.txt`).

## Kurzurteil

Im Code habe ich **keinen kritischen Fehler** gefunden. Alle 8 Schreibstellen sind sauber gebaut: Zweifach-Sperre, frisches Lesen, `IfError`, Nachprüfung, Ladezeile mit Stempel. Die Freigabe-Regel ist an allen schreibenden und prüfenden Stellen gleich. Es gibt keine Testreste. **Als Pilot ist die App go-live-fähig.** Die Risiken liegen beim Betrieb und in vier Punkten, die nur ein Test klären kann (siehe „Muss vor dem 14.10.“).

## Bekannte Abweichungen: Ergebnis der Prüfung

| Punkt | Ergebnis |
|---|---|
| S3b nicht eingefügt | **bestätigt.** `lblStatusHeute.Text/.Color` rechnen mit `varFreigabeGrenze`. Folgen siehe M5. |
| `btn5Std.Fill` in der G-Fassung | **bestätigt.** `LookUp` ohne Freigabe-Regel. Ein verfallener Termin färbt rot, der Knopf bleibt aber bedienbar (`DisplayMode` aus F5). |
| `recBuchungDanach1.Visible` ohne G25 | **bestätigt.** |
| `recBuchungDavor1.X/.Width` und `recBuchungDanach1.X/.Width/.Visible` fragen `Raumbuchungen` ab | **bestätigt** (Formel ohne Schutzbedingung). In `a` gemessen: 1 Abfrage je Property. `Label4/5.Text` sind geschützt. |
| `Timer1` statt `tmrAktualisieren` | **bestätigt.** `Duration` (15000) und `OnTimerEnd` stimmen Zeichen für Zeichen mit dem Soll überein. `Repeat`, `AutoStart` und `Visible = false` sind gesetzt. |
| `icoAktualisierenGrundriss` als Zusatz | **bestätigt.** Es liegt mit Z 7 unter der Sperre (Z 8). Neue App-Prüfungs-Hinweise: kein `AccessibleLabel`, kein `TabIndex`. |
| `btnGrundrissSperre`: Radius 10, kein `AccessibleLabel` | **bestätigt.** `OnSelect` fehlt, das ist der Standardwert `false` und gewollt. X/Y fehlen ebenfalls, Standard 0 = Soll. |
| Weitere kleine Abweichungen, nicht in der Liste | `btnGrundrissAktualisieren`: Breite 240 statt 280, `Size`/`FontWeight`/`AccessibleLabel` fehlen (nur Optik). Minus-Knöpfe mit „−“, einmal klein: „−2std“. `lblTischLeer_1` zeigt „-Keine Buchungen-“. Die Reihenfolge im Panel ist Datum → Beginn → Ende → Tisch statt G23. Das ist fachlich sogar besser, weil die Tischliste von Datum und Zeit abhängt. |

## Schreibstellen (Auftrag 1)

| Stelle | Sperre | `varIsLoading` auf allen Pfaden zurück | frisch gelesen | Ladezeile + Stempel | Freigabe-Regel |
|---|---|---|---|---|---|
| `btnSpeichern.OnSelect` | ja | ja (Ende der Kette, auch bei Prüf-Abbrüchen) | neu angelegt, Nachlese pro Klick eindeutig | ja (nur Zweig „gebucht/versucht“) | ja (Belegt, Ich, Nachlese) |
| `btnSpeichernTischePanel.OnSelect` | ja | ja | wie oben | ja | ja |
| `btnEinchecken.OnSelect` | ja (Rückfrage-Zweig bewusst außerhalb, setzt nur 1-s-Sperre) | ja | `LookUp` + Statusabgleich | ja | ja |
| `btnStornieren(_1).OnSelect` | ja | ja | `LookUp`, Eigentümer mit `Lower()` | ja | entfällt |
| `btnVerlängern(_1).OnSelect` | ja | ja | `LookUp` | ja | ja (eigene verfallene Buchung wird abgelehnt) |
| `btnStornierenKlein.OnSelect` | ja | ja | `colStornoFrisch` (nur eigene) | ja | entfällt |

Alle 17 Ladestellen von `colGrundriss` sind wortgleich (maschinell geprüft, nur der Meldetext unterscheidet sich). Jede setzt vorher `varFreigabeGrenze` und den Stempel nur im Erfolgszweig. `DropColumns(…; Erstellt)` steht als Bezeichner. Ein Typwechsel bei Variablen kommt nicht vor: `varSelectedBuchung` bekommt immer einen `Tischbuchungen`-Datensatz oder `Blank()`. Keine Variable wird gelesen, ohne irgendwo gesetzt zu werden.

## Befunde

### Mittel

**M1 Timer-Erinnerung über den Anzeigenamen statt über die E-Mail** (geschlussfolgert, UNSICHER)
- Stelle: `Timer1.OnTimerEnd`, Vorfilter `LookUp(colGrundriss; Name = User().FullName …)`.
- Fehlerweg: Der SharePoint-Anzeigename (`Person.DisplayName`) weicht von `User().FullName` ab (Schreibweise, Doppelname). Dann findet der Vorfilter nichts, und während die App offen ist, kommt nie eine Check-in-Erinnerung. Die Buchung verfällt ohne Hinweis. Beim Start funktioniert die Frage, weil sie über die E-Mail sucht.
- Korrektur: Vorfilter über die eigene Dashboard-Liste: `!IsBlank(LookUp(galTischbuchungenHeute.AllItems; !CheckedIn && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()).ID)`. Das ist eine einzige Property, es kommt keine Abfrage dazu, und es gilt nur, solange `varAnsichtsDatum = Today()` ist (das prüft der Timer schon). Alternativ im Test mit 2–3 Kollegen prüfen, ob die Erinnerung kommt.

**M2 Desktop und Handy verhalten sich bei Doppelbuchung und leerem `Erstellt` verschieden** (belegt aus den Exporten, Folge geschlussfolgert)
- Stellen: `btnEinchecken.OnSelect` (`colCheckinAndere`: jede fremde aktive Überlappung blockiert) gegenüber Handy `btnEincheckenH.OnSelect` („Älterer gewinnt“, `ID >= varCheckinID`). Dazu alle Desktop-Regeln ohne `!IsBlank(Erstellt)`, die das Handy hat.
- Fehlerweg: Zwei Personen buchen fast gleichzeitig denselben Tisch, und die Nachlese meldet das nur. Auf dem Handy kann der Ältere einchecken. Am PC wird auch der Ältere abgewiesen („schon an jemand anderen vergeben“). Checkt keiner ein, verfallen beide Buchungen. Selten.
- Dazu kommt: Die Nachprüfung nach dem Check-in-Patch wiederholt dieselbe Abfrage wie die Vorprüfung. Ob sie dann frisch vom Server kommt, ist UNSICHER (vgl. Nachtrag 4, „eindeutige URL“).
- Korrektur: in der nächsten Desktop-Fassung wie vorgemerkt (Älterer gewinnt, `!IsBlank(Erstellt)`, eindeutige Nachprüfung). Für den Go-Live nicht nötig.

**M3 `Erstellt` in Sammlungen und Variablen nicht nachgewiesen** (UNSICHER)
- Stellen: `RemoveIf(colNeuBelegt/colNeuIch/colNeuNachlese/colCheckinAndere/colVerlKonflikt/colKachel/colCheckinFrage; … Erstellt …)` und `varCheckinBuchung.Erstellt`, `varVerlBuchung.Erstellt`.
- Hintergrund: `sharepointselectsenabled = true`, die App lädt also nur die genutzten Spalten. Im Grundriss steht `B.Erstellt` direkt im `ForAll`, das ist sicher. In Sammlungen hängt es an der Datenflussanalyse.
- Fehlerweg, falls `Erstellt` dort leer ankommt: Spät gebucht um 08:20 für 08:00 bis 12:00. Ab 08:30 statt ab 08:50 gilt die Buchung als verfallen. Jemand anders kann den Tisch dann buchen, und der Inhaber wird beim Einchecken mit „Zu spät“ abgewiesen.
- Korrektur: Test „Spätbuchung“ (siehe Muss-Liste). Fällt er durch, die Handy-Schreibweise `!IsBlank(Erstellt) && …` übernehmen und `Erstellt` im `Filter` per `ForAll`-Projektion holen.

**M4 Buchungen-Tab fragt beim Start ab und veraltet** (belegt aus der Formel und gemessen in `a`)
- Stelle: `galAlleTischbuchungen.Items` (`Endzeit >= Now()`, ohne Schutzbedingung). Der Tab ist beim Start unsichtbar.
- Fehlerweg 1: Beim Start läuft eine Abfrage, obwohl der Tab nicht offen ist.
- Fehlerweg 2: Wer den Tab erst Stunden später öffnet, sieht schon beendete Buchungen. `btnStornieren_1` und `btnStornierenKlein` (dort nur über `colStornoFrisch` geschützt) löschen dann Verlauf, oder es kommt die Meldung „gibt es nicht mehr“.
- Korrektur: `If(varAktiverTab = "buchungen"; With({erzwingeNeuaufbau: varGalleryNeuAufbauen}; …))`. Beim Öffnen des Tabs wird die Liste dann frisch geladen, mit aktuellem `Now()`.

**M5 Status im Dashboard veraltet (Folge von S3b)** (belegt)
- Stelle: `lblStatusHeute.Text/.Color`.
- Fehlerweg: Die Buchung beginnt 08:00, die letzte Aktion war 08:10. Um 09:00 steht weiter „Einchecken“ in Orange. Erst ein Tippen zeigt „Zu spät“. Andersherum ist es nicht möglich, die Anzeige ist also nur zu optimistisch.
- Korrektur: S3b einfügen (rechnet mit `varJetztTakt`). Empfohlen vor dem Go-Live, weil es die Check-in-Pflicht sichtbar macht.

**M6 Betrieb am ersten Tag: Freigabe nach 30 Minuten** (geschlussfolgert)
- Fehlerweg: Am 14.10. kennt niemand die Check-in-Pflicht, und die Tischgeräte fallen weg. Wer um 08:00 bucht und um 08:45 kommt, findet den Tisch frei oder vergeben vor. Einchecken ist nur in der App möglich.
- Korrektur: In der Go-Live-Mail die Pflicht ganz oben nennen. Josias kann überlegen, `varFreigabeMinuten` in der ersten Woche höher zu setzen (eine Zeile in `App.OnStart`). Das Handy müsste dann gleich gesetzt werden, sonst gelten verschiedene Regeln.

### Niedrig

- **N1 Aktualisieren-Knöpfe ohne Sperre** (geschlussfolgert). Stellen: `Icon1_1`, `Icon1`, `Image6`, `btnHitArea_1`, `icoAktualisierenGrundriss`, `btnGrundrissAktualisieren` (`.OnSelect`). Sie setzen `varIsLoading` ohne Prüfung auf true und am Ende auf false. Mit der Maus verhindert das das Overlay (Z 14 über allem). Per Tastatur (Enter auf dem fokussierten Symbol) während einer laufenden Speicherung gibt das Ende des Aktualisierens die Sperre zu früh frei. Korrektur: Rumpf in `If(!varIsLoading; …)`.
- **N2 Überflüssige Abfragen** (geschlussfolgert). `btnStornieren(_1)`, `btnVerlängern(_1)` und `btnStornierenKlein` rufen nach `Remove`/`Patch` noch `Refresh(Tischbuchungen)` auf. Das sind etwa 2 zusätzliche Galerie-Abfragen. `btnEinchecken` lädt den Grundriss auch nach reinen Hinweisen („erst ab 30 Minuten“). Korrektur: `Refresh` streichen (wie N4 beim Speichern) und die Ladezeile nur nach einem Patch ausführen.
- **N3 Grundriss-Abfrage beim Start doppelt** (gemessen in `a`, Trace 3–5). Die `App.OnStart`-Abfrage geht zweimal raus, einmal mit `null`-Werten (0 Zeilen, vermutlich Vorabruf durch `formuladataprefetch`). Das kostet etwa 250–350 ms parallel und schadet nicht. In `f` ist es wahrscheinlich gleich. Neuer Trace nötig.
- **N4 Zeitumstellung 25.10.** (geschlussfolgert, wie U-Z1). `T.Value + varNeuStartZeit` sowie `DateAdd(Today(); Minuten)` in `varNeuJetzt`, `varCheckinNeuesEnde` und `btn5Std/btn9Std` verschieben **nur am Sonntag selbst** um 1 Std. `varVerlTagesende` rechnet ab dem Beginn und ist nicht betroffen. Keine Aktion. Optionaler 1-Minuten-Test in Studio: Beschriftung `Text(DateAdd(Date(2026;10;23); 3; TimeUnit.Days) + Time(8;0;0); "dd.mm.yyyy hh:mm")` muss „26.10.2026 08:00“ zeigen. Dann sind auch Serien über das Wochenende sicher (das hatte die frühere Prüfung schon als korrekt bewertet).
- **N5 Mitternacht** (UNSICHER). `dpAnsichtsDatum` hat kein `DefaultDate`, der Standard ist `Today()`. `Timer1` setzt nach Mitternacht `varAnsichtsDatum` neu und ruft `Reset(dpAnsichtsDatum)` auf. Der Datumswähler kann dann noch das Vortagsdatum zeigen, während die Liste schon „Heute“ zeigt. Nur bei über Nacht offener App. Korrektur: `dpAnsichtsDatum.DefaultDate = varAnsichtsDatum`.
- **N6 `Circle1.BorderColor`** (belegt, schon in `a`): prüft `varAnsichtsDatum` nicht. Für andere Tage zeigt der schwarze Ring die Belegung von heute. Korrektur: wie `Circle1.Fill` mit `If(varAnsichtsDatum = Today(); …; …)`.
- **N7 Gesperrt veraltet** (geschlussfolgert). `btnHitArea.OnSelect` und `ddTischePanel.Items` lesen `Gesperrt` aus dem beim Start geladenen `Tische`. Neu gesperrte Tische fängt das Speichern ab (frisches `LookUp`). **Entsperrte** Tische bleiben im Grundriss gesperrt, bis jemand das Stockwerk wechselt oder die App neu startet. Korrektur: `Refresh(Tische)` in `btnGrundrissAktualisieren.OnSelect` oder Josias’ Ablauf „nach dem Entsperren App neu starten“ in das Betriebshandbuch.
- **N8 Check-in-Dialog nicht modal** (belegt, Z-Reihenfolge). `conCheckinDialog` (Z 9) bleibt beim Öffnen des Panels (`btnTischHinzufügen` setzt `varZeigeCheckin` nicht zurück) über dem Grundriss stehen. Optik. Korrektur: `Set(varZeigeCheckin; false)` in `btnTischHinzufügen.OnSelect`.
- **N9 Verwalten vergangener Buchungen** (belegt). Wählt man im Dashboard einen früheren Tag, lassen sich dessen Buchungen stornieren oder verlängern. Verkürzen kann das Ende in die Vergangenheit legen. Fachlich unkritisch. Korrektur bei Bedarf: in `btnVerwalten.OnSelect` bei `ThisItem.Endzeit < Now()` nur einen Hinweis zeigen.
- **N10 Erinnerung endet zu früh** (belegt): Der Vorfilter in `Timer1` (`Startzeit > Now() − 30`) kennt die `Erstellt`-Hälfte nicht. Spät gebuchte Termine bekommen nach Beginn + 30 Min keine Erinnerung mehr, obwohl sie bis Erstellt + 30 gültig sind. Mit M1 zusammen beheben.
- **N11 Texte und Reste** (belegt). Leeres Dashboard zeigt „---“ (`lblTischLeer.Text`). Gemischte Schreibweise „−1Std/−2std/−3Std“, „+1Std“ ohne Leerzeichen. `varProfilFarbe` (`RandBetween`) ist ungenutzt, insgesamt 11 ungenutzte Variablen. „Bitte bis 30 Minuten nach Beginn einchecken“ ist bei Spätbuchungen nur vorsichtiger als die Regel, also kein Fehler. **Testknöpfe oder Testwerte gibt es nicht:** `varFreigabeMinuten` wird nur einmal gesetzt (30), `varGrundrissSperreSekunden` nur einmal (120). Keine Steuerelemente mit Test/Debug im Namen, keine fest eingetragene E-Mail.
- **N12 Panel fragt bei jeder Eingabe mehrfach ab** (gemessen in `a`, Trace 4: `btn5Std/btn9Std.DisplayMode` je 12–13 Mal). Jede Änderung von Datum, Zeit oder Tisch löst etwa 5 Abfragen aus (`ddTischePanel.Items` sowie `btn5Std/btn9Std` mit `.DisplayMode` und `.Fill`). `ForAll(Tische …)` in `ddTischePanel.Items` läuft auch bei geschlossenem Panel einmal beim Start. Nach dem Go-Live zusammenfassen.

## Abfragen (Auftrag 2)

| Anlass | Abfragen in `f` (geschlussfolgert aus den Formeln) | `a` (gemessen 07.10.) |
|---|---|---|
| Start, ohne Tippen | etwa 12–15: OnStart Check-in-Frage 1 (+1 `LookUp` bei Treffer), Grundriss 1 (+1 Vorabruf), `galTischbuchungenHeute` 1, `galAlleTischbuchungen` 1 (unsichtbar), `Tische` 3–4 (`TischNrOG/UG`, `Gallery1`, `ddTischePanel` unsichtbar), `Raumbuchungen` 5 (`recBuchung*`, unsichtbar, bekannt) | **50** (36 × `Raumbuchungen`, 10 × `Tischbuchungen`, 3 × `Tische`, 1 × `Räume`) |
| `Timer1` alle 15 s | 0. Nur bei passender Erinnerung höchstens 1–2 Abfragen, gedrosselt auf 5 Min | – |
| Kachel antippen | 1 (+1 `LookUp` bei belegtem Tisch) | – |
| Buchen (Dialog) | etwa 7 + n (Gesperrt, Belegt, Ich, n Einzel-Anlagen, Nachlese, Grundriss, 2 Galerien) | Serie mit 11 Terminen ~4,7 s (L2) |
| Verwalten öffnen | 1 (B0, die Plus-Knöpfe fragen nicht mehr ab) | 8–13 je Plus/Minus-Knopf |
| Verlängern, Stornieren, Einchecken | je etwa 6–8 (davon 2 überflüssig, N2) | – |
| Aktualisieren | 3 | – |

- **Delegation:** Die App-Prüfung meldet für `Tischbuchungen` keine Warnung mehr. Am 07.10. waren es 46. Die übrigen 10 Warnungen betreffen nur den stillgelegten Raumcode (`galRäume`, `recBuchung*`). Die Filter auf `Person.Email = User().Email` laufen auf dem Server (in `a` an der URL gemessen: `Person/EMail eq '…'`). Das Zeilenlimit ist 1000.
- **`Now()`/`Today()` in Datenformeln:** `galTischbuchungenHeute.Items` und `galAlleTischbuchungen.Items` (veralten bis zur nächsten Änderung, siehe M4). `Rectangle1/Circle1/Label1` im Grundriss veralten auch, aber die Grundriss-Sperre zwingt nach 120 s zum Neuladen, und damit ist es gelöst. `ddStart`/`ddStartTischePanel` rechnen richtig mit `varDialogJetzt`/`varPanelJetzt`.

## Logik (Auftrag 4): bestätigt

- **Freigabe-Regel:** Sie lautet `!CheckedIn && Startzeit <= G && Erstellt <= G` (bzw. ihre Verneinung) und steht gleich in OnStart, Grundriss (17×), Speichern (Belegt, Ich, Nachlese), Einchecken, Verlängern, Verwalten-Öffnen, Kachel, `ddTischePanel`, `btn5Std/btn9Std.DisplayMode` und `btn9Std.Fill`. Ausnahmen: `btn5Std.Fill` (bekannt), `lblStatusHeute` (S3b) und der Timer-Vorfilter (N10). Die Handy-App hat dieselbe Regel mit 30 Min, zusätzlich `!IsBlank(Erstellt)` (M2).
- **06:00–22:00:** Start ab 06:00 bzw. ab der nächsten halben Stunde, letzter Start 21:30, Ende höchstens 22:00 (`ddStart/ddEnde.Items`, Panel gleich). Verlängern prüft `varVerlTagesende`. F-L1 ist behoben.
- **Keine Buchung in der Vergangenheit:** Gegen `varNeuJetzt` (aktuelle halbe Stunde). **Keine zwei Tische:** `colNeuIch` beim Buchen, `colVerlIch` beim Verlängern.
- **Grundriss-Sperre und Dialoge:** Die Sperre liegt nur in `conGrundriss` (Z 1). Alle Dialoge liegen darüber (Z 6–11), das Lade-Overlay ganz oben (Z 14). Sie erscheint erst nach dem Ende von OnStart (`varJetztTakt` wird zuletzt gesetzt) und bei Ladefehlern sofort. Der Tageswechsel leert den Stempel. Die Sperre deckt `ddStockwerk` und `icoAktualisierenGrundriss` ab (gewollt). Es bleibt die offene Frage an Josias: 120 s und kein automatisches Neuladen.
- **Check-in-Frage:** Beim Start über die E-Mail, im Timer nur einmal je Buchung (`varCheckinGefragtID`). M1 beachten.
- **Auschecken:** Erstes Tippen fragt nach und setzt 1 s Sperre. Das zweite Tippen beendet die Buchung (Ende = jetzt + 1 Min). Vor Beginn heißt Auschecken „CheckedIn = false“. Der Status wird gegen frisch gelesene Daten abgeglichen. `varAuscheckFrageID` wird beim Öffnen über die Liste zurückgesetzt.

## App-Prüfung (Auftrag 5)

| | 07.10. (`a`) | 08.10. (`f`) |
|---|---|---|
| Hinweise gesamt | 134 | 92 |
| Delegation (`SuggestRemoteExecutionHint*`) | 56 (46 Tisch, 10 Raum) | 10 (nur Raum) |
| `ForAllWithMutation` | 1 | 0 |
| Ungenutzte Variablen | 10 | 11 (+`varProfilFarbe`) |
| Barrierefreiheit (Label/TabIndex/Fokus) | 63 | 67 (neu: `icoAktualisierenGrundriss` ×2, `btnGrundrissSperre` ×2) |
| Fehler | 0 | 0 |

`ParserErrorCount = 1` steht in beiden Exporten (`Properties.json`), ist also unverändert und nicht neu. Die Ursache ist nicht ermittelt (UNSICHER, vermutlich alt).

## Was hat sich gegenüber `a` verändert?

**Verbessert:**
- Doppelklick-Sperre an allen 8 Schreibstellen (vorher 0).
- Frisches Lesen, `IfError` und Nachprüfung überall (vorher teilweise).
- Startabfragen etwa 50 → 12–15. Das ist aus den Formeln geschlussfolgert und muss mit einem neuen Trace bestätigt werden.
- Delegationswarnungen für Tische 46 → 0.
- Verwalten-Knöpfe ohne Abfragen.
- Freigabe in der App, ohne zu löschen.
- Tischauswahl im Panel zeigt nur freie Tische.
- Gesperrt-Spalte wird geprüft.
- Datum/Zeit im Dialog werden beim Öffnen zurückgesetzt (F-L11).

**Verschlechtert oder neu zu tragen:**
- Ein Speichervorgang braucht 2–3 Abfragen mehr (Gesperrt, Ich, Nachlese). Bei Einzelbuchungen ist das kaum spürbar.
- Die Grundriss-Sperre nach 120 s ist eine neue Hürde für alle Nutzer (offene Entscheidung).
- Die Dashboard-Listen aktualisieren sich nicht mehr selbst.
- Stornieren geht ohne Rückfrage (Josias’ Entscheidung).

## Muss vor dem 14.10.

1. **Veröffentlichen und sichern.** Den Stand `f` veröffentlichen, falls noch nicht geschehen (aus dem Export nicht erkennbar), und die `.msapp` als Rückfall sichern.
2. **Test Spätbuchung und Freigabe mit echten 30 Minuten (klärt M3).**
   - Person A bucht um :20 für :00 und checkt nicht ein.
   - Um :35 sieht Person B den Tisch noch als belegt.
   - Um :55 ist er für B frei, und A wird beim Einchecken mit „Zu spät“ abgewiesen.
   - Ist der Tisch schon um :35 frei, kommt `Erstellt` in den Sammlungen leer an. Dann muss die Regel angepasst werden, bevor die App live geht.
3. **Test der Rückmeldungen.** Einchecken, Auschecken, Verlängern und Stornieren müssen die Erfolgsmeldung zeigen, nicht „nicht angekommen“. Das schließt einen Zwischenspeicher bei den Nachprüfungen aus. Dazu Doppelklick auf jeden Knopf: Es darf nur eine Aktion ausgeführt werden.
4. **Check-in-Erinnerung mit 2–3 Kollegen prüfen (M1).** App offen lassen, Buchung beginnt in 25 Min: Kommt die Frage? Wenn nicht, die Ersatzformel aus M1 einfügen.
5. **Neuen Monitor-Trace aufnehmen** (Start und eine Buchung) und mit den 50 Startabfragen vom 07.10. vergleichen.
6. **Betrieb klären.** In der Go-Live-Mail steht die Check-in-Pflicht ganz oben (M6). Josias entscheidet über die Grundriss-Sperre (120 s). SharePoint-Rechte: Lesen auf alle Elemente, Bearbeiten nur eigene. Vertretung für Michael ab 12.10.

**Empfohlen, aber kein Muss:**
- S3b einfügen (M5).
- `galAlleTischbuchungen.Items` mit Tab-Bedingung (M4).
- N1, N2 und N7.
