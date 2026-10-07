# BEFUNDE_DESKTOP.md — Fehler in der Desktop-App

**Kurzfassung:** Hier sammle ich, was mir an der produktiven Desktop-App auffällt. **Ich behebe nichts davon** (Leitplanke L1), ich schreibe es nur auf. Die Befunde stammen aus der vollständigen Quellcode-Analyse vom 06.10.2026; die ausführliche Fassung mit allen Formeln steht in `C:\tischbuchung_work\UEBERGABE_2026-10-06\02_BUTTONS.md`. Zeilenangaben beziehen sich auf `UEBERGABE_2026-10-06\src\Src\Screen1.pa.yaml`. Für die Handy-App ist jeder dieser Befunde zugleich eine Anforderung, es besser zu machen.

---

## Kritisch (können zu falschen Belegungen führen)

### BD-01 — Kollisionsabfrage ohne Zeitgrenze, in **beiden** Speichern-Knöpfen
**BELEGT.** `btnSpeichern` Z. 2734 und `btnSpeichernTischePanel` Z. 966:

```
bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)
```

Kein Zeitfilter. Die Abfrage lädt alle Buchungen dieses Tisches bis zum Datenzeilenlimit (1000). Darüber hinaus fehlen Zeilen stillschweigend, und eine Kollision wird nicht erkannt.

*Anmerkung zum Auftrag:* Abschnitt 7, D1 nennt nur `btnSpeichernTischePanel`. `btnSpeichern` hat denselben Fehler.

### BD-02 — Befund B0: Der Verwalten-Dialog prüft die falsche Buchung
**BELEGT.** `conVerwaltenDialog_1` im Buchungen-Tab speichert `varSelectedBuchungTab` (`btnVerlängern_1`, Z. 3708), aber alle zwölf Plus-/Minus-Properties lesen `varSelectedBuchung` (Z. 3753, 3765, 3802, 3814, 3851, 3862, 3884, 3896, 3934, 3946, 3984, 3996), also die zuletzt im **Grundriss** angeklickte Buchung.

Folge: Ein Verlängern-Knopf kann grün und freigegeben sein, obwohl die Verlängerung der angezeigten Buchung mit einer anderen kollidiert. Das ist der einzige belegte Weg zu einer stillen Doppelbuchung im heutigen Code. Beim Verkürzen kann umgekehrt eine Endzeit vor der Startzeit entstehen.

Die Korrektur K1 aus `ENTWURF_SPEICHERN.md` (eine Zeile `Set(varSelectedBuchung; ThisItem)` in `btnVerwalten_2.OnSelect`) ist **nicht eingebaut**.

### BD-03 — Verlängern prüft beim Speichern gar nicht
**BELEGT.** `btnVerlängern` (Z. 3256) und `btnVerlängern_1` (Z. 3702) schreiben ohne jede Kollisionsprüfung. Geprüft wird nur beim Einfärben der Plus-Knöpfe, mit dem Stand vom Öffnen des Dialogs. Zwischen Öffnen und Klicken kann jemand anders buchen.

### BD-04 — Keine Doppelklick-Sperre
**BELEGT.** Keiner der vier Knöpfe `btnSpeichern`, `btnSpeichernTischePanel`, `btnVerlängern`, `btnVerlängern_1` hat eine `DisplayMode`-Property (per Skript über alle 1985 Properties geprüft). Ein zweiter Klick während des Speicherns ist möglich. Die Korrektur K5 ist nicht eingebaut.

### BD-05 — `Remove` auf einer Variablen statt auf frischem Datensatz
**BELEGT.** `btnStornieren` Z. 3237:

```
=Remove(Tischbuchungen, varSelectedBuchung); Set(varZeigeVerwalten, false)
```

Kein `LookUp` auf den aktuellen Stand, kein `IfError`, kein `Refresh`, keine Meldung. Wurde die Buchung inzwischen anderswo gelöscht, läuft das Entfernen auf einen Datensatz, den es nicht mehr gibt. Das ist der wahrscheinliche Ursprung des „Item Not Found"-Fehlers.

### BD-06 — Eine Person kann zur selben Zeit zwei Tische buchen
**BELEGT durch Abwesenheit.** In keiner Formel der App kommt eine Prüfung vor, die eigene Buchungen zur selben Zeit an anderen Tischen sucht. Die Kollisionsprüfung filtert immer auf `Tisch.Value`.

---

## Meldungen, die nicht die Wahrheit sagen

### BD-07 — Zahlen stammen aus lokalen Collections, nicht aus SharePoint
**BELEGT.** `btnSpeichern` Z. 2805: `anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze)`. Was SharePoint tatsächlich angenommen hat, wird nie nachgelesen. Bei einem Teilausfall sagt die Meldung nur „Möglicherweise wurden einzelne Termine gespeichert".

### BD-08 — Der Kappungshinweis verdrängt die anderen Meldungen
**BELEGT.** `btnSpeichern` Z. 2810 und `btnSpeichernTischePanel` Z. 1032: `If(effektivesBisRoh > effektivesBis; Notify("Wiederholung wurde auf 2 Wochen begrenzt."); …)` steht **vor** der Kollisions- und der Erfolgsmeldung. Wird gekappt, erfährt der Nutzer nicht, ob überhaupt etwas gespeichert wurde.

### BD-09 — Erfolgsmeldung ohne Fehlerprüfung
**BELEGT.** `btnStornieren_1` Z. 3680: `Notify("Buchung storniert.", NotificationType.Success)` steht unbedingt nach `Remove` und `Refresh`, ohne `IfError`. `btnSpeichernTischePanel` meldet „gespeichert" aus einem `With`-Rumpf, dessen Variable `neuerEintrag` gar nicht ausgewertet wird (Z. 1009 bis 1023).

### BD-10 — Vier Aktualisieren-Knöpfe melden Erfolg ohne Prüfung
**BELEGT.** `Image6`, `btnHitArea_1`, `Icon1`, `Icon1_1` haben wortgleich `Set(varIsLoading, true); Refresh(Tischbuchungen); Set(varIsLoading, false); Notify("Aktualisiert.", NotificationType.Success)`. Kein `IfError`.

---

## Zustand und Aufräumen

### BD-11 — Der Aufräumblock läuft auch nach Fehlern
**BELEGT.** `btnSpeichern` Z. 2828 bis 2839 und `btnSpeichernTischePanel` Z. 1048 bis 1069 laufen unbedingt: Dialog schließt, Eingaben werden zurückgesetzt, auch wenn `speicherStatus = "fehler"` ist. Der Nutzer muss alles neu eingeben.

### BD-12 — `varAusgewaehltePlusDauer` wird einmal mit `0` statt `Blank()` belegt
**BELEGT.** `ddStockwerk.OnSelect` Z. 333: `Set(varAusgewaehltePlusDauer, 0)`. Überall sonst steht `Blank()`. Beide Verlängern-Knöpfe prüfen nur `IsBlank(varAusgewaehltePlusDauer)`; `0` ist nicht leer. Wer das Stockwerk wechselt und danach ohne Dauerwahl „Speichern" drückt, könnte eine Verlängerung um 0 Minuten auslösen statt der Warnung zu sehen. **Laufzeitverhalten ungetestet.**

### BD-13 — Doppelter Ladeanzeiger
**BELEGT.** `Screen1.LoadingSpinner = LoadingSpinner.Data` (Z. 13) **und** das eigene bildschirmfüllende Overlay `conLadeOverlay` (Z. 4341) sind gleichzeitig aktiv.

### BD-14 — Zwei widersprüchliche Statuslogiken
**BELEGT.** Eingecheckt ist im Grundriss **rot** `#EB3951` (Z. 80) und auf der Dashboard-Karte **grün** `#00A96B` (Z. 444). Siehe `ENTSCHEIDUNGEN.md` E-A09.

---

## Funktionale Lücken

### BD-15 — Check-in ohne Zeitfenster
**BELEGT.** `btnEincheckenHeute` (Z. 472) und `btnEinchecken` (Z. 3063) prüfen keine Uhrzeit. Eine Buchung für übermorgen kann heute eingecheckt werden. Die Kachelfarbe zeigt dann „eingecheckt" für einen Tisch, an dem niemand sitzt.

### BD-16 — Verlängern kennt keine 22:00-Grenze
**BELEGT.** `btnPlus1Std` bis `btnPlus3Std` prüfen nur auf Kollision. Eine Buchung kann über 22:00 hinaus und in den Folgetag verlängert werden, obwohl die Zeit-Dropdowns bei 22:00 enden.

### BD-17 — „Alle auswählen" markiert nur die geladenen Zeilen
**BELEGT.** `chkAlleAuswählen.OnCheck` Z. 4195: `ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)`. `AllItems` ist die geladene Teilmenge, nicht die Gesamtmenge. Korrektur A.3 ist nicht eingebaut.

### BD-18 — Kopierfehler in `chkAuswahl.X`
**BELEGT.** Z. 3601: `=btnVerwalten_2.X - btnVerwalten.Width - 10`. `btnVerwalten` liegt in einer anderen Galerie (`conDashboard.galTischbuchungenHeute`). Funktioniert nur zufällig, weil beide Knöpfe 50 breit sind. Korrektur A.4 ist nicht eingebaut.

### BD-19 — Kein Schutz gegen Buchungen in der Vergangenheit
**BELEGT durch Abwesenheit.** Keine Formel prüft `Startzeit >= Now()`. `dpAnsichtsDatum` hat kein Mindestdatum, und `dpDatum`/`dpDatumTischePanel` übernehmen dieses Datum als Vorbelegung.

### BD-20 — Serien an Wochenenden nicht möglich, obwohl vorgesehen
**BELEGT.** `varTagSa` und `varTagSo` werden in beiden Speichern-Knöpfen ausgewertet, aber es gibt keine Bedienelemente dafür (nur `tglTagMo` bis `tglTagFr`). Beide Variablen werden nur auf `false` gesetzt.

---

## Aufräumbares

### BD-21 — Zehn Variablen werden geschrieben und nie gelesen
**BELEGT**, bestätigt durch `app-UnusedVariables` in `AppCheckerResult.sarif`: `varZeigeVerlaengern`, `varWiederholenBis`, `varZeigeRaumInfo`, `varZeigeRaumVerwalten`, `varPanX`, `varPanY`, `varWiederholenBisGewaehlt`, `varStockwerkDropdownOffen`, `varMehrfachAuswahlModus`, `varSpinnerWinkel`.

`varMehrfachAuswahlModus` beantwortet die offene Frage 6 des Briefings: tot. Die wirksame Variable ist `varAuswahlModusAktiv`.

### BD-22 — Toter Raumcode
**BELEGT.** `conRaumBuchungenPanel`, `conRaumBestätigen` und `galRaumbuchungenHeute` sind über `Visible: =false` unerreichbar (`btnRaumHinzufügen.Visible` Z. 704, `galRaumbuchungenHeute.Visible` Z. 513). Sie bringen 21 Steuerelemente mit Verhaltensformel, 24 Delegationswarnungen und die beiden Listen `Räume` und `Raumbuchungen` mit.

### BD-23 — Toter Code in `dpWiederholenBis_1.OnChange`
**BELEGT.** Z. 1179: `=If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate)` berechnet einen Wert und verwirft ihn. Die Formel bewirkt nichts.

### BD-24 — Unerreichbarer Zweig „Täglich"
**BELEGT.** `varWiederholenModus` wird nirgends auf `"Taeglich"` gesetzt, nur auf `"Wochentage"`. Der Zweig `varWiederholenModus = "Taeglich"` in beiden Speichern-Knöpfen (Z. 2749, Z. 981) ist unerreichbar.

### BD-25 — Doppelte Anweisung
**BELEGT.** `btnAbbrechenTischePanel.OnSelect` Z. 1088 und 1089: `Set(varZeigeTischBuchungForm, false)` steht zweimal hintereinander.

### BD-26 — `Label14` liest das falsche Datumsfeld
**BELEGT.** Im Tische-Panel vergleichen `Label14.Color` (Z. 1193) und `Label14.Text` (Z. 1201) gegen `dpDatum.SelectedDate` — den Datumswähler des **Buchungsdialogs**, nicht gegen `dpDatumTischePanel.SelectedDate`. Der Hinweis „max. 2 Wochen" färbt sich also nach dem falschen Dialog.

---

## Neu aus dem Bau der Handy-App

### BD-27 — Ursache der 56 Delegationswarnungen: `CountRows` selbst
**BELEGT** an der Handy-App am 06.10.2026. Die Studio-App-Prüfung meldet zu `CountRows(Filter(Tischbuchungen, …)) > 0` wörtlich: „Der Vorgang ‚CountRows' wird durch diesen Connector nicht unterstützt." Das gilt auch dann, wenn alle Bedingungen im inneren `Filter` delegierbar sind. Die 56 Warnungen der Desktop-App stehen laut Briefing alle auf genau diesem Muster (Verlängern- und Dauer-Knöpfe, `btn5Std`, `btn9Std`, Raumcode).

**Behebung, an der Handy-App bestätigt:** `!IsBlank(LookUp(Tischbuchungen, …).ID)` statt `CountRows(Filter(…)) > 0`. Danach meldet die App-Prüfung keine Delegationswarnung mehr. Für die Desktop-App nur dokumentiert, nicht umgesetzt (L1).

**Ergänzende Beobachtung:** Ob zusätzlich Datensatzfelder auf der rechten Seite (`varSelectedBuchung.Tisch.Value`) eine Warnung auslösen, habe ich nicht isoliert geprüft. In der Handy-App habe ich sie vorsorglich durch einfache Variablen ersetzt; die Warnung verschwand aber erst mit dem Wegfall von `CountRows`. **UNSICHER.**

## Nicht beurteilbar ohne Messung

- Warum `galAlleTischbuchungen.Items` ein Delegationsdreieck zeigt, obwohl beide Filterbedingungen delegierbar sind
- Ob der neue Sammel-`Patch` in `btnSpeichern` `Person` und `Tisch` korrekt schreibt (Ü6)
- Ob er einen oder N Netzwerkaufrufe erzeugt (Ü5)
- Ob `chkAuswahl.OnCheck` beim Neuaufbau der Galerie Dubletten erzeugt
