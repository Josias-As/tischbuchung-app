# P4 Grundriss-Laden, Fassung 2 (Tischbuchung Desktop, 10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (`EINSETZPLAN.md`), **als letztes** einzufügen, in einer ruhigen Stunde. Grundlage: **Export 10.11. 08:13 + P0–P3**. K1–L4 sind **unverändert** aus Fassung 1 (13.10.), ihre Vorher-Fassungen passen auf den Export 10.11. genau (maschinell geprüft). Neu ist **L5**. Erzeugt und geprüft mit `werkzeuge/grundriss_laden.py` und `werkzeuge/abstimmung.py` (0 Fehler). **Nicht unabhängig geprüft** (Josias’ Entscheidung, 13.10.). In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Was es bringt:** Keine Kacheln mehr kurz oben links bei 0/0 beim Start (Stufe 1: L1 + L2). Wechsel OG↔UG sofort, weil alle Tische einmal gelesen und dann lokal gefiltert werden (Stufe 2: L3, dazu L4 als Kann). K1 macht die gewählte Zeile im Geschoss-Menü lesbar.
- **Neu in Fassung 2, L5 (Befund der Abstimmung):** Nach L3 liefert die Grundriss-Galerie Datensätze aus `TischeLokal` (`{ID; Titel; Geschoss; Gesperrt}`). „Neu buchen“ aus P3 füllte `varSelectedTisch` aber mit einem vollen Datensatz aus `Tische`. **Zwei Datensatz-Typen in einer Variable** (Regel aus dem Projekt, belegt durch frühere Fehler). L5 ändert in `btnNeuBuchenHeute.OnSelect` ein Wort: `LookUp(TischeLokal; …)` statt `LookUp(Tische; …)`. Damit liest „Neu buchen“ auch keine Liste mehr.
- **Gesperrt:** Mit L5 kennt „Neu buchen“ die Sperre wie die Kachel ab App-Start. Buchen geht trotzdem nicht, weil `btnSpeichern` frisch am Server prüft (belegt).
- **Umfang:** 6 Properties (`App.Formulas` zweimal: Stufe 1, dann Endfassung) + L5 = 7 Blöcke. Kein neues Steuerelement, keine neue Variable, kein Schreibzugriff.
- **Reihenfolge:** K1 jederzeit. L1 → L2 direkt hintereinander. Dann L3, L4. **L5 direkt nach L3** (vorher passt der Typ noch, nachher nicht mehr). Fehlt P3, entfällt L5.

## 1. Ursache und Bewertung des Plans
**Warum stehen Kacheln kurz bei 0/0?** (geschlussfolgert, nicht gemessen)
- `usenonblockingonstartrule` ist an (belegt, `Properties.json`). Der Bildschirm wird also gezeichnet, während `App.OnStart` noch läuft.
- `Rectangle1.X` ist `LookUp(colTischPositionen…; Tisch = ThisItem.Titel).X * BasisSkalierung` (belegt). Solange die Sammlung leer ist, ergibt das leer → 0. Die Breite fällt dann auf „hoch“ zurück, weil `Ausrichtung` leer ≠ „Horizontal“ ist. Man sieht also hochkant stehende Kacheln oben links. Das passt zur Beobachtung.
- Benannte Formeln sind nie „noch nicht gesetzt“. Sie werden berechnet, sobald eine Kachel sie braucht. Microsoft empfiehlt sie genau dafür statt Sammlungen in `App.OnStart` (App-Prüfung, belegt; Microsoft-Seite „Große Apps“, Websuche).

**Warum ist der erste Wechsel OG↔UG langsam?** (geschlussfolgert)
- `Gallery1.Items = Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)` und `TischNrOG`/`TischNrUG` fragen je Geschoss am Server ab. Beim ersten Mal wird geladen, danach kommt das Ergebnis aus dem Zwischenspeicher.
- `ddStockwerk.OnChange` lädt außerdem `colGrundriss` neu (Ladezeile, belegt). Das bleibt so. Die Kacheln stehen sofort da, die Farben kommen mit der Antwort.

**Antworten auf die Fragen aus der Übergabe (Abschnitt 3):**

| Frage | Antwort |
|---|---|
| Plan tragfähig? | Ja. Positionen als benannte Formeln: ja. `colTische` ersetze ich durch die benannte Formel `TischeLokal`, Gründe in der Kurzfassung |
| Fallen bei benannten Formeln | (a) **Gleicher Name wie die alte Sammlung.** Zwischen L1 und L2 meldet Studio kurz „Name unbekannt“ an `Rectangle1`/`conDetailsPopup`. Das ist erwartet, nach L2 ist es weg (U2). (b) **Schreibgeschützt:** Niemand außer `App.OnStart` schreibt die Positionen (maschinell geprüft), also passt es. (c) **Abschlusszeichen:** jede Definition mit `;;` wie im Export, maschinell gezählt. (d) **Tabellenliteral:** gleiche Spalten und Werte, nur `Table(…)` statt `ClearCollect(…)`. `LookUp` darauf aus `Rectangle1.*` und `conDetailsPopup.*` funktioniert wie mit einer Sammlung (geschlussfolgert, Test 2/3) |
| Zwischenzustand beim Start | **Stufe 1:** Positionen sind immer da. Kacheln erscheinen, sobald `Tische` geantwortet hat, und gleich an der richtigen Stelle. **Stufe 2:** Bis `TischeLokal` geladen ist, ist die Galerie leer (keine Kachel statt falscher Kachel). Danach kommen Kacheln, `Nr` und Positionen **gleichzeitig**, weil Galerie und `TischNr` dieselbe Quelle haben. Fehler wirft das nicht (leerer `Filter`) |
| Schutz nötig (`Gallery1.Visible`)? | Nein. Eine leere Galerie zeigt nichts. Eine Sperre über `varJetztTakt` würde die Kacheln erst nach dem ganzen `App.OnStart` zeigen, also später. Nicht in v1 (U6) |
| Reihenfolge / `Nr` | Heute stammen `Nr` und Galerie aus zwei getrennten Server-Abfragen, beide ohne Sortierung, also nach ID. Künftig stammen beide aus **derselben** Tabelle und können nicht mehr auseinanderlaufen. Bleibt die Reihenfolge der Liste gleich (nach ID, geschlussfolgert), ändert sich keine Kachel um einen Pixel. Test 5 prüft das gegen Bildschirmfotos (U5) |
| Wirkung auf **Gesperrt** | Gleich wie heute: Stand beim App-Start (Betriebshandbuch). Ein frisch gesperrter Tisch ist bis zum Neustart grün. **Buchen geht trotzdem nicht**, weil `btnSpeichern`/`btnSpeichernTischePanel` frisch am Server prüfen (`LookUp(Tische; ID = varNeuTischID && Gesperrt = true)`, belegt). Test 8 |
| Typen | `varSelectedTisch` und `varDetailsTisch` wurden im Export 13.10. nur aus `ThisItem` der Galerie oder mit `Blank()` gefüllt (belegt). **Seit P3 füllt auch „Neu buchen“ `varSelectedTisch`, deshalb L5.** Danach gibt es wieder nur einen Datensatz-Typ (maschinell geprüft). Gelesen werden nur `ID`, `Titel`, `Geschoss`, `Gesperrt` (maschinell). Die liefert `TischeLokal` |
| Alternativen | (1) **Nur Positionen** = Stufe 1 allein. Löst 0/0, der erste Wechsel bleibt langsam. (2) **Nur `colTische`**, ohne benannte Positionen: löst 0/0 nicht sicher, weil die Positionen weiter von `App.OnStart` abhängen. (3) **`colTische` wie vorgeschlagen:** geht auch, aber mit neuer Start-Abhängigkeit, Prüfhinweis und offener Frage zu Formeln über Sammlungen. (4) **Später, Backlog:** echte Bild-Y-Werte in die Positionen, dann braucht `Rectangle1.Y` die Reihenfolge der Liste nicht mehr |
| Aufwand/Nutzen vor dem Go-Live | Nutzen klein (ca. 1 s beim Start, erster Wechsel sofort, kein Sprung). Risiko: `App.Formulas` und `App.OnStart` sind die zwei Properties, an denen der ganze Grundriss hängt. **Nach dem Go-Live**, ich stimme Claude Code zu. Ausnahme: K1 (nur eine Farbe) |

## 2. Einfügen
1. **Sicherung:** Datei → Speichern unter → Diesen Computer (`.msapp`). Bildschirmfotos für Test 5 machen, **bevor** etwas geändert wird (Test 0).
2. Reihenfolge: **K1** · **L1 → L2** direkt hintereinander, dann Tests 1–3 · **L3** (erst `App.Formulas`, dann `Gallery1.Items`) · **sofort L5** · dann Tests 4–8 und L5-Test · **L4** (Kann), dann Test 9.
3. Nach jedem Schritt die App-Prüfung ansehen: keine roten Fehler. Ausnahme: zwischen L1 und L2 kurz Fehler an `Rectangle1`/`conDetailsPopup` (siehe L1).
4. `App.Formulas` liegt in Studio bei **App** → Property-Liste oben links → `Formulas`. Den ganzen Inhalt markieren (Strg+A) und ersetzen.
5. Erst nach Test 10 veröffentlichen.

## 3. Schritte

### K1 Auswahlfarbe der Geschoss-Auswahl lesbar

**Befund 1 aus der Übergabe (belegt):** Die gewählte Zeile im Geschoss-Menü hat weiße Schrift auf Hellgrau `RGBA(196, 196, 203)`. Der Kontrast liegt bei **1,7 : 1** (gerechnet, WCAG verlangt 4,5 : 1). Mit `RGBA(32, 54, 71)`, dem Dunkelblau der App (`Gallery1.BorderColor`, `ddTischePanel.BorderColor`), sind es **7,2 : 1**.

**Test:** Geschoss-Menü öffnen. Die gewählte Zeile ist dunkel beschriftet und gut lesbar.
**Rückfall:** `RGBA(255; 255; 255; 1)`.

#### `ddStockwerk.SelectionColor`

Ort: `Screen1 > conGrundriss > ddStockwerk` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-RGBA(255; 255; 255; 1)
+RGBA(32; 54; 71; 1)
```

Vollständiger Block:

```
RGBA(32; 54; 71; 1)
```

### L1 App.OnStart: Positionen herausnehmen

**Was:** Die zwei Blöcke `ClearCollect(colTischPositionen; …)` und `ClearCollect(colTischPositionenUG; …)` werden entfernt. Sonst ändert sich nichts: gleiche Reihenfolge, Ladezeile unverändert, `Set(varJetztTakt; Now())` bleibt die letzte Anweisung (maschinell geprüft).

**Erwartet:** Direkt danach zeigt die App-Prüfung Fehler an `Rectangle1.X/Y/Width/Height` und `conDetailsPopup.X/Y` („Name ist ungültig“), weil die Namen kurz fehlen. **Sofort mit L2 weitermachen**, nichts dazwischen speichern oder veröffentlichen.

**Rückfall:** Originalfassung aus Anhang A.

#### `App.OnStart`

Ort: `App` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -51,21 +51,2 @@
 Set(varWiederholenBisGewaehlt; false);;
-ClearCollect(
-  colTischPositionen;
-  {Tisch: "OG Desk 1"; X: 1380; Y: 270; Ausrichtung: "Vertikal"};
-  {Tisch: "OG Desk 2"; X: 1629; Y: 290; Ausrichtung: "Horizontal"};
-  {Tisch: "OG Desk 3"; X: 1732; Y: 288; Ausrichtung: "Horizontal"};
-  {Tisch: "OG Desk 4"; X: 1629; Y: 348; Ausrichtung: "Horizontal"};
-  {Tisch: "OG Desk 5"; X: 1732; Y: 346; Ausrichtung: "Horizontal"};
-  {Tisch: "OG Desk 6"; X: 1734; Y: 536; Ausrichtung: "Horizontal"};
-  {Tisch: "OG Desk 7"; X: 1734; Y: 596; Ausrichtung: "Horizontal"};
-  {Tisch: "OG Desk 8"; X: 1500; Y: 484; Ausrichtung: "Vertikal"};
-  {Tisch: "OG Desk 9"; X: 1500; Y: 584; Ausrichtung: "Vertikal"};
-  {Tisch: "OG Desk 10"; X: 1500; Y: 683; Ausrichtung: "Vertikal"};
-  {Tisch: "OG Desk 11"; X: 1560; Y: 468; Ausrichtung: "Vertikal"};
-  {Tisch: "OG Desk 12"; X: 1560; Y: 582; Ausrichtung: "Vertikal"};
-  {Tisch: "OG Desk 13"; X: 1560; Y: 681; Ausrichtung: "Vertikal"};
-  {Tisch: "Quiet Desk 3"; X: 870; Y: 687; Ausrichtung: "Vertikal"};
-  {Tisch: "Quiet Desk 2"; X: 870; Y: 594; Ausrichtung: "Vertikal"};
-  {Tisch: "Quiet Desk 1"; X: 870; Y: 501; Ausrichtung: "Vertikal"}
-);;
 Set(varSelectedBuchungTab; Blank());;
@@ -86,24 +67,2 @@
 Set(varGeklickteBuchungKlein; Blank());;
-ClearCollect(
-  colTischPositionenUG;
-  {Tisch: "UG Desk 1";  X: 530;  Y: 592; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 2";  X: 530;  Y: 679; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 3";  X: 582;  Y: 588; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 4";  X: 582;  Y: 675; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 5";  X: 738;  Y: 584; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 6";  X: 738;  Y: 671; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 7";  X: 790;  Y: 579; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 8";  X: 790;  Y: 666; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 9";  X: 1011; Y: 575; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 10"; X: 1011; Y: 662; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 11"; X: 1063; Y: 571; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 12"; X: 1063; Y: 658; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 13"; X: 1202; Y: 260; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 14"; X: 1202; Y: 337; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 16"; X: 1255; Y: 346; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 15"; X: 1255; Y: 258; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 17"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
-  {Tisch: "UG Desk 18"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
-  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
-);;
 Set(varIsLoading; false);;
```

Vollständiger Block:

```
Set(varFreigabeMinuten; 30);;
Set(varCheckinGefragtID; 0);;
Set(varAuscheckFrageID; 0);;
Set(varGrundrissSperreSekunden; 120);;
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
Set(varSelectedBuchungTab; Blank());;
Set(varZeigeVerwaltenTab; false);;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varAnsichtsDatum; Today());;
Set(varAusgewaehltesStockwerk; "UG");;
Set(varStockwerkDropdownOffen; false);;
Set(varStartOverride; "");;
Set(varEndeOverride; "");;
Clear(colAusgewaehlteBuchungen);;
Set(varMehrfachAuswahlModus; false);;
Set(varAuswahlModusAktiv; false);;
Set(varZeigeVerwaltenKlein; false);;
Set(varGalleryNeuAufbauen; 0);;
Set(varGeklickteBuchungKlein; Blank());;
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
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
Set(varJetztTakt; Now())
```

### L2 App.Formulas Stufe 1: Positionen als benannte Formeln

**Was:** Am Ende von `App.Formulas` kommen die zwei Positionstabellen dazu, gleiche Namen, Werte 1:1 aus `App.OnStart` (maschinell verglichen, 16 OG + 19 UG). Alles andere bleibt zeichengleich.

**Tests (nach L1 + L2):**
1. App-Prüfung: keine roten Fehler. Die zwei Hinweise „Die Sammlung wird initialisiert, aber nie aktualisiert“ (Leistung) sind weg.
2. **Speichern, Studio schließen und die App neu öffnen** (dann läuft `App.OnStart` wie beim Start). Beim Aufbau steht **keine Kachel oben links**. Die Kacheln stehen wie auf den Fotos aus Test 0 (UG, dann OG).
3. Eine freie Kachel antippen: Buchungsdialog mit Tischname und „… MMS Untergeschoss“. Schließen. Eine belegte Kachel antippen: Das Details-Fenster erscheint neben der Kachel.

**Rückfall:** `App.Formulas` aus Anhang A, dann `App.OnStart` aus Anhang A (in dieser Reihenfolge, dazwischen kurz Fehler).

#### `App.Formulas` (Stufe 1)

Ort: `App` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -24 +24,42 @@
 BasisSkalierungReferenz = Min(881 / BasisBreite; 678 / BasisHoehe);;
+// Grundriss-Laden 2026-10-13: Positionen als benannte Formeln statt ClearCollect in App.OnStart.
+// Werden berechnet, wenn eine Kachel sie braucht, also nie leer (keine Kacheln bei 0/0 beim Start). Werte unverändert aus App.OnStart.
+colTischPositionen = Table(
+  {Tisch: "OG Desk 1"; X: 1380; Y: 270; Ausrichtung: "Vertikal"};
+  {Tisch: "OG Desk 2"; X: 1629; Y: 290; Ausrichtung: "Horizontal"};
+  {Tisch: "OG Desk 3"; X: 1732; Y: 288; Ausrichtung: "Horizontal"};
+  {Tisch: "OG Desk 4"; X: 1629; Y: 348; Ausrichtung: "Horizontal"};
+  {Tisch: "OG Desk 5"; X: 1732; Y: 346; Ausrichtung: "Horizontal"};
+  {Tisch: "OG Desk 6"; X: 1734; Y: 536; Ausrichtung: "Horizontal"};
+  {Tisch: "OG Desk 7"; X: 1734; Y: 596; Ausrichtung: "Horizontal"};
+  {Tisch: "OG Desk 8"; X: 1500; Y: 484; Ausrichtung: "Vertikal"};
+  {Tisch: "OG Desk 9"; X: 1500; Y: 584; Ausrichtung: "Vertikal"};
+  {Tisch: "OG Desk 10"; X: 1500; Y: 683; Ausrichtung: "Vertikal"};
+  {Tisch: "OG Desk 11"; X: 1560; Y: 468; Ausrichtung: "Vertikal"};
+  {Tisch: "OG Desk 12"; X: 1560; Y: 582; Ausrichtung: "Vertikal"};
+  {Tisch: "OG Desk 13"; X: 1560; Y: 681; Ausrichtung: "Vertikal"};
+  {Tisch: "Quiet Desk 3"; X: 870; Y: 687; Ausrichtung: "Vertikal"};
+  {Tisch: "Quiet Desk 2"; X: 870; Y: 594; Ausrichtung: "Vertikal"};
+  {Tisch: "Quiet Desk 1"; X: 870; Y: 501; Ausrichtung: "Vertikal"}
+);;
+colTischPositionenUG = Table(
+  {Tisch: "UG Desk 1";  X: 530;  Y: 592; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 2";  X: 530;  Y: 679; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 3";  X: 582;  Y: 588; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 4";  X: 582;  Y: 675; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 5";  X: 738;  Y: 584; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 6";  X: 738;  Y: 671; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 7";  X: 790;  Y: 579; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 8";  X: 790;  Y: 666; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 9";  X: 1011; Y: 575; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 10"; X: 1011; Y: 662; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 11"; X: 1063; Y: 571; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 12"; X: 1063; Y: 658; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 13"; X: 1202; Y: 260; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 14"; X: 1202; Y: 337; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 16"; X: 1255; Y: 346; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 15"; X: 1255; Y: 258; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 17"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
+  {Tisch: "UG Desk 18"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
+  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
+);;
```

Vollständiger Block:

```
BasisBreite = 1920;;
BasisHoehe = 1080;;
BasisSkalierung = Min(conGrundriss.Width / BasisBreite; conGrundriss.Height / BasisHoehe);;
BasisKachelbreiteQuer = 101;;
BasisKachelhoeheQuer = 60;;
BasisKachelbreiteHoch = 60;;
BasisKachelhoeheHoch = 101;;
BasisKreisgroesse = 45;;
btnAbstand = 6;;
btnBreite = Min(80; Max(44; (conVerwaltenDialog_1.Width - 5*btnAbstand - 40) / 6));;
BasisKachelbreiteHochUG = 52;;
BasisKachelhoeheHochUG = 89;;
BasisKachelbreiteQuerUG = 89;;
BasisKachelhoeheQuerUG = 52;;
BasisKreisgroesseUG = 39;;
BasisSchriftgroesseUG = 11;;
// Josias 2026-09-28: eigene Breite fuer Big Table UG, deutlich breiter als Standardtisch, Hoehe bleibt Basishoehe horizontal
BasisKachelbreiteBigTableUG = 220;;

// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
TischNrOG = With({src: Filter(Tische; Geschoss.Value = "OG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
TischNrUG = With({src: Filter(Tische; Geschoss.Value = "UG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
// Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
BasisSkalierungReferenz = Min(881 / BasisBreite; 678 / BasisHoehe);;
// Grundriss-Laden 2026-10-13: Positionen als benannte Formeln statt ClearCollect in App.OnStart.
// Werden berechnet, wenn eine Kachel sie braucht, also nie leer (keine Kacheln bei 0/0 beim Start). Werte unverändert aus App.OnStart.
colTischPositionen = Table(
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
colTischPositionenUG = Table(
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
  {Tisch: "UG Desk 14"; X: 1202; Y: 337; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 16"; X: 1255; Y: 346; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 15"; X: 1255; Y: 258; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 17"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 18"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
);;
```

### L3 Stufe 2: Tische einmal lokal laden

**Was:**
- `App.Formulas` (Endfassung, Diff gegen Stufe 1): Neu ist `TischeLokal = ForAll(Tische As T; {ID: …; Titel: …; Geschoss: …; Gesperrt: …})`. `TischNrOG` und `TischNrUG` lesen daraus statt aus `Tische`. Sonst bleibt alles zeichengleich.
- `Gallery1.Items` liest aus `TischeLokal`.
- **Reihenfolge:** erst `App.Formulas`, dann `Gallery1.Items`.

**Tests (nach L3):**
4. App-Prüfung: keine roten Fehler, kein neuer Delegierungshinweis an `App.Formulas`. App neu öffnen (wie Test 2). Dann **sofort** auf OG wechseln: Die Kacheln stehen sofort da. Das Bild selbst kann beim allerersten Mal einen Moment brauchen (U4). Mehrmals hin und her wechseln.
5. **Positionen gegen die Fotos aus Test 0**, beide Geschosse und beide Fenstergrößen. Besonders UG Desk 13–18 und OG Desk 6–13 ansehen. Weicht eine Kachel um ein paar Pixel nach oben oder unten ab, ist die Reihenfolge anders (U5) → Rückfall Stufe 2, Foto an mich.
6. Im Grundriss das Datum auf morgen stellen: Die Farben ändern sich, die Positionen nicht.
7. Am Grundriss **UG Desk 14** für morgen 08:00–09:00 buchen. Die Kachel wird für morgen orange, die Buchung steht in der Liste. Danach stornieren.
8. **Gesperrt** (nur Josias, an einem Tisch ohne Buchungen, z. B. UG Desk 18):
   1. In SharePoint `Gesperrt` = Ja setzen. Die App bleibt offen.
   2. Die Kachel ist noch grün, wie heute. Antippen → Dialog → Speichern: Die App meldet, dass der Tisch gesperrt ist, und es entsteht keine Buchung.
   3. App neu öffnen: Die Kachel ist grau, Antippen meldet „gesperrt“.
   4. In SharePoint `Gesperrt` = Nein setzen, App neu öffnen.

**Rückfall Stufe 2:** `App.Formulas` = Block aus L2 (Stufe 1), dann `Gallery1.Items` = `Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)`.

#### `App.Formulas` (Endfassung)

Ort: `App` · **ganze Property ersetzen**

Änderung gegenüber Stufe 1 (L2) (`-` alt, `+` neu):

```diff
@@ -19,5 +19,8 @@
 
+// Grundriss-Laden 2026-10-13: alle Tische einmal lesen (ForAll = eine Abfrage, danach lokal). Gallery1, TischNrOG/UG und ddTischePanel lesen daraus.
+// Reihenfolge = Reihenfolge der Liste (nach ID), wie bisher beim Filtern auf Tische. Gesperrt gilt wie bisher ab App-Start.
+TischeLokal = ForAll(Tische As T; {ID: T.ID; Titel: T.Titel; Geschoss: T.Geschoss; Gesperrt: T.Gesperrt});;
 // Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
-TischNrOG = With({src: Filter(Tische; Geschoss.Value = "OG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
-TischNrUG = With({src: Filter(Tische; Geschoss.Value = "UG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
+TischNrOG = With({src: Filter(TischeLokal; Geschoss.Value = "OG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
+TischNrUG = With({src: Filter(TischeLokal; Geschoss.Value = "UG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
 // Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
```

Vollständiger Block:

```
BasisBreite = 1920;;
BasisHoehe = 1080;;
BasisSkalierung = Min(conGrundriss.Width / BasisBreite; conGrundriss.Height / BasisHoehe);;
BasisKachelbreiteQuer = 101;;
BasisKachelhoeheQuer = 60;;
BasisKachelbreiteHoch = 60;;
BasisKachelhoeheHoch = 101;;
BasisKreisgroesse = 45;;
btnAbstand = 6;;
btnBreite = Min(80; Max(44; (conVerwaltenDialog_1.Width - 5*btnAbstand - 40) / 6));;
BasisKachelbreiteHochUG = 52;;
BasisKachelhoeheHochUG = 89;;
BasisKachelbreiteQuerUG = 89;;
BasisKachelhoeheQuerUG = 52;;
BasisKreisgroesseUG = 39;;
BasisSchriftgroesseUG = 11;;
// Josias 2026-09-28: eigene Breite fuer Big Table UG, deutlich breiter als Standardtisch, Hoehe bleibt Basishoehe horizontal
BasisKachelbreiteBigTableUG = 220;;

// Grundriss-Laden 2026-10-13: alle Tische einmal lesen (ForAll = eine Abfrage, danach lokal). Gallery1, TischNrOG/UG und ddTischePanel lesen daraus.
// Reihenfolge = Reihenfolge der Liste (nach ID), wie bisher beim Filtern auf Tische. Gesperrt gilt wie bisher ab App-Start.
TischeLokal = ForAll(Tische As T; {ID: T.ID; Titel: T.Titel; Geschoss: T.Geschoss; Gesperrt: T.Gesperrt});;
// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
TischNrOG = With({src: Filter(TischeLokal; Geschoss.Value = "OG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
TischNrUG = With({src: Filter(TischeLokal; Geschoss.Value = "UG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
// Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
BasisSkalierungReferenz = Min(881 / BasisBreite; 678 / BasisHoehe);;
// Grundriss-Laden 2026-10-13: Positionen als benannte Formeln statt ClearCollect in App.OnStart.
// Werden berechnet, wenn eine Kachel sie braucht, also nie leer (keine Kacheln bei 0/0 beim Start). Werte unverändert aus App.OnStart.
colTischPositionen = Table(
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
colTischPositionenUG = Table(
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
  {Tisch: "UG Desk 14"; X: 1202; Y: 337; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 16"; X: 1255; Y: 346; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 15"; X: 1255; Y: 258; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 17"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 18"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
);;
```

#### `Gallery1.Items`

Ort: `Screen1 > conGrundriss > Gallery1` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)
+Filter(TischeLokal; Geschoss.Value = varAusgewaehltesStockwerk)
```

Vollständiger Block:

```
Filter(TischeLokal; Geschoss.Value = varAusgewaehltesStockwerk)
```

### L5 „Neu buchen“ liest den Tisch aus TischeLokal (gleicher Typ wie die Grundriss-Kachel)

**Was:** In `btnNeuBuchenHeute.OnSelect` wird nur `Tische` durch `TischeLokal` ersetzt. Sonst nichts (maschinell geprüft).
- Danach füllen alle Setzer von `varSelectedTisch` denselben Typ: `ThisItem` der Galerie (`TischeLokal`), `varNeuBuchenTisch` (`TischeLokal`) oder `Blank()` (maschinell geprüft). Gelesen werden nur `ID`, `Titel`, `Geschoss`, `Gesperrt`, die `TischeLokal` alle hat.

**Test (L5):** App-Prüfung ohne Fehler an `varSelectedTisch`/`btnNeuBuchenHeute`. Dann Einsetzplan Teil A Test 9 wiederholen (mit Testknopf): „Neu buchen“ öffnet den Dialog mit dem richtigen Tisch und Geschoss (wie beim Antippen der Kachel), Speichern bucht.

**Rückfall:** Anhang A (`LookUp(Tische; …)`). Nur zusammen mit Stufe 2 zurücknehmen, sonst entsteht der Typ-Konflikt umgekehrt.

#### `btnNeuBuchenHeute.OnSelect`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnNeuBuchenHeute` · **ganze Property ersetzen**

Änderung gegenüber P3 (Nachtrag 6 v2) (`-` alt, `+` neu):

```diff
@@ -2,3 +2,3 @@
   !varIsLoading;
-  Set(varNeuBuchenTisch; LookUp(Tische; Titel = ThisItem.Tisch.Value));;
+  Set(varNeuBuchenTisch; LookUp(TischeLokal; Titel = ThisItem.Tisch.Value));;
   If(
```

Vollständiger Block:

```
If(
  !varIsLoading;
  Set(varNeuBuchenTisch; LookUp(TischeLokal; Titel = ThisItem.Tisch.Value));;
  If(
    IsBlank(varNeuBuchenTisch.ID);
    Notify("Diesen Tisch gibt es nicht mehr."; NotificationType.Warning);
    varNeuBuchenTisch.Gesperrt;
    Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
    Set(varSelectedTisch; varNeuBuchenTisch);;
    Set(varDialogJetzt; Now());;
    Reset(tglFuerAndere);;
    Reset(txtGastName);;
    Set(varFbTrotzdem; false);;
    Set(varEndeOverride; Text(ThisItem.Endzeit; "hh:mm"));;
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
  )
)
```

### L4 Kann: Tischliste im Panel liest dieselben Tische

**Was:** Die Tischliste im Panel („Tisch buchen“) liest `TischeLokal` statt `Tische`. Es ist genau ein Wort. Felder, Filter und Sortierung bleiben gleich.

**Warum Kann:** Die Formel wird auch bei geschlossenem Panel berechnet und liest heute beim Start alle Tische ein zweites Mal (geschlussfolgert, „unsichtbar ≠ nicht berechnet“). Mit L4 bleibt es bei der einen Abfrage. `Gesperrt` gilt auch hier ab App-Start, wie heute. Beim Speichern prüft die App frisch.

**Test:**
9. Panel öffnen, heute, eine freie Zeit: Die Liste zeigt alle buchbaren Tische, ohne Big Table und ohne gesperrte, gleiche Sortierung wie vorher (vor dem Einfügen ein Foto machen). Einen Tisch über das Panel buchen und wieder stornieren.

**Rückfall:** Original aus Anhang A (`Tische As Ti`).

#### `ddTischePanel.Items`

Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -36,3 +36,3 @@
             ForAll(
-              Tische As Ti;
+              TischeLokal As Ti;
               With(
```

Vollständiger Block:

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
              TischeLokal As Ti;
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

## 4. Testbogen (Zeitachse)
| Zeit | Schritt | Test |
|---|---|---|
| vorher | **Test 0:** Sicherung `.msapp`. Bildschirmfotos des Grundrisses UG und OG im **Vollbild** und in einem **halb so breiten** Fenster. Dazu ein Foto der Panel-Tischliste (heute, eine freie Zeit). Optional Monitor starten (Studio → Erweiterte Tools → Monitor) und beim Start die Zeilen mit `Tische` zählen | Fotos liegen vor |
| K1 | Farbe | K1-Test |
| L1 + L2 | Positionen | Tests 1–3 |
| L3 + L5 | Tische lokal, Neu buchen | Tests 4–8, L5-Test |
| L4 | Panel-Liste | Test 9 |
| danach | **Test 10:** Monitor beim Start: `Tische` wird **einmal** abgefragt. Beim Wechsel aufs OG gibt es keine `Tische`-Abfrage. Dann veröffentlichen und im Browser mit Strg+F5 neu laden: keine Kachel oben links | Abfragen wie erwartet |
| danach | **Test 11:** Handy-Gegenprobe: am Handy einen Tisch buchen, am PC „Aktualisieren“. Die Kachel wird orange (Weg unverändert, nur zur Sicherheit) | wie vorher |

Gezählt wird beim Start, nicht beim Speichern. Testbuchungen danach stornieren. `Gesperrt` am Ende wieder auf Nein.

## 5. Rückfall (gesamt)
- **Einzelschritte:** jeweils unter dem Schritt. Die Originale stehen in Anhang A.
- **Alles auf einmal:** make.powerapps.com → App → … → Details → **Versionen** → letzte Version vor der Änderung → **Wiederherstellen**. Oder die `.msapp`-Sicherung öffnen und veröffentlichen.
- Was nach dem Rückfall gilt: Die App verhält sich wie im Export 13.10. (0/0-Sprung beim Start, erster Wechsel lädt).

## 6. UNSICHER
| Nr | Was | Prüfen / Folge |
|---|---|---|
| U1 | `ForAll(Tische As T; {…})` in einer **benannten Formel**: Wird sie einmal geladen und dann wiederverwendet? Benannte Formeln mit `Tische` gibt es schon (`TischNrOG/UG`, belegt), mit `ForAll` noch nicht | Test 4 (App-Prüfung) und Test 10 (Monitor). Meldet Studio einen Fehler an `TischeLokal` oder fragt `Tische` öfter als einmal ab → Rückfall Stufe 2. Stufe 1 bleibt und löst 0/0 trotzdem |
| U2 | Benannte Formel mit demselben Namen wie die gerade entfernte Sammlung | Bleiben nach L2 Fehler an `Rectangle1`/`conDetailsPopup` stehen: speichern, Studio schließen und neu öffnen. Bleiben sie dann noch → Rückfall Stufe 1, mir die Fehlermeldung schicken |
| U3 | Ursache 0/0 ist geschlussfolgert, nicht gemessen | Test 2. Springen die Kacheln nach Stufe 1 weiter → Bildschirmvideo an mich. Möglich wäre dann noch `BasisSkalierung` beim Aufbau |
| U4 | Das OG-Bild (PNG, ca. 430 KB) ist beim Start unsichtbar und wird erst beim ersten Wechsel angezeigt. Ob der Browser es vorher lädt, steht nicht im Export | Test 4. Erscheinen die Kacheln sofort und das Bild kurz danach, liegt das am Bild, nicht an den Daten. Das lässt sich mit Formeln kaum ändern |
| U5 | `ForAll(Tische)` und `Filter(Tische; Geschoss…)` liefern dieselbe Reihenfolge (nach ID). Gestützt durch die REST-Reihenfolge vom 12.10. (nach ID, 35 Zeilen) | Test 5. Bei Abweichung verschiebt sich eine Kachel um ca. 1 Pixel je Platz in der Reihenfolge (geschlussfolgert aus `Rectangle1.Y`) |
| U6 | Kacheln können beim Start kurz **grün** sein, bevor `colGrundriss` geladen ist (Ladezeile am Ende von `App.OnStart`). Das ist heute schon so und wird nicht geändert | beobachten. Wenn es stört: später `Gallery1.Items` an `varJetztTakt` koppeln (zeigt Kacheln erst nach `App.OnStart`) |
| U7 | Scheitert das Laden von `Tische` (Netz), bleibt der Grundriss leer, ohne Meldung. Heute ist es ähnlich | App neu öffnen. Benannte Formeln dürfen kein `Notify` enthalten, deshalb gibt es keine Meldung |
| U8 | L5: `LookUp` auf eine benannte Formel mit `ForAll` im OnSelect einer Galerie-Karte (geschlussfolgert: geht wie auf jede Tabelle) | L5-Test |

## 7. Unabhängige Prüfung
Auf Josias’ Wunsch (13.10.) **keine unabhängige Prüfung**. Die begonnene Prüfung wurde abgebrochen, bevor sie einen Bericht geschrieben hat. Geprüft ist nur maschinell (Anhang B) und durch meine eigene Durchsicht. Umso wichtiger sind Test 0 (Fotos vorher) und Test 5 (Positionen gegen die Fotos).

## Anhang A: Originale (Rückfall)

**`ddStockwerk.SelectionColor`**

```
RGBA(255; 255; 255; 1)
```

**`App.OnStart`**

```
Set(varFreigabeMinuten; 30);;
Set(varCheckinGefragtID; 0);;
Set(varAuscheckFrageID; 0);;
Set(varGrundrissSperreSekunden; 120);;
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
Set(varAusgewaehltesStockwerk; "UG");;
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
  {Tisch: "UG Desk 14"; X: 1202; Y: 337; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 16"; X: 1255; Y: 346; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 15"; X: 1255; Y: 258; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 17"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 18"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
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
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
Set(varJetztTakt; Now())
```

**`App.Formulas`**

```
BasisBreite = 1920;;
BasisHoehe = 1080;;
BasisSkalierung = Min(conGrundriss.Width / BasisBreite; conGrundriss.Height / BasisHoehe);;
BasisKachelbreiteQuer = 101;;
BasisKachelhoeheQuer = 60;;
BasisKachelbreiteHoch = 60;;
BasisKachelhoeheHoch = 101;;
BasisKreisgroesse = 45;;
btnAbstand = 6;;
btnBreite = Min(80; Max(44; (conVerwaltenDialog_1.Width - 5*btnAbstand - 40) / 6));;
BasisKachelbreiteHochUG = 52;;
BasisKachelhoeheHochUG = 89;;
BasisKachelbreiteQuerUG = 89;;
BasisKachelhoeheQuerUG = 52;;
BasisKreisgroesseUG = 39;;
BasisSchriftgroesseUG = 11;;
// Josias 2026-09-28: eigene Breite fuer Big Table UG, deutlich breiter als Standardtisch, Hoehe bleibt Basishoehe horizontal
BasisKachelbreiteBigTableUG = 220;;

// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
TischNrOG = With({src: Filter(Tische; Geschoss.Value = "OG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
TischNrUG = With({src: Filter(Tische; Geschoss.Value = "UG")}; ForAll(Sequence(CountRows(src)); {Titel: Index(src; Value).Titel; Nr: Value}));;
// Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
BasisSkalierungReferenz = Min(881 / BasisBreite; 678 / BasisHoehe);;
```

**`Gallery1.Items`**

```
Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)
```

**`ddTischePanel.Items`**

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

**`btnNeuBuchenHeute.OnSelect`**

```
If(
  !varIsLoading;
  Set(varNeuBuchenTisch; LookUp(Tische; Titel = ThisItem.Tisch.Value));;
  If(
    IsBlank(varNeuBuchenTisch.ID);
    Notify("Diesen Tisch gibt es nicht mehr."; NotificationType.Warning);
    varNeuBuchenTisch.Gesperrt;
    Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
    Set(varSelectedTisch; varNeuBuchenTisch);;
    Set(varDialogJetzt; Now());;
    Reset(tglFuerAndere);;
    Reset(txtGastName);;
    Set(varFbTrotzdem; false);;
    Set(varEndeOverride; Text(ThisItem.Endzeit; "hh:mm"));;
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
  )
)
```

Die Originale stammen aus dem Export 10.11. 08:13 (= Export 13.10. an diesen Stellen), `btnNeuBuchenHeute.OnSelect` aus P3. Deutsche Schreibweise.

## Anhang B: Maschinelle Prüfung

Paket allein:

```
Grundriss-Laden v1: 6 Blöcke (6 Properties, App.Formulas zweistufig) in 5 Schritten. Grundlage: Export 13.10. 09:59.
Je Block: Anker genau 1x, Klammern, Rückübersetzung (App.Formulas mit Kommentaren), keine Kommentare in anderen Formeln,
benannte Formeln eindeutig und je mit ';' (deutsch ';;') abgeschlossen, vorhandener Text unverändert, OnStart nur um die zwei Blöcke kürzer,
varJetztTakt bleibt letzte Anweisung, Ladezeile unverändert, Positionen 1:1, keine Schreibzugriffe auf die Positionen, Felder vollständig,
ein Record-Typ für varSelectedTisch/varDetailsTisch, Tische nur noch in TischeLokal + frische Gesperrt-Prüfung beim Speichern.
props_de.json = Export 13.10. (2076 Properties, nach Abzug der Anführungszeichen-Reste 0 Abweichungen)
ddStockwerk: Kontrast Schrift/Auswahl alt 1.73:1, neu 7.21:1 (WCAG AA verlangt 4,5:1)
App.Formulas#1: 22 benannte Formeln: BasisBreite, BasisHoehe, BasisSkalierung, BasisKachelbreiteQuer, BasisKachelhoeheQuer, BasisKachelbreiteHoch, BasisKachelhoeheHoch, BasisKreisgroesse, btnAbstand, btnBreite, BasisKachelbreiteHochUG, BasisKachelhoeheHochUG, BasisKachelbreiteQuerUG, BasisKachelhoeheQuerUG, BasisKreisgroesseUG, BasisSchriftgroesseUG, BasisKachelbreiteBigTableUG, TischNrOG, TischNrUG, BasisSkalierungReferenz, colTischPositionen, colTischPositionenUG
App.Formulas: 23 benannte Formeln: BasisBreite, BasisHoehe, BasisSkalierung, BasisKachelbreiteQuer, BasisKachelhoeheQuer, BasisKachelbreiteHoch, BasisKachelhoeheHoch, BasisKreisgroesse, btnAbstand, btnBreite, BasisKachelbreiteHochUG, BasisKachelhoeheHochUG, BasisKachelbreiteQuerUG, BasisKachelhoeheQuerUG, BasisKreisgroesseUG, BasisSchriftgroesseUG, BasisKachelbreiteBigTableUG, TischeLokal, TischNrOG, TischNrUG, BasisSkalierungReferenz, colTischPositionen, colTischPositionenUG
Positionen: OG 16, UG 19 (inkl. Big Table) = Tische-Liste 12.10. (REST, 35 Zeilen), Namen und Geschoss gleich
Nr OG (Listenreihenfolge 12.10.): 1=OG 1, 2=OG 2, 3=OG 3, 4=OG 4, 5=OG 5, 6=OG 8, 7=OG 9, 8=OG 12, 9=OG 10, 10=OG 13, 11=OG 6, 12=OG 7, 13=OG 11, 14=Quiet 3, 15=Quiet 2, 16=Quiet 1
Nr UG (Listenreihenfolge 12.10.): 1=UG 1, 2=UG 2, 3=UG 3, 4=UG 4, 5=UG 5, 6=UG 6, 7=UG 7, 8=UG 8, 9=UG 9, 10=UG 10, 11=UG 11, 12=UG 12, 13=UG 13, 14=UG 15, 15=UG 16, 16=UG 17, 17=UG 18, 18=Big Table, 19=UG 14
Gelesene Felder aus Kachel/Auswahl/Tischliste: Geschoss, Gesperrt, ID, Titel (alle in TischeLokal)
Tische direkt gelesen vorher: App.Formulas, Gallery1.Items, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, ddTischePanel.Items
Tische direkt gelesen nachher: App.Formulas, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect (App.Formulas nur noch in TischeLokal, Speichern prüft Gesperrt weiter frisch am Server)
Prüfung: 0 Fehler
```

Alle Pakete zusammen (`werkzeuge/abstimmung.py`):

```
Abstimmung der Pakete, Grundlage Export 10.11. 08:13 („echt“, App „Tischbuchung“, Desktop).
Reihenfolge: P0 Design → P1 Für andere buchen v2 → P2 Nachtrag 5 → P3 Nachtrag 6 v2 → P4 Grundriss-Laden v2 (= v1 + L5).

P0: 7 Properties, davon 7 mit Vorher (alle passen genau), 0 neu/bisher Standard, 0 neue Steuerelemente
P1: 179 Properties, davon 19 mit Vorher (alle passen genau), 160 neu/bisher Standard, 10 neue Steuerelemente
P2: 21 Properties, davon 21 mit Vorher (alle passen genau), 0 neu/bisher Standard, 0 neue Steuerelemente
P3: 32 Properties, davon 2 mit Vorher (alle passen genau), 30 neu/bisher Standard, 1 neue Steuerelemente
P4: 7 Properties, davon 7 mit Vorher (alle passen genau), 0 neu/bisher Standard, 0 neue Steuerelemente

Zusammen: 243 verschiedene Properties, 246 Blöcke, 11 neue Steuerelemente: tglFuerAndere (P1), txtGastName (P1), tglFuerAnderePanel (P1), txtGastNamePanel (P1), btnFbHintergrund (P1), conFbHinweis (P1), lblFbTitel (P1), lblFbHinweis (P1), btnFbAbbrechen (P1), btnFbTrotzdem (P1), btnNeuBuchenHeute (P3)
Properties, die mehr als ein Paket ändert (jeweils auf dem Stand des vorigen aufgebaut, Vorher geprüft):
  btnHitArea.OnSelect: P1 → P3
  btnNeuBuchenHeute.OnSelect: P3 → P4
  App.Formulas: P4 → P4

Endzustand:
  Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden: alle 243 geänderten Properties.
  Öffner Buchungsdialog (btnHitArea.OnSelect, btnNeuBuchenHeute.OnSelect): setzen Gast-Schalter, Gastname, „Trotzdem“, Ende-Vorgabe, Datum und Ende zurück.
  Öffner Panel (btnTischHinzufügen.OnSelect): setzen Gast-Schalter, Gastname und „Trotzdem“ zurück.
  Schreibstellen (8): alle mit Zweifach-Sperre und Ladezeile. Ladezeile 18× in einer Fassung (Aktualisieren-Knöpfe zusätzlich mit Erfolgsmeldung).
  varSelectedTisch: Setzer ['Blank()', 'ThisItem', 'varNeuBuchenTisch']; Gallery1 und „Neu buchen“ lesen beide aus TischeLokal.
  GastName in jeder Füllung von colNeuIch, colVerlIch (dort mit GastName gelesen).
  Gewählte Buchung (varSelectedBuchung, …Tab, varCheckinBuchung): jeder Setzer liefert einen Datensatz aus Tischbuchungen (mit GastName).
  Positionen: benannte Formeln, keine Sammlung mehr. Freigabe-Grenze überall 30 Min (Coalesce).

Check-in-Fenster (Bestand, nicht geändert):
  App.OnStart: 30, 60 Min
  Timer1.OnTimerEnd: 30 Min
  btnEinchecken.OnSelect: 60 Min

Prüfung: 0 Fehler
```
