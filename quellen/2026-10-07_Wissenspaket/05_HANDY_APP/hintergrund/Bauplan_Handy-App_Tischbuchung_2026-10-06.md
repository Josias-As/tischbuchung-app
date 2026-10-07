# Bauplan: Handy-App „Tischbuchung Mobil" — alle Schritte

**Stand:** 06.10.2026 · **Art:** Planung und Übersicht, **noch keine Formeln**
**Grundlage:** Quellcode der Desktop-App aus dem Export vom 30.09.2026 (`C:\tischbuchung_work\src`). Alle Steuerelementnamen und Formelinhalte der Desktop-App unten stammen aus diesem Quellcode und nicht aus der Doku.

---

## 0. Kurzfassung

1. **Korrektur zu meiner Analyse von heute Vormittag:** Im Quellcode steht `ScaleToFit = False`, `MaintainAspectRatio = False`, `LockOrientation = False`. Die Desktop-App ist also **schon responsiv eingestellt** und nicht auf 16:9 fixiert. Damit stimmt meine Begründung „ein Handy-Screen in derselben App geht technisch nicht" **nicht**. Er geht. Siehe Abschnitt 1. Ich empfehle trotzdem die eigene App, aber aus anderen Gründen, und die Entscheidung ist knapper als dargestellt.
2. Der Bauplan hat **13 Phasen** mit zusammen rund **45 Steuerelementen**. Das sind deutlich weniger als die über 180 in der Desktop-App.
3. Fast alles lässt sich aus vorhandenen Formeln ableiten. Neu gedacht werden müssen nur drei Teile: das Dropdown „nur freie Tische", der Buchen-Knopf mit frischer Kollisionsprüfung und das Einchecken mit Zeitfenster.
4. Bei der **Doppelbuchungsvermeidung** habe ich im Quellcode sieben Schwachstellen gefunden, die die Handy-App **nicht** übernehmen darf (Abschnitt 11). Die wichtigste: Die Desktop-App holt für die Kollisionsprüfung *alle* Buchungen eines Tisches ohne Zeitgrenze und filtert erst im Handy bzw. Browser. Das wird ab einer bestimmten Listengröße stillschweigend unvollständig.
5. **Vor Phase 1** sollten ein neuer Export und zehn Entscheidungen stehen (Abschnitt 2).

---

## 1. Neue Lage: Variante „eigene App" oder „neuer Screen in derselben App"

### Was der Quellcode sagt

Ausschnitt aus `Properties.json`, Export vom 30.09.:

| Einstellung | Wert |
|---|---|
| `DocumentAppType` | DesktopOrTablet |
| `DocumentLayoutWidth` × `Height` | 1366 × 768, Querformat |
| `DocumentLayoutScaleToFit` | **False** |
| `DocumentLayoutMaintainAspectRatio` | **False** |
| `DocumentLayoutLockOrientation` | **False** |

Screen1 ist mit Formeln wie `Parent.Width - (conDashboard.X + conDashboard.Width) - 10` aufgebaut. Der Grundriss rechnet über `BasisSkalierung` und `BasisSkalierungReferenz` selbst (Grundriss-Fix vom 30.09.).

**Folge:** Ein zusätzlicher Screen `scrMobil` in der Desktop-App, gestartet über `App.StartScreen = If(Host.OSType = "iOS" || Host.OSType = "Android"; scrMobil; Screen1)`, würde am Handy die volle Breite im Hochformat nutzen. Variante B aus der Vormittags-Analyse ist **möglich**.

⚠ Bitte im Studio kurz gegenprüfen (Einstellungen → Anzeige). Der Export ist vom 30.09., und laut `STOPP.md` von heute kommt die App-ID `d247d18b-…` im Paket nicht vor.

### Ehrlicher Vergleich

| | Eigene App | Neuer Screen in „Tischbuchung" |
|---|---|---|
| Risiko für den Go-Live am 14.10. | **keins**, die Desktop-App wird nicht angefasst | Jede Änderung am Handy-Screen ist eine Änderung an der produktiven App. Ein halbfertiger Screen wird mitveröffentlicht. |
| Bauen im Studio | Hochformat-Zeichenfläche, man sieht, was man baut | Zeichenfläche bleibt 1366 × 768 quer. Den Hochformat-Screen baut man blind über Formeln und prüft nur in der Vorschau. |
| Namen | sauber, keine Kollision | Viele Namen sind belegt, es entstehen wieder `_1`/`_2`-Namen. Das war schon einmal Fehlerquelle (`Label14`). |
| Variablen | eigene, klein | geteilt mit Screen1, z. B. `varSelectedBuchung`, die schon zwei Dialoge bedient (Bug B0) |
| Doppelte Logik | ja, Speichern/Prüfen zweimal | ebenfalls. Auch im selben Screen sind Formeln pro Steuerelement doppelt (siehe `btnSpeichern` / `btnSpeichernTischePanel`). |
| Link / Freigabe | zweiter Link, zweite Freigabe | ein Link, automatische Weiterleitung |
| Datenquellen, Named Formulas | neu anlegen | schon vorhanden |

**Meine Empfehlung bleibt die eigene App.** Der Grund ist nicht mehr „geht nicht", sondern: Go-Live in acht Tagen, die Desktop-App bleibt unberührt, und man baut auf einer Zeichenfläche, die wie ein Handy aussieht. Der Vorteil „doppelte Logik vermeiden" fällt für den neuen Screen kleiner aus als gedacht, weil Power Apps Formeln ohnehin pro Steuerelement speichert.

**Der Bauplan unten gilt für beide Varianten.** Wo sie sich unterscheiden, steht es dabei (🅂 = nur bei neuem Screen).

---

## 2. Phase 0 — Vorbereitung und Entscheidungen

### 0.1 Neuer Export
- Die App „Tischbuchung" (ID `d247d18b-…`) als Paket exportieren.
- Zweck 1: Sicherung. Zweck 2: Claude Code bekommt den Stand **nach** Sammel-`Patch`, neuem Stornieren und K1–K5. Der Plan hier basiert auf dem 30.09.-Stand.
- Damit ist auch die Übergabe-Aufgabe (`STOPP.md`) wieder lauffähig.

### 0.2 Anzeige-Einstellungen in der Desktop-App ansehen
- *Scale to fit*, Seitenverhältnis, Ausrichtung notieren. Bestätigt oder widerlegt Abschnitt 1.
- Außerdem das Datenzeilenlimit (Einstellungen → Allgemein). **Der Export vom 30.09. sagt 1000, das Briefing sagt 2000.**

### 0.3 Entscheidungen (vor dem Bauen)

| # | Frage | Mein Vorschlag |
|---|---|---|
| E1 | Eigene App oder neuer Screen? | Eigene App |
| E2 | Klassische oder moderne Steuerelemente? | **Klassisch**: dieselben Eigenschaften wie in der Desktop-App, Formeln übertragbar, bekanntes Verhalten. Modern sieht am Handy besser aus, hat aber andere Eigenschaftsnamen. |
| E3 | Buchen nur für heute oder auch für andere Tage? | Auch andere Tage, aber **keine Serienbuchung** |
| E4 | Schnellwahl „5 Std / 9 Std" übernehmen? | Ersetzen durch einen Knopf „bis 17:00". Die 5/9-Std-Knöpfe machen je drei ungefilterte Abfragen pro Bildschirmaufbau. |
| E5 | Einchecken: ab wann erlaubt? | 30 Min vor Start bis Ende (passt zur 30-Min-Logik im Grundriss). Die Desktop-App erlaubt heute Einchecken jederzeit. |
| E6 | Auschecken am Handy? | Ja, aber als „Buchung beenden" (Endzeit auf jetzt setzen). So wird der Tisch wirklich frei, statt nur den Haken umzuschalten. |
| E7 | Verlängern/Verkürzen am Handy? | Nur Verlängern um +1 Std/+2 Std und „Jetzt beenden". Kein Verkürzen in der Zukunft. |
| E8 | Darf eine Person zur selben Zeit zwei Tische haben? | **Nein**, in der Handy-App prüfen. Die Desktop-App prüft das heute nicht. |
| E9 | Welche Tische dürfen am Handy gebucht werden? | Alle außer „Big Table" (wie Josias' Vorgabe beim Alternativen-Konzept). Unklar ist der Umgang mit „Quiet Desk 1–3" (OG-Liste). |
| E10 | Nachlese nach dem Speichern? (Abschnitt 11, R1) | Ja, als einfache Variante. Fachlich klären, wer bei gleichzeitiger Buchung „gewinnt". |

---

## 3. Phase 1 — App anlegen und Grundeinstellungen

```
App „Tischbuchung Mobil"
├── Anlegen
│   ├── Leere Canvas-App, Format: Smartphone
│   ├── Umgebung: „Personal Productivity" (dieselbe wie Desktop)
│   └── Name, Symbol (Technoform-Blau #171496), Beschreibung
├── Einstellungen → Anzeige
│   ├── Scale to fit: AUS
│   ├── Lock orientation: AN, Hochformat
│   └── (Lock aspect ratio geht automatisch aus)
├── Einstellungen → Allgemein
│   ├── Datenzeilenlimit: gleicher Wert wie Desktop-App
│   └── Debug-Version veröffentlichen: AUS
├── Einstellungen → Updates
│   └── Moderne Steuerelemente nur, falls E2 = modern
├── Datenquellen
│   ├── Tischbuchungen  (SharePoint, gleiche Site)
│   ├── Tische          (SharePoint, gleiche Site)
│   └── Spalten per Autovervollständigung prüfen, NICHT aus diesem Dokument abtippen:
│       Titel, Geschoss (Tische) · Tisch, Startzeit, Endzeit, Person, CheckedIn/Checkedin, SerienID (Tischbuchungen)
├── App.Formulas (Named Formulas)
│   ├── Farben: Blau #171496, Grün #00A96B, Orange #FFA500, Rot #EB3951, Grau
│   ├── MeineMail (User().Email)
│   ├── HeuteStart / HeuteEnde (Tagesgrenzen für delegierbare Filter)
│   ├── TagesEnde-Regel (22:00, wie Desktop)
│   └── BuchbareTische (Tische ohne Big Table, siehe E9)
├── App.OnStart (klein halten, jede Variable typgerecht vorbelegen, kein Blank())
│   ├── varTab ("heute")
│   ├── varIsLoading (false)
│   ├── varSelectedBuchung (leerer Datensatz vom Typ Tischbuchungen statt Blank())
│   ├── varZeigeVerwalten (false)
│   ├── varZeigeStornoBestaetigen (false)
│   ├── varPlusDauer (0)
│   └── varEndeOverride ("")
├── App.StartScreen
│   └── vorerst leer; später für QR-Check-in (Phase 13)
└── scrMobil (Screen)
    ├── Fill
    └── LoadingSpinner: None    ← Lehre aus dem doppelten Spinner (Screen1.LoadingSpinner = Data + conLadeOverlay)
```

🅂 Bei neuem Screen fallen Anlegen, Datenquellen und Anzeige weg. Stattdessen: `App.StartScreen` setzen, eigene Variablen mit Präfix (z. B. `varM…`), damit Screen1 nichts davon mitbekommt.

---

## 4. Phase 2 — Grundgerüst (Container)

Reihenfolge in der Strukturansicht ist wichtig: Was unten in der Liste steht, liegt oben auf dem Bildschirm. Dialoge und Overlay liegen **direkt im Screen**, nicht in einem Auto-Layout-Container (Lehre vom 10.09.: dort werden X/Y ignoriert, und `conBuchungDialog` lag schon einmal versehentlich in `Gallery1`).

```
scrMobil
├── conRoot                    Vertikaler Auto-Layout-Container
│   ├── X, Y = 0
│   ├── Width = Parent.Width
│   ├── Height = Parent.Height
│   ├── LayoutDirection = Vertical
│   ├── Gap = 0
│   ├── conHeader              (Phase 3)
│   │   ├── FillPortions = 0, feste Height
│   │   └── LayoutDirection = Horizontal, AlignInContainer
│   ├── conInhalt              Manuell oder vertikal, nimmt den Rest ein
│   │   ├── FillPortions = 1 (flexible Höhe)
│   │   ├── conHeute    Visible: varTab = "heute"     (Phase 5)
│   │   ├── conBuchen   Visible: varTab = "buchen"    (Phase 6)
│   │   └── conMeine    Visible: varTab = "meine"     (Phase 7)
│   └── conTabLeiste           (Phase 4)
│       ├── FillPortions = 0, feste Height
│       └── LayoutDirection = Horizontal, drei gleich breite Kinder
├── conDlgHintergrund          Halbtransparentes Rechteck, ganze Fläche, fängt Tipps ab
│   └── Visible: varZeigeVerwalten || varZeigeStornoBestaetigen
├── conDlgVerwalten            (Phase 8)
├── conDlgStorno               (Phase 8)
└── conLadeOverlay             Ganz oben, Visible: varIsLoading   (Phase 9)
```

Pro Container zu setzen: `X`, `Y`, `Width`, `Height` als Formel (nie ziehen, das überschreibt Formeln mit Zahlen), `Fill`, `Visible`, Radien, `DropShadow`.

---

## 5. Phase 3 — Header

**Vorlage:** `conHeader` der Desktop-App (`Image6`, `btnTabDashboard`, `btnTabBuchungen`, `Circle2`, `lblInitialen`, `btnHitArea_1`). Die Tab-Knöpfe wandern am Handy nach unten.

```
conHeader
├── imgLogo
│   ├── Image (Technoform-Logo, aus Desktop-App exportieren/neu hochladen)
│   └── Height, Width
├── lblAppTitel
│   ├── Text ("Tischbuchung")
│   ├── Size, FontWeight, Color
│   └── FillPortions (nimmt Platz in der Mitte ein)
├── btnAktualisieren          ersetzt Image6 + btnHitArea_1 + Icon1_1 + Icon1 (vier Refresh-Knöpfe in der Desktop-App)
│   ├── Icon (Pfeil im Kreis)
│   ├── OnSelect: Overlay an → Refresh(Tischbuchungen) → Overlay aus → Meldung
│   ├── DisplayMode: gesperrt während varIsLoading
│   └── Width/Height ≥ Touch-Größe
├── Circle (Profilfarbe)
│   └── Fill (Desktop: varProfilFarbe per RandBetween → am Handy feste Farbe reicht)
└── lblInitialen
    ├── Text: wörtlich von Desktop übernehmen (Split(User().FullName …))
    └── Align, Size, Color
```

---

## 6. Phase 4 — Tab-Leiste unten

**Vorlage:** `btnTabDashboard.OnSelect` / `btnTabBuchungen.OnSelect`. Die Desktop-Variante schließt beim Tabwechsel sechs Dialog-Variablen. Am Handy sind es nur zwei.

```
conTabLeiste
├── btnTabHeute
│   ├── Text ("Heute") + Icon darüber oder davor
│   ├── OnSelect: varTab = "heute"; offene Dialoge zu (varZeigeVerwalten, varZeigeStornoBestaetigen)
│   ├── Fill / Color: aktiver Tab hervorgehoben (Abfrage auf varTab)
│   ├── PressedFill (in der Desktop-App teils leer, siehe OFFENE_FUNDE F3)
│   └── Height ≥ Touch-Größe, Width = Parent.Width / 3
├── btnTabBuchen       (gleiches Schema, varTab = "buchen", zusätzlich Buchen-Felder zurücksetzen)
└── btnTabMeine        (gleiches Schema, varTab = "meine")
```

---

## 7. Phase 5 — Tab „Heute" (abgeleitet aus `conDashboard`)

**Vorlage:** `conDashboard` mit `galTischbuchungenHeute`, `lblTischLeer`, `Label16`, `dpAnsichtsDatum`, `btnTischHinzufügen`.
**Wegfall:** `galRaumbuchungenHeute`, `lblRaumLeer`, `lblMyMeetings`, `btnRaumHinzufügen` (alles toter Raumcode, `Visible: false`), `dpAnsichtsDatum` (am Handy nur heute).

```
conHeute
├── lblHeuteTitel
│   └── Text ("Heute, " + Wochentag + Datum)
├── galHeuteMeine                                 ← Vorlage galTischbuchungenHeute
│   ├── Items
│   │   ├── Vorlage: Filter(Tischbuchungen; Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < … && (… || Endzeit >= Now()))
│   │   ├── Am Handy fest auf heute (HeuteStart/HeuteEnde statt varAnsichtsDatum)
│   │   ├── Sortierung nach Startzeit
│   │   └── Delegation prüfen (Person.Email = delegierbar; Now() als Konstante)
│   ├── TemplateSize (groß, Karte)
│   ├── TemplatePadding
│   ├── Rechteck „Karte"
│   │   └── Fill, Radius
│   ├── lblTisch
│   │   └── Text: wie lblTischHeute ("Tisch " & ThisItem.Tisch.Value)
│   ├── lblZeit
│   │   └── Text: wie lblZeitHeute
│   ├── lblStatus                                  ← Vorlage lblStatusHeute, erweitert
│   │   ├── Text: drei Zustände statt zwei
│   │   │   ├── „Eingecheckt"
│   │   │   ├── „Bitte einchecken" (im Zeitfenster E5)
│   │   │   └── „Ab hh:mm eincheckbar" (vor dem Zeitfenster)
│   │   └── Color: Grün / Orange / Grau
│   ├── btnEinchecken                              ← Vorlage btnEincheckenHeute + conCheckinDialog.btnEinchecken
│   │   ├── Text („Einchecken")
│   │   ├── Visible: nicht eingecheckt UND im Zeitfenster
│   │   ├── DisplayMode: gesperrt während varIsLoading (Doppeltipp)
│   │   ├── Fill / PressedFill / Color (Orange wie Dashboard-Vorbild)
│   │   ├── Height ≥ Touch-Größe, volle Kartenbreite
│   │   └── OnSelect (direkt, OHNE Check-in-Dialog — ein Tipp statt zwei)
│   │       ├── Overlay an
│   │       ├── Buchung frisch per LookUp(ID) holen
│   │       ├── Existiert nicht mehr → Meldung „wurde storniert", Ende
│   │       ├── Zeitfenster erneut prüfen (Now() zum Klickzeitpunkt)
│   │       ├── IfError(Patch CheckedIn = true)
│   │       │   ⚠ Desktop schaltet um (!CheckedIn). Am Handy fest auf true, damit ein zweiter Tipp nicht auscheckt.
│   │       ├── Meldung Erfolg / Fehler
│   │       └── Overlay aus — auf JEDEM Pfad
│   └── btnVerwalten                               ← Vorlage btnVerwalten
│       ├── Icon (Stift oder „…")
│       ├── OnSelect: varSelectedBuchung = ThisItem; varPlusDauer = 0; varZeigeVerwalten = true
│       └── Größe ≥ Touch-Größe
├── lblKeineBuchungHeute                           ← Vorlage lblTischLeer
│   ├── Text („Heute keine Buchung")
│   └── Visible: galHeuteMeine.AllItemsCount = 0
├── btnJetztBuchen                                 ← Vorlage btnTischHinzufügen
│   ├── Text („Tisch buchen")
│   ├── Visible: wenn keine laufende Buchung
│   └── OnSelect: Buchen-Felder zurücksetzen; varTab = "buchen"
└── (optional) galFreieTischeJetzt                 Liste „Gerade frei"
    ├── Items: BuchbareTische ohne aktuelle Belegung, Belegung EINMAL laden (siehe 11, R2)
    ├── lblTischName, lblGeschoss
    └── btnSchnellBuchen → vorbelegt in Tab „Buchen" springen
```

⚠ Status-Logik für „belegt/fällig/eingecheckt" muss **wortgleich** zur Grundriss-Bedingung in `Rectangle1.Fill` sein (`Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; Minutes)`), sonst zeigt das Handy etwas anderes als der Desktop.

---

## 8. Phase 6 — Tab „Buchen" (abgeleitet aus `conTischBuchungenPanel`)

**Vorlage:** `ddTischePanel`, `dpDatumTischePanel`, `ddStartTischePanel`, `ddEndTischePanel`, `btnSpeichernTischePanel`, `btnAbbrechenTischePanel`, `btn5Std`, `btn9Std`.
**Wegfall:** `chkWiederholenPanel`, `tglTagMo_1`…`tglTagFr_1`, `dpWiederholenBis_1`, `Label14` (Serienbuchung, E3).
**Wichtigste Änderung:** Die Reihenfolge dreht sich. Desktop: Tisch → Datum → Zeit. Handy: **Datum → Zeit → nur freie Tische**. Ohne Grundriss muss das Dropdown zeigen, was frei ist.

```
conBuchen
├── lblBuchenTitel
│   └── Text („Tisch buchen")
├── dpDatum                                        ← Vorlage dpDatumTischePanel
│   ├── DefaultDate: Today() (Desktop: varAnsichtsDatum)
│   ├── Keine vergangenen Tage (Begrenzung oder Warnung)
│   ├── Format, Size, Height (Touch)
│   └── OnChange: Start, Ende, Tisch zurücksetzen (Desktop setzt nur Start und Ende zurück)
├── ddStart                                        ← Vorlage ddStartTischePanel
│   ├── Items: Formel wörtlich übernehmen, Datumswähler-Name ersetzen
│   ├── Default: wörtlich übernehmen, Override-Variable ersetzen
│   ├── OnChange: Tisch zurücksetzen
│   └── Size, Height
├── ddEnde                                         ← Vorlage ddEndTischePanel
│   ├── Items / Default: wörtlich übernehmen, Namen ersetzen
│   ├── OnChange: Tisch zurücksetzen
│   └── Size, Height
├── btnBis17                                       ersetzt btn5Std / btn9Std (E4)
│   ├── Text („bis 17:00")
│   ├── OnSelect: varEndeOverride setzen, ddEnde zurücksetzen
│   └── DisplayMode: aus, wenn Start ≥ 17:00
├── ddTisch                                        NEU — ersetzt ddTischePanel (Items: Tische)
│   ├── Items: nur freie Tische im gewählten Zeitraum
│   │   ├── Schritt 1: Belegung im Zeitraum EINMAL holen (delegierbar: Startzeit < neuEnde && Endzeit > neuStart)
│   │   ├── Schritt 2: lokal BuchbareTische minus belegte Titel
│   │   ├── Schritt 3: sortieren nach Geschoss, dann Name
│   │   └── Big Table raus (E9)
│   ├── Anzeige: Titel (+ Geschoss)
│   ├── Default: leer, Platzhaltertext „Tisch wählen"
│   └── Size, Height
├── lblKeinTischFrei
│   ├── Text („Im gewählten Zeitraum ist kein Tisch frei")
│   └── Visible: Items leer
├── lblZusammenfassung
│   └── Text („OG Desk 5 · Di 07.10. · 08:00–17:00") — damit vor dem Tippen klar ist, was gebucht wird
├── btnBuchen                                      ← Vorlage btnSpeichernTischePanel, stark reduziert
│   ├── Text („Buchen")
│   ├── DisplayMode: gesperrt, wenn varIsLoading ODER kein Tisch ODER Ende ≤ Start
│   ├── Fill / DisabledFill / PressedFill
│   └── OnSelect — Ablauf (Details zur Prüfung in Abschnitt 11)
│       ├── 1  Overlay an (varIsLoading = true)
│       ├── 2  Start- und Endzeit aus Datum + Dropdowns berechnen (wie Desktop neuStart/neuEnde)
│       ├── 3  Plausibilität: Ende > Start, Start nicht in der Vergangenheit, Ende ≤ 22:00
│       ├── 4  Frisch prüfen: fremde Buchung an DIESEM Tisch im Zeitraum? (mit Zeitgrenze im Filter)
│       ├── 5  Frisch prüfen: eigene Buchung an IRGENDEINEM Tisch im Zeitraum? (E8)
│       ├── 6  IfError(Patch(Tischbuchungen; Defaults(…); { Tisch {Id; Value}, Startzeit, Endzeit, Person (volles Schema) }))
│       ├── 7  (E10) Nachlese: gibt es jetzt eine Überschneidung? → Regel anwenden
│       ├── 8  Meldung je Ausgang: gebucht / belegt (mit Tischname) / eigene Überschneidung / Fehler
│       ├── 9  Nur bei Erfolg: Felder zurücksetzen, varTab = "heute"
│       ├── 10 Refresh(Tischbuchungen)
│       └── 11 Overlay aus — auf JEDEM Pfad (Lehre 1B/2C)
└── btnZuruecksetzen                               ← Vorlage btnAbbrechenTischePanel
    └── OnSelect: alle Felder zurücksetzen (Reset(...) für jedes Feld, nicht nur Variablen)
```

---

## 9. Phase 7 — Tab „Meine" (abgewandelte Form von `conBuchungen`)

**Vorlage:** `galAlleTischbuchungen`, `lblÜberschriftBuchungen`, `lblTischLeer_1`, `Icon1`.
**Wegfall:** `tglAuswahlModus`, `chkAlleAuswählen`, `chkAuswahl`, `conVerwaltenKlein`, `colAusgewaehlteBuchungen`, `varGalleryNeuAufbauen` (Mehrfachauswahl gibt es am Handy nicht). `conVerwaltenDialog_1` wird durch `conDlgVerwalten` ersetzt (Phase 8).

```
conMeine
├── lblMeineTitel                                  ← Vorlage lblÜberschriftBuchungen
│   └── Text („Meine Buchungen")
├── galMeine                                       ← Vorlage galAlleTischbuchungen
│   ├── Items
│   │   ├── Vorlage: SortByColumns(Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now()); "Startzeit"; Ascending)
│   │   ├── With({erzwingeNeuaufbau: varGalleryNeuAufbauen}) weglassen
│   │   └── Delegationsdreieck der Vorlage klären (offene Frage 7 im Briefing)
│   ├── TemplateSize
│   ├── lblTisch                                   ← lblTischName
│   ├── lblDatumZeit                               ← lblRaumZeit, plus Wochentag („Mi 08.10. · 08:00–17:00")
│   ├── lblStatus (eingecheckt / offen)
│   ├── Trennlinie
│   └── btnVerwalten                               ← btnVerwalten_2, aber nur der Nicht-Auswahlmodus-Zweig
│       └── OnSelect: varSelectedBuchung = ThisItem; varPlusDauer = 0; varZeigeVerwalten = true
│           (EINE Variable für EINEN Dialog → Bug B0 kann gar nicht entstehen)
└── lblKeineEintraege                              ← Vorlage lblTischLeer_1
    └── Visible: galMeine.AllItemsCount = 0
        ⚠ BEFUND in der Desktop-App: lblTischLeer_1.Visible prüft galTischbuchungenHeute (die Galerie aus dem Dashboard!)
          statt galAlleTischbuchungen. Im Buchungen-Tab steht „-Keine Einträge-", sobald man HEUTE keine Buchung hat,
          auch wenn künftige Buchungen existieren. Möglicher Zusammenhang mit Bug 3 vom 30.09. („Buchungen-Tab zeigt
          manchmal keine Einträge"). Nicht übernehmen.
```

---

## 10. Phase 8 — Dialoge

### 10.1 `conDlgVerwalten` (ersetzt `conVerwaltenDialog` UND `conVerwaltenDialog_1`)

**Vorlage:** `lblTitel3_1`, `lblZeit3_1`, `lblVerwaltenTag`, `btnStornieren_1`, `btnVerlängern_1`, `btnPlus1Std_1`, `btnPlus2Std_1`, `btnSchließen4_1`.
Eine Variable (`varSelectedBuchung`), ein Dialog. Die Desktop-App hat dafür zwei Dialoge, zwei Variablen und eine Verwechslung.

```
conDlgVerwalten (direkt im Screen, unten angedockt wie ein „Bottom Sheet")
├── Visible: varZeigeVerwalten
├── X / Y / Width / Height: volle Breite, untere Bildschirmhälfte
├── lblDlgTisch        Text: Tisch aus varSelectedBuchung
├── lblDlgTag          Text: Wochentag + Datum (Vorlage lblVerwaltenTag)
├── lblDlgZeit         Text: Zeit, bei gewählter Verlängerung „08:00–17:00 → 18:00"
├── btnPlus1Std                                    ← Vorlage btnPlus1Std_1
│   ├── OnSelect: varPlusDauer umschalten (60 ↔ 0)
│   ├── Fill: gewählt hervorheben
│   └── DisplayMode
│       ├── Vorlage: CountRows(Filter(Tischbuchungen; Tisch.Value = … && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0
│       ├── ⚠ Vorlage liest varSelectedBuchung im Tab-Dialog (Bug B0) → am Handy automatisch richtig, weil nur eine Variable
│       ├── zusätzlich: über 22:00 → gesperrt
│       └── zusätzlich: varIsLoading → gesperrt
├── btnPlus2Std        (gleiches Schema, 120)
├── btnJetztBeenden                                NEU (E6) — ersetzt Auschecken und Verkürzen
│   ├── Visible: Buchung läuft gerade
│   └── OnSelect: frisch holen → IfError(Patch Endzeit = jetzt (gerundet)) → Meldung → Dialog zu
├── btnSpeichern                                   ← Vorlage btnVerlängern_1
│   ├── DisplayMode: aus, wenn varPlusDauer = 0 oder varIsLoading
│   └── OnSelect
│       ├── Overlay an
│       ├── frisch holen (LookUp ID); existiert nicht mehr → Meldung, Dialog zu
│       ├── neue Endzeit berechnen; über 22:00 → Meldung
│       ├── KOLLISION JETZT NOCH EINMAL PRÜFEN (nur das neue Stück: Startzeit < neueEndzeit && Endzeit > alteEndzeit)
│       │   ⚠ Die Desktop-App prüft beim Speichern NICHT, nur beim Färben der Knöpfe (Stand beim Öffnen)
│       ├── IfError(Patch Endzeit)
│       ├── Meldung
│       ├── nur bei Erfolg: Dialog zu, varPlusDauer = 0
│       └── Refresh; Overlay aus auf jedem Pfad
├── btnStornieren                                  ← Vorlage btnStornieren_1
│   └── OnSelect: varZeigeStornoBestaetigen = true (NICHT sofort löschen, Fehltipp am Handy)
└── btnSchließen
    └── OnSelect: varZeigeVerwalten = false; varPlusDauer = 0
```

### 10.2 `conDlgStorno` (neu, Bestätigung)

```
conDlgStorno
├── Visible: varZeigeStornoBestaetigen
├── lblFrage           „Buchung OG Desk 5, Mi 08.10., 08:00–17:00 wirklich stornieren?"
├── btnJaStornieren
│   └── OnSelect
│       ├── Overlay an
│       ├── frisch holen (LookUp ID); existiert nicht mehr → „war bereits storniert" (Ü3)
│       ├── IfError(Remove(Tischbuchungen; frischerDatensatz))
│       │   ⚠ Desktop entfernt den gespeicherten Variablen-Datensatz direkt → Ursache für „Item Not Found" (Bug 4 vom 30.09.)
│       ├── Meldung
│       ├── Dialoge zu, varSelectedBuchung leeren
│       └── Refresh; Overlay aus auf jedem Pfad
└── btnNein
    └── OnSelect: varZeigeStornoBestaetigen = false
```

---

## 11. Phase 9 — Doppelbuchungsvermeidung (gilt quer durch Phasen 5–8)

### Was ich im Quellcode der Desktop-App gefunden habe

| # | Schwachstelle | Fundort (Export 30.09.) | Was die Handy-App anders macht |
|---|---|---|---|
| **R1** | **Prüfen-dann-Schreiben ist nicht atomar.** Zwischen der Prüfung und dem `Patch` vergehen Sekundenbruchteile bis Sekunden. Buchen zwei Personen gleichzeitig denselben Tisch, bestehen beide die Prüfung. SharePoint verhindert das nicht. | alle Speichern-Knöpfe | Lässt sich in SharePoint ohne Transaktionen **nicht vollständig** lösen. Abhilfe: Nachlese direkt nach dem Speichern (E10). Gibt es danach eine Überschneidung, gilt eine feste Regel, z. B. „ältere ID gewinnt, die neuere wird zurückgenommen und der Nutzer informiert". ⚠ Diese Regel wurde im Briefing für Verlängerungen angegriffen (2B). Für Einzelbuchungen am Handy ist sie vertretbar, muss aber fachlich entschieden werden. |
| **R2** | **Kollisionsabfrage ohne Zeitgrenze.** `bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel)` holt alle Buchungen des Tisches. Die Zeitprüfung läuft danach lokal. Über dem Datenzeilenlimit fehlen Zeilen, und die Prüfung meldet „frei", obwohl es nicht stimmt. | `btnSpeichernTischePanel`, `btnSpeichern` (K4.1 soll das beheben, Stand unbekannt) | Zeitgrenze **im** Filter: Tisch **und** `Startzeit < neuEnde` **und** `Endzeit > neuStart`. Alles davon ist bei SharePoint delegierbar. |
| **R3** | **Prüfung nur beim Anzeigen, nicht beim Speichern.** Die +1/+2/+3-Knöpfe werden beim Öffnen des Dialogs grau oder aktiv. Beim Speichern wird nicht mehr geprüft. Wer den Dialog lange offen lässt, verlängert in eine inzwischen gebuchte Zeit. | `btnVerlängern`, `btnVerlängern_1` | Prüfung beim Speichern wiederholen (Phase 8). |
| **R4** | **Falsche Variable im Prüfknopf (B0).** Im Buchungen-Tab prüfen alle Plus-/Minus-Knöpfe `varSelectedBuchung` (die zuletzt im Grundriss angeklickte Buchung) statt `varSelectedBuchungTab`. Grün heißt dann nicht frei. | `btnPlus1Std_1` … `btnMinus3std` | Nur eine Variable, nur ein Dialog. |
| **R5** | **Doppeltipp.** Kein Speichern-Knopf ist während des Speicherns gesperrt. Zwei schnelle Tipps = zwei Buchungen, weil die zweite Prüfung die erste Buchung noch nicht sieht. Am Handy ist das wahrscheinlicher als mit der Maus. | alle Speichern-Knöpfe (K5 soll das beheben) | `DisplayMode` an `varIsLoading` koppeln, und das Overlay deckt den Bildschirm ab. |
| **R6** | **Eine Person, zwei Tische zur gleichen Zeit** wird nirgends geprüft. | – | Prüfung E8 im Buchen-Knopf. |
| **R7** | **Unsichtbare Buchungen.** Wird `Person` oder `Tisch` falsch geschrieben, landet die Buchung zwar in der Liste, erscheint aber in keiner Ansicht (alle filtern auf `Person.Email`). Sie blockiert trotzdem den Tisch. | Ü6 im Briefing | Exakt das Personen-Schema der Desktop-App (`Claims`, `Department`, `DisplayName`, `Email`, `JobTitle`, `Picture`) und `Tisch: {Id; Value}`. Nach dem ersten Testlauf in SharePoint direkt nachsehen. |

### Geteilte Regeln (müssen in beiden Apps wortgleich sein)

In `KONTEXT.md` für Claude Code als eigenen Abschnitt anlegen:

1. **Überschneidung:** `Startzeit < neuesEnde && Endzeit > neuerStart` (Grenzen berühren sich = keine Überschneidung)
2. **Status jetzt:** belegt, wenn `Endzeit >= Now() && Startzeit <= Now() + 30 Min`
3. **Tagesende:** 22:00
4. **Zeitraster:** 30 Minuten
5. **Personenfeld-Schema** und **Lookup-Schema** beim Schreiben
6. **Nicht buchbar:** Big Table (E9)

Jede Änderung an einer dieser Regeln gilt für beide Apps. Der Desktop-Fix K4 (Zeitgrenze, `IfError`) und der Handy-Buchen-Knopf sollten am Ende **dieselbe** Prüfformel haben.

---

## 12. Phase 10 — Lade-Overlay und Fehlerbehandlung

```
conLadeOverlay                ← Vorlage conLadeOverlay (+ imgSpinner)
├── Visible: varIsLoading
├── Fill: halbtransparent schwarz (wie Desktop RGBA(0;0;0;0,4))
├── Width/Height: ganze Fläche → fängt alle Tipps ab
└── imgSpinner (GIF aus der Desktop-App übernehmen)

Regeln für jede Verhaltensformel
├── Overlay an am Anfang, aus am Ende auf JEDEM Pfad
├── Jeder Patch / Remove in IfError
├── Verständliche deutsche Meldungen, nie rohe Fehlertexte
└── Aufräumen (Felder leeren, Dialog zu) nur bei Erfolg (Ü2)
```

---

## 13. Phase 11 — Testen

### 13.1 Technisch
- Browser-Geräteemulation (F12 → Strg+Umschalt+M), iPhone- und Android-Profil
- Echtes iPhone und Android, jeweils Browser **und** Power Apps Mobile
- Debug-Label (während der Entwicklung): `Host.OSType`, `App.Width × App.Height`
- Nach der ersten Buchung in SharePoint nachsehen: Person, Tisch, Start, Ende korrekt? (R7)

### 13.2 Fachliche Testfälle

| # | Fall | Erwartung |
|---|---|---|
| T1 | Freien Tisch für heute buchen | erscheint in „Heute" und in „Meine", am Desktop im Grundriss orange |
| T2 | Tisch, der am Desktop 10–12 belegt ist, am Handy 11–13 suchen | erscheint **nicht** im Dropdown |
| T3 | Handy-Dropdown öffnen, dann am Desktop denselben Tisch buchen, dann am Handy „Buchen" | Meldung „inzwischen belegt", keine zweite Buchung (R1/R2) |
| T4 | Zwei Handys, gleicher Tisch, möglichst gleichzeitig „Buchen" | genau eine Buchung bleibt (Nachlese, E10) |
| T5 | „Buchen" doppelt schnell antippen | genau eine Buchung (R5) |
| T6 | Eigene Buchung OG 5 08–12, dann UG 3 10–14 buchen | abgelehnt (E8) |
| T7 | 40 Min vor Start einchecken | nicht möglich, Text „ab hh:mm" |
| T8 | 20 Min vor Start einchecken | möglich, am Desktop rot |
| T9 | Verlängern, während jemand anderes direkt danach gebucht hat | +1 Std gesperrt; falls Dialog vorher offen war: Speichern lehnt ab (R3) |
| T10 | Buchung am Desktop stornieren, am Handy danach verwalten | „existiert nicht mehr", kein Netzwerkfehler |
| T11 | Verlängern über 22:00 | gesperrt bzw. Meldung |
| T12 | Big Table | nie im Dropdown |
| T13 | Kein Netz (Flugmodus) beim Buchen | Fehlermeldung, Overlay geht wieder weg |
| T14 | Keine Buchung heute, aber künftige | „Heute" leer, „Meine" zeigt die künftigen (Gegenprobe zum `lblTischLeer_1`-Befund) |

---

## 14. Phase 12 — Veröffentlichen und Verteilen

```
├── Speichern mit Versionsnotiz
├── App-Prüfung (Studio): Fehler 0, Delegationswarnungen ansehen
├── Veröffentlichen
├── Freigeben: gleiche Personen/Gruppe wie Desktop-App (fehlen Rechte → Michael)
├── Link erzeugen: apps.powerapps.com/play/e/<Umgebungs-ID>/a/<App-ID>  (mit Umgebungs-ID, Pflicht seit 05/2026)
├── Testgruppe: Julia + 2–3 Personen mit iPhone und Android
├── Kurzanleitung: Link öffnen, zum Startbildschirm hinzufügen bzw. Power Apps Mobile → „Pin to Home"
└── Projektnotiz: App-ID, Link, Stand der geteilten Regeln
```

🅂 Bei neuem Screen: kein eigener Link; stattdessen `App.StartScreen` testen (Desktop öffnet Screen1, Handy öffnet scrMobil).

---

## 15. Phase 13 — Später (nicht vor dem Go-Live)

```
├── QR-Check-in am Tisch
│   ├── QR-Code pro Tisch mit Link …?tisch=OG%20Desk%205
│   ├── Param("tisch") auslesen (StartScreen / OnStart)
│   └── passende Buchung → direkt einchecken; frei → „Jetzt buchen?"
├── Weiterleitung aus der Desktop-App auf die Handy-App (Host.OSType, Launch)
└── Nachträglich: Desktop-Bugs aus Abschnitt 11 und 16 dort beheben
```

---

## 16. Nebenbei gefundene Desktop-Befunde (Export 30.09., Stand heute unbekannt)

| # | Befund | Status |
|---|---|---|
| N1 | `lblTischLeer_1.Visible` prüft `galTischbuchungenHeute` statt `galAlleTischbuchungen` | **neu**, BELEGT |
| N2 | `btnStornieren` (Grundriss-Verwalten) entfernt direkt `varSelectedBuchung`, ohne frisches Holen, ohne `IfError`, ohne Overlay | BELEGT, passt zu Bug 4 „Item Not Found" |
| N3 | `btnEinchecken` schaltet `CheckedIn` um, ohne Zeitfenster; ein zweiter Klick checkt aus | BELEGT |
| N4 | `ddTischePanel.Items = Tische`: alle Tische, auch belegte, und Big Table, sofern er in der Liste `Tische` steht (in `colTischPositionenUG` steht er) | BELEGT (Formel), Listeninhalt nicht geprüft |
| N5 | Datenzeilenlimit im Export 1000, im Briefing 2000 | klären |
| N6 | `btnAbbrechenTischePanel` setzt `varZeigeTischBuchungForm` zweimal auf false | kosmetisch |
| N7 | Vier verschiedene Refresh-Knöpfe mit identischer Formel (`Image6`, `btnHitArea_1`, `Icon1_1`, `Icon1`) | kosmetisch |

---

## 17. Übersicht: Was übernommen, angepasst oder weggelassen wird

| Desktop-Steuerelement | Handy | Art |
|---|---|---|
| `conHeader` (Logo, Initialen, Refresh) | `conHeader` | angepasst |
| `btnTabDashboard`, `btnTabBuchungen` | `conTabLeiste` (3 Tabs, unten) | angepasst |
| `conDashboard` / `galTischbuchungenHeute` | `conHeute` / `galHeuteMeine` | angepasst, fest auf heute |
| `btnEincheckenHeute` + `conCheckinDialog` | `btnEinchecken` in der Karte | zusammengelegt, ohne Dialog |
| `btnVerwalten` (Dashboard) | `btnVerwalten` | übernommen |
| `conTischBuchungenPanel` | `conBuchen` | stark angepasst (Reihenfolge, frei-Filter) |
| `ddStartTischePanel`, `ddEndTischePanel` | `ddStart`, `ddEnde` | Formeln übernommen |
| `ddTischePanel` | `ddTisch` | neu (nur freie) |
| `btnSpeichernTischePanel` | `btnBuchen` | neu gebaut, ohne Serie |
| `btn5Std`, `btn9Std` | `btnBis17` | ersetzt (E4) |
| Serien-Steuerelemente (`chk…`, `tgl…_1`, `dpWiederholenBis_1`, `Label14`) | – | weggelassen |
| `conBuchungen` / `galAlleTischbuchungen` | `conMeine` / `galMeine` | angepasst |
| Mehrfachauswahl (`tglAuswahlModus`, `chkAuswahl`, `chkAlleAuswählen`, `conVerwaltenKlein`) | – | weggelassen |
| `conVerwaltenDialog` + `conVerwaltenDialog_1` | `conDlgVerwalten` | zusammengelegt |
| – | `conDlgStorno` | neu |
| `conLadeOverlay` | `conLadeOverlay` | übernommen |
| `conGrundriss`, `Gallery1`, `ddStockwerk`, Koordinaten | – | weggelassen |
| `conBuchungDialog`, `conDetailsPopup` | – | weggelassen |
| Raumcode (`conRaumBuchungenPanel`, `conRaumBestätigen`, `galRaumbuchungenHeute`, …) | – | weggelassen (tot) |

---

## 18. Arbeitsteilung und Reihenfolge

| Schritt | Wer |
|---|---|
| Phase 0: Export, Einstellungen ansehen, E1–E10 entscheiden | Josias |
| Phase 1–2: App anlegen, Datenquellen, Gerüst | Josias (Klickarbeit), Formeln für Formulas/OnStart von Claude Code |
| Phase 3–4: Header, Tabs | Claude Code Formeln → Josias einfügen |
| Phase 7: Tab „Meine" (nur lesen) — **zuerst**, schnellster sichtbarer Erfolg und Test der Datenanbindung | Claude Code → Josias |
| Phase 5: Tab „Heute" mit Einchecken | Claude Code → Josias |
| Phase 8: Dialoge | Claude Code → Josias |
| Phase 6 + 9: Buchen und Doppelbuchungsschutz — **zuletzt**, weil am kritischsten | Claude Code → Josias, danach unabhängige Prüfung wie beim Speichern-Lauf |
| Phase 10–12: Overlay, Test, Veröffentlichen | Josias |

**Für Claude Code:** Dieses Dokument plus der neue Export (Phase 0.1) sind die Grundlage. Formeln in deutscher Locale (`;` / `;;`), ohne Kommentare, immer als vollständige Formel pro Eigenschaft.
