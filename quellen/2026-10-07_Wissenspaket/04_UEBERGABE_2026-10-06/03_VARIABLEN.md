# 03 — Variablen, Collections, Named Formulas

**Kurzfassung:** Die App hat 50 globale Variablen (`Set`), 5 Collections und 20 Named Formulas. **Kontextvariablen gibt es nicht** (kein `UpdateContext`, kein `Navigate` mit Kontext — die App hat nur einen Screen). 10 Variablen werden geschrieben, aber nie gelesen. Die Fundstellen stammen per Skript aus dem Quellcode (`skripte/analyse.js`); „geschrieben" heißt `Set`/`Collect`/`ClearCollect`/`Clear`/`Remove`, „gelesen" heißt Vorkommen in einer anderen Formel. Besonderheiten stehen je Eintrag unter „Hinweis".

## Auf einen Blick

**Geschrieben, aber nie gelesen (10):** `varMehrfachAuswahlModus`, `varPanX`, `varPanY`, `varSpinnerWinkel`, `varStockwerkDropdownOffen`, `varWiederholenBis`, `varWiederholenBisGewaehlt`, `varZeigeRaumInfo`, `varZeigeRaumVerwalten`, `varZeigeVerlaengern`. Die App-Prüfung meldet davon zehn als `app-UnusedVariables` (`AppCheckerResult.sarif`).

**Gelesen, aber nie geschrieben:** keine. Jeder gelesene `var…`/`col…`-Name wird irgendwo geschrieben (geprüft per Skript über alle Formeln).

**Zwei Variablen für denselben Zweck:** `varMehrfachAuswahlModus` (tot) und `varAuswahlModusAktiv` (wirksam).

**Dieselbe Variable von zwei Dialogen:** `varSelectedBuchung` bedient den Grundriss-Dialog **und** die Dauer-Knöpfe des Buchungen-Tabs, obwohl dieser Dialog `varSelectedBuchungTab` führt (Befund B0).

**Mit zwei verschiedenen Record-Typen befüllt:** keine gefunden. `varSelectedBuchung`, `varSelectedBuchungTab` und `varGeklickteBuchungKlein` tragen stets Datensätze aus `Tischbuchungen` (`ThisItem` zweier Galerien, `LookUp`-Ergebnis, `Patch`-Rückgabe, `Blank()`). `varSelectedTisch` und `varAusgewähltRaum` tragen Datensätze aus `Tische` bzw. `Räume`. **UNSICHER** bleibt `varAusgewaehltePlusDauer`: Zahl (`60`, `-120`), `Blank()` und an einer Stelle `0` — alle numerisch, aber `0` hat eine andere Bedeutung als `Blank()`.

**Nicht in `App.OnStart` initialisiert:** `varZeigeTischBuchungForm`, `varDetailsTisch`.

## Globale Variablen (50)

### varAktiverTab

- **Art:** globale Variable (`Set`)
- **Geschrieben in (4):** `App.OnStart`, `btnSpeichernTischePanel.OnSelect`, `btnTabDashboard.OnSelect`, `btnTabBuchungen.OnSelect`
- **Gelesen in (2):** `conDashboard.Visible`, `conBuchungen.Visible`

### varAnsichtsDatum

- **Art:** globale Variable (`Set`)
- **Geschrieben in (2):** `App.OnStart`, `dpAnsichtsDatum.OnChange`
- **Gelesen in (9):** `Rectangle1.Fill`, `Circle1.BorderStyle`, `Circle1.Fill`, `Label1.Text`, `btnHitArea.OnSelect`, `galTischbuchungenHeute.Items`, `Label16.Text`, `dpDatumTischePanel.DefaultDate`, `dpDatum.DefaultDate`

### varAusgewaehltePanelDauer

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btn5Std.OnSelect`, `btn9Std.OnSelect`
- **Gelesen in (4):** `btn5Std.Fill`, `btn5Std.OnSelect`, `btn9Std.Fill`, `btn9Std.OnSelect`

### varAusgewaehltePlusDauer

- **Art:** globale Variable (`Set`)
- **Geschrieben in (14):** `App.OnStart`, `ddStockwerk.OnSelect`, `btnVerwalten.OnSelect`, `btnVerlängern.OnSelect`, `btnPlus1Std.OnSelect`, `btnPlus2Std.OnSelect`, `btnPlus3Std.OnSelect`, `btnVerlängern_1.OnSelect`, `btnPlus1Std_1.OnSelect`, `btnPlus2Std_1.OnSelect`, `btnPlus3Std_1.OnSelect`, `btnMinus1Std.OnSelect`, `btnMinus2Std.OnSelect`, `btnMinus3std.OnSelect`
- **Gelesen in (20):** `btnVerlängern.OnSelect`, `btnPlus1Std.Fill`, `btnPlus1Std.OnSelect`, `btnPlus2Std.Fill`, `btnPlus2Std.OnSelect`, `btnPlus3Std.Fill`, `btnPlus3Std.OnSelect`, `btnVerlängern_1.OnSelect`, `btnPlus1Std_1.Fill`, `btnPlus1Std_1.OnSelect`, `btnPlus2Std_1.Fill`, `btnPlus2Std_1.OnSelect`, `btnPlus3Std_1.Fill`, `btnPlus3Std_1.OnSelect`, `btnMinus1Std.Fill`, `btnMinus1Std.OnSelect`, `btnMinus2Std.Fill`, `btnMinus2Std.OnSelect`, `btnMinus3std.Fill`, `btnMinus3std.OnSelect`
- **Hinweis:** Wird an einer Stelle mit `0` belegt (`ddStockwerk.OnSelect`), überall sonst mit `Blank()` oder einer Minutenzahl. Die Prüfung `IsBlank(varAusgewaehltePlusDauer)` in den Verlängern-Knöpfen greift bei `0` nicht.

### varAusgewaehltesStockwerk

- **Art:** globale Variable (`Set`)
- **Geschrieben in (2):** `App.OnStart`, `ddStockwerk.OnChange`
- **Gelesen in (13):** `imgGrundrissOG.Visible`, `imgGrundrissUG.Visible`, `Gallery1.Items`, `Rectangle1.Height`, `Rectangle1.Width`, `Rectangle1.X`, `Rectangle1.Y`, `Circle1.Height`, `Circle1.Width`, `Label1.Size`, `Label18.Text`, `conDetailsPopup.X`, `conDetailsPopup.Y`

### varAusgewählteEndzeit

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnSlot1.OnSelect`, `btnSlot2.OnSelect`, `btnSlot3.OnSelect`, `btnSlot4.OnSelect`
- **Gelesen in (11):** `Label10.Text`, `btnSpeichernRaumPanel.OnSelect`, `recNeueBuchung.Width`, `recNeueBuchung.X`, `recBuchungDavor1.Width`, `recBuchungDavor1.X`, `recBuchungDanach1.Visible`, `recBuchungDanach1.Width`, `recBuchungDanach1.X`, `Label4.Text`, `Label13.Text`

### varAusgewählteStartzeit

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnSlot1.OnSelect`, `btnSlot2.OnSelect`, `btnSlot3.OnSelect`, `btnSlot4.OnSelect`
- **Gelesen in (12):** `Label10.Text`, `btnSpeichernRaumPanel.OnSelect`, `recNeueBuchung.Width`, `recNeueBuchung.X`, `recBuchungDavor1.Visible`, `recBuchungDavor1.Width`, `recBuchungDavor1.X`, `recBuchungDanach1.Width`, `recBuchungDanach1.X`, `Label4.Text`, `Label5.Text`, `Label13.Text`

### varAusgewähltRaum

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnSlot1.OnSelect`, `btnSlot2.OnSelect`, `btnSlot3.OnSelect`, `btnSlot4.OnSelect`
- **Gelesen in (10):** `Label9.Text`, `btnSpeichernRaumPanel.OnSelect`, `recBuchungDavor1.Visible`, `recBuchungDavor1.Width`, `recBuchungDavor1.X`, `recBuchungDanach1.Visible`, `recBuchungDanach1.Width`, `recBuchungDanach1.X`, `Label4.Text`, `Label5.Text`

### varAuswahlModusAktiv

- **Art:** globale Variable (`Set`)
- **Geschrieben in (4):** `App.OnStart`, `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`, `tglAuswahlModus.OnChange`
- **Gelesen in (3):** `btnVerwalten_2.OnSelect`, `chkAuswahl.Visible`, `chkAlleAuswählen.Visible`
- **Hinweis:** Die wirksame Variable für den Auswahlmodus (siehe `varMehrfachAuswahlModus`).

### varDetailsTisch

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `btnHitArea.OnSelect`
- **Gelesen in (2):** `conDetailsPopup.X`, `conDetailsPopup.Y`
- **Hinweis:** Wird in `App.OnStart` **nicht** initialisiert und nur in `btnHitArea.OnSelect` geschrieben.

### varEndeOverride

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (1):** `ddEnde.Default`
- **Hinweis:** Wie `varStartOverride`: nur in `App.OnStart` gesetzt, Zweig in `ddEnde.Default` unerreichbar.

### varEndeOverridePanel

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btn5Std.OnSelect`, `btn9Std.OnSelect`
- **Gelesen in (1):** `ddEndTischePanel.Default`

### varGalleryNeuAufbauen

- **Art:** globale Variable (`Set`)
- **Geschrieben in (2):** `App.OnStart`, `tglAuswahlModus.OnChange`
- **Gelesen in (2):** `galAlleTischbuchungen.Items`, `tglAuswahlModus.OnChange`
- **Hinweis:** Zähler, der nur dazu dient, `galAlleTischbuchungen.Items` zum Neurechnen zu zwingen (`With({erzwingeNeuaufbau: varGalleryNeuAufbauen}, …)`).

### varGeklickteBuchungKlein

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnVerwalten_2.OnSelect`, `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`, `tglAuswahlModus.OnChange`
- **Gelesen in (3):** `lblVerwaltenKleinDatum.Text`, `lblVerwaltenKleinZeit.Text`, `lblVerwaltenKleinTitel.Text`

### varIsLoading

- **Art:** globale Variable (`Set`)
- **Geschrieben in (9):** `App.OnStart`, `Icon1_1.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `btnStornieren_1.OnSelect`, `btnStornierenKlein.OnSelect`, `Icon1.OnSelect`, `Image6.OnSelect`, `btnHitArea_1.OnSelect`
- **Gelesen in (1):** `conLadeOverlay.Visible`

### varMehrfachAuswahlModus

- **Art:** globale Variable (`Set`)
- **Geschrieben in (2):** `App.OnStart`, `btnVerlängern_1.OnSelect`
- **Gelesen in (0):** —
- **Hinweis:** Wird geschrieben, aber nirgends gelesen. Zusammen mit `varAuswahlModusAktiv` sind das **zwei Variablen für denselben Zweck**; nur `varAuswahlModusAktiv` wirkt. Offene Frage 6 des Briefings ist damit beantwortet: tot.

### varPanX

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen. Zusammen mit `varPanY` und `varZoom` Rest einer Zoom-/Verschiebe-Funktion; nur `varZoom` wirkt noch (in `Circle1.Height`/`Width`).

### varPanY

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen (siehe `varPanX`).

### varProfilFarbe

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (1):** `Circle2.Fill`

### varSelectedBuchung

- **Art:** globale Variable (`Set`)
- **Geschrieben in (7):** `App.OnStart`, `btnHitArea.OnSelect`, `ddStockwerk.OnSelect`, `btnEincheckenHeute.OnSelect`, `btnVerwalten.OnSelect`, `btnEinchecken.OnSelect`, `btnVerlängern.OnSelect`
- **Gelesen in (32):** `conCheckinDialog.Y`, `lblTitel.Text`, `lblZeit.Text`, `btnEinchecken.Fill`, `btnEinchecken.OnSelect`, `btnEinchecken.PressedColor`, `btnEinchecken.Text`, `lblTitel2.Text`, `lblZeit2.Text`, `lblPerson.Text`, `lblTitel3.Text`, `lblZeit3.Text`, `btnStornieren.OnSelect`, `btnVerlängern.OnSelect`, `btnPlus1Std.DisplayMode`, `btnPlus1Std.Fill`, `btnPlus2Std.DisplayMode`, `btnPlus2Std.Fill`, `btnPlus3Std.DisplayMode`, `btnPlus3Std.Fill`, `btnPlus1Std_1.DisplayMode`, `btnPlus1Std_1.Fill`, `btnPlus2Std_1.DisplayMode`, `btnPlus2Std_1.Fill`, `btnPlus3Std_1.DisplayMode`, `btnPlus3Std_1.Fill`, `btnMinus1Std.DisplayMode`, `btnMinus1Std.Fill`, `btnMinus2Std.DisplayMode`, `btnMinus2Std.Fill`, `btnMinus3std.DisplayMode`, `btnMinus3std.Fill`
- **Hinweis:** Wird von **zwei Dialogen** benutzt: dem Grundriss-/Dashboard-Dialog `conVerwaltenDialog` (richtig) und — über die zwölf Dauer-Knopf-Properties in `conVerwaltenDialog_1` — auch vom Buchungen-Tab, der eigentlich `varSelectedBuchungTab` führt. Das ist Befund B0 (siehe `02_BUTTONS.md`, `btnPlus1Std_1`).

### varSelectedBuchungTab

- **Art:** globale Variable (`Set`)
- **Geschrieben in (3):** `App.OnStart`, `btnVerwalten_2.OnSelect`, `btnVerlängern_1.OnSelect`
- **Gelesen in (5):** `lblTitel3_1.Text`, `lblZeit3_1.Text`, `lblVerwaltenTag.Text`, `btnStornieren_1.OnSelect`, `btnVerlängern_1.OnSelect`
- **Hinweis:** Variable des Buchungen-Tab-Dialogs. Die Dauer-Knöpfe desselben Dialogs lesen aber `varSelectedBuchung` (Befund B0).

### varSelectedTisch

- **Art:** globale Variable (`Set`)
- **Geschrieben in (3):** `App.OnStart`, `btnHitArea.OnSelect`, `ddStockwerk.OnSelect`
- **Gelesen in (3):** `Label3.Text`, `Label2.Text`, `btnSpeichern.OnSelect`

### varSpinnerWinkel

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen. Es gibt keinen Timer in der App; der Spinner `imgSpinner` ist ein animiertes Bild.

### varStartOverride

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (1):** `ddStart.Default`
- **Hinweis:** Wird nur in `App.OnStart` auf `""` gesetzt und sonst nie geschrieben. `ddStart.Default` prüft `varStartOverride <> ""` — der Zweig ist unerreichbar (im Buchungsdialog gibt es keine Schnellwahl-Knöpfe).

### varStartOverridePanel

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btn5Std.OnSelect`, `btn9Std.OnSelect`
- **Gelesen in (1):** `ddStartTischePanel.Default`

### varStockwerkDropdownOffen

- **Art:** globale Variable (`Set`)
- **Geschrieben in (3):** `App.OnStart`, `ddStockwerk.OnChange`, `ddStockwerk.OnSelect`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen.

### varTagDi

- **Art:** globale Variable (`Set`)
- **Geschrieben in (8):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `tglTagDi_1.OnChange`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `tglTagDi.OnChange`
- **Gelesen in (3):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `tglTagDi.Default`

### varTagDo

- **Art:** globale Variable (`Set`)
- **Geschrieben in (8):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `tglTagDo_1.OnChange`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `tglTagDo.OnChange`
- **Gelesen in (3):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `tglTagDo.Default`

### varTagFr

- **Art:** globale Variable (`Set`)
- **Geschrieben in (8):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `tglTagFr_1.OnChange`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `tglTagFr.OnChange`
- **Gelesen in (3):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `tglTagFr.Default`

### varTagMi

- **Art:** globale Variable (`Set`)
- **Geschrieben in (8):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `tglTagMi_1.OnChange`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `tglTagMi.OnChange`
- **Gelesen in (3):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `tglTagMi.Default`

### varTagMo

- **Art:** globale Variable (`Set`)
- **Geschrieben in (8):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `tglTagMo_1.OnChange`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `tglTagMo.OnChange`
- **Gelesen in (3):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `tglTagMo.Default`

### varTagSa

- **Art:** globale Variable (`Set`)
- **Geschrieben in (6):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`
- **Gelesen in (2):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`

### varTagSo

- **Art:** globale Variable (`Set`)
- **Geschrieben in (6):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`
- **Gelesen in (2):** `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`

### varWiederholen

- **Art:** globale Variable (`Set`)
- **Geschrieben in (11):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btnAbbrechenTischePanel.OnSelect`, `chkWiederholenPanel.OnCheck`, `chkWiederholenPanel.OnUncheck`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `chkWiederholen.OnCheck`, `chkWiederholen.OnUncheck`
- **Gelesen in (21):** `btnSpeichernTischePanel.OnSelect`, `tglTagMo_1.Visible`, `tglTagDi_1.Visible`, `tglTagMi_1.Visible`, `tglTagDo_1.Visible`, `tglTagFr_1.Visible`, `dpWiederholenBis_1.OnChange`, `dpWiederholenBis_1.Visible`, `Label14.Visible`, `conBuchungDialog.Height`, `btnSpeichern.OnSelect`, `btnSpeichern.Y`, `btnAbbrechen.Y`, `chkWiederholen.Default`, `tglTagMo.Visible`, `tglTagDi.Visible`, `tglTagMi.Visible`, `tglTagDo.Visible`, `tglTagFr.Visible`, `dpWiederholenBis.Visible`, `Label15.Visible`

### varWiederholenBis

- **Art:** globale Variable (`Set`)
- **Geschrieben in (3):** `App.OnStart`, `dpWiederholenBis_1.OnSelect`, `dpWiederholenBis.OnSelect`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen. Beide Speichern-Knöpfe lesen stattdessen direkt `dpWiederholenBis.SelectedDate` bzw. `dpWiederholenBis_1.SelectedDate`.

### varWiederholenBisGewaehlt

- **Art:** globale Variable (`Set`)
- **Geschrieben in (2):** `App.OnStart`, `dpWiederholenBis.OnChange`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen.

### varWiederholenModus

- **Art:** globale Variable (`Set`)
- **Geschrieben in (6):** `App.OnStart`, `btnHitArea.OnSelect`, `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`
- **Gelesen in (12):** `btnSpeichernTischePanel.OnSelect`, `tglTagMo_1.Visible`, `tglTagDi_1.Visible`, `tglTagMi_1.Visible`, `tglTagDo_1.Visible`, `tglTagFr_1.Visible`, `btnSpeichern.OnSelect`, `tglTagMo.Visible`, `tglTagDi.Visible`, `tglTagMi.Visible`, `tglTagDo.Visible`, `tglTagFr.Visible`
- **Hinweis:** Wird nur auf `"Wochentage"` gesetzt, nie auf `"Taeglich"`. Der Zweig `varWiederholenModus = "Taeglich"` in beiden Speichern-Knöpfen ist unerreichbar.

### varZeigeCheckin

- **Art:** globale Variable (`Set`)
- **Geschrieben in (9):** `App.OnStart`, `btnHitArea.OnSelect`, `ddStockwerk.OnSelect`, `btnEincheckenHeute.OnSelect`, `btnVerwalten.OnSelect`, `btnEinchecken.OnSelect`, `btnSchließen2.OnSelect`, `btnVerwalten_2.OnSelect`, `btnTabBuchungen.OnSelect`
- **Gelesen in (1):** `conCheckinDialog.Visible`

### varZeigeDetails

- **Art:** globale Variable (`Set`)
- **Geschrieben in (8):** `App.OnStart`, `btnHitArea.OnSelect`, `ddStockwerk.OnSelect`, `btnEincheckenHeute.OnSelect`, `btnVerwalten.OnSelect`, `btnSchließen3.OnSelect`, `btnVerwalten_2.OnSelect`, `btnTabBuchungen.OnSelect`
- **Gelesen in (1):** `conDetailsPopup.Visible`

### varZeigeDialog

- **Art:** globale Variable (`Set`)
- **Geschrieben in (9):** `App.OnStart`, `btnHitArea.OnSelect`, `ddStockwerk.OnSelect`, `btnEincheckenHeute.OnSelect`, `btnVerwalten.OnSelect`, `btnSpeichern.OnSelect`, `btnAbbrechen.OnSelect`, `btnVerwalten_2.OnSelect`, `btnTabBuchungen.OnSelect`
- **Gelesen in (1):** `conBuchungDialog.Visible`

### varZeigeRaumBestätigung

- **Art:** globale Variable (`Set`)
- **Geschrieben in (7):** `App.OnStart`, `btnSlot1.OnSelect`, `btnSlot2.OnSelect`, `btnSlot3.OnSelect`, `btnSlot4.OnSelect`, `btnSpeichernRaumPanel.OnSelect`, `Button7.OnSelect`
- **Gelesen in (1):** `conRaumBestätigen.Visible`

### varZeigeRaumBuchungForm

- **Art:** globale Variable (`Set`)
- **Geschrieben in (4):** `App.OnStart`, `btnRaumHinzufügen.OnSelect`, `btnAbbrechenRaumPanel.OnSelect`, `btnSpeichernRaumPanel.OnSelect`
- **Gelesen in (2):** `conDashboard.Visible`, `conRaumBuchungenPanel.Visible`

### varZeigeRaumInfo

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen (toter Raumcode).

### varZeigeRaumVerwalten

- **Art:** globale Variable (`Set`)
- **Geschrieben in (2):** `App.OnStart`, `btnTabBuchungen.OnSelect`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen (toter Raumcode).

### varZeigeTischBuchungForm

- **Art:** globale Variable (`Set`)
- **Geschrieben in (3):** `btnTischHinzufügen.OnSelect`, `btnSpeichernTischePanel.OnSelect`, `btnAbbrechenTischePanel.OnSelect`
- **Gelesen in (2):** `conDashboard.Visible`, `conTischBuchungenPanel.Visible`
- **Hinweis:** Wird in `App.OnStart` **nicht** initialisiert (alle anderen `varZeige…` schon). Vor dem ersten Klick auf „Tisch Buchen" ist sie leer; `conTischBuchungenPanel.Visible` wertet das als `false`.

### varZeigeVerlaengern

- **Art:** globale Variable (`Set`)
- **Geschrieben in (3):** `App.OnStart`, `ddStockwerk.OnSelect`, `btnTabBuchungen.OnSelect`
- **Gelesen in (0):** —
- **Hinweis:** Geschrieben, nie gelesen.

### varZeigeVerwalten

- **Art:** globale Variable (`Set`)
- **Geschrieben in (9):** `App.OnStart`, `btnHitArea.OnSelect`, `ddStockwerk.OnSelect`, `btnEincheckenHeute.OnSelect`, `btnVerwalten.OnSelect`, `btnStornieren.OnSelect`, `btnVerlängern.OnSelect`, `btnSchließen4.OnSelect`, `btnTabBuchungen.OnSelect`
- **Gelesen in (1):** `conVerwaltenDialog.Visible`

### varZeigeVerwaltenKlein

- **Art:** globale Variable (`Set`)
- **Geschrieben in (5):** `App.OnStart`, `btnVerwalten_2.OnSelect`, `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`, `tglAuswahlModus.OnChange`
- **Gelesen in (1):** `conVerwaltenKlein.Visible`

### varZeigeVerwaltenTab

- **Art:** globale Variable (`Set`)
- **Geschrieben in (6):** `App.OnStart`, `btnVerwalten_2.OnSelect`, `btnStornieren_1.OnSelect`, `btnVerlängern_1.OnSelect`, `btnSchließen4_1.OnSelect`, `tglAuswahlModus.OnChange`
- **Gelesen in (1):** `conVerwaltenDialog_1.Visible`

### varZoom

- **Art:** globale Variable (`Set`)
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (2):** `Circle1.Height`, `Circle1.Width`

## Collections (5)

### colAusgewaehlteBuchungen

- **Art:** Collection
- **Geschrieben in (9):** `App.OnStart`, `chkAuswahl.OnCheck`, `chkAuswahl.OnUncheck`, `btnVerlängern_1.OnSelect`, `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`, `tglAuswahlModus.OnChange`, `chkAlleAuswählen.OnCheck`, `chkAlleAuswählen.OnUncheck`
- **Gelesen in (5):** `chkAuswahl.Default`, `chkAuswahl.OnUncheck`, `lblVerwaltenKleinTitel.Text`, `btnStornierenKlein.OnSelect`, `chkAlleAuswählen.Default`
- **Hinweis:** Die Auswahl der Mehrfachauswahl. Wird mit `ThisItem` aus `galAlleTischbuchungen` (Typ `Tischbuchungen`) und mit `galAlleTischbuchungen.AllItems` gefüllt; beide sind Datensätze derselben Liste. `Collect` in `chkAuswahl.OnCheck` prüft nicht auf Dubletten.

### colStornoFrisch

- **Art:** Collection
- **Geschrieben in (2):** `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`
- **Gelesen in (1):** `btnStornierenKlein.OnSelect`
- **Hinweis:** Hilfs-Collection von Entwurf A: frisch gelesene eigene künftige Buchungen. Wird in `btnStornierenKlein` und `btnSchließenKlein` geleert.

### colStornoZiele

- **Art:** Collection
- **Geschrieben in (2):** `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`
- **Gelesen in (1):** `btnStornierenKlein.OnSelect`
- **Hinweis:** Hilfs-Collection von Entwurf A: Schnittmenge aus `colStornoFrisch` und `colAusgewaehlteBuchungen`; die tatsächlich gelöschte Menge.

### colTischPositionen

- **Art:** Collection
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (6):** `Rectangle1.Height`, `Rectangle1.Width`, `Rectangle1.X`, `Rectangle1.Y`, `conDetailsPopup.X`, `conDetailsPopup.Y`
- **Hinweis:** Feste Koordinatentabelle der OG-Tische (16 Einträge, in `App.OnStart` einprogrammiert). Spalten: `Tisch`, `X`, `Y`, `Ausrichtung`. Nicht aus SharePoint, obwohl die Liste `Tische` die Spalten `X`, `Y` und `Ausrichtung` hat.

### colTischPositionenUG

- **Art:** Collection
- **Geschrieben in (1):** `App.OnStart`
- **Gelesen in (6):** `Rectangle1.Height`, `Rectangle1.Width`, `Rectangle1.X`, `Rectangle1.Y`, `conDetailsPopup.X`, `conDetailsPopup.Y`
- **Hinweis:** Feste Koordinatentabelle der UG-Tische (18 Einträge inkl. „Big Table"). Siehe `colTischPositionen`.

## Kontextvariablen

Keine. Im gesamten Quellcode kommt weder `UpdateContext` noch ein `Navigate` mit Kontextsatz vor (per Skript geprüft). Die App hat genau einen Screen (`Screen1`).

## Named Formulas (20)

Alle stehen in `App.Formulas`. Named Formulas werden bei Bedarf ausgewertet, nicht beim Start.

### BasisBreite

```powerfx
BasisBreite = 1920
```

- **Gelesen in (2):** `imgGrundrissOG.Width`, `imgGrundrissUG.Width` (zusätzlich innerhalb von `App.Formulas` selbst)

### BasisHoehe

```powerfx
BasisHoehe = 1080
```

- **Gelesen in (2):** `imgGrundrissOG.Height`, `imgGrundrissUG.Height` (zusätzlich innerhalb von `App.Formulas` selbst)

### BasisSkalierung

```powerfx
BasisSkalierung = Min(conGrundriss.Width / BasisBreite, conGrundriss.Height / BasisHoehe)
```

- **Gelesen in (13):** `imgGrundrissOG.Height`, `imgGrundrissOG.Width`, `imgGrundrissUG.Height`, `imgGrundrissUG.Width`, `Rectangle1.Height`, `Rectangle1.Width`, `Rectangle1.X`, `Rectangle1.Y`, `Circle1.Height`, `Circle1.Width`, `Label1.Size`, `conDetailsPopup.X`, `conDetailsPopup.Y`

### BasisKachelbreiteQuer

```powerfx
BasisKachelbreiteQuer = 101
```

- **Gelesen in (1):** `Rectangle1.Width`

### BasisKachelhoeheQuer

```powerfx
BasisKachelhoeheQuer = 60
```

- **Gelesen in (1):** `Rectangle1.Height`

### BasisKachelbreiteHoch

```powerfx
BasisKachelbreiteHoch = 60
```

- **Gelesen in (1):** `Rectangle1.Width`

### BasisKachelhoeheHoch

```powerfx
BasisKachelhoeheHoch = 101
```

- **Gelesen in (1):** `Rectangle1.Height`

### BasisKreisgroesse

```powerfx
BasisKreisgroesse = 39
```

- **Gelesen in (2):** `Circle1.Height`, `Circle1.Width`

### btnAbstand

```powerfx
btnAbstand = 6
```

- **Gelesen in (5):** `btnPlus1Std_1.X`, `btnPlus2Std_1.X`, `btnPlus3Std_1.X`, `btnMinus1Std.X`, `btnMinus2Std.X` (zusätzlich innerhalb von `App.Formulas` selbst)

### btnBreite

```powerfx
btnBreite = Min(80, Max(44, (conVerwaltenDialog_1.Width - 5*btnAbstand - 40) / 6))
```

- **Gelesen in (11):** `btnPlus1Std_1.Width`, `btnPlus1Std_1.X`, `btnPlus2Std_1.Width`, `btnPlus2Std_1.X`, `btnPlus3Std_1.Width`, `btnPlus3Std_1.X`, `btnMinus1Std.Width`, `btnMinus1Std.X`, `btnMinus2Std.Width`, `btnMinus2Std.X`, `btnMinus3std.Width`

### BasisKachelbreiteHochUG

```powerfx
BasisKachelbreiteHochUG = 52
```

- **Gelesen in (1):** `Rectangle1.Width`

### BasisKachelhoeheHochUG

```powerfx
BasisKachelhoeheHochUG = 89
```

- **Gelesen in (1):** `Rectangle1.Height`

### BasisKachelbreiteQuerUG

```powerfx
BasisKachelbreiteQuerUG = 89
```

- **Gelesen in (1):** `Rectangle1.Width`

### BasisKachelhoeheQuerUG

```powerfx
BasisKachelhoeheQuerUG = 52
```

- **Gelesen in (1):** `Rectangle1.Height`

### BasisKreisgroesseUG

```powerfx
BasisKreisgroesseUG = 34
```

- **Gelesen in (2):** `Circle1.Height`, `Circle1.Width`

### BasisSchriftgroesseUG

```powerfx
BasisSchriftgroesseUG = 12
```

- **Gelesen in (1):** `Label1.Size`

### BasisKachelbreiteBigTableUG

```powerfx
// Josias 2026-09-28: eigene Breite fuer Big Table UG, deutlich breiter als Standardtisch, Hoehe bleibt Basishoehe horizontal
BasisKachelbreiteBigTableUG = 220
```

- **Gelesen in (1):** `Rectangle1.Width`

### TischNrOG

```powerfx
// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
TischNrOG = With({src: Filter(Tische, Geschoss.Value = "OG")}, ForAll(Sequence(CountRows(src)), {Titel: Index(src, Value).Titel, Nr: Value}))
```

- **Gelesen in (1):** `Rectangle1.Y`

### TischNrUG

```powerfx
TischNrUG = With({src: Filter(Tische, Geschoss.Value = "UG")}, ForAll(Sequence(CountRows(src)), {Titel: Index(src, Value).Titel, Nr: Value}))
```

- **Gelesen in (1):** `Rectangle1.Y`

### BasisSkalierungReferenz

```powerfx
// Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
BasisSkalierungReferenz = Min(881 / BasisBreite, 678 / BasisHoehe)
```

- **Gelesen in (1):** `Rectangle1.Y`
