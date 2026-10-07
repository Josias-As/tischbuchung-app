# ARBEITSSTAND_SPEICHERN.md — Runde 0 und Runde 1

Arbeitsdatei zum Lauf `AUFGABE_SPEICHERN.md`. Fortlaufend geführt, nicht am Ende aus der Erinnerung geschrieben. Das Endergebnis steht in `ENTWURF_SPEICHERN.md`, das Verwurfsprotokoll in `VERWORFEN_SPEICHERN.md`.

**Stand: 03.10.2026**

---

## Runde 0 — Die drei Pflichtfragen, belegt

### Frage 1: Was passiert heute bei fünf angehakten Buchungen, „+1 Std", „Speichern"?

**Antwort: Dieser Ablauf ist nicht erreichbar. Keine Buchung wird geändert, weil es den Weg nicht gibt.**

Beweiskette aus dem Quellcode:

**Schritt 1 — Auswahlmodus einschalten.** `conBuchungen.tglAuswahlModus.OnChange`, Zeile 4133:
```
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
Die letzte Anweisung setzt `varZeigeVerwaltenTab` auf `false`.

**Schritt 2 — der große Verwalten-Dialog wird dadurch unsichtbar.** `conBuchungen.conVerwaltenDialog_1.Visible`, Zeile 3613:
```
Visible: =varZeigeVerwaltenTab
```

**Schritt 3 — der Verwalten-Knopf führt im Auswahlmodus woandershin.** `galAlleTischbuchungen.btnVerwalten_2.OnSelect`, Zeile 3556:
```
=If(
  varAuswahlModusAktiv,
  Set(varGeklickteBuchungKlein, ThisItem);
  Set(varZeigeVerwaltenKlein, true),
  Set(varSelectedBuchungTab, ThisItem);
  Set(varZeigeVerwaltenTab, true);
  ...
)
```
Im Auswahlmodus öffnet er `conVerwaltenKlein`, nicht `conVerwaltenDialog_1`.

**Schritt 4 — `conVerwaltenKlein` hat keine Dauer-Knöpfe und kein Speichern.** Zeile 4013–4117, fünf Kinder:
`lblVerwaltenKleinDatum`, `lblVerwaltenKleinZeit`, `lblVerwaltenKleinTitel`, `btnStornierenKlein`, `btnSchließenKlein`.

**Es gibt im Auswahlmodus nur Stornieren und Schließen.** `btnVerlängern_1` (die Beschriftung „Speichern", Zeile 3679) sitzt in `conVerwaltenDialog_1` und ist im Auswahlmodus nicht erreichbar.

### Frage 2: Absicht oder Fehler?

**Weder noch — es ist eine Lücke, und die Oberfläche lügt dabei nicht.**

`conVerwaltenKlein` bietet ausschließlich „Stornieren" an und benennt den Umfang korrekt. `lblVerwaltenKleinTitel`, Zeile 4053:
```
=varGeklickteBuchungKlein.Tisch.Value &
If(
  CountRows(colAusgewaehlteBuchungen) > 1,
  " +" & (CountRows(colAusgewaehlteBuchungen) - 1) & " weitere",
  ""
)
```
Der Nutzer liest „OG Desk 3 +4 weitere" und bekommt genau einen Knopf, der auf alle fünf wirkt. Keine falsche Erfolgsmeldung, keine Sammelbeschriftung für eine Einzelaktion. **Kriterium 2 ist im Ist-Zustand nicht verletzt.**

Der irreführende Name `btnVerlängern_1` mit der Beschriftung „Speichern" betrifft nur den Einzeldialog und ist ein Namensproblem, kein Funktionsproblem.

### Frage 3: Was wäre das erwartete Verhalten?

Mehrfach-Verlängern und Mehrfach-Verkürzen existieren nicht und werden **neu gebaut, von Anfang an als Sammeloperation.** Es gibt nichts zu optimieren — ein einzelner `Patch` ist bereits schnell.

**Damit verschiebt sich der Schwerpunkt dieses Laufs.** Baustelle 1 ist Neubau einer fehlenden Funktion, nicht Beschleunigung einer langsamen. Die eigentliche Beschleunigungsarbeit liegt in Baustelle 2.

---

## Runde 0 — Der Befund, der alles andere überlagert

### B0 — Die sechs Dauer-Knöpfe im Buchungen-Tab lesen die falsche Buchung

**Steuerelemente:** `conBuchungen.conVerwaltenDialog_1.btnPlus1Std_1`, `btnPlus2Std_1`, `btnPlus3Std_1`, `btnMinus1Std`, `btnMinus2Std`, `btnMinus3std`
**Properties:** je `DisplayMode` und `Fill` — **zwölf Properties**
**Zeilen:** 3741, 3753, 3790, 3802, 3839, 3850, 3872, 3884, 3922, 3934, 3972, 3984

Alle zwölf beginnen mit:
```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
```

**Der Dialog arbeitet aber auf `varSelectedBuchungTab`.** Beleg, dieselbe Container-Ebene:
- `lblTitel3_1.Text`, Z. 3626: `varSelectedBuchungTab.Tisch.Value`
- `lblZeit3_1.Text`, Z. 3637: `varSelectedBuchungTab.Startzeit`
- `btnStornieren_1.OnSelect`, Z. 3666: `Remove(Tischbuchungen, varSelectedBuchungTab)`
- `btnVerlängern_1.OnSelect`, Z. 3692: `LookUp(Tischbuchungen, ID = varSelectedBuchungTab.ID)`

Und `btnVerwalten_2.OnSelect` (Z. 3561) setzt **ausschließlich** `varSelectedBuchungTab`. `varSelectedBuchung` wird im Buchungen-Tab nie gesetzt — es trägt noch den Wert aus dem Dashboard oder dem Grundriss, oder ist `Blank()`.

**Folge, und zwar in der gefährlichsten Richtung:** Die Knöpfe entscheiden über Freigabe (`DisplayMode`) und Farbe (`Fill`) anhand einer **fremden Buchung**. Der Nutzer sieht „+2 Std" grün und anklickbar, weil die *andere* Buchung dort frei wäre — klickt, speichert, und `btnVerlängern_1` verlängert die **richtige** Buchung in eine bestehende fremde Buchung hinein. Die einzige Kollisionsprüfung dieses Wegs sitzt in den Knopffarben; `btnVerlängern_1.OnSelect` selbst prüft nichts außer `IsBlank(varAusgewaehltePlusDauer)`.

**Das ist ein Doppelbuchungsweg, der ohne jede Fehlermeldung durchläuft.** Nach Kriterium 1 der höchste Rang in diesem Lauf.

Im Grundriss-Dialog `conVerwaltenDialog` (Z. 3283–3430) ist es korrekt: dort setzen `btnVerwalten.OnSelect` und `btnHitArea.OnSelect` tatsächlich `varSelectedBuchung`, und die Knöpfe lesen dieselbe Variable. **Nur die `_1`-Fassung ist kaputt** — beim Kopieren wurden Titel, Zeit, Stornieren und Speichern auf `varSelectedBuchungTab` umgestellt, die zwölf Knopf-Properties nicht.

Genau das Muster, vor dem `KONTEXT.md` warnt: „Nach jedem Kopieren die variierende Zahl in ALLEN Properties prüfen."

---

## Runde 0 — Nullpunkt Baustelle 2: Serienbuchung

Zwei wortgleiche Fassungen:

| Knopf | Container | Steuerelemente, die er liest |
|---|---|---|
| `btnSpeichern` (Z. 2716) | `conBuchungDialog` | `dpDatum`, `ddStart`, `ddEnde`, `dpWiederholenBis`, `varSelectedTisch` |
| `btnSpeichernTischePanel` (Z. 948) | `conTischBuchungenPanel` | `dpDatumTischePanel`, `ddStartTischePanel`, `ddEndTischePanel`, `dpWiederholenBis_1`, `ddTischePanel.Selected` |

Kern beider, hier `btnSpeichern` (Z. 2727–2827), gekürzt auf die entscheidenden Zeilen:

```
=Set(varIsLoading, true);
With(
  {
    neuStart: dpDatum.SelectedDate + Time(...),
    neuEnde: dpDatum.SelectedDate + Time(...),
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate, dpWiederholenBis.SelectedDate, dpDatum.SelectedDate),
    bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)
  },
  ...
      ergebnisse:
        ForAll(
          datumsListe As Eintrag,
          If(
            CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (...) && Endzeit > (...))) = 0,
            With(
              { neuerEintrag: Patch(Tischbuchungen, Defaults(Tischbuchungen), { ... }) },
              "gespeichert"
            ),
            "übersprungen"
          )
        )
  ...
);
Refresh(Tischbuchungen);
...
```

### Bewertung nach den sechs Kriterien, mit Belegen

**K1 Doppelbuchung.** Das Fenster ist **groß**. `bestehendeBuchungenTisch` wird im äußersten `With` **einmal** gelesen (Z. 2734) und danach für alle bis zu 14 Schleifendurchläufe wiederverwendet. Zwischen diesem Lesevorgang und dem letzten `Patch` liegt die gesamte Schreibdauer der Serie — bei beobachteter Drosselung mehrere Sekunden. Ein zweiter Nutzer, der in dieser Zeit denselben Tisch bucht, erzeugt eine echte Doppelbuchung, beide mit grüner Erfolgsmeldung.

**K2 Ehrlichkeit.** Grundsätzlich in Ordnung: Z. 2798–2806 zählt `anzahlUebersprungen` und meldet „X von Y Terminen konnten wegen Kollision nicht gebucht werden." **Aber zwei Löcher.** Erstens hat `Patch` kein `IfError` — schlägt ein Schreibvorgang fehl, zählt er trotzdem als „gespeichert", weil der `With`-Rückgabewert die Konstante `"gespeichert"` ist, unabhängig vom Ergebnis des `Patch`. Zweitens schlägt die Begrenzungsmeldung die Kollisionsmeldung: Z. 2800 prüft `effektivesBisRoh > effektivesBis` **zuerst** und meldet dann nur „Wiederholung wurde auf 2 Wochen begrenzt" — wurden gleichzeitig Termine wegen Kollision übersprungen, erfährt der Nutzer davon nichts.

**K3 Zugriffe.**

| Serientermine | Zugriffe | Zusammensetzung |
|---|---|---|
| 1 | 3 | 1 Lesen + 1 `Patch` + 1 `Refresh` |
| 5 | 7 | 1 + 5 + 1 |
| 14 | 16 | 1 + 14 + 1 |
| 50 | — | nicht erreichbar, Z. 2737 kappt bei `dpDatum.SelectedDate + 14` |

Gezählt: ein `Filter` auf `Tischbuchungen` (Z. 2734), ein `Patch` je nicht kollidierendem Schleifendurchlauf (Z. 2777), ein `Refresh` (Z. 2816). Die `CountRows(Filter(bestehendeBuchungenTisch; …))` in der Schleife laufen lokal auf der bereits geladenen Collection und kosten keinen Zugriff.

**K4 Delegierbarkeit.** `Filter(Tischbuchungen, Tisch.Value = …)` **ohne jede Zeitgrenze** — holt alle Buchungen dieses Tisches, die je existiert haben. Die App-Prüfung meldet diese Zeile nicht, meldet `Tisch.Value` aber an zehn anderen Stellen als `OpNotSupportedByColumn`. Bei zugekappten 2000 Zeilen Datenzeilenlimit und einem Aufräum-Flow, der nur 7 Tage zurück aufräumt, ist das heute unkritisch, aber unnötig.

**K5 Wartungsfläche.** **Zwei wortgleiche Fassungen** von rund 100 Zeilen, die bei jeder Änderung beide angefasst werden müssen. Dazu 15 Aufräum-Anweisungen (`Set`/`Reset`) am Ende jedes Knopfs, ebenfalls doppelt.

**K6 Einfügeaufwand.** Entfällt, Ist-Zustand.

**App-Prüfung:** `app-ForAllWithMutation` meldet drei Stellen. Eine war `btnStornierenKlein` (im Stornieren-Lauf behandelt). **Die beiden anderen sind genau diese zwei Speichern-Knöpfe:** `Screen1.conTischBuchungenPanel.btnSpeichernTischePanel.OnSelect` und `Screen1.conBuchungDialog.btnSpeichern.OnSelect`.

---

## Unbestätigte Kernannahme

**`VORHER_NACHHER.md` existiert nicht, und es liegen keinerlei Messwerte im Ordner.** Damit ist die zentrale Annahme dieses Laufs — dass weniger Datenquellen-Zugriffe spürbar schneller sind — in dieser App **nie gemessen worden.** Sie ist plausibel und durch das gemeldete Drosselungsmuster gestützt (bei 10 Wiederholungen waren Durchlauf 6 und 7 langsam), aber unbelegt.

**Was passiert, falls sie nicht stimmt:** Die Zugriffsreduktion bringt dann wenig, die Korrektheitsgewinne bleiben aber vollständig erhalten — B0 geschlossen, `IfError` überall, ehrliche Meldungen, kleineres Doppelbuchungsfenster. Diese Arbeit wäre dann immer noch richtig, nur aus einem anderen Grund.

---

## Runde 1 — Die acht Entwürfe

### Baustelle 1 — Mehrfach-Verlängern und -Verkürzen (Neubau)

- **1A — Sammel-`Patch` auf frisch aufgelöster Menge, Teilerfolg erlaubt.** Ein Lesevorgang beim Öffnen des Dialogs versorgt sowohl die Knopffarben als auch die Kollisionsprüfung. Beim Speichern ein zweiter Lesevorgang, dann ein `Patch` für alle. Kollidierende werden übersprungen und gezählt.
- **1B — Sammel-`Patch`, alles oder nichts.** Gleiche Vorprüfung, aber bei auch nur einer Kollision wird **nichts** geschrieben und die betroffenen Buchungen werden benannt.
- **1C — Absolute Zielzeit statt Delta.** Die sechs Dauer-Knöpfe weichen einer Auswahl „neues Ende: 15:00 / 16:00 / …". Die Operation wird dadurch wiederholbar: zweimal ausgeführt ändert nichts.
- **1D — Nicht verlängern, sondern ersetzen.** Auswahl stornieren und in einem `Collect` neu anlegen.

### Baustelle 2 — Serienbuchung

- **2A — Sammel-`Collect` mit lokal vorberechneter Datumsliste.** Ein Kollisions-Lesevorgang mit Zeitgrenze, lokale Prüfung aller Termine, ein `Collect` für die Überlebenden. Verhalten wie heute (Teilerfolg).
- **2B — Sammel-`Collect` mit `SerienID` und Nachprüfung-und-Rücknahme.** Wie 2A, zusätzlich eine gemeinsame `GUID()` je Serie. Nach dem Schreiben wird über `SerienID` nachgelesen; ergibt sich eine Kollision mit einer fremden Buchung, werden die eigenen Verlierer wieder entfernt. Schließt das Doppelbuchungsfenster.
- **2C — Alles oder nichts mit Vorab-Bericht.** Kollidiert ein Termin, wird nichts gespeichert und die betroffenen Tage werden genannt.
- **2D — Die Serie als ein Datensatz.** Statt 14 Zeilen eine Zeile mit Regel (Wochentage, Bis-Datum), die beim Lesen aufgefächert wird.

**Vorab ausgeschlossen, ohne eigene Runde:** Auslagern an einen Power-Automate-Flow. Diese Familie wurde im Stornieren-Lauf angegriffen und verworfen (`VERWORFEN.md`, Entwurf D) — nach einem Verbindungsabbruch kann die App nicht mehr feststellen, was geschehen ist. Die Begründung gilt beim Schreiben unverändert und wird nicht ein zweites Mal geprüft.
