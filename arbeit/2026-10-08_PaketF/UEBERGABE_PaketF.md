# Paket F: Freigabe in der App statt Flow, dazu der Storno-Fix

Stand 08.10.2026 · erzeugt aus dem Export 07.10. und den Endfassungen des Gesamtplans (`werkzeuge/paket_f.py`, `doc_paket_f.py`) · ersetzt Schritt **G-F** (Flow) des Gesamtplans · Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**

## 0. Kurzfassung
- **Was passiert:** Wer nicht bis 30 Minuten nach Beginn eingecheckt hat, **verliert den Tisch**. Die Buchung bleibt aber in der Liste stehen, sie heißt jetzt **„verfallen“**, und die App behandelt sie überall wie „frei“. **Es wird nichts gelöscht, und es gibt keinen Flow.**
- **Spät gebucht ist kein Problem:** Die 30 Minuten zählen ab dem späteren der beiden Zeitpunkte **Beginn** und **Buchungszeitpunkt** (SharePoint-Spalte `Erstellt`). Wer um 09:29 für 09:00 bucht (geht in der Handy-App, oder wenn der Dialog vor 09:00 geöffnet wurde), hat bis 09:59 Zeit.
- **Auschecken** nach Beginn beendet die Buchung (Ende = jetzt). Der Tisch ist für andere wieder buchbar (ab der nächsten halben Stunde, im Grundriss spätestens nach 5 Min grün). Vor dem Beginn nimmt Auschecken nur den Check-in zurück.
- **Einchecken** geht ab 30 Minuten vor Beginn bis 30 Minuten nach Beginn (bisher: bis zum Ende).
- **Neu:** Die App **fragt einmal je Buchung nach dem Check-in**: beim Öffnen, sonst im 5-Minuten-Takt, wenn das Dashboard für heute offen ist und kein Dialog. Ein Klick genügt, ohne neues Steuerelement.
- **Storno-Fix:** Die Rückfrage merkt sich die Buchung beim Öffnen. Gelöscht werden nur eigene Buchungen. Ein dunkler Hintergrund sperrt alle anderen Klicks.
- **Umfang:** 8 Schritte, 44 Properties, 1 neues Steuerelement (`btnStornoHintergrund`). Einfügen **nach** dem vollständigen Gesamtplan (Phasen 1–7). Jeder Block ist die **ganze Property** in ihrer Endfassung, inklusive aller Gesamtplan-Änderungen.
- **Unabhängig geprüft** (Prüf-Agent, 08.10.): kein kritischer Befund. 13 Befunde (Z-Order, leere Einstellung, zwei nicht ausführbare Tests, Texte, Nachlese beim Check-in, „zwei Tische“ beim Verlängern) sind eingearbeitet, siehe `pruefung_paket_f.md`.
- **Ehrlich:**
  - Nichts davon ist in Studio getestet.
  - Alles ist aus dem Export erzeugt und maschinell geprüft: 0 Fehler, jede der 39 Abfragen auf `Tischbuchungen` einzeln eingeordnet.
  - Die Spalte `Erstellt` ist im Export **belegt** (lesbar, filterbar).
  - Ob Studio sie unter dem Namen `Erstellt` annimmt, steht unter UNSICHER (Test U1).

## 1. Die Regel (eine Zeile, überall gleich)
Eine Buchung ist **verfallen**, wenn alle drei Bedingungen gelten:
1. **nicht eingecheckt**,
2. **Beginn** liegt mehr als 30 Minuten zurück,
3. **Buchungszeitpunkt** (`Erstellt`) liegt mehr als 30 Minuten zurück.

In der App steht das als `!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze`, mit `varFreigabeGrenze = jetzt − varFreigabeMinuten`. Die 30 stehen **einmal** in `App.OnStart` (`Set(varFreigabeMinuten; 30)`). Willst du später 15 oder 45 Minuten, änderst du nur diese Zahl. Ist die Variable einmal leer (z. B. in Studio, bevor `OnStart` lief), rechnet die App mit 30 (`Coalesce`).

**Beispiele** (Buchung 09:00–17:00, heute um 08:00 angelegt):

| Uhrzeit | Was passiert |
|---|---|
| 08:30 | Einchecken möglich. Beim Öffnen der App fragt sie: „Check-in: OG Desk 5“ |
| 09:10 | Noch nicht eingecheckt → Kachel **orange** |
| 09:30 | Frist abgelaufen. Ab dem nächsten Laden (spätestens 5 Min, Timer) ist die Kachel **grün**. Ein Klick auf die Kachel prüft sofort frisch und öffnet den Buchungsdialog |
| 09:40 | Kollegin bucht den Tisch 10:00–12:00 → klappt. Die verfallene Buchung blockiert nicht |
| 09:45 | Du willst einchecken → „Zu spät: … verfällt die Buchung … Bitte neu buchen.“ Im Dashboard steht bei deiner Buchung **„Verfallen“** (grau) |

| Sonderfall | Ergebnis |
|---|---|
| Um 09:29 für 09:00 gebucht (Handy-App oder Dialog vor 09:00 geöffnet) | Frist bis 09:59 (ab Buchungszeitpunkt) |
| Eingecheckt, um 11:17 ausgecheckt | Ende wird 11:18, die Buchung ist korrekt erledigt. Andere können ab 11:30 buchen |
| Vor 09:00 eingecheckt und wieder ausgecheckt | Nur der Check-in wird zurückgenommen, die Buchung bleibt |
| Serie Mo–Fr | Jeder Termin für sich: Wer am Dienstag nicht eincheckt, verliert nur Dienstag |
| Verfallene eigene Buchung verlängern | geht nicht („Diese Buchung ist verfallen …“), stornieren geht |
| Eigene verfallene Buchung, neu buchen zur selben Zeit (anderer Tisch) | geht, die verfallene zählt nicht als „du hast schon einen Tisch“ |

## 2. Wege, die ich geprüft habe

| Weg | Bewertung |
|---|---|
| **A. Flow löscht** (Gesamtplan G-F) | verworfen. Löscht in zwei Fällen falsch (spät gebucht, Auschecken). Läuft unter einem Konto. Daten sind weg. Josias will es nicht |
| **B. Die App löscht fremde Buchungen**, sobald sie verfallen sind | verworfen. Mit „nur eigene Elemente“ (G-R) darf niemand fremde Einträge löschen. Jede offene App würde gleichzeitig löschen (Konflikte) |
| **C. „Verfallen“ berechnen, nichts löschen** | **gewählt.** Kein Flow, keine Rechte-Probleme, keine zusätzlichen Anfragen für die Anzeige. Die No-Shows bleiben als Zahl erhalten (Auswertung möglich) |
| D. Neue Spalte `FreigabeAb` beim Buchen schreiben | verworfen. Alte Buchungen und die Handy-App hätten sie nicht. `Erstellt` setzt SharePoint immer selbst |
| E. Berechnete SharePoint-Spalte | verworfen. Kennt kein „jetzt“, und Power Apps kann danach nicht serverseitig filtern |
| F. Serverseitig nach `CheckedIn` filtern | verworfen. Ja/Nein-Spalten gelten in SharePoint als unzuverlässig delegierbar ([Community](https://powerappsguide.com/blog/post/sharepoint---filtering-data)). **Der Server filtert nur nach Zeit, Tisch und Person (delegierbar, belegt). `CheckedIn` und `Erstellt` prüft die App lokal auf dem kleinen Ergebnis.** Das ist dasselbe Muster wie die gemessene L2-Ladezeile |
| G. Check-in-Frage beim Öffnen und per Timer | **gewählt.** Nutzt den vorhandenen Check-in-Dialog, kein neues Steuerelement. Fragt nur einmal je Buchung |
| H. Automatisch einchecken, wenn jemand „für jetzt“ bucht | verworfen. Man kann auch von zu Hause buchen |
| I. QR-Code am Tisch → Handy-App checkt ein (`Param("tisch")`) | **später** (Handy-App). Würde „Einchecken von zu Hause“ verhindern. GoBright bietet dasselbe mit NFC/QR ([GoBright](https://gobright.com/?p=2189)) |
| J. Mail an No-Shows | später, braucht einen Flow. GoBright hat das als Option ([GoBright](https://gobright.com/new-features-and-innovation/new-features-improved-notifications-for-bookings/)) |

**Vergleich mit GoBright:** GoBright arbeitet mit einem Check-in-Fenster vor und nach Beginn. Ohne Check-in wird die Buchung beendet und als No-Show gezählt ([GoBright, Desk-Profil](https://gobright.com/?p=2189)). Paket F macht dasselbe, nur ohne Server-Dienst.

## 3. So arbeitest du das Paket ab
1. **Erst den Gesamtplan vollständig** (Phasen 1–7, ohne G-F) einfügen und testen. Paket F setzt ihn voraus: Die Blöcke lesen Steuerelemente, Spalten und Variablen aus dem Gesamtplan (`conStornoFrage`, `btnStornoJa`, `tmrAktualisieren`, `Tische.Gesperrt`, `varDialogJetzt`, `varPanelJetzt`, `lblBelegtHeute`). Fehlt einer davon, gibt es rote Fehler.
2. **Reihenfolge F1 → F8 einhalten.** F1 legt `varFreigabeMinuten` an, alle anderen lesen sie.
3. Je Property: Steuerelement suchen (Ort steht dabei), **ganze Property ersetzen**, Enter. Nach jedem Schritt App-Prüfung (keine neuen roten Fehler), Test, Strg+S.
4. Zwischen den Schritten bleibt die App lauffähig. Die Ladestellen können einzeln umgestellt werden, weil `colGrundriss` dieselben Spalten behält.
5. **Veröffentlichen** erst nach F8 und bestandenem Testbogen (Abschnitt 6).
6. **Rückfall:** Anhang A enthält die Fassung **vor** Paket F (Gesamtplan bzw. Export). Neues Steuerelement löschen.
7. Alle Blöcke sind deutsch (`;` trennt, `;;` verkettet). Nichts umschreiben.

## 4. Schritte

| Schritt | Was | Properties | neu anzulegen |
|---|---|---|---|
| F1 | App-Start: Einstellung 30 Minuten, Check-in-Frage beim Öffnen | 1 | – |
| F2 | Storno-Fix: richtige Buchung, nur eigene, Hintergrund sperrt | 20 | `btnStornoHintergrund` |
| F3 | Grundriss: verfallene Buchungen als frei anzeigen | 7 | – |
| F4 | Buchen: verfallene Buchungen blockieren nicht | 2 | – |
| F5 | Panel „Tisch buchen“: Liste und 5/9-Std.-Knöpfe | 6 | – |
| F6 | Verlängern: verfallene Buchungen blockieren nicht | 4 | – |
| F7 | Einchecken bis 30 Min nach Beginn, Auschecken beendet die Buchung | 3 | – |
| F8 | Check-in-Erinnerung alle 5 Minuten | 1 | – |

### F1 App-Start: Einstellung 30 Minuten, Check-in-Frage beim Öffnen

**Problem:** Die 30 Minuten standen bisher nirgends. Die App fragte nie nach dem Check-in.
**Lösung:** `Set(varFreigabeMinuten; 30)` steht ganz oben (die eine Zahl zum Ändern). Am Ende, **vor** der Ladezeile, sucht die App die eigene Buchung, bei der gerade eingecheckt werden kann (Beginn in höchstens 30 Min, noch nicht zu Ende, nicht eingecheckt, nicht verfallen). Gibt es eine, öffnet sich der vorhandene Check-in-Dialog. Die Ladezeile lädt `Erstellt` mit und lässt verfallene Buchungen weg.
**Danach sofort:** in der Strukturansicht `App` → **…** → **OnStart ausführen**, erst dann weiter mit F2.
**Test (U1 zuerst):** Nach dem Einfügen: App-Prüfung ohne roten Fehler bei `Erstellt` (sonst siehe UNSICHER U1). Eigene Buchung „jetzt bis +1 Std“ anlegen, App schließen und neu öffnen (bzw. in Studio „App.OnStart ausführen“) → Check-in-Dialog erscheint. Ohne passende Buchung erscheint nichts.

**`App.OnStart`** · Ort: `App` · **ganze Property ersetzen** · vorher: Gesamtplan G1

```
Set(varFreigabeMinuten; 30);;
Set(varCheckinGefragtID; 0);;
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
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
ClearCollect(colCheckinFrage; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()));;
RemoveIf(colCheckinFrage; CheckedIn || (Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
If(
  !IsEmpty(colCheckinFrage);
  Set(varCheckinGefragtID; First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID);;
  Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinGefragtID));;
  Set(varZeigeCheckin; true)
);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
```

**Rückfall F1:** Fassungen aus Anhang A wieder einsetzen.

### F2 Storno-Fix: richtige Buchung, nur eigene, Hintergrund sperrt

**Problem (aus der unabhängigen Durchsicht, nachgeprüft):** Bei offener Storno-Frage war der Rest der App klickbar. Ein Klick auf eine Grundriss-Kachel setzte `varSelectedBuchung` auf deren Buchung, eventuell die eines Kollegen. „Ja, stornieren“ löschte dann diese.
**Lösung:**
1. Beim Klick auf „Stornieren“ wird die ID in `varStornoID` festgehalten. „Ja“ löscht nur diese.
2. Vor dem Löschen prüft die App, ob die Buchung der angemeldeten Person gehört (`Lower(E-Mail)`, weil Groß-/Kleinschreibung abweichen kann). Sonst: „Nur eigene Buchungen können storniert werden.“
3. Neuer Knopf `btnStornoHintergrund` über den ganzen Bildschirm, halb dunkel. Er fängt alle Klicks ab. Ein Klick daneben heißt „Nein“.

**Anlegen:** `Screen1` markieren → Einfügen → Schaltfläche (klassisch) → umbenennen in `btnStornoHintergrund`. Danach **`conStornoFrage` markieren → … → Neu anordnen → Ganz nach vorne bringen** (nicht nur „Nach vorne bringen“, das hebt nur um eine Ebene). **Prüfen in der Strukturansicht:** `conStornoFrage` ist der oberste Eintrag unter `Screen1`, `btnStornoHintergrund` direkt darunter. Sonst trifft jeder Klick auf „Ja“ den Hintergrund und wirkt wie „Nein“.
**Test:** Dashboard → Verwalten → Stornieren → die Frage erscheint auf dunklem Hintergrund. Klick auf eine Kachel → nichts passiert, die Frage schließt sich (= Nein). Nochmal → „Ja, stornieren“ → genau die gewählte Buchung ist weg. Dasselbe im Tab „Buchungen“ und mit Mehrfachauswahl.

Neues Steuerelement (zuerst anlegen, Name exakt so): `btnStornoHintergrund` (Button (Einfügen → Schaltfläche, klassisch), auf oberster Ebene einfügen, danach `conStornoFrage` markieren → **Nach vorne bringen**)

**`btnStornoHintergrund.Text`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
""
```

**`btnStornoHintergrund.X`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.Y`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.Width`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
Parent.Width
```

**`btnStornoHintergrund.Height`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
Parent.Height
```

**`btnStornoHintergrund.Visible`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
varZeigeStornoFrage
```

**`btnStornoHintergrund.Fill`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
RGBA(0; 0; 0; 0,35)
```

**`btnStornoHintergrund.HoverFill`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
RGBA(0; 0; 0; 0,35)
```

**`btnStornoHintergrund.PressedFill`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
RGBA(0; 0; 0; 0,35)
```

**`btnStornoHintergrund.BorderThickness`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.FocusedBorderThickness`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.RadiusTopLeft`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.RadiusTopRight`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.RadiusBottomLeft`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.RadiusBottomRight`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
0
```

**`btnStornoHintergrund.OnSelect`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
Set(varZeigeStornoFrage; false)
```

**`btnStornoHintergrund.AccessibleLabel`** · Ort: `(neu) Screen1 > btnStornoHintergrund` · **neu setzen**

```
"Abfrage schließen"
```

**`btnStornieren.OnSelect`** · Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **ganze Property ersetzen** · vorher: Gesamtplan G4

```
Set(varStornoID; varSelectedBuchung.ID);;
Set(varStornoQuelle; "dash");;
Set(varZeigeStornoFrage; true)
```

**`btnStornieren_1.OnSelect`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **ganze Property ersetzen** · vorher: Gesamtplan G4

```
Set(varStornoID; varSelectedBuchungTab.ID);;
Set(varStornoQuelle; "tab");;
Set(varZeigeStornoFrage; true)
```

**`btnStornoJa.OnSelect`** · Ort: `(neu) conStornoFrage > btnStornoJa` · **ganze Property ersetzen** · vorher: Gesamtplan G4

```
Set(varZeigeStornoFrage; false);;
Switch(
  varStornoQuelle;
  "dash";
  If(
    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
    Set(varIsLoading; true);;
    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varStornoID));;
    If(
      IsBlank(varStornoBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwalten; false);
      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
      Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
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
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  );
  "tab";
  If(
    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
    Set(varIsLoading; true);;
    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varStornoID));;
    If(
      IsBlank(varStornoBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwaltenTab; false);
      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
      Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
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
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
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
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
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

**Rückfall F2:** Fassungen aus Anhang A wieder einsetzen, neues Steuerelement löschen.

### F3 Grundriss: verfallene Buchungen als frei anzeigen

**Problem:** Der Grundriss zeigt jede Buchung als belegt, auch wenn niemand gekommen ist.
**Lösung:**
- **Ladezeile** (an allen Stellen, die nur laden: Stockwerk, Datum, die vier Aktualisieren-Symbole): lädt `Erstellt` mit und übernimmt nur nicht verfallene Buchungen in `colGrundriss`. Kachel, Kreis, Initialen und „Belegt:“-Hinweis folgen automatisch.
- **Kachel-Klick (`btnHitArea`)** fragt frisch: Buchungen des Tisches holen, verfallene entfernen. Ist nichts übrig, öffnet sich der Buchungsdialog, sonst das Details-Popup.

**Test:** Testbuchung mit Beginn vor über 30 Min, ohne Check-in, direkt in der SharePoint-Liste anlegen. **`Erstellt` ist dann „jetzt“**, die Kachel bleibt also noch `varFreigabeMinuten` lang orange (Testmodus, siehe Testbogen: 1 Min). Danach Aktualisieren → Kachel grün. Klick → Buchungsdialog.

**`btnHitArea.OnSelect`** · Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen** · vorher: Gesamtplan G7

```
If(
  ThisItem.Gesperrt;
  Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  If(
    varAnsichtsDatum = Today();
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes)));
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)))
  );;
  RemoveIf(colKachel; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varKachelID; First(SortByColumns(colKachel; "Startzeit"; SortOrder.Ascending)).ID);;
  If(
    IsBlank(varKachelID);
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
      Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varKachelID));;
      Set(varZeigeDetails; true);;
      Set(varZeigeDialog; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false)
  )
)
```

**`ddStockwerk.OnChange`** · Ort: `Screen1 > conGrundriss > ddStockwerk` · **ganze Property ersetzen** · vorher: Export 07.10.

```
Set(varAusgewaehltesStockwerk; ddStockwerk.Selected.Kurz);;
Set(varStockwerkDropdownOffen; false);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
```

**`dpAnsichtsDatum.OnChange`** · Ort: `Screen1 > conDashboard > dpAnsichtsDatum` · **ganze Property ersetzen** · vorher: Export 07.10.

```
Set(varAnsichtsDatum; dpAnsichtsDatum.SelectedDate);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
```

**`Icon1_1.OnSelect`** · Ort: `Screen1 > conDashboard > Icon1_1` · **ganze Property ersetzen** · vorher: Gesamtplan G12

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Icon1.OnSelect`** · Ort: `Screen1 > conBuchungen > Icon1` · **ganze Property ersetzen** · vorher: Gesamtplan G12

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Image6.OnSelect`** · Ort: `Screen1 > conHeader > Image6` · **ganze Property ersetzen** · vorher: Gesamtplan G12

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnHitArea_1.OnSelect`** · Ort: `Screen1 > conHeader > btnHitArea_1` · **ganze Property ersetzen** · vorher: Gesamtplan G12

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**Rückfall F3:** Fassungen aus Anhang A wieder einsetzen.

### F4 Buchen: verfallene Buchungen blockieren nicht

**Problem:** Beide Speichern-Knöpfe würden eine verfallene Buchung als Kollision zählen. Die Nachlese hätte den eigenen neuen Termin sogar als „fast gleichzeitig vor dir gebucht“ gemeldet.
**Lösung:** Nach den beiden Abfragen „Tisch belegt“ und „ich habe schon einen Tisch“ entfernt die App verfallene Buchungen (`RemoveIf`). Die Nachlese ignoriert verfallene **fremde** Buchungen. Der eigene neue Termin (gleiche `SerienID`) bleibt immer drin. Die Erfolgsmeldung nennt die Minuten aus `varFreigabeMinuten`.
**Test:** Auf einen Tisch mit verfallener Buchung buchen → „Gebucht: …“ ohne Warnung. In SharePoint stehen beide Zeilen, die alte unverändert.

**`btnSpeichern.OnSelect`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen** · vorher: Gesamtplan G6

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
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
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
    RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
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
      RemoveIf(colNeuNachlese; SerienID <> varSerienID && !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
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
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnSpeichernTischePanel.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen** · vorher: Gesamtplan G6

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
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
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
    RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
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
      RemoveIf(colNeuNachlese; SerienID <> varSerienID && !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
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
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**Rückfall F4:** Fassungen aus Anhang A wieder einsetzen.

### F5 Panel „Tisch buchen“: Liste und 5/9-Std.-Knöpfe

**Problem:** Die Tischliste im Panel und die Knöpfe 5 Std / 9 Std halten verfallene Buchungen für belegt.
**Lösung:** Beim Öffnen des Panels wird `varFreigabeGrenze` gesetzt. Die Liste rechnet für jede Buchung `Aktiv` aus und zählt nur aktive. Die beiden Knöpfe ebenso.
**Test:** Panel öffnen, heute, Zeit der verfallenen Buchung → der Tisch steht ohne „(an … belegt)“ in der Liste. 5 Std ist wählbar.

**`btnTischHinzufügen.OnSelect`** · Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen** · vorher: Gesamtplan G7

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
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel);;
Reset(dpWiederholenBis_1)
```

**`ddTischePanel.Items`** · Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen** · vorher: Gesamtplan G9

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
              {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit; Aktiv: CheckedIn || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze}
            );
            FirstN(Table({TischName: ""; Beginn: Now(); Schluss: Now(); Aktiv: true}); 0)
          )
        };
        SortByColumns(
          Filter(
            ForAll(
              Tische As Ti;
              With(
                { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegtListe; Aktiv && TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
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

**`btn5Std.DisplayMode`** · Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · vorher: Gesamtplan G10

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
          IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

**`btn5Std.Fill`** · Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · vorher: Gesamtplan G10

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
            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btn9Std.DisplayMode`** · Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · vorher: Gesamtplan G10

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
          IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

**`btn9Std.Fill`** · Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · vorher: Gesamtplan G10

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
            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**Rückfall F5:** Fassungen aus Anhang A wieder einsetzen.

### F6 Verlängern: verfallene Buchungen blockieren nicht

**Problem:** Wer an einem Tisch verlängern will, an dem eine verfallene Buchung hängt (z. B. weil man selbst darüber gebucht hat), wird fälschlich blockiert. Die eigene verfallene Buchung ließ sich verlängern.
**Lösung:** Beim Öffnen der Verwalten-Dialoge: die nächste Buchung am Tisch ohne verfallene bestimmen (Grenze für die Dauer-Knöpfe). Beim Verlängern: Kollisionen ohne verfallene. **Neu (Prüf-Agent):** Verlängern prüft auch, ob du in der neuen Zeit schon einen anderen Tisch hast (Regel „keine zwei Tische zur selben Zeit“, fehlte bisher). Eigene verfallene Buchung → „Diese Buchung ist verfallen … Bitte neu buchen.“
**Hinweis beim Einfügen:** `varVerlNaechste` wechselt den Typ (Datensatz aus der Collection statt aus der Liste). Zeigt Studio nach `btnVerwalten` einen roten Fehler bei `varVerlNaechste`, verschwindet er nach `btnVerwalten_2`.
**Test:** Eigene Buchung, die eine verfallene fremde überlappt → +1 Std geht. Eigene verfallene Buchung → +1 Std → Meldung. Zwei eigene Buchungen nacheinander an verschiedenen Tischen → die erste um 1 Std in die zweite hinein verlängern → „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“

**`btnVerwalten.OnSelect`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten` · **ganze Property ersetzen** · vorher: Gesamtplan G2

```
Set(varSelectedBuchung; ThisItem);;
Set(varVerlTisch; ThisItem.Tisch.Value);;
Set(varVerlEndeAlt; ThisItem.Endzeit);;
Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false)
```

**`btnVerwalten_2.OnSelect`** · Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2` · **ganze Property ersetzen** · vorher: Gesamtplan G2

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varVerlTisch; ThisItem.Tisch.Value);;
  Set(varVerlEndeAlt; ThisItem.Endzeit);;
  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
  RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

**`btnVerlängern.OnSelect`** · Ort: `Screen1 > conVerwaltenDialog > btnVerlängern` · **ganze Property ersetzen** · vorher: Gesamtplan G3

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
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
    ClearCollect(colVerlKonflikt; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
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
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerlängern_1.OnSelect`** · Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1` · **ganze Property ersetzen** · vorher: Gesamtplan G3

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
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
    ClearCollect(colVerlKonflikt; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
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
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**Rückfall F6:** Fassungen aus Anhang A wieder einsetzen.

### F7 Einchecken bis 30 Min nach Beginn, Auschecken beendet die Buchung

**Problem:** Einchecken ging bis zum Ende der Buchung. Mit der Freigabe könnte man um 11:00 einchecken, obwohl der Tisch seit 09:40 jemand anderem gehört. Auschecken setzte nur `CheckedIn` zurück, die Buchung blieb belegt.
**Lösung:**
- Einchecken nur von 30 Min vor Beginn bis zur Frist.
- Zusätzlich frisch prüfen, ob der Tisch in der Zeit schon an jemand anderen vergeben ist, und nach dem Einchecken noch einmal nachlesen (falls jemand in derselben Sekunde gebucht hat). Das verhindert eine **Doppelbelegung**, auch bei falsch gehender Uhr. Einen zu frühen Verlust durch eine vorgehende Uhr bei jemand anderem verhindert es nicht (U3).
- Auschecken nach Beginn: Ende = jetzt (auf die nächste Minute), der Tisch ist frei. Vor Beginn: nur Check-in zurücknehmen.
- Im Dashboard steht bei verfallenen Buchungen „Verfallen“ in Grau.

**Test:** Buchung in 1 Std → „erst ab 30 Minuten vor Beginn“. Laufende Buchung → „Eingecheckt.“, Kachel rot. Danach Auschecken → „endet um hh:mm, der Tisch ist wieder frei“, Kachel grün. Verfallene Buchung → „Zu spät …“, Status „Verfallen“.

**`btnEinchecken.OnSelect`** · Ort: `Screen1 > conCheckinDialog > btnEinchecken` · **ganze Property ersetzen** · vorher: Gesamtplan G5

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  Set(varCheckinTisch; varCheckinBuchung.Tisch.Value);;
  Set(varCheckinStart; varCheckinBuchung.Startzeit);;
  Set(varCheckinEnde; varCheckinBuchung.Endzeit);;
  If(
    IsBlank(varCheckinBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);;
    Set(varZeigeCheckin; false);
    varCheckinBuchung.CheckedIn && Now() < varCheckinStart;
    IfError(
      Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: false});
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
      If(
        !varSelectedBuchung.CheckedIn;
        Notify("Ausgecheckt. Die Buchung bleibt bestehen, bitte zum Beginn wieder einchecken."; NotificationType.Success);;
        Set(varZeigeCheckin; false);
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
      )
    );
    varCheckinBuchung.CheckedIn && DateAdd(Now(); 1; TimeUnit.Minutes) >= varCheckinEnde;
    Notify("Die Buchung endet ohnehin jetzt. Der Tisch ist gleich wieder frei."; NotificationType.Information);;
    Set(varZeigeCheckin; false);
    varCheckinBuchung.CheckedIn;
    Set(varCheckinNeuesEnde; DateAdd(Today(); Hour(Now()) * 60 + Minute(Now()) + 1; TimeUnit.Minutes));;
    IfError(
      Patch(Tischbuchungen; varCheckinBuchung; {Endzeit: varCheckinNeuesEnde});
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
      If(
        varSelectedBuchung.Endzeit < varCheckinEnde;
        Notify("Ausgecheckt. Deine Buchung endet um " & Text(varSelectedBuchung.Endzeit; "hh:mm") & " Uhr, der Tisch ist wieder frei."; NotificationType.Success);;
        Set(varZeigeCheckin; false);
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
      )
    );
    Now() < DateAdd(varCheckinStart; -30; TimeUnit.Minutes);
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich."; NotificationType.Warning);
    Now() >= varCheckinEnde;
    Notify("Diese Buchung ist schon zu Ende."; NotificationType.Warning);;
    Set(varZeigeCheckin; false);
    varCheckinStart <= varFreigabeGrenze && varCheckinBuchung.Erstellt <= varFreigabeGrenze;
    Notify("Zu spät: Ohne Check-in bis " & varFreigabeMinuten & " Minuten nach Beginn verfällt die Buchung, der Tisch ist wieder frei. Bitte neu buchen."; NotificationType.Warning);;
    Set(varZeigeCheckin; false);
    ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
    RemoveIf(colCheckinAndere; ID = varCheckinBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !IsEmpty(colCheckinAndere);
      Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen."; NotificationType.Error);;
      Set(varZeigeCheckin; false);
      IfError(
        Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: true});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
        ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
        RemoveIf(colCheckinAndere; ID = varCheckinBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
        If(
          varSelectedBuchung.CheckedIn && !IsEmpty(colCheckinAndere);
          Notify("Eingecheckt, aber der Tisch wurde gleichzeitig an jemand anderen vergeben. Bitte unter Buchungen prüfen und klären."; NotificationType.Error);;
          Set(varZeigeCheckin; false);
          varSelectedBuchung.CheckedIn;
          Notify("Eingecheckt."; NotificationType.Success);;
          Set(varZeigeCheckin; false);
          Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
        )
      )
    )
  );;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`lblStatusHeute.Text`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **ganze Property ersetzen** · vorher: Export 07.10.

```
If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; "Verfallen"; "Einchecken")
```

**`lblStatusHeute.Color`** · Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **ganze Property ersetzen** · vorher: Export 07.10.

```
If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; ColorValue("#A6A6A6"); ColorValue("#FFA500"))
```

**Rückfall F7:** Fassungen aus Anhang A wieder einsetzen.

### F8 Check-in-Erinnerung alle 5 Minuten

**Problem:** Wer die App morgens öffnet und offen lässt, bekommt keinen Hinweis, wenn die nächste Buchung ansteht.
**Lösung:** Der vorhandene 5-Minuten-Timer fragt zusätzlich nach dem Check-in. Bedingungen: Dashboard sichtbar, heutiger Tag, kein Dialog offen, und nur einmal je Buchung (`varCheckinGefragtID`). Wer die Frage wegklickt, wird für diese Buchung nicht noch einmal gefragt.
**Test:** App offen lassen, eigene Buchung mit Beginn in 20 Min (vorher angelegt) → spätestens nach 5 Min erscheint der Check-in-Dialog. Schließen → er kommt für diese Buchung nicht wieder.

**`tmrAktualisieren.OnTimerEnd`** · Ort: `(neu) Screen1 > tmrAktualisieren` · **ganze Property ersetzen** · vorher: Gesamtplan G8

```
If(
  !varIsLoading && !varZeigeDialog && !varZeigeTischBuchungForm && !varZeigeVerwalten && !varZeigeVerwaltenTab && !varZeigeVerwaltenKlein && !varZeigeCheckin && !varZeigeStornoFrage;
  If(
    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today();
    Set(varAnsichtsDatum; Today());;
    Reset(dpAnsichtsDatum)
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
  If(
    varAktiverTab = "dashboard" && varAnsichtsDatum = Today() && !varZeigeDetails && !varZeigeRaumBuchungForm;
    ClearCollect(colCheckinFrage; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()));;
    RemoveIf(colCheckinFrage; CheckedIn || (Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !IsEmpty(colCheckinFrage) && First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID <> varCheckinGefragtID;
      Set(varCheckinGefragtID; First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID);;
      Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinGefragtID));;
      Set(varZeigeCheckin; true)
    )
  )
)
```

**Rückfall F8:** Fassungen aus Anhang A wieder einsetzen.

## 5. Für den Handy-Chat (bitte weitergeben)
Die Handy-App liest dieselbe Liste. **Ohne dieselbe Regel passt es nicht zusammen:**
- Die Handy-App zeigt einen freigegebenen Tisch weiter als belegt. Das ist harmlos.
- Sie lässt aber das Einchecken einer verfallenen Buchung zu, auch wenn der Tisch schon neu vergeben ist. **Dann sitzen zwei Personen „eingecheckt“ am selben Tisch.**

Deshalb muss die Handy-App vor dem Teilen dasselbe tun. Die Einzelheiten stehen in `AUFTRAG_Handy_Freigabe.md`.

## 6. Testbogen Paket F

| ✓ | Test | Ergebnis | Notiz |
|---|---|---|---|
| ☐ | Vorbereitung Testmodus: in Studio einen **Testknopf** `btnTestFreigabe` einfügen, `OnSelect`: `Set(varFreigabeMinuten; 1)`. In der Vorschau einmal drücken. `App.OnStart` **nicht** ändern | | |
| ☐ | F1 App-Prüfung ohne rote Fehler (U1, U2) | | |
| ☐ | F1 Check-in-Frage beim Start erscheint bei anstehender Buchung, sonst nicht | | |
| ☐ | F2 Storno: Hintergrund dunkel, Klick daneben = Nein, richtige Buchung gelöscht (Dashboard, Tab, Mehrfach) | | |
| ☐ | F3 Verfallene Buchung (in SharePoint angelegt, Beginn vor 1 Std) → Kachel grün, Klick öffnet Buchungsdialog | | |
| ☐ | F4 Über die verfallene Buchung buchen → „Gebucht“, keine Warnung | | |
| ☐ | F5 Panel: Tisch ohne „belegt“, 5 Std wählbar | | |
| ☐ | F6 Verlängern über verfallene fremde Buchung geht, eigene verfallene → Meldung | | |
| ☐ | F7 Einchecken zu früh → Meldung; laufend → eingecheckt; Auschecken → Ende jetzt, Kachel grün; verfallen → „Zu spät“, Status grau | | |
| ☐ | F8 Erinnerung nach ≤ 5 Min, nur einmal | | |
| ☐ | U7: Monitor zeigt `Created` im `$select`. Spät gebucht (Handy-App, hh:20 für hh:00, Testmodus aus) → Kachel bis hh:50 orange | | |
| ☐ | **Testknopf `btnTestFreigabe` löschen.** In `App.OnStart` steht `Set(varFreigabeMinuten; 30)` | | |
| ☐ | Doppelklick auf Einchecken → eine Änderung | | |
| ☐ | Veröffentlichen | | |

## 7. Texte für Nutzer und Betrieb
Die neuen Fassungen liegen als eigene Dateien daneben, die alten bleiben erhalten:
- `KURZANLEITUNG_und_GoLive_Mail_v2.md`: Regel „bis 30 Min nach Beginn einchecken, sonst ist der Tisch weg“. Auschecken gibt den Tisch frei. „Ab sofort für den 14.10. buchen“. Kontakt per Mail statt Teams-Chat (solange es den Chat nicht gibt).
- `BETRIEBSHANDBUCH_Michael_v2.md`: kein Freigabe-Flow, „Verfallen“ erklärt. Überlappende Buchungen sind normal, wenn die ältere verfallen ist. Notbuchungen durch Michael kann die Person nicht selbst ändern.

## 8. UNSICHER (mit Test)

| Nr | Was | Test / Abhilfe |
|---|---|---|
| U1 | Studio nimmt die Spalte unter dem Anzeigenamen **`Erstellt`** an. Der Export führt `Created` mit Anzeigename „Erstellt“, und die App schreibt auch sonst Anzeigenamen (`CheckedIn` statt intern `Checkedin`), das ist belegt | Nach F1: App-Prüfung. Ist `Erstellt` rot, Claude Code melden: Der Generator setzt dann überall `Created` ein (ein Wort im Skript) |
| U2 | `DropColumns(…; "Erstellt")` mit Spaltenname als Text gilt bei `powerfxv1 = false` (wie `SortByColumns(…; "Startzeit")` in derselben App) | App-Prüfung nach F1. Rot → melden |
| U3 | Uhrzeiten der Geräte: Die Regel rechnet mit der Uhr des jeweiligen Geräts. Geht die Uhr bei jemandem vor, kann er über eine Buchung buchen, die noch nicht ganz verfallen ist. Der Besitzer bekommt dann beim Einchecken „schon vergeben“ und verliert den Tisch zu früh. Eine **Doppelbelegung** verhindert die Prüfung beim Einchecken (vorher und danach) | Firmengeräte gehen per Zeitserver auf Sekunden genau. Kein Test nötig |
| U4 | Position des Check-in-Dialogs beim App-Start: `conCheckinDialog.Y` richtet sich nach der Zeile in der Dashboard-Liste. Beim Start könnte die Liste noch laden | Test F1. Sitzt der Dialog falsch, wird er nach dem Laden richtig gesetzt (Formel reagiert). Sonst melden |
| U5 | Die Anzeige wechselt erst beim nächsten Laden von orange auf grün (Timer 5 Min, Aktualisieren-Symbol, jede Buchung). Der Klick auf die Kachel prüft immer frisch | gewollt, wie beim Flow (5 Min) |
| U7 | „Explizite Spaltenauswahl“ (in dieser App an, belegt): Power Apps lädt nur Spalten, die benutzt werden. `Erstellt` wird überall direkt benutzt (`RemoveIf(col; … Erstellt …)`, `B.Erstellt`, `ThisItem.Erstellt`), sollte also geladen werden. Fehlt die Spalte doch, ist sie leer, und nur „spät gebucht“ verliert die Schonfrist. Alles andere funktioniert | **Monitor:** Grundriss aktualisieren und Kachel anklicken, in der `getRows`-Anfrage auf `Tischbuchungen` muss `$select` die Spalte `Created` enthalten. **Praxistest:** in der Handy-App um hh:20 für hh:00 buchen (oder den Dialog vor hh:00 öffnen und nach hh:00 speichern), nicht einchecken → Kachel bleibt bis hh:50 orange |
| U6 | Testbuchungen „in der Vergangenheit“ kann die App nicht anlegen (Sperre). Für die Tests F3–F7 eine Zeile **direkt in der SharePoint-Liste** anlegen (Beginn vor 1 Std). `Erstellt` ist dann jetzt, die Frist läuft also erst 30 Min nach dem Anlegen ab | Testmodus mit einem **Testknopf** (Testbogen), **nicht** `App.OnStart` ändern |

## 9. Später (nicht in diesem Paket)
- **QR-Check-in** am Tisch über die Handy-App (`Param("tisch")`): verhindert das Einchecken von zu Hause. Braucht Aufkleber je Tisch.
- **No-Show-Auswertung:** In SharePoint eine Ansicht „Verfallen“ anlegen (Filter: CheckedIn = Nein, Startzeit < heute). Damit siehst du, wie oft Tische ungenutzt blockiert wurden.
- **Mail an No-Shows** (nur mit Flow, wenn gewünscht).
- **Aufräum-Flow (täglich 03:00, laut Doku vorhanden):** löscht Buchungen, die älter als 7 Tage sind, also auch die verfallenen. Wer No-Shows auswerten will, setzt die Frist dort hoch.

## Anhang A: Fassungen vor Paket F (für den Rückfall)

Je Property die Fassung, die nach dem Gesamtplan gilt (bzw. aus dem Export, wenn der Gesamtplan sie nicht ändert).

**`App.OnStart`** (Schritt F1, Gesamtplan G1)

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

**`btnStornieren.OnSelect`** (Schritt F2, Gesamtplan G4)

```
Set(varStornoQuelle; "dash");;
Set(varZeigeStornoFrage; true)
```

**`btnStornieren_1.OnSelect`** (Schritt F2, Gesamtplan G4)

```
Set(varStornoQuelle; "tab");;
Set(varZeigeStornoFrage; true)
```

**`btnStornoJa.OnSelect`** (Schritt F2, Gesamtplan G4)

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

**`btnHitArea.OnSelect`** (Schritt F3, Gesamtplan G7)

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

**`ddStockwerk.OnChange`** (Schritt F3, Export 07.10.)

```
Set(varAusgewaehltesStockwerk; ddStockwerk.Selected.Kurz);;
Set(varStockwerkDropdownOffen; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`dpAnsichtsDatum.OnChange`** (Schritt F3, Export 07.10.)

```
Set(varAnsichtsDatum; dpAnsichtsDatum.SelectedDate);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`Icon1_1.OnSelect`** (Schritt F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Icon1.OnSelect`** (Schritt F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Image6.OnSelect`** (Schritt F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnHitArea_1.OnSelect`** (Schritt F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnSpeichern.OnSelect`** (Schritt F4, Gesamtplan G6)

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

**`btnSpeichernTischePanel.OnSelect`** (Schritt F4, Gesamtplan G6)

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

**`btnTischHinzufügen.OnSelect`** (Schritt F5, Gesamtplan G7)

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

**`ddTischePanel.Items`** (Schritt F5, Gesamtplan G9)

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

**`btn5Std.DisplayMode`** (Schritt F5, Gesamtplan G10)

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

**`btn5Std.Fill`** (Schritt F5, Gesamtplan G10)

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

**`btn9Std.DisplayMode`** (Schritt F5, Gesamtplan G10)

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

**`btn9Std.Fill`** (Schritt F5, Gesamtplan G10)

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

**`btnVerwalten.OnSelect`** (Schritt F6, Gesamtplan G2)

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

**`btnVerwalten_2.OnSelect`** (Schritt F6, Gesamtplan G2)

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

**`btnVerlängern.OnSelect`** (Schritt F6, Gesamtplan G3)

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

**`btnVerlängern_1.OnSelect`** (Schritt F6, Gesamtplan G3)

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

**`btnEinchecken.OnSelect`** (Schritt F7, Gesamtplan G5)

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

**`lblStatusHeute.Text`** (Schritt F7, Export 07.10.)

```
If(ThisItem.CheckedIn; "Eingecheckt"; "Einchecken")
```

**`lblStatusHeute.Color`** (Schritt F7, Export 07.10.)

```
If(ThisItem.CheckedIn; ColorValue("#00A96B"); ColorValue("#FFA500"))
```

**`tmrAktualisieren.OnTimerEnd`** (Schritt F8, Gesamtplan G8)

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

## Anhang B: Maschinelle Prüfung

```
44 Properties in 8 Schritten, 1 neues Steuerelement.
Grundlage: Export 07.10. + Endfassungen Gesamtplan (23 Properties bauen auf dem Gesamtplan auf).
Ladezeile neu an 14 Stellen, alte Ladezeile an 0 Stellen.
Schreibstellen: 6 (btnEinchecken.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnStornoJa.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect), alle mit Zweifach-Sperre und neuer Ladezeile.
Abfragen auf Tischbuchungen (ohne reine ID-Abfragen, auch mehrzeilige): 42, jede einzeln geprüft: Freigabe-Regel lokal angewandt oder bewusst ausgenommen (3: eigene Listen und Mehrfach-Stornieren).
Je Property geprüft: Klammern, Rückübersetzung deutsch->englisch, keine Kommentare, Steuerelemente bekannt/neu, jede gelesene var/col wird gesetzt, varFreigabeGrenze vor Gebrauch gesetzt.
Jede Property kommt genau einmal vor.
Prüfung: 0 Fehler
```

Bewusst ohne Freigabe-Regel:

- `galTischbuchungenHeute.Items`: eigene Buchungen im Dashboard; die verfallene Buchung bleibt sichtbar (Status „Verfallen“)
- `galAlleTischbuchungen.Items`: eigene Buchungen im Tab; eine verfallene Buchung darf storniert werden
- `btnStornoJa.OnSelect#Person.Email = User().Email && Endzeit >= Now()`: Mehrfach-Stornieren eigener Buchungen; verfallene dürfen mit storniert werden
