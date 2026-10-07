# TESTPROTOKOLL.md — Jeder Test mit Datum, Erwartung, Ergebnis, Beleg

**Kurzfassung:** Hier steht jeder Test, den ich ausgeführt habe, mit Datum und Uhrzeit, den Schritten, der Erwartung, dem tatsächlichen Ergebnis und dem Beleg. Ein Test ohne Beleg gilt als nicht ausgeführt. Bisher sind die Lesefunktion „Meine Buchungen" und die Darstellung auf zwei Bildschirmgrößen geprüft; alle Schreibfunktionen stehen noch aus. Die Prüfstufen P1 bis P5 stehen in `AUFTRAG_MOBIL.md` Abschnitt 5.3.

---

## Prüfstufen

| Stufe | Was | Beleg |
|---|---|---|
| P1 | Kompiliert ohne Fehler | Ausgabe zitiert |
| P2 | Keine neuen Delegationswarnungen, oder jede begründet unkritisch | Liste hier |
| P3 | Läuft zur Laufzeit in Handy-Größe (390 × 844 und 360 × 800) | Screenshot in `screenshots\` |
| P4 | Bei jeder Schreiboperation: Nachlese in SharePoint | Ergebnis hier |
| P5 | Bei jeder schreibenden Formel: Angriff durch Prüf-Subagent in frischem Kontext | Fazit in `ENTSCHEIDUNGEN.md` |

---

## Ausgeführte Tests

### Messung — Koordinatensystem der App
**Datum:** 06.10.2026, ca. 15:25 Uhr
**Schritte:** Temporäres Label `lblDebug` mit `App.Width`, `App.Height` und `varTab` in der Geräteemulation 390 × 844 abgelesen.
**Ergebnis:** `App 780 x 1688 | Screen 780 x 1688 | varTab: heute`
**Folgerung:** Das Koordinatensystem ist exakt **verdoppelt**; eine App-Einheit entspricht einem halben CSS-Pixel. Alle Maße und Schriftgrößen wurden daraufhin verdoppelt (Tippflächen 96 Einheiten = 48 px, Fließtext 24, Überschriften 30 bis 34).

### P1 — App-Prüfung, Bereich Formeln (A04)
**Datum:** 06.10.2026, ca. 15:28 Uhr
**Schritte:** Studio → App-Überprüfung → Formeln.
**Erwartung:** keine Fehler.
**Ergebnis:** **bestanden.** Die Anzeige lautet wörtlich „Keine Fehler gefunden".
**Beleg:** `screenshots\A04_app_pruefung_formeln_keine_fehler_2026-10-06.jpg`

### T-01 — „Meine Buchungen" zeigt die eigenen kommenden Buchungen (A16)
**Datum:** 06.10.2026, ca. 15:30 Uhr
**Schritte:** Vorschau starten, Geräteemulation iPhone 390 × 844, Tab „Meine" antippen.
**Erwartung:** Alle eigenen Buchungen mit Endzeit in der Zukunft, chronologisch nach Startzeit, je mit Wochentag.
**Ergebnis:** **bestanden.** Angezeigt wurden unter anderem OG Desk 1 am Dienstag, 06.10.2026 von 14:30 bis 19:30; OG Desk 8 am Dienstag, 06.10.2026 von 15:30 bis 20:30; OG Desk 1 am Mittwoch, 07.10.2026 von 08:00 bis 08:30; weitere Termine an OG Desk 1 am 08.10., 12.10. und 13.10. Reihenfolge aufsteigend nach Startzeit, Wochentag ausgeschrieben.
**Beleg:** `screenshots\A03_A16_meine_390x844_korrekte_groessen.jpg`
**Vollständigkeits-Gegenprobe (06.10.2026, 16:21):** SharePoint direkt gelesen (REST-GET, siehe unten „Nachlese-Methode"): eigene Buchungen mit `Endzeit >= jetzt` = **23 Zeilen**, IDs nach Startzeit: 482, 483, 494, 480, 493, 474, 489, 486, 475, 488, 481, 485, 479, 491, 473, 490, 495, 477, 492, 478, 484, 487, 476. Ein temporäres Label in der App mit `galMeine.AllItemsCount` und `Concat(galMeine.AllItems, Text(ID), ", ")` zeigte **„MEINE (23)"** mit **denselben IDs in derselben Reihenfolge**. Label danach gelöscht.
**Ergebnis: bestanden, vollständig.** Beleg `screenshots\T01_meine_23_IDs_wie_sharepoint.png`

### T-25 — Darstellung bei 390 × 844 (A03)
**Datum:** 06.10.2026, ca. 15:32 Uhr
**Schritte:** Vorschau, Geräteauswahl „Apple iPhone 12, 13, 14, 14 Pro (390 × 844)".
**Erwartung:** Kopfzeile, Inhalt und Tab-Leiste füllen die Breite, kein horizontales Scrollen.
**Ergebnis:** **bestanden.**
**Beleg:** `screenshots\A03_A16_meine_390x844_korrekte_groessen.jpg`

### T-26 — Darstellung bei 360 × 800 (A03)
**Datum:** 06.10.2026, ca. 15:33 Uhr
**Schritte:** Vorschau, Geräteauswahl „Benutzerdefiniert", Breite 360, Höhe 800.
**Erwartung:** wie T-25.
**Ergebnis:** **bestanden**, kein horizontales Scrollen.
**Mangel gefunden und behoben:** Der Kopfzeilentitel war auf „Tischbuc..." abgeschnitten. Logo von 215 auf 170 Einheiten verschmälert, Schriftgröße von 26 auf 23 gesetzt, Lücke von 16 auf 10 verringert.
**Beleg:** `screenshots\A03_meine_360x800_kein_horizontales_scrollen.jpg`

### T-33 — Tischauswahl zeigt nur freie Tische, ohne Big Table; Gegenprobe gegen SharePoint (A12, A13)
**Datum:** 06.10.2026, ca. 16:15–16:20 Uhr
**Schritte:** Vorschau, Tab „Buchen", Datum heute, 16:00 bis 17:00 (Vorbelegung). Tischauswahl geöffnet. Zusätzlich ein temporäres Label mit derselben Rechnung wie `ddTisch.Items`, das die freien Tische, die überlappenden Buchungen und die Big-Table-Zeilen ausgibt. Danach SharePoint unabhängig per REST gelesen.
**Erwartung:** frei = alle 34 Tische minus die im Zeitraum belegten minus Big Table.
**Ergebnis App:** FREI = 30 Tische (OG Desk 2–7, 9–13; UG Desk 1–17; Quiet Desk 2, 3). BELEGT = OG Desk 1 (14:30–19:30), OG Desk 8 (15:30–20:30), Quiet Desk 1 (16:00–20:00). BIG = „Big Table".
**Ergebnis SharePoint** (`$filter=Startzeit lt 17:00 und Endzeit gt 16:00` in UTC): genau **3 Zeilen**, ID 482 OG Desk 1, ID 483 OG Desk 8, ID 494 Quiet Desk 1 — identisch.
**Rechnung:** 34 − 3 − 1 = 30 ✓. Die Auswahl ist nach Geschoss, Tischart und Nummer sortiert (OG Desk 2, 3, 4 … statt 1, 10, 11 …). Die Zusammenfassung zeigt „OG Desk 2 / Dienstag, 06.10.2026 / 16:00 bis 17:00 Uhr".
**Ergebnis: bestanden.**
**Belege:** `screenshots\A12_debug_frei_belegt_heute_1600_1700.png`, `screenshots\A12_tischauswahl_sortiert.png`, `screenshots\A12_A13_buchen_390_zusammenfassung.png`
**Nebenbefund:** `Tische` hat **34 Zeilen** (BELEGT; vorher in `APP_WISSEN.md` als UNSICHER geführt).

### Nachlese-Methode für alle Schreibtests (P4)
SharePoint wird **unabhängig von der App** gelesen: im Browser ein reiner GET auf
`https://technoformgroup.sharepoint.com/sites/IMSKonzept/_api/web/lists/getbytitle('Tischbuchungen')/items?$select=ID,Startzeit,Endzeit,Checkedin,Tisch/Title,Person/EMail&$expand=Tisch,Person&$filter=…`
mit `Accept: application/json;odata=nometadata`. Das ist eine Leseabfrage mit Josias' Sitzung, sie ändert nichts. Fremde E-Mail-Adressen gebe ich dabei nicht aus, nur „eigene ja/nein".

### T-04 / T-05 — Buchung anlegen, Nachlese, Anzeige (A14, A25/D6)
**Datum:** 06.10.2026, 16:27 Uhr. **Testbuchung:** TB-1.
**Schritte:** Buchen → Samstag, 31.10.2026 → 08:00 bis 12:00 → UG Desk 17 → einmal „Jetzt buchen".
**Erwartung:** eine Zeile mit richtigem Tisch-Nachschlagewert, richtiger Zeit und Josias als Person; Anzeige in „Meine".
**Ergebnis App:** Lade-Overlay, dann „Gebucht: UG Desk 17, 31.10., 08:00 bis 12:00 Uhr", automatischer Wechsel zu „Meine"; dort am Ende „UG Desk 17 / Samstag, 31.10.2026 / 08:00 bis 12:00".
**Ergebnis SharePoint (REST, unabhängig):** ID 496, `Tisch = {Id: 30, Title: "UG Desk 17"}`, in `Tische` ist ID 30 = „UG Desk 17"; `Startzeit 2026-10-31T07:00:00Z` (= 08:00 MEZ), Ende 12:00, `Person` = Josias Assefaw, `Author` = Josias, `Checkedin` = false, `SerienID` leer.
**Ergebnis: bestanden** (Teil Desktop-App steht noch aus).
**Belege:** `screenshots\A14_TB1_vor_dem_buchen_UG17_31-10_0800-1200.png`, `A29_TB1_ladeoverlay_waehrend_buchen.jpg`, `A14_TB1_gebucht_meldung_und_wechsel_zu_meine.jpg`

### T-17 — Eigene Überschneidung an anderem Tisch (A24, D5)
**Datum:** 06.10.2026, 16:28 Uhr. **Voraussetzung:** TB-1 (UG Desk 17, 08–12).
**Schritte:** 31.10. 10:00 bis 14:00, UG Desk 16, „Jetzt buchen". UG Desk 17 fehlte dabei in der Auswahl (belegt) — zusätzlicher Beleg für A12.
**Erwartung:** abgelehnt, keine Zeile.
**Ergebnis:** Meldung „Du hast in dieser Zeit schon einen Tisch gebucht.", Overlay verschwunden, Knopf wieder aktiv. REST 16:28:56: am Wochenende weiterhin nur ID 496, höchste ID 496.
**Ergebnis: bestanden.** **Belege:** `screenshots\A12_A24_UG17_fehlt_in_auswahl_10-14.png`, `A24_D5_abgelehnt_eigene_ueberschneidung.jpg`

### T-15 — Doppeltipp auf „Jetzt buchen" (A22, D3)
**Datum:** 06.10.2026, 16:29 Uhr. **Testbuchung:** TB-2.
**Schritte:** 31.10. 14:00 bis 15:00, UG Desk 15, Doppelklick plus ein dritter Klick auf „Jetzt buchen".
**Ergebnis SharePoint:** **genau eine** Zeile, ID 497. Für das Kriterium „genau eine Buchung" bestanden.
**Aber:** Auf dem Bildschirm folgte nach „Gebucht" noch „Der Tisch ist in dieser Zeit schon belegt" — ein eingereihter Zweit-Tipp lief nach dem ersten. Siehe T-34 und `ENTSCHEIDUNGEN.md` E-07. **Nach der Korrektur wird T-15 mit einer neuen Testbuchung wiederholt.**
**Beleg:** `screenshots\A22_TB2_doppeltipp_buchen_zweiter_lauf_meldet_belegt.jpg`

### T-34 — Doppeltipp auf „+1 Std" (D3, A17) — Fehler gefunden und behoben
**Vorher (16:31):** TB-2 14:00–15:00, Doppelklick auf „+1 Std" → App und REST: **14:00–17:00**. **Fehlgeschlagen**, zweimal verlängert. Beleg `screenshots\D3_FEHLER_doppeltipp_plus1_verlaengert_doppelt_14-17.jpg`
**Korrektur:** E-07 (Sperre `varIsLoading` + `varSperreBis` in allen sechs Schreib-Handlern).
**Nachher (16:37):** TB-2 14:00–17:00, Doppelklick auf „+1 Std" → App „Buchung verlängert.", REST: **14:00–18:00**. **Bestanden**, genau einmal verlängert. Zugleich Beleg für A17 „+1 Std mit Nachlese". Beleg `screenshots\D3_KORRIGIERT_doppeltipp_plus1_genau_einmal_14-18.jpg`

### T-35 — Verlängern +2, Grenze 22:00 (A17, V5)
**Datum:** 06.10.2026, 16:39–16:42. **Testbuchung:** TB-2 (497).
- +2 Std von 14–18 → 14–20 („Buchung verlängert.")
- +2 Std von 14–20 → **14–22** (genau 22:00 ist erlaubt), REST 16:40:51: `497 … 14:00–22:00`
- +1 Std von 14–22 → **„Eine Buchung kann nicht nach 22:00 Uhr enden."**, Overlay verschwunden, Dialog bleibt offen.
**Ergebnis: bestanden.** **Belege:** `screenshots\A17_A29_plus2_erster_tipp_sofort_ladeoverlay.jpg`, `A17_TB2_plus2_bis_2200_erlaubt.jpg`
**Zusatz D3 (Gegenprobe zu T-34):** TB-1 08–12, Dialog geöffnet, 3 s gewartet, Doppelklick „+1 Std": Overlay nach 1 s sichtbar (erster Tipp registriert), Ergebnis **08–13**, REST bestätigt. Damit ist belegt, dass die Sperre den zweiten Tipp abfängt und nicht etwa der erste verloren ging. **Belege:** `D3_TB1_doppeltipp_erster_tipp_registriert.jpg`, `D3_TB1_doppeltipp_plus1_genau_einmal_08-13.jpg`
**Beobachtung Vorschau:** Zweimal ging der **erste** Tipp nach dem Öffnen eines Dialogs verloren (kein Overlay, keine Meldung, der zweite Tipp wirkte). Beide Male lag davor ein Klick außerhalb der Vorschau (Studio-Meldung schließen). **VERMUTUNG:** Fokuswechsel zwischen Studio und Vorschau-Rahmen; auf dem Handy nicht zu erwarten. Wird bei J1 beobachtet.

### T-14 — Zwei Fenster, derselbe Tisch (A21, D2)
**Datum:** 06.10.2026, 16:50–16:57.
1. Fenster A (Handy-App, Studio-Vorschau): 31.10., 09:00–10:00, UG Desk 13 ausgewählt, **nicht** gebucht. Beleg `A21_fenster_A_handy_UG13_ausgewaehlt_noch_nicht_gebucht.png`
2. Fenster B (**Desktop-App**, Wiedergabe-Modus, keine Bearbeitung): UG Desk 13, 31.10., 09:00–10:00 gebucht → „Buchung(en) erfolgreich gespeichert". REST 16:56:07: **ID 498** (TB-4). Belege `A21_fenster_B_desktop_UG13_0900-1000.png`, `A21_fenster_B_desktop_gespeichert_ID498.jpg`
3. Fenster A: „Jetzt buchen" mit der veralteten Auswahl → **„Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch wählen."**, Overlay weg, die Auswahl hat sich selbst aktualisiert (UG Desk 13 verschwunden). REST 16:56:38: weiterhin genau 496, 497, 498; höchste ID 498 — **keine zweite Buchung**. Beleg `A21_fenster_A_handy_abgelehnt_tisch_belegt.jpg`
**Ergebnis: bestanden.** Zugleich A29-Pfad „Kollision".
**Nebenbeleg A14 (Desktop):** Die Desktop-App zeigte am 31.10. die beiden Handy-Buchungen „UG Desk 17 08:00–13:00" und „UG Desk 15 14:00–22:00" in „My personal desk" und als belegt (orange, „JA") im Grundriss UG. Beleg `A14_desktop_app_zeigt_handy_buchungen_496_497.jpg`. Umgekehrt zeigte „Meine" in der Handy-App die in der Desktop-App angelegte 498. Beleg `A14_handy_meine_zeigt_desktop_buchung_498.jpg`

### T-22 / T-23 — Buchung wurde inzwischen anderswo gelöscht (A19, A29, A30)
**Datum:** 06.10.2026, 16:57–16:59.
1. Handy: Verwalten-Dialog für TB-4 (UG Desk 13, 498) geöffnet und offen gelassen.
2. Desktop-App: TB-4 über deren Verwalten → „Stornieren" gelöscht. REST 16:57:36: 498 weg (nur noch 496, 497). Beleg `T22_desktop_storniert_TB4_waehrend_handy_dialog_offen.jpg`
3. Handy „+1 Std" → **„Diese Buchung gibt es nicht mehr. Bitte aktualisieren."**, Overlay weg. **Mangel (kosmetisch):** Der Dialog blieb offen und leer (Tischname fehlt, nur „bis"). Beleg `T22_A29_verlaengern_geloeschte_buchung_meldung_dialog_leer.jpg`. **Korrektur vorbereitet** in `yaml\dialoge.yaml`: in diesem Fall schließt der Dialog jetzt und die Meldung lautet „… Die Liste wird aktualisiert." (gilt für +1, +2 und Jetzt beenden). Wird mit dem nächsten Einfügen übernommen.
4. Handy „Stornieren" → „Ja, stornieren" → **„Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."**, beide Dialoge geschlossen, Liste ohne UG Desk 13, keine englische Fehlermeldung. Beleg `T23_A19_A30_stornieren_geloeschte_buchung_deutsche_meldung.jpg`
**Ergebnis: bestanden** (mit dem kosmetischen Mangel in Schritt 3, behoben im Quelltext).

---

## Delegationswarnungen (P2, laufende Liste)

**Stand 06.10.2026, 16:20 Uhr (nach dem Bau von „Buchen"): Formeln ohne Befund, keine Delegationswarnung.** Leistung meldet drei Hinweise, alle bewertet:

| Ort | Hinweis (Studio) | Bewertung |
|---|---|---|
| `App.OnStart` `ClearCollect(colTische; Tische)` | „Die aus der Datenquelle abgerufenen Zeilen sind möglicherweise nicht vollständig" | **unkritisch:** `Tische` hat 34 Zeilen, das Limit ist 1000. Die Sammlung ist nötig, weil `Filter(Tische, … in …)` nicht delegierbar wäre. |
| `App.OnStart` `colTische` | „Die Sammlung wird initialisiert, aber nie aktualisiert" (Vorschlag: benannte Formel) | **unkritisch:** Tische ändern sich praktisch nie; ein Neustart der App lädt sie neu. |
| `btnBuchen.OnSelect` `colKollision` | wie oben | **gewollt:** `colKollision` ist eine Momentaufnahme genau zum Zeitpunkt der Nachlese. Eine benannte Formel würde sich selbstständig neu berechnen und wäre als Nachlese wertlos. |

**Unterwegs gefunden und behoben (6 Warnungen beim ersten Einfügen):** siehe `FORTSCHRITT.md`, Eintrag „Bereich Buchen".

### Ältere Stände

Stand 06.10.2026, 15:28 Uhr. Beleg: `screenshots\A05_app_pruefung_leistung_4_unbenutzte_variablen.jpg`

**Es gibt keine Delegationswarnung.** Die App-Prüfung meldet unter „Leistung" vier Hinweise, alle vom selben Typ:

| Steuerelement.Property | Warnung | Bewertung | Status |
|---|---|---|---|
| `App.OnStart` (`varBuchung`) | Nicht verwendete Variable | unkritisch: wird geschrieben, aber noch nicht gelesen, weil der Verwalten-Dialog fehlt | löst sich mit dem nächsten Bauschritt |
| `App.OnStart` (`varBuchungID`) | Nicht verwendete Variable | wie oben | wie oben |
| `App.OnStart` (`varZeigeVerwalten`) | Nicht verwendete Variable | wie oben | wie oben |
| `App.OnStart` (`varZeigeStorno`) | Nicht verwendete Variable | wie oben | wie oben |

**Beobachtung, noch nicht erklärt:** `galMeine.Items` benutzt dieselbe Filterlogik wie `galAlleTischbuchungen` in der Desktop-App (`Person.Email = User().Email && Endzeit >= Now()`, umschlossen von `SortByColumns`). In der Desktop-App zeigt Studio dort ein Delegationsdreieck (offene Frage 7 des Briefings), in der Handy-App **nicht**. Mögliche Ursache: die zusätzliche `With`-Hülle oder eine neuere Studio-Version. Wird weiter beobachtet; falls die Warnung später auftaucht, kommt sie hier in die Liste.

---

## Vorab geplante Testfälle

Diese Liste wächst mit dem Bau. Sie bildet die Abnahmekriterien A01–A33 ab.

### Lesen
- **T-01** „Meine Buchungen" zeigt dieselben Zeilen wie die Desktop-App für denselben Nutzer (A16) — **ausgeführt, bestanden**
- **T-02** „Heute" zeigt nur heutige, noch nicht beendete eigene Buchungen, nach Startzeit sortiert (A08)
- **T-03** Leerzustand: kein Eintrag heute → Hinweis plus Weg zum Buchen (A11)

### Schreiben
- **T-04** Buchung anlegen, Nachlese: `Person`, `Tisch`, `Startzeit`, `Endzeit` stehen korrekt in SharePoint (A14, D6)
- **T-05** Dieselbe Buchung erscheint danach in „Heute", in „Meine" und in der Desktop-App (A14)
- **T-06** Einchecken setzt `Checkedin` auf wahr, Nachlese (A10)
- **T-07** Zweiter Tipp auf Einchecken checkt **nicht** aus (A10, V3)
- **T-08** Einchecken außerhalb des Zeitfensters ist nicht möglich (A10, V2)
- **T-09** Verlängern +1 Std, Nachlese der neuen Endzeit (A17)
- **T-10** Verlängern über 22:00 wird abgelehnt (A17, V5)
- **T-11** „Jetzt beenden" setzt die Endzeit, Tisch danach wieder in der Auswahl frei (A18)
- **T-12** Stornieren mit Bestätigung, Nachlese: Zeile weg (A19)

### Doppelbuchungen
- **T-13** D1: Die Kollisionsabfrage enthält eine Zeitgrenze im Filter (A20, Code-Beleg)
- **T-14** D2: Tisch am Handy wählen, in einem zweiten Fenster denselben Tisch im selben Zeitraum buchen, dann am Handy buchen → abgelehnt, keine zweite Zeile (A21)
- **T-15** D3: Doppeltipp auf Buchen → genau eine Zeile in SharePoint (A22)
- **T-16** D4: Der Verwalten-Dialog prüft denselben Datensatz, den er anzeigt (A23, Code-Beleg)
- **T-17** D5: eigene Buchung 08–12 an Tisch A, dann 10–14 an Tisch B → abgelehnt (A24)
- **T-18** D7: zwei gleichzeitige Buchungen desselben Tisches, Verhalten dokumentiert und ehrlich bewertet (A26)
- **T-19** D8: Jede Erfolgsmeldung stammt aus einer Nachlese (A27, Code-Beleg)

### Fehlerpfade und Robustheit
- **T-20** Lade-Overlay verschwindet nach einer abgelehnten Kollision (A29)
- **T-21** Lade-Overlay verschwindet nach einem Schreibfehler (A29)
- **T-22** Lade-Overlay verschwindet, wenn der Datensatz inzwischen gelöscht wurde (A29)
- **T-23** Stornieren einer bereits anderswo gelöschten Buchung → verständliche deutsche Meldung, kein Netzwerkfehler (A19, A30)
- **T-24** Ungültige Eingaben: Ende ≤ Start, Vergangenheit, nach 22:00 (A15)

### Darstellung
- **T-25** Geräteemulation 390 × 844: kein horizontales Scrollen (A03) — **ausgeführt, bestanden**
- **T-26** Geräteemulation 360 × 800: kein horizontales Scrollen (A03) — **ausgeführt, bestanden**
- **T-27** Tabwechsel schließt offene Dialoge (A07)
- **T-28** Aktualisieren im Header lädt neu und meldet es (A06)

### Vergleichstests gegen die Desktop-App
- **T-29** A09: Dieselbe Buchung, derselbe Zeitpunkt — Check-in-Zustand stimmt in beiden Apps überein, und das Einchecken-Zeitfenster hat dieselben Grenzen wie das Relevanzfenster des Grundrisses (Auslegung siehe `ENTSCHEIDUNGEN.md` E-A09)
- **T-30** Eine am Handy angelegte Buchung erscheint im Grundriss der Desktop-App mit der richtigen Farbe

### Abschluss
- **T-31** A31: Alle Testbuchungen aus `TESTDATEN.md` sind gelöscht, Nachlese
- **T-32** A02: Versionsliste der produktiven App enthält keine Version aus meinem Arbeitszeitraum
