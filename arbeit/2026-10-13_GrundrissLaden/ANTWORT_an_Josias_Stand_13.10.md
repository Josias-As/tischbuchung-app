# Antwort an Josias: Stand 13.10., Nachtrag 5, Dokumente, GoBright-Import

13.10.2026 · zur Übergabe von Claude Code, Abschnitt 2 und 4 · Grundlage: Export Desktop 13.10. 09:59, Handy-Export 12.10. 12:05 (ein neuerer Handy-Export liegt mir nicht vor). Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Der Prüfstand von Claude Code stimmt** (belegt, maschinell nachgeprüft): 94 Hinweise, 0 Fehler. Nachtrag 5 ist **nicht** drin. Alle 21 Vorher-Fassungen passen noch unverändert, die Blöcke gelten also so, wie sie sind.
- **Die Einschätzung von Claude Code teile ich im Kern.** Nichts aus Nachtrag 5 ist für richtige Buchungen zwingend.
  - Damit korrigiere ich meine Abschlussanalyse. Dort stand „Nachtrag 5 vor dem Go-Live einfügen“. Grund war dein Auftrag zur Storno-Bestätigung und die Dokumente, nicht ein Fehler im Code.
- **Was ich anders sehe (4 Punkte):**
  1. **Handy: H8 ist ein Muss, und zwar die fehlende Zeile.** Im Handy-Export vom 12.10. ist H8 nur zu 3/4 drin, `varHeute` wird beim Start nicht gesetzt (belegt).
     - Folge: Etwa 1 Minute nach dem Start hält der Timer den Tag für gewechselt und setzt die Datumsauswahl auf „Heute“ zurück (belegt aus `tmrJetzt.OnTimerEnd`, Dauer Standard 60 s).
     - Wer in der ersten Minute „Morgen“ wählt und es nicht bemerkt, bucht für heute.
     - **Abhilfe:** eine Zeile `Set(varHeute; Today());;` in `App.OnStart` (Schritt **T0** in `HANDY_TISCH_ZEIGEN.md`, für den Handy-Chat). Ein halbes H8 ist schlechter als keins.
  2. **Nachtrag 6 fehlt in der Einschätzung.** Das ist dein eigener Fund: Eine verfallene Buchung öffnet den Check-in-Dialog.
     - Nicht gefährlich: Das Einchecken prüft frisch und meldet „zu spät“ (belegt).
     - Empfehlung: **R1** (3 Properties, Karte gesperrt) zusammen mit N4. R2/R3 („Neu buchen“) nach dem Go-Live.
     - Alle Vorher-Fassungen von Nachtrag 6 passen zum Export 13.10. (belegt).
  3. **N1–N3 nicht „wegen der Dokumente“ einfügen**, die sind in 5 Minuten angepasst (Tabelle unten). Der eigentliche Grund ist ein anderer:
     - `Remove` löscht endgültig.
     - Am ersten Tag benutzen viele die App zum ersten Mal.
     - Die Handy-App fragt vor dem Stornieren (V8).
     - **Meine Empfehlung:** einfügen, wenn heute 20 Minuten Test drin sind (Testbogen Nachtrag 5, Tests zum Stornieren). Sonst die Dokumente anpassen und N1–N3 in der ersten Woche nachholen.
  4. **Ein zweiter Widerspruch in der Kurzanleitung:** „Der Tab ‚Buchungen‘ lädt jedes Mal neu, wenn du ihn öffnest“ gilt erst mit **N7**. Ohne N7 zeigt der Tab den Stand vom letzten Aktualisieren.
     - Außerdem nennt das Betriebshandbuch noch **34 Tische**. Es sind **35** (OG 16, UG 19 inkl. Big Table; belegt aus Positionen und Tische-Liste 12.10.).
- **Der größte offene Punkt für morgen ist der GoBright-Import**, nicht der Code. Die Mail v4 sagt „wird nicht übernommen“, die Übergabe plant ~237 Buchungen per Flow. Das muss heute entschieden sein, **bevor** die Mail rausgeht (Abschnitt 3).

## 1. Nachtrag 5, Nachtrag 6, H8: Einordnung
| Teil | Inhalt | Claude Code | Ich | Begründung |
|---|---|---|---|---|
| N4 | S3b „Verfallen“ ohne Tippen, F5 `btn5Std.Fill`, G25 (1 Raumcode-Abfrage beim Start) | empfohlen | **empfohlen, heute** | 4 Properties, nur Anzeige und eine Bedingung, kein Schreiben. **`btn5Std.Fill` im Export ist die alte G-Fassung** (belegt, = Vorher-Fassung von N4): Der 5-Std-Knopf sieht belegt aus, wenn dort nur eine verfallene Buchung liegt. N4 holt F5 nach |
| N1–N3 | Stornieren mit Bestätigung, Rücksetzen | empfohlen (Dokumente) | **empfohlen, wenn heute getestet** | siehe Kurzfassung Punkt 3. Der Code in der Bestätigung ist die Export-Fassung unverändert, nur eingerückt (maschinell geprüft) |
| R1 (Nachtrag 6) | Karte bei verfallen/beendet nicht anklickbar | – | **empfohlen, mit N4** | dein Fund. 3 Properties. Rechnet mit derselben Regel wie S3b, deshalb mit N4 zusammen |
| N6 | Check-in-Erinnerung über E-Mail statt Anzeigename | nach Konten-Test | einverstanden | Wirkung nur, wenn `User().FullName` ≠ SharePoint-Anzeigename. Kein Risiko, aber auch kein Muss |
| N5, N7 | Raumcode-Abfragen weg, Tab-Liste nur im Tab | nach Go-Live | einverstanden | Nur Abfragen, keine sichtbaren Fehler. Passt zusammen mit „Grundriss-Laden v1“ in eine ruhige Stunde nach dem Go-Live |
| R2, R3 (Nachtrag 6) | „Neu buchen“ | – | nach Go-Live | neues Steuerelement, nicht unabhängig geprüft (deine Entscheidung) |
| H8 T0 (Handy) | `varHeute` beim Start | „H8 empfohlen“ | **Muss vor Go-Live** | siehe Kurzfassung Punkt 1 |
| K1 | `ddStockwerk.SelectionColor` dunkel | soll | **heute** | 1 Property, nur Farbe. Kontrast 1,7 : 1 → 7,2 : 1 (gerechnet). Block in `UEBERGABE_Grundriss_Laden_v1.md` |
| `Label3.Text` | festes „OG“? | prüfen | **kein Fehler** | belegt: Das „OG“ ist ein Vergleich mit `varSelectedTisch.Geschoss.Value`. Bei einem UG-Tisch steht „MMS Untergeschoss“ da |

**Reihenfolge heute (Desktop):** K1 → N4 → R1 → (N1–N3, falls Testzeit). Danach ein Export an mich. Ich gleiche ihn maschinell gegen den Soll-Stand ab, das dauert Minuten (Lehre vom 08.10.: „passt“ ≠ eingefügt).

**Zwingend bleiben die Betriebspunkte aus der Abschlussanalyse** (unverändert, keiner davon ist im Export prüfbar):
- Lesen auf beiden Listen = alle Elemente.
- Test 17 (Spätbuchung mit echten 30 Minuten).
- Sicherung `.msapp` beider Apps.
- Gerätetest Handy (Anmeldung am Firmenhandy).
- Check-in-Pflicht ganz oben in die Mail.
- **Vertretung für Michael:** Er ist seit 12.10. im Urlaub. Mindestens eine Person mit Rechten auf SharePoint und Power Platform benennen, die morgen erreichbar ist.

## 2. Dokumente: was zu ändern ist
Gilt für Kurzanleitung v4 und v5 (v5 = v4 + Handy-Abschnitt, im Repo) und Betriebshandbuch v4.

| Stelle | Wenn N1–N3 (bzw. N7) drin | Wenn nicht |
|---|---|---|
| Kurzanleitung, Zeile „**Stornieren:**“ | bleibt | „**Stornieren:** ‚Stornieren‘ tippen. Die Buchung ist sofort weg. Du kannst nur deine eigenen Buchungen stornieren.“ |
| Kurzanleitung, Zeile „**Mehrere stornieren:**“ | bleibt | „… eine antippen → ‚Stornieren‘.“ (ohne „Ja, 3 stornieren“) |
| Kurzanleitung, Absatz „Grundriss blass?“, letzter Satz | bleibt (mit N7) | „Der Tab ‚Buchungen‘ zeigt den Stand vom letzten Aktualisieren.“ |
| Kurzanleitung, Kopfzeile v4 | bleibt | „Stornieren mit Bestätigung“ streichen |
| Mail: „Bestehende GoBright-Buchungen werden **nicht** übernommen.“ | je nach Import-Entscheidung (Abschnitt 3) | |
| Betriebshandbuch, Tabelle Liste `Tische` | „**35 Tische (OG 16, UG 19 inkl. Big Table)**“ | gleich |
| Betriebshandbuch, Abschnitt Regeln „Stornieren mit Bestätigung …“ | bleibt | „Stornieren ohne Rückfrage, nur eigene Buchungen. Versehentlich storniert: Josias stellt die Zeile aus dem SharePoint-Papierkorb wieder her.“ |
| Betriebshandbuch, Störung „Stornieren geht nicht“ | bleibt | Zeile streichen |
| Betriebshandbuch, „… beim Öffnen des Tabs ‚Buchungen‘“ (kein automatisches Aktualisieren) | bleibt (mit N7) | den Halbsatz streichen |
| Betriebshandbuch, „Tisch umbenennen oder neuer Tisch“ | nach „Grundriss-Laden v1“: „`colTischPositionen`/`colTischPositionenUG` in **`App.Formulas`**“ | bis dahin `App.OnStart` (stimmt) |

Wenn du willst, erzeuge ich nach deiner Entscheidung fertige v6-Dateien. Das dauert Minuten.

## 3. GoBright-Import: übernehmen oder nicht?
**Der Widerspruch (belegt):** Die Mail v4 schreibt „Bestehende GoBright-Buchungen werden nicht übernommen. Bitte bucht ab sofort in der App“. Die Übergabe von Claude Code plant einen Flow-Import von ~237 Buchungen. Beides zusammen gibt Doppelbuchungen: Kollegen buchen neu, und der Import legt dieselben Zeiten noch einmal an.

**Meine Empfehlung:**
- **Ist die Mail schon raus, oder buchen Kollegen schon in der App:** nicht importieren. Die Mail bleibt, wie sie ist.
- **Ist die Mail noch nicht raus:** Importieren geht, aber nur, wenn es **heute** fertig und geprüft ist, und zwar **vor** der Mail. Danach die Mail ändern: „Eure GoBright-Buchungen ab 14.10. sind übernommen, bitte prüft sie unter ‚Meine Buchungen‘ und bucht sie nicht doppelt.“
- Schafft der Import es heute nicht sauber: nicht importieren. Halbe Importe sind das größte Risiko.

**Wenn importiert wird, muss der Flow Folgendes einhalten** (jeder Punkt ist eine Falle, die die App sonst abfängt, der Flow aber nicht):

| Nr | Punkt | Warum |
|---|---|---|
| I1 | **Tisch-Zuordnung:** alte GoBright-Namen → Namen in `Tische`. **UG 14–17 → 15–18**, der neue UG Desk 14 bekommt nichts. OG und Big Table bleiben gleich. Tisch als Lookup `{Id: <ID aus Tische>, Value: <Titel>}` | Die Kachel sucht über den **Namen** (belegt). Ein falscher Name zeigt den Tisch als frei → Doppelbuchung |
| I2 | **Person** mit Claims `i:0#.f|membership|<email klein>` | Ohne passende E-Mail erscheint die Buchung nicht unter „Meine“, und die Person kann sie nicht stornieren, verlängern oder einchecken (die App vergleicht `Person.Email`, belegt) |
| I3 | **Zeitzone:** Die Zeiten als Ortszeit mit Versatz schreiben, **+02:00 bis 25.10., ab 26.10. +01:00** (Zeitumstellung am 25.10.). Oder sauber in UTC umrechnen | Sonst sind alle Buchungen nach dem 25.10. um eine Stunde verschoben (geschlussfolgert, gleiche Falle wie in der Handy-App) |
| I4 | **Nur Buchungen ab 14.10.**, nur 06:00–22:00, Ende nach Beginn am selben Tag. Big Table darf rein (am PC für alle buchbar, deine Entscheidung 08.10.) | Die App-Regeln gelten für den Flow nicht. |
| I5 | **Kollisionen:** pro Zeile vorher prüfen, ob der Tisch zu der Zeit schon belegt ist oder die Person zur selben Zeit schon einen Tisch hat. Wenn ja, die Zeile **nicht** anlegen und in eine Liste schreiben | Die App prüft das beim Buchen, der Flow nicht |
| I6 | **Markierung:** `Titel` = „GoBright-Import“ | Die App schreibt `Titel` nicht (belegt), die Markierung stört also nichts. Bei einem Fehler lassen sich die Zeilen in SharePoint filtern und gesammelt löschen |
| I7 | `CheckedIn` = Nein, `SerienID` leer | Importierte Buchungen **verfallen wie alle anderen** 30 Min nach Beginn ohne Check-in, weil `Erstellt` (= Importzeit) vor dem Beginn liegt (Freigabe-Regel, belegt). Das gehört in die Mail. Leere `SerienID` zeigt jeden Termin einzeln |
| I8 | **Besitzer der Zeilen:** Die Zeilen gehören dem Konto der Flow-Verbindung (dir) | Solange „nur eigene Elemente“ **nicht** gesetzt ist (deine Entscheidung vom 08.10.), können die Personen ihre Buchungen trotzdem bearbeiten. Wird die Einstellung später gesetzt, können sie es nicht mehr (Betriebshandbuch) |
| I9 | **Erst 3 Zeilen testen:** je eine OG-, eine UG-15–18- und eine Buchung nach dem 25.10. Dann in der App prüfen: richtiger Tisch im Grundriss, richtige Uhrzeit, unter „Meine“ der Person, Stornieren durch die Person geht. Erst dann der Rest | |

**Fehlt mir für eine genauere Antwort:** ob die Mail schon raus ist, das GoBright-Exportformat (Spalten, Zeitzone, Tischnamen) und ob der Flow schon existiert. Mit einer CSV-Probe (5 Zeilen, Namen dürfen geschwärzt sein) baue ich dir die Zuordnung I1 und die Zeitumrechnung I3 als Tabelle.

## 4. Grundriss-Laden (Auftrag A)
Siehe `UEBERGABE_Grundriss_Laden_v1.md` im selben Ordner. Kurz:
- Der Plan von Claude Code trägt. Statt `colTische` nehme ich die benannte Formel `TischeLokal`, das empfiehlt auch die App-Prüfung selbst.
- Es gibt zwei Stufen: 0/0 weg, danach sofortiger Wechsel.
- **Nach dem Go-Live** einfügen. Nur K1 (eine Farbe) geht heute.
