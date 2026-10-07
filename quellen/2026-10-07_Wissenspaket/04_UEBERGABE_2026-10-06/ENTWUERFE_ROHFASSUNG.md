# ENTWUERFE_ROHFASSUNG.md — Runde 1, Eingabe für die Angriffsrunde

Arbeitsdatei. Enthält die Entwürfe mit vollständigen Formeln, bevor sie angegriffen wurden. **Noch nicht einfügen** — erst `ENTWURF_SPEICHERN.md` abwarten.

Deutsche Locale: `;` trennt Argumente, `;;` verkettet. Keine Kommentare.

---

# BAUSTELLE 1 — Mehrfach-Verlängern und -Verkürzen

Neubau. Die Funktion existiert nicht (siehe `ARBEITSSTAND_SPEICHERN.md`, Runde 0).

## Gemeinsame Grundlage für 1A, 1B, 1C

### G1 — Neue Variablen in `App.OnStart`

Ans Ende anhängen. **Die bisher letzte Zeile ist `Set(varSpinnerWinkel, 0)` ohne abschließendes Verkettungszeichen** — dort zuerst `;;` ergänzen.

```
Set(varDauerKlein; Blank());;
Clear(colPruefBestand);;
Clear(colPlan);;
Clear(colNachher);;
Clear(colPlanOk)
```

### G2 — `btnVerwalten_2.OnSelect` lädt den Bestand beim Öffnen

`Screen1.conBuchungen.galAlleTischbuchungen.btnVerwalten_2`, Zeile 3556.

ORIGINAL:
```
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

NEU:
```
If(
    varAuswahlModusAktiv;
    Set(varGeklickteBuchungKlein; ThisItem);;
    Set(varDauerKlein; Blank());;
    ClearCollect(colPruefBestand; Filter(Tischbuchungen; Endzeit >= Now()));;
    Set(varZeigeVerwaltenKlein; true);
    Set(varSelectedBuchungTab; ThisItem);;
    Set(varSelectedBuchung; ThisItem);;
    Set(varZeigeVerwaltenTab; true);;
    Set(varZeigeCheckin; false);;
    Set(varZeigeDetails; false);;
    Set(varZeigeDialog; false)
)
```

Zwei Änderungen. Erstens wird im Auswahlmodus einmal der künftige Bestand geladen, aus dem danach sowohl die Knopffarben als auch die Kollisionsprüfung gespeist werden — ohne weiteren Datenquellen-Zugriff. Zweitens wird im Einzelmodus zusätzlich `varSelectedBuchung` gesetzt: **das schließt Befund B0**, weil die zwölf Dauer-Knopf-Properties in `conVerwaltenDialog_1` diese Variable lesen.

### G3 — `conVerwaltenKlein` vergrößern

`Screen1.conBuchungen.conVerwaltenKlein`, Zeile 4013.

| Property | ORIGINAL | NEU |
|---|---|---|
| `Height` | `=150` | `230` |

### G4 — Sechs neue Dauer-Knöpfe in `conVerwaltenKlein`

Neu anzulegen, Typ `Classic/Button`. Namen und Positionen:

| Name | Offset `d` | `X` | `Text` |
|---|---|---|---|
| `btnKleinMinus3` | `-180` | `25` | `"-3Std"` |
| `btnKleinMinus2` | `-120` | `85` | `"-2Std"` |
| `btnKleinMinus1` | `-60` | `145` | `"-1Std"` |
| `btnKleinPlus1` | `60` | `205` | `"+1Std"` |
| `btnKleinPlus2` | `120` | `265` | `"+2Std"` |
| `btnKleinPlus3` | `180` | `325` | `"+3Std"` |

Gemeinsam für alle sechs: `Width: 50`, `Y: 95`, `Font: Font.'Open Sans'`, `Color: RGBA(255, 255, 255, 1)`, `DisabledFill: ColorFade(ColorValue("#EB3951"); 70%)`, `BorderColor: ColorFade(Self.Fill; -15%)`, `HoverFill: ColorFade(Self.Fill; -15%)`.

**`OnSelect`**, hier für `btnKleinPlus1`, bei den anderen nur die Zahl `60` durch den Offset aus der Tabelle ersetzen:
```
Set(varDauerKlein; If(varDauerKlein = 60; Blank(); 60))
```

**`Fill`**, hier für `btnKleinPlus1`:
```
With(
    { d: 60 };
    With(
        { betroffen: Filter(colPruefBestand As P; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = P.ID))) };
        With(
            {
                problem: CountRows(
                    Filter(
                        betroffen As B;
                        DateAdd(B.Endzeit; d; TimeUnit.Minutes) <= B.Startzeit ||
                        CountRows(
                            Filter(
                                colPruefBestand As N;
                                N.Tisch.Value = B.Tisch.Value && N.ID <> B.ID &&
                                N.Startzeit < DateAdd(B.Endzeit; d; TimeUnit.Minutes) && N.Endzeit > B.Startzeit
                            )
                        ) > 0
                    )
                )
            };
            If(
                varDauerKlein = d;
                ColorValue("#00A96B");
                If(
                    problem = 0;
                    ColorFade(ColorValue("#00A96B"); 70%);
                    ColorFade(ColorValue("#EB3951"); 70%)
                )
            )
        )
    )
)
```

**`DisplayMode`**, hier für `btnKleinPlus1`:
```
With(
    { d: 60 };
    With(
        { betroffen: Filter(colPruefBestand As P; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = P.ID))) };
        With(
            {
                moeglich: CountRows(
                    Filter(
                        betroffen As B;
                        DateAdd(B.Endzeit; d; TimeUnit.Minutes) > B.Startzeit &&
                        CountRows(
                            Filter(
                                colPruefBestand As N;
                                N.Tisch.Value = B.Tisch.Value && N.ID <> B.ID &&
                                N.Startzeit < DateAdd(B.Endzeit; d; TimeUnit.Minutes) && N.Endzeit > B.Startzeit
                            )
                        ) = 0
                    )
                )
            };
            If(moeglich = 0; DisplayMode.Disabled; DisplayMode.Edit)
        )
    )
)
```

**Bekannte Vereinfachung, bewusst so gewählt:** Die Einfärbung rechnet gegen den Bestand **vor** der Änderung. Werden zwei ausgewählte Buchungen auf demselben Tisch gleichzeitig verlängert, kann die Färbung zu optimistisch sein. Der Speichern-Schritt rechnet die gegenseitige Beeinflussung vollständig durch und meldet das Ergebnis. Die Farbe ist ein Hinweis, die Meldung ist die Wahrheit.

### G5 — Die drei Aktionsknöpfe nach unten

| Steuerelement | Property | ORIGINAL | NEU |
|---|---|---|---|
| `btnSchließenKlein` | `Y` | `=95` | `170` |
| `btnSchließenKlein` | `Width` | `=btnStornierenKlein.Width` | `(Parent.Width - 80) / 3` |
| `btnStornierenKlein` | `Y` | `=95` | `170` |
| `btnStornierenKlein` | `Width` | `=Parent.Width / 2 - 30` | `(Parent.Width - 80) / 3` |
| `btnStornierenKlein` | `X` | `=Parent.Width - Self.Width - 25` | `25 + (Parent.Width - 80) / 3 + 15` |

Neu: `btnSpeichernKlein`, `Width: (Parent.Width - 80) / 3`, `X: Parent.Width - Self.Width - 25`, `Y: 170`, `Fill: ColorValue("#171496")`, `Text: "Speichern"`.

---

## Entwurf 1A — Sammel-`Patch`, Teilerfolg erlaubt

`btnSpeichernKlein.OnSelect`:

```
Set(varIsLoading; true);;
If(
    IsBlank(varDauerKlein);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    If(
        CountRows(colAusgewaehlteBuchungen) = 0;
        Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
        ClearCollect(colPruefBestand; Filter(Tischbuchungen; Endzeit >= Now()));;
        ClearCollect(
            colPlan;
            ForAll(
                Filter(colPruefBestand As P; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = P.ID))) As B;
                {
                    PlanID: B.ID;
                    PlanTisch: B.Tisch.Value;
                    PlanStart: B.Startzeit;
                    PlanEndeNeu: DateAdd(B.Endzeit; varDauerKlein; TimeUnit.Minutes)
                }
            )
        );;
        ClearCollect(
            colNachher;
            ForAll(
                colPruefBestand As P;
                {
                    NID: P.ID;
                    NTisch: P.Tisch.Value;
                    NStart: P.Startzeit;
                    NEnde: If(
                        IsBlank(LookUp(colPlan As Q; Q.PlanID = P.ID));
                        P.Endzeit;
                        LookUp(colPlan As Q; Q.PlanID = P.ID).PlanEndeNeu
                    )
                }
            )
        );;
        ClearCollect(
            colPlanOk;
            Filter(
                colPlan As P;
                P.PlanEndeNeu > P.PlanStart &&
                CountRows(
                    Filter(
                        colNachher As N;
                        N.NTisch = P.PlanTisch && N.NID <> P.PlanID &&
                        N.NStart < P.PlanEndeNeu && N.NEnde > P.PlanStart
                    )
                ) = 0
            )
        );;
        If(
            CountRows(colPlanOk) = 0;
            Notify("Keine der ausgewählten Buchungen lässt sich so ändern. Es wurde nichts gespeichert."; NotificationType.Warning);
            IfError(
                Patch(Tischbuchungen; ForAll(colPlanOk As P; {ID: P.PlanID; Endzeit: P.PlanEndeNeu}));
                Notify("Speichern fehlgeschlagen. Die Liste wurde aktualisiert, bitte prüfen."; NotificationType.Error);
                If(
                    CountRows(colPlanOk) < CountRows(colAusgewaehlteBuchungen);
                    Notify(CountRows(colPlanOk) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen geändert. Bei den übrigen war die Zeit belegt oder die Buchung zu kurz."; NotificationType.Warning);
                    Notify(CountRows(colPlanOk) & " Buchungen geändert."; NotificationType.Success)
                )
            )
        )
    )
);;
Refresh(Tischbuchungen);;
Clear(colPruefBestand);;
Clear(colPlan);;
Clear(colNachher);;
Clear(colPlanOk);;
Clear(colAusgewaehlteBuchungen);;
Set(varDauerKlein; Blank());;
Set(varGeklickteBuchungKlein; Blank());;
Set(varZeigeVerwaltenKlein; false);;
Set(varAuswahlModusAktiv; false);;
Reset(tglAuswahlModus);;
Set(varIsLoading; false)
```

**Zugriffe:** 1 Lesen beim Öffnen (G2) + 1 Lesen beim Speichern + 1 `Patch` + 1 `Refresh` = **4, konstant bei 1, 5, 14 und 50.**

---

## Entwurf 1B — Sammel-`Patch`, alles oder nichts

Wie 1A bis einschließlich `colPlanOk`. Danach:

```
        If(
            CountRows(colPlanOk) < CountRows(colPlan);
            Notify(
                "Nicht gespeichert: bei " & (CountRows(colPlan) - CountRows(colPlanOk)) & " von " & CountRows(colPlan) &
                " Buchungen ist die neue Zeit belegt oder die Buchung würde zu kurz. Bitte Auswahl oder Dauer anpassen."; NotificationType.Warning
            );
            IfError(
                Patch(Tischbuchungen; ForAll(colPlanOk As P; {ID: P.PlanID; Endzeit: P.PlanEndeNeu}));
                Notify("Speichern fehlgeschlagen. Die Liste wurde aktualisiert, bitte prüfen."; NotificationType.Error);
                Notify(CountRows(colPlanOk) & " Buchungen geändert."; NotificationType.Success)
            )
        )
```

Zusätzlich im Fehlerfall **nicht** aufräumen, damit der Nutzer die Auswahl behält und die Dauer ändern kann. Der Aufräumblock am Ende wird dazu in den Erfolgszweig verschoben.

**Zugriffe:** identisch zu 1A, **4 konstant**, im Verweigerungsfall **2** (zwei Lesevorgänge, kein Schreiben).

---

## Entwurf 1C — Absolute Zielzeit statt Delta

Statt sechs Dauer-Knöpfen ein Dropdown `ddZielEndeKlein` in `conVerwaltenKlein`.

`Items`:
```
ForAll(
    Sequence(29; 16) As S;
    { Value: Text(Time(RoundDown(S.Value * 30 / 60; 0); Mod(S.Value * 30; 60); 0); "hh:mm") }
)
```
(Halbstundenschritte von 08:00 bis 22:00.)

`OnChange`:
```
Set(varZielEndeKlein; ddZielEndeKlein.Selected.Value)
```

Im Speichern-Schritt ersetzt
```
PlanEndeNeu: DateAdd(B.Endzeit; varDauerKlein; TimeUnit.Minutes)
```
durch
```
PlanEndeNeu: DateValue(Text(B.Startzeit; "yyyy-mm-dd")) + Time(Value(Left(varZielEndeKlein; 2)); Value(Mid(varZielEndeKlein; 4; 2)); 0)
```
Der Rest ist identisch zu 1A.

**Der Unterschied ist fachlich, nicht technisch:** Die Operation wird dadurch wiederholbar — zweimal „bis 17:00" ausgeführt ändert beim zweiten Mal nichts. Zweimal „+1 Std" verlängert um zwei Stunden.

**Zugriffe:** wie 1A, **4 konstant**.

---

## Entwurf 1D — Nicht ändern, sondern ersetzen

Auswahl stornieren und in einem `Collect` mit neuen Zeiten neu anlegen.

**Keine Formeln ausgearbeitet.** Der Entwurf scheidet vor der Angriffsrunde aus strukturellen Gründen aus, die keine Formel heilt — Begründung in `VERWORFEN_SPEICHERN.md`.

---

# BAUSTELLE 2 — Serienbuchung

Beide Knöpfe sind wortgleich. Unten steht die Fassung für `conBuchungDialog.btnSpeichern`. Für `btnSpeichernTischePanel` sind durchgängig zu ersetzen: `dpDatum` → `dpDatumTischePanel`, `ddStart` → `ddStartTischePanel`, `ddEnde` → `ddEndTischePanel`, `dpWiederholenBis` → `dpWiederholenBis_1`, `varSelectedTisch` → `ddTischePanel.Selected`.

## Gemeinsame Grundlage für 2A, 2B, 2C

### G6 — Neue Variablen in `App.OnStart`

```
Set(varNeuStart; Blank());;
Set(varNeuEnde; Blank());;
Set(varBisRoh; Blank());;
Set(varBis; Blank());;
Set(varSerienID; "");;
Clear(colSerieTage);;
Clear(colBestandTisch);;
Clear(colNeueBuchungen)
```

**Warum überhaupt Variablen:** `With()` wertet seine Felder gleichzeitig aus, deshalb kann `bestehendeBuchungenTisch` im heutigen Code nicht auf `effektivesBis` zugreifen — genau deshalb fehlt dort die Zeitgrenze. Aufeinanderfolgende `Set` und `ClearCollect` im Verhaltensausdruck lösen das Problem ohne sechsfache `With`-Verschachtelung.

---

## Entwurf 2A — Sammel-`Collect`, Teilerfolg wie heute

`conBuchungDialog.btnSpeichern.OnSelect`:

```
Set(varIsLoading; true);;
Set(varNeuStart; dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0));;
Set(varNeuEnde; dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0));;
Set(varBisRoh; If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate));;
Set(varBis; Min(varBisRoh; dpDatum.SelectedDate + 14));;
Set(varSerienID; GUID());;
ClearCollect(
    colSerieTage;
    Filter(
        ForAll(
            Sequence(DateDiff(dpDatum.SelectedDate; varBis; TimeUnit.Days) + 1; 0) As S;
            { Tag: DateAdd(dpDatum.SelectedDate; S.Value; TimeUnit.Days) }
        ) As T;
        If(
            !varWiederholen;
            T.Tag = dpDatum.SelectedDate;
            If(
                varWiederholenModus = "Taeglich";
                true;
                Switch(Weekday(T.Tag; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
            )
        )
    )
);;
ClearCollect(
    colBestandTisch;
    Filter(
        Tischbuchungen;
        Tisch.Value = varSelectedTisch.Titel && Startzeit >= dpDatum.SelectedDate && Startzeit < DateAdd(varBis; 1; TimeUnit.Days)
    )
);;
ClearCollect(
    colNeueBuchungen;
    ForAll(
        Filter(
            colSerieTage As T;
            CountRows(
                Filter(
                    colBestandTisch As B;
                    B.Startzeit < (T.Tag + Time(Hour(varNeuEnde); Minute(varNeuEnde); 0)) &&
                    B.Endzeit > (T.Tag + Time(Hour(varNeuStart); Minute(varNeuStart); 0))
                )
            ) = 0
        ) As F;
        {
            Tisch: { Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel };
            Startzeit: F.Tag + Time(Hour(varNeuStart); Minute(varNeuStart); 0);
            Endzeit: F.Tag + Time(Hour(varNeuEnde); Minute(varNeuEnde); 0);
            SerienID: varSerienID;
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
);;
If(
    CountRows(colSerieTage) = 0;
    If(
        !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
        Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
        Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
    );
    If(
        CountRows(colNeueBuchungen) = 0;
        Notify("Alle " & CountRows(colSerieTage) & " Termine sind bereits belegt. Es wurde nichts gespeichert."; NotificationType.Warning);
        IfError(
            Collect(Tischbuchungen; colNeueBuchungen);
            Notify("Speichern fehlgeschlagen. Bitte die Liste prüfen und erneut versuchen."; NotificationType.Error);
            Notify(
                CountRows(colNeueBuchungen) & " von " & CountRows(colSerieTage) & " Terminen gespeichert." &
                If(CountRows(colNeueBuchungen) < CountRows(colSerieTage); " Die übrigen waren belegt."; "") &
                If(varBisRoh > varBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
                If(
                    CountRows(colNeueBuchungen) < CountRows(colSerieTage) || varBisRoh > varBis;
                    NotificationType.Warning;
                    NotificationType.Success
                )
            )
        )
    )
);;
Refresh(Tischbuchungen);;
Clear(colSerieTage);;
Clear(colBestandTisch);;
Clear(colNeueBuchungen);;
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

**Zugriffe:** 1 Lesen + 1 `Collect` + 1 `Refresh` = **3, konstant bei 1, 5 und 14.** Heute: 3 / 7 / 16.

**Drei Korrekturen gegenüber heute, über die reine Geschwindigkeit hinaus:**
1. `colBestandTisch` hat eine Zeitgrenze (heute: keine).
2. `IfError` um den Schreibvorgang (heute: keiner, und ein fehlgeschlagener `Patch` zählte als „gespeichert").
3. Eine Meldung trägt beide Tatsachen — Kollision **und** Zweiwochenkappung. Heute verdeckt die Kappungsmeldung die Kollisionsmeldung.

---

## Entwurf 2B — Sammel-`Collect` mit `SerienID`, Nachprüfung und Rücknahme

Wie 2A bis einschließlich `Collect`. Danach, im `DefaultResult` des `IfError` **vor** der Erfolgsmeldung eingefügt:

```
ClearCollect(
    colKontrolle;
    Filter(
        Tischbuchungen;
        Tisch.Value = varSelectedTisch.Titel && Startzeit >= dpDatum.SelectedDate && Startzeit < DateAdd(varBis; 1; TimeUnit.Days)
    )
);;
ClearCollect(
    colVerlierer;
    Filter(
        colKontrolle As M;
        M.SerienID = varSerienID &&
        CountRows(
            Filter(colKontrolle As O; O.ID < M.ID && O.Startzeit < M.Endzeit && O.Endzeit > M.Startzeit)
        ) > 0
    )
);;
If(
    CountRows(colVerlierer) > 0;
    IfError(
        Remove(Tischbuchungen; colVerlierer);
        Notify("Achtung: " & CountRows(colVerlierer) & " Termine wurden zeitgleich von jemand anderem gebucht und konnten nicht zurückgenommen werden. Bitte die Liste prüfen."; NotificationType.Error);
        Notify(
            (CountRows(colNeueBuchungen) - CountRows(colVerlierer)) & " von " & CountRows(colSerieTage) &
            " Terminen gespeichert. " & CountRows(colVerlierer) & " Termine wurden zeitgleich von jemand anderem gebucht und deshalb wieder freigegeben.";
            NotificationType.Warning
        )
    );
    Notify( ... Erfolgsmeldung wie in 2A ... )
)
```

**Die Regel „niedrigste ID gewinnt"** ist symmetrisch: Beide gleichzeitig schreibenden Clients lesen hinterher denselben Bestand und kommen zum selben Ergebnis. Der Zweite nimmt seine Zeilen zurück, der Erste behält seine. Niemand bekommt eine Erfolgsmeldung für etwas, das nicht gilt.

**Zugriffe:** 1 Lesen + 1 `Collect` + 1 Nachlesen + 1 `Refresh` = **4 konstant**, im Kollisionsfall 5.

Zusätzlich in `App.OnStart`: `Clear(colKontrolle);; Clear(colVerlierer)`.

---

## Entwurf 2C — Alles oder nichts

Wie 2A, aber:

```
    If(
        CountRows(colNeueBuchungen) < CountRows(colSerieTage);
        Notify(
            "Nicht gespeichert: " & (CountRows(colSerieTage) - CountRows(colNeueBuchungen)) & " von " & CountRows(colSerieTage) &
            " Terminen sind belegt. Bitte Zeitraum oder Uhrzeit anpassen."; NotificationType.Warning
        );
        IfError( ... Collect wie in 2A ... )
    )
```
Der Dialog bleibt im Verweigerungsfall offen, der Aufräumblock wandert in den Erfolgszweig.

**Zugriffe:** 3 konstant, im Verweigerungsfall 1.

---

## Entwurf 2D — Die Serie als ein Datensatz

Statt 14 Zeilen eine Zeile mit Wiederholungsregel, die beim Lesen aufgefächert wird.

**Keine Formeln ausgearbeitet.** Scheidet vor der Angriffsrunde strukturell aus — Begründung in `VERWORFEN_SPEICHERN.md`.
