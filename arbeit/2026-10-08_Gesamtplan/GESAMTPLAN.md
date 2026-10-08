# GESAMTPLAN Tischbuchung: alle Änderungen Schritt für Schritt
**Stand 08.10.2026 · Basis: veröffentlichter Export vom 07.10. (enthält L2) · ersetzt das Einfügen von Paket K v2 und Paket L einzeln: Jede Property steht hier genau einmal in ihrer Endfassung · maschinell erzeugt und geprüft (`werkzeuge/gesamtplan.py`, Anhang B) · Go-Live 14.10.2026, harter Umstieg (GoBright-Vertrag endet)**

Kennzeichnung: **belegt** (im Export nachgesehen) · **gemessen** (Monitor/Test) · **geschlussfolgert** · **UNSICHER** (mit Test).

## 0. Kurzfassung
- **Was das ist:** ein fertiger Plan zum Abarbeiten, Schritt für Schritt. Jeder Schritt sagt, welches Problem er löst, wie, was genau einzufügen ist (vollständige Formel, deutsche Schreibweise) und wie du testest. Du arbeitest ihn mit einem anderen Chat durch, der Startprompt steht in `START_PROMPT_fuer_Chat.md`.
- **Umfang:** 26 App-Schritte (253 Properties, 7 neue Steuerelemente), dazu Vorbereitung in SharePoint, ein Power-Automate-Flow, die Rechte, 2 Properties in der Handy-App, Test mit Kollegen und Go-Live-Checkliste.
- **Reihenfolge = Wichtigkeit.** Phase 1 (Schritte G1–G7) ist das Fundament gegen Doppelbuchungen, falsche Tage und rohe Fehler. **Ohne Phase 1 nicht live gehen.** Danach Freigabe-Flow und Timer (Phase 2), Tischauswahl (Phase 3), Grundriss-Erweiterungen (Phase 4), Optik (Phase 5), Raumcode ruhig (Phase 6), Barrierefreiheit (Phase 7), Handy-App (Phase 8), Test und Go-Live (Phase 9).
- **Zeitbedarf (Einschätzung):** Phase 0–2 ein Tag, Phase 3–5 ein Tag, Phase 6–9 ein Tag, plus Kollegentest. Das passt in deine 3–4 Tage, wenn nichts Größeres schiefgeht. Wenn es knapp wird: Phase 5 und 7 nach dem Go-Live.
- **Deine Entscheidungen aus dem Interview** sind eingebaut: harter Umstieg, automatische Freigabe nach 30 Min (nur löschen), Start ab 06:00, Serien Mo–Fr, Namen sichtbar, Raumcode bleibt (wird nur ruhiggestellt), Liste „nur eigene Elemente bearbeiten“, Tische sperren nur durch dich, Big Table für alle über den Grundriss.
- **Was ich für dich entschieden habe** (du hattest „wie du es für sinnvoll hältst“ gesagt), steht in Abschnitt 2.
- **Ehrlich:** Nichts davon ist in Studio getestet. Alles ist aus dem Export erzeugt und maschinell geprüft. Paket K v2 und L wurden je zweimal unabhängig geprüft, die Ergänzungen aus dem Interview (06:00, Gesperrt, Storno-Bestätigung, Timer, „Andere Zeit buchen“, Raumcode ruhig, Barrierefreiheit, Handy) noch **nicht**. Die offenen Laufzeitfragen stehen im Abschnitt UNSICHER.

## 1. So arbeitest du den Plan ab
1. **Ein Schritt nach dem anderen.** Bei jedem Schritt: Steuerelement in der Strukturansicht suchen (Ort steht dabei), Property im Formelfeld wählen, **ganze Property ersetzen** (alles markieren, einfügen), Enter.
2. **Nach jedem Schritt:** App-Prüfung (oben rechts das Stethoskop-Symbol): neue **Formelfehler** (rot)? Dann stoppen und im Chat melden (Schritt, Property, Fehlertext). Warnungen (gelb) notieren, nicht stoppen.
3. **Testen:** Test unter dem Schritt durchführen, im Testbogen (Abschnitt 13) abhaken.
4. **Speichern** nach jedem Schritt (Strg+S). Veröffentlichen erst am Ende einer Phase.
5. **Rückfall:** Jede Originalformel steht im Anhang A. Ganze Property wieder ersetzen. Neue Properties: leeren bzw. Standard. Neue Steuerelemente: löschen.
6. **Neue Steuerelemente** (G4, G8, G14): Anleitung steht beim Schritt. **Name exakt so** vergeben (Doppelklick auf den Namen in der Strukturansicht), sonst passen die Formeln nicht.
7. **`Items.Value`** (G9) ist kein Formelfeld: rechts im Eigenschaftenbereich „Wert“ auswählen.
8. **Deutsche Schreibweise:** Alle Blöcke sind schon deutsch (`;` trennt, `;;` verkettet). Nichts umschreiben.

## 2. Entscheidungen, die im Plan stecken
| # | Thema | Entscheidung | Wer |
|---|---|---|---|
| E1 | Verlängern über 22:00 | abgelehnt, Plus-Knopf wird grau | Claude (Regel der Handy-App) |
| E2 | Zwei Tische zur selben Zeit | verhindert | Claude (Handy-Regel V6) |
| E3 | Einchecken | ab 30 Min vor Beginn bis Ende. Auschecken jederzeit | Claude (Handy V2) |
| E4 | Buchen in der Vergangenheit | gesperrt (vor der laufenden halben Stunde) | Claude |
| E5 | Big Table | in der Panel-Liste nicht, im Grundriss für alle buchbar | Josias |
| E6 | 5 Std / 9 Std an anderen Tagen | ab 08:00 | Claude |
| E7 | Mehrfachauswahl, Serien | bleiben | Claude |
| E8 | Frühester Start | 06:00. Der **Vorschlag** an anderen Tagen bleibt 08:00, damit niemand aus Versehen um 06:00 bucht | Josias / Claude |
| E9 | Automatische Freigabe | 30 Min nach Beginn ohne Check-in wird gelöscht, keine Mail | Josias |
| E10 | Storno | mit Rückfrage „Wirklich stornieren?“ (Handy V8) | Claude |
| E11 | Handy-App | am 14.10. mit den Kollegen mit Firmenhandy teilen. Deren GoBright-App fällt auch weg, und am Handy kann man einchecken, was mit der Freigabe wichtig wird | Claude |
| E12 | Raumcode | bleibt im Code, fragt aber beim Start nichts mehr ab (36 Abfragen weniger) | Josias (behalten) / Claude (ruhigstellen) |
| E13 | Tisch-Anzeigen von GoBright | werden am 14.10. abgeschaltet bzw. zeigen nichts mehr (Abschnitt 12) | Josias / Claude |

## 3. Phase 0: Vorbereitung (zuerst, ohne App-Formeln)
### G0.1 Sicherung
- In Studio: **Datei → Speichern unter → Diesen Computer** (`.msapp`). Name z. B. `Tischbuchung_vor_Gesamtplan_2026-10-08.msapp`.
- Die aktuelle **Versionsnummer** im Versionsverlauf notieren (Rückfall: „Wiederherstellen“).
- **Prüfe, dass seit dem Export vom 07.10. nichts geändert wurde.** Wenn doch, schick mir einen neuen Export. Der Plan ist gegen den 07.10. erzeugt, und ganze Properties würden spätere Änderungen überschreiben.

### G0.2 Bestandsdaten prüfen (kaputte Buchungen finden)
**Problem:** Der veröffentlichte Stand kann Buchungen mit Ende vor Beginn (Start 22:00, F-L1), über 22:00 oder über Mitternacht (Verlängern ohne Grenze) erzeugt haben. Solche Zeilen stören Prüfungen und Anzeigen.
**So findest du sie:** Vorübergehend eine leere **vertikale Galerie** auf `Screen1` einfügen, `Items`:
```
Filter(Tischbuchungen; Endzeit <= Startzeit || Day(Endzeit) <> Day(Startzeit) || Hour(Endzeit) * 60 + Minute(Endzeit) > 22 * 60)
```
Die Delegierungswarnung ist hier egal (~250 Zeilen, Limit 1.000). Die Galerie zeigt die betroffenen Buchungen (Titel-Feld der Galerie auf `ThisItem.Tisch.Value & " " & Text(ThisItem.Startzeit; "dd.mm. hh:mm") & "–" & Text(ThisItem.Endzeit; "dd.mm. hh:mm")` stellen). Diese Zeilen in der SharePoint-Liste korrigieren oder löschen, **danach die Galerie wieder löschen**.

### G0.3 Spalte „Gesperrt“ in der Liste `Tische`
**Warum:** Damit du Tische sperren kannst (Reparatur, Umbau), ohne den Code zu ändern (Plan P4). Mehrere Schritte (G6, G7, G9, G13, G14) lesen diese Spalte. **Sie muss vor G6 existieren.**
1. SharePoint → Liste **Tische** → **+ Spalte hinzufügen → Ja/Nein**. Name genau **`Gesperrt`**, Standardwert **Nein**. Speichern.
2. In Studio: links **Daten** → bei **Tische** auf **…** → **Aktualisieren**. Ohne das kennt die App die Spalte nicht, und die Formeln werden rot.
3. Sperren: In der Liste beim Tisch `Gesperrt = Ja`. Entsperren: `Nein`. Den Big Table **nicht** sperren (alle dürfen ihn über den Grundriss buchen).

### G0.4 Mail an Michael (heute)
Vorschlag zum Kopieren:
> Hallo Michael,
> am 14.10. löst unsere eigene Tischbuchungs-App GoBright ab. Dazu brauche ich bitte kurz deine Hilfe:
> 1. **Datenschutz/Betriebsrat:** Die App zeigt im Grundriss Initialen und im Popup den Namen der Person, die einen Tisch gebucht hat (wie GoBright). Müssen wir das mit dem Datenschutz oder Betriebsrat abstimmen?
> 2. **Mitbesitzer:** Ich möchte dich als Mitbesitzer der App „Tischbuchung“, der SharePoint-Listen `Tischbuchungen` und `Tische` und der Flows eintragen, damit du im Notfall eingreifen kannst. Ist das okay?
> 3. **Lizenzen:** Haben alle Nutzer eine M365-Lizenz mit Power-Apps-Nutzungsrecht? (Die App nutzt nur Standard-Konnektoren.)
> 4. **GoBright-Hardware:** Die Tischanzeigen und das Gateway hängen an der GoBright-Cloud und funktionieren nach Vertragsende vermutlich nicht mehr. Sollen wir sie ausstecken bzw. abbauen?
> Danke! Josias

## Übersicht aller App-Schritte

| Schritt | Phase | Was | Properties | neu anzulegen |
|---|---|---|---|---|
| G1 | 1 | Grundlage: Variablen beim App-Start | 1 | – |
| G2 | 1 | Verwalten-Dialoge: Grenze beim Öffnen, Dauer-Knöpfe ohne Abfrage | 20 | – |
| G3 | 1 | Verlängern/Verkürzen sicher | 4 | – |
| G4 | 1 | Stornieren sicher, mit Bestätigung | 48 | `btnStornoJa`, `btnStornoNein`, `conStornoFrage`, `lblStornoFrage` |
| G5 | 1 | Einchecken sicher | 2 | – |
| G6 | 1 | Neue Buchung speichern (Dialog und Panel) | 4 | – |
| G7 | 1 | Dialoge öffnen mit frischen Eingaben, Startzeiten ab 06:00 | 6 | – |
| G8 | 2 | Automatisch aktualisieren (Timer) | 5 | `tmrAktualisieren` |
| G9 | 3 | Tischauswahl im Panel: nur freie Tische | 4 | – |
| G10 | 3 | Knöpfe 5 Std / 9 Std | 6 | – |
| G11 | 3 | Hinweistext Wiederholung im Panel | 2 | – |
| G12 | 3 | Kleine Korrekturen | 6 | – |
| G13 | 4 | Grundriss: gesperrte Tische grau | 2 | – |
| G14 | 4 | Grundriss: freie Zeit an belegten Tischen buchen | 24 | `btnAndereZeit`, `lblBelegtHeute` |
| G15 | 4 | Details-Popup: Status wie Kachel | 2 | – |
| G16 | 4 | Dashboard-Liste nach Uhrzeit | 2 | – |
| G17 | 5 | Gedrückte Knöpfe lesbar | 13 | – |
| G18 | 5 | Aktiver Tab sichtbar | 2 | – |
| G19 | 5 | Profilfarbe fest | 1 | – |
| G20 | 5 | Buchungsdialog im selben Design wie das Panel | 14 | – |
| G21 | 5 | Stornieren rot | 3 | – |
| G22 | 5 | Texte einheitlich Deutsch | 18 | – |
| G23 | 5 | Auswahl- und Trennlinienfarben | 16 | – |
| G24 | 5 | Einheitlicher Hover auf Klickflächen | 5 | – |
| G25 | 6 | Raumcode ruhigstellen (bleibt erhalten) | 6 | – |
| G26 | 7 | Barrierefreiheit: Beschriftungen | 37 | – |

## 4. Phase 1: Fundament (Pflicht vor dem Go-Live)
Diese sieben Schritte schließen alle Wege zu Doppelbuchungen, Buchungen am falschen Tag und rohen Fehlermeldungen. Sie gehören zusammen. **Teste erst nach G7 alles zusammen**, einzelne Kurztests stehen trotzdem bei jedem Schritt.

### G1 Grundlage: Variablen beim App-Start

**Problem:** Die neue Doppelklick-Sperre und die Verlängern-Grenzen brauchen Startwerte.
**Lösung:** Drei Zeilen ganz am **Anfang** von `App.OnStart` (`varSperreBis`, `varVerlGrenze`, `varVerlGrenzeTab`). Die L2-Ladezeile bleibt die letzte Anweisung. Die Sperre funktioniert auch ohne diese Zeilen (sie fängt ein leeres `varSperreBis` ab), aber so sind die Typen eindeutig.
**Test:** App-Prüfung ohne Fehler. In der Strukturansicht bei **App** auf **…** → **OnStart ausführen** (Studio führt OnStart nach dem Einfügen nicht von selbst aus). Vorschau: Der Grundriss lädt wie bisher.

**`App.OnStart`** · Ort: `App` · **ganze Property ersetzen** · Herkunft: K v2 0

```
Set(varSperreBis; Now());;
Set(varVerlGrenze; Now());;
Set(varVerlGrenzeTab; Now());;
Set(varSelectedTisch; Blank());;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedBuchung; Blank());;
Set(varAktiverTab; "dashboard");;
Set(varZeigeRaumBuchungForm; false);;
Set(varAusgewähltRaum; Blank());;
Set(varAusgewählteStartzeit; Blank());;
Set(varAusgewählteEndzeit; Blank());;
Set(varZeigeRaumBestätigung; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varWiederholenBis; Today() + 14);;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeRaumInfo; false);;
Set(varZeigeRaumVerwalten; false);;
Set(
  varProfilFarbe;
  Switch(
    RandBetween(1; 8);
    1; ColorValue("#8CAFF4");
    2; ColorValue("#82C7B3");
    3; ColorValue("#EFA897");
    4; ColorValue("#B59EDC");
    5; ColorValue("#82CCC5");
    6; ColorValue("#F5C295");
    7; ColorValue("#A1AADB");
    ColorValue("#A1B1BA")
  )
);;
Set(varZoom; 1);;
Set(varPanX; 0);;
Set(varPanY; 0);;
Set(varWiederholenBisGewaehlt; false);;
ClearCollect(
  colTischPositionen;
  {Tisch: "OG Desk 1"; X: 1380; Y: 270; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 2"; X: 1629; Y: 290; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 3"; X: 1732; Y: 288; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 4"; X: 1629; Y: 348; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 5"; X: 1732; Y: 346; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 6"; X: 1734; Y: 536; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 7"; X: 1734; Y: 596; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 8"; X: 1500; Y: 484; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 9"; X: 1500; Y: 584; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 10"; X: 1500; Y: 683; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 11"; X: 1560; Y: 468; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 12"; X: 1560; Y: 582; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 13"; X: 1560; Y: 681; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 3"; X: 870; Y: 687; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 2"; X: 870; Y: 594; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 1"; X: 870; Y: 501; Ausrichtung: "Vertikal"}
);;
Set(varSelectedBuchungTab; Blank());;
Set(varZeigeVerwaltenTab; false);;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varAnsichtsDatum; Today());;
Set(varAusgewaehltesStockwerk; "OG");;
Set(varStockwerkDropdownOffen; false);;
Set(varStartOverride; "");;
Set(varEndeOverride; "");;
Clear(colAusgewaehlteBuchungen);;
Set(varMehrfachAuswahlModus; false);;
Set(varAuswahlModusAktiv; false);;
Set(varZeigeVerwaltenKlein; false);;
Set(varGalleryNeuAufbauen; 0);;
Set(varGeklickteBuchungKlein; Blank());;
ClearCollect(
  colTischPositionenUG;
  {Tisch: "UG Desk 1";  X: 530;  Y: 592; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 2";  X: 530;  Y: 679; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 3";  X: 582;  Y: 588; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 4";  X: 582;  Y: 675; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 5";  X: 738;  Y: 584; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 6";  X: 738;  Y: 671; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 7";  X: 790;  Y: 579; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 8";  X: 790;  Y: 666; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 9";  X: 1011; Y: 575; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 10"; X: 1011; Y: 662; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 11"; X: 1063; Y: 571; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 12"; X: 1063; Y: 658; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 13"; X: 1202; Y: 260; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 14"; X: 1210; Y: 348; Ausrichtung: "Horizontal"};
  {Tisch: "UG Desk 15"; X: 1255; Y: 256; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 16"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 17"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
);;
Set(varIsLoading; false);;
Set(varSpinnerWinkel; 0);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

### G2 Verwalten-Dialoge: Grenze beim Öffnen, Dauer-Knöpfe ohne Abfrage

**Problem (belegt):** (1) **Befund B0:** Der Verwalten-Dialog im Buchungen-Tab merkt sich die Buchung in `varSelectedBuchungTab`, seine sechs Dauer-Knöpfe prüfen aber `varSelectedBuchung`, also die zuletzt im Dashboard angeklickte Buchung. Ein Knopf kann grün sein, obwohl hinter **dieser** Buchung jemand gebucht hat → stille Doppelbuchung. (2) Jeder der 9 Dauer-Knöpfe fragt in `DisplayMode` und `Fill` selbst SharePoint ab, zusammen 18 Abfragen, auch bei geschlossenem Dialog (gemessen: ~50 Abfragen pro Schreibvorgang mit den Panel-Knöpfen). (3) Im Tab blieb die zuletzt gewählte Dauer stehen. (4) Verlängern über 22:00 war möglich.
**Lösung:** Beim Klick auf „Verwalten“ wird **einmal** die **Grenze** berechnet: der Beginn der nächsten Buchung am selben Tisch nach meinem Ende, höchstens 22:00 am Buchungstag. Dafür gibt es eine delegierbare Abfrage `First(Sort(Filter(…)))`, die Werte stehen in globalen Variablen. Die Knöpfe vergleichen nur noch `Ende + Dauer > Grenze`. Das ist dieselbe Bedingung wie vorher (logisch umgeformt, zweimal unabhängig geprüft), plus 22:00. Jeder Dialog hat seine eigene Grenze (`varVerlGrenze` Dashboard, `varVerlGrenzeTab` Tab), der Tab liest jetzt seine eigene Buchung. Beim Öffnen wird die Dauer geleert.
**Test:** Dashboard → Verwalten einer heutigen Buchung, die um 20:30 endet: +1 grün, +2 und +3 grau. **B0-Test:** Im Dashboard Buchung A verwalten und schließen. Im Tab Buchung B verwalten, hinter der direkt jemand gebucht hat → +1 ist grau. Tab: −1/−2/−3 je nach Länge grau.

**`btnVerwalten.OnSelect`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten` · **ganze Property ersetzen** · Herkunft: K v2 A1

```
Set(varSelectedBuchung; ThisItem);;
Set(varVerlTisch; ThisItem.Tisch.Value);;
Set(varVerlEndeAlt; ThisItem.Endzeit);;
Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false)
```

**`btnVerwalten_2.OnSelect`** · Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2` · **ganze Property ersetzen** · Herkunft: K v2 A2

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varVerlTisch; ThisItem.Tisch.Value);;
  Set(varVerlEndeAlt; ThisItem.Endzeit);;
  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
  Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

**`btnPlus1Std.DisplayMode`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus1Std` · **ganze Property ersetzen** · Herkunft: K v2 A3

```
If(IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenze; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnPlus1Std.Fill`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus1Std` · **ganze Property ersetzen** · Herkunft: K v2 A3

```
If(
  varAusgewaehltePlusDauer = 60;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenze;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnPlus2Std.DisplayMode`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus2Std` · **ganze Property ersetzen** · Herkunft: K v2 A3

```
If(IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenze; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnPlus2Std.Fill`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus2Std` · **ganze Property ersetzen** · Herkunft: K v2 A3

```
If(
  varAusgewaehltePlusDauer = 120;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenze;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnPlus3Std.DisplayMode`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus3Std` · **ganze Property ersetzen** · Herkunft: K v2 A3

```
If(IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenze; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnPlus3Std.Fill`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus3Std` · **ganze Property ersetzen** · Herkunft: K v2 A3

```
If(
  varAusgewaehltePlusDauer = 180;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenze;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnPlus1Std_1.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus1Std_1` · **ganze Property ersetzen** · Herkunft: K v2 A4

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenzeTab; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnPlus1Std_1.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus1Std_1` · **ganze Property ersetzen** · Herkunft: K v2 A4

```
If(
  varAusgewaehltePlusDauer = 60;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenzeTab;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnPlus2Std_1.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus2Std_1` · **ganze Property ersetzen** · Herkunft: K v2 A4

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenzeTab; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnPlus2Std_1.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus2Std_1` · **ganze Property ersetzen** · Herkunft: K v2 A4

```
If(
  varAusgewaehltePlusDauer = 120;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenzeTab;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnPlus3Std_1.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus3Std_1` · **ganze Property ersetzen** · Herkunft: K v2 A4

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenzeTab; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnPlus3Std_1.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus3Std_1` · **ganze Property ersetzen** · Herkunft: K v2 A4

```
If(
  varAusgewaehltePlusDauer = 180;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenzeTab;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnMinus1Std.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus1Std` · **ganze Property ersetzen** · Herkunft: K v2 A5

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -60; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnMinus1Std.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus1Std` · **ganze Property ersetzen** · Herkunft: K v2 A5

```
If(
  varAusgewaehltePlusDauer = -60;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -60; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnMinus2Std.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus2Std` · **ganze Property ersetzen** · Herkunft: K v2 A5

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -120; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnMinus2Std.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus2Std` · **ganze Property ersetzen** · Herkunft: K v2 A5

```
If(
  varAusgewaehltePlusDauer = -120;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -120; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**`btnMinus3std.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus3std` · **ganze Property ersetzen** · Herkunft: K v2 A5

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -180; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnMinus3std.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus3std` · **ganze Property ersetzen** · Herkunft: K v2 A5

```
If(
  varAusgewaehltePlusDauer = -180;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -180; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

### G3 Verlängern/Verkürzen sicher

**Problem (belegt):** Verlängern prüfte die Belegung nur beim Einfärben, nicht beim Speichern. Zwischen Öffnen und Klick konnte jemand buchen. Doppelklick verlängerte doppelt (in der Handy-App gemessen: aus +1 wurden +2). Fehler wurden verschluckt, Dauer `0` nach Stockwerkwechsel schrieb „+0“.
**Lösung:** Erprobtes Muster aus der Handy-App: **Zweifach-Sperre** (`varIsLoading` + 2 Sekunden `varSperreBis`) → Buchung **frisch** laden → Prüfungen mit eigener Meldung (keine Dauer, gelöscht, wäre leer, über 22:00, inzwischen belegt) → `Patch` in `IfError` → **Nachlese**: Ist das neue Ende wirklich angekommen? → ehrliche Meldung → Liste und Grundriss neu laden. Der Knopf ist erst bedienbar, wenn eine Dauer gewählt ist. Nach „inzwischen belegt“ werden die Plus-Knöpfe grau.
**Test:** +1 Std → „Buchung geändert, neues Ende hh:mm Uhr.“. **Doppelklick** → nur einmal verlängert. Zwei Browser-Tabs: In Tab 2 direkt dahinter buchen, in Tab 1 verlängern → „inzwischen belegt“. Im Tab −1 Std → verkürzt.

**`btnVerlängern.OnSelect`** · Ort: `Screen1 > conVerwaltenDialog > btnVerlängern` · **ganze Property ersetzen** · Herkunft: K v2 A6

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varVerlBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0;
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    IsBlank(varVerlBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwalten; false);
    Set(varVerlTisch; varVerlBuchung.Tisch.Value);;
    Set(varVerlEndeAlt; varVerlBuchung.Endzeit);;
    Set(varVerlEndeNeu; DateAdd(varVerlBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes));;
    Set(varVerlTagesende; DateAdd(varVerlBuchung.Startzeit; 22 * 60 - (Hour(varVerlBuchung.Startzeit) * 60 + Minute(varVerlBuchung.Startzeit)); TimeUnit.Minutes));;
    If(
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID);
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
      Set(varVerlGrenze; varVerlEndeAlt);
      IfError(
        Patch(Tischbuchungen; varVerlBuchung; {Endzeit: varVerlEndeNeu});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varVerlBuchung.ID));;
        If(
          varSelectedBuchung.Endzeit = varVerlEndeNeu;
          Notify("Buchung geändert, neues Ende " & Text(varVerlEndeNeu; "hh:mm") & " Uhr."; NotificationType.Success);;
          Set(varZeigeVerwalten; false);
          Notify("Die Änderung ist nicht angekommen. Bitte die Buchung in der Liste prüfen."; NotificationType.Warning)
        )
      )
    )
  );;
  Refresh(Tischbuchungen);;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerlängern.DisplayMode`** · Ort: `Screen1 > conVerwaltenDialog > btnVerlängern` · **neu setzen** · Herkunft: K v2 A6

```
If(varIsLoading || IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnVerlängern_1.OnSelect`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1` · **ganze Property ersetzen** · Herkunft: K v2 A7

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varVerlBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
  If(
    IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0;
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    IsBlank(varVerlBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwaltenTab; false);
    Set(varVerlTisch; varVerlBuchung.Tisch.Value);;
    Set(varVerlEndeAlt; varVerlBuchung.Endzeit);;
    Set(varVerlEndeNeu; DateAdd(varVerlBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes));;
    Set(varVerlTagesende; DateAdd(varVerlBuchung.Startzeit; 22 * 60 - (Hour(varVerlBuchung.Startzeit) * 60 + Minute(varVerlBuchung.Startzeit)); TimeUnit.Minutes));;
    If(
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID);
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
      Set(varVerlGrenzeTab; varVerlEndeAlt);
      IfError(
        Patch(Tischbuchungen; varVerlBuchung; {Endzeit: varVerlEndeNeu});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchungTab; LookUp(Tischbuchungen; ID = varVerlBuchung.ID));;
        If(
          varSelectedBuchungTab.Endzeit = varVerlEndeNeu;
          Notify("Buchung geändert, neues Ende " & Text(varVerlEndeNeu; "hh:mm") & " Uhr."; NotificationType.Success);;
          Set(varZeigeVerwaltenTab; false);
          Notify("Die Änderung ist nicht angekommen. Bitte die Buchung in der Liste prüfen."; NotificationType.Warning)
        )
      )
    )
  );;
  Refresh(Tischbuchungen);;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerlängern_1.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1` · **neu setzen** · Herkunft: K v2 A7

```
If(varIsLoading || IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0; DisplayMode.Disabled; DisplayMode.Edit)
```

### G4 Stornieren sicher, mit Bestätigung

**Problem (belegt):** Stornieren im Dashboard löschte den Stand vom Öffnen des Dialogs (`Remove(…; varSelectedBuchung)`) ohne Fehlerbehandlung. War die Buchung inzwischen weg, kam die rohe englische Meldung **„Item Not Found“** (euer gemeldeter Fehler vom 30.09.). Es gab keine Rückfrage, ein Fehlklick löschte sofort, und Doppelklick war nicht gesperrt.
**Lösung:** (1) Die drei Storno-Knöpfe (Dashboard, Tab, Mehrfach) **fragen nur noch**: Sie merken sich, woher die Frage kommt (`varStornoQuelle`), und öffnen den neuen Dialog `conStornoFrage`. (2) „Ja, stornieren“ führt je nach Herkunft die sichere Storno-Formel aus: Sperre → frisch laden → `Remove` in `IfError` → Nachlese (ist sie wirklich weg?) → Meldung → neu laden. Für das Mehrfach-Stornieren bleibt deine bewährte Formel, nur mit Sperre.
**Neues Steuerelement anlegen (4 Stück), dann alle Properties unten setzen:**
1. In der Strukturansicht `Screen1` wählen → **Einfügen → Layout → Container** → umbenennen in **`conStornoFrage`**. Er muss direkt unter `Screen1` liegen, nicht in einem anderen Container.
2. `conStornoFrage` wählen → **Einfügen → Textbeschriftung** → **`lblStornoFrage`**.
3. `conStornoFrage` wählen → **Einfügen → Schaltfläche** (klassisch) → **`btnStornoNein`**, noch einmal → **`btnStornoJa`**.
4. Liegt `conStornoFrage` in der Strukturansicht **über** `conLadeOverlay`, ist das in Ordnung (der Dialog schließt sich vor dem Laden).
**Test:** Dashboard → Verwalten → Stornieren → Rückfrage → „Nein“ → nichts passiert. Noch einmal → „Ja, stornieren“ → „Buchung storniert.“. Zwei Tabs: In Tab 2 stornieren, in Tab 1 stornieren → „Diese Buchung gibt es nicht mehr…“ (kein „Item Not Found“). Tab „Buchungen“ und Mehrfachauswahl genauso. Die Rückfrage nennt bei der Mehrfachauswahl die Anzahl.

Neue Steuerelemente (zuerst anlegen, Name exakt so): `conStornoFrage` (Container (Einfügen → Layout → Container), auf oberster Ebene einfügen (nicht in einen anderen Container)), `lblStornoFrage` (Label (Einfügen → Textbeschriftung), in `conStornoFrage` einfügen), `btnStornoNein` (Button (Einfügen → Schaltfläche, klassisch), in `conStornoFrage` einfügen), `btnStornoJa` (Button (Einfügen → Schaltfläche, klassisch), in `conStornoFrage` einfügen)

**`conStornoFrage.Visible`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
varZeigeStornoFrage
```

**`conStornoFrage.X`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
(Parent.Width - Self.Width) / 2
```

**`conStornoFrage.Y`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
(Parent.Height - Self.Height) / 2
```

**`conStornoFrage.Width`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
420
```

**`conStornoFrage.Height`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
150
```

**`conStornoFrage.Fill`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
Color.White
```

**`conStornoFrage.BorderColor`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
RGBA(32; 54; 71; 1)
```

**`conStornoFrage.BorderThickness`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
1
```

**`conStornoFrage.RadiusTopLeft`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
16
```

**`conStornoFrage.RadiusTopRight`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
16
```

**`conStornoFrage.RadiusBottomLeft`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
16
```

**`conStornoFrage.RadiusBottomRight`** · Ort: `(neu) Screen1 > conStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
16
```

**`lblStornoFrage.Text`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
If(varStornoQuelle = "klein"; "Wirklich " & CountRows(colAusgewaehlteBuchungen) & " Buchung(en) stornieren?"; "Diese Buchung wirklich stornieren?")
```

**`lblStornoFrage.X`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
25
```

**`lblStornoFrage.Y`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
20
```

**`lblStornoFrage.Width`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
370
```

**`lblStornoFrage.Height`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
50
```

**`lblStornoFrage.Size`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
15
```

**`lblStornoFrage.FontWeight`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
FontWeight.Bold
```

**`lblStornoFrage.Color`** · Ort: `(neu) conStornoFrage > lblStornoFrage` · **neu setzen** · Herkunft: P6 neu

```
RGBA(32; 54; 71; 1)
```

**`btnStornoNein.Text`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
"Nein"
```

**`btnStornoNein.X`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
25
```

**`btnStornoNein.Y`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
90
```

**`btnStornoNein.Width`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
170
```

**`btnStornoNein.Height`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
40
```

**`btnStornoNein.Fill`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
Color.Black
```

**`btnStornoNein.Color`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
Color.White
```

**`btnStornoNein.HoverFill`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
ColorFade(Self.Fill; 30%)
```

**`btnStornoNein.PressedFill`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
ColorFade(Color.Black; 30%)
```

**`btnStornoNein.PressedColor`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
Color.White
```

**`btnStornoNein.OnSelect`** · Ort: `(neu) conStornoFrage > btnStornoNein` · **neu setzen** · Herkunft: P6 neu

```
Set(varZeigeStornoFrage; false)
```

**`btnStornoJa.Text`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
"Ja, stornieren"
```

**`btnStornoJa.X`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
225
```

**`btnStornoJa.Y`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
90
```

**`btnStornoJa.Width`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
170
```

**`btnStornoJa.Height`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
40
```

**`btnStornoJa.Fill`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
ColorValue("#EB3951")
```

**`btnStornoJa.Color`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
Color.White
```

**`btnStornoJa.HoverFill`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
ColorFade(Self.Fill; -20%)
```

**`btnStornoJa.PressedFill`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
ColorFade(Self.Fill; -30%)
```

**`btnStornoJa.PressedColor`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
Color.White
```

**`btnStornoJa.DisplayMode`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnStornoJa.OnSelect`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **neu setzen** · Herkunft: P6 neu

```
Set(varZeigeStornoFrage; false);;
Switch(
  varStornoQuelle;
  "dash";
  If(
    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
    Set(varIsLoading; true);;
    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
    If(
      IsBlank(varStornoBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwalten; false);
      IfError(
        Remove(Tischbuchungen; varStornoBuchung);
        Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        If(
          IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
          Notify("Buchung storniert."; NotificationType.Success);;
          Set(varZeigeVerwalten; false);
          Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
        )
      )
    );;
    Refresh(Tischbuchungen);;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  );
  "tab";
  If(
    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
    Set(varIsLoading; true);;
    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
    If(
      IsBlank(varStornoBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwaltenTab; false);
      IfError(
        Remove(Tischbuchungen; varStornoBuchung);
        Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        If(
          IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
          Notify("Buchung storniert."; NotificationType.Success);;
          Set(varZeigeVerwaltenTab; false);
          Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
        )
      )
    );;
    Refresh(Tischbuchungen);;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  );
  If(
    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
    Set(varIsLoading; true);;
    ClearCollect(
        colStornoFrisch;
        Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
    );;
    ClearCollect(
        colStornoZiele;
        Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
    );;
    If(
        CountRows(colAusgewaehlteBuchungen) = 0;
        Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
        If(
            CountRows(colStornoZiele) = 0;
            Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
            IfError(
                Remove(Tischbuchungen; colStornoZiele);
                Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
                If(
                    CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
                    Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
                    Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
                )
            )
        )
    );;
    Refresh(Tischbuchungen);;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
    Clear(colStornoFrisch);;
    Clear(colStornoZiele);;
    Clear(colAusgewaehlteBuchungen);;
    Set(varGeklickteBuchungKlein; Blank());;
    Set(varZeigeVerwaltenKlein; false);;
    Set(varAuswahlModusAktiv; false);;
    Reset(tglAuswahlModus);;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  )
)
```

**`btnStornieren.OnSelect`** · Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **ganze Property ersetzen** · Herkunft: K v2 A8, P6

```
Set(varStornoQuelle; "dash");;
Set(varZeigeStornoFrage; true)
```

**`btnStornieren.DisplayMode`** · Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **neu setzen** · Herkunft: K v2 A8

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnStornieren_1.OnSelect`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **ganze Property ersetzen** · Herkunft: K v2 A9, P6

```
Set(varStornoQuelle; "tab");;
Set(varZeigeStornoFrage; true)
```

**`btnStornieren_1.DisplayMode`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **neu setzen** · Herkunft: K v2 A9

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnStornierenKlein.OnSelect`** · Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein` · **ganze Property ersetzen** · Herkunft: K v2 D3, P6

```
Set(varStornoQuelle; "klein");;
Set(varZeigeStornoFrage; true)
```

### G5 Einchecken sicher

**Problem (belegt):** Einchecken ging für jeden Tag und zu jeder Zeit (z. B. übermorgen), ohne Fehlerbehandlung. Mit der automatischen Freigabe ist Check-in jetzt wichtig und muss zuverlässig sein.
**Lösung:** Sperre → frisch laden → **Fenster ab 30 Min vor Beginn bis Ende** (wie in der Handy-App) → `Patch` in `IfError` → Nachlese → Meldung „Eingecheckt.“/„Ausgecheckt.“. Auschecken bleibt jederzeit möglich.
**Test:** Buchung, die in einer Stunde beginnt → Einchecken → Meldung „erst ab 30 Minuten vor Beginn“. Laufende Buchung → „Eingecheckt.“, Kachel rot.

**`btnEinchecken.OnSelect`** · Ort: `Screen1 > conCheckinDialog > btnEinchecken` · **ganze Property ersetzen** · Herkunft: K v2 A10

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varCheckinBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);;
    Set(varZeigeCheckin; false);
    !varCheckinBuchung.CheckedIn && (Now() < DateAdd(varCheckinBuchung.Startzeit; -30; TimeUnit.Minutes) || Now() > varCheckinBuchung.Endzeit);
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn und nur bis zum Ende möglich."; NotificationType.Warning);
    IfError(
      Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: !varCheckinBuchung.CheckedIn});
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
      If(
        varSelectedBuchung.CheckedIn <> varCheckinBuchung.CheckedIn;
        Notify(If(varSelectedBuchung.CheckedIn; "Eingecheckt."; "Ausgecheckt."); NotificationType.Success);;
        Set(varZeigeCheckin; false);
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
      )
    )
  );;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnEinchecken.DisplayMode`** · Ort: `Screen1 > conCheckinDialog > btnEinchecken` · **neu setzen** · Herkunft: K v2 A10

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

### G6 Neue Buchung speichern (Dialog und Panel)

**Problem (belegt):** Die beiden Speichern-Knöpfe (Buchungsdialog aus dem Grundriss und Panel „Tisch buchen“) waren verschieden gebaut. Der Dialog nutzt den Sammel-Patch, das Panel eine alte Schleife. Keiner prüfte, ob die Person zur selben Zeit schon einen Tisch hat. Beide erlaubten Buchungen in der Vergangenheit. Die Kollisionsabfrage lud **alle** Buchungen des Tisches (Datenzeilenlimit). Meldungen zählten lokal statt nachzulesen, und „auf 2 Wochen begrenzt“ verdrängte die Kollisionsmeldung. Nach einem Fehler schloss der Dialog und die Eingaben waren weg. Doppelklick buchte doppelt.
**Lösung:** **Ein** Ablauf für beide Knöpfe:
1. Sperre setzen.
2. Werte zum Klickzeitpunkt in Variablen übernehmen.
3. Termine berechnen (Serie mit Kappung auf 14 Tage, Wochentage Mo–Fr).
4. Prüfungen mit je eigener Meldung: Tisch gewählt? Ende nach Beginn? Wochentag gewählt? Bis-Datum vor dem Start? Tisch **gesperrt** (neu)? Vergangenheit?
5. **Eine** delegierbare Abfrage „Tisch belegt im Zeitraum“ und **eine** „ich habe schon einen Tisch“.
6. Je Termin entscheiden: frei, Tisch belegt oder „ich belegt“.
7. **Sammel-Patch** der freien Termine mit gemeinsamer **`SerienID`** (die Spalte gibt es, sie war nie befüllt).
8. `Refresh` und **Nachlese:** Wie viele sind wirklich angekommen? Hat jemand in derselben Sekunde mit kleinerer ID gebucht?
9. **Eine** Meldung mit allem. Bei Erfolg kommt dazu der Hinweis **„Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben.“**
10. Nur wenn etwas gebucht wurde: Dialog schließen und Eingaben leeren.

**Test:** Einzelbuchung → „Gebucht: OG Desk 5, 09.10., 09:00 bis 10:00 Uhr. Bitte bis 30 Minuten …“. In SharePoint hat die neue Zeile eine `SerienID`. Serie Mo–Fr über 2 Wochen mit einem belegten Tag → „9 von 10 Terminen gebucht … 1× war der Tisch schon belegt.“. Zur selben Zeit schon anderswo gebucht → „Du hast in dieser Zeit schon einen Tisch gebucht.“. Gesperrter Tisch → Meldung. Datum gestern → „Vergangenheit“. **Doppelklick** → eine Buchung.

**`btnSpeichern.OnSelect`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen** · Herkunft: K v2 B1, Check-in-Hinweis, P4 Gesperrt

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varNeuTischTitel; varSelectedTisch.Titel);;
  Set(varNeuTischID; varSelectedTisch.ID);;
  Set(varNeuEmail; User().Email);;
  Set(varNeuDatum; dpDatum.SelectedDate);;
  Set(varNeuStartZeit; Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0));;
  Set(varNeuEndeZeit; Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0));;
  Set(varNeuBisRoh; If(varWiederholen; dpWiederholenBis.SelectedDate; varNeuDatum));;
  Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
  Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
  ClearCollect(
    colNeuTermine;
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum; 0; DateDiff(varNeuDatum; varNeuBis; TimeUnit.Days) + 1); 0); DateAdd(varNeuDatum; Value; TimeUnit.Days)) As D;
        !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
      ) As T;
      {Start: T.Value + varNeuStartZeit; Ende: T.Value + varNeuEndeZeit}
    )
  );;
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID);
    Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
    varNeuEndeZeit <= varNeuStartZeit;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
    Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
    varWiederholen && varNeuBisRoh < varNeuDatum;
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varNeuTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    IsEmpty(colNeuTermine);
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning);
    First(colNeuTermine).Start < varNeuJetzt;
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    Set(varNeuSpanStart; First(colNeuTermine).Start);;
    Set(varNeuSpanEnde; Last(colNeuTermine).Ende);;
    Set(varNeuGesamt; CountRows(colNeuTermine));;
    ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(
      colNeuErgebnis;
      ForAll(
        colNeuTermine As T;
        {
          Start: T.Start;
          Ende: T.Ende;
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "tisch";
            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
      Notify(
        If(
          varNeuGesamt = 1;
          If(varNeuTischBelegt = 1; "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen."; "Du hast in dieser Zeit schon einen Tisch gebucht.");
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        );
        NotificationType.Warning
      );;
      Refresh(Tischbuchungen);
      Set(varSerienID; Text(GUID()));;
      IfError(
        Patch(
          Tischbuchungen;
          ForAll(Filter(colNeuErgebnis; Grund = "frei"); Defaults(Tischbuchungen));
          ForAll(
            Filter(colNeuErgebnis; Grund = "frei") As F;
            {
              Tisch: {Id: varNeuTischID; Value: varNeuTischTitel};
              Startzeit: F.Start;
              Endzeit: F.Ende;
              Person: {
                Claims: "i:0#.f|membership|" & Lower(User().Email);
                Department: "";
                DisplayName: User().FullName;
                Email: User().Email;
                JobTitle: "";
                Picture: ""
              };
              SerienID: varSerienID
            }
          )
        );
        Set(varNeuFehler; true);
        Set(varNeuFehler; false)
      );;
      Refresh(Tischbuchungen);;
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0; " " & varNeuTischBelegt & "× war der Tisch schon belegt."; "") &
          If(varNeuIchBelegt > 0; " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch."; "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl; " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden."; "") &
          If(varNeuBisRoh > varNeuBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
          NotificationType.Warning
        )
      );;
      If(
        varNeuAnzahl > 0;
        Set(varZeigeDialog; false);;
        Set(varWiederholen; false);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Set(varTagSa; false);;
        Set(varTagSo; false)
      )
    );;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnSpeichern.DisplayMode`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **neu setzen** · Herkunft: K v2 B1

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**`btnSpeichernTischePanel.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen** · Herkunft: K v2 B2, Check-in-Hinweis, P4 Gesperrt

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varNeuTischTitel; ddTischePanel.Selected.Titel);;
  Set(varNeuTischID; ddTischePanel.Selected.ID);;
  Set(varNeuEmail; User().Email);;
  Set(varNeuDatum; dpDatumTischePanel.SelectedDate);;
  Set(varNeuStartZeit; Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0));;
  Set(varNeuEndeZeit; Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0));;
  Set(varNeuBisRoh; If(varWiederholen; dpWiederholenBis_1.SelectedDate; varNeuDatum));;
  Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
  Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
  ClearCollect(
    colNeuTermine;
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum; 0; DateDiff(varNeuDatum; varNeuBis; TimeUnit.Days) + 1); 0); DateAdd(varNeuDatum; Value; TimeUnit.Days)) As D;
        !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
      ) As T;
      {Start: T.Value + varNeuStartZeit; Ende: T.Value + varNeuEndeZeit}
    )
  );;
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID);
    Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
    varNeuEndeZeit <= varNeuStartZeit;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
    Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
    varWiederholen && varNeuBisRoh < varNeuDatum;
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varNeuTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    IsEmpty(colNeuTermine);
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning);
    First(colNeuTermine).Start < varNeuJetzt;
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    Set(varNeuSpanStart; First(colNeuTermine).Start);;
    Set(varNeuSpanEnde; Last(colNeuTermine).Ende);;
    Set(varNeuGesamt; CountRows(colNeuTermine));;
    ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(
      colNeuErgebnis;
      ForAll(
        colNeuTermine As T;
        {
          Start: T.Start;
          Ende: T.Ende;
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "tisch";
            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
      Notify(
        If(
          varNeuGesamt = 1;
          If(varNeuTischBelegt = 1; "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen."; "Du hast in dieser Zeit schon einen Tisch gebucht.");
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        );
        NotificationType.Warning
      );;
      Refresh(Tischbuchungen);
      Set(varSerienID; Text(GUID()));;
      IfError(
        Patch(
          Tischbuchungen;
          ForAll(Filter(colNeuErgebnis; Grund = "frei"); Defaults(Tischbuchungen));
          ForAll(
            Filter(colNeuErgebnis; Grund = "frei") As F;
            {
              Tisch: {Id: varNeuTischID; Value: varNeuTischTitel};
              Startzeit: F.Start;
              Endzeit: F.Ende;
              Person: {
                Claims: "i:0#.f|membership|" & Lower(User().Email);
                Department: "";
                DisplayName: User().FullName;
                Email: User().Email;
                JobTitle: "";
                Picture: ""
              };
              SerienID: varSerienID
            }
          )
        );
        Set(varNeuFehler; true);
        Set(varNeuFehler; false)
      );;
      Refresh(Tischbuchungen);;
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0; " " & varNeuTischBelegt & "× war der Tisch schon belegt."; "") &
          If(varNeuIchBelegt > 0; " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch."; "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl; " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden."; "") &
          If(varNeuBisRoh > varNeuBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
          NotificationType.Warning
        )
      );;
      If(
        varNeuAnzahl > 0;
        Set(varZeigeTischBuchungForm; false);;
        Set(varAktiverTab; "dashboard");;
        Set(varWiederholen; false);;
        Reset(chkWiederholenPanel);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Reset(tglTagMo_1);;
        Reset(tglTagDi_1);;
        Reset(tglTagMi_1);;
        Reset(tglTagDo_1);;
        Reset(tglTagFr_1);;
        Set(varAusgewaehltePanelDauer; Blank());;
        Set(varStartOverridePanel; "");;
        Set(varEndeOverridePanel; "")
      )
    );;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnSpeichernTischePanel.DisplayMode`** · Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **neu setzen** · Herkunft: K v2 B2

```
If(varIsLoading || IsBlank(ddTischePanel.Selected.Titel); DisplayMode.Disabled; DisplayMode.Edit)
```

### G7 Dialoge öffnen mit frischen Eingaben, Startzeiten ab 06:00

**Problem (belegt):**
1. Datum, Start, Ende und „Wiederholen bis“ im Buchungsdialog blieben vom letzten Öffnen stehen. Wer im Dialog „morgen“ wählte und abbrach, sah beim nächsten Tisch wieder „morgen“, obwohl der Grundriss heute zeigt.
2. Die Startliste rechnete mit `Now()`. Das wird in solchen Formeln nicht von selbst neu berechnet, deshalb wurde die Startzeit nach Stunden alt.
3. Die Startliste bot **22:00** an. Dann war die Endliste leer, und die Buchung wurde mit **Ende 00:00 vor dem Beginn** gespeichert.
4. Der früheste Start war 08:00 (an anderen Tagen).
5. Gesperrte Tische ließen sich im Grundriss öffnen.

**Lösung:**
- Beim Öffnen (Kachel bzw. „Tisch buchen“) wird der Zeitpunkt in `varDialogJetzt`/`varPanelJetzt` gemerkt, und alle Eingaben werden mit `Reset` zurückgesetzt. Die Startliste und der Startvorschlag rechnen mit diesem Zeitpunkt statt mit `Now()`.
- Die Startliste endet um **21:30** (wie in der Handy-App) und beginnt um **06:00**. Heute beginnt sie bei der nächsten halben Stunde, aber nicht vor 06:00. Der **Vorschlag** an anderen Tagen bleibt 08:00.
- Eine gesperrte Kachel meldet „Dieser Tisch ist zurzeit gesperrt.“

**Test:**
1. Grundriss → freie Kachel → im Dialog „morgen 14:00“ einstellen → Abbrechen. Andere Kachel → heute, nächste halbe Stunde.
2. Dialog um 10:05 öffnen (Start 10:30), schließen, nach 11:00 erneut öffnen → Start 11:30.
3. Datum morgen → Liste ab 06:00, vorgeschlagen 08:00, letzte Startzeit 21:30.
4. Panel „Tisch buchen“ genauso.
5. Einen Tisch in SharePoint sperren → Kachel antippen → Meldung.

**`btnHitArea.OnSelect`** · Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen** · Herkunft: L L13, P4 Gesperrt

```
If(
  ThisItem.Gesperrt;
  Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
  With(
    {
      relevanteBuchung:
        If(
          varAnsichtsDatum = Today();
          LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
          LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
        )
    };
    If(
      IsBlank(relevanteBuchung);
        Set(varSelectedTisch; ThisItem);;
        Set(varDialogJetzt; Now());;
        Reset(dpDatum);;
        Reset(ddStart);;
        Reset(ddEnde);;
        Reset(dpWiederholenBis);;
        Set(varZeigeDialog; true);;
        Set(varZeigeDetails; false);;
        Set(varZeigeCheckin; false);;
        Set(varZeigeVerwalten; false);;
        Set(varWiederholen; false);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Set(varTagSa; false);;
        Set(varTagSo; false);
        Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; relevanteBuchung);;
        Set(varZeigeDetails; true);;
        Set(varZeigeDialog; false);;
        Set(varZeigeCheckin; false);;
        Set(varZeigeVerwalten; false)
    )
  )
)
```

**`btnTischHinzufügen.OnSelect`** · Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen** · Herkunft: K v2 C2, L L13

```
Set(varZeigeTischBuchungForm; true);;
Reset(dpDatumTischePanel);;
Reset(ddTischePanel);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Reset(tglTagMo_1);;
Reset(tglTagDi_1);;
Reset(tglTagMi_1);;
Reset(tglTagDo_1);;
Reset(tglTagFr_1);;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Set(varPanelJetzt; Now());;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel);;
Reset(dpWiederholenBis_1)
```

**`ddStart.Items`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **ganze Property ersetzen** · Herkunft: L L1, 06:00

```
With(
  { minutenJetzt: Hour(varDialogJetzt)*60 + Minute(varDialogJetzt) };
  With(
    {
      minutenStart:
        If(
          dpDatum.SelectedDate = Date(Year(varDialogJetzt); Month(varDialogJetzt); Day(varDialogJetzt));
          Max(6 * 60; 30 * RoundUp(minutenJetzt / 30; 0));
          6 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(Max(0; RoundDown((minutenEnde - minutenStart) / 30; 0)); 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`ddStart.Default`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **ganze Property ersetzen** · Herkunft: L L1, 06:00

```
If(
  varStartOverride <> "";
  varStartOverride;
  With(
    { minutenJetzt: Hour(varDialogJetzt)*60 + Minute(varDialogJetzt) };
    With(
      {
        minutenStart:
          If(
            dpDatum.SelectedDate = Date(Year(varDialogJetzt); Month(varDialogJetzt); Day(varDialogJetzt));
            Max(6 * 60; 30 * RoundUp(minutenJetzt / 30; 0));
            8 * 60
          )
      };
      Text(Time(RoundDown(minutenStart / 60; 0); Mod(minutenStart; 60); 0); "hh:mm")
    )
  )
)
```

**`ddStartTischePanel.Items`** · Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel` · **ganze Property ersetzen** · Herkunft: L L1, 06:00

```
With(
  { minutenJetzt: Hour(varPanelJetzt)*60 + Minute(varPanelJetzt) };
  With(
    {
      minutenStart:
        If(
          dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt));
          Max(6 * 60; 30 * RoundUp(minutenJetzt / 30; 0));
          6 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(Max(0; RoundDown((minutenEnde - minutenStart) / 30; 0)); 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`ddStartTischePanel.Default`** · Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel` · **ganze Property ersetzen** · Herkunft: L L1, 06:00

```
If(
  varStartOverridePanel <> "";
  varStartOverridePanel;
  With(
    { minutenJetzt: Hour(varPanelJetzt)*60 + Minute(varPanelJetzt) };
    With(
      {
        minutenStart:
          If(
            dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt));
            Max(6 * 60; 30 * RoundUp(minutenJetzt / 30; 0));
            8 * 60
          )
      };
      Text(Time(RoundDown(minutenStart / 60; 0); Mod(minutenStart; 60); 0); "hh:mm")
    )
  )
)
```

## 5. Phase 2: Automatische Freigabe, Aktualisieren, Rechte

### G-F Flow „Tischbuchung – Freigabe ohne Check-in“ (Power Automate)
**Problem:** Einchecken hatte bisher keine Folge. Nicht genutzte Tische blieben belegt. GoBright gab sie frei, und so hast du es entschieden (30 Min, nur löschen).
**Lösung:** Ein geplanter Flow unter deinem Konto, alle 5 Minuten:
1. make.powerautomate.com → **Erstellen → Geplanter Cloud-Flow**. Name **`Tischbuchung – Freigabe ohne Check-in`**. Wiederholen alle **5 Minuten**.
2. **Neuer Schritt → SharePoint → Elemente abrufen.** Website: die Site `IMSKonzept`, Liste: **Tischbuchungen**.
   - **Filterabfrage** (Spaltennamen sind die **internen** Namen, `Checkedin` mit kleinem i, belegt):
   ```
   Checkedin eq 0 and Startzeit le '@{formatDateTime(addMinutes(utcNow(), -30), 'yyyy-MM-ddTHH:mm:ssZ')}' and Endzeit gt '@{formatDateTime(utcNow(), 'yyyy-MM-ddTHH:mm:ssZ')}'
   ```
   - Die Ausdrücke `@{…}` über **Ausdruck** einfügen oder genau so in das Feld tippen. Die Zeiten sind UTC, SharePoint speichert UTC: Das passt.
   - Höchstanzahl: **100**.
3. **Neuer Schritt → Auf alle anwenden** (Ausgabe `value` von „Elemente abrufen“) → darin **SharePoint → Element löschen**: Site und Liste wie oben, ID = **ID** aus „Elemente abrufen“.
4. Speichern und **Testen → Manuell**.

**Was er tut:** Er löscht nur Buchungen, die **gerade laufen** (Ende in der Zukunft), seit mindestens 30 Minuten begonnen haben und **nicht eingecheckt** sind. Vergangene Buchungen fasst er nicht an, das macht weiter dein Aufräum-Flow.

**Test:**
1. Buchung mit Start vor 40 Minuten und Ende in 2 Stunden anlegen, **nicht** einchecken → Flow manuell starten → die Buchung ist weg.
2. Dasselbe **mit** Check-in → bleibt.
3. Buchung, die vor 10 Minuten begann → bleibt.

**UNSICHER:** ob `Checkedin eq 0` für Ja/Nein-Spalten im Flow passt. Falls der Flow nichts findet, `Checkedin eq false` versuchen und melden. Die Spalten `Startzeit`/`Endzeit` müssen die internen Namen sein. Prüfen in den Listeneinstellungen: Spalte anklicken, am Ende der Adresse steht `Field=…`.
**Ablauf für Nutzer:** Ab dem Go-Live **innerhalb von 30 Minuten nach Beginn einchecken** (Dashboard „Einchecken“ oder Handy-App). Das muss in die Kurzanleitung und die Go-Live-Mail.
**Aufwand:** etwa 20 Min. **Rückfall:** Flow ausschalten.

### G8 Automatisch aktualisieren (Timer)

**Problem (belegt):** Die App hatte keinen Timer. Bei offener App blieb der Grundriss veraltet. Mit der automatischen Freigabe verschwinden jetzt laufend Buchungen, die App zeigt sie aber weiter als belegt. Über Mitternacht blieb das Ansichtsdatum auf gestern.
**Lösung:** Ein unsichtbarer Timer `tmrAktualisieren`, alle 5 Minuten. Er lädt Liste und Grundriss neu und wechselt nach Mitternacht auf heute. **Er tut nichts, solange ein Dialog oder das Panel offen ist oder gerade gespeichert wird**, damit Eingaben nicht verspringen. Er zeigt keine Warnmeldung (alle 5 Minuten eine gelbe Meldung bei kurzem Netzausfall wäre lästig). Kosten: pro offener App etwa 25 Abfragen alle 5 Minuten, weit unter dem SharePoint-Limit (geschlussfolgert).
**Neues Steuerelement anlegen:** `Screen1` wählen → **Einfügen → Eingabe → Timer** → umbenennen in **`tmrAktualisieren`** → Properties setzen.
**Test:** App offen lassen. In einem zweiten Tab eine Buchung anlegen. Nach spätestens 5 Minuten erscheint sie im Grundriss. Mit offenem Dialog passiert nichts.

Neue Steuerelemente (zuerst anlegen, Name exakt so): `tmrAktualisieren` (Timer (Einfügen → Eingabe → Timer), auf oberster Ebene einfügen)

**`tmrAktualisieren.Duration`** · Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen** · Herkunft: P3 neu

```
300000
```

**`tmrAktualisieren.Repeat`** · Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen** · Herkunft: P3 neu

```
true
```

**`tmrAktualisieren.AutoStart`** · Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen** · Herkunft: P3 neu

```
true
```

**`tmrAktualisieren.Visible`** · Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen** · Herkunft: P3 neu

```
false
```

**`tmrAktualisieren.OnTimerEnd`** · Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen** · Herkunft: P3 neu

```
If(
  !varIsLoading && !varZeigeDialog && !varZeigeTischBuchungForm && !varZeigeVerwalten && !varZeigeVerwaltenTab && !varZeigeVerwaltenKlein && !varZeigeCheckin && !varZeigeStornoFrage;
  If(
    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today();
    Set(varAnsichtsDatum; Today());;
    Reset(dpAnsichtsDatum)
  );;
  Refresh(Tischbuchungen);;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; neu)))
)
```

### G-R Rechte: „nur eigene Elemente bearbeiten“
**Problem:** Damit die App schreiben kann, dürfen alle Nutzer die Liste bearbeiten, also auch im Browser direkt **fremde** Buchungen ändern oder löschen, an allen Regeln vorbei.
**Lösung:** SharePoint → Liste **Tischbuchungen** → Zahnrad → **Listeneinstellungen** → **Erweiterte Einstellungen** → **Elementbasierte Berechtigungen**:
- Lesezugriff: **Alle Elemente lesen**.
- Erstellen und Bearbeiten: **Nur eigene Elemente erstellen und bearbeiten**.
- Speichern.

„Eigene“ heißt **„Erstellt von“**. Das passt, weil die App unter dem Konto des Nutzers schreibt. Du als Listenbesitzer (und Michael als Mitbesitzer) dürft weiterhin alles. Deshalb laufen deine beiden Flows weiter.
**Test (wichtig):**
1. Ein Kollege ohne Besitzerrechte storniert in der App seine Buchung → geht.
2. Derselbe Kollege öffnet die Liste im Browser und versucht, **deine** Buchung zu bearbeiten → nicht erlaubt.
3. Freigabe-Flow und Aufräum-Flow einmal manuell laufen lassen → löschen weiter.

**Wann:** nach dem Freigabe-Flow, vor dem Kollegentest.

## 6. Phase 3: Tischauswahl und Panel

### G9 Tischauswahl im Panel: nur freie Tische

**Problem (belegt):** Die Tischauswahl im Panel zeigte alle 34 Tische unsortiert, auch belegte und den Big Table. Ob ein Tisch frei ist, erfuhr man erst über graue Knöpfe oder beim Speichern. Das wäre wohl die häufigste Beschwerde gewesen. Beim erneuten Öffnen blieb der zuletzt gewählte Tisch stehen.
**Lösung:**
- Die Liste rechnet mit denselben Terminen wie Speichern. Sie holt **eine** Abfrage „Buchungen an den betroffenen Tagen“, die Grenzen stehen direkt als Steuerelement-Ausdrücke im Filter (laut Messung in der Handy-App die delegierbare Form).
- Danach zeigt sie nur Tische, die an mindestens einem Termin frei sind, ohne Big Table und ohne gesperrte Tische.
- Sortierung: ganz freie zuerst, dann das Stockwerk aus dem Grundriss, dann nach Nummer. Bei Serien steht dabei „(an 2 von 10 Tagen belegt)“.
- Kein Tisch ist vorausgewählt. Speichern ist ohne Tisch grau (G6). Bei geschlossenem Panel fragt die Liste nichts ab.

**Hinweis:** `Items.Value` → rechts „Wert“ auf **Anzeige** stellen.
**Test:**
1. Panel öffnen: kein Tisch gewählt, Speichern grau.
2. Morgen 09:00–10:00: belegte Tische und der Big Table fehlen, das Stockwerk des Grundrisses steht zuerst, `OG Desk 2` vor `OG Desk 10`.
3. Wiederholen Mo–Fr: Tische mit „(an x von y Tagen belegt)“ stehen hinten.
4. **Zeit ändern, nachdem ein Tisch gewählt war → notieren, ob die Auswahl bleibt oder leer wird** (UNSICHER U-C1, beides ist sicher, weil Speichern den gewählten Tisch prüft und nennt).
5. App-Prüfung: Steht eine Warnung an `Startzeit`/`Endzeit` in `ddTischePanel.Items`? → melden (U-V3).

**`ddTischePanel.Items`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen** · Herkunft: K v2 C1, P4 Gesperrt, P4 Gesperrt

```
With(
  {
    datum: dpDatumTischePanel.SelectedDate;
    startZeit: Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0);
    endeZeit: Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0);
    bisRoh: If(varWiederholen; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate)
  };
  With(
    { bis: If(bisRoh > datum + 14; datum + 14; bisRoh) };
    With(
      {
        termine: ForAll(
          Filter(
            ForAll(Sequence(If(bis < datum; 0; DateDiff(datum; bis; TimeUnit.Days) + 1); 0); DateAdd(datum; Value; TimeUnit.Days)) As D;
            !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
          ) As T;
          {Start: T.Value + startZeit; Ende: T.Value + endeZeit}
        )
      };
      With(
        {
          belegtListe: If(
            varZeigeTischBuchungForm;
            ForAll(
              Filter(
                Tischbuchungen;
                Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(varWiederholen && dpWiederholenBis_1.SelectedDate > dpDatumTischePanel.SelectedDate; Min(DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days); 14); 0) + 1; TimeUnit.Days) && Endzeit > dpDatumTischePanel.SelectedDate
              );
              {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit}
            );
            FirstN(Table({TischName: ""; Beginn: Now(); Schluss: Now()}); 0)
          )
        };
        SortByColumns(
          Filter(
            ForAll(
              Tische As Ti;
              With(
                { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegtListe; TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
                {
                  Titel: Ti.Titel;
                  Gesperrt: Ti.Gesperrt;
                  ID: Ti.ID;
                  Belegt: n;
                  Etage: If(Ti.Geschoss.Value = varAusgewaehltesStockwerk; 0; 1);
                  Schluessel: Ti.Geschoss.Value & Left(Ti.Titel; Len(Ti.Titel) - Len(Last(Split(Ti.Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Ti.Titel; " ")).Value); 0); "000");
                  Anzeige: Ti.Titel & If(n = 0; ""; "  (an " & n & " von " & CountRows(termine) & " Tagen belegt)")
                }
              )
            );
            !Gesperrt && !("big table" in Lower(Titel)) && (Belegt = 0 || Belegt < CountRows(termine))
          );
          "Belegt"; SortOrder.Ascending;
          "Etage"; SortOrder.Ascending;
          "Schluessel"; SortOrder.Ascending
        )
      )
    )
  )
)
```

**`ddTischePanel.Items.Value`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen** · Herkunft: K v2 C1
(rechts im Eigenschaftenbereich „Wert“ auswählen, kein Formelfeld)

```
Anzeige
```

**`ddTischePanel.AllowEmptySelection`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **neu setzen** · Herkunft: K v2 C1

```
true
```

**`ddTischePanel.Default`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **neu setzen** · Herkunft: K v2 C1

```
Blank()
```

### G10 Knöpfe 5 Std / 9 Std

**Problem (belegt):** „5 Std“/„9 Std“ rechneten an anderen Tagen ab der aktuellen Uhrzeit (sinnlos) und waren ohne gewählten Tisch gesperrt. Mit „erst Zeit, dann Tisch“ ist das falsch herum. Bei geschlossenem Panel fragten sie trotzdem ab. `CountRows(Filter(…))` erzeugte Delegierungswarnungen.
**Lösung:** Heute ab der nächsten halben Stunde (nicht vor 06:00), an anderen Tagen ab 08:00. Ohne Tisch bedienbar, mit Tisch nur, wenn er frei ist (`LookUp(…).ID`, delegierbar). Bei geschlossenem Panel keine Abfrage. Farbe und Bedienbarkeit rechnen mit dem Öffnungszeitpunkt.
**Test:** Morgen → „5 Std“ → 08:00–13:00. Heute nach 17:00 → „5 Std“ grau. Tisch gewählt, der in den nächsten 5 Std belegt ist → grau.

**`btn5Std.DisplayMode`** · Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · Herkunft: K v2 C3, 06:00 + Öffnungszeitpunkt

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde;
      DisplayMode.Disabled;
      If(
        IsBlank(ddTischePanel.Selected.Titel);
        DisplayMode.Edit;
        If(
          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

**`btn5Std.Fill`** · Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · Herkunft: K v2 C3, 06:00 + Öffnungszeitpunkt

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btn5Std.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · Herkunft: K v2 C3, 06:00

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 5 };
  With(
    { minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(); Max(6 * 60; 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0)); 8 * 60) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 5 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 5));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

**`btn9Std.DisplayMode`** · Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · Herkunft: K v2 C4, 06:00 + Öffnungszeitpunkt

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde;
      DisplayMode.Disabled;
      If(
        IsBlank(ddTischePanel.Selected.Titel);
        DisplayMode.Edit;
        If(
          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

**`btn9Std.Fill`** · Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · Herkunft: K v2 C4, 06:00 + Öffnungszeitpunkt

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 9;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btn9Std.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · Herkunft: K v2 C4, 06:00

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 9 };
  With(
    { minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(); Max(6 * 60; 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0)); 8 * 60) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 9 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 9));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

### G11 Hinweistext Wiederholung im Panel

**Problem (belegt):** Text und Farbe des Hinweises „*Zu weit gewählt“ im Panel rechneten mit dem Datum des **Buchungsdialogs** (`dpDatum`) statt des Panels.
**Lösung:** beide auf `dpDatumTischePanel`.
**Test:** Panel → Wiederholen → Bis-Datum 3 Wochen später → roter Hinweis.

**`Label14.Text`** · Ort: `Screen1 > conTischBuchungenPanel > Label14` · **ganze Property ersetzen** · Herkunft: K v2 C5

```
If(
  DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
  "*Zu weit gewählt —      es werden 2 Wochen gespeichert";
  "*Wiederholung nur für max. 2 Wochen möglich"
)
```

**`Label14.Color`** · Ort: `Screen1 > conTischBuchungenPanel > Label14` · **ganze Property ersetzen** · Herkunft: K v2 C5

```
If(
  DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
  ColorValue("#EB3951");
  RGBA(50; 49; 48; 1)
)
```

### G12 Kleine Korrekturen

**Problem (belegt):** (1) Ein Stockwerkwechsel setzte die Dauer auf `0` statt leer (BD-12). (2) Die vier Aktualisieren-Stellen meldeten „Aktualisiert.“ auch dann, wenn das Laden scheiterte, und überdeckten die Warnung (BD-10). (3) Im Panel stand „schließen“ doppelt im Code (BD-25).
**Lösung:** leer statt `0`. „Aktualisiert.“ nur bei Erfolg. Doppelte Zeile weg.
**Test:** Aktualisieren → „Aktualisiert.“. WLAN aus → nur die gelbe Warnung.

**`ddStockwerk.OnSelect`** · Ort: `Screen1 > conGrundriss > ddStockwerk` · **ganze Property ersetzen** · Herkunft: K v2 D1

```
Set(varStockwerkDropdownOffen; true);;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedTisch; Blank());;
Set(varSelectedBuchung; Blank());;
Set(varAusgewaehltePlusDauer; Blank())

```

**`Icon1.OnSelect`** · Ort: `Screen1 > conBuchungen > Icon1` · **ganze Property ersetzen** · Herkunft: K v2 D2

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Icon1_1.OnSelect`** · Ort: `Screen1 > conDashboard > Icon1_1` · **ganze Property ersetzen** · Herkunft: K v2 D2

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Image6.OnSelect`** · Ort: `Screen1 > conHeader > Image6` · **ganze Property ersetzen** · Herkunft: K v2 D2

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnHitArea_1.OnSelect`** · Ort: `Screen1 > conHeader > btnHitArea_1` · **ganze Property ersetzen** · Herkunft: K v2 D2

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnAbbrechenTischePanel.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btnAbbrechenTischePanel` · **ganze Property ersetzen** · Herkunft: K v2 D4

```
Set(varZeigeTischBuchungForm; false);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel)
```

## 7. Phase 4: Grundriss und Dashboard

### G13 Grundriss: gesperrte Tische grau

**Problem:** Gesperrte Tische (G0.3) sahen im Grundriss aus wie freie.
**Lösung:** Gesperrte Kachel grau `#A6A6A6`, Kreis weiß. Das Antippen meldet „gesperrt“ (G7).
**Test:** Tisch in SharePoint sperren → in Studio Daten **Tische** aktualisieren bzw. App neu starten → Kachel grau.

**`Rectangle1.Fill`** · Ort: `Screen1 > conGrundriss > Gallery1 > Rectangle1` · **ganze Property ersetzen** · Herkunft: P4 Gesperrt

```
If(
  ThisItem.Gesperrt;
  ColorValue("#A6A6A6");
  With(
    {
      relevanteBuchung:
        If(
          varAnsichtsDatum = Today();
          LookUp(colGrundriss; TischName = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
          LookUp(colGrundriss; TischName = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
        )
    };
    If(
      IsBlank(relevanteBuchung);
      ColorValue("#00A96B");
      If(
        relevanteBuchung.Eingecheckt;
        ColorValue("#EB3951");
        ColorValue("#FFA500")
      )
    )
  )
)
```

**`Circle1.Fill`** · Ort: `Screen1 > conGrundriss > Gallery1 > Circle1` · **ganze Property ersetzen** · Herkunft: P4 Gesperrt

```
If(
  ThisItem.Gesperrt;
  Color.White;
  With(
    {
      relevanteBuchung:
        If(
          varAnsichtsDatum = Today();
          LookUp(colGrundriss; TischName = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
          LookUp(colGrundriss; TischName = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
        )
    };
    If(IsBlank(relevanteBuchung); ColorValue("#4DC398"); Color.White)
  )
)
```

### G14 Grundriss: freie Zeit an belegten Tischen buchen

**Problem (belegt):** Ist ein Tisch zu **irgendeiner** Zeit des Tages belegt (bei anderen Tagen) oder gerade belegt (heute), öffnet die Kachel nur das Details-Popup. Die freien Stunden des Tisches waren über den Grundriss nicht buchbar. Und im Buchungsdialog sah man nicht, wann der Tisch belegt ist.
**Lösung:**
- Ins Details-Popup kommt ein Knopf **„Andere Zeit buchen“**. Er öffnet den normalen Buchungsdialog für diesen Tisch, mit denselben frischen Eingaben wie G7.
- Im Buchungsdialog steht neu **„Belegt: 08:00–10:00, 14:00–17:00“** bzw. „An diesem Tag noch frei.“, aus den schon geladenen Grundriss-Daten (keine neue Abfrage). Die Zeile verschwindet, wenn im Dialog ein anderes Datum gewählt wird.
- Das Popup wird 46 px höher. Speichern prüft wie immer am Server (G6).

**Neue Steuerelemente anlegen:**
1. `conDetailsPopup` wählen → **Einfügen → Schaltfläche** (klassisch) → **`btnAndereZeit`**.
2. `conBuchungDialog` wählen → **Einfügen → Textbeschriftung** → **`lblBelegtHeute`**.

**Test:** Tisch heute 08:00–10:00 buchen (oder einen belegten wählen) → Kachel → Popup → „Andere Zeit buchen“ → Dialog zeigt „Belegt: 08:00–10:00“ → 13:00–17:00 buchen → klappt.

Neue Steuerelemente (zuerst anlegen, Name exakt so): `btnAndereZeit` (Button (Einfügen → Schaltfläche, klassisch), in `conDetailsPopup` einfügen), `lblBelegtHeute` (Label (Einfügen → Textbeschriftung), in `conBuchungDialog` einfügen)

**`conDetailsPopup.Height`** · Ort: `Screen1 > conDetailsPopup` · **ganze Property ersetzen** · Herkunft: P1 neu

```
200
```

**`Image7.Height`** · Ort: `Screen1 > conDetailsPopup > Image7` · **ganze Property ersetzen** · Herkunft: P1 neu

```
Parent.Height
```

**`btnAndereZeit.Text`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
"Andere Zeit buchen"
```

**`btnAndereZeit.X`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
25
```

**`btnAndereZeit.Y`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
152
```

**`btnAndereZeit.Width`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
210
```

**`btnAndereZeit.Height`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
36
```

**`btnAndereZeit.Size`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
12
```

**`btnAndereZeit.Fill`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
ColorValue("#171496")
```

**`btnAndereZeit.Color`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
Color.White
```

**`btnAndereZeit.HoverFill`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
ColorFade(Self.Fill; -20%)
```

**`btnAndereZeit.PressedFill`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
ColorFade(Self.Fill; -30%)
```

**`btnAndereZeit.PressedColor`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
Color.White
```

**`btnAndereZeit.Visible`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
!varDetailsTisch.Gesperrt
```

**`btnAndereZeit.OnSelect`** · Ort: `(neu) conDetailsPopup > btnAndereZeit` · **neu setzen** · Herkunft: P1 neu

```
Set(varSelectedTisch; varDetailsTisch);;
Set(varDialogJetzt; Now());;
Reset(dpDatum);;
Reset(ddStart);;
Reset(ddEnde);;
Reset(dpWiederholenBis);;
Set(varZeigeDialog; true);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false)
```

**`lblBelegtHeute.Text`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
With(
  { belegt: SortByColumns(Filter(colGrundriss; TischName = varSelectedTisch.Titel && Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)); "Startzeit"; SortOrder.Ascending) };
  If(IsEmpty(belegt); "An diesem Tag noch frei."; "Belegt: " & Concat(belegt; Text(Startzeit; "hh:mm") & "–" & Text(Endzeit; "hh:mm"); ", "))
)
```

**`lblBelegtHeute.Visible`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
varZeigeDialog && dpDatum.SelectedDate = varAnsichtsDatum
```

**`lblBelegtHeute.X`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
270
```

**`lblBelegtHeute.Y`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
110
```

**`lblBelegtHeute.Width`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
165
```

**`lblBelegtHeute.Height`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
150
```

**`lblBelegtHeute.Size`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
11
```

**`lblBelegtHeute.VerticalAlign`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
VerticalAlign.Top
```

**`lblBelegtHeute.Color`** · Ort: `(neu) conBuchungDialog > lblBelegtHeute` · **neu setzen** · Herkunft: P1 neu

```
RGBA(32; 54; 71; 1)
```

### G15 Details-Popup: Status wie Kachel

**Problem (belegt):** Das Popup zeigte immer „Besetzt“ in Rot, auch wenn die Kachel orange ist (gebucht, nicht eingecheckt).
**Lösung:** „Eingecheckt“ rot oder „Gebucht“ orange, wie die Kachel.
**Test:** Orange Kachel → „Gebucht“. Rote Kachel → „Eingecheckt“.

**`lblStatus.Text`** · Ort: `Screen1 > conDetailsPopup > lblStatus` · **ganze Property ersetzen** · Herkunft: L L6

```
If(varSelectedBuchung.CheckedIn; "Eingecheckt"; "Gebucht")
```

**`lblStatus.Color`** · Ort: `Screen1 > conDetailsPopup > lblStatus` · **ganze Property ersetzen** · Herkunft: L L6

```
If(varSelectedBuchung.CheckedIn; ColorValue("#EB3951"); ColorValue("#FFA500"))
```

### G16 Dashboard-Liste nach Uhrzeit

**Problem (belegt/geschlussfolgert):** „Meine Tischbuchungen“ im Dashboard war nicht nach Uhrzeit sortiert. Der Check-in-Dialog berechnet seine Position aus der Reihenfolge.
**Lösung:** Nach Startzeit sortieren. Die Position des Check-in-Dialogs rechnet mit derselben Reihenfolge.
**Test:** Erst eine Buchung für 14:00, dann eine für 08:00 anlegen → 08:00 steht oben. Einchecken bei der unteren → Dialog auf Höhe der richtigen Zeile.

**`galTischbuchungenHeute.Items`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute` · **ganze Property ersetzen** · Herkunft: L L2

```
SortByColumns(
  Filter(
    Tischbuchungen;
    Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
  );
  "Startzeit";
  SortOrder.Ascending
)
```

**`conCheckinDialog.Y`** · Ort: `Screen1 > conCheckinDialog` · **ganze Property ersetzen** · Herkunft: L L2

```
With(
        { _idx: CountRows(Filter(galTischbuchungenHeute.AllItems; Startzeit < varSelectedBuchung.Startzeit || (Startzeit = varSelectedBuchung.Startzeit && ID < varSelectedBuchung.ID))) + 1 };
            conDashboard.Y + galTischbuchungenHeute.Y + (_idx - galTischbuchungenHeute.VisibleIndex) * galTischbuchungenHeute.TemplateHeight + (galTischbuchungenHeute.TemplateHeight - Self.Height) / 2
            )
```

## 8. Phase 5: Einheitliche Optik
Die App wirkte wie aus zwei Apps zusammengesetzt (belegt): Der Buchungsdialog nutzt das Standard-Graublau von Power Apps, das Panel das Markenblau. Speichern war mal grün, mal blau. Stornieren sah aus wie Speichern. Gedrückte Knöpfe waren unlesbar. Der aktive Tab war unsichtbar. Deutsch und Englisch waren gemischt. Diese Schritte ändern **nur Aussehen und Texte**, kein Verhalten.

### G17 Gedrückte Knöpfe lesbar

**Problem (belegt):** Bei 7 Knöpfen ist die Schrift im gedrückten Zustand unsichtbar (schwarz auf schwarz bzw. grün auf grün).
**Lösung:** Gedrückt dunkelgrau mit weißer Schrift.
**Test:** Knöpfe gedrückt halten: Die Schrift bleibt lesbar.

**`btnAbbrechen.PressedColor`** · Ort: `Screen1 > conBuchungDialog > btnAbbrechen` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

**`btnAbbrechen.PressedFill`** · Ort: `Screen1 > conBuchungDialog > btnAbbrechen` · **ganze Property ersetzen** · Herkunft: L L3

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen2.PressedColor`** · Ort: `Screen1 > conCheckinDialog > btnSchließen2` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

**`btnSchließen2.PressedFill`** · Ort: `Screen1 > conCheckinDialog > btnSchließen2` · **ganze Property ersetzen** · Herkunft: L L3

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen3.PressedColor`** · Ort: `Screen1 > conDetailsPopup > btnSchließen3` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

**`btnSchließen3.PressedFill`** · Ort: `Screen1 > conDetailsPopup > btnSchließen3` · **ganze Property ersetzen** · Herkunft: L L3

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen4.PressedColor`** · Ort: `Screen1 > conVerwaltenDialog > btnSchließen4` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

**`btnSchließen4.PressedFill`** · Ort: `Screen1 > conVerwaltenDialog > btnSchließen4` · **ganze Property ersetzen** · Herkunft: L L3

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen4_1.PressedColor`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnSchließen4_1` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

**`btnSchließen4_1.PressedFill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnSchließen4_1` · **ganze Property ersetzen** · Herkunft: L L3

```
ColorFade(Color.Black; 30%)
```

**`btnSchließenKlein.PressedColor`** · Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnSchließenKlein` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

**`btnSchließenKlein.PressedFill`** · Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnSchließenKlein` · **ganze Property ersetzen** · Herkunft: L L3

```
ColorFade(Color.Black; 30%)
```

**`btnSpeichern.PressedColor`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen** · Herkunft: L L3

```
Color.White
```

### G18 Aktiver Tab sichtbar

**Problem (belegt):** Beide Tabs haben immer dieselbe Farbe.
**Lösung:** Aktiver Tab dunkelblau, inaktiver hellblau (35 %, Kontrast ok).
**Test:** Tabs wechseln.

**`btnTabDashboard.Fill`** · Ort: `Screen1 > conHeader > btnTabDashboard` · **ganze Property ersetzen** · Herkunft: L L4

```
If(varAktiverTab = "dashboard"; ColorValue("#171496"); ColorFade(ColorValue("#171496"); 35%))
```

**`btnTabBuchungen.Fill`** · Ort: `Screen1 > conHeader > btnTabBuchungen` · **ganze Property ersetzen** · Herkunft: L L4

```
If(varAktiverTab = "buchungen"; ColorValue("#171496"); ColorFade(ColorValue("#171496"); 35%))
```

### G19 Profilfarbe fest

**Problem (belegt):** Die Profilfarbe wurde bei jedem Start zufällig gewählt.
**Lösung:** Die Farbe ergibt sich aus der E-Mail-Adresse und ist damit immer gleich. `varProfilFarbe` in OnStart bleibt ungenutzt stehen (harmlos).
**Test:** Zweimal starten: gleiche Farbe.

**`Circle2.Fill`** · Ort: `Screen1 > conHeader > Circle2` · **ganze Property ersetzen** · Herkunft: L L5

```
Switch(
  Mod(Len(User().Email); 8) + 1;
  1; ColorValue("#8CAFF4");
  2; ColorValue("#82C7B3");
  3; ColorValue("#EFA897");
  4; ColorValue("#B59EDC");
  5; ColorValue("#82CCC5");
  6; ColorValue("#F5C295");
  7; ColorValue("#A1AADB");
  ColorValue("#A1B1BA")
)
```

### G20 Buchungsdialog im selben Design wie das Panel

**Problem (belegt):** Im Buchungsdialog sind die Schalter, Pfeile und Kalender graublau, Speichern ist grün. Im Panel ist alles markenblau, die Schalter grün.
**Lösung:** Der Dialog sieht aus wie das Panel: Schalter grün, Pfeile und Kalender blau, Speichern blau, Auswahlmodus blau.
**Test:** Kachel → Dialog sieht aus wie das Panel.

**`tglTagMo.TrueFill`** · Ort: `Screen1 > conBuchungDialog > tglTagMo` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#00A96B")
```

**`tglTagDi.TrueFill`** · Ort: `Screen1 > conBuchungDialog > tglTagDi` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#00A96B")
```

**`tglTagMi.TrueFill`** · Ort: `Screen1 > conBuchungDialog > tglTagMi` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#00A96B")
```

**`tglTagDo.TrueFill`** · Ort: `Screen1 > conBuchungDialog > tglTagDo` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#00A96B")
```

**`tglTagFr.TrueFill`** · Ort: `Screen1 > conBuchungDialog > tglTagFr` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#00A96B")
```

**`dpDatum.IconBackground`** · Ort: `Screen1 > conBuchungDialog > dpDatum` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#171496")
```

**`dpWiederholenBis.IconBackground`** · Ort: `Screen1 > conBuchungDialog > dpWiederholenBis` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#171496")
```

**`ddStart.ChevronBackground`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#171496")
```

**`ddStart.HoverFill`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorFade(Self.Fill; -20%)
```

**`ddEnde.ChevronBackground`** · Ort: `Screen1 > conBuchungDialog > ddEnde` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#171496")
```

**`ddEnde.HoverFill`** · Ort: `Screen1 > conBuchungDialog > ddEnde` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorFade(Self.Fill; -20%)
```

**`btnSpeichern.Fill`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#171496")
```

**`btnSpeichern.PressedFill`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorFade(Self.Fill; -20%)
```

**`tglAuswahlModus.TrueFill`** · Ort: `Screen1 > conBuchungen > tglAuswahlModus` · **ganze Property ersetzen** · Herkunft: L L7

```
ColorValue("#171496")
```

### G21 Stornieren rot

**Problem:** Stornieren (gefährlich) sah aus wie Speichern (blau) und steht im Tab direkt daneben.
**Lösung:** Stornieren rot.
**Test:** Verwalten-Dialoge ansehen.

**`btnStornieren.Fill`** · Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **ganze Property ersetzen** · Herkunft: L L8

```
ColorValue("#EB3951")
```

**`btnStornieren_1.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **ganze Property ersetzen** · Herkunft: L L8

```
ColorValue("#EB3951")
```

**`btnStornierenKlein.Fill`** · Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein` · **ganze Property ersetzen** · Herkunft: L L8

```
ColorValue("#EB3951")
```

### G22 Texte einheitlich Deutsch

**Problem (belegt):** Englische und uneinheitliche Texte: „My personal desk“, „Tisch Buchen“, „+1Std“, „-2std“, „Tisch OG Desk 5“, „---“, „-Keine Einträge-“, verschiedene Titelformen.
**Lösung:** Einheitlich deutsch: „Meine Tischbuchungen“, „Tisch buchen“, „+1 Std“, „−1 Std“, Titel „Verwalten: OG Desk 5“ bzw. nur der Tischname, leere Listen „Keine Buchungen“.
**Test:** Texte durchsehen. Werden „+1 Std“ und ähnliche Texte abgeschnitten, bei diesen Knöpfen `Size` um 1 verkleinern (UNSICHER).

**`lblMyPersonalDesk.Text`** · Ort: `Screen1 > conDashboard > lblMyPersonalDesk` · **ganze Property ersetzen** · Herkunft: L L9

```
"Meine Tischbuchungen"
```

**`btnTischHinzufügen.Text`** · Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen** · Herkunft: L L9

```
"Tisch buchen"
```

**`lblTischeBuchenPanel.Text`** · Ort: `Screen1 > conTischBuchungenPanel > lblTischeBuchenPanel` · **ganze Property ersetzen** · Herkunft: L L9

```
"Tisch buchen"
```

**`btnPlus1Std.Text`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus1Std` · **ganze Property ersetzen** · Herkunft: L L9

```
"+1 Std"
```

**`btnPlus2Std.Text`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus2Std` · **ganze Property ersetzen** · Herkunft: L L9

```
"+2 Std"
```

**`btnPlus3Std.Text`** · Ort: `Screen1 > conVerwaltenDialog > btnPlus3Std` · **ganze Property ersetzen** · Herkunft: L L9

```
"+3 Std"
```

**`btnPlus1Std_1.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus1Std_1` · **ganze Property ersetzen** · Herkunft: L L9

```
"+1 Std"
```

**`btnPlus2Std_1.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus2Std_1` · **ganze Property ersetzen** · Herkunft: L L9

```
"+2 Std"
```

**`btnPlus3Std_1.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus3Std_1` · **ganze Property ersetzen** · Herkunft: L L9

```
"+3 Std"
```

**`btnMinus1Std.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus1Std` · **ganze Property ersetzen** · Herkunft: L L9

```
"−1 Std"
```

**`btnMinus2Std.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus2Std` · **ganze Property ersetzen** · Herkunft: L L9

```
"−2 Std"
```

**`btnMinus3std.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus3std` · **ganze Property ersetzen** · Herkunft: L L9

```
"−3 Std"
```

**`lblTischLeer.Text`** · Ort: `Screen1 > conDashboard > lblTischLeer` · **ganze Property ersetzen** · Herkunft: L L9

```
"Keine Buchungen"
```

**`lblTischLeer_1.Text`** · Ort: `Screen1 > conBuchungen > lblTischLeer_1` · **ganze Property ersetzen** · Herkunft: L L9

```
"Keine Buchungen"
```

**`lblTitel3.Text`** · Ort: `Screen1 > conVerwaltenDialog > lblTitel3` · **ganze Property ersetzen** · Herkunft: L L9

```
If(IsBlank(varSelectedBuchung); ""; varSelectedBuchung.Tisch.Value)
```

**`lblTitel3_1.Text`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > lblTitel3_1` · **ganze Property ersetzen** · Herkunft: L L9

```
"Verwalten: " & varSelectedBuchungTab.Tisch.Value
```

**`lblTitel2.Text`** · Ort: `Screen1 > conDetailsPopup > lblTitel2` · **ganze Property ersetzen** · Herkunft: L L9

```
varSelectedBuchung.Tisch.Value
```

**`lblTischHeute.Text`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblTischHeute` · **ganze Property ersetzen** · Herkunft: L L9

```
ThisItem.Tisch.Value
```

### G23 Auswahl- und Trennlinienfarben

**Problem (belegt):** Auswahlbalken, markierte Listenzeilen, Pfeil-Hover und Trennlinien sind graublau statt blau. Beim Hover springt ein blauer Pfeil auf Graublau.
**Lösung:** alles Markenblau. Pfeil beim Hover dunkler blau.
**Test:** Liste öffnen, Zeile markieren, über den Pfeil fahren.

**`Rectangle3_2.Fill`** · Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > Rectangle3_2` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`Rectangle5.Fill`** · Ort: `Screen1 > conBuchungDialog > Rectangle5` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`Rectangle6.Fill`** · Ort: `Screen1 > conBuchungDialog > Rectangle6` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`Rectangle6_1.Fill`** · Ort: `Screen1 > conCheckinDialog > Rectangle6_1` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`Rectangle6_2.Fill`** · Ort: `Screen1 > conDetailsPopup > Rectangle6_2` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddStockwerk.SelectionFill`** · Ort: `Screen1 > conGrundriss > ddStockwerk` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddTischePanel.SelectionFill`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddStartTischePanel.SelectionFill`** · Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddEndTischePanel.SelectionFill`** · Ort: `Screen1 > conTischBuchungenPanel > ddEndTischePanel` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddStart.SelectionFill`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddEnde.SelectionFill`** · Ort: `Screen1 > conBuchungDialog > ddEnde` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorValue("#171496")
```

**`ddTischePanel.ChevronHoverBackground`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddStartTischePanel.ChevronHoverBackground`** · Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddEndTischePanel.ChevronHoverBackground`** · Ort: `Screen1 > conTischBuchungenPanel > ddEndTischePanel` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddStart.ChevronHoverBackground`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddEnde.ChevronHoverBackground`** · Ort: `Screen1 > conBuchungDialog > ddEnde` · **ganze Property ersetzen** · Herkunft: L L10

```
ColorFade(Self.ChevronBackground; -20%)
```

### G24 Einheitlicher Hover auf Klickflächen

**Problem (belegt):** Fünf unsichtbare Klickflächen dunkeln beim Hover verschieden stark ab (4–20 %).
**Lösung:** einheitlich 10 %.
**Test:** über Kachel, Einchecken, Verwalten-Pfeile und Logo fahren.

**`btnHitArea.HoverFill`** · Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen** · Herkunft: L L11

```
RGBA(0; 0; 0; 0,1)
```

**`btnEincheckenHeute.HoverFill`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute` · **ganze Property ersetzen** · Herkunft: L L11

```
RGBA(0; 0; 0; 0,1)
```

**`btnVerwalten.HoverFill`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten` · **ganze Property ersetzen** · Herkunft: L L11

```
RGBA(0; 0; 0; 0,1)
```

**`btnVerwalten_2.HoverFill`** · Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2` · **ganze Property ersetzen** · Herkunft: L L11

```
RGBA(0; 0; 0; 0,1)
```

**`btnHitArea_1.HoverFill`** · Ort: `Screen1 > conHeader > btnHitArea_1` · **ganze Property ersetzen** · Herkunft: L L11

```
RGBA(0; 0; 0; 0,1)
```

## 9. Phase 6: Raumcode ruhigstellen (bleibt erhalten)

### G25 Raumcode ruhigstellen (bleibt erhalten)

**Problem (gemessen/belegt):** Der ausgeblendete Raumcode fragt beim App-Start trotzdem ab (36 Abfragen, darunter die langsamsten). Du willst ihn behalten.
**Lösung:** Der Code bleibt vollständig erhalten. Er wird nur hinter eine Bedingung gestellt: Er rechnet erst, wenn das Raum-Panel bzw. die Raumbestätigung offen ist (`varZeigeRaumBuchungForm`/`varZeigeRaumBestätigung`). Die Raum-Galerien sind dann leer, also rechnen auch ihre Knöpfe und Labels nicht.
**Zurückholen:** jeweils die äußere Bedingung entfernen (Original in Anhang A).
**Test:** App starten: unverändert. Optional mit dem Monitor: keine Abfragen mehr auf `Raumbuchungen` und `Räume` beim Start.

**`galRäume.Items`** · Ort: `Screen1 > conRaumBuchungenPanel > galRäume` · **ganze Property ersetzen** · Herkunft: Raum ruhig

```
If(
  varZeigeRaumBuchungForm;
  With(
    { basisStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value; 2)); Value(Mid(ddBeginnRaumPanel.Selected.Value; 4; 2)); 0) };
    Filter(
      Räume As R;
      CountRows(
        Filter(
          Table({Offset: 0}; {Offset: 30}; {Offset: 60}; {Offset: 90}) As Slot;
          With(
            { slotStart: DateAdd(basisStart; Slot.Offset; TimeUnit.Minutes) };
            With(
              { slotEnde: DateAdd(slotStart; 30; TimeUnit.Minutes) };
              CountRows(Filter(Raumbuchungen; Raum.Value = R.Titel && Startzeit < slotEnde && Endzeit > slotStart)) = 0
            )
          )
        )
      ) > 0
    )
  )
)
```

**`galRaumbuchungenHeute.Items`** · Ort: `Screen1 > conDashboard > galRaumbuchungenHeute` · **ganze Property ersetzen** · Herkunft: Raum ruhig

```
If(
  varZeigeRaumBuchungForm;
  Filter(Raumbuchungen; Person.Email = User().Email && Startzeit >= Today() && Startzeit < DateAdd(Today(); 1; TimeUnit.Days) && Endzeit >= Now())
)
```

**`recBuchungDavor1.Visible`** · Ort: `Screen1 > conRaumBestätigen > recBuchungDavor1` · **ganze Property ersetzen** · Herkunft: Raum ruhig

```
varZeigeRaumBestätigung && CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes))) > 0
```

**`recBuchungDanach1.Visible`** · Ort: `Screen1 > conRaumBestätigen > recBuchungDanach1` · **ganze Property ersetzen** · Herkunft: Raum ruhig

```
varZeigeRaumBestätigung && CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes))) > 0
```

**`Label4.Text`** · Ort: `Screen1 > conRaumBestätigen > Label4` · **ganze Property ersetzen** · Herkunft: Raum ruhig

```
If(
  varZeigeRaumBestätigung;
  With(
    {
      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
      fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes)
    };
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
      If(
        IsBlank(buchung);
        "";
        If(
          recBuchungDanach1.Width < 40;
          "";
          If(
            recBuchungDanach1.Width < 90;
            Left(First(Split(buchung.Person.DisplayName; " ")).Value; 1) & Left(Last(Split(buchung.Person.DisplayName; " ")).Value; 1);
            buchung.Person.DisplayName
          )
        )
      )
    )
  );
  ""
)
```

**`Label5.Text`** · Ort: `Screen1 > conRaumBestätigen > Label5` · **ganze Property ersetzen** · Herkunft: Raum ruhig

```
If(
  varZeigeRaumBestätigung;
  With(
    { fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes) };
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
      If(IsBlank(buchung); ""; buchung.Person.DisplayName)
    )
  );
  ""
)
```

## 10. Phase 7: Barrierefreiheit

### G26 Barrierefreiheit: Beschriftungen

**Problem (belegt):** 37 Steuerelemente ohne Beschriftung für Screenreader (App-Prüfung).
**Lösung:** `AccessibleLabel` mit kurzem deutschem Text. Das ändert nichts Sichtbares.
**Test:** App-Prüfung: Die Einträge „Fehlende Beschriftung“ verschwinden.

**`Image6.AccessibleLabel`** · Ort: `Screen1 > conHeader > Image6` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Aktualisieren"
```

**`dpDatumRaum.AccessibleLabel`** · Ort: `Screen1 > conRaumBuchungenPanel > dpDatumRaum` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Datum Raumbuchung"
```

**`ddBeginnRaumPanel.AccessibleLabel`** · Ort: `Screen1 > conRaumBuchungenPanel > ddBeginnRaumPanel` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Beginn Raumbuchung"
```

**`ddDauerRaumPanel.AccessibleLabel`** · Ort: `Screen1 > conRaumBuchungenPanel > ddDauerRaumPanel` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Dauer Raumbuchung"
```

**`galRäume.AccessibleLabel`** · Ort: `Screen1 > conRaumBuchungenPanel > galRäume` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Räume"
```

**`Icon1.AccessibleLabel`** · Ort: `Screen1 > conBuchungen > Icon1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Aktualisieren"
```

**`tglAuswahlModus.AccessibleLabel`** · Ort: `Screen1 > conBuchungen > tglAuswahlModus` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Mehrfachauswahl ein oder aus"
```

**`galAlleTischbuchungen.AccessibleLabel`** · Ort: `Screen1 > conBuchungen > galAlleTischbuchungen` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Meine Tischbuchungen"
```

**`dpAnsichtsDatum.AccessibleLabel`** · Ort: `Screen1 > conDashboard > dpAnsichtsDatum` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Angezeigtes Datum wählen"
```

**`Icon1_1.AccessibleLabel`** · Ort: `Screen1 > conDashboard > Icon1_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Aktualisieren"
```

**`galTischbuchungenHeute.AccessibleLabel`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Meine Buchungen am gewählten Tag"
```

**`galRaumbuchungenHeute.AccessibleLabel`** · Ort: `Screen1 > conDashboard > galRaumbuchungenHeute` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Meine Raumbuchungen"
```

**`ddTischePanel.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Tisch"
```

**`dpDatumTischePanel.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > dpDatumTischePanel` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Datum"
```

**`ddStartTischePanel.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Beginn"
```

**`ddEndTischePanel.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > ddEndTischePanel` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Ende"
```

**`tglTagMo_1.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > tglTagMo_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Montag"
```

**`tglTagDi_1.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > tglTagDi_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Dienstag"
```

**`dpWiederholenBis_1.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > dpWiederholenBis_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Wiederholen bis"
```

**`tglTagMi_1.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > tglTagMi_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Mittwoch"
```

**`tglTagDo_1.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > tglTagDo_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Donnerstag"
```

**`tglTagFr_1.AccessibleLabel`** · Ort: `Screen1 > conTischBuchungenPanel > tglTagFr_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Freitag"
```

**`ddStockwerk.AccessibleLabel`** · Ort: `Screen1 > conGrundriss > ddStockwerk` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Stockwerk"
```

**`imgGrundrissUG.AccessibleLabel`** · Ort: `Screen1 > conGrundriss > imgGrundrissUG` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Grundriss Untergeschoss"
```

**`Gallery1.AccessibleLabel`** · Ort: `Screen1 > conGrundriss > Gallery1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Tische im Grundriss"
```

**`Rectangle6_2.AccessibleLabel`** · Ort: `Screen1 > conDetailsPopup > Rectangle6_2` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Trennlinie"
```

**`Image1_4.AccessibleLabel`** · Ort: `Screen1 > conCheckinDialog > Image1_4` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Symbolbild"
```

**`Rectangle6_1.AccessibleLabel`** · Ort: `Screen1 > conCheckinDialog > Rectangle6_1` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Trennlinie"
```

**`dpDatum.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > dpDatum` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Datum"
```

**`ddStart.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > ddStart` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Beginn"
```

**`ddEnde.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > ddEnde` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Ende"
```

**`tglTagMo.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > tglTagMo` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Montag"
```

**`tglTagDi.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > tglTagDi` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Dienstag"
```

**`tglTagMi.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > tglTagMi` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Mittwoch"
```

**`tglTagDo.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > tglTagDo` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Donnerstag"
```

**`tglTagFr.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > tglTagFr` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Freitag"
```

**`dpWiederholenBis.AccessibleLabel`** · Ort: `Screen1 > conBuchungDialog > dpWiederholenBis` · **neu setzen** · Herkunft: Barrierefreiheit

```
"Wiederholen bis"
```

## 11. Phase 8: Handy-App

**Problem:**
- Die Handy-App startet heute an anderen Tagen um 08:00. Laut deiner Entscheidung soll ab 06:00 gebucht werden können.
- Eine **Auswahl-Vorgabe** fehlte, die Liste nahm einfach den ersten Eintrag. Mit 06:00 als erstem Eintrag würde an anderen Tagen 06:00 vorgeschlagen.

**Lösung:** Startliste ab 06:00 (heute ab der laufenden halben Stunde, nicht vor 06:00). Neue Vorgabe: heute die erste mögliche Zeit, an anderen Tagen **08:00**.
**Wo:** App **„Tischbuchung Handy“** in Studio öffnen (nicht die Desktop-App!). Steuerelement `ddStart`.
**Test:** Handy-Vorschau → morgen → Start 08:00 vorgeschlagen, Liste ab 06:00. Heute vor 06:00 öffnen (oder Datum heute) → erster Eintrag.
**Teilen (E11):** Danach veröffentlichen und **teilen** mit den Kollegen mit Firmenhandy: Datei → Teilen → Namen eingeben, **ohne** Mitbesitzer-Recht. Die App erscheint dann in **Power Apps Mobile**, die die Kollegen aus dem App Store installieren und sich mit dem Firmenkonto anmelden.
**UNSICHER:** Die Handy-App nutzt `Now()` in der Startliste und hat keinen Timer. Bleibt sie stundenlang offen, veraltet die Liste. Abhilfe: Datum kurz wechseln oder die App neu öffnen. Ein dauerhafter Fix (wie G7) gehört in ein eigenes kleines Handy-Paket.

**Handy-App `ddStart.Items`** · **ganze Property ersetzen**

```
With(
  { ab: If(ddDatum.Selected.Tag = Today(); Max(6 * 60; 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0)); 6 * 60) };
  ForAll(
    Sequence(Max(0; (21 * 60 + 30 - ab) / 30 + 1); 0) As n;
    {
      Value: Text(Time(RoundDown((ab + n.Value * 30) / 60; 0); Mod(ab + n.Value * 30; 60); 0); "hh:mm");
      Min: ab + n.Value * 30
    }
  )
)
```

**Handy-App `ddStart.Default`** · **neu setzen**

```
If(
  ddDatum.Selected.Tag = Today();
  With(
    { ab: Max(6 * 60; 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0)) };
    Text(Time(RoundDown(ab / 60; 0); Mod(ab; 60); 0); "hh:mm")
  );
  "08:00"
)
```

## 12. Phase 9: Test, Go-Live, Betrieb
### G-T Test mit 3–5 Kollegen (vor dem 14.10.)
1. **Vorher:** alle Phasen bis mindestens 4 eingefügt, veröffentlicht, Flow an, Rechte gesetzt.
2. **Ablauf (60–90 Min):** Jeder Kollege bucht nach Kurzanleitung:
   - eine Einzelbuchung über den Grundriss,
   - eine Serie Mo–Fr über das Panel,
   - einmal verlängern, einmal stornieren (mit Rückfrage), einmal einchecken.
3. **Gezielt:**
   - Zwei Kollegen buchen gleichzeitig denselben Tisch zur selben Zeit (einer bekommt „belegt“ oder die rote Gleichzeitig-Meldung).
   - Einer bucht und checkt **nicht** ein → nach 30 Minuten weg.
   - Einer versucht, im Browser eine fremde Buchung zu ändern → verboten.
4. **Notieren:** jede Meldung, die verwirrt, und jeder Fehlertext (Foto). Dauer gefühlt ok?
5. **Danach:** Export und Monitor-Trace an mich, ich werte aus.

### G-G Go-Live-Checkliste (13./14.10.)
- [ ] Alle Phasen 1–4 eingefügt, App-Prüfung ohne Formelfehler, veröffentlicht
- [ ] Flow „Freigabe ohne Check-in“ an, Aufräum-Flow an
- [ ] Rechte „nur eigene Elemente“ gesetzt und getestet
- [ ] Bestandsdaten geprüft (G0.2)
- [ ] App mit allen 30 Nutzern geteilt (Datei → Teilen, ggf. über eine Gruppe), Handy-App mit den Firmenhandy-Kollegen
- [ ] Michael ist Mitbesitzer von App, Listen und Flows, Betriebshandbuch übergeben
- [ ] Kurzanleitung (1 Seite) und Go-Live-Mail verschickt. Inhalt: Link zur App, „innerhalb von 30 Minuten nach Beginn einchecken“, Teams-Chat für Fehler
- [ ] GoBright-Tischanzeigen: Umgang geklärt (Abschnitt 12a)
- [ ] `.msapp`-Sicherung des Go-Live-Stands

### G-Z Rückfall (ohne GoBright)
Da GoBright am 14.10. endet, gibt es keinen Weg zurück dorthin. Rückfall heißt: **auf die letzte funktionierende Version der eigenen App**.
1. **Ein Schritt macht Probleme:** Original aus Anhang A einfügen, veröffentlichen.
2. **Ganze Phase:** Studio → **Versionsverlauf** → Version vor der Phase **wiederherstellen** → veröffentlichen.
3. **App komplett kaputt:** gesicherte `.msapp` (G0.1) importieren bzw. Version wiederherstellen.
4. **Flow löscht Falsches:** Flow ausschalten. Gelöschte Buchungen liegen 93 Tage im **Papierkorb** der SharePoint-Site (wiederherstellbar).
5. **Notbetrieb:** Buchungen direkt in der SharePoint-Liste `Tischbuchungen` anlegen (Tisch, Start, Ende, Person). Die App zeigt sie an.

### 12a. GoBright-Tischanzeigen und Gateway
**Recherche (belegt, Herstellerseiten, abgerufen 08.10.):** Das Gateway muss mit der GoBright-Plattform verbunden sein. Die Tischanzeigen („GoBright Connect“) brauchen eine **Lizenz pro Tisch**. Die GoBright-API ist ein Cloud-Dienst der Plattform. Lokal bietet das Gateway nur eine Aktivierungsseite (Port 8080), keine Steuerschnittstelle. Eine Anbindung an deine App ohne GoBright-Vertrag ist damit **nach allem, was öffentlich bekannt ist, nicht möglich**.
**Empfehlung:**
1. Mit dem Vertragsende **Anzeigen und Gateway ausschalten** bzw. ausstecken, damit sie keinen falschen Status zeigen (ein grünes Licht an einem gebuchten Tisch wäre schlimmer als gar keins).
2. Wer es genau wissen will: eine Mail an support@gobright.com mit der Frage, ob Gateway und Anzeigen ohne Plattform-Lizenz ansteuerbar sind.
3. **Ersatz für später:** **QR-Code am Tisch**, der die Handy-App mit diesem Tisch öffnet und einchecken lässt (Power Apps `Param("tisch")`). Das braucht ein kleines Handy-Paket, ist aber günstig und zuverlässig.

Quellen: [GoBright Connect](https://gobright.com/products/desk-booking-system/connect/), [Produktblatt Connect (PDF)](https://gobright.com/wp-content/uploads/2023/09/GoBright-Downloads-GoBright-Connect-Product-Information.pdf), [Gateway konfigurieren](https://support.gobright.com/hc/en-us/articles/360010138740-Configure-a-Gateway-Device), [API-Erweiterung](https://gobright.com/new-features-and-innovation/api-extension-to-extract-data-from-gobright/), [Gateway-Setup (Partner)](https://ascentae.magentrixcloud.com/articles/knowledgebase/GoBright-Gateway-Setup-10-5-2023).

## 13. Bewusst nicht im Plan (mit Grund)
| Vorhaben | Warum nicht jetzt | Nächster Schritt |
|---|---|---|
| Outlook-Einladung (P5) | braucht ein Funktionspostfach und Klärung mit Michael, zwei Flows und eine Spalte `KalenderID` | nach Michaels Antwort eigenes Paket |
| Koordinaten aus der Liste (P7) | Positionen sind von dir final bestätigt, ein Umzug in die Liste birgt Verschiebungsrisiko | nach dem Go-Live mit Screenshots |
| Eigene Umgebung/Lösung (P8) | IT-Thema | mit Michael |
| QR-Check-in am Tisch | Handy-Paket | nach dem Go-Live |
| Buchungen-Tab „manchmal leer“ | Ursache unbekannt | beim nächsten Auftreten Monitor-Trace aufnehmen |
| Mehrfach-Verlängern, Alternativtische | eigene Konzepte | bei Bedarf |
| Hover-Richtung vereinheitlichen, Grautöne, Farbtabelle | nur Optik, viele Properties | später in einem Zug |
| Tab-Reihenfolge (19 Hinweise der App-Prüfung) | geringe Wirkung | später |

## 14. UNSICHER (mit Test)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U-C1 | Behält die Tischauswahl die Auswahl, wenn sich die Zeit ändert? | Tisch neu wählen (lästig, nicht gefährlich) | G9 Test 4 |
| U-V3 | Wird die Abfrage der Tischliste delegiert? | Bei sehr vielen Buchungen zeigt die Liste einen belegten Tisch als frei, Speichern prüft trotzdem richtig | App-Prüfung nach G9 |
| U-B1 | `SerienID` wird beim Sammel-Patch geschrieben | falsche Meldung „nicht angekommen“ (keine Doppelbuchung) | G6 Test |
| U-R1 | `Reset` direkt nach `Set(varDialogJetzt; Now())` liefert die neue Startzeit | alte Startzeit | G7 Test 2 |
| U-F1 | Flow-Filter `Checkedin eq 0` | Flow findet nichts oder alles | G-F Test |
| U-S1 | Sperre gegen Doppelklick in der Desktop-App (in der Handy-App gemessen) | doppelte Aktion | Doppelklick-Tests G3, G6 |
| U-T1 | Timer mit `Refresh` alle 5 Min stört nicht | Flackern in Listen | G8 Test, Kollegentest |
| U-G1 | Spalte `Gesperrt` ist ohne „Daten aktualisieren“ unbekannt | rote Formeln in G6/G7/G9/G13/G14 | G0.3 Schritt 2 |
| U-H1 | Handy-Vorgabe „08:00“ greift (Default-Text passt zur Liste) | Vorschlag 06:00 | Phase 8 Test |
| U-Z1 | Zeitumstellung 25.10. (Sonntag) | Buchungen am Sonntag selbst eine Stunde verschoben | sehr selten, keine Aktion |

## 15. Testbogen
| ☐ | Schritt | Ergebnis | Notiz |
|---|---|---|---|
| ☐ | G0.1–G0.4 Vorbereitung | | |
| ☐ | G1 OnStart | | |
| ☐ | G2 Verwalten (inkl. B0-Test) | | |
| ☐ | G3 Verlängern (inkl. Doppelklick, zwei Tabs) | | |
| ☐ | G4 Stornieren mit Rückfrage (alle drei Wege) | | |
| ☐ | G5 Einchecken (Fenster) | | |
| ☐ | G6 Speichern (Einzel, Serie, Person, gesperrt, Vergangenheit, Doppelklick, SerienID) | | |
| ☐ | G7 Frische Eingaben, 06:00, 21:30, gesperrte Kachel | | |
| ☐ | G-F Flow Freigabe | | |
| ☐ | G8 Timer | | |
| ☐ | G-R Rechte | | |
| ☐ | G9–G12 Panel | | |
| ☐ | G13–G16 Grundriss/Dashboard | | |
| ☐ | G17–G24 Optik | | |
| ☐ | G25 Raumcode ruhig | | |
| ☐ | G26 Barrierefreiheit | | |
| ☐ | Phase 8 Handy-App, geteilt | | |
| ☐ | G-T Kollegentest | | |
| ☐ | App-Prüfung: vorher 134 Einträge, nachher ___ (erwartet deutlich weniger: ~47 Delegations- und 37 Beschriftungs-Hinweise fallen weg) | | |

## Anhang A: Originale für den Rückfall (Export 07.10.)

Properties, die es vorher nicht gab: leeren bzw. auf Standard setzen. Neue Steuerelemente: löschen.

**`App.OnStart`** (Schritt G1)

```
Set(varSelectedTisch; Blank());;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedBuchung; Blank());;
Set(varAktiverTab; "dashboard");;
Set(varZeigeRaumBuchungForm; false);;
Set(varAusgewähltRaum; Blank());;
Set(varAusgewählteStartzeit; Blank());;
Set(varAusgewählteEndzeit; Blank());;
Set(varZeigeRaumBestätigung; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varWiederholenBis; Today() + 14);;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeRaumInfo; false);;
Set(varZeigeRaumVerwalten; false);;
Set(
  varProfilFarbe;
  Switch(
    RandBetween(1; 8);
    1; ColorValue("#8CAFF4");
    2; ColorValue("#82C7B3");
    3; ColorValue("#EFA897");
    4; ColorValue("#B59EDC");
    5; ColorValue("#82CCC5");
    6; ColorValue("#F5C295");
    7; ColorValue("#A1AADB");
    ColorValue("#A1B1BA")
  )
);;
Set(varZoom; 1);;
Set(varPanX; 0);;
Set(varPanY; 0);;
Set(varWiederholenBisGewaehlt; false);;
ClearCollect(
  colTischPositionen;
  {Tisch: "OG Desk 1"; X: 1380; Y: 270; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 2"; X: 1629; Y: 290; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 3"; X: 1732; Y: 288; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 4"; X: 1629; Y: 348; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 5"; X: 1732; Y: 346; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 6"; X: 1734; Y: 536; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 7"; X: 1734; Y: 596; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 8"; X: 1500; Y: 484; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 9"; X: 1500; Y: 584; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 10"; X: 1500; Y: 683; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 11"; X: 1560; Y: 468; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 12"; X: 1560; Y: 582; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 13"; X: 1560; Y: 681; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 3"; X: 870; Y: 687; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 2"; X: 870; Y: 594; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 1"; X: 870; Y: 501; Ausrichtung: "Vertikal"}
);;
Set(varSelectedBuchungTab; Blank());;
Set(varZeigeVerwaltenTab; false);;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varAnsichtsDatum; Today());;
Set(varAusgewaehltesStockwerk; "OG");;
Set(varStockwerkDropdownOffen; false);;
Set(varStartOverride; "");;
Set(varEndeOverride; "");;
Clear(colAusgewaehlteBuchungen);;
Set(varMehrfachAuswahlModus; false);;
Set(varAuswahlModusAktiv; false);;
Set(varZeigeVerwaltenKlein; false);;
Set(varGalleryNeuAufbauen; 0);;
Set(varGeklickteBuchungKlein; Blank());;
ClearCollect(
  colTischPositionenUG;
  {Tisch: "UG Desk 1";  X: 530;  Y: 592; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 2";  X: 530;  Y: 679; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 3";  X: 582;  Y: 588; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 4";  X: 582;  Y: 675; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 5";  X: 738;  Y: 584; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 6";  X: 738;  Y: 671; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 7";  X: 790;  Y: 579; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 8";  X: 790;  Y: 666; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 9";  X: 1011; Y: 575; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 10"; X: 1011; Y: 662; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 11"; X: 1063; Y: 571; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 12"; X: 1063; Y: 658; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 13"; X: 1202; Y: 260; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 14"; X: 1210; Y: 348; Ausrichtung: "Horizontal"};
  {Tisch: "UG Desk 15"; X: 1255; Y: 256; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 16"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 17"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
);;
Set(varIsLoading; false);;
Set(varSpinnerWinkel; 0);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnVerwalten.OnSelect`** (Schritt G2)

```
Set(varSelectedBuchung; ThisItem);;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false);;
Set(varAusgewaehltePlusDauer; Blank())
```

**`btnVerwalten_2.OnSelect`** (Schritt G2)

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

**`btnPlus1Std.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnPlus1Std.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 60;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnPlus2Std.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnPlus2Std.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 120;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnPlus3Std.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnPlus3Std.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes);
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 180;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnPlus1Std_1.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnPlus1Std_1.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 60;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnPlus2Std_1.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnPlus2Std_1.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 120;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnPlus3Std_1.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes); tischWert: aktuelleBuchung.Tisch.Value; endeAlt: aktuelleBuchung.Endzeit };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnPlus3Std_1.Fill`** (Schritt G2)

```
With({ aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) }; With({ tischWert: aktuelleBuchung.Tisch.Value; endeAlt: aktuelleBuchung.Endzeit; neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes) }; With({ direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0 }; If(varAusgewaehltePlusDauer = 180; ColorValue("#00A96B"); If(direktBesetzt; ColorFade(ColorValue("#EB3951"); 70%); ColorFade(ColorValue("#00A96B"); 70%))))))
```

**`btnMinus1Std.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -60; TimeUnit.Minutes) };
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnMinus1Std.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -60; TimeUnit.Minutes);
      zuKurz: DateAdd(aktuelleBuchung.Endzeit; -60; TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    };
    If(
      varAusgewaehltePlusDauer = -60;
      ColorValue("#00A96B");
      If(
        zuKurz;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnMinus2Std.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes) };
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnMinus2Std.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes);
      zuKurz: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    };
    If(
      varAusgewaehltePlusDauer = -120;
      ColorValue("#00A96B");
      If(
        zuKurz;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnMinus3std.DisplayMode`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -180; TimeUnit.Minutes) };
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btnMinus3std.Fill`** (Schritt G2)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -180; TimeUnit.Minutes);
      zuKurz: DateAdd(aktuelleBuchung.Endzeit; -180; TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    };
    If(
      varAusgewaehltePlusDauer = -180;
      ColorValue("#00A96B");
      If(
        zuKurz;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

**`btnVerlängern.OnSelect`** (Schritt G3)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
    }));;
    Set(varZeigeVerwalten; false);;
    Set(varAusgewaehltePlusDauer; Blank())
  )
);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnVerlängern_1.OnSelect`** (Schritt G3)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    Set(varSelectedBuchungTab; Patch(Tischbuchungen; aktuelleBuchung; {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
    }));;
    Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
    Set(varZeigeVerwaltenTab; false);;
    Set(varAusgewaehltePlusDauer; Blank());;
    Clear(colAusgewaehlteBuchungen);;
    Set(varMehrfachAuswahlModus; false)
  )
)
```

**`btnStornieren.OnSelect`** (Schritt G4)

```
Remove(Tischbuchungen; varSelectedBuchung);; Set(varZeigeVerwalten; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnStornieren_1.OnSelect`** (Schritt G4)

```
Set(varIsLoading; true);;
If(
  IsBlank(varSelectedBuchungTab);
  Notify("Keine Buchung ausgewählt."; NotificationType.Warning);
  Remove(Tischbuchungen; varSelectedBuchungTab);;
  Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Notify("Buchung storniert."; NotificationType.Success)
);;
Set(varZeigeVerwaltenTab; false);;
Set(varIsLoading; false)
```

**`btnStornierenKlein.OnSelect`** (Schritt G4)

```
Set(varIsLoading; true);;
ClearCollect(
    colStornoFrisch;
    Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
);;
ClearCollect(
    colStornoZiele;
    Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
);;
If(
    CountRows(colAusgewaehlteBuchungen) = 0;
    Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
    If(
        CountRows(colStornoZiele) = 0;
        Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
        IfError(
            Remove(Tischbuchungen; colStornoZiele);
            Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
            If(
                CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
                Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
                Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
            )
        )
    )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Clear(colStornoFrisch);;
Clear(colStornoZiele);;
Clear(colAusgewaehlteBuchungen);;
Set(varGeklickteBuchungKlein; Blank());;
Set(varZeigeVerwaltenKlein; false);;
Set(varAuswahlModusAktiv; false);;
Reset(tglAuswahlModus);;
Set(varIsLoading; false)
```

**`btnEinchecken.OnSelect`** (Schritt G5)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {CheckedIn: !aktuelleBuchung.CheckedIn}))
);;
Set(varZeigeCheckin; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnSpeichern.OnSelect`** (Schritt G6)

```
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel)
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatum.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatum.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatum.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatum.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                neueDatensaetze:
                  ForAll(
                    Filter(
                      datumsListe As Eintrag;
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0
                    ) As Frei;
                    {
                      Tisch: {Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel};
                      Startzeit: Frei.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                      Endzeit: Frei.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                      Person: {
                        Claims: "i:0#.f|membership|" & Lower(User().Email);
                        Department: "";
                        DisplayName: User().FullName;
                        Email: User().Email;
                        JobTitle: "";
                        Picture: ""
                      }
                    }
                  )
              };
              With(
                {
                  speicherStatus:
                    If(
                      CountRows(neueDatensaetze) = 0;
                      "keine";
                      IfError(
                        Patch(Tischbuchungen; ForAll(neueDatensaetze; Defaults(Tischbuchungen)); neueDatensaetze);
                        "fehler";
                        "ok"
                      )
                    )
                };
                With(
                  { anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze) };
                  If(
                    speicherStatus = "fehler";
                    Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen."; NotificationType.Error);
                    If(
                      effektivesBisRoh > effektivesBis;
                      Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
                      If(
                        anzahlUebersprungen > 0;
                        Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
                        Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varZeigeDialog; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varIsLoading; false)
```

**`btnSpeichernTischePanel.OnSelect`** (Schritt G6)

```
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel)
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatumTischePanel.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatumTischePanel.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatumTischePanel.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatumTischePanel.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                ergebnisse:
                  ForAll(
                    datumsListe As Eintrag;
                    If(
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0;
                      With(
                        {
                          neuerEintrag: Patch(Tischbuchungen; Defaults(Tischbuchungen); {
                            Tisch: {Id: ddTischePanel.Selected.ID; Value: ddTischePanel.Selected.Titel};
                            Startzeit: Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                            Endzeit: Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                            Person: {
                              Claims: "i:0#.f|membership|" & Lower(User().Email);
                              Department: "";
                              DisplayName: User().FullName;
                              Email: User().Email;
                              JobTitle: "";
                              Picture: ""
                            }
                          })
                        };
                        "gespeichert"
                      );
                      "übersprungen"
                    )
                  )
              };
              With(
                { anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen")) };
                If(
                  effektivesBisRoh > effektivesBis;
                  Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
                  If(
                    anzahlUebersprungen > 0;
                    Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
                    Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varZeigeTischBuchungForm; false);;
Set(varAktiverTab; "dashboard");;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Reset(tglTagMo_1);;
Reset(tglTagDi_1);;
Reset(tglTagMi_1);;
Reset(tglTagDo_1);;
Reset(tglTagFr_1);;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Set(varIsLoading; false)
```

**`btnHitArea.OnSelect`** (Schritt G7)

```
With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today();
        LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
        LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
      )
  };
  If(
    IsBlank(relevanteBuchung);
      Set(varSelectedTisch; ThisItem);;
      Set(varZeigeDialog; true);;
      Set(varZeigeDetails; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false);;
      Set(varWiederholen; false);;
      Set(varWiederholenModus; "Wochentage");;
      Set(varTagMo; false);;
      Set(varTagDi; false);;
      Set(varTagMi; false);;
      Set(varTagDo; false);;
      Set(varTagFr; false);;
      Set(varTagSa; false);;
      Set(varTagSo; false);
      Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; relevanteBuchung);;
      Set(varZeigeDetails; true);;
      Set(varZeigeDialog; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false)
  )
)
```

**`btnTischHinzufügen.OnSelect`** (Schritt G7)

```
Set(varZeigeTischBuchungForm; true);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Reset(tglTagMo_1);;
Reset(tglTagDi_1);;
Reset(tglTagMi_1);;
Reset(tglTagDo_1);;
Reset(tglTagFr_1);;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "")
```

**`ddStart.Items`** (Schritt G7)

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
  With(
    {
      minutenStart:
        If(
          dpDatum.SelectedDate = Today();
          30 * RoundUp(minutenJetzt / 30; 0);
          8 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30; 0) + 1; 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`ddStart.Default`** (Schritt G7)

```
If(
  varStartOverride <> "";
  varStartOverride;
  With(
    { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
    With(
      {
        minutenStart:
          If(
            dpDatum.SelectedDate = Today();
            30 * RoundUp(minutenJetzt / 30; 0);
            8 * 60
          )
      };
      Text(Time(RoundDown(minutenStart / 60; 0); Mod(minutenStart; 60); 0); "hh:mm")
    )
  )
)
```

**`ddStartTischePanel.Items`** (Schritt G7)

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
  With(
    {
      minutenStart:
        If(
          dpDatumTischePanel.SelectedDate = Today();
          30 * RoundUp(minutenJetzt / 30; 0);
          8 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30; 0) + 1; 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`ddStartTischePanel.Default`** (Schritt G7)

```
If(
  varStartOverridePanel <> "";
  varStartOverridePanel;
  With(
    { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
    With(
      {
        minutenStart:
          If(
            dpDatumTischePanel.SelectedDate = Today();
            30 * RoundUp(minutenJetzt / 30; 0);
            8 * 60
          )
      };
      Text(Time(RoundDown(minutenStart / 60; 0); Mod(minutenStart; 60); 0); "hh:mm")
    )
  )
)
```

**`ddTischePanel.Items`** (Schritt G9)

```
Tische
```

**`ddTischePanel.Items.Value`** (Schritt G9)

```
Title
```

**`btn5Std.DisplayMode`** (Schritt G10)

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btn5Std.Fill`** (Schritt G10)

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          IsBlank(ddTischePanel.Selected);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0;
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btn5Std.OnSelect`** (Schritt G10)

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 5 };
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 5 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 5));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

**`btn9Std.DisplayMode`** (Schritt G10)

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

**`btn9Std.Fill`** (Schritt G10)

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 9;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          IsBlank(ddTischePanel.Selected);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0;
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btn9Std.OnSelect`** (Schritt G10)

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 9 };
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 9 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 9));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

**`Label14.Text`** (Schritt G11)

```
If(
  DateDiff(dpDatum.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
  "*Zu weit gewählt —      es werden 2 Wochen gespeichert";
  "*Wiederholung nur für max. 2 Wochen möglich"
)
```

**`Label14.Color`** (Schritt G11)

```
If(
  DateDiff(dpDatum.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
  ColorValue("#EB3951");
  RGBA(50; 49; 48; 1)
)
```

**`ddStockwerk.OnSelect`** (Schritt G12)

```
Set(varStockwerkDropdownOffen; true);;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedTisch; Blank());;
Set(varSelectedBuchung; Blank());;
Set(varAusgewaehltePlusDauer; 0)

```

**`Icon1.OnSelect`** (Schritt G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

**`Icon1_1.OnSelect`** (Schritt G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

**`Image6.OnSelect`** (Schritt G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

**`btnHitArea_1.OnSelect`** (Schritt G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

**`btnAbbrechenTischePanel.OnSelect`** (Schritt G12)

```
Set(varZeigeTischBuchungForm; false);;
Set(varZeigeTischBuchungForm; false);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel)
```

**`Rectangle1.Fill`** (Schritt G13)

```
With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today();
        LookUp(colGrundriss; TischName = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
        LookUp(colGrundriss; TischName = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
      )
  };
  If(
    IsBlank(relevanteBuchung);
    ColorValue("#00A96B");
    If(
      relevanteBuchung.Eingecheckt;
      ColorValue("#EB3951");
      ColorValue("#FFA500")
    )
  )
)
```

**`Circle1.Fill`** (Schritt G13)

```
With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today();
        LookUp(colGrundriss; TischName = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
        LookUp(colGrundriss; TischName = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
      )
  };
  If(IsBlank(relevanteBuchung); ColorValue("#4DC398"); Color.White)
)
```

**`conDetailsPopup.Height`** (Schritt G14)

```
154
```

**`Image7.Height`** (Schritt G14)

```
154
```

**`lblStatus.Text`** (Schritt G15)

```
"Besetzt"
```

**`lblStatus.Color`** (Schritt G15)

```
ColorValue("#EB3951")
```

**`galTischbuchungenHeute.Items`** (Schritt G16)

```
Filter(
  Tischbuchungen;
  Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
)
```

**`conCheckinDialog.Y`** (Schritt G16)

```
With(
        { _idx: CountRows(Filter(galTischbuchungenHeute.AllItems; ID < varSelectedBuchung.ID)) + 1 };
            conDashboard.Y + galTischbuchungenHeute.Y + (_idx - galTischbuchungenHeute.VisibleIndex) * galTischbuchungenHeute.TemplateHeight + (galTischbuchungenHeute.TemplateHeight - Self.Height) / 2
            )
```

**`btnAbbrechen.PressedColor`** (Schritt G17)

```
Self.Fill
```

**`btnAbbrechen.PressedFill`** (Schritt G17)

```
Color.Black
```

**`btnSchließen2.PressedColor`** (Schritt G17)

```
Self.Fill
```

**`btnSchließen2.PressedFill`** (Schritt G17)

```
Color.Black
```

**`btnSchließen3.PressedColor`** (Schritt G17)

```
Self.Fill
```

**`btnSchließen3.PressedFill`** (Schritt G17)

```
Color.Black
```

**`btnSchließen4.PressedColor`** (Schritt G17)

```
Color.Black
```

**`btnSchließen4.PressedFill`** (Schritt G17)

```
Color.Black
```

**`btnSchließen4_1.PressedColor`** (Schritt G17)

```
Color.Black
```

**`btnSchließen4_1.PressedFill`** (Schritt G17)

```
Color.Black
```

**`btnSchließenKlein.PressedColor`** (Schritt G17)

```
Color.Black
```

**`btnSchließenKlein.PressedFill`** (Schritt G17)

```
Color.Black
```

**`btnSpeichern.PressedColor`** (Schritt G17)

```
Self.Fill
```

**`btnTabDashboard.Fill`** (Schritt G18)

```
ColorValue("#171496")
```

**`btnTabBuchungen.Fill`** (Schritt G18)

```
ColorValue("#171496")
```

**`Circle2.Fill`** (Schritt G19)

```
varProfilFarbe
```

**`tglTagMo.TrueFill`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`tglTagDi.TrueFill`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`tglTagMi.TrueFill`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`tglTagDo.TrueFill`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`tglTagFr.TrueFill`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`dpDatum.IconBackground`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`dpWiederholenBis.IconBackground`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`ddStart.ChevronBackground`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`ddStart.HoverFill`** (Schritt G20)

```
RGBA(205; 209; 213; 1)
```

**`ddEnde.ChevronBackground`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`ddEnde.HoverFill`** (Schritt G20)

```
RGBA(205; 209; 213; 1)
```

**`btnSpeichern.Fill`** (Schritt G20)

```
ColorValue("#00A96B")
```

**`btnSpeichern.PressedFill`** (Schritt G20)

```
ColorValue("#00a96b")
```

**`tglAuswahlModus.TrueFill`** (Schritt G20)

```
RGBA(100; 118; 132; 1)
```

**`btnStornieren.Fill`** (Schritt G21)

```
ColorValue("#171496")
```

**`btnStornieren_1.Fill`** (Schritt G21)

```
ColorValue("#171496")
```

**`btnStornierenKlein.Fill`** (Schritt G21)

```
ColorValue("#171496")
```

**`lblMyPersonalDesk.Text`** (Schritt G22)

```
"My personal desk"
```

**`btnTischHinzufügen.Text`** (Schritt G22)

```
"Tisch Buchen"
```

**`lblTischeBuchenPanel.Text`** (Schritt G22)

```
"Tisch Buchen"
```

**`btnPlus1Std.Text`** (Schritt G22)

```
"+1Std"
```

**`btnPlus2Std.Text`** (Schritt G22)

```
"+2Std"
```

**`btnPlus3Std.Text`** (Schritt G22)

```
"+3Std"
```

**`btnPlus1Std_1.Text`** (Schritt G22)

```
"+1Std"
```

**`btnPlus2Std_1.Text`** (Schritt G22)

```
"+2Std"
```

**`btnPlus3Std_1.Text`** (Schritt G22)

```
"+3Std"
```

**`btnMinus1Std.Text`** (Schritt G22)

```
"-1Std"
```

**`btnMinus2Std.Text`** (Schritt G22)

```
"-2std"
```

**`btnMinus3std.Text`** (Schritt G22)

```
"-3Std"
```

**`lblTischLeer.Text`** (Schritt G22)

```
"---"
```

**`lblTischLeer_1.Text`** (Schritt G22)

```
"-Keine Einträge-"
```

**`lblTitel3.Text`** (Schritt G22)

```
If(IsBlank(varSelectedBuchung); ""; "Tisch " & varSelectedBuchung.Tisch.Value)
```

**`lblTitel3_1.Text`** (Schritt G22)

```
"Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value
```

**`lblTitel2.Text`** (Schritt G22)

```
"Tisch: " & varSelectedBuchung.Tisch.Value
```

**`lblTischHeute.Text`** (Schritt G22)

```
"Tisch " & ThisItem.Tisch.Value
```

**`Rectangle3_2.Fill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`Rectangle5.Fill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`Rectangle6.Fill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`Rectangle6_1.Fill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`Rectangle6_2.Fill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddStockwerk.SelectionFill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddTischePanel.SelectionFill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddStartTischePanel.SelectionFill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddEndTischePanel.SelectionFill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddStart.SelectionFill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddEnde.SelectionFill`** (Schritt G23)

```
RGBA(100; 118; 132; 1)
```

**`ddTischePanel.ChevronHoverBackground`** (Schritt G23)

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddStartTischePanel.ChevronHoverBackground`** (Schritt G23)

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddEndTischePanel.ChevronHoverBackground`** (Schritt G23)

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddStart.ChevronHoverBackground`** (Schritt G23)

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddEnde.ChevronHoverBackground`** (Schritt G23)

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`btnHitArea.HoverFill`** (Schritt G24)

```
RGBA(0; 0; 0; 0,15)
```

**`btnEincheckenHeute.HoverFill`** (Schritt G24)

```
RGBA(0; 0; 0; 0,04)
```

**`btnVerwalten.HoverFill`** (Schritt G24)

```
RGBA(0; 0; 0; 0,2)
```

**`btnVerwalten_2.HoverFill`** (Schritt G24)

```
RGBA(0; 0; 0; 0,2)
```

**`btnHitArea_1.HoverFill`** (Schritt G24)

```
RGBA(0; 0; 0; 0,08)
```

**`galRäume.Items`** (Schritt G25)

```
With(
  { basisStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value; 2)); Value(Mid(ddBeginnRaumPanel.Selected.Value; 4; 2)); 0) };
  Filter(
    Räume As R;
    CountRows(
      Filter(
        Table({Offset: 0}; {Offset: 30}; {Offset: 60}; {Offset: 90}) As Slot;
        With(
          { slotStart: DateAdd(basisStart; Slot.Offset; TimeUnit.Minutes) };
          With(
            { slotEnde: DateAdd(slotStart; 30; TimeUnit.Minutes) };
            CountRows(Filter(Raumbuchungen; Raum.Value = R.Titel && Startzeit < slotEnde && Endzeit > slotStart)) = 0
          )
        )
      )
    ) > 0
  )
)
```

**`galRaumbuchungenHeute.Items`** (Schritt G25)

```
Filter(Raumbuchungen; Person.Email = User().Email && Startzeit >= Today() && Startzeit < DateAdd(Today(); 1; TimeUnit.Days) && Endzeit >= Now())
```

**`recBuchungDavor1.Visible`** (Schritt G25)

```
CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes))) > 0
```

**`recBuchungDanach1.Visible`** (Schritt G25)

```
CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes))) > 0
```

**`Label4.Text`** (Schritt G25)

```
With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
    fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes)
  };
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
    If(
      IsBlank(buchung);
      "";
      If(
        recBuchungDanach1.Width < 40;
        "";
        If(
          recBuchungDanach1.Width < 90;
          Left(First(Split(buchung.Person.DisplayName; " ")).Value; 1) & Left(Last(Split(buchung.Person.DisplayName; " ")).Value; 1);
          buchung.Person.DisplayName
        )
      )
    )
  )
)
```

**`Label5.Text`** (Schritt G25)

```
With(
  { fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes) };
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
    If(IsBlank(buchung); ""; buchung.Person.DisplayName)
  )
)
```

**Handy-App `ddStart.Items`**

```
With(
  { ab: If(ddDatum.Selected.Tag = Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); 8 * 60) };
  ForAll(
    Sequence(Max(0; (21 * 60 + 30 - ab) / 30 + 1); 0) As n;
    {
      Value: Text(Time(RoundDown((ab + n.Value * 30) / 60; 0); Mod(ab + n.Value * 30; 60); 0); "hh:mm");
      Min: ab + n.Value * 30
    }
  )
)
```

## Anhang B: Maschinelle Prüfung

```
253 Properties Desktop-App in 26 Schritten, 2 Properties Handy-App, 7 neue Steuerelemente.
Schreibstellen auf Tischbuchungen nach dem Plan: 6 (btnEinchecken.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnStornoJa.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect), alle mit Zweifach-Sperre und Ladezeile.
Je Property geprüft: Klammern, Rückübersetzung deutsch->englisch, keine Kommentare, Steuerelemente bekannt oder neu angelegt, jede gelesene var/col wird irgendwo gesetzt.
Jede Property kommt genau einmal vor.
Prüfung: 0 Fehler
```
