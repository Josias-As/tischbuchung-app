# 05 — Stand der Änderungen am 06.10.2026

**Kurzfassung:** Gegenüber dem Export vom 30.09.2026 haben sich genau **drei Properties** geändert, alle drei in Verhaltensformeln: `btnSpeichern.OnSelect` (Sammel-`Patch`), `btnStornierenKlein.OnSelect` (Stornieren-Neubau „Entwurf A", A.1) und `btnSchließenKlein.OnSelect` (A.2). Kein Steuerelement kam hinzu oder fiel weg, keine weitere Property wurde angefasst. **K1 bis K5 aus `ENTWURF_SPEICHERN.md` sind nicht eingebaut. A.3 und A.4 sind nicht eingebaut.** `btnSpeichernTischePanel` ist unverändert auf dem alten Stand.

Vergleich per Skript (`skripte/diff_alt_neu.js`): alter Quellcode `C:\tischbuchung_work\src\` (Export vom 30.09.2026, appVersion 2026-09-30T08:53:57Z) gegen `UEBERGABE_2026-10-06/src/` (Export vom 06.10.2026, appVersion 2026-10-05T11:58:19Z). Verglichen wurden alle 186 Steuerelemente mit allen 1979 Properties plus App und Screen.

| | alt (30.09.) | neu (05.10.) |
|---|---|---|
| Steuerelemente | 186 | 186 |
| Properties | 1979 | 1979 |
| neu hinzugekommen | — | 0 |
| entfallen | — | 0 |
| geändert | — | **3** |

---

## 1. Sammel-`Patch` in `btnSpeichern.OnSelect` — EINGEBAUT

**Kennzeichen aus der Aufgabe:** `neueDatensaetze`, `speicherStatus`. Beide stehen im Quellcode.

Fundstelle `src/Src/Screen1.pa.yaml`, Z. 2770 bis 2802, wortgetreu:

```powerfx
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
```

```powerfx
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
```

Das entspricht Abschnitt 5.1 des Briefings wortgetreu. Die vollständige Formel steht in `01_APP_KOMPLETT.md` unter `btnSpeichern` und in `02_BUTTONS.md`.

**Folgen, die im Quellcode sichtbar sind:**
- `btnSpeichern` ist der einzige Knopf mit `IfError` in der ganzen App (per Skript geprüft: `IfError` kommt zweimal vor, hier und in `btnStornierenKlein`).
- Die Warnung `app-ForAllWithMutation` der App-Prüfung steht jetzt nur noch an `btnSpeichernTischePanel.OnSelect` (eine statt drei; `AppCheckerResult.sarif`).
- `speicherStatus = "keine"` wird nirgends abgefragt: Sind alle Termine belegt, läuft die Meldungskette in den Zweig „n von m Terminen konnten wegen Kollision nicht gebucht werden".

**Nicht prüfbar am Quellcode (UNSICHER):** ob `Person` und `Tisch` zur Laufzeit korrekt geschrieben werden (offene Frage 2 des Briefings, Ü6), wie viele Netzwerkaufrufe entstehen, und was bei einem Teilausfall passiert. Dafür braucht es den Power-Apps-Monitor.

---

## 2. Stornieren-Neubau „Entwurf A" — A.1 und A.2 EINGEBAUT, A.3 und A.4 NICHT

### A.1 `btnStornierenKlein.OnSelect` — eingebaut

**Kennzeichen:** `colStornoFrisch`, `colStornoZiele`, `IfError(Remove(...))`. Alle drei stehen im Quellcode, `src/Src/Screen1.pa.yaml`, Z. 4086 bis 4121:

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

Das ist die Struktur aus Abschnitt 5.2 des Briefings, mit den dort gekürzten Meldungstexten jetzt vollständig.

### A.2 `btnSchließenKlein.OnSelect` — eingebaut

`Clear(colStornoFrisch);` und `Clear(colStornoZiele);` stehen in Z. 4144 und 4145, genau wie in `ENTWURF_MEHRFACHAUSWAHL.md` gefordert.

### A.3 „Alle auswählen" reparieren — NICHT eingebaut

`chkAlleAuswählen.OnCheck` steht unverändert auf (Z. 4195):

```powerfx
=ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)
```

Gefordert war `ClearCollect(colAusgewaehlteBuchungen; SortByColumns(Filter(Tischbuchungen; …); "Startzeit"; SortOrder.Ascending))`. Der Fehler besteht also fort: „Alle auswählen" markiert nur die in der Galerie geladenen Zeilen.

### A.4 Kopierfehler in `chkAuswahl.X` — NICHT eingebaut

`chkAuswahl.X` steht unverändert auf (Z. 3601):

```powerfx
=btnVerwalten_2.X - btnVerwalten.Width - 10
```

Gefordert war `btnVerwalten_2.Width`. `btnVerwalten` liegt in einer anderen Galerie (`conDashboard.galTischbuchungenHeute`).

---

## 3. K1 bis K5 aus `ENTWURF_SPEICHERN.md` — alle NICHT eingebaut

| | Was gefordert war | Stand im Quellcode |
|---|---|---|
| **K1** | `Set(varSelectedBuchung; ThisItem)` zusätzlich in `btnVerwalten_2.OnSelect` | **nicht da.** Z. 3568 bis 3578 enthält nur `Set(varSelectedBuchungTab, ThisItem)`. Befund B0 besteht fort. |
| **K2** | neue `btnVerlängern_1.OnSelect` mit Prüfreihenfolge und `IfError` | **nicht da.** Z. 3702 bis 3717 ist der alte Stand aus Abschnitt 5.3 des Briefings, einschließlich `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus, false)`, die laut K2 entfallen sollten. |
| **K3** | dasselbe für `conVerwaltenDialog.btnVerlängern` | **nicht da.** Z. 3256 bis 3268 ist der alte Stand. |
| **K4.1** | Zeitgrenze in der Kollisionsabfrage beider Speichern-Knöpfe | **nicht da.** `bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = …)` ohne Zeitgrenze in Z. 2734 und Z. 966. |
| **K4.2** | `>` statt `<>` in `effektivesBisRoh` | **nicht da.** `<>` steht in Z. 2733 und Z. 965. |
| **K4.3** | `IfError` um den `Patch` je Termin | in `btnSpeichern` **anders gelöst** (ein `IfError` um den Sammel-`Patch`, siehe oben). In `btnSpeichernTischePanel` **nicht da**. |
| **K4.4** | kombinierte Meldung, Kappungshinweis nicht verdrängend | **nicht da.** In beiden Knöpfen verdrängt `If(effektivesBisRoh > effektivesBis; Notify("… auf 2 Wochen begrenzt."); …)` weiterhin die anderen Meldungen (Z. 2810, Z. 1032). |
| **K5** | `DisplayMode: If(varIsLoading; …)` an vier Knöpfen | **nicht da.** Keiner von `btnSpeichern`, `btnSpeichernTischePanel`, `btnVerlängern`, `btnVerlängern_1` hat eine `DisplayMode`-Property (per Skript geprüft). |

---

## 4. Was sich gegenüber `INVENTAR.md` sonst geändert hat

Nichts. Der Skript-Vergleich der Formeln findet außer den drei oben genannten Properties keinen Unterschied. Damit gelten alle anderen Feststellungen aus `INVENTAR.md` unverändert, unter anderem:

- genau ein Screen (`Screen1`), kein `Screen2`
- `Screen1.LoadingSpinner = LoadingSpinner.Data` (Z. 13) neben dem eigenen Overlay `conLadeOverlay`
- `varSpinnerWinkel` ohne Timer (es gibt im ganzen Quellcode kein Timer-Steuerelement)
- `powerfxv1 = False` (`Properties.json`)
- neun `Refresh`-Aufrufe, keiner in einer Schleife (per Skript nachgezählt: neun Vorkommen von `Refresh(Tischbuchungen)`)
- `SerienID` existiert und wird nirgends benutzt

**Eine Zahl aus `INVENTAR.md` stimmt so nicht mehr:** Dort steht „79 Vorkommen `Titel`, 0× `Title`". Im neuen Quellcode zählt das Skript **84× `Titel`** und **3× `Title`**. Zwei der drei `Title`-Treffer sind der Steuerelementname `Title1` in `galRäume` (Z. 1566, 1600). Der dritte ist eine echte Spaltenangabe: `ddTischePanel.Items.Value: =Title` (Z. 825), der interne Name der Titelspalte von `Tische`. Die Regel „die App schreibt `Titel`" gilt also mit genau dieser einen Ausnahme.

**Geändert hat sich die Zahl der Prüfungsmeldungen**, weil der Sammel-`Patch` die `ForAll`-mit-Schreiben-Warnung von `btnSpeichern` beseitigt hat. Der neue `AppCheckerResult.sarif` (Stand 05.10.2026 11:58) enthält 134 Ergebnisse, davon 0 Fehler:

| Regel | Anzahl |
|---|---|
| `acc-AccessibleLabelNeeded` | 37 |
| `app-SuggestRemoteExecutionHint` | 32 |
| `acc-TabIndexShouldBeDefinedForInteractiveControl` | 19 |
| `app-SuggestRemoteExecutionHint-OpNotSupportedByService` | 14 |
| `app-SuggestRemoteExecutionHint-OpNotSupportedByColumn` | 10 |
| `app-UnusedVariables` | 10 |
| `acc-FocusBorderShouldBeVisible` | 7 |
| `app-CollectingReadOnlyTable` | 2 |
| `acc-ReadableScreenNameNeeded` | 1 |
| `app-ScreenHasManyControls` | 1 |
| `app-ForAllWithMutation` | 1 |

Die 56 Delegationswarnungen des Briefings entsprechen den 56 `app-SuggestRemoteExecutionHint`-Meldungen (32 + 14 + 10). `app-ForAllWithMutation` steht nur noch an `btnSpeichernTischePanel.OnSelect`.

---

## 5. Was daraus folgt

1. **Der Sammel-`Patch` steht nur in einem der beiden Speichern-Wege.** `btnSpeichernTischePanel` schreibt weiter je Termin einzeln, ohne `IfError`. Ü8 des Briefings gilt unverändert: Jede Änderung muss in beiden Knöpfen separat gemacht werden.
2. **Befund B0 ist offen.** Die zwölf Dauer-Knopf-Properties im Buchungen-Tab lesen weiter `varSelectedBuchung`. Das ist der einzige belegte Weg zu einer stillen Doppelbuchung im heutigen Code.
3. **Keine Doppelklick-Sperre.** K5 fehlt überall; kein Speichern- oder Verlängern-Knopf hat `DisplayMode`.
4. **Die Serienbuchung kennt weiterhin keine `SerienID`.** Ohne sie ist eine Nachlese nach dem Speichern (Ü1) nicht möglich.
