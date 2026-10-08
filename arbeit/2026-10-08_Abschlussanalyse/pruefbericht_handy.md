# Prüfbericht Handy-App „Tischbuchung Handy“ (Stand Export 08.10.2026, 14:25)

Unabhängige Prüfung durch Claude Code, nur lesend. Grundlage: `A.lade_handy_fertig()` (h), `A.lade_handy_0810()` (h0), `A.lade_handy()` (hv), `A.lade_desktop_fertig()` (d), `Properties.json`, `AppCheckerResult.sarif`, `UMBAUPLAN_Handy_v2.md` + `handy_bloecke.json`, `fix_pruefung.js`, `AUFTRAG_Handy_Freigabe.md`, Gesamtplan Phase 8. Skripte liegen in `scratchpad/analyse_handy/`.

## Kurzfassung
- **Umbauplan v2 ist exakt drin:** Alle 16 Blöcke H2–H7 stimmen Zeichen für Zeichen mit `handy_bloecke.json` überein. `App.OnStart` (H1) ist um `varProfilFarbe` ergänzt, sonst gleich (belegt, maschinell verglichen).
- **Keine Testreste:** `varFreigabeMinuten` = 30, `lblTestErstellt` und `btnTestErstellt` gibt es nicht mehr. Keine Variable wird gelesen, ohne gesetzt zu werden, und keine wird gesetzt, ohne gelesen zu werden. Die App-Prüfung meldet keine Delegationswarnung (belegt).
- **Alle 6 Schreibstellen** haben die Zweifach-Sperre, setzen `varIsLoading` auf jedem Pfad zurück und lesen vor dem Schreiben frisch. Die Nachprüfungen bei Buchen, Verlängern und Einchecken sind pro Klick eindeutig (belegt).
- **Kein kritischer und kein hoher Befund in der App selbst.** Der wichtigste Befund ist **mittel**: Die App bemerkt keinen Tageswechsel. Bleibt sie über Nacht im Hintergrund offen, zeigt sie gestern als „Heute“, und der Check-in kann ausbleiben (H-1).
- **Regeln Desktop ↔ Handy:** Die Verfallsregel, 30 Min, 06:00/22:00, „zwei Tische“, Gesperrt und das Check-in-Fenster sind gleich. **Zwei echte Unterschiede** gibt es, beide schon für die nächste Desktop-Fassung vorgemerkt: Beim Einchecken gewinnt am Handy die ältere Buchung, am PC blockiert jede andere (D-1). Ein leeres `Erstellt` zählt nur am PC als verfallen (D-2). Systematische Doppelbuchungen entstehen daraus nur im Grenzfall.
- **B1–B11:** Alles erledigt, was im Repo dokumentiert ist. Achtung, die Nummern sind doppelt vergeben (Abschnitt 4).
- **Lese-Recht „nur eigene“:** Die Aussage stimmt. Am Handy sind 5 Properties mit 9 Abfragen betroffen, am PC 25. **Darf nie gesetzt werden.** Josias als Besitzer würde den Fehler selbst nicht sehen (Abschnitt 5).
- **Urteil:** Als Pilot go-live-fähig, mit 5 Punkten vor dem 14.10. (Abschnitt 6).

---

## 1. Befunde im aktuellen Stand `h`

| # | Schwere | Kennz. | `Steuerelement.Property` | Fehlerweg | Korrektur |
|---|---|---|---|---|---|
| H-1 | **mittel** | geschlussfolgert (Regel „Now()/Today() in Datenformeln“ belegt, CLAUDE.md §8) | `ddDatum.Items`, `lblHeuteTitel.Text`, `galHeute.Items` (`Today()`), `ddStart.Items`/`.Default` (`Now()`) | Die App bleibt in Power Apps Mobile über Nacht im Hintergrund offen. Am Morgen ist „Heute“ noch gestern und „Morgen“ in Wahrheit heute. `galHeute` zeigt die gestrigen Buchungen oder „keinen Tisch“. Die heutige Buchung ist nicht zu sehen, deshalb **checkt niemand ein, und sie verfällt nach 30 Min**. Wer „Morgen“ wählt, bucht heute (`lblZusammenfassung` zeigt zwar das echte Datum, das mildert es ab). Die Desktop-App hat dafür einen Tageswechsel im `Timer1`, das Handy nicht. | Vorschlag (in Studio testen): `App.OnStart` früh `Set(varHeute; Today())`. `tmrJetzt.OnTimerEnd`: `Set(varJetzt; Now());; If(Coalesce(varHeute; Today()) <> Today(); Set(varHeute; Today());; Reset(ddDatum);; Set(varNeuLaden; varNeuLaden + 1))`. In `ddDatum.Items`, `lblHeuteTitel.Text` und `galHeute.Items` `Today()` durch `Coalesce(varHeute; Today())` ersetzen. Alternativ bis dahin in der Kurzanleitung: „Morgens oben auf Aktualisieren tippen“. |
| H-2 | niedrig | belegt | `galHeute.Items`, `galMeine.Items`, `ddTisch.Items` | Es gibt kein automatisches Nachladen (wie am PC seit der Grundriss-Sperre). Eine am PC gebuchte Buchung für heute erscheint am Handy erst nach einer Aktion oder nach „Aktualisieren“. Wer das nicht weiß, sieht keinen Check-in-Knopf. | In die Kurzanleitung schreiben. Option: Ein eigener Takt nur für `galHeute` (`With({neuLaden: varNeuLaden; takt: varHeuteTakt}; …)`), den `tmrJetzt` alle 5 Min hochzählt, wenn `varTab = "heute"` ist. Das kostet 1 Abfrage pro 5 Min. |
| H-3 | niedrig | belegt (`Properties.json`) | App-Einstellung `usenonblockingonstartrule: true` | Der Handy-Chat schreibt „Nicht blockierender OnStart aus lassen“, im Export ist er aber **an**. Folgen geprüft: Vor dem Ende von OnStart ist `varTab` leer (kurz leerer Inhalt). `varJetzt` ist leer (Einchecken grau). `varListeGrenze` ist leer, dann zählen alle Buchungen als aktiv, also vorsichtig. `varProfilFarbe` ist leer. Die Sperren bleiben wirksam. Keine Fehlbuchung möglich. | Keine Formeländerung. Die Notiz des Handy-Chats korrigieren. Die Einstellung so lassen, eine blockierende Variante macht den Start langsamer. |
| H-4 | niedrig | belegt | `ddTisch.Items` (`"big table" in Lower(Titel)`) | Der Handy-Chat schlägt vor, den Big Table „besser über Gesperrt zu steuern“. **Das wäre falsch:** `btnSpeichern.OnSelect` und `btnHitArea` am PC prüfen `Gesperrt`. Der Big Table wäre dann auch im Grundriss nicht mehr buchbar, gegen Josias’ Entscheidung (Gesamtplan G0.3: „Den Big Table nicht sperren“). | Beim Namen bleiben. Wenn der Name sich ändern kann, eine eigene Ja/Nein-Spalte anlegen (z. B. `NurGrundriss`) und nur am Handy auswerten. |
| H-5 | niedrig | geschlussfolgert | `btnBuchen`, `btnVerl1/2`, `btnEincheckenH` (`Tisch.Value = var…Name`), `colTische` | Die Kollision wird über den **Tisch-Titel** geprüft. Josias will die Tische umbenennen („ab Desk 13 alles um 1 verschoben“). Wenn bei offener App umbenannt wird oder zwischendurch zwei Tische denselben Titel haben, sucht die Prüfung den alten Namen und findet nichts. Der Patch schreibt aber über die `Id`, und es entsteht eine Doppelbuchung. | Umbenennen **vor** dem Teilen, wenn niemand bucht, und von oben nach unten (erst Desk 18→19, dann 17→18 …). In SharePoint bei `Tische.Titel` „Eindeutige Werte erzwingen“ einschalten. Danach beide Apps neu starten. Am PC die Namen in `colTischPositionen`/`colTischPositionenUG` (`App.OnStart`) anpassen. |
| H-6 | niedrig | geschlussfolgert | Liste `Tischbuchungen` | Die Liste hat keine Indizes. Ab 5.000 Einträgen scheitern Filter auf nicht indizierten Spalten (Schwelle). Bei 30 Nutzern ist das nach etwa 8–10 Monaten so weit. | Jetzt, wenn Josias ohnehin alle Buchungen löscht, Indizes auf `Startzeit`, `Endzeit`, `Tisch` und `Person` anlegen (Listeneinstellungen → Indizierte Spalten). Auf einer leeren Liste dauert das Sekunden. |
| H-7 | niedrig | geschlussfolgert | `btnBuchen.OnSelect`, `btnVerl1/2.OnSelect` | `ClearCollect(colBuchBelegt/colBuchIch)` bzw. `colVerlBelegt/colVerlIch` laufen **vor** den Eingabeprüfungen („Ende nach Beginn“, „bereits beendet“, „verfallen“, „22:00“). In diesen Fehlerpfaden sind das 2 überflüssige Abfragen. In h0 lagen die LookUps erst im jeweiligen Zweig. | Nicht vor dem Go-Live. Später die Abfragen in den Zweig nach den reinen Eingabeprüfungen verschieben. |
| H-8 | niedrig | geschlussfolgert | `icoAktualisieren_1.OnSelect`, Start | Beim Start laufen 4 Abfragen (`Tische`, `galHeute`, `galMeine`, `ddTisch`), die unsichtbaren Tabs fragen mit. Nach jeder Aktion sind es 3. „Aktualisieren“ lädt `galHeute`/`galMeine` vermutlich doppelt: erst `Refresh`, dann noch einmal über `varNeuLaden`, und wegen `Now()` im Filter hilft kein Zwischenspeicher. | Beim Gerätetest am Montag im Monitor zählen. Ändern nur, wenn es spürbar ist. |
| H-9 | niedrig | UNSICHER | `ddDatum.Items` (`DateAdd(Today(); n; TimeUnit.Days)`) | Die Zeitumstellung am 25.10. ist bei Buchen, Verlängern, Beenden und Einchecken richtig gelöst (`DateTime(…)`, Minuten absolut, belegt). Offen ist nur: Falls `DateAdd(…; Days)` 24 h absolut rechnet, wäre ab dem 26.10. jedes `Tag` 23:00 des Vortags. Die Liste zeigte dann den 25.10. doppelt und der letzte Tag fehlte. Anzeige und Buchung bleiben dabei gleich, eine Buchung am falschen Tag gibt es nicht. | 1-Min-Test in Studio, Beschriftung `Text(DateAdd(Date(2026;10;24); 3; TimeUnit.Days); "dd.mm.yyyy hh:mm")` → erwartet `27.10.2026 00:00`. |
| H-10 | niedrig | geschlussfolgert | alle Filter `Person.Email = User().Email` | Bei Kollegen, deren Anmeldename (UPN) von der Mailadresse abweicht, ist „Heute“/„Meine“ leer, und „zwei Tische“ greift nicht. Die Desktop-App hat dieselbe Schwäche. | Beim Kollegentest gezielt darauf achten. Kein Umbau vor dem Go-Live. |
| H-11 | niedrig | belegt | `lblTischH.Width` (`Parent.Width - 300`) vs. `lblStatusH.X` (`Parent.Width - 330`) | Die beiden Beschriftungen überlappen um 58 px. Ein langer Tischname und „Nicht eingecheckt“ können sich überdecken. Vorher stand dort `- 360`. | `lblTischH.Width = Parent.Width - 360`. |
| H-12 | niedrig | belegt | `Properties.json` `AppDescription` | „Testphase, noch nicht freigegeben.“ erscheint in der App-Liste der Nutzer. | Vor dem Teilen ändern. |
| H-13 | niedrig | belegt | `btnVerl1/2.OnSelect` (beide Apps) | Beim Verlängern wird `Gesperrt` nicht geprüft. Einen Tisch, der nach dem Buchen gesperrt wurde, kann man weiter verlängern. | Hinnehmen, Josias sperrt selten. |
| – | Hinweis | belegt + getestet | `btnStornoJa`, `btnJetztBeenden` | Die Nachprüfung nutzt dieselbe Abfrage wie das Lesen davor (`LookUp(…; ID = varBuchungID)`), ist also nicht „pro Klick eindeutig“. Laut Testprotokoll (T-22/T-23, A-Tests) kommt sie richtig an. | Kein Handlungsbedarf. |

**Geprüft und in Ordnung (belegt):** Doppelklick-Sperre an allen 6 Schreibstellen. `varIsLoading` steht am Ende jedes Zweigs. `IfError` liegt um jeden Patch/Remove. Die ID kommt aus dem Patch (`varNeuID`). „Älterer gewinnt“ ist in Vor- und Nachprüfung gleich. Leeres `Erstellt` zählt nie als verfallen (alle 15 Vergleiche mit `Erstellt` abgesichert). `varJetzt` steuert nur Anzeigen und löst keine Abfrage aus. `tmrJetzt.Duration` fehlt im Export, das bedeutet Standard 60 s, so wie in `tmrJetzt.yaml`. Alle Filter sind delegierbar (Metadaten: `Created`, `Checkedin`, `Gesperrt` eq/lt/gt). `ClearCollect(colTische; Tische)` hat 34 Zeilen bei einer Grenze von 500. Beide Apps nutzen dieselben Listen-GUIDs.

## 2. Gleiche Regeln Desktop ↔ Handy

| Regel | Handy (h) | Desktop (d) | Gleich? |
|---|---|---|---|
| Verfallen | `!CheckedIn && Startzeit <= G && !IsBlank(Erstellt) && Erstellt <= G` | `!CheckedIn && Startzeit <= G && Erstellt <= G` | **fast** (D-2) |
| Minuten | `varFreigabeMinuten` 30, `Coalesce(…; 30)` | 30 | ja |
| Frühester Start / Ende | 06:00 / 22:00 (`ddStart.Items`, `DateTime(…;22;0;0)`) | 06:00 / 22:00 | ja |
| Vergangenheit | Prüfung: Beginn ≥ laufende halbe Stunde. Liste ab **laufender** halber Stunde | Prüfung gleich (`varNeuJetzt`). Liste ab **nächster** halber Stunde | Prüfung ja, Liste unterschiedlich (gewollt, Plan §3) |
| Zwei Tische | `colBuchIch`/`colVerlIch` ohne verfallene | `colNeuIch`/`colVerlIch` ohne verfallene | ja |
| Gesperrt | Liste aus `colTische` (Start/Aktualisieren), Buchen frisch `LookUp(Tische…)` | Buchen frisch, Panel/Grundriss | ja |
| Big Table | nie | Grundriss ja, Panel nein | gewollt |
| Einchecken | ab −30 Min bis Frist, nicht nach Ende | gleich | ja |
| Einchecken: andere Buchung am Tisch | nur **ältere** (`ID >= varCheckinID` raus) | **jede** andere (`ID = eigene` raus) | **nein** (D-1) |
| Liste „frei“ | Grenze `varListeGrenze` (Start, Tab Buchen, Aktualisieren) | Grenze beim letzten Laden von `colGrundriss` bzw. `varFreigabeGrenze` | Zeitpunkt verschieden, nur Anzeige |
| Beenden | Ende = laufende halbe Stunde | Auschecken: Ende = jetzt + 1 Min | verschieden, keine Doppelbuchung |
| Datum + Uhrzeit | `DateTime(…)` | `T.Value + varNeuStartZeit` | am 25.10. verschieden (D-3) |

| # | Schwere | Kennz. | `Steuerelement.Property` | Fehlerweg | Korrektur |
|---|---|---|---|---|---|
| D-1 | mittel | belegt (Formeln), Grenzfall geschlussfolgert | Handy `btnEincheckenH.OnSelect` ↔ Desktop `btnEinchecken.OnSelect` | Zwei überlappende aktive Buchungen entstehen nur durch gleichzeitiges Buchen. Dann kann die ältere am Handy einchecken, am PC aber nicht, dort verfällt sie. Grenzfall: Gehen die Uhren zweier Geräte an der 30-Min-Grenze um Sekunden auseinander, bucht B neu und checkt ein. Danach checkt A (ältere ID, nach A’s Uhr nicht verfallen) am Handy ein, weil die Handy-Prüfung neuere IDs ignoriert. **Dann sind zwei eingecheckt.** | Desktop auf „Älterer gewinnt“ bringen (ist schon vorgemerkt). Beide Apps sind dann gleich und der Grenzfall bleibt sehr selten. Das Handy nicht ändern. |
| D-2 | mittel | belegt (Formeln), Auswirkung UNSICHER | alle 43 Desktop-Vergleiche mit `Erstellt` (z. B. `btnSpeichern.OnSelect`, `ddTischePanel.Items`, Ladezeile `colGrundriss`) | Kommt `Erstellt` am PC in einer Sammlung nicht an (der Vorab-Test „Erstellt“ wurde am PC gestrichen), zählt der PC jede nicht eingecheckte Buchung 30 Min nach Beginn als verfallen. Das gilt auch für spät gebuchte. Beispiel: Am Handy wird um 10:25 für 10:00 gebucht, um 10:31 zeigt der PC den Tisch frei und lässt eine zweite Buchung zu. Die Handy-Person kann danach noch einchecken (Älterer gewinnt) → **Doppelbelegung**. | Desktop gleich halten: `!IsBlank(Erstellt) &&` ergänzen (vorgemerkt). **Test vor dem Go-Live:** am Handy um hh:20–hh:29 für hh:00 buchen, ab hh:31 am PC prüfen, ob der Tisch belegt ist. Er muss belegt sein. |
| D-3 | niedrig | geschlussfolgert | Desktop `btnSpeichern`/`btnSpeichernTischePanel` (`T.Value + varNeuStartZeit`), `varNeuJetzt` | Am So 25.10. landen Desktop-Buchungen eine Stunde zu früh (Datum + Zeit wird absolut addiert, an diesem Tag sind es 23 h). Das Handy rechnet richtig. | Für den Desktop schon vorgemerkt. Sonntag, sehr selten. |

**Ergebnis zu 2:** Mit vorhandenem `Erstellt` zeigen beide Apps zur gleichen Zeit und mit frischen Daten dieselben freien Tische. Unterschiede in der **Anzeige** entstehen nur, weil die Listen zu verschiedenen Zeitpunkten geladen werden. Beim Schreiben prüfen beide frisch. Doppelbuchungen sind nur über D-2 (wenn `Erstellt` fehlt) und den Grenzfall von D-1 möglich.

## 3. Was der Umbau gebracht hat

**hv (07.10.) → h (08.10. fertig), 40 Properties:**
- **Besser:**
  - B-Befunde: Verlängern mit 22:00 per `DateTime`, „bereits beendet“, „zwei Tische“ und Nachprüfung mit Rücknahme. Jetzt beenden nicht nach dem Ende, Ende auf die halbe Stunde. Storno-Knopf mit Sperre.
  - Dazu `tmrJetzt` und `App.OnError`.
  - H1–H7: Freigabe-Regel, Gesperrt, Einchecken bis zur Frist mit Prüfung „schon vergeben“, ID aus dem Patch, Stornieren und Beenden nur für eigene Buchungen, 06:00, Zeitumstellung beim Buchen.
  - **Der kritische Weg „Einchecken auf eine verfallene, neu vergebene Buchung“ ist geschlossen** (Test K2 laut Handy-Chat bestanden).
- **Schlechter oder neu:**
  - Ein Tisch, der nach dem Start gesperrt wird, steht bis zum Aktualisieren weiter in der Liste (beim Buchen abgefangen).
  - `lblTischH` überlappt mit dem Status (H-11).
  - Die Profilfarbe ist zufällig (Paket L hatte das am PC als Mangel geführt, Josias wollte es so).
  - `App.OnError` zeigt bei jedem Fehler „Verbindung zu SharePoint“, auch wenn die Ursache eine andere ist.

**h0 (08.10. 11:51) → h, 19 Properties:**
- **Besser:** Alles aus H1–H7 (siehe oben). Die Nachprüfung beim Buchen findet die eigene Buchung über die ID statt über Mail und Zeit und überschreibt `varBuchungID` nicht mehr.
- **Mehr Abfragen:**
  - +1 beim Buchen (Gesperrt).
  - +1 beim Einchecken (Prüfung „andere Buchung“).
  - +1–2 beim Aktualisieren (`colTische`).
  - +2 in Fehlerpfaden (H-7).
  - Spürbar ist das nicht. Der Monitor beim Gerätetest entscheidet.
- **Neu und vorsichtig:** Die Liste rechnet mit der eigenen Grenze `varListeGrenze`. Wer lange im Tab „Buchen“ bleibt, sieht freigegebene Tische weiter als belegt. Das ist harmlos.

## 4. B1–B11: abgedeckt?

Die Befunde B1–B11 sind im Repo **nur** über `quellen/…/05_HANDY_APP/skripte/fix_pruefung.js` dokumentiert. Das Skript nennt B1, B4, B5, B8 und B10 beim Namen. B2, B3, B6, B7, B9 und B11 stehen nur als unbenannte Änderungen im Skript (Verlängern-Block, beide Knöpfe). **Achtung, doppelte Nummern:** `UMBAUPLAN_Handy_v2.md` (Zeile 3) nennt mit „Handy-Befunde B5/B6/B7“ etwas anderes, nämlich die Rückmeldung des Handy-Chats zu ID aus dem Patch und Zeitumstellung.

| Befund (laut `fix_pruefung.js`) | Status | Fundstelle in h |
|---|---|---|
| B1 + B4 Jetzt beenden: nicht nach dem Ende, Ende auf die halbe Stunde, nicht vor Beginn | erledigt | `btnJetztBeenden.OnSelect` (`Now() >= varBuchung.Endzeit`, `varNeuEnde = With({ab: DateTime(…)}…)`) |
| B5 Einchecken mit eigener Variable `varCheckinID` | erledigt (mit H6) | `btnEincheckenH.OnSelect` |
| B8 Knopfanzeige mit `varJetzt` | erledigt (mit H6) | `btnEincheckenH.DisplayMode`, `.Text`, `lblStatusH.*` |
| B10 Stornieren-Knopf mit Sperre | erledigt | `btnStornierenD.OnSelect` |
| unbenannt (B2/B3/B6/B7/B9/B11, Zuordnung UNSICHER): Verlängern 22:00 per `DateTime` | erledigt | `btnVerl1/2.OnSelect` (`varTagesEnde = DateTime(…; 22; 0; 0)`) |
| unbenannt: Verlängern „bereits beendet“ | erledigt | `btnVerl1/2.OnSelect` (`varEndeAlt <= Now()`) |
| unbenannt: Verlängern „zwei Tische“ | erledigt | `btnVerl1/2.OnSelect` (`colVerlIch`) |
| unbenannt: Verlängern Nachprüfung mit Rücknahme | erledigt | `btnVerl1/2.OnSelect` (`colKollision`, Patch auf `varEndeAlt`) |
| `tmrJetzt` (eigene YAML) | erledigt | `tmrJetzt.OnTimerEnd` |
| Nachtrag „leerer Dialog nach ‚gibt es nicht mehr‘“ (T-22/23) | erledigt | `Set(varZeigeVerwalten; false)` in allen „gibt es nicht mehr“-Zweigen |
| „Handy-Befunde“ B5/B6 (v2): ID aus dem Patch | erledigt | `btnBuchen.OnSelect` (`varNeuID`) |
| „Handy-Befund“ B7 (v2): Zeitumstellung | erledigt | `btnBuchen.OnSelect` (`DateTime(…)`) |
| Gesamtplan Phase 8 (06:00) | erledigt = H7 | `ddStart.Items`, `ddStart.Default` |
| `AUFTRAG_Handy_Freigabe.md`: ddTisch, btnBuchen, Einchecken, Verlängern, Status „Verfallen“ in galHeute | erledigt | H3–H6 |
| `AUFTRAG_Handy_Freigabe.md`: Status in `galMeine` | bewusst weggelassen (N1, Josias) | – |

**Antwort an den Handy-Chat:** Umbauplan v2 deckt B1–B11 ab, und alles, was im Repo dokumentiert ist, steht in h. Es fehlt nichts. Wenn der Handy-Chat eine eigene Liste B1–B11 mit Titeln hat (Prüfbericht A28), soll er die sechs unbenannten Nummern gegen die vier Verlängern-Teile oben abhaken.

## 5. Lese-Recht „nur eigene Elemente lesen“

**Die Aussage stimmt** (belegt aus den Formeln, das SharePoint-Verhalten ist bekannt). Mit „Lesezugriff: nur selbst erstellte Elemente“ liefern alle Filter ohne Personen-Bedingung nur noch die eigenen Zeilen. Fremde Buchungen sind dann unsichtbar: **Jeder Tisch erscheint frei, außer den eigenen**, Vor- und Nachprüfung finden keinen Konflikt, und es kommt zu Doppelbuchungen ohne jede Warnung.

- **Handy, betroffen (5 Properties, 9 Abfragen):**
  - `ddTisch.Items` (belegte Tische)
  - `btnBuchen.OnSelect` (`colBuchBelegt`, Nachprüfung `colKollision`)
  - `btnVerl1.OnSelect` und `btnVerl2.OnSelect` (`colVerlBelegt`, `colKollision`)
  - `btnEincheckenH.OnSelect` (`colCheckinAndere`, zweimal)
- **Handy, nicht betroffen:** `galHeute`, `galMeine`, `colBuchIch` und `colVerlIch` filtern auf die eigene Person. Die Angabe des Handy-Chats „galHeute“ trifft also nicht zu. Diese Stellen gehen nur dann schief, wenn jemand für einen anderen bucht, denn es zählt der **Ersteller**.
- **Desktop, betroffen (25 Properties):**
  - alle Ladestellen von `colGrundriss` (`App.OnStart`, `Icon1`, `Icon1_1`, `Image6`, `btnHitArea_1`, `ddStockwerk`, `dpAnsichtsDatum`, `icoAktualisierenGrundriss`, `btnGrundrissAktualisieren`, `btnStornieren`, `btnStornieren_1`, `btnStornierenKlein`, `btnSpeichern`, `btnSpeichernTischePanel`, `btnEinchecken`, `btnVerlängern` …)
  - `ddTischePanel.Items`, `btn5Std`/`btn9Std` (`.DisplayMode`, `.Fill`)
  - `btnSpeichern`, `btnSpeichernTischePanel` (Prüfung und Nachlese)
  - `btnVerlängern`/`_1`, `btnVerwalten`/`_2` (Grenze), `btnEinchecken`, `btnHitArea`
  - Im Grundriss verschwinden außerdem alle Namen.
- **Tückisch:** Wer „Listenverhalten außer Kraft setzen“ hat (Besitzer, Vollzugriff, also Josias), sieht weiter alles. **Josias’ eigene Tests würden den Fehler nicht zeigen.**
- **Ebenso gilt:** Steht das Recht auf der Liste `Tische`, ist `colTische` leer, das Handy zeigt „kein Tisch frei“ und der PC einen leeren Grundriss.
- **Festhalten (Betriebshandbuch):** Lesezugriff auf `Tischbuchungen` und `Tische` immer „Alle Elemente lesen“. Erlaubt ist nur die Einschränkung beim **Bearbeiten** („nur eigene“).
- **Prüfen:** Liste → Einstellungen → Erweiterte Einstellungen → Lesezugriff. Den Gerätetest am Montag mit einem **normalen** Konto machen.

## 6. Urteil

**Die Handy-App ist als Pilot go-live-fähig.** Der Umbauplan ist vollständig und unverändert drin, an keiner Schreibstelle gibt es einen kritischen oder hohen Fehler, und der gefährliche Weg (Einchecken auf eine neu vergebene Buchung) ist zu. Die offenen Risiken liegen beim Betrieb und in den Unterschieden zum PC, nicht in der Handy-Logik.

**Vor dem 14.10.:**
1. **Lese-Recht prüfen und festschreiben** (Abschnitt 5). Beide Listen auf „Alle Elemente lesen“. Muss.
2. **Gerätetest am Montag mit einem normalen Konto:** buchen, einchecken, verfallen lassen (vorübergehend `Set(varFreigabeMinuten; 1)` per Testknopf, danach löschen und 30 prüfen). Dazu die Gegenprobe am PC und den **D-2-Test** (am Handy für die laufende halbe Stunde buchen, nach 30 Min am PC: Der Tisch muss belegt bleiben). Im Monitor die Abfragen beim Start und nach dem Buchen zählen. Muss.
3. **Tische umbenennen und Buchungen löschen, bevor geteilt wird.** Titel eindeutig erzwingen, von oben nach unten umbenennen, Desktop-Positionen anpassen, danach beide Apps neu starten (H-5). Bei der Gelegenheit die Indizes anlegen (H-6). Muss bzw. jetzt billig.
4. **Tageswechsel (H-1):** einbauen (4 Properties, Vorschlag oben) oder mindestens in die Kurzanleitung schreiben: „Morgens auf Aktualisieren tippen, sonst fehlt die heutige Buchung und der Check-in.“ Dringend empfohlen.
5. **Desktop gleich halten (D-1, D-2):** „Älterer gewinnt“ und `!IsBlank(Erstellt)` in die nächste Desktop-Fassung, mindestens den D-2-Test aus Punkt 2 bestehen. Empfohlen. Zusätzlich die App-Beschreibung ändern (H-12) und `lblTischH.Width` (H-11). Kosmetik.

Nicht nötig vor dem Go-Live: die Grundriss-Sperre fürs Handy (das Handy hat keinen Grundriss, das frische Lesen vor jedem Schreiben genügt), H-7, H-8, H-10, H-13.
