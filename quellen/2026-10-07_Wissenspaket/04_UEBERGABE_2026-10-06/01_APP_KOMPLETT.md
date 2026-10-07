# 01 — Die komplette App: jedes Steuerelement, jede Property, wortgetreu

**Kurzfassung:** Diese Datei wurde per Skript (`skripte/extrahiere.js`, `skripte/gen01.js`) aus `src/Src/App.pa.yaml` und `src/Src/Screen1.pa.yaml` erzeugt, nichts ist abgetippt. Sie enthält die App, den einen Screen und 186 Steuerelemente mit zusammen 1985 gesetzten Properties. Formeln stehen so, wie sie im Quellcode stehen: englische Schreibweise mit `,` als Argumenttrenner und `.` als Dezimaltrenner, mit führendem `=`. Studio zeigt dieselben Formeln in deutscher Schreibweise (`;`). Die Reihenfolge ist die des Quellcodes (Baum, Properties alphabetisch). Quelle: Export `TischbuchungApp06.10.2026_20261006112813.zip`, appVersion 2026-10-05T11:58:19Z.

Lesehinweis: `[C###]` ist die laufende Nummer im Baum. „Z." ist die Zeile des Steuerelements in `Screen1.pa.yaml`. Eine Property, die hier nicht steht, ist im Quellcode nicht gesetzt (Standardwert des Steuerelementtyps).

## Baumübersicht

```text
App
Screen1
  conGrundriss  [GroupContainer]
    imgGrundrissOG  [Image]
    imgGrundrissUG  [Image]
    Gallery1  [Gallery]
      Rectangle1  [Rectangle]
      Circle1  [Circle]
      Label1  [Label]
      btnHitArea  [Classic/Button]
    Image8  [Image]
    Label18  [Label]
    ddStockwerk  [Classic/DropDown]
  conDashboard  [GroupContainer]
    galTischbuchungenHeute  [Gallery]
      Rectangle4  [Rectangle]
      Image1_1  [Image]
      Image3  [Image]
      lblTischHeute  [Label]
      lblZeitHeute  [Label]
      lblStatusHeute  [Label]
      Rectangle3  [Rectangle]
      btnEincheckenHeute  [Classic/Button]
      btnVerwalten  [Classic/Button]
    galRaumbuchungenHeute  [Gallery]
      Rectangle4_1  [Rectangle]
      Image1_2  [Image]
      Image3_1  [Image]
      Rectangle3_1  [Rectangle]
      lblTischHeute_1  [Label]
      lblZeitHeute_1  [Label]
      btnInfoRaum  [Classic/Button]
      btnVerwalten_1  [Classic/Button]
    Image4  [Image]
    lblTischLeer  [Label]
    lblRaumLeer  [Label]
    lblMyPersonalDesk  [Label]
    lblMyMeetings  [Label]
    lblDatumLabel  [Label]
    Label16  [Label]
    btnRaumHinzufügen  [Classic/Button]
    btnTischHinzufügen  [Classic/Button]
    dpAnsichtsDatum  [Classic/DatePicker]
    Icon1_1  [Classic/Icon]
  conTischBuchungenPanel  [GroupContainer]
    lblTischeBuchenPanel  [Label]
    ddTischePanel  [Classic/DropDown]
    ddStartTischePanel  [Classic/DropDown]
    dpDatumTischePanel  [Classic/DatePicker]
    ddEndTischePanel  [Classic/DropDown]
    btnSpeichernTischePanel  [Classic/Button]
    btnAbbrechenTischePanel  [Classic/Button]
    tglTagMo_1  [Classic/Toggle]
    tglTagDi_1  [Classic/Toggle]
    tglTagMi_1  [Classic/Toggle]
    tglTagDo_1  [Classic/Toggle]
    tglTagFr_1  [Classic/Toggle]
    chkWiederholenPanel  [Classic/CheckBox]
    dpWiederholenBis_1  [Classic/DatePicker]
    Label14  [Label]
    btn5Std  [Classic/Button]
    btn9Std  [Classic/Button]
  conRaumBuchungenPanel  [GroupContainer]
    dpDatumRaum  [Classic/DatePicker]
    ddDauerRaumPanel  [Classic/DropDown]
    lblRaumBuchenPanel  [Label]
    ddBeginnRaumPanel  [Classic/DropDown]
    btnAbbrechenRaumPanel  [Classic/Button]
    Label6  [Label]
    Label7  [Label]
    lblDatumBetätigen  [Label]
    galRäume  [Gallery]
      Rectangle7  [Rectangle]
      Label11  [Label]
      Image1  [Image]
      Title1  [Label]
      Subtitle1  [Label]
      lblSlot1Info  [Label]
      lblSlot2Info  [Label]
      lblSlot3Info  [Label]
      lblSlot4Info  [Label]
      NextArrow1  [Classic/Icon]
      Rectangle2  [Rectangle]
      btnSlot1  [Classic/Button]
      btnSlot2  [Classic/Button]
      btnSlot3  [Classic/Button]
      btnSlot4  [Classic/Button]
  conRaumBestätigen  [GroupContainer]
    Label9  [Label]
    Label10  [Label]
    btnSpeichernRaumPanel  [Classic/Button]
    Button7  [Classic/Button]
    recZeitleisteBg  [Rectangle]
    recNeueBuchung  [Rectangle]
    recBuchungDavor1  [Rectangle]
    recBuchungDanach1  [Rectangle]
    Label4  [Label]
    Label5  [Label]
    Label13  [Label]
    Label17  [Label]
    Image5  [Image]
  conBuchungDialog  [GroupContainer]
    Rectangle5  [Rectangle]
    Image2  [Image]
    Label3  [Label]
    Label2  [Label]
    Label12  [Label]
    ddStart  [Classic/DropDown]
    ddEnde  [Classic/DropDown]
    btnSpeichern  [Classic/Button]
    btnAbbrechen  [Classic/Button]
    dpDatum  [Classic/DatePicker]
    chkWiederholen  [Classic/CheckBox]
    tglTagMo  [Classic/Toggle]
    tglTagDi  [Classic/Toggle]
    tglTagMi  [Classic/Toggle]
    tglTagDo  [Classic/Toggle]
    tglTagFr  [Classic/Toggle]
    dpWiederholenBis  [Classic/DatePicker]
    Rectangle6  [Rectangle]
    Label15  [Label]
  conCheckinDialog  [GroupContainer]
    Image1_4  [Image]
    Rectangle6_1  [Rectangle]
    lblTitel  [Label]
    lblZeit  [Label]
    btnEinchecken  [Classic/Button]
    btnSchließen2  [Classic/Button]
  conDetailsPopup  [GroupContainer]
    Image7  [Image]
    Rectangle6_2  [Rectangle]
    lblTitel2  [Label]
    lblZeit2  [Label]
    lblPerson  [Label]
    lblStatus  [Label]
    btnSchließen3  [Classic/Button]
  conVerwaltenDialog  [GroupContainer]
    lblTitel3  [Label]
    lblZeit3  [Label]
    btnStornieren  [Classic/Button]
    btnVerlängern  [Classic/Button]
    btnSchließen4  [Classic/Button]
    btnPlus1Std  [Classic/Button]
    btnPlus2Std  [Classic/Button]
    btnPlus3Std  [Classic/Button]
  conBuchungen  [GroupContainer]
    galAlleTischbuchungen  [Gallery]
      Rectangle4_2  [Rectangle]
      Image1_3  [Image]
      Image3_2  [Image]
      lblTischName  [Label]
      lblRaumZeit  [Label]
      Rectangle3_2  [Rectangle]
      btnVerwalten_2  [Classic/Button]
      chkAuswahl  [Classic/CheckBox]
    lblÜberschriftBuchungen  [Label]
    conVerwaltenDialog_1  [GroupContainer]
      lblTitel3_1  [Label]
      lblZeit3_1  [Label]
      lblVerwaltenTag  [Label]
      btnStornieren_1  [Classic/Button]
      btnVerlängern_1  [Classic/Button]
      btnSchließen4_1  [Classic/Button]
      btnPlus1Std_1  [Classic/Button]
      btnPlus2Std_1  [Classic/Button]
      btnPlus3Std_1  [Classic/Button]
      btnMinus1Std  [Classic/Button]
      btnMinus2Std  [Classic/Button]
      btnMinus3std  [Classic/Button]
    conVerwaltenKlein  [GroupContainer]
      lblVerwaltenKleinDatum  [Label]
      lblVerwaltenKleinZeit  [Label]
      lblVerwaltenKleinTitel  [Label]
      btnStornierenKlein  [Classic/Button]
      btnSchließenKlein  [Classic/Button]
    lblTischLeer_1  [Label]
    tglAuswahlModus  [Classic/Toggle]
    chkAlleAuswählen  [Classic/CheckBox]
    Icon1  [Classic/Icon]
  conHeader  [GroupContainer]
    Image6  [Image]
    btnTabDashboard  [Classic/Button]
    btnTabBuchungen  [Classic/Button]
    Circle2  [Circle]
    lblInitialen  [Label]
    btnHitArea_1  [Classic/Button]
  conLadeOverlay  [GroupContainer]
    imgSpinner  [Image]
```

## App

### [APP] App
Typ: `App` · Properties: 3 · Quelle: `src/Src/App.pa.yaml`

**Formulas**
```powerfx
=BasisBreite = 1920;
BasisHoehe = 1080;
BasisSkalierung = Min(conGrundriss.Width / BasisBreite, conGrundriss.Height / BasisHoehe);
BasisKachelbreiteQuer = 101;
BasisKachelhoeheQuer = 60;
BasisKachelbreiteHoch = 60;
BasisKachelhoeheHoch = 101;
BasisKreisgroesse = 39;
btnAbstand = 6;
btnBreite = Min(80, Max(44, (conVerwaltenDialog_1.Width - 5*btnAbstand - 40) / 6));
BasisKachelbreiteHochUG = 52;
BasisKachelhoeheHochUG = 89;
BasisKachelbreiteQuerUG = 89;
BasisKachelhoeheQuerUG = 52;
BasisKreisgroesseUG = 34;
BasisSchriftgroesseUG = 12;
// Josias 2026-09-28: eigene Breite fuer Big Table UG, deutlich breiter als Standardtisch, Hoehe bleibt Basishoehe horizontal
BasisKachelbreiteBigTableUG = 220;

// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch in derselben Reihenfolge wie Gallery1.Items (Gallery1 versetzt jeden Eintrag um eine Vorlagenhoehe)
TischNrOG = With({src: Filter(Tische, Geschoss.Value = "OG")}, ForAll(Sequence(CountRows(src)), {Titel: Index(src, Value).Titel, Nr: Value}));
TischNrUG = With({src: Filter(Tische, Geschoss.Value = "UG")}, ForAll(Sequence(CountRows(src)), {Titel: Index(src, Value).Titel, Nr: Value}));
// Grundriss-Fix 2026-09-30: Skalierung, bei der die Tischpositionen eingemessen wurden (Design 1366 x 768 -> conGrundriss 881 x 678)
BasisSkalierungReferenz = Min(881 / BasisBreite, 678 / BasisHoehe);
```

**OnStart**
```powerfx
=Set(varSelectedTisch, Blank());
Set(varZeigeDialog, false);
Set(varZeigeDetails, false);
Set(varZeigeCheckin, false);
Set(varZeigeVerwalten, false);
Set(varZeigeVerlaengern, false);
Set(varSelectedBuchung, Blank());
Set(varAktiverTab, "dashboard");
Set(varZeigeRaumBuchungForm, false);
Set(varAusgewähltRaum, Blank());
Set(varAusgewählteStartzeit, Blank());
Set(varAusgewählteEndzeit, Blank());
Set(varZeigeRaumBestätigung, false);
Set(varWiederholen, false);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Set(varWiederholenBis, Today() + 14);
Set(varAusgewaehltePlusDauer, Blank());
Set(varZeigeRaumInfo, false);
Set(varZeigeRaumVerwalten, false);
Set(
  varProfilFarbe,
  Switch(
    RandBetween(1, 8),
    1, ColorValue("#8CAFF4"),
    2, ColorValue("#82C7B3"),
    3, ColorValue("#EFA897"),
    4, ColorValue("#B59EDC"),
    5, ColorValue("#82CCC5"),
    6, ColorValue("#F5C295"),
    7, ColorValue("#A1AADB"),
    ColorValue("#A1B1BA")
  )
);
Set(varZoom, 1);
Set(varPanX, 0);
Set(varPanY, 0);
Set(varWiederholenBisGewaehlt, false);
ClearCollect(
  colTischPositionen,
  {Tisch: "OG Desk 1", X: 1380, Y: 270, Ausrichtung: "Vertikal"},
  {Tisch: "OG Desk 2", X: 1629, Y: 290, Ausrichtung: "Horizontal"},
  {Tisch: "OG Desk 3", X: 1732, Y: 288, Ausrichtung: "Horizontal"},
  {Tisch: "OG Desk 4", X: 1629, Y: 348, Ausrichtung: "Horizontal"},
  {Tisch: "OG Desk 5", X: 1732, Y: 346, Ausrichtung: "Horizontal"},
  {Tisch: "OG Desk 6", X: 1734, Y: 536, Ausrichtung: "Horizontal"},
  {Tisch: "OG Desk 7", X: 1734, Y: 596, Ausrichtung: "Horizontal"},
  {Tisch: "OG Desk 8", X: 1500, Y: 484, Ausrichtung: "Vertikal"},
  {Tisch: "OG Desk 9", X: 1500, Y: 584, Ausrichtung: "Vertikal"},
  {Tisch: "OG Desk 10", X: 1500, Y: 683, Ausrichtung: "Vertikal"},
  {Tisch: "OG Desk 11", X: 1560, Y: 468, Ausrichtung: "Vertikal"},
  {Tisch: "OG Desk 12", X: 1560, Y: 582, Ausrichtung: "Vertikal"},
  {Tisch: "OG Desk 13", X: 1560, Y: 681, Ausrichtung: "Vertikal"},
  {Tisch: "Quiet Desk 3", X: 870, Y: 687, Ausrichtung: "Vertikal"},
  {Tisch: "Quiet Desk 2", X: 870, Y: 594, Ausrichtung: "Vertikal"},
  {Tisch: "Quiet Desk 1", X: 870, Y: 501, Ausrichtung: "Vertikal"}
);
Set(varSelectedBuchungTab, Blank());
Set(varZeigeVerwaltenTab, false);
Set(varStartOverridePanel, "");
Set(varEndeOverridePanel, "");
Set(varAusgewaehltePanelDauer, Blank());
Set(varAnsichtsDatum, Today());
Set(varAusgewaehltesStockwerk, "OG");
Set(varStockwerkDropdownOffen, false);
Set(varStartOverride, "");
Set(varEndeOverride, "");
Clear(colAusgewaehlteBuchungen);
Set(varMehrfachAuswahlModus, false);
Set(varAuswahlModusAktiv, false);
Set(varZeigeVerwaltenKlein, false);
Set(varGalleryNeuAufbauen, 0);
Set(varGeklickteBuchungKlein, Blank());
ClearCollect(
  colTischPositionenUG,
  {Tisch: "UG Desk 1",  X: 530,  Y: 592, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 2",  X: 530,  Y: 679, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 3",  X: 582,  Y: 588, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 4",  X: 582,  Y: 675, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 5",  X: 738,  Y: 584, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 6",  X: 738,  Y: 671, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 7",  X: 790,  Y: 579, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 8",  X: 790,  Y: 666, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 9",  X: 1011, Y: 575, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 10", X: 1011, Y: 662, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 11", X: 1063, Y: 571, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 12", X: 1063, Y: 658, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 13", X: 1202, Y: 260, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 14", X: 1210, Y: 348, Ausrichtung: "Horizontal"},
  {Tisch: "UG Desk 15", X: 1255, Y: 256, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 16", X: 1360, Y: 254, Ausrichtung: "Vertikal"},
  {Tisch: "UG Desk 17", X: 1410, Y: 252, Ausrichtung: "Vertikal"},
  {Tisch: "Big Table", X: 1254, Y: 630, Ausrichtung: "BigTable"}
);
Set(varIsLoading, false);
Set(varSpinnerWinkel, 0)
```

**Theme**
```powerfx
=PowerAppsTheme
```

## Screens

### [SCR] Screen1
Typ: `Screen` · Properties: 3 · Z. 10 in `Screen1.pa.yaml`

**Fill**
```powerfx
=RGBA(233, 233, 235, 1)
```

**LoadingSpinner**
```powerfx
=LoadingSpinner.Data
```

**LoadingSpinnerColor**
```powerfx
=RGBA(100, 118, 132, 1)
```

## Steuerelemente (Baum, Reihenfolge wie im Quellcode)

### [C001] Screen1 / conGrundriss
Name: `conGrundriss` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 8 · Z. 16

**Height**
```powerfx
=Parent.Height - (conHeader.Y + conHeader.Height) - 15
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Width**
```powerfx
=Parent.Width - (conDashboard.X + conDashboard.Width) - 10
```

**X**
```powerfx
=conDashboard.X + conDashboard.Width + 5
```

**Y**
```powerfx
=conHeader.Y + conHeader.Height + 10
```

### [C002] Screen1 / conGrundriss / imgGrundrissOG
Name: `imgGrundrissOG` · Typ: `Image@2.2.3` · Eltern: `conGrundriss` · Properties: 7 · Z. 29

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=BasisHoehe * BasisSkalierung
```

**Image**
```powerfx
='grundriss_transparent (1)'
```

**Visible**
```powerfx
=varAusgewaehltesStockwerk = "OG"
```

**Width**
```powerfx
=BasisBreite * BasisSkalierung
```

**X**
```powerfx
=(conGrundriss.Width - imgGrundrissOG.Width) / 2
```

**Y**
```powerfx
=(conGrundriss.Height - imgGrundrissOG.Height) / 2
```

### [C003] Screen1 / conGrundriss / imgGrundrissUG
Name: `imgGrundrissUG` · Typ: `Image@2.2.3` · Eltern: `conGrundriss` · Properties: 7 · Z. 39

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=BasisHoehe * BasisSkalierung
```

**Image**
```powerfx
='grundriss_UG_bearbeitet_PREVIEW (3)'
```

**Visible**
```powerfx
=varAusgewaehltesStockwerk = "UG"
```

**Width**
```powerfx
=BasisBreite * BasisSkalierung
```

**X**
```powerfx
=(conGrundriss.Width - imgGrundrissUG.Width) / 2
```

**Y**
```powerfx
=(conGrundriss.Height - imgGrundrissUG.Height) / 2
```

### [C004] Screen1 / conGrundriss / Gallery1
Name: `Gallery1` · Typ: `Gallery@2.15.0` · Variante: `BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0` · Eltern: `conGrundriss` · Properties: 7 · Z. 49

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=imgGrundrissOG.Height
```

**Items**
```powerfx
=Filter(Tische, Geschoss.Value = varAusgewaehltesStockwerk)
```

**TemplateSize**
```powerfx
=1
```

**Width**
```powerfx
=imgGrundrissOG.Width
```

**X**
```powerfx
=imgGrundrissOG.X
```

**Y**
```powerfx
=imgGrundrissOG.Y
```

### [C005] Screen1 / conGrundriss / Gallery1 / Rectangle1
Name: `Rectangle1` · Typ: `Rectangle@2.3.0` · Eltern: `Gallery1` · Properties: 8 · Z. 61

**BorderColor**
```powerfx
=Color.Black
```

**BorderThickness**
```powerfx
=2
```

**Fill**
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
    ColorValue("#00A96B"),
    If(
      relevanteBuchung.CheckedIn,
      ColorValue("#EB3951"),
      ColorValue("#FFA500")
    )
  )
)
```

**Height**
```powerfx
=(If(
    varAusgewaehltesStockwerk = "OG",
    If(
    LookUp(colTischPositionen, Tisch = ThisItem.Titel).Ausrichtung = "Horizontal",
    BasisKachelhoeheQuer,
    BasisKachelhoeheHoch
    ),
    // Josias 2026-09-28: Big Table nutzt bewusst dieselbe Basishoehe wie andere horizontale Tische (kein eigener Hoehenwert)
    If(
    ThisItem.Titel = "Big Table",
    BasisKachelhoeheQuerUG,
    If(
    LookUp(colTischPositionenUG, Tisch = ThisItem.Titel).Ausrichtung = "Horizontal",
    BasisKachelhoeheQuerUG,
    BasisKachelhoeheHochUG
    )
    )
    ) - If(StartsWith(ThisItem.Titel, "Quiet Desk"), 7, 0)) * BasisSkalierung
```

**OnSelect**
```powerfx
=
```

**Width**
```powerfx
=(If(
    varAusgewaehltesStockwerk = "OG",
    If(
    LookUp(colTischPositionen, Tisch = ThisItem.Titel).Ausrichtung = "Horizontal",
    BasisKachelbreiteQuer,
    BasisKachelbreiteHoch
    ),
    // Josias 2026-09-28: Big Table bekommt eigene Breite statt Basisbreite (siehe BasisKachelbreiteBigTableUG)
    If(
    ThisItem.Titel = "Big Table",
    BasisKachelbreiteBigTableUG,
    If(
    LookUp(colTischPositionenUG, Tisch = ThisItem.Titel).Ausrichtung = "Horizontal",
    BasisKachelbreiteQuerUG,
    BasisKachelbreiteHochUG
    )
    )
    ) - If(StartsWith(ThisItem.Titel, "Quiet Desk"), 10, 0)) * BasisSkalierung
```

**X**
```powerfx
=If(
  varAusgewaehltesStockwerk = "OG",
  LookUp(colTischPositionen, Tisch = ThisItem.Titel).X,
  LookUp(colTischPositionenUG, Tisch = ThisItem.Titel).X
) * BasisSkalierung
```

**Y**
```powerfx
=With(
  {
    // Grundriss-Fix 2026-09-30: Gallery1 schiebt jeden Eintrag um (TemplateHeight + TemplatePadding) Pixel nach unten, unskaliert.
    // Die Positionen wurden bei BasisSkalierungReferenz eingemessen (Versatz dort eingebaut) -> Versatz dieser Groesse mitskalieren, echten Versatz abziehen.
    nrVersatz: LookUp(If(varAusgewaehltesStockwerk = "OG", TischNrOG, TischNrUG), Titel = ThisItem.Titel).Nr - 1,
    vorlagenVersatz: Gallery1.TemplateHeight + Gallery1.TemplatePadding
  },
  (If(
    varAusgewaehltesStockwerk = "OG",
    LookUp(colTischPositionen, Tisch = ThisItem.Titel).Y,
    LookUp(colTischPositionenUG, Tisch = ThisItem.Titel).Y
  ) + nrVersatz * vorlagenVersatz / BasisSkalierungReferenz) * BasisSkalierung
  - nrVersatz * vorlagenVersatz
)
```

### [C006] Screen1 / conGrundriss / Gallery1 / Circle1
Name: `Circle1` · Typ: `Circle@2.3.0` · Eltern: `Gallery1` · Properties: 9 · Z. 146

**BorderColor**
```powerfx
=With(
  { relevanteBuchung: LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)) },
  If(IsBlank(relevanteBuchung), Color.Transparent, Color.Black)
)
```

**BorderStyle**
```powerfx
=With(
  {
    istBesetzt:
      If(
        varAnsichtsDatum = Today(),
        !IsBlank(LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Now() >= Startzeit && Now() <= Endzeit)),
        !IsBlank(LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)))
      ),
    istAusstehend:
      varAnsichtsDatum = Today() &&
      !IsBlank(LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit > Now() && Startzeit <= DateAdd(Now(), 60, TimeUnit.Minutes)))
  },
  If(istBesetzt Or istAusstehend, BorderStyle.Solid, BorderStyle.None)
)
```

**BorderThickness**
```powerfx
=1
```

**Fill**
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(IsBlank(relevanteBuchung), ColorValue("#4DC398"), Color.White)
)
```

**Height**
```powerfx
=If(
  varAusgewaehltesStockwerk = "OG",
  BasisKreisgroesse,
  BasisKreisgroesseUG
) * BasisSkalierung * varZoom
```

**OnSelect**
```powerfx
=
```

**Width**
```powerfx
=If(
  varAusgewaehltesStockwerk = "OG",
  BasisKreisgroesse,
  BasisKreisgroesseUG
) * BasisSkalierung * varZoom
```

**X**
```powerfx
=Rectangle1.X + (Rectangle1.Width/2) - (Circle1.Width/2)
```

**Y**
```powerfx
=Rectangle1.Y + (Rectangle1.Height/2) - (Circle1.Height/2)
```

### [C007] Screen1 / conGrundriss / Gallery1 / Label1
Name: `Label1` · Typ: `Label@2.5.1` · Eltern: `Gallery1` · Properties: 11 · Z. 197

**Align**
```powerfx
=Align.Center
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=Circle1.Height
```

**OnSelect**
```powerfx
=
```

**Size**
```powerfx
=If(
  varAusgewaehltesStockwerk = "OG",
  13,
  BasisSchriftgroesseUG
) * BasisSkalierung
```

**Text**
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
    "",
    Upper(Left(First(Split(relevanteBuchung.Person.DisplayName, " ")).Value, 1) &
          Left(Last(Split(relevanteBuchung.Person.DisplayName, " ")).Value, 1))
  )
)
```

**Width**
```powerfx
=Circle1.Width + 4
```

**X**
```powerfx
=Circle1.X -2
```

**Y**
```powerfx
=Circle1.Y
```

### [C008] Screen1 / conGrundriss / Gallery1 / btnHitArea
Name: `btnHitArea` · Typ: `Classic/Button@2.2.0` · Eltern: `Gallery1` · Properties: 17 · Z. 233

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=Rectangle1.Height
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.15)
```

**OnSelect**
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
      Set(varSelectedTisch, ThisItem);
      Set(varZeigeDialog, true);
      Set(varZeigeDetails, false);
      Set(varZeigeCheckin, false);
      Set(varZeigeVerwalten, false);
      Set(varWiederholen, false);
      Set(varWiederholenModus, "Wochentage");
      Set(varTagMo, false);
      Set(varTagDi, false);
      Set(varTagMi, false);
      Set(varTagDo, false);
      Set(varTagFr, false);
      Set(varTagSa, false);
      Set(varTagSo, false),
      Set(varDetailsTisch, ThisItem); Set(varSelectedBuchung, relevanteBuchung);
      Set(varZeigeDetails, true);
      Set(varZeigeDialog, false);
      Set(varZeigeCheckin, false);
      Set(varZeigeVerwalten, false)
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=ColorFade(Rectangle1.Fill, -30%)
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=Rectangle1.Width
```

**X**
```powerfx
=Rectangle1.X
```

**Y**
```powerfx
=Rectangle1.Y
```

### [C009] Screen1 / conGrundriss / Image8
Name: `Image8` · Typ: `Image@2.2.3` · Eltern: `conGrundriss` · Properties: 5 · Z. 285

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=62
```

**Image**
```powerfx
=chevron_technoform
```

**X**
```powerfx
=ddStockwerk.X + 140
```

**Y**
```powerfx
=ddStockwerk.Y 
```

### [C010] Screen1 / conGrundriss / Label18
Name: `Label18` · Typ: `Label@2.5.1` · Eltern: `conGrundriss` · Properties: 7 · Z. 293

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=9
```

**Text**
```powerfx
="Matthäus-Merian-Strasse 6 / Lohfelden  >  " & If(varAusgewaehltesStockwerk = "OG", "MMS Obergeschoss", "MMS Untergeschoss")
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=ddStockwerk.X + 5
```

**Y**
```powerfx
=ddStockwerk.Y - 7
```

### [C011] Screen1 / conGrundriss / ddStockwerk
Name: `ddStockwerk` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conGrundriss` · Properties: 23 · Z. 303

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 0)
```

**BorderThickness**
```powerfx
=0
```

**ChevronBackground**
```powerfx
=RGBA(0, 0, 0, 0)
```

**ChevronFill**
```powerfx
=RGBA(0, 0, 0, 0)
```

**ChevronHoverBackground**
```powerfx
=RGBA(0, 0, 0, 0)
```

**ChevronHoverFill**
```powerfx
=RGBA(0, 0, 0, 0)
```

**Color**
```powerfx
=Color.Black
```

**Fill**
```powerfx
=RGBA(0, 0, 0, 0)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=62
```

**HoverColor**
```powerfx
=Color.Black
```

**HoverFill**
```powerfx
=RGBA(23, 20, 150, 0.08)
```

**Items**
```powerfx
=Table({Value: "MMS Obergeschoss", Kurz: "OG"}, {Value: "MMS Untergeschoss", Kurz: "UG"})
```

**Items.Value**
```powerfx
=Value
```

**OnChange**
```powerfx
=Set(varAusgewaehltesStockwerk, ddStockwerk.Selected.Kurz);
Set(varStockwerkDropdownOffen, false)
```

**OnSelect**
```powerfx
=Set(varStockwerkDropdownOffen, true);
Set(varZeigeDialog, false);
Set(varZeigeDetails, false);
Set(varZeigeCheckin, false);
Set(varZeigeVerwalten, false);
Set(varZeigeVerlaengern, false);
Set(varSelectedTisch, Blank());
Set(varSelectedBuchung, Blank());
Set(varAusgewaehltePlusDauer, 0)
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=20
```

**Y**
```powerfx
=15
```

### [C012] Screen1 / conDashboard
Name: `conDashboard` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 341

**Fill**
```powerfx
=ColorValue("#f7f7f7")
```

**Height**
```powerfx
=Parent.Height - 90
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varAktiverTab = "dashboard" && !varZeigeTischBuchungForm && !varZeigeRaumBuchungForm
```

**Width**
```powerfx
=470
```

**X**
```powerfx
=5
```

**Y**
```powerfx
=conHeader.Height + 15
```

### [C013] Screen1 / conDashboard / galTischbuchungenHeute
Name: `galTischbuchungenHeute` · Typ: `Gallery@2.15.0` · Variante: `BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0` · Eltern: `conDashboard` · Properties: 6 · Z. 357

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=400
```

**Items**
```powerfx
=Filter(
  Tischbuchungen,
  Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
)
```

**Visible**
```powerfx
=galTischbuchungenHeute.AllItemsCount > 0
```

**Width**
```powerfx
=470
```

**Y**
```powerfx
=lblMyPersonalDesk.Y + lblMyPersonalDesk.Height + 10
```

### [C014] Screen1 / conDashboard / galTischbuchungenHeute / Rectangle4
Name: `Rectangle4` · Typ: `Rectangle@2.3.0` · Eltern: `galTischbuchungenHeute` · Properties: 7 · Z. 372

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=ColorValue("#F0F0F0")
```

**Height**
```powerfx
=Parent.TemplateHeight - 20
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=Parent.TemplateWidth - 30
```

**X**
```powerfx
=15
```

**Y**
```powerfx
=10
```

### [C015] Screen1 / conDashboard / galTischbuchungenHeute / Image1_1
Name: `Image1_1` · Typ: `Image@2.2.3` · Eltern: `galTischbuchungenHeute` · Properties: 7 · Z. 382

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=72
```

**Image**
```powerfx
=img_20260916_085456
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=72
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=(Parent.TemplateHeight / 2) - (Self.Height / 2)
```

### [C016] Screen1 / conDashboard / galTischbuchungenHeute / Image3
Name: `Image3` · Typ: `Image@2.2.3` · Eltern: `galTischbuchungenHeute` · Properties: 8 · Z. 392

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=50
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**Image**
```powerfx
=img_bearbeiten_heller
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=403
```

**Y**
```powerfx
=27
```

### [C017] Screen1 / conDashboard / galTischbuchungenHeute / lblTischHeute
Name: `lblTischHeute` · Typ: `Label@2.5.1` · Eltern: `galTischbuchungenHeute` · Properties: 16 · Z. 403

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Color**
```powerfx
=RGBA(50, 49, 48, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=If(ThisItem.IsSelected, FontWeight.Semibold, FontWeight.Normal)
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=0
```

**PaddingLeft**
```powerfx
=12
```

**PaddingRight**
```powerfx
=0
```

**PaddingTop**
```powerfx
=0
```

**Size**
```powerfx
=14
```

**Text**
```powerfx
="Tisch " & ThisItem.Tisch.Value
```

**VerticalAlign**
```powerfx
=VerticalAlign.Top
```

**Width**
```powerfx
=Parent.TemplateWidth - 173
```

**X**
```powerfx
=100
```

**Y**
```powerfx
=27
```

### [C018] Screen1 / conDashboard / galTischbuchungenHeute / lblZeitHeute
Name: `lblZeitHeute` · Typ: `Label@2.5.1` · Eltern: `galTischbuchungenHeute` · Properties: 15 · Z. 422

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=If(ThisItem.IsSelected, FontWeight.Semibold, FontWeight.Normal)
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=0
```

**PaddingLeft**
```powerfx
=12
```

**PaddingRight**
```powerfx
=0
```

**PaddingTop**
```powerfx
=0
```

**Size**
```powerfx
=12
```

**Text**
```powerfx
=Text(ThisItem.Startzeit, "hh:mm") & " – " & Text(ThisItem.Endzeit, "hh:mm")
```

**VerticalAlign**
```powerfx
=VerticalAlign.Top
```

**Width**
```powerfx
=lblTischHeute.Width
```

**X**
```powerfx
=lblTischHeute.X
```

**Y**
```powerfx
=lblTischHeute.Y + lblTischHeute.Height
```

### [C019] Screen1 / conDashboard / galTischbuchungenHeute / lblStatusHeute
Name: `lblStatusHeute` · Typ: `Label@2.5.1` · Eltern: `galTischbuchungenHeute` · Properties: 7 · Z. 440

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=If(ThisItem.CheckedIn, ColorValue("#00A96B"), ColorValue("#FFA500"))
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Text**
```powerfx
=If(ThisItem.CheckedIn, "Eingecheckt", "Einchecken")
```

**X**
```powerfx
=270
```

**Y**
```powerfx
=43
```

### [C020] Screen1 / conDashboard / galTischbuchungenHeute / Rectangle3
Name: `Rectangle3` · Typ: `Rectangle@2.3.0` · Eltern: `galTischbuchungenHeute` · Properties: 7 · Z. 450

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=Parent.TemplateHeight
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PressedFill**
```powerfx
=Color.Transparent
```

**Visible**
```powerfx
=ThisItem.IsSelected
```

**Width**
```powerfx
=4
```

### [C021] Screen1 / conDashboard / galTischbuchungenHeute / btnEincheckenHeute
Name: `btnEincheckenHeute` · Typ: `Classic/Button@2.2.0` · Eltern: `galTischbuchungenHeute` · Properties: 17 · Z. 460

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=Rectangle4.Height
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.04)
```

**OnSelect**
```powerfx
=Set(varSelectedBuchung, ThisItem); Set(varZeigeCheckin, true); Set(varZeigeDetails, false); Set(varZeigeDialog, false); Set(varZeigeVerwalten, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=
```

**PressedFill**
```powerfx
=RGBA(0, 0, 0, 0.1)
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=Rectangle4.Width
```

**X**
```powerfx
=Rectangle4.X
```

**Y**
```powerfx
=Rectangle4.Y
```

### [C022] Screen1 / conDashboard / galTischbuchungenHeute / btnVerwalten
Name: `btnVerwalten` · Typ: `Classic/Button@2.2.0` · Eltern: `galTischbuchungenHeute` · Properties: 17 · Z. 480

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=50
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.2)
```

**OnSelect**
```powerfx
=Set(varSelectedBuchung, ThisItem);
Set(varZeigeVerwalten, true);
Set(varZeigeCheckin, false);
Set(varZeigeDetails, false);
Set(varZeigeDialog, false);
Set(varAusgewaehltePlusDauer, Blank())
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=400
```

**Y**
```powerfx
=30
```

### [C023] Screen1 / conDashboard / galRaumbuchungenHeute
Name: `galRaumbuchungenHeute` · Typ: `Gallery@2.15.0` · Variante: `BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0` · Eltern: `conDashboard` · Properties: 7 · Z. 506

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=260
```

**Items**
```powerfx
=Filter(Raumbuchungen, Person.Email = User().Email && Startzeit >= Today() && Startzeit < DateAdd(Today(), 1, TimeUnit.Days) && Endzeit >= Now())
```

**Visible**
```powerfx
=false
```

**Width**
```powerfx
=470
```

**X**
```powerfx
=galTischbuchungenHeute.X
```

**Y**
```powerfx
=lblMyMeetings.Y + lblMyMeetings.Height + 5
```

### [C024] Screen1 / conDashboard / galRaumbuchungenHeute / Rectangle4_1
Name: `Rectangle4_1` · Typ: `Rectangle@2.3.0` · Eltern: `galRaumbuchungenHeute` · Properties: 7 · Z. 518

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=ColorValue("#F0F0F0")
```

**Height**
```powerfx
=Parent.TemplateHeight - 20
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=Parent.TemplateWidth - 30
```

**X**
```powerfx
=15
```

**Y**
```powerfx
=10
```

### [C025] Screen1 / conDashboard / galRaumbuchungenHeute / Image1_2
Name: `Image1_2` · Typ: `Image@2.2.3` · Eltern: `galRaumbuchungenHeute` · Properties: 7 · Z. 528

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=72
```

**Image**
```powerfx
=img_meetings_kraeftiger
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=72
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=(Parent.TemplateHeight / 2) - (Self.Height / 2)
```

### [C026] Screen1 / conDashboard / galRaumbuchungenHeute / Image3_1
Name: `Image3_1` · Typ: `Image@2.2.3` · Eltern: `galRaumbuchungenHeute` · Properties: 7 · Z. 538

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=50
```

**Image**
```powerfx
=img_bearbeiten_heller
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=403
```

**Y**
```powerfx
=27
```

### [C027] Screen1 / conDashboard / galRaumbuchungenHeute / Rectangle3_1
Name: `Rectangle3_1` · Typ: `Rectangle@2.3.0` · Eltern: `galRaumbuchungenHeute` · Properties: 6 · Z. 548

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=Parent.TemplateHeight
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Visible**
```powerfx
=ThisItem.IsSelected
```

**Width**
```powerfx
=4
```

### [C028] Screen1 / conDashboard / galRaumbuchungenHeute / lblTischHeute_1
Name: `lblTischHeute_1` · Typ: `Label@2.5.1` · Eltern: `galRaumbuchungenHeute` · Properties: 8 · Z. 557

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Text**
```powerfx
="Raum " & ThisItem.Raum.Value
```

**Width**
```powerfx
=Parent.TemplateWidth - 173
```

**X**
```powerfx
=100
```

**Y**
```powerfx
=27
```

### [C029] Screen1 / conDashboard / galRaumbuchungenHeute / lblZeitHeute_1
Name: `lblZeitHeute_1` · Typ: `Label@2.5.1` · Eltern: `galRaumbuchungenHeute` · Properties: 8 · Z. 568

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Text**
```powerfx
=Text(ThisItem.Startzeit, "hh:mm") & " – " & Text(ThisItem.Endzeit, "hh:mm")
```

**Width**
```powerfx
=lblTischHeute_1.Width
```

**X**
```powerfx
=lblTischHeute_1.X
```

**Y**
```powerfx
=lblTischHeute_1.Y + lblTischHeute_1.Height
```

### [C030] Screen1 / conDashboard / galRaumbuchungenHeute / btnInfoRaum
Name: `btnInfoRaum` · Typ: `Classic/Button@2.2.0` · Eltern: `galRaumbuchungenHeute` · Properties: 17 · Z. 579

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=Rectangle4_1.Height
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.04)
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=Rectangle4_1.Width
```

**X**
```powerfx
=Rectangle4_1.X
```

**Y**
```powerfx
=Rectangle4_1.Y
```

### [C031] Screen1 / conDashboard / galRaumbuchungenHeute / btnVerwalten_1
Name: `btnVerwalten_1` · Typ: `Classic/Button@2.2.0` · Eltern: `galRaumbuchungenHeute` · Properties: 16 · Z. 599

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=50
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.2)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=400
```

**Y**
```powerfx
=30
```

### [C032] Screen1 / conDashboard / Image4
Name: `Image4` · Typ: `Image@2.2.3` · Eltern: `conDashboard` · Properties: 5 · Z. 618

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=dpAnsichtsDatum.Height
```

**Image**
```powerfx
=chevron_technoform
```

**X**
```powerfx
=85
```

**Y**
```powerfx
=dpAnsichtsDatum.Y - 2
```

### [C033] Screen1 / conDashboard / lblTischLeer
Name: `lblTischLeer` · Typ: `Label@2.5.1` · Eltern: `conDashboard` · Properties: 6 · Z. 626

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
="---"
```

**Visible**
```powerfx
=galTischbuchungenHeute.AllItemsCount = 0
```

**X**
```powerfx
=60
```

**Y**
```powerfx
=galTischbuchungenHeute.Y 
```

### [C034] Screen1 / conDashboard / lblRaumLeer
Name: `lblRaumLeer` · Typ: `Label@2.5.1` · Eltern: `conDashboard` · Properties: 7 · Z. 635

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=20
```

**Text**
```powerfx
="---"
```

**Visible**
```powerfx
=false
```

**X**
```powerfx
=60
```

**Y**
```powerfx
=galRaumbuchungenHeute.Y + 10
```

### [C035] Screen1 / conDashboard / lblMyPersonalDesk
Name: `lblMyPersonalDesk` · Typ: `Label@2.5.1` · Eltern: `conDashboard` · Properties: 8 · Z. 645

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=10
```

**Text**
```powerfx
="My personal desk"
```

**Width**
```powerfx
=200
```

**X**
```powerfx
=galTischbuchungenHeute.X + 10
```

**Y**
```powerfx
=75
```

### [C036] Screen1 / conDashboard / lblMyMeetings
Name: `lblMyMeetings` · Typ: `Label@2.5.1` · Eltern: `conDashboard` · Properties: 7 · Z. 656

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Text**
```powerfx
="My meetings"
```

**Visible**
```powerfx
=false
```

**X**
```powerfx
=galTischbuchungenHeute.X + 10
```

**Y**
```powerfx
=btnTischHinzufügen.Y + btnTischHinzufügen.Height + 20
```

### [C037] Screen1 / conDashboard / lblDatumLabel
Name: `lblDatumLabel` · Typ: `Label@2.5.1` · Eltern: `conDashboard` · Properties: 7 · Z. 666

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=RGBA(120, 120, 120, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=12
```

**Text**
```powerfx
="Datum"
```

**X**
```powerfx
=10
```

**Y**
```powerfx
=dpAnsichtsDatum.Y - 17
```

### [C038] Screen1 / conDashboard / Label16
Name: `Label16` · Typ: `Label@2.5.1` · Eltern: `conDashboard` · Properties: 8 · Z. 676

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=51
```

**Size**
```powerfx
=16  
```

**Text**
```powerfx
=If(varAnsichtsDatum = Today(), "Heute", Text(varAnsichtsDatum, "dd.mm.yyyy"))
```

**X**
```powerfx
=dpAnsichtsDatum.X
```

**Y**
```powerfx
=dpAnsichtsDatum.Y
```

### [C039] Screen1 / conDashboard / btnRaumHinzufügen
Name: `btnRaumHinzufügen` · Typ: `Classic/Button@2.2.0` · Eltern: `conDashboard` · Properties: 18 · Z. 687

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#D0D0D0")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.2)
```

**OnSelect**
```powerfx
=Set(varZeigeRaumBuchungForm, true)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Size**
```powerfx
=11
```

**Text**
```powerfx
="Raum Buchen"
```

**Visible**
```powerfx
=false
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=40
```

**Y**
```powerfx
=galRaumbuchungenHeute.Y + 
If(
  galRaumbuchungenHeute.AllItemsCount = 0, 40,
  Min(galRaumbuchungenHeute.AllItemsCount * 104, 260)
) + 20
```

### [C040] Screen1 / conDashboard / btnTischHinzufügen
Name: `btnTischHinzufügen` · Typ: `Classic/Button@2.2.0` · Eltern: `conDashboard` · Properties: 17 · Z. 713

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#D0D0D0")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.2)
```

**OnSelect**
```powerfx
=Set(varZeigeTischBuchungForm, true);
Set(varWiederholen, false);
Reset(chkWiederholenPanel);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Reset(tglTagMo_1);
Reset(tglTagDi_1);
Reset(tglTagMi_1);
Reset(tglTagDo_1);
Reset(tglTagFr_1);
Set(varAusgewaehltePanelDauer, Blank());
Set(varStartOverridePanel, "");
Set(varEndeOverridePanel, "")
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Size**
```powerfx
=11
```

**Text**
```powerfx
="Tisch Buchen"
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=40
```

**Y**
```powerfx
=galTischbuchungenHeute.Y + 
If(
  galTischbuchungenHeute.AllItemsCount = 0, 40,
  Min(galTischbuchungenHeute.AllItemsCount * 104, 400)
) + 20
```

### [C041] Screen1 / conDashboard / dpAnsichtsDatum
Name: `dpAnsichtsDatum` · Typ: `Classic/DatePicker@2.6.0` · Eltern: `conDashboard` · Properties: 12 · Z. 757

**BorderColor**
```powerfx
=Color.Transparent
```

**BorderThickness**
```powerfx
=0
```

**Color**
```powerfx
=Color.Transparent
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=51
```

**IconBackground**
```powerfx
=Color.Transparent
```

**IconFill**
```powerfx
=Color.Transparent
```

**OnChange**
```powerfx
=Set(varAnsichtsDatum, dpAnsichtsDatum.SelectedDate)
```

**Width**
```powerfx
=150
```

**X**
```powerfx
=10
```

**Y**
```powerfx
=24
```

### [C042] Screen1 / conDashboard / Icon1_1
Name: `Icon1_1` · Typ: `Classic/Icon@2.5.0` · Eltern: `conDashboard` · Properties: 8 · Z. 772

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=20
```

**Icon**
```powerfx
=Icon.Sync
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Width**
```powerfx
=20
```

**X**
```powerfx
=140
```

**Y**
```powerfx
=87
```

### [C043] Screen1 / conTischBuchungenPanel
Name: `conTischBuchungenPanel` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 787

**Fill**
```powerfx
=ColorValue("#f7f7f7")
```

**Height**
```powerfx
=conDashboard.Height
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeTischBuchungForm
```

**Width**
```powerfx
=conDashboard.Width
```

**X**
```powerfx
=conDashboard.X
```

**Y**
```powerfx
=conDashboard.Y 
```

### [C044] Screen1 / conTischBuchungenPanel / lblTischeBuchenPanel
Name: `lblTischeBuchenPanel` · Typ: `Label@2.5.1` · Eltern: `conTischBuchungenPanel` · Properties: 8 · Z. 802

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=17
```

**Text**
```powerfx
="Tisch Buchen"
```

**Width**
```powerfx
=200
```

**X**
```powerfx
=75
```

**Y**
```powerfx
=45
```

### [C045] Screen1 / conTischBuchungenPanel / ddTischePanel
Name: `ddTischePanel` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conTischBuchungenPanel` · Properties: 16 · Z. 814

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=Tische
```

**Items.Value**
```powerfx
=Title
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Width**
```powerfx
=350
```

**X**
```powerfx
=80
```

**Y**
```powerfx
=100
```

### [C046] Screen1 / conTischBuchungenPanel / ddStartTischePanel
Name: `ddStartTischePanel` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conTischBuchungenPanel` · Properties: 17 · Z. 833

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Default**
```powerfx
=If(
  varStartOverridePanel <> "",
  varStartOverridePanel,
  With(
    { minutenJetzt: Hour(Now())*60 + Minute(Now()) },
    With(
      {
        minutenStart:
          If(
            dpDatumTischePanel.SelectedDate = Today(),
            30 * RoundUp(minutenJetzt / 30, 0),
            8 * 60
          )
      },
      Text(Time(RoundDown(minutenStart / 60, 0), Mod(minutenStart, 60), 0), "hh:mm")
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) },
  With(
    {
      minutenStart:
        If(
          dpDatumTischePanel.SelectedDate = Today(),
          30 * RoundUp(minutenJetzt / 30, 0),
          8 * 60
        ),
      minutenEnde: 22 * 60
    },
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30, 0) + 1, 0),
      With(
        { m: minutenStart + Value * 30 },
        { Value: Text(Time(RoundDown(m / 60, 0), Mod(m, 60), 0), "hh:mm") }
      )
    )
  )
)
```

**Items.Value**
```powerfx
=Value
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Width**
```powerfx
=240
```

**X**
```powerfx
=ddTischePanel.X
```

**Y**
```powerfx
=220
```

### [C047] Screen1 / conTischBuchungenPanel / dpDatumTischePanel
Name: `dpDatumTischePanel` · Typ: `Classic/DatePicker@2.6.0` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 892

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**DefaultDate**
```powerfx
=varAnsichtsDatum
```

**Font**
```powerfx
=Font.'Open Sans'
```

**IconBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**IconFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**OnChange**
```powerfx
=Reset(ddStartTischePanel);
Reset(ddEndTischePanel)
```

**Width**
```powerfx
=ddTischePanel.Width
```

**X**
```powerfx
=ddTischePanel.X
```

**Y**
```powerfx
=160
```

### [C048] Screen1 / conTischBuchungenPanel / ddEndTischePanel
Name: `ddEndTischePanel` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conTischBuchungenPanel` · Properties: 17 · Z. 906

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Default**
```powerfx
=If(
  varEndeOverridePanel = "",
  Text(
    DateAdd(
      Time(Value(Left(ddStartTischePanel.Selected.Value, 2)), Value(Mid(ddStartTischePanel.Selected.Value, 4, 2)), 0),
      30,
      TimeUnit.Minutes
    ),
    "hh:mm"
  ),
  varEndeOverridePanel
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=With(
  { startMinuten: Value(Left(ddStartTischePanel.Selected.Value, 2)) * 60 + Value(Mid(ddStartTischePanel.Selected.Value, 4, 2)) },
  ForAll(
    Sequence(RoundDown((22*60 - startMinuten) / 30, 0), 1),
    With(
      { m: startMinuten + Value * 30 },
      { Value: Text(Time(RoundDown(m / 60, 0), Mod(m, 60), 0), "hh:mm") }
    )
  )
)
```

**Items.Value**
```powerfx
=Value
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Width**
```powerfx
=240
```

**X**
```powerfx
=ddTischePanel.X
```

**Y**
```powerfx
=280
```

### [C049] Screen1 / conTischBuchungenPanel / btnSpeichernTischePanel
Name: `btnSpeichernTischePanel` · Typ: `Classic/Button@2.2.0` · Eltern: `conTischBuchungenPanel` · Properties: 15 · Z. 948

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
With(
  {
    neuStart: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddStartTischePanel.Selected.Value, 2)), Value(Mid(ddStartTischePanel.Selected.Value, 4, 2)), 0),
    neuEnde: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddEndTischePanel.Selected.Value, 2)), Value(Mid(ddEndTischePanel.Selected.Value, 4, 2)), 0),
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate),
    bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel)
  },
  With(
    { effektivesBis: Min(effektivesBisRoh, dpDatumTischePanel.SelectedDate + 14) },
    With(
      { anzahlTage: DateDiff(dpDatumTischePanel.SelectedDate, effektivesBis, TimeUnit.Days) + 1 },
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage, 0), DateAdd(dpDatumTischePanel.SelectedDate, Value, TimeUnit.Days)) },
        With(
          {
            datumsListe:
              If(
                !varWiederholen,
                [dpDatumTischePanel.SelectedDate],
                If(
                  varWiederholenModus = "Taeglich",
                  alleDatumsWerte,
                  Filter(
                    alleDatumsWerte,
                    Switch(
                      Weekday(Value, StartOfWeek.Monday),
                      1, varTagMo, 2, varTagDi, 3, varTagMi, 4, varTagDo, 5, varTagFr, 6, varTagSa, 7, varTagSo
                    )
                  )
                )
              )
          },
          If(
            varWiederholen && CountRows(datumsListe) = 0,
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo,
              Notify("Bitte mindestens einen Wochentag auswählen.", NotificationType.Warning),
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen.", NotificationType.Warning)
            ),
            With(
              {
                ergebnisse:
                  ForAll(
                    datumsListe As Eintrag,
                    If(
                      CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0)))) = 0,
                      With(
                        {
                          neuerEintrag: Patch(Tischbuchungen, Defaults(Tischbuchungen), {
                            Tisch: {Id: ddTischePanel.Selected.ID, Value: ddTischePanel.Selected.Titel},
                            Startzeit: Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0),
                            Endzeit: Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0),
                            Person: {
                              Claims: "i:0#.f|membership|" & Lower(User().Email),
                              Department: "",
                              DisplayName: User().FullName,
                              Email: User().Email,
                              JobTitle: "",
                              Picture: ""
                            }
                          })
                        },
                        "gespeichert"
                      ),
                      "übersprungen"
                    )
                  )
              },
              With(
                { anzahlUebersprungen: CountRows(Filter(ergebnisse, Value = "übersprungen")) },
                If(
                  effektivesBisRoh > effektivesBis,
                  Notify("Wiederholung wurde auf 2 Wochen begrenzt.", NotificationType.Warning),
                  If(
                    anzahlUebersprungen > 0,
                    Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden.", NotificationType.Warning),
                    Notify("Buchung(en) erfolgreich gespeichert.", NotificationType.Success)
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);
Refresh(Tischbuchungen);
Set(varZeigeTischBuchungForm, false);
Set(varAktiverTab, "dashboard");
Set(varWiederholen, false);
Reset(chkWiederholenPanel);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Reset(tglTagMo_1);
Reset(tglTagDi_1);
Reset(tglTagMi_1);
Reset(tglTagDo_1);
Reset(tglTagFr_1);
Set(varAusgewaehltePanelDauer, Blank());
Set(varStartOverridePanel, "");
Set(varEndeOverridePanel, "");
Set(varIsLoading, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="Speichern"
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - btnSpeichernTischePanel.Width
```

**Y**
```powerfx
=tglTagFr_1.Y + tglTagFr_1.Height + 20
```

### [C050] Screen1 / conTischBuchungenPanel / btnAbbrechenTischePanel
Name: `btnAbbrechenTischePanel` · Typ: `Classic/Button@2.2.0` · Eltern: `conTischBuchungenPanel` · Properties: 16 · Z. 1076

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=RGBA(150, 150, 150, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**OnSelect**
```powerfx
=Set(varZeigeTischBuchungForm, false);
Set(varZeigeTischBuchungForm, false);
Set(varWiederholen, false);
Reset(chkWiederholenPanel)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="<"
```

**Width**
```powerfx
=40
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=45
```

### [C051] Screen1 / conTischBuchungenPanel / tglTagMo_1
Name: `tglTagMo_1` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 1099

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**FalseText**
```powerfx
="Mo"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagMo, tglTagMo_1.Value)
```

**TrueFill**
```powerfx
=ColorValue("#00a96b")
```

**TrueText**
```powerfx
="Mo"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - tglTagMi_1.Width
```

**Y**
```powerfx
=chkWiederholenPanel.Y + (chkWiederholenPanel.Height / 2) - (tglTagMo_1.Height / 2)
```

### [C052] Screen1 / conTischBuchungenPanel / tglTagDi_1
Name: `tglTagDi_1` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 1111

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**FalseText**
```powerfx
="Di"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagDi, tglTagDi_1.Value)
```

**TrueFill**
```powerfx
=ColorValue("#00a96b")
```

**TrueText**
```powerfx
="Di"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - tglTagMi_1.Width
```

**Y**
```powerfx
=tglTagMo_1.Y + tglTagMo_1.Height +  10
```

### [C053] Screen1 / conTischBuchungenPanel / tglTagMi_1
Name: `tglTagMi_1` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 1123

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**FalseText**
```powerfx
="Mi"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagMi, tglTagMi_1.Value)
```

**TrueFill**
```powerfx
=ColorValue("#00a96b")
```

**TrueText**
```powerfx
="Mi"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - tglTagMi_1.Width
```

**Y**
```powerfx
=tglTagDi_1.Y + tglTagMo_1.Height +  10
```

### [C054] Screen1 / conTischBuchungenPanel / tglTagDo_1
Name: `tglTagDo_1` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 1135

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**FalseText**
```powerfx
="Do"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagDo, tglTagDo_1.Value)
```

**TrueFill**
```powerfx
=ColorValue("#00a96b")
```

**TrueText**
```powerfx
="Do"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - tglTagMi_1.Width
```

**Y**
```powerfx
=tglTagMi_1.Y + tglTagMo_1.Height +  10
```

### [C055] Screen1 / conTischBuchungenPanel / tglTagFr_1
Name: `tglTagFr_1` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 1147

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**FalseText**
```powerfx
="Fr"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagFr, tglTagFr_1.Value)
```

**TrueFill**
```powerfx
=ColorValue("#00a96b")
```

**TrueText**
```powerfx
="Fr"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - tglTagMi_1.Width
```

**Y**
```powerfx
=tglTagDo_1.Y + tglTagMo_1.Height +  10
```

### [C056] Screen1 / conTischBuchungenPanel / chkWiederholenPanel
Name: `chkWiederholenPanel` · Typ: `Classic/CheckBox@2.1.0` · Eltern: `conTischBuchungenPanel` · Properties: 10 · Z. 1159

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckboxBorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckmarkFill**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**OnCheck**
```powerfx
=Set(varWiederholen, true)
```

**OnUncheck**
```powerfx
=Set(varWiederholen, false)
```

**Text**
```powerfx
="Wiederholen"
```

**X**
```powerfx
=ddTischePanel.X
```

**Y**
```powerfx
=320
```

### [C057] Screen1 / conTischBuchungenPanel / dpWiederholenBis_1
Name: `dpWiederholenBis_1` · Typ: `Classic/DatePicker@2.6.0` · Eltern: `conTischBuchungenPanel` · Properties: 12 · Z. 1172

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**IconBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**IconFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**OnChange**
```powerfx
=If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate)
```

**OnSelect**
```powerfx
=Set(varWiederholenBis, dpWiederholenBis_1.SelectedDate)
```

**StartOfWeek**
```powerfx
=StartOfWeek.Monday
```

**StartYear**
```powerfx
=2026
```

**Visible**
```powerfx
=varWiederholen
```

**Width**
```powerfx
=200
```

**X**
```powerfx
=ddTischePanel.X
```

**Y**
```powerfx
=380
```

### [C058] Screen1 / conTischBuchungenPanel / Label14
Name: `Label14` · Typ: `Label@2.5.1` · Eltern: `conTischBuchungenPanel` · Properties: 9 · Z. 1187

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=If(
  DateDiff(dpDatum.SelectedDate, dpWiederholenBis_1.SelectedDate, TimeUnit.Days) > 14,
  ColorValue("#EB3951"),
  RGBA(50, 49, 48, 1)
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=67
```

**Text**
```powerfx
=If(
  DateDiff(dpDatum.SelectedDate, dpWiederholenBis_1.SelectedDate, TimeUnit.Days) > 14,
  "*Zu weit gewählt —      es werden 2 Wochen gespeichert",
  "*Wiederholung nur für max. 2 Wochen möglich"
)
```

**Visible**
```powerfx
=varWiederholen
```

**Width**
```powerfx
=211
```

**X**
```powerfx
=ddTischePanel.X
```

**Y**
```powerfx
=420
```

### [C059] Screen1 / conTischBuchungenPanel / btn5Std
Name: `btn5Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conTischBuchungenPanel` · Properties: 18 · Z. 1209

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 5, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 5, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      varAusgewaehltePanelDauer = 5,
      ColorValue("#00A96B"),
      If(
        endeZeit > tagesEnde,
        ColorFade(ColorValue("#EB3951"), 70%),
        If(
          IsBlank(ddTischePanel.Selected),
          ColorFade(ColorValue("#00A96B"), 70%),
          If(
            CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0,
            ColorFade(ColorValue("#00A96B"), 70%),
            ColorFade(ColorValue("#EB3951"), 70%)
          )
        )
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 5 },
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 5, TimeUnit.Hours),
        tagesEnde: Time(22, 0, 0)
      },
      If(
        !warAusgewaehlt && endeZeit > tagesEnde,
        Notify("Für 5 Std. ab jetzt reicht der Tag nicht mehr aus.", NotificationType.Warning),
        Set(varAusgewaehltePanelDauer, If(warAusgewaehlt, Blank(), 5));
        Set(varStartOverridePanel, If(warAusgewaehlt, "", Text(startZeit, "hh:mm")));
        Set(varEndeOverridePanel, If(warAusgewaehlt, "", Text(endeZeit, "hh:mm")))
      )
    )
  )
);
Reset(ddStartTischePanel);
Reset(ddEndTischePanel)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="5 Std"
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - btn5Std.Width
```

**Y**
```powerfx
=ddStartTischePanel.Y
```

### [C060] Screen1 / conTischBuchungenPanel / btn9Std
Name: `btn9Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conTischBuchungenPanel` · Properties: 18 · Z. 1294

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 9, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 9, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      varAusgewaehltePanelDauer = 9,
      ColorValue("#00A96B"),
      If(
        endeZeit > tagesEnde,
        ColorFade(ColorValue("#EB3951"), 70%),
        If(
          IsBlank(ddTischePanel.Selected),
          ColorFade(ColorValue("#00A96B"), 70%),
          If(
            CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0,
            ColorFade(ColorValue("#00A96B"), 70%),
            ColorFade(ColorValue("#EB3951"), 70%)
          )
        )
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 9 },
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 9, TimeUnit.Hours),
        tagesEnde: Time(22, 0, 0)
      },
      If(
        !warAusgewaehlt && endeZeit > tagesEnde,
        Notify("Für 9 Std. ab jetzt reicht der Tag nicht mehr aus.", NotificationType.Warning),
        Set(varAusgewaehltePanelDauer, If(warAusgewaehlt, Blank(), 9));
        Set(varStartOverridePanel, If(warAusgewaehlt, "", Text(startZeit, "hh:mm")));
        Set(varEndeOverridePanel, If(warAusgewaehlt, "", Text(endeZeit, "hh:mm")))
      )
    )
  )
);
Reset(ddStartTischePanel);
Reset(ddEndTischePanel)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="9 Std"
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=ddTischePanel.X + ddTischePanel.Width - btn9Std.Width
```

**Y**
```powerfx
=ddEndTischePanel.Y
```

### [C061] Screen1 / conRaumBuchungenPanel
Name: `conRaumBuchungenPanel` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 5 · Z. 1379

**Fill**
```powerfx
=ColorValue("#f7f7f7")
```

**Height**
```powerfx
=conDashboard.Height
```

**Visible**
```powerfx
=varZeigeRaumBuchungForm
```

**Width**
```powerfx
=620
```

**Y**
```powerfx
=80
```

### [C062] Screen1 / conRaumBuchungenPanel / dpDatumRaum
Name: `dpDatumRaum` · Typ: `Classic/DatePicker@2.6.0` · Eltern: `conRaumBuchungenPanel` · Properties: 8 · Z. 1389

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(241, 241, 241, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**IconBackground**
```powerfx
=RGBA(220, 220, 220, 1)
```

**IconFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Width**
```powerfx
=150
```

**X**
```powerfx
=60
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y + lblRaumBuchenPanel.Height + 50
```

### [C063] Screen1 / conRaumBuchungenPanel / ddDauerRaumPanel
Name: `ddDauerRaumPanel` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conRaumBuchungenPanel` · Properties: 17 · Z. 1400

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Fill**
```powerfx
=RGBA(241, 241, 241, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=Table(
  {Value: "30 Min.", Minuten: 30},
  {Value: "1 Stunde", Minuten: 60},
  {Value: "1,5 Stunden", Minuten: 90},
  {Value: "2 Stunden", Minuten: 120}
)
```

**Items.Value**
```powerfx
=Value
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Width**
```powerfx
=150
```

**X**
```powerfx
=423
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y + lblRaumBuchenPanel.Height + 50
```

### [C064] Screen1 / conRaumBuchungenPanel / lblRaumBuchenPanel
Name: `lblRaumBuchenPanel` · Typ: `Label@2.5.1` · Eltern: `conRaumBuchungenPanel` · Properties: 9 · Z. 1426

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=17
```

**Text**
```powerfx
="Raum Buchen"
```

**Width**
```powerfx
=180
```

**X**
```powerfx
=100
```

**Y**
```powerfx
=40
```

### [C065] Screen1 / conRaumBuchungenPanel / ddBeginnRaumPanel
Name: `ddBeginnRaumPanel` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conRaumBuchungenPanel` · Properties: 17 · Z. 1438

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Fill**
```powerfx
=RGBA(241, 241, 241, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=ForAll(Sequence(29, 0), {Value: Text(DateAdd(Time(8, 0, 0), Value * 30, TimeUnit.Minutes), "hh:mm")})
```

**Items.Value**
```powerfx
=Value
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Width**
```powerfx
=150
```

**X**
```powerfx
=241
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y + lblRaumBuchenPanel.Height + 50
```

### [C066] Screen1 / conRaumBuchungenPanel / btnAbbrechenRaumPanel
Name: `btnAbbrechenRaumPanel` · Typ: `Classic/Button@2.2.0` · Eltern: `conRaumBuchungenPanel` · Properties: 17 · Z. 1459

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=Color.Black
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=RGBA(241, 241, 241, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varZeigeRaumBuchungForm, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Size**
```powerfx
=25
```

**Text**
```powerfx
="<"
```

**Width**
```powerfx
=40
```

**X**
```powerfx
=45
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y
```

### [C067] Screen1 / conRaumBuchungenPanel / Label6
Name: `Label6` · Typ: `Label@2.5.1` · Eltern: `conRaumBuchungenPanel` · Properties: 5 · Z. 1479

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
="Dauer"
```

**X**
```powerfx
=423
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y + lblRaumBuchenPanel.Height + 13
```

### [C068] Screen1 / conRaumBuchungenPanel / Label7
Name: `Label7` · Typ: `Label@2.5.1` · Eltern: `conRaumBuchungenPanel` · Properties: 5 · Z. 1487

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
="Beginn"
```

**X**
```powerfx
=241
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y + lblRaumBuchenPanel.Height + 13
```

### [C069] Screen1 / conRaumBuchungenPanel / lblDatumBetätigen
Name: `lblDatumBetätigen` · Typ: `Label@2.5.1` · Eltern: `conRaumBuchungenPanel` · Properties: 5 · Z. 1495

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
="Datum"
```

**X**
```powerfx
=60
```

**Y**
```powerfx
=lblRaumBuchenPanel.Y + lblRaumBuchenPanel.Height + 13
```

### [C070] Screen1 / conRaumBuchungenPanel / galRäume
Name: `galRäume` · Typ: `Gallery@2.15.0` · Variante: `BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0` · Eltern: `conRaumBuchungenPanel` · Properties: 6 · Z. 1503

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=316
```

**Items**
```powerfx
=With(
  { basisStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  Filter(
    Räume As R,
    CountRows(
      Filter(
        Table({Offset: 0}, {Offset: 30}, {Offset: 60}, {Offset: 90}) As Slot,
        With(
          { slotStart: DateAdd(basisStart, Slot.Offset, TimeUnit.Minutes) },
          With(
            { slotEnde: DateAdd(slotStart, 30, TimeUnit.Minutes) },
            CountRows(Filter(Raumbuchungen, Raum.Value = R.Titel && Startzeit < slotEnde && Endzeit > slotStart)) = 0
          )
        )
      )
    ) > 0
  )
)
```

**Width**
```powerfx
=575
```

**X**
```powerfx
=20
```

**Y**
```powerfx
=dpDatumRaum.Y + dpDatumRaum.Height + 30
```

### [C071] Screen1 / conRaumBuchungenPanel / galRäume / Rectangle7
Name: `Rectangle7` · Typ: `Rectangle@2.3.0` · Eltern: `galRäume` · Properties: 7 · Z. 1532

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=ColorValue("#F0F0F0")
```

**Height**
```powerfx
=90
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=Parent.Width - 14
```

**X**
```powerfx
=9
```

**Y**
```powerfx
=7
```

### [C072] Screen1 / conRaumBuchungenPanel / galRäume / Label11
Name: `Label11` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 7 · Z. 1542

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=94
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=390
```

**X**
```powerfx
=40
```

**Y**
```powerfx
=10
```

### [C073] Screen1 / conRaumBuchungenPanel / galRäume / Image1
Name: `Image1` · Typ: `Image@2.2.3` · Eltern: `galRäume` · Properties: 11 · Z. 1552

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=72
```

**Image**
```powerfx
=img_meetings_kraeftiger
```

**OnSelect**
```powerfx
=Select(Parent)
```

**RadiusBottomLeft**
```powerfx
=8
```

**RadiusBottomRight**
```powerfx
=8
```

**RadiusTopLeft**
```powerfx
=8
```

**RadiusTopRight**
```powerfx
=8
```

**Width**
```powerfx
=72
```

**X**
```powerfx
=16
```

**Y**
```powerfx
=(Parent.TemplateHeight / 2) - (Self.Height / 2)
```

### [C074] Screen1 / conRaumBuchungenPanel / galRäume / Title1
Name: `Title1` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 16 · Z. 1566

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Color**
```powerfx
=RGBA(50, 49, 48, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=If(ThisItem.IsSelected, FontWeight.Semibold, FontWeight.Normal)
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=0
```

**PaddingLeft**
```powerfx
=12
```

**PaddingRight**
```powerfx
=0
```

**PaddingTop**
```powerfx
=0
```

**Size**
```powerfx
=16
```

**Text**
```powerfx
=ThisItem.Titel
```

**VerticalAlign**
```powerfx
=VerticalAlign.Top
```

**Width**
```powerfx
=Parent.TemplateWidth - 173
```

**X**
```powerfx
=100
```

**Y**
```powerfx
=50
```

### [C075] Screen1 / conRaumBuchungenPanel / galRäume / Subtitle1
Name: `Subtitle1` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 15 · Z. 1585

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=If(ThisItem.IsSelected, FontWeight.Semibold, FontWeight.Normal)
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=0
```

**PaddingLeft**
```powerfx
=12
```

**PaddingRight**
```powerfx
=0
```

**PaddingTop**
```powerfx
=0
```

**Size**
```powerfx
=10
```

**Text**
```powerfx
="Matthäus-Merian-Strasse 6 / Lohfelden  MMS Obergeschoss"
```

**VerticalAlign**
```powerfx
=VerticalAlign.Top
```

**Width**
```powerfx
=Title1.Width
```

**X**
```powerfx
=100
```

**Y**
```powerfx
=15
```

### [C076] Screen1 / conRaumBuchungenPanel / galRäume / lblSlot1Info
Name: `lblSlot1Info` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 8 · Z. 1603

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=9
```

**Text**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        {
          vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes),
          verfuegbareMinuten: DateDiff(slotStart, maxVerfuegbarBis, TimeUnit.Minutes)
        },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          "",
          "Nur " & If(
            verfuegbareMinuten >= 60,
            If(
              Mod(verfuegbareMinuten, 60) = 0,
              Text(verfuegbareMinuten / 60) & " Std.",
              Text(verfuegbareMinuten / 60, "0.#") & " Std."
            ),
            Text(verfuegbareMinuten) & " Min."
          )
        )
      )
    )
  )
)
```

**Visible**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        vollDauerEnde > maxVerfuegbarBis
      )
    )
  )
)
```

**Width**
```powerfx
=100
```

**X**
```powerfx
=btnSlot1.X
```

**Y**
```powerfx
=64
```

### [C077] Screen1 / conRaumBuchungenPanel / galRäume / lblSlot2Info
Name: `lblSlot2Info` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 8 · Z. 1655

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=9
```

**Text**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        {
          vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes),
          verfuegbareMinuten: DateDiff(slotStart, maxVerfuegbarBis, TimeUnit.Minutes)
        },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          "",
          "Nur " & If(
            verfuegbareMinuten >= 60,
            If(
              Mod(verfuegbareMinuten, 60) = 0,
              Text(verfuegbareMinuten / 60) & " Std.",
              Text(verfuegbareMinuten / 60, "0.#") & " Std."
            ),
            Text(verfuegbareMinuten) & " Min."
          )
        )
      )
    )
  )
)
```

**Visible**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        vollDauerEnde > maxVerfuegbarBis
      )
    )
  )
)
```

**Width**
```powerfx
=100
```

**X**
```powerfx
=btnSlot2.X
```

**Y**
```powerfx
=64
```

### [C078] Screen1 / conRaumBuchungenPanel / galRäume / lblSlot3Info
Name: `lblSlot3Info` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 8 · Z. 1707

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=9
```

**Text**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        {
          vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes),
          verfuegbareMinuten: DateDiff(slotStart, maxVerfuegbarBis, TimeUnit.Minutes)
        },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          "",
          "Nur " & If(
            verfuegbareMinuten >= 60,
            If(
              Mod(verfuegbareMinuten, 60) = 0,
              Text(verfuegbareMinuten / 60) & " Std.",
              Text(verfuegbareMinuten / 60, "0.#") & " Std."
            ),
            Text(verfuegbareMinuten) & " Min."
          )
        )
      )
    )
  )
)
```

**Visible**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        vollDauerEnde > maxVerfuegbarBis
      )
    )
  )
)
```

**Width**
```powerfx
=100
```

**X**
```powerfx
=btnSlot3.X
```

**Y**
```powerfx
=64
```

### [C079] Screen1 / conRaumBuchungenPanel / galRäume / lblSlot4Info
Name: `lblSlot4Info` · Typ: `Label@2.5.1` · Eltern: `galRäume` · Properties: 8 · Z. 1759

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=9
```

**Text**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        {
          vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes),
          verfuegbareMinuten: DateDiff(slotStart, maxVerfuegbarBis, TimeUnit.Minutes)
        },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          "",
          "Nur " & If(
            verfuegbareMinuten >= 60,
            If(
              Mod(verfuegbareMinuten, 60) = 0,
              Text(verfuegbareMinuten / 60) & " Std.",
              Text(verfuegbareMinuten / 60, "0.#") & " Std."
            ),
            Text(verfuegbareMinuten) & " Min."
          )
        )
      )
    )
  )
)
```

**Visible**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        vollDauerEnde > maxVerfuegbarBis
      )
    )
  )
)
```

**Width**
```powerfx
=100
```

**X**
```powerfx
=btnSlot4.X
```

**Y**
```powerfx
=64
```

### [C080] Screen1 / conRaumBuchungenPanel / galRäume / NextArrow1
Name: `NextArrow1` · Typ: `Classic/Icon@2.5.0` · Eltern: `galRäume` · Properties: 14 · Z. 1811

**AccessibleLabel**
```powerfx
=Self.Tooltip
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Height**
```powerfx
=50
```

**Icon**
```powerfx
=Icon.ChevronRight
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=16
```

**PaddingLeft**
```powerfx
=16
```

**PaddingRight**
```powerfx
=16
```

**PaddingTop**
```powerfx
=16
```

**Tooltip**
```powerfx
="Elementdetails anzeigen"
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=Parent.TemplateWidth - Self.Width - 12
```

**Y**
```powerfx
=(Parent.TemplateHeight / 2) - (Self.Height / 2)
```

### [C081] Screen1 / conRaumBuchungenPanel / galRäume / Rectangle2
Name: `Rectangle2` · Typ: `Rectangle@2.3.0` · Eltern: `galRäume` · Properties: 6 · Z. 1828

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Height**
```powerfx
=Parent.TemplateHeight
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Visible**
```powerfx
=ThisItem.IsSelected
```

**Width**
```powerfx
=4
```

### [C082] Screen1 / conRaumBuchungenPanel / galRäume / btnSlot1
Name: `btnSlot1` · Typ: `Classic/Button@2.2.0` · Eltern: `galRäume` · Properties: 19 · Z. 1837

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

**DisplayMode**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

**Fill**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { istBesetzt: CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0 },
    With(
      { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
      With(
        { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
        With(
          { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
          If(
            istBesetzt,
            ColorFade(ColorValue("#EB3951"), 85%),
            If(
              vollDauerEnde <= maxVerfuegbarBis,
              ColorFade(ColorValue("#00A96B"), 70%),
              ColorFade(ColorValue("#FFA500"), 70%)
            )
          )
        )
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

**OnSelect**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        {
          vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes),
          slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis)
        },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
=Text(
  dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0),
  "hh:mm"
)
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=200
```

**Y**
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          45,
          35
        )
      )
    )
  )
)
```

### [C083] Screen1 / conRaumBuchungenPanel / galRäume / btnSlot2
Name: `btnSlot2` · Typ: `Classic/Button@2.2.0` · Eltern: `galRäume` · Properties: 18 · Z. 1948

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

**DisplayMode**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

**Fill**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 70%),
          ColorFade(ColorValue("#FFA500"), 70%)
        )
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

**OnSelect**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis) },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
=Text(
  DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes),
  "hh:mm"
)
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=btnSlot1.X + btnSlot1.Width + 10
```

**Y**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          45,
          35
        )
      )
    )
  )
)
```

### [C084] Screen1 / conRaumBuchungenPanel / galRäume / btnSlot3
Name: `btnSlot3` · Typ: `Classic/Button@2.2.0` · Eltern: `galRäume` · Properties: 18 · Z. 2048

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

**DisplayMode**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

**Fill**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 70%),
          ColorFade(ColorValue("#FFA500"), 70%)
        )
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

**OnSelect**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis) },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
=Text(
  DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes),
  "hh:mm"
)
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=btnSlot2.X + btnSlot2.Width + 10
```

**Y**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          45,
          35
        )
      )
    )
  )
)
```

### [C085] Screen1 / conRaumBuchungenPanel / galRäume / btnSlot4
Name: `btnSlot4` · Typ: `Classic/Button@2.2.0` · Eltern: `galRäume` · Properties: 18 · Z. 2148

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

**DisplayMode**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

**Fill**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 70%),
          ColorFade(ColorValue("#FFA500"), 70%)
        )
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

**OnSelect**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis) },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
=Text(
  DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes),
  "hh:mm"
)
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=btnSlot3.X + btnSlot3.Width + 10
```

**Y**
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          45,
          35
        )
      )
    )
  )
)
```

### [C086] Screen1 / conRaumBestätigen
Name: `conRaumBestätigen` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 2248

**Fill**
```powerfx
=ColorValue("#f7f7f7")
```

**Height**
```powerfx
=203
```

**RadiusBottomLeft**
```powerfx
=20
```

**RadiusBottomRight**
```powerfx
=20
```

**RadiusTopLeft**
```powerfx
=20
```

**RadiusTopRight**
```powerfx
=20
```

**Visible**
```powerfx
=varZeigeRaumBestätigung
```

**Width**
```powerfx
=650
```

**X**
```powerfx
=643
```

**Y**
```powerfx
=284
```

### [C087] Screen1 / conRaumBestätigen / Label9
Name: `Label9` · Typ: `Label@2.5.1` · Eltern: `conRaumBestätigen` · Properties: 8 · Z. 2263

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=24
```

**Text**
```powerfx
=If(IsBlank(varAusgewähltRaum), "", varAusgewähltRaum.Titel)
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=205
```

**Y**
```powerfx
=12
```

### [C088] Screen1 / conRaumBestätigen / Label10
Name: `Label10` · Typ: `Label@2.5.1` · Eltern: `conRaumBestätigen` · Properties: 7 · Z. 2274

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=15
```

**Text**
```powerfx
=If(
  IsBlank(varAusgewählteStartzeit),
  "",
  Text(varAusgewählteStartzeit, "hh:mm") & " – " & Text(varAusgewählteEndzeit, "hh:mm")
)
```

**X**
```powerfx
=205
```

**Y**
```powerfx
=52
```

### [C089] Screen1 / conRaumBestätigen / btnSpeichernRaumPanel
Name: `btnSpeichernRaumPanel` · Typ: `Classic/Button@2.2.0` · Eltern: `conRaumBestätigen` · Properties: 15 · Z. 2289

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**OnSelect**
```powerfx
=Patch(Raumbuchungen, Defaults(Raumbuchungen), {
  Raum: {Id: varAusgewähltRaum.ID, Value: varAusgewähltRaum.Titel},
  Startzeit: varAusgewählteStartzeit,
  Endzeit: varAusgewählteEndzeit,
  Person: {
    '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
    Claims: "i:0#.f|membership|" & Lower(User().Email),
    DisplayName: User().FullName,
    Email: User().Email,
    JobTitle: "",
    Department: "",
    Picture: ""
  }
});
Set(varZeigeRaumBestätigung, false);
Set(varZeigeRaumBuchungForm, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="Speichern"
```

**X**
```powerfx
=recZeitleisteBg.X + recZeitleisteBg.Width - btnSpeichernRaumPanel.Width
```

**Y**
```powerfx
=recZeitleisteBg.Y + recZeitleisteBg.Height + 15
```

### [C090] Screen1 / conRaumBestätigen / Button7
Name: `Button7` · Typ: `Classic/Button@2.2.0` · Eltern: `conRaumBestätigen` · Properties: 15 · Z. 2323

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**OnSelect**
```powerfx
=Set(varZeigeRaumBestätigung, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="Abbrechen"
```

**X**
```powerfx
=recZeitleisteBg.X
```

**Y**
```powerfx
=recZeitleisteBg.Y + recZeitleisteBg.Height + 15
```

### [C091] Screen1 / conRaumBestätigen / recZeitleisteBg
Name: `recZeitleisteBg` · Typ: `Rectangle@2.3.0` · Eltern: `conRaumBestätigen` · Properties: 6 · Z. 2341

**BorderColor**
```powerfx
=Color.Black
```

**Fill**
```powerfx
=ColorFade(ColorValue("#00A96B"), 70%)
```

**Height**
```powerfx
=40
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=205
```

**Y**
```powerfx
=92
```

### [C092] Screen1 / conRaumBestätigen / recNeueBuchung
Name: `recNeueBuchung` · Typ: `Rectangle@2.3.0` · Eltern: `conRaumBestätigen` · Properties: 6 · Z. 2350

**BorderColor**
```powerfx
=Color.Black
```

**Fill**
```powerfx
=ColorValue("#eb3951")
```

**Height**
```powerfx
=recZeitleisteBg.Height
```

**Width**
```powerfx
=With(
  { gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes) },
  (DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
)
```

**X**
```powerfx
=With(
  {
    dauerMinuten: DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes),
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes)
  },
  recZeitleisteBg.X + (90 / gesamtFenster) * recZeitleisteBg.Width
)
```

**Y**
```powerfx
=recZeitleisteBg.Y
```

### [C093] Screen1 / conRaumBestätigen / recBuchungDavor1
Name: `recBuchungDavor1` · Typ: `Rectangle@2.3.0` · Eltern: `conRaumBestätigen` · Properties: 7 · Z. 2370

**BorderColor**
```powerfx
=Color.Black
```

**Fill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 40%)
```

**Height**
```powerfx
=recZeitleisteBg.Height
```

**Visible**
```powerfx
=CountRows(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes))) > 0
```

**Width**
```powerfx
=With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes),
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes)
  },
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart), "Startzeit", SortOrder.Descending)) },
    (DateDiff(Max(fensterStart, buchung.Startzeit), buchung.Endzeit, TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
  )
)
```

**X**
```powerfx
=With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes),
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes)
  },
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart), "Startzeit", SortOrder.Descending)) },
    recZeitleisteBg.X + Max(0, DateDiff(fensterStart, buchung.Startzeit, TimeUnit.Minutes)) / gesamtFenster * recZeitleisteBg.Width
  )
)
```

**Y**
```powerfx
=recZeitleisteBg.Y
```

### [C094] Screen1 / conRaumBestätigen / recBuchungDanach1
Name: `recBuchungDanach1` · Typ: `Rectangle@2.3.0` · Eltern: `conRaumBestätigen` · Properties: 7 · Z. 2400

**BorderColor**
```powerfx
=Color.Black
```

**Fill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 40%)
```

**Height**
```powerfx
=recZeitleisteBg.Height
```

**Visible**
```powerfx
=CountRows(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit, 90, TimeUnit.Minutes))) > 0
```

**Width**
```powerfx
=With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes),
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes)
  },
  With(
    { fensterEnde: DateAdd(varAusgewählteEndzeit, 90, TimeUnit.Minutes) },
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde), "Startzeit", SortOrder.Ascending)) },
      (DateDiff(buchung.Startzeit, Min(buchung.Endzeit, fensterEnde), TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
    )
  )
)
```

**X**
```powerfx
=With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes),
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes)
  },
  With(
    { fensterEnde: DateAdd(varAusgewählteEndzeit, 90, TimeUnit.Minutes) },
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde), "Startzeit", SortOrder.Ascending)) },
      recZeitleisteBg.X + (DateDiff(fensterStart, buchung.Startzeit, TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
    )
  )
)
```

**Y**
```powerfx
=recZeitleisteBg.Y
```

### [C095] Screen1 / conRaumBestätigen / Label4
Name: `Label4` · Typ: `Label@2.5.1` · Eltern: `conRaumBestätigen` · Properties: 10 · Z. 2436

**Align**
```powerfx
=Align.Center
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Text**
```powerfx
=With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes),
    fensterEnde: DateAdd(varAusgewählteEndzeit, 90, TimeUnit.Minutes)
  },
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde), "Startzeit", SortOrder.Ascending)) },
    If(
      IsBlank(buchung),
      "",
      If(
        recBuchungDanach1.Width < 40,
        "",
        If(
          recBuchungDanach1.Width < 90,
          Left(First(Split(buchung.Person.DisplayName, " ")).Value, 1) & Left(Last(Split(buchung.Person.DisplayName, " ")).Value, 1),
          buchung.Person.DisplayName
        )
      )
    )
  )
)
```

**Visible**
```powerfx
=recBuchungDanach1.Visible
```

**Width**
```powerfx
=recBuchungDanach1.Width
```

**X**
```powerfx
=recBuchungDanach1.X
```

**Y**
```powerfx
=recBuchungDanach1.Y 
```

### [C096] Screen1 / conRaumBestätigen / Label5
Name: `Label5` · Typ: `Label@2.5.1` · Eltern: `conRaumBestätigen` · Properties: 8 · Z. 2471

**Align**
```powerfx
=Align.Center
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=With(
  { fensterStart: DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes) },
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen, Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart), "Startzeit", SortOrder.Descending)) },
    If(IsBlank(buchung), "", buchung.Person.DisplayName)
  )
)
```

**Visible**
```powerfx
=recBuchungDavor1.Visible
```

**Width**
```powerfx
=recBuchungDavor1.Width
```

**X**
```powerfx
=recBuchungDavor1.X
```

**Y**
```powerfx
=recBuchungDavor1.Y - 6
```

### [C097] Screen1 / conRaumBestätigen / Label13
Name: `Label13` · Typ: `Label@2.5.1` · Eltern: `conRaumBestätigen` · Properties: 11 · Z. 2489

**Align**
```powerfx
=Align.Right
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=23
```

**Size**
```powerfx
=10
```

**Text**
```powerfx
=With(
  { dauerMinuten: DateDiff(varAusgewählteStartzeit, varAusgewählteEndzeit, TimeUnit.Minutes) },
  If(
    dauerMinuten >= 60,
    If(
      Mod(dauerMinuten, 60) = 0,
      Text(dauerMinuten / 60) & " Std.",
      Text(dauerMinuten / 60, "0.#") & " Std."
    ),
    Text(dauerMinuten) & " Min."
  )
)
```

**Width**
```powerfx
=62
```

**X**
```powerfx
=543
```

**Y**
```powerfx
=69
```

### [C098] Screen1 / conRaumBestätigen / Label17
Name: `Label17` · Typ: `Label@2.5.1` · Eltern: `conRaumBestätigen` · Properties: 9 · Z. 2515

**Align**
```powerfx
=Align.Center
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=recNeueBuchung.Height
```

**Text**
```powerfx
="Neu"
```

**Width**
```powerfx
=recNeueBuchung.Width
```

**X**
```powerfx
=recNeueBuchung.X
```

**Y**
```powerfx
=recNeueBuchung.Y
```

### [C099] Screen1 / conRaumBestätigen / Image5
Name: `Image5` · Typ: `Image@2.2.3` · Eltern: `conRaumBestätigen` · Properties: 5 · Z. 2527

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(241, 241, 241, 1)
```

**Height**
```powerfx
=203
```

**Image**
```powerfx
=meeting_icon
```

**Width**
```powerfx
=188
```

### [C100] Screen1 / conBuchungDialog
Name: `conBuchungDialog` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 2535

**Fill**
```powerfx
=Color.White
```

**Height**
```powerfx
=If(varWiederholen, 500, 350)
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeDialog
```

**Width**
```powerfx
=800
```

**X**
```powerfx
=(Parent.Width - Self.Width)/2
```

**Y**
```powerfx
=(Parent.Height - Self.Height)/2
```

### [C101] Screen1 / conBuchungDialog / Rectangle5
Name: `Rectangle5` · Typ: `Rectangle@2.3.0` · Eltern: `conBuchungDialog` · Properties: 5 · Z. 2550

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=1
```

**Width**
```powerfx
=Parent.Width
```

**Y**
```powerfx
=Image2.Height
```

### [C102] Screen1 / conBuchungDialog / Image2
Name: `Image2` · Typ: `Image@2.2.3` · Eltern: `conBuchungDialog` · Properties: 4 · Z. 2558

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=278
```

**Image**
```powerfx
=img_20260916_085456
```

**Width**
```powerfx
=245
```

### [C103] Screen1 / conBuchungDialog / Label3
Name: `Label3` · Typ: `Label@2.5.1` · Eltern: `conBuchungDialog` · Properties: 6 · Z. 2565

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=If(
  IsBlank(varSelectedTisch.Geschoss),
  "",
  If(
    varSelectedTisch.Geschoss.Value = "OG",
    "Matthäus-Merian-Strasse 6 / Lohfelden  MMS Obergeschoss",
    "Matthäus-Merian-Strasse 6 / Lohfelden  MMS Untergeschoss"
  )
)
```

**Width**
```powerfx
=500
```

**X**
```powerfx
=270
```

**Y**
```powerfx
=15
```

### [C104] Screen1 / conBuchungDialog / Label2
Name: `Label2` · Typ: `Label@2.5.1` · Eltern: `conBuchungDialog` · Properties: 9 · Z. 2583

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=50
```

**Size**
```powerfx
=20
```

**Text**
```powerfx
=varSelectedTisch.Titel
```

**Width**
```powerfx
=226
```

**X**
```powerfx
=270
```

**Y**
```powerfx
=50
```

### [C105] Screen1 / conBuchungDialog / Label12
Name: `Label12` · Typ: `Label@2.5.1` · Eltern: `conBuchungDialog` · Properties: 9 · Z. 2595

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=If(
  DateDiff(dpDatum.SelectedDate, dpWiederholenBis.SelectedDate, TimeUnit.Days) > 14,
  ColorValue("#EB3951"),
  RGBA(50, 49, 48, 1)
)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=42
```

**Text**
```powerfx
=If(
  DateDiff(dpDatum.SelectedDate, dpWiederholenBis.SelectedDate, TimeUnit.Days) > 14,
  "*Zu weit gewählt — es werden 2 Wochen gespeichert",
  "*Wiederholung max. 2 Wochen möglich"
)
```

**Width**
```powerfx
=345
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=395
```

### [C106] Screen1 / conBuchungDialog / ddStart
Name: `ddStart` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conBuchungDialog` · Properties: 16 · Z. 2617

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Default**
```powerfx
=If(
  varStartOverride <> "",
  varStartOverride,
  With(
    { minutenJetzt: Hour(Now())*60 + Minute(Now()) },
    With(
      {
        minutenStart:
          If(
            dpDatum.SelectedDate = Today(),
            30 * RoundUp(minutenJetzt / 30, 0),
            8 * 60
          )
      },
      Text(Time(RoundDown(minutenStart / 60, 0), Mod(minutenStart, 60), 0), "hh:mm")
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) },
  With(
    {
      minutenStart:
        If(
          dpDatum.SelectedDate = Today(),
          30 * RoundUp(minutenJetzt / 30, 0),
          8 * 60
        ),
      minutenEnde: 22 * 60
    },
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30, 0) + 1, 0),
      With(
        { m: minutenStart + Value * 30 },
        { Value: Text(Time(RoundDown(m / 60, 0), Mod(m, 60), 0), "hh:mm") }
      )
    )
  )
)
```

**Items.Value**
```powerfx
=Value
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=122
```

### [C107] Screen1 / conBuchungDialog / ddEnde
Name: `ddEnde` · Typ: `Classic/DropDown@2.3.1` · Eltern: `conBuchungDialog` · Properties: 16 · Z. 2675

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**ChevronBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**ChevronFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**ChevronHoverBackground**
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

**ChevronHoverFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**Default**
```powerfx
=If(
  varEndeOverride = "",
  Text(
    DateAdd(
      Time(Value(Left(ddStart.Selected.Value, 2)), Value(Mid(ddStart.Selected.Value, 4, 2)), 0),
      30,
      TimeUnit.Minutes
    ),
    "hh:mm"
  ),
  varEndeOverride
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverFill**
```powerfx
=RGBA(205, 209, 213, 1)
```

**Items**
```powerfx
=With(
  { startMinuten: Value(Left(ddStart.Selected.Value, 2)) * 60 + Value(Mid(ddStart.Selected.Value, 4, 2)) },
  ForAll(
    Sequence(RoundDown((22*60 - startMinuten) / 30, 0), 1),
    With(
      { m: startMinuten + Value * 30 },
      { Value: Text(Time(RoundDown(m / 60, 0), Mod(m, 60), 0), "hh:mm") }
    )
  )
)
```

**Items.Value**
```powerfx
=Value
```

**PressedColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**PressedFill**
```powerfx
=RGBA(32, 54, 71, 1)
```

**SelectionColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**SelectionFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=186
```

### [C108] Screen1 / conBuchungDialog / btnSpeichern
Name: `btnSpeichern` · Typ: `Classic/Button@2.2.0` · Eltern: `conBuchungDialog` · Properties: 15 · Z. 2716

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#00A96B")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
With(
  {
    neuStart: dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value, 2)), Value(Mid(ddStart.Selected.Value, 4, 2)), 0),
    neuEnde: dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value, 2)), Value(Mid(ddEnde.Selected.Value, 4, 2)), 0),
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate, dpWiederholenBis.SelectedDate, dpDatum.SelectedDate),
    bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)
  },
  With(
    { effektivesBis: Min(effektivesBisRoh, dpDatum.SelectedDate + 14) },
    With(
      { anzahlTage: DateDiff(dpDatum.SelectedDate, effektivesBis, TimeUnit.Days) + 1 },
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage, 0), DateAdd(dpDatum.SelectedDate, Value, TimeUnit.Days)) },
        With(
          {
            datumsListe:
              If(
                !varWiederholen,
                [dpDatum.SelectedDate],
                If(
                  varWiederholenModus = "Taeglich",
                  alleDatumsWerte,
                  Filter(
                    alleDatumsWerte,
                    Switch(
                      Weekday(Value, StartOfWeek.Monday),
                      1, varTagMo, 2, varTagDi, 3, varTagMi, 4, varTagDo, 5, varTagFr, 6, varTagSa, 7, varTagSo
                    )
                  )
                )
              )
          },
          If(
            varWiederholen && CountRows(datumsListe) = 0,
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo,
              Notify("Bitte mindestens einen Wochentag auswählen.", NotificationType.Warning),
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen.", NotificationType.Warning)
            ),
            With(
              {
                neueDatensaetze:
                  ForAll(
                    Filter(
                      datumsListe As Eintrag,
                      CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0)))) = 0
                    ) As Frei,
                    {
                      Tisch: {Id: varSelectedTisch.ID, Value: varSelectedTisch.Titel},
                      Startzeit: Frei.Value + Time(Hour(neuStart), Minute(neuStart), 0),
                      Endzeit: Frei.Value + Time(Hour(neuEnde), Minute(neuEnde), 0),
                      Person: {
                        Claims: "i:0#.f|membership|" & Lower(User().Email),
                        Department: "",
                        DisplayName: User().FullName,
                        Email: User().Email,
                        JobTitle: "",
                        Picture: ""
                      }
                    }
                  )
              },
              With(
                {
                  speicherStatus:
                    If(
                      CountRows(neueDatensaetze) = 0,
                      "keine",
                      IfError(
                        Patch(Tischbuchungen, ForAll(neueDatensaetze, Defaults(Tischbuchungen)), neueDatensaetze),
                        "fehler",
                        "ok"
                      )
                    )
                },
                With(
                  { anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze) },
                  If(
                    speicherStatus = "fehler",
                    Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen.", NotificationType.Error),
                    If(
                      effektivesBisRoh > effektivesBis,
                      Notify("Wiederholung wurde auf 2 Wochen begrenzt.", NotificationType.Warning),
                      If(
                        anzahlUebersprungen > 0,
                        Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden.", NotificationType.Warning),
                        Notify("Buchung(en) erfolgreich gespeichert.", NotificationType.Success)
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
);
Refresh(Tischbuchungen);
Set(varZeigeDialog, false);
Set(varWiederholen, false);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Set(varIsLoading, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=ColorValue("#00a96b")
```

**Text**
```powerfx
="Speichern"
```

**X**
```powerfx
=616
```

**Y**
```powerfx
=If(varWiederholen, 445, 293)
```

### [C109] Screen1 / conBuchungDialog / btnAbbrechen
Name: `btnAbbrechen` · Typ: `Classic/Button@2.2.0` · Eltern: `conBuchungDialog` · Properties: 15 · Z. 2846

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, 30%)
```

**OnSelect**
```powerfx
=Set(varZeigeDialog, false);
Set(varWiederholen, false);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Color.Black
```

**Text**
```powerfx
="Abbrechen"
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=If(varWiederholen, 445, 293)
```

### [C110] Screen1 / conBuchungDialog / dpDatum
Name: `dpDatum` · Typ: `Classic/DatePicker@2.6.0` · Eltern: `conBuchungDialog` · Properties: 8 · Z. 2874

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**DefaultDate**
```powerfx
=varAnsichtsDatum
```

**Font**
```powerfx
=Font.'Open Sans'
```

**IconBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**IconFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**OnChange**
```powerfx
=Reset(ddStart);
Reset(ddEnde)
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=60
```

### [C111] Screen1 / conBuchungDialog / chkWiederholen
Name: `chkWiederholen` · Typ: `Classic/CheckBox@2.1.0` · Eltern: `conBuchungDialog` · Properties: 11 · Z. 2887

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckboxBorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckmarkFill**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Default**
```powerfx
=varWiederholen
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**OnCheck**
```powerfx
=Set(varWiederholen, true)
```

**OnUncheck**
```powerfx
=Set(varWiederholen, false)
```

**Text**
```powerfx
="Wiederholen"
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=226
```

### [C112] Screen1 / conBuchungDialog / tglTagMo
Name: `tglTagMo` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conBuchungDialog` · Properties: 10 · Z. 2901

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Default**
```powerfx
=varTagMo
```

**FalseText**
```powerfx
="Mo"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagMo, tglTagMo.Value)
```

**TrueFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**TrueText**
```powerfx
="Mo"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=300
```

**Y**
```powerfx
=290
```

### [C113] Screen1 / conBuchungDialog / tglTagDi
Name: `tglTagDi` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conBuchungDialog` · Properties: 10 · Z. 2914

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Default**
```powerfx
=varTagDi
```

**FalseText**
```powerfx
="Di"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagDi, tglTagDi.Value)
```

**TrueFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**TrueText**
```powerfx
="Di"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=tglTagMo.X + 100
```

**Y**
```powerfx
=tglTagMo.Y
```

### [C114] Screen1 / conBuchungDialog / tglTagMi
Name: `tglTagMi` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conBuchungDialog` · Properties: 10 · Z. 2927

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Default**
```powerfx
=varTagMi
```

**FalseText**
```powerfx
="Mi"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagMi, tglTagMi.Value)
```

**TrueFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**TrueText**
```powerfx
="Mi"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=tglTagDi.X + 100
```

**Y**
```powerfx
=tglTagMo.Y
```

### [C115] Screen1 / conBuchungDialog / tglTagDo
Name: `tglTagDo` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conBuchungDialog` · Properties: 10 · Z. 2940

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Default**
```powerfx
=varTagDo
```

**FalseText**
```powerfx
="Do"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagDo, tglTagDo.Value)
```

**TrueFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**TrueText**
```powerfx
="Do"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=tglTagMi.X + 100
```

**Y**
```powerfx
=tglTagMo.Y
```

### [C116] Screen1 / conBuchungDialog / tglTagFr
Name: `tglTagFr` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conBuchungDialog` · Properties: 10 · Z. 2953

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Default**
```powerfx
=varTagFr
```

**FalseText**
```powerfx
="Fr"
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varTagFr, tglTagFr.Value)
```

**TrueFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**TrueText**
```powerfx
="Fr"
```

**Visible**
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

**X**
```powerfx
=tglTagDo.X + 100
```

**Y**
```powerfx
=tglTagMo.Y
```

### [C117] Screen1 / conBuchungDialog / dpWiederholenBis
Name: `dpWiederholenBis` · Typ: `Classic/DatePicker@2.6.0` · Eltern: `conBuchungDialog` · Properties: 11 · Z. 2966

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**IconBackground**
```powerfx
=RGBA(100, 118, 132, 1)
```

**IconFill**
```powerfx
=RGBA(255, 255, 255, 1)
```

**OnChange**
```powerfx
=Set(varWiederholenBisGewaehlt, true)
```

**OnSelect**
```powerfx
=Set(varWiederholenBis, dpWiederholenBis.SelectedDate)
```

**StartOfWeek**
```powerfx
=StartOfWeek.Monday
```

**StartYear**
```powerfx
=2026
```

**Visible**
```powerfx
=varWiederholen
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=352
```

### [C118] Screen1 / conBuchungDialog / Rectangle6
Name: `Rectangle6` · Typ: `Rectangle@2.3.0` · Eltern: `conBuchungDialog` · Properties: 5 · Z. 2980

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=Parent.Height
```

**Width**
```powerfx
=1
```

**X**
```powerfx
=Image2.Width
```

### [C119] Screen1 / conBuchungDialog / Label15
Name: `Label15` · Typ: `Label@2.5.1` · Eltern: `conBuchungDialog` · Properties: 6 · Z. 2988

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
="Wiederholen bis:"
```

**Visible**
```powerfx
=varWiederholen
```

**X**
```powerfx
=448
```

**Y**
```powerfx
=314
```

### [C120] Screen1 / conCheckinDialog
Name: `conCheckinDialog` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 2997

**Fill**
```powerfx
=Color.White
```

**Height**
```powerfx
=140
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeCheckin
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=conDashboard.X + conDashboard.Width + 10
```

**Y**
```powerfx
=With(
        { _idx: CountRows(Filter(galTischbuchungenHeute.AllItems, ID < varSelectedBuchung.ID)) + 1 },
            conDashboard.Y + galTischbuchungenHeute.Y + (_idx - galTischbuchungenHeute.VisibleIndex) * galTischbuchungenHeute.TemplateHeight + (galTischbuchungenHeute.TemplateHeight - Self.Height) / 2
            )
```

### [C121] Screen1 / conCheckinDialog / Image1_4
Name: `Image1_4` · Typ: `Image@2.2.3` · Eltern: `conCheckinDialog` · Properties: 5 · Z. 3016

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=140
```

**Image**
```powerfx
=img_20260916_085456
```

**Width**
```powerfx
=125
```

**X**
```powerfx
=275
```

### [C122] Screen1 / conCheckinDialog / Rectangle6_1
Name: `Rectangle6_1` · Typ: `Rectangle@2.3.0` · Eltern: `conCheckinDialog` · Properties: 5 · Z. 3024

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=Parent.Height
```

**Width**
```powerfx
=1
```

**X**
```powerfx
=Image1_4.X
```

### [C123] Screen1 / conCheckinDialog / lblTitel
Name: `lblTitel` · Typ: `Label@2.5.1` · Eltern: `conCheckinDialog` · Properties: 7 · Z. 3032

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Text**
```powerfx
="Check-in: " & varSelectedBuchung.Tisch.Value
```

**Width**
```powerfx
=195
```

**X**
```powerfx
=20
```

**Y**
```powerfx
=10
```

### [C124] Screen1 / conCheckinDialog / lblZeit
Name: `lblZeit` · Typ: `Label@2.5.1` · Eltern: `conCheckinDialog` · Properties: 6 · Z. 3043

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=Text(varSelectedBuchung.Startzeit, "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit, "hh:mm")
```

**Width**
```powerfx
=134
```

**X**
```powerfx
=lblTitel.X
```

**Y**
```powerfx
=lblTitel.Y + 30
```

### [C125] Screen1 / conCheckinDialog / btnEinchecken
Name: `btnEinchecken` · Typ: `Classic/Button@2.2.0` · Eltern: `conCheckinDialog` · Properties: 17 · Z. 3052

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=Color.White
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=If(varSelectedBuchung.CheckedIn, ColorValue("#EB3951"), ColorValue("#00a96b"))
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -30%)
```

**OnSelect**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  Set(varSelectedBuchung, Patch(Tischbuchungen, aktuelleBuchung, {CheckedIn: !aktuelleBuchung.CheckedIn}))
);
Set(varZeigeCheckin, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=If(varSelectedBuchung.CheckedIn, ColorValue("#EB3951"), ColorValue("#00a96b"))
```

**PressedFill**
```powerfx
=Self.Color
```

**Size**
```powerfx
=14
```

**Text**
```powerfx
=If(varSelectedBuchung.CheckedIn, "Auschecken", "Einchecken")
```

**Width**
```powerfx
=120
```

**X**
```powerfx
=Image1_4.X*3/4 - Self.Width/2
```

**Y**
```powerfx
=Parent.Height - Self.Height - 10
```

### [C126] Screen1 / conCheckinDialog / btnSchließen2
Name: `btnSchließen2` · Typ: `Classic/Button@2.2.0` · Eltern: `conCheckinDialog` · Properties: 17 · Z. 3077

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, 30%)
```

**OnSelect**
```powerfx
=Set(varZeigeCheckin, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Color.Black
```

**Size**
```powerfx
=14
```

**Text**
```powerfx
="Schließen"
```

**Width**
```powerfx
=120
```

**X**
```powerfx
=Image1_4.X*1/4 - Self.Width/2
```

**Y**
```powerfx
=btnEinchecken.Y
```

### [C127] Screen1 / conDetailsPopup
Name: `conDetailsPopup` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 3097

**Fill**
```powerfx
=Color.White
```

**Height**
```powerfx
=154
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeDetails
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=With({pos: If(varAusgewaehltesStockwerk = "OG", LookUp(colTischPositionen, Tisch = varDetailsTisch.Titel), LookUp(colTischPositionenUG, Tisch = varDetailsTisch.Titel))}, With({tx: conGrundriss.X + imgGrundrissOG.X + pos.X * BasisSkalierung}, If(tx + 28 + 10 + Self.Width <= Parent.Width - 10, tx + 28 + 10, Max(10, tx - Self.Width - 10))))
```

**Y**
```powerfx
=With({pos: If(varAusgewaehltesStockwerk = "OG", LookUp(colTischPositionen, Tisch = varDetailsTisch.Titel), LookUp(colTischPositionenUG, Tisch = varDetailsTisch.Titel))}, With({ty: conGrundriss.Y + imgGrundrissOG.Y + pos.Y * BasisSkalierung}, Max(conHeader.Y + conHeader.Height + 10, Min(ty + 23 - Self.Height / 2, Parent.Height - Self.Height - 10))))
```

### [C128] Screen1 / conDetailsPopup / Image7
Name: `Image7` · Typ: `Image@2.2.3` · Eltern: `conDetailsPopup` · Properties: 5 · Z. 3114

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=154
```

**Image**
```powerfx
=img_20260916_085456
```

**Width**
```powerfx
=144
```

**X**
```powerfx
=256
```

### [C129] Screen1 / conDetailsPopup / Rectangle6_2
Name: `Rectangle6_2` · Typ: `Rectangle@2.3.0` · Eltern: `conDetailsPopup` · Properties: 5 · Z. 3122

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=Parent.Height
```

**Width**
```powerfx
=1
```

**X**
```powerfx
=Image7.X
```

### [C130] Screen1 / conDetailsPopup / lblTitel2
Name: `lblTitel2` · Typ: `Label@2.5.1` · Eltern: `conDetailsPopup` · Properties: 8 · Z. 3130

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=35
```

**Text**
```powerfx
="Tisch: " & varSelectedBuchung.Tisch.Value
```

**Width**
```powerfx
=180
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=10
```

### [C131] Screen1 / conDetailsPopup / lblZeit2
Name: `lblZeit2` · Typ: `Label@2.5.1` · Eltern: `conDetailsPopup` · Properties: 5 · Z. 3142

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=Text(varSelectedBuchung.Startzeit, "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit, "hh:mm")
```

**X**
```powerfx
=lblTitel2.X
```

**Y**
```powerfx
=100
```

### [C132] Screen1 / conDetailsPopup / lblPerson
Name: `lblPerson` · Typ: `Label@2.5.1` · Eltern: `conDetailsPopup` · Properties: 5 · Z. 3150

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=varSelectedBuchung.Person.DisplayName
```

**X**
```powerfx
=lblTitel2.X
```

**Y**
```powerfx
=lblStatus.Y + lblStatus.Height
```

### [C133] Screen1 / conDetailsPopup / lblStatus
Name: `lblStatus` · Typ: `Label@2.5.1` · Eltern: `conDetailsPopup` · Properties: 8 · Z. 3158

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=ColorValue("#EB3951")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=26
```

**Text**
```powerfx
="Besetzt"
```

**X**
```powerfx
=lblTitel2.X
```

**Y**
```powerfx
=lblTitel2.Y + lblTitel2.Height
```

### [C134] Screen1 / conDetailsPopup / btnSchließen3
Name: `btnSchließen3` · Typ: `Classic/Button@2.2.0` · Eltern: `conDetailsPopup` · Properties: 22 · Z. 3169

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=20
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, 30%)
```

**OnSelect**
```powerfx
=Set(varZeigeDetails, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Color.Black
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Size**
```powerfx
=10
```

**Text**
```powerfx
="x"
```

**Width**
```powerfx
=20
```

**X**
```powerfx
=378
```

**Y**
```powerfx
=2
```

### [C135] Screen1 / conVerwaltenDialog
Name: `conVerwaltenDialog` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 3194

**Fill**
```powerfx
=Color.White
```

**Height**
```powerfx
=154
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeVerwalten
```

**Width**
```powerfx
=450
```

**X**
```powerfx
=490
```

**Y**
```powerfx
=140
```

### [C136] Screen1 / conVerwaltenDialog / lblTitel3
Name: `lblTitel3` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenDialog` · Properties: 6 · Z. 3209

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Text**
```powerfx
=If(IsBlank(varSelectedBuchung), "", "Tisch " & varSelectedBuchung.Tisch.Value)
```

**X**
```powerfx
=10
```

**Y**
```powerfx
=10
```

### [C137] Screen1 / conVerwaltenDialog / lblZeit3
Name: `lblZeit3` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenDialog` · Properties: 5 · Z. 3218

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=If(IsBlank(varSelectedBuchung), "", Text(varSelectedBuchung.Startzeit, "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit, "hh:mm"))
```

**X**
```powerfx
=12
```

**Y**
```powerfx
=50
```

### [C138] Screen1 / conVerwaltenDialog / btnStornieren
Name: `btnStornieren` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog` · Properties: 16 · Z. 3226

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=Remove(Tischbuchungen, varSelectedBuchung); Set(varZeigeVerwalten, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Stornieren"
```

**Width**
```powerfx
=btnSchließen4.Width
```

**X**
```powerfx
=btnSchließen4.X + btnSchließen4.Width +10
```

**Y**
```powerfx
=100
```

### [C139] Screen1 / conVerwaltenDialog / btnVerlängern
Name: `btnVerlängern` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog` · Properties: 16 · Z. 3245

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  If(
    IsBlank(varAusgewaehltePlusDauer),
    Notify("Bitte eine Dauer auswählen.", NotificationType.Warning),
    Set(varSelectedBuchung, Patch(Tischbuchungen, aktuelleBuchung, {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit, varAusgewaehltePlusDauer, TimeUnit.Minutes)
    }));
    Set(varZeigeVerwalten, false);
    Set(varAusgewaehltePlusDauer, Blank())
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Verlängern"
```

**Width**
```powerfx
=btnStornieren.Width
```

**X**
```powerfx
=btnStornieren.X + btnStornieren.Width + 10
```

**Y**
```powerfx
=100
```

### [C140] Screen1 / conVerwaltenDialog / btnSchließen4
Name: `btnSchließen4` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog` · Properties: 16 · Z. 3276

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, 30%)
```

**OnSelect**
```powerfx
=Set(varZeigeVerwalten, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Color.Black
```

**PressedFill**
```powerfx
=Color.Black
```

**Text**
```powerfx
="Schließen"
```

**Width**
```powerfx
=(Parent.Width - 4 * 10) / 3
```

**X**
```powerfx
=10
```

**Y**
```powerfx
=100
```

### [C141] Screen1 / conVerwaltenDialog / btnPlus1Std
Name: `btnPlus1Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog` · Properties: 18 · Z. 3295

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 60,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 60, Blank(), 60))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="+1Std"
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=175
```

**Y**
```powerfx
=35
```

### [C142] Screen1 / conVerwaltenDialog / btnPlus2Std
Name: `btnPlus2Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog` · Properties: 18 · Z. 3344

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 120,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 120, Blank(), 120))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="+2Std"
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=btnPlus1Std.X + btnPlus1Std.Width + 10 
```

**Y**
```powerfx
=btnPlus1Std.Y
```

### [C143] Screen1 / conVerwaltenDialog / btnPlus3Std
Name: `btnPlus3Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog` · Properties: 18 · Z. 3393

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes),
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 180,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 180, Blank(), 180))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="+3Std"
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=btnPlus2Std.X + btnPlus1Std.Width + 10 
```

**Y**
```powerfx
=btnPlus1Std.Y
```

### [C144] Screen1 / conBuchungen
Name: `conBuchungen` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 10 · Z. 3443

**Fill**
```powerfx
=ColorValue("#f7f7f7")
```

**Height**
```powerfx
=Parent.Height - conHeader.Height - 15
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varAktiverTab = "buchungen"
```

**Width**
```powerfx
=Parent.Width - 10
```

**X**
```powerfx
=5
```

**Y**
```powerfx
=conHeader.Height + 10
```

### [C145] Screen1 / conBuchungen / galAlleTischbuchungen
Name: `galAlleTischbuchungen` · Typ: `Gallery@2.15.0` · Variante: `BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0` · Eltern: `conBuchungen` · Properties: 7 · Z. 3458

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=546
```

**Items**
```powerfx
=With(
  { erzwingeNeuaufbau: varGalleryNeuAufbauen },
  SortByColumns(
    Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()),
    "Startzeit",
    SortOrder.Ascending
  )
)
```

**Visible**
```powerfx
=galAlleTischbuchungen.AllItemsCount > 0
```

**Width**
```powerfx
=Max(350, Min(600, Parent.Width - (galAlleTischbuchungen.X + 40 + 550 + 80)))
```

**X**
```powerfx
=80
```

**Y**
```powerfx
=80
```

### [C146] Screen1 / conBuchungen / galAlleTischbuchungen / Rectangle4_2
Name: `Rectangle4_2` · Typ: `Rectangle@2.3.0` · Eltern: `galAlleTischbuchungen` · Properties: 7 · Z. 3478

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(234, 234, 236, 1)
```

**Height**
```powerfx
=Parent.TemplateHeight - 20
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=Parent.TemplateWidth - 30
```

**X**
```powerfx
=15
```

**Y**
```powerfx
=10
```

### [C147] Screen1 / conBuchungen / galAlleTischbuchungen / Image1_3
Name: `Image1_3` · Typ: `Image@2.2.3` · Eltern: `galAlleTischbuchungen` · Properties: 7 · Z. 3488

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=72
```

**Image**
```powerfx
=img_20260916_085456
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=72
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=(Parent.TemplateHeight / 2) - (Self.Height / 2)
```

### [C148] Screen1 / conBuchungen / galAlleTischbuchungen / Image3_2
Name: `Image3_2` · Typ: `Image@2.2.3` · Eltern: `galAlleTischbuchungen` · Properties: 8 · Z. 3498

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=50
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**Image**
```powerfx
=img_bearbeiten_heller
```

**OnSelect**
```powerfx
=Select(Parent)
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=galAlleTischbuchungen.Width - Self.Width - 25
```

**Y**
```powerfx
=23
```

### [C149] Screen1 / conBuchungen / galAlleTischbuchungen / lblTischName
Name: `lblTischName` · Typ: `Label@2.5.1` · Eltern: `galAlleTischbuchungen` · Properties: 16 · Z. 3509

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Color**
```powerfx
=RGBA(50, 49, 48, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=If(ThisItem.IsSelected, FontWeight.Semibold, FontWeight.Normal)
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=0
```

**PaddingLeft**
```powerfx
=12
```

**PaddingRight**
```powerfx
=0
```

**PaddingTop**
```powerfx
=0
```

**Size**
```powerfx
=14
```

**Text**
```powerfx
=ThisItem.Tisch.Value
```

**VerticalAlign**
```powerfx
=VerticalAlign.Top
```

**Width**
```powerfx
=Parent.TemplateWidth - 173
```

**X**
```powerfx
=100
```

**Y**
```powerfx
=27
```

### [C150] Screen1 / conBuchungen / galAlleTischbuchungen / lblRaumZeit
Name: `lblRaumZeit` · Typ: `Label@2.5.1` · Eltern: `galAlleTischbuchungen` · Properties: 15 · Z. 3528

**BorderColor**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=If(ThisItem.IsSelected, FontWeight.Semibold, FontWeight.Normal)
```

**Height**
```powerfx
=Self.Size * 1.8
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PaddingBottom**
```powerfx
=0
```

**PaddingLeft**
```powerfx
=12
```

**PaddingRight**
```powerfx
=0
```

**PaddingTop**
```powerfx
=0
```

**Size**
```powerfx
=12
```

**Text**
```powerfx
=Text(ThisItem.Startzeit, "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit, "hh:mm") & " – " & Text(ThisItem.Endzeit, "hh:mm")
```

**VerticalAlign**
```powerfx
=VerticalAlign.Top
```

**Width**
```powerfx
=lblTischName.Width
```

**X**
```powerfx
=lblTischName.X
```

**Y**
```powerfx
=lblTischName.Y + lblTischName.Height
```

### [C151] Screen1 / conBuchungen / galAlleTischbuchungen / Rectangle3_2
Name: `Rectangle3_2` · Typ: `Rectangle@2.3.0` · Eltern: `galAlleTischbuchungen` · Properties: 7 · Z. 3546

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Fill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**Height**
```powerfx
=Parent.TemplateHeight
```

**OnSelect**
```powerfx
=Select(Parent)
```

**PressedFill**
```powerfx
=Color.Transparent
```

**Visible**
```powerfx
=ThisItem.IsSelected
```

**Width**
```powerfx
=4
```

### [C152] Screen1 / conBuchungen / galAlleTischbuchungen / btnVerwalten_2
Name: `btnVerwalten_2` · Typ: `Classic/Button@2.2.0` · Eltern: `galAlleTischbuchungen` · Properties: 17 · Z. 3556

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=50
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.2)
```

**OnSelect**
```powerfx
=If(
  varAuswahlModusAktiv,
  Set(varGeklickteBuchungKlein, ThisItem);
  Set(varZeigeVerwaltenKlein, true),
  Set(varSelectedBuchungTab, ThisItem);
  Set(varZeigeVerwaltenTab, true);
  Set(varZeigeCheckin, false);
  Set(varZeigeDetails, false);
  Set(varZeigeDialog, false)
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=50
```

**X**
```powerfx
=Image3_2.X
```

**Y**
```powerfx
=Image3_2.Y
```

### [C153] Screen1 / conBuchungen / galAlleTischbuchungen / chkAuswahl
Name: `chkAuswahl` · Typ: `Classic/CheckBox@2.1.0` · Eltern: `galAlleTischbuchungen` · Properties: 14 · Z. 3586

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckboxBorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckmarkFill**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Default**
```powerfx
=!IsBlank(LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=40
```

**HoverColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**OnCheck**
```powerfx
=Collect(colAusgewaehlteBuchungen, ThisItem)
```

**OnUncheck**
```powerfx
=Remove(colAusgewaehlteBuchungen, LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
```

**Text**
```powerfx
=
```

**Visible**
```powerfx
=varAuswahlModusAktiv
```

**Width**
```powerfx
=40
```

**X**
```powerfx
=btnVerwalten_2.X - btnVerwalten.Width - 10
```

**Y**
```powerfx
=btnVerwalten_2.Y +btnVerwalten_2.Height/2 -chkAuswahl.Height/2 
```

### [C154] Screen1 / conBuchungen / lblÜberschriftBuchungen
Name: `lblÜberschriftBuchungen` · Typ: `Label@2.5.1` · Eltern: `conBuchungen` · Properties: 9 · Z. 3603

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Height**
```powerfx
=60
```

**Size**
```powerfx
=20
```

**Text**
```powerfx
="Tischbuchungen"
```

**Width**
```powerfx
=300
```

**X**
```powerfx
=galAlleTischbuchungen.X
```

**Y**
```powerfx
=galAlleTischbuchungen.Y - lblÜberschriftBuchungen.Height 
```

### [C155] Screen1 / conBuchungen / conVerwaltenDialog_1
Name: `conVerwaltenDialog_1` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `conBuchungen` · Properties: 10 · Z. 3615

**Fill**
```powerfx
=RGBA(234, 234, 236, 1)
```

**Height**
```powerfx
=251
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeVerwaltenTab
```

**Width**
```powerfx
=Min(550, Parent.Width - (galAlleTischbuchungen.X + galAlleTischbuchungen.Width + 40) - 80)
```

**X**
```powerfx
=galAlleTischbuchungen.X + galAlleTischbuchungen.Width + 40
```

**Y**
```powerfx
=galAlleTischbuchungen.Y
```

### [C156] Screen1 / conBuchungen / conVerwaltenDialog_1 / lblTitel3_1
Name: `lblTitel3_1` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenDialog_1` · Properties: 8 · Z. 3630

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=18
```

**Text**
```powerfx
="Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=12
```

**Y**
```powerfx
=10
```

### [C157] Screen1 / conBuchungen / conVerwaltenDialog_1 / lblZeit3_1
Name: `lblZeit3_1` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenDialog_1` · Properties: 7 · Z. 3642

**Align**
```powerfx
=Align.Right
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=15
```

**Text**
```powerfx
=If(IsBlank(varSelectedBuchungTab), "", Text(varSelectedBuchungTab.Startzeit, "hh:mm") & " – " & Text(varSelectedBuchungTab.Endzeit, "hh:mm"))
```

**X**
```powerfx
=374
```

**Y**
```powerfx
=lblTitel3_1.Y + lblTitel3_1.Height + 10
```

### [C158] Screen1 / conBuchungen / conVerwaltenDialog_1 / lblVerwaltenTag
Name: `lblVerwaltenTag` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenDialog_1` · Properties: 7 · Z. 3652

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Size**
```powerfx
=15
```

**Text**
```powerfx
=Text(varSelectedBuchungTab.Startzeit, "dddd, dd.mm.yyyy")
```

**Width**
```powerfx
=250
```

**X**
```powerfx
=btnSchließen4_1.X
```

**Y**
```powerfx
=lblZeit3_1.Y
```

### [C159] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnStornieren_1
Name: `btnStornieren_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 16 · Z. 3662

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
If(
  IsBlank(varSelectedBuchungTab),
  Notify("Keine Buchung ausgewählt.", NotificationType.Warning),
  Remove(Tischbuchungen, varSelectedBuchungTab);
  Refresh(Tischbuchungen);
  Notify("Buchung storniert.", NotificationType.Success)
);
Set(varZeigeVerwaltenTab, false);
Set(varIsLoading, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Stornieren"
```

**Width**
```powerfx
=btnSchließen4_1.Width
```

**X**
```powerfx
=(conVerwaltenDialog_1.Width / 3) * 1.5 - (btnStornieren_1.Width / 2)
```

**Y**
```powerfx
=btnSchließen4_1.Y
```

### [C160] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnVerlängern_1
Name: `btnVerlängern_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 16 · Z. 3691

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchungTab.ID) },
  If(
    IsBlank(varAusgewaehltePlusDauer),
    Notify("Bitte eine Dauer auswählen.", NotificationType.Warning),
    Set(varSelectedBuchungTab, Patch(Tischbuchungen, aktuelleBuchung, {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit, varAusgewaehltePlusDauer, TimeUnit.Minutes)
    }));
    Refresh(Tischbuchungen);
    Set(varZeigeVerwaltenTab, false);
    Set(varAusgewaehltePlusDauer, Blank());
    Clear(colAusgewaehlteBuchungen);
    Set(varMehrfachAuswahlModus, false)
  )
)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Speichern"
```

**Width**
```powerfx
=btnStornieren_1.Width
```

**X**
```powerfx
=(conVerwaltenDialog_1.Width / 3) * 2.5 - (btnVerlängern_1.Width / 2)
```

**Y**
```powerfx
=btnSchließen4_1.Y
```

### [C161] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnSchließen4_1
Name: `btnSchließen4_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 16 · Z. 3725

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, 30%)
```

**OnSelect**
```powerfx
=Set(varZeigeVerwaltenTab, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Color.Black
```

**PressedFill**
```powerfx
=Color.Black
```

**Text**
```powerfx
="Schließen"
```

**Width**
```powerfx
=(Parent.Width) / 3 - 30
```

**X**
```powerfx
=(conVerwaltenDialog_1.Width / 3) * 0.5 - (btnSchließen4_1.Width / 2)
```

**Y**
```powerfx
=btnMinus3std.Y + btnMinus3std.Height + 15
```

### [C162] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnPlus1Std_1
Name: `btnPlus1Std_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 18 · Z. 3744

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 60,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 60, Blank(), 60))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="+1Std"
```

**Width**
```powerfx
=btnBreite
```

**X**
```powerfx
=btnMinus1Std.X + btnBreite + btnAbstand
```

**Y**
```powerfx
=btnMinus3std.Y
```

### [C163] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnPlus2Std_1
Name: `btnPlus2Std_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 18 · Z. 3793

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 120,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 120, Blank(), 120))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="+2Std"
```

**Width**
```powerfx
=btnBreite
```

**X**
```powerfx
=btnPlus1Std_1.X + btnBreite + btnAbstand
```

**Y**
```powerfx
=btnMinus3std.Y
```

### [C164] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnPlus3Std_1
Name: `btnPlus3Std_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 18 · Z. 3842

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes), tischWert: aktuelleBuchung.Tisch.Value, endeAlt: aktuelleBuchung.Endzeit },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With({ aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) }, With({ tischWert: aktuelleBuchung.Tisch.Value, endeAlt: aktuelleBuchung.Endzeit, neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) }, With({ direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0 }, If(varAusgewaehltePlusDauer = 180, ColorValue("#00A96B"), If(direktBesetzt, ColorFade(ColorValue("#EB3951"), 70%), ColorFade(ColorValue("#00A96B"), 70%))))))
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 180, Blank(), 180))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="+3Std"
```

**Width**
```powerfx
=btnBreite
```

**X**
```powerfx
=btnPlus2Std_1.X + btnBreite + btnAbstand
```

**Y**
```powerfx
=btnMinus3std.Y
```

### [C165] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnMinus1Std
Name: `btnMinus1Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 18 · Z. 3875

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -60, TimeUnit.Minutes) },
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -60, TimeUnit.Minutes),
      zuKurz: DateAdd(aktuelleBuchung.Endzeit, -60, TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    },
    If(
      varAusgewaehltePlusDauer = -60,
      ColorValue("#00A96B"),
      If(
        zuKurz,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = -60, Blank(), -60))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="-1Std"
```

**Width**
```powerfx
=btnBreite
```

**X**
```powerfx
=btnMinus2Std.X + btnBreite + btnAbstand
```

**Y**
```powerfx
=btnMinus3std.Y
```

### [C166] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnMinus2Std
Name: `btnMinus2Std` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 18 · Z. 3925

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -120, TimeUnit.Minutes) },
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -120, TimeUnit.Minutes),
      zuKurz: DateAdd(aktuelleBuchung.Endzeit, -120, TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    },
    If(
      varAusgewaehltePlusDauer = -120,
      ColorValue("#00A96B"),
      If(
        zuKurz,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = -120, Blank(), -120))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="-2std"
```

**Width**
```powerfx
=btnBreite
```

**X**
```powerfx
=btnMinus3std.X + btnBreite + btnAbstand
```

**Y**
```powerfx
=btnMinus3std.Y
```

### [C167] Screen1 / conBuchungen / conVerwaltenDialog_1 / btnMinus3std
Name: `btnMinus3std` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenDialog_1` · Properties: 18 · Z. 3975

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**DisabledFill**
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

**DisplayMode**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -180, TimeUnit.Minutes) },
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

**Fill**
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -180, TimeUnit.Minutes),
      zuKurz: DateAdd(aktuelleBuchung.Endzeit, -180, TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    },
    If(
      varAusgewaehltePlusDauer = -180,
      ColorValue("#00A96B"),
      If(
        zuKurz,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**OnSelect**
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = -180, Blank(), -180))
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=Self.Color
```

**Text**
```powerfx
="-3Std"
```

**Width**
```powerfx
=btnBreite
```

**X**
```powerfx
=20
```

**Y**
```powerfx
=lblZeit3_1.Y + lblZeit3_1.Height + 15 
```

### [C168] Screen1 / conBuchungen / conVerwaltenKlein
Name: `conVerwaltenKlein` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `conBuchungen` · Properties: 10 · Z. 4025

**Fill**
```powerfx
=RGBA(234, 234, 236, 1)
```

**Height**
```powerfx
=150
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Visible**
```powerfx
=varZeigeVerwaltenKlein
```

**Width**
```powerfx
=400
```

**X**
```powerfx
=conVerwaltenDialog_1.X
```

**Y**
```powerfx
=conVerwaltenDialog_1.Y
```

### [C169] Screen1 / conBuchungen / conVerwaltenKlein / lblVerwaltenKleinDatum
Name: `lblVerwaltenKleinDatum` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenKlein` · Properties: 6 · Z. 4040

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=Text(varGeklickteBuchungKlein.Startzeit, "dddd, dd.mm.yyyy")
```

**Width**
```powerfx
=200
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=50
```

### [C170] Screen1 / conBuchungen / conVerwaltenKlein / lblVerwaltenKleinZeit
Name: `lblVerwaltenKleinZeit` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenKlein` · Properties: 6 · Z. 4049

**Align**
```powerfx
=Align.Right
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
=Text(varGeklickteBuchungKlein.Startzeit, "hh:mm") & " – " & Text(varGeklickteBuchungKlein.Endzeit, "hh:mm")
```

**X**
```powerfx
=Parent.Width - lblVerwaltenKleinZeit.Width - 25
```

**Y**
```powerfx
=60
```

### [C171] Screen1 / conBuchungen / conVerwaltenKlein / lblVerwaltenKleinTitel
Name: `lblVerwaltenKleinTitel` · Typ: `Label@2.5.1` · Eltern: `conVerwaltenKlein` · Properties: 8 · Z. 4058

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=17
```

**Text**
```powerfx
=varGeklickteBuchungKlein.Tisch.Value &
If(
  CountRows(colAusgewaehlteBuchungen) > 1,
  " +" & (CountRows(colAusgewaehlteBuchungen) - 1) & " weitere",
  ""
)
```

**Width**
```powerfx
=350
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=15
```

### [C172] Screen1 / conBuchungen / conVerwaltenKlein / btnStornierenKlein
Name: `btnStornierenKlein` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenKlein` · Properties: 16 · Z. 4075

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
ClearCollect(
    colStornoFrisch,
    Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now())
);
ClearCollect(
    colStornoZiele,
    Filter(colStornoFrisch As F, !IsBlank(LookUp(colAusgewaehlteBuchungen As A, A.ID = F.ID)))
);
If(
    CountRows(colAusgewaehlteBuchungen) = 0,
    Notify("Keine Buchungen ausgewählt.", NotificationType.Warning),
    If(
        CountRows(colStornoZiele) = 0,
        Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert.", NotificationType.Warning),
        IfError(
            Remove(Tischbuchungen, colStornoZiele),
            Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen.", NotificationType.Error),
            If(
                CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen),
                Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert.", NotificationType.Warning),
                Notify(CountRows(colStornoZiele) & " Buchungen storniert.", NotificationType.Success)
            )
        )
    )
);
Refresh(Tischbuchungen);
Clear(colStornoFrisch);
Clear(colStornoZiele);
Clear(colAusgewaehlteBuchungen);
Set(varGeklickteBuchungKlein, Blank());
Set(varZeigeVerwaltenKlein, false);
Set(varAuswahlModusAktiv, false);
Reset(tglAuswahlModus);
Set(varIsLoading, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Stornieren"
```

**Width**
```powerfx
=Parent.Width / 2 - 30
```

**X**
```powerfx
=Parent.Width - Self.Width - 25
```

**Y**
```powerfx
=95
```

### [C173] Screen1 / conBuchungen / conVerwaltenKlein / btnSchließenKlein
Name: `btnSchließenKlein` · Typ: `Classic/Button@2.2.0` · Eltern: `conVerwaltenKlein` · Properties: 16 · Z. 4129

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Black
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, 30%)
```

**OnSelect**
```powerfx
=Set(varZeigeVerwaltenKlein, false);
Set(varGeklickteBuchungKlein, Blank());
Clear(colAusgewaehlteBuchungen);
Clear(colStornoFrisch);
Clear(colStornoZiele);
Set(varAuswahlModusAktiv, false);
Reset(tglAuswahlModus)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Color.Black
```

**PressedFill**
```powerfx
=Color.Black
```

**Text**
```powerfx
="Schließen"
```

**Width**
```powerfx
=btnStornierenKlein.Width
```

**X**
```powerfx
=25
```

**Y**
```powerfx
=95
```

### [C174] Screen1 / conBuchungen / lblTischLeer_1
Name: `lblTischLeer_1` · Typ: `Label@2.5.1` · Eltern: `conBuchungen` · Properties: 6 · Z. 4155

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Text**
```powerfx
="-Keine Einträge-"
```

**Visible**
```powerfx
=galTischbuchungenHeute.AllItemsCount = 0
```

**X**
```powerfx
=95
```

**Y**
```powerfx
=70
```

### [C175] Screen1 / conBuchungen / tglAuswahlModus
Name: `tglAuswahlModus` · Typ: `Classic/Toggle@2.1.0` · Eltern: `conBuchungen` · Properties: 7 · Z. 4164

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**DisplayMode**
```powerfx
=If(galAlleTischbuchungen.AllItemsCount <= 1, DisplayMode.Disabled, DisplayMode.Edit)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**OnChange**
```powerfx
=Set(varAuswahlModusAktiv, tglAuswahlModus.Value);
If(
  !tglAuswahlModus.Value,
  Clear(colAusgewaehlteBuchungen);
  Set(varZeigeVerwaltenKlein, false);
  Set(varGeklickteBuchungKlein, Blank())
);
Set(varGalleryNeuAufbauen, varGalleryNeuAufbauen + 1);
If(
  tglAuswahlModus.Value,
  Set(varZeigeVerwaltenTab, false)
)
```

**TrueFill**
```powerfx
=RGBA(100, 118, 132, 1)
```

**X**
```powerfx
=galAlleTischbuchungen.X + galAlleTischbuchungen.Width - Self.Width
```

**Y**
```powerfx
=52
```

### [C176] Screen1 / conBuchungen / chkAlleAuswählen
Name: `chkAlleAuswählen` · Typ: `Classic/CheckBox@2.1.0` · Eltern: `conBuchungen` · Properties: 13 · Z. 4186

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckboxBorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**CheckmarkFill**
```powerfx
=RGBA(0, 0, 0, 1)
```

**Default**
```powerfx
=CountRows(colAusgewaehlteBuchungen) > 0 && CountRows(colAusgewaehlteBuchungen) = galAlleTischbuchungen.AllItemsCount
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**OnCheck**
```powerfx
=ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)
```

**OnUncheck**
```powerfx
=Clear(colAusgewaehlteBuchungen)
```

**Text**
```powerfx
=
```

**Visible**
```powerfx
=varAuswahlModusAktiv
```

**Width**
```powerfx
=40
```

**X**
```powerfx
=tglAuswahlModus.X - Self.Width - 3
```

**Y**
```powerfx
=41
```

### [C177] Screen1 / conBuchungen / Icon1
Name: `Icon1` · Typ: `Classic/Icon@2.5.0` · Eltern: `conBuchungen` · Properties: 8 · Z. 4202

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=30
```

**Icon**
```powerfx
=Icon.Sync
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Width**
```powerfx
=30
```

**X**
```powerfx
=40
```

**Y**
```powerfx
=35
```

### [C178] Screen1 / conHeader
Name: `conHeader` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 9 · Z. 4217

**Fill**
```powerfx
=ColorValue("#f7f7f7")
```

**Height**
```powerfx
=70
```

**RadiusBottomLeft**
```powerfx
=16
```

**RadiusBottomRight**
```powerfx
=16
```

**RadiusTopLeft**
```powerfx
=16
```

**RadiusTopRight**
```powerfx
=16
```

**Width**
```powerfx
=Parent.Width - 10
```

**X**
```powerfx
=5
```

**Y**
```powerfx
=5
```

### [C179] Screen1 / conHeader / Image6
Name: `Image6` · Typ: `Image@2.2.3` · Eltern: `conHeader` · Properties: 7 · Z. 4231

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Height**
```powerfx
=53
```

**Image**
```powerfx
='Technoform_Logo-Frame_Blue-Green_sRGB'
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Width**
```powerfx
=155
```

**X**
```powerfx
=(conDashboard.Width - 3*140) / 4 - 5
```

**Y**
```powerfx
=Parent.Height/2 - Self.Height/2
```

### [C180] Screen1 / conHeader / btnTabDashboard
Name: `btnTabDashboard` · Typ: `Classic/Button@2.2.0` · Eltern: `conHeader` · Properties: 16 · Z. 4245

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=Set(varAktiverTab, "dashboard")
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Dashboard"
```

**Width**
```powerfx
=140
```

**X**
```powerfx
=Image6.X + 140 + (conDashboard.Width - 3*140) / 4 + 13
```

**Y**
```powerfx
=Parent.Height/2 - Self.Height/2
```

### [C181] Screen1 / conHeader / btnTabBuchungen
Name: `btnTabBuchungen` · Typ: `Classic/Button@2.2.0` · Eltern: `conHeader` · Properties: 16 · Z. 4264

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=ColorValue("#171496")
```

**Font**
```powerfx
=Font.'Open Sans'
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=ColorFade(Self.Fill, -20%)
```

**OnSelect**
```powerfx
=Set(varAktiverTab, "buchungen");
Set(varZeigeRaumVerwalten, false);
Set(varZeigeVerwalten, false);
Set(varZeigeDialog, false);
Set(varZeigeDetails, false);
Set(varZeigeCheckin, false);
Set(varZeigeVerlaengern, false)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=
```

**Text**
```powerfx
="Buchungen"
```

**Width**
```powerfx
=140
```

**X**
```powerfx
=btnTabDashboard.X + btnTabBuchungen.Width + ((conDashboard.Width - 3*140) / 4)
```

**Y**
```powerfx
=Parent.Height/2 - Self.Height/2
```

### [C182] Screen1 / conHeader / Circle2
Name: `Circle2` · Typ: `Circle@2.3.0` · Eltern: `conHeader` · Properties: 7 · Z. 4290

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**BorderThickness**
```powerfx
=3
```

**Fill**
```powerfx
=varProfilFarbe
```

**Height**
```powerfx
=60
```

**Width**
```powerfx
=60
```

**X**
```powerfx
=conHeader.Width - Circle2.Width - 20
```

**Y**
```powerfx
=conHeader.Height/2 - Circle2.Height/2
```

### [C183] Screen1 / conHeader / lblInitialen
Name: `lblInitialen` · Typ: `Label@2.5.1` · Eltern: `conHeader` · Properties: 10 · Z. 4300

**Align**
```powerfx
=Align.Center
```

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**Color**
```powerfx
=RGBA(50, 49, 48, 1)
```

**Font**
```powerfx
=Font.'Open Sans'
```

**FontWeight**
```powerfx
=FontWeight.Bold
```

**Size**
```powerfx
=20
```

**Text**
```powerfx
=With(
  { teile: Split(User().FullName, " ") },
  Upper(Left(First(teile).Value, 1) & Left(Last(teile).Value, 1))
)
```

**Width**
```powerfx
=47
```

**X**
```powerfx
=Circle2.X + Circle2.Width/2 -lblInitialen.Width/2
```

**Y**
```powerfx
=Circle2.Y + (Circle2.Height/2) - (lblInitialen.Height/2)
```

### [C184] Screen1 / conHeader / btnHitArea_1
Name: `btnHitArea_1` · Typ: `Classic/Button@2.2.0` · Eltern: `conHeader` · Properties: 17 · Z. 4317

**BorderColor**
```powerfx
=ColorFade(Self.Fill, -15%)
```

**Color**
```powerfx
=RGBA(255, 255, 255, 1)
```

**DisabledBorderColor**
```powerfx
=RGBA(166, 166, 166, 1)
```

**Fill**
```powerfx
=Color.Transparent
```

**Font**
```powerfx
=Font.'Open Sans'
```

**Height**
```powerfx
=Image6.Height
```

**HoverBorderColor**
```powerfx
=ColorFade(Self.BorderColor, 20%)
```

**HoverColor**
```powerfx
=RGBA(255, 255, 255, 1)
```

**HoverFill**
```powerfx
=RGBA(0, 0, 0, 0.08)
```

**OnSelect**
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**PressedBorderColor**
```powerfx
=Self.Fill
```

**PressedColor**
```powerfx
=Self.Fill
```

**PressedFill**
```powerfx
=ColorFade(Image6.Fill, -30%)
```

**Text**
```powerfx
=
```

**Width**
```powerfx
=Image6.Width
```

**X**
```powerfx
=Image6.X
```

**Y**
```powerfx
=Image6.Y
```

### [C185] Screen1 / conLadeOverlay
Name: `conLadeOverlay` · Typ: `GroupContainer@1.5.0` · Variante: `ManualLayout` · Eltern: `Screen1` · Properties: 4 · Z. 4341

**Fill**
```powerfx
=RGBA(0, 0, 0, 0.4)
```

**Height**
```powerfx
=Parent.Height
```

**Visible**
```powerfx
=varIsLoading
```

**Width**
```powerfx
=Parent.Width
```

### [C186] Screen1 / conLadeOverlay / imgSpinner
Name: `imgSpinner` · Typ: `Image@2.2.3` · Eltern: `conLadeOverlay` · Properties: 7 · Z. 4350

**BorderColor**
```powerfx
=RGBA(32, 54, 71, 1)
```

**DisplayMode**
```powerfx
=DisplayMode.Disabled
```

**Height**
```powerfx
=80
```

**Image**
```powerfx
='Spinner@1x-1.0s-201px-201px'
```

**Width**
```powerfx
=80
```

**X**
```powerfx
=(conLadeOverlay.Width/2) - (imgSpinner.Width/2)
```

**Y**
```powerfx
=(conLadeOverlay.Height/2) - (imgSpinner.Height/2)
```

## App-Einstellungen aus den Metadaten

Wortgetreu aus den Dateien des Exports (nur lesend). Datenzeilenlimit, `powerfxv1` und Feature-Flags stehen in `Properties.json` unter `AppPreviewFlagsMap` und in den Angaben von `Header.json` und der App-JSON des Pakets.

### src/Header.json
```json
{"DocVersion":"1.349","MinVersionToLoad":"1.349","MSAppStructureVersion":"2.4.0","LastSavedDateTimeUTC":"10/05/2026 11:58:18","AnalysisOptions":{"DataflowAnalysisEnabled":true,"DataflowAnalysisFlagStateToggledByUser":false}}
```

### src/Properties.json
```json
{
  "Author": "",
  "Name": "Tischbuchung",
  "Id": "e61d887c-84cf-4e0b-839c-79dbc3c333f8",
  "FileID": "e61d887c-84cf-4e0b-839c-79dbc3c333f8",
  "LocalConnectionReferences": "{\"78f6a232-a68a-4270-a9c6-8a907d8111f6\":{\"id\":\"78f6a232-a68a-4270-a9c6-8a907d8111f6\",\"connectionInstanceId\":\"/providers/microsoft.powerapps/apis/shared_sharepointonline/connections/shared-sharepointonline-939df73353394c89a0a25beae3b479e3\",\"dataSources\":[\"Tische\",\"Räume\",\"Raumbuchungen\",\"Tischbuchungen\"],\"datasets\":{\"https://technoformgroup.sharepoint.com/sites/IMSKonzept\":{\"dataSources\":{\"Tische\":{\"tableName\":\"2616c57d-887d-4d28-8188-6736c3ac21e9\"},\"Räume\":{\"tableName\":\"88536ba1-0a1f-4d49-9b4d-7c108e901932\"},\"Raumbuchungen\":{\"tableName\":\"0b5b1083-d01c-4121-8fda-d7fbc316c7c8\"},\"Tischbuchungen\":{\"tableName\":\"76791681-4416-481c-81a7-9dd8c2f1bded\"}}}},\"dependencies\":{},\"dependents\":[],\"connectionRef\":{\"id\":\"/providers/microsoft.powerapps/apis/shared_sharepointonline\",\"displayName\":\"SharePoint\",\"apiTier\":\"Standard\",\"iconUri\":\"https://static.powerapps.com/resource/ppcr/releases/v1.0.1827/1.0.1827.4913/sharepointonline/icon.png\",\"parameterHints\":{},\"parameterHintsV2\":{}},\"appActions\":[\"providers/PowerPlatform.Governance/Operations/Read\",\"providers/PowerPlatform.Governance/Operations/Write\",\"providers/PowerPlatform.Governance/Operations/Delete\"]}}",
  "LocalDatabaseReferences": "",
  "LibraryDependencies": "[]",
  "AppPreviewFlagsMap": {
    "delayloadscreens": true,
    "errorhandling": true,
    "enableappembeddingux": false,
    "blockmovingcontrol": true,
    "projectionmapping": true,
    "usedisplaynamemetadata": true,
    "usenonblockingonstartrule": true,
    "longlivingcache": false,
    "useguiddatatypes": true,
    "useexperimentalcdsconnector": true,
    "useenforcesavedatalimits": true,
    "webbarcodescanner": false,
    "datatablev2control": false,
    "nativecdsexperimental": true,
    "delaycontrolrendering": true,
    "useexperimentalsqlconnector": true,
    "formuladataprefetch": true,
    "generatedebugpublishedapp": false,
    "keeprecentscreensloaded": false,
    "aibuilderserviceenrollment": false,
    "dynamicschema": false,
    "enablerowscopeonetonexpand": false,
    "herocontrols": false,
    "classiccontrols": false,
    "fluentv9controls": false,
    "fluentv9controlspreview": false,
    "onegrid": false,
    "enablepcfmoderndatasets": true,
    "optimizedforteamsmeeting": false,
    "behaviorpropertyui": true,
    "autocreateenvironmentvariables": false,
    "externalmessage": false,
    "enableonstartnavigate": false,
    "enableexcelonlinebusinessv2connector": true,
    "enableonstart": true,
    "exportimportcomponents2": true,
    "copyandmerge": false,
    "allowmultiplescreensincanvaspages": false,
    "enablecomponentscopeoldbehavior": false,
    "enablecomponentnamemaps": false,
    "enablecreateaformula": true,
    "enablesaveloadcleardataonweb": true,
    "rtlsupport": false,
    "improvedtabstopbehavior": false,
    "rtlinstudiopreview": false,
    "cdsdataformatting": false,
    "enablerpawarecomponentdependency": true,
    "expandedsavedatasupport": true,
    "appinsightserrortracing": false,
    "appinstrumentationcorrelationtracing": false,
    "powerfxv1": false,
    "zeroalltabindexes": true,
    "dataverseactionsenabled": true,
    "pdffunction": false,
    "packagemodernruntime": false,
    "enablecopilotcontrol": false,
    "disablem365copilot": false,
    "showm365copilot": false,
    "enablecopilotanswercontrol": false,
    "disableruntimepolicies": false,
    "enablelegacybarcodescanner": false,
    "enabledataverseoffline": false,
    "mobilenativerendering": false,
    "smartemaildatacard": false,
    "enableupdateifdelegation": true,
    "dataflowanalysisenabled": true,
    "showclassicthemes": false,
    "userdefinedtypes": true,
    "enableeditinmcs": true,
    "disablebehaviorreturntypecheck": false,
    "commentgeneratedformulasv2": true,
    "enablecanvasappruntimecopilot": false,
    "offlineprofilegenerationemitscolumns": false,
    "proactivecontrolrename": true,
    "sharepointselectsenabled": true,
    "adaptivepaging": false,
    "optimizestartscreenpublishedappload": true,
    "loadcomponentdefinitionsondemand": true,
    "tabledoesntwraprecords": true,
    "consistentreturnschemafortabularfunctions": true,
    "supportcolumnnamesasidentifiers": true,
    "powerfxdecimal": false,
    "reservedkeywords": false,
    "isemptyrequirestableargument": true,
    "primaryoutputpropertycoerciondeprecated": true
  },
  "DocumentLayoutWidth": 1366,
  "DocumentLayoutHeight": 768,
  "DocumentLayoutOrientation": "landscape",
  "DocumentLayoutScaleToFit": false,
  "DocumentLayoutMaintainAspectRatio": false,
  "DocumentLayoutLockOrientation": false,
  "ShowStatusBar": false,
  "OriginatingVersion": "1.349",
  "DocumentAppType": "DesktopOrTablet",
  "DocumentType": "App",
  "AppCreationSource": "AppFromScreenTemplate",
  "AppDescription": "",
  "ManualOfflineProfileId": "",
  "DefaultConnectedDataSourceMaxGetRowsCount": 1000,
  "ContainsThirdPartyPcfControls": false,
  "ParserErrorCount": 1,
  "BindingErrorCount": 0,
  "ConnectionString": "",
  "EnableInstrumentation": false,
  "ControlCount": {
    "screen": 1,
    "groupContainer": 14,
    "image": 17,
    "circle": 2,
    "button": 44,
    "label": 55,
    "datepicker": 6,
    "dropdown": 8,
    "gallery": 5,
    "galleryTemplate": 5,
    "rectangle": 17,
    "icon": 3,
    "checkbox": 4,
    "toggleSwitch": 11
  },
  "DeserializationLoadTime": 1.931055,
  "AnalysisLoadTime": 2.2150472
}
```

### paket/Microsoft.PowerApps/apps/1516988942138200528/1516988942138200528.json
```json
{
  "schemaVersion": "1.0",
  "appDefinitionTemplate": {
    "id": "/providers/Microsoft.PowerApps/apps/",
    "type": "Microsoft.PowerApps/apps",
    "tags": {
      "primaryDeviceWidth": "1366",
      "primaryDeviceHeight": "768",
      "supportsPortrait": "true",
      "supportsLandscape": "true",
      "primaryFormFactor": "Tablet",
      "showStatusBar": "false",
      "publisherVersion": "3.26093.10",
      "minimumRequiredApiVersion": "2.2.0",
      "hasComponent": "false",
      "hasUnlockedComponent": "false",
      "isUnifiedRootApp": "false",
      "m365CopilotSettingValue": "0",
      "sienaVersion": "20260924T085441Z-3.26092.9.0"
    },
    "properties": {
      "appVersion": "2026-10-05T11:58:19Z",
      "lifeCycleId": "Published",
      "createdByClientVersion": {
        "major": 3,
        "minor": 26093,
        "build": 10,
        "revision": 0,
        "majorRevision": 0,
        "minorRevision": 0
      },
      "minClientVersion": {
        "major": 3,
        "minor": 26093,
        "build": 10,
        "revision": 0,
        "majorRevision": 0,
        "minorRevision": 0
      },
      "backgroundColor": "rgba(255, 255, 255, 1)",
      "backgroundImageUri": "/1516988942138200528/N4e69722d-e46a-4681-8af6-b67ea378a3ef-logoSmallFile",
      "displayName": "Tischbuchung",
      "commitMessage": "",
      "appUris": {
        "documentUri": {
          "value": "/1516988942138200528/N2392ebf5-6046-4245-a450-550349017614-document.msapp"
        },
        "imageUris": [],
        "additionalUris": [
          {
            "isSolutionAware": false,
            "value": "/1516988942138200528/N7acce795-4eff-4128-b3ff-718b48bae5f1-identity.json"
          }
        ]
      },
      "createdTime": "0001-01-01T00:00:00Z",
      "lastModifiedTime": "0001-01-01T00:00:00Z",
      "sharedGroupsCount": 0,
      "sharedUsersCount": 0,
      "connectionReferences": {
        "78f6a232-a68a-4270-a9c6-8a907d8111f6": {
          "id": "277fca69-d3a7-4537-885e-ae29c43b6568",
          "displayName": "SharePoint",
          "iconUri": "https://static.powerapps.com/resource/ppcr/releases/v1.0.1827/1.0.1827.4913/sharepointonline/icon.png",
          "dataSources": [
            "Tische",
            "Räume",
            "Raumbuchungen",
            "Tischbuchungen"
          ],
          "dependencies": [],
          "dependents": [],
          "parameterHints": {},
          "parameterHintsV2": {},
          "isOnPremiseConnection": false,
          "bypassConsent": false,
          "dataSets": {
            "https://technoformgroup.sharepoint.com/sites/IMSKonzept": {
              "dataSources": {
                "Tische": {
                  "tableName": "2616c57d-887d-4d28-8188-6736c3ac21e9"
                },
                "Räume": {
                  "tableName": "88536ba1-0a1f-4d49-9b4d-7c108e901932"
                },
                "Raumbuchungen": {
                  "tableName": "0b5b1083-d01c-4121-8fda-d7fbc316c7c8"
                },
                "Tischbuchungen": {
                  "tableName": "76791681-4416-481c-81a7-9dd8c2f1bded"
                }
              }
            }
          },
          "apiTier": "Standard",
          "isCustomApiConnection": false,
          "actions": [
            "providers/PowerPlatform.Governance/Operations/Read",
            "providers/PowerPlatform.Governance/Operations/Write",
            "providers/PowerPlatform.Governance/Operations/Delete"
          ]
        }
      },
      "databaseReferences": {},
      "almMode": "Environment",
      "performanceOptimizationEnabled": true,
      "canConsumeAppPass": true,
      "enableModernRuntimeMode": false,
      "executionRestrictions": {
        "isTeamsOnly": false,
        "dataLossPreventionEvaluationResult": {
          "status": "Compliant",
          "lastEvaluationDate": "2026-09-29T23:24:47.5780881Z",
          "violations": [],
          "violationsByPolicy": [],
          "violationErrorMessage": "The app uses the following connectors: shared_sharepointonline."
        }
      }
    },
    "isAppComponentLibrary": false,
    "appType": "ClassicCanvasApp",
    "appComponents": []
  }
}
```
