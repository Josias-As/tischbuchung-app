# ENTWURF_SPEICHERN.md

**Stand: 03.10.2026** · Grundlage: Quellcode in `./src`, `INVENTAR.md`, Prüfberichte von sechs Subagenten

---

# KURZFASSUNG

## Das eigentliche Problem

**Die Annahme, auf der diese Aufgabe beruht, trägt nicht.** „Sammelaufruf statt Schleife" spart gegen SharePoint keine Aufrufe — `Collect`, `Patch` und `Remove` mit einer Tabelle sind für den SharePoint-Konnektor keine Sammelvorgänge, sondern ein Aufruf je Zeile. Drei Prüfer, die voneinander nichts wussten, sind unabhängig darauf gekommen. Was sich ändert, ist nur die Verpackung: Die Aufrufe gehen als Bündel hinaus statt nacheinander — was eine Drosselung mit 429 eher auslöst als verhindert.

**Das Mehrfach-Speichern, das schneller werden sollte, gibt es nicht.** Im Auswahlmodus öffnet der Stift-Knopf den kleinen Dialog `conVerwaltenKlein`, und der hat nur „Stornieren" und „Schließen". Der Knopf mit der Beschriftung „Speichern" sitzt im anderen Dialog und ändert genau eine Buchung.

**Dafür gibt es im Ist-Zustand einen Weg zur Doppelbuchung, der ohne jede Fehlermeldung durchläuft.** Die sechs Dauer-Knöpfe im Buchungen-Tab entscheiden über Freigabe und Farbe anhand einer **anderen Buchung** als der, die gespeichert wird.

## Was ich empfehle

**Baue das Mehrfach-Speichern jetzt nicht.** Acht Entwurfsfamilien sind an den Ausschlusskriterien gescheitert, sechs davon im Angriff durch unabhängige Prüfer. Zehn Tage vor dem Produktivgang ist eine neue Funktion, die in acht Anläufen nicht ehrlich zu bekommen war, das falsche Risiko.

**Nimm stattdessen die fünf Korrekturen unten.** Sie sind klein, voneinander unabhängig, hängen nicht an der widerlegten Geschwindigkeitsannahme und schließen je einen belegten Fehler. Zusammen etwa eine Stunde.

**Miss danach.** Ohne Zahl bleibt jede Aussage über Geschwindigkeit in diesem Projekt Glaubenssache — auch meine aus dem Stornieren-Lauf.

## Einfügereihenfolge

| | Was | Wo | Dauer |
|---|---|---|---|
| 1 | **K1 — Dauer-Knöpfe lesen die richtige Buchung** | `btnVerwalten_2.OnSelect`, eine Zeile mehr | 5 Min |
| 2 | **K2 — Verlängern prüft, bevor es schreibt** | `btnVerlängern_1.OnSelect` | 15 Min |
| 3 | **K3 — dasselbe im Grundriss-Dialog** | `btnVerlängern.OnSelect` | 10 Min |
| 4 | **K4 — Serienbuchung wird ehrlich** | `btnSpeichern.OnSelect`, danach `btnSpeichernTischePanel.OnSelect` | 30 Min |
| 5 | **K5 — Doppelklick-Riegel** | `DisplayMode` an vier Knöpfen | 5 Min |

## Der eine Test, der beweist, dass es gewirkt hat

**Zwei Browser-Tabs.** In Tab 1 im Buchungen-Tab eine Buchung 10:00–12:00 an OG Desk 1 verwalten, aber noch nicht speichern. In Tab 2 denselben Tisch 12:00–14:00 buchen. Zurück in Tab 1 „+3 Std" wählen und „Speichern".

- **Vorher:** Der Knopf ist grün, es wird gespeichert, OG Desk 1 ist von 12:00 bis 14:00 doppelt belegt, beide Nutzer haben eine Erfolgsmeldung gesehen.
- **Nachher:** „Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen." Nichts wird geschrieben.

## Welche Annahme unbestätigt ist

**Dass weniger Datenquellen-Zugriffe diese App spürbar schneller machen — das ist in diesem Projekt nie gemessen worden.** `VORHER_NACHHER.md` existiert nicht, es liegen keinerlei Messwerte vor.

Inzwischen spricht mehr dagegen als dafür: Wenn der Sammelaufruf keine Aufrufe spart, dann gab es bei der Serienbuchung nie etwas einzusparen, und die beobachtete Langsamkeit kommt allein aus der Drosselung. **Falls das stimmt, bringt kein Umbau der Schreibpfade Geschwindigkeit** — dann hilft nur, weniger und seltener zu schreiben, und die eigentliche Arbeit liegt bei der Ladezeit und beim Rendern des Grundrisses.

**Das betrifft auch meine letzte Lieferung.** Die Empfehlung in `ENTWURF_MEHRFACHAUSWAHL.md` beruht auf derselben Annahme; sie ist dort als `UNSICHER` markiert. Die Korrektheitsgewinne dort bleiben gültig, der Geschwindigkeitsgewinn ist fraglich geworden. Miss beim Stornieren mit, wenn du es einbaust.

---
---

# TEIL 1 — Was die Prüfung ergeben hat

## 1.1 Die drei Pflichtfragen

**Was passiert heute bei fünf angehakten Buchungen, „+1 Std", „Speichern"? — Der Ablauf ist nicht erreichbar.**

`tglAuswahlModus.OnChange` (Z. 4144) setzt beim Einschalten `varZeigeVerwaltenTab` auf `false`, und `conVerwaltenDialog_1.Visible` (Z. 3613) hängt daran. `btnVerwalten_2.OnSelect` (Z. 3556) öffnet im Auswahlmodus `conVerwaltenKlein`. Dessen fünf Kinder (Z. 4013–4117) sind zwei Beschriftungen, eine Zeitangabe, „Stornieren" und „Schließen". Keine Dauer-Knöpfe, kein Speichern.

**Absicht oder Fehler? — Eine Lücke, und die Oberfläche lügt dabei nicht.** `lblVerwaltenKleinTitel` (Z. 4053) schreibt korrekt „OG Desk 3 +4 weitere" und bietet genau einen Knopf, der auf alle fünf wirkt. Kriterium 2 ist im Ist-Zustand an dieser Stelle **nicht** verletzt.

**Was wäre das erwartete Verhalten? — Neubau als Sammeloperation.** Genau das wurde versucht, achtmal, und ist achtmal gescheitert. Siehe Teil 2.

## 1.2 Der Befund, der alles überlagert: B0

**Die zwölf Dauer-Knopf-Properties im Buchungen-Tab lesen `varSelectedBuchung`. Der Dialog arbeitet auf `varSelectedBuchungTab`.**

Betroffen: `btnPlus1Std_1`, `btnPlus2Std_1`, `btnPlus3Std_1`, `btnMinus1Std`, `btnMinus2Std`, `btnMinus3std`, je `DisplayMode` und `Fill`. Zeilen 3741, 3753, 3790, 3802, 3839, 3850, 3872, 3884, 3922, 3934, 3972, 3984 — alle beginnen mit:
```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
```

Der Dialog dagegen liest überall `varSelectedBuchungTab`: Titel (Z. 3626), Zeit (Z. 3637), Stornieren (Z. 3666), Speichern (Z. 3692). Und `btnVerwalten_2.OnSelect` (Z. 3561) setzt **ausschließlich** `varSelectedBuchungTab`. `varSelectedBuchung` trägt noch den Wert aus dem Dashboard oder dem Grundriss, oder ist `Blank()`.

**Folge in der gefährlichsten Richtung:** Der Nutzer sieht „+2 Std" grün und anklickbar, weil die *andere* Buchung dort frei wäre. Er klickt, speichert, und `btnVerlängern_1` verlängert die **richtige** Buchung in eine fremde hinein. Die einzige Kollisionsprüfung dieses Wegs steckt in den Knopffarben — `btnVerlängern_1.OnSelect` selbst prüft nichts außer `IsBlank(varAusgewaehltePlusDauer)`.

Im Grundriss-Dialog `conVerwaltenDialog` ist es korrekt. **Nur die `_1`-Fassung ist kaputt**: Beim Kopieren wurden Titel, Zeit, Stornieren und Speichern umgestellt, die zwölf Knopf-Properties nicht.

## 1.3 Zwei weitere belegte Fehler im Ist-Zustand

**B1 — Keine Kappung bei 22:00 beim Verlängern.** Die Tagesende-Prüfung steht nur in `btn5Std` und `btn9Std` (Z. 1226, 1245, 1311, 1330) sowie im toten Raumcode. Keiner der sechs Plus-Knöpfe prüft sie, und sie sind wiederholt klickbar. Aus 19:00–22:00 werden in vier Klicks 19:00 bis 10:00 des Folgetags. Diese Buchungen reichen über Mitternacht und werden von jeder Kollisionsprüfung übersehen, die über `Startzeit` eingrenzt.

**B2 — Ein fehlgeschlagener `Patch` zählt in der Serienbuchung als Erfolg.** Z. 2775–2792: Der `With`-Rückgabewert ist die Konstante `"gespeichert"`, unabhängig davon, ob der `Patch` darin durchlief. Ohne `IfError` kann die Erfolgszählung nicht stimmen.

**B3 — Die Kappungsmeldung verdeckt die Kollisionsmeldung.** Z. 2799–2807 prüft `effektivesBisRoh > effektivesBis` zuerst. Wurden gleichzeitig Termine wegen Kollision übersprungen, erfährt der Nutzer davon nichts.

**B4 — `dpWiederholenBis` hat kein `DefaultDate`** (Z. 2954) und steht damit auf heute. Wer ein künftiges Datum wählt und „Wiederholen" anhakt, ohne den Bis-Picker anzufassen, bekommt ein Enddatum **vor** dem Startdatum. `DateDiff + 1` wird negativ. Im heutigen Code führt das zu einer leeren Datumsliste und der Meldung „Bitte mindestens einen Wochentag auswählen" — die im Modus „Taeglich" nicht befolgbar ist, weil die Schalter dort unsichtbar sind.

---
---

# TEIL 2 — Warum acht Entwürfe gefallen sind

Vollständig in `VERWORFEN_SPEICHERN.md`. Hier die Kurzfassung, weil sie die Empfehlung trägt.

| Entwurf | Familie | Gescheitert an |
|---|---|---|
| 1A | Sammel-`Patch`, Teilerfolg | K2 — Meldung lügt in beide Richtungen; Kollisionsprüfung weist zu viel ab |
| 1B | Sammel-`Patch`, alles oder nichts | K2 + App bleibt nach jeder Fehlbedienung gesperrt |
| 1C | Absolute Zielzeit statt Delta | K2 fünffach; speichert in der Fassung gar nicht |
| 1D | Stornieren und neu anlegen | K1 strukturell — der Tisch ist zwischendurch nachweislich frei |
| 2A | Sammel-`Collect`, Teilerfolg | K2 — beschuldigt den Nutzer seiner eigenen Buchungen; Typkonflikt |
| 2B | `SerienID` + Nachprüfung und Rücknahme | K2 vierfach; kann gültige fremde Buchungen löschen |
| 2C | Alles oder nichts | K5/K6 — verweigert, ohne sagen zu können woran es liegt |
| 2D | Serie als ein Datensatz | K5 strukturell — macht 24 Leseabfragen undelegierbar |

**Was allen gemeinsam war:** Ein Dialog, der auf einer **unsichtbaren Menge** arbeitet und das Ergebnis als **Zahl** meldet. Der Nutzer sieht eine Buchung benannt, geändert werden andere. Er wählt eine Dauer, ohne zu sehen, was sie bei jeder einzelnen bewirkt. Am Ende liest er „N Buchungen geändert", wobei N aus einer lokalen Collection stammt und nicht aus dem, was SharePoint angenommen hat. Jede einzelne Falschmeldung der sechs Prüfberichte lässt sich darauf zurückführen.

**Was ich daraus gelernt habe, in drei Sätzen.** Erstens: Der Sammelaufruf war nie die Lösung, weil es das Problem, das er löst, gegen SharePoint nicht gibt — und weil ich das nicht geprüft hatte, bevor ich darauf aufgebaut habe, waren alle sechs Zugriffszahlen in meiner Rohfassung falsch. Zweitens: Eine Sammeloperation ist nur so ehrlich wie ihre Rückmeldung, und eine Rückmeldung aus einer lokalen Collection weiß nichts darüber, was der Server angenommen hat — deshalb scheiterten fünf von sechs Entwürfen an derselben Stelle, obwohl sie technisch sehr verschieden waren. Drittens: In einer App ohne Transaktionen ist eine Operation, die weniger ändert, fast immer besser als eine, die mehr auf einmal ändert und dafür mehr erklären muss.

---
---

# TEIL 3 — Die fünf Korrekturen

Deutsche Locale: `;` trennt Argumente, `;;` verkettet. Die `ORIGINAL`-Zitate stammen aus dem YAML-Export und stehen deshalb mit Komma.

---

## K1 — Die Dauer-Knöpfe lesen die richtige Buchung

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 3556
**Steuerelement:** `Screen1.conBuchungen.galAlleTischbuchungen.btnVerwalten_2`
**Property:** `OnSelect`

**ORIGINAL:**
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

**NEU:**
```
If(
    varAuswahlModusAktiv;
    Set(varGeklickteBuchungKlein; ThisItem);;
    Set(varZeigeVerwaltenKlein; true);
    Set(varSelectedBuchungTab; ThisItem);;
    Set(varSelectedBuchung; ThisItem);;
    Set(varZeigeVerwaltenTab; true);;
    Set(varZeigeCheckin; false);;
    Set(varZeigeDetails; false);;
    Set(varZeigeDialog; false)
)
```

**WARUM:** Eine einzige zusätzliche Zeile bringt alle zwölf Dauer-Knopf-Properties dazu, die Buchung zu bewerten, die auch gespeichert wird — Befund B0 ist damit geschlossen, ohne zwölf Formeln anzufassen.

**TEST:** Im Dashboard eine Buchung verwalten und den Dialog schließen. Dann in den Buchungen-Tab wechseln und eine **andere** Buchung verwalten. Die Plus- und Minus-Knöpfe müssen jetzt zu dieser Buchung passen — vorher trugen sie die Freigaben der zuerst geöffneten.

**RISIKO:** niedrig — `ThisItem` ist hier ein `Tischbuchungen`-Datensatz, derselbe Typ, den `varSelectedBuchung` überall sonst trägt. Keine Typvermischung.

---

## K2 — Verlängern prüft, bevor es schreibt

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 3690
**Steuerelement:** `Screen1.conBuchungen.conVerwaltenDialog_1.btnVerlängern_1`
**Property:** `OnSelect`

**ORIGINAL:**
```
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

**NEU:**
```
With(
    { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID) };
    If(
        IsBlank(varAusgewaehltePlusDauer);
        Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
        IsBlank(aktuelleBuchung);
        Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);
        With(
            {
                neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes);
                tagesEnde: aktuelleBuchung.Startzeit - Time(Hour(aktuelleBuchung.Startzeit); Minute(aktuelleBuchung.Startzeit); Second(aktuelleBuchung.Startzeit)) + Time(22; 0; 0)
            };
            If(
                neueEndzeit <= aktuelleBuchung.Startzeit;
                Notify("Die Buchung wäre danach leer. Bitte eine kürzere Verkürzung wählen."; NotificationType.Warning);
                neueEndzeit > tagesEnde;
                Notify("Über 22:00 Uhr hinaus kann nicht verlängert werden."; NotificationType.Warning);
                CountRows(
                    Filter(
                        Tischbuchungen;
                        Tisch.Value = aktuelleBuchung.Tisch.Value &&
                        ID <> aktuelleBuchung.ID &&
                        Startzeit < neueEndzeit &&
                        Endzeit > aktuelleBuchung.Startzeit
                    )
                ) > 0;
                Notify("Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen."; NotificationType.Warning);
                IfError(
                    Patch(Tischbuchungen; aktuelleBuchung; { Endzeit: neueEndzeit });
                    Notify("Speichern fehlgeschlagen. Die Liste wird aktualisiert, bitte prüfen."; NotificationType.Error);
                    Notify("Buchung geändert, neues Ende " & Text(neueEndzeit; "hh:mm") & " Uhr."; NotificationType.Success);;
                    Set(varZeigeVerwaltenTab; false)
                )
            )
        )
    )
);;
Refresh(Tischbuchungen);;
Set(varAusgewaehltePlusDauer; Blank())
```

**WARUM:** Heute ist die Knopffarbe die einzige Kollisionsprüfung dieses Wegs, und sie wertet beim Rendern aus — zwischen Anzeige und Klick kann beliebig viel Zeit liegen. Diese Fassung prüft unmittelbar vor dem Schreiben gegen frische Serverdaten, kappt bei 22:00 (Befund B1) und kann nicht mehr behaupten, gespeichert zu haben, wenn der `Patch` fehlschlug.

**TEST:** Der Zwei-Tab-Test aus der Kurzfassung. Zusätzlich: Eine Buchung 19:00–22:00 anlegen und „+1 Std" versuchen — erwartet wird „Über 22:00 Uhr hinaus kann nicht verlängert werden", vorher ging das durch.

**RISIKO:** mittel — mehrarmiges `If` (`If(bed1; erg1; bed2; erg2; …; standard)`) ist gültiges Power Fx, in dieser App bisher aber nicht verwendet. Falls das Studio es ablehnt, lässt es sich in verschachtelte zweiarmige `If` auflösen, ohne die Logik zu ändern.

**Bewusst entfernt:** `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus; false)`. Beide gehören nicht hierher — der Knopf ändert eine einzelne Buchung, und `varMehrfachAuswahlModus` wird nirgends gelesen (siehe `OFFENE_FUNDE.md`, F2).

---

## K3 — Dasselbe im Grundriss-Dialog

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 3244
**Steuerelement:** `Screen1.conVerwaltenDialog.btnVerlängern`
**Property:** `OnSelect`

**ORIGINAL:**
```
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

**NEU:** Wortgleich zu K2, mit drei Ersetzungen: `varSelectedBuchungTab` → `varSelectedBuchung`, `Set(varZeigeVerwaltenTab; false)` → `Set(varZeigeVerwalten; false)`. Die Schlusszeilen lauten hier:
```
);;
Refresh(Tischbuchungen);;
Set(varAusgewaehltePlusDauer; Blank())
```

**WARUM:** Derselbe Weg, dieselbe Lücke. Dieser Knopf hat heute nicht einmal ein `Refresh`.

**TEST:** Wie K2, aber über den Grundriss: belegten Tisch anklicken, verwalten, verlängern.

**RISIKO:** mittel — gleiche Begründung wie K2. **Prüfe nach dem Einfügen jede der drei Ersetzungen einzeln nach**; genau dieses Kopieren zwischen den beiden Dialogen hat Befund B0 erzeugt.

---

## K4 — Die Serienbuchung wird ehrlich

Vier Eingriffe in `btnSpeichern.OnSelect` (Zeile 2727). Die Struktur bleibt wie sie ist — die `ForAll` bleibt, weil ihre Beseitigung nach Ü5 keine Aufrufe spart.

**Datei:** `./src/Src/Screen1.pa.yaml`
**Steuerelement:** `Screen1.conBuchungDialog.btnSpeichern`
**Property:** `OnSelect`

### K4.1 — Die Kollisionsabfrage bekommt eine Zeitgrenze

**ORIGINAL** (Zeile 2734, eine Zeile im äußeren `With`):
```
bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)
```

**NEU:**
```
bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel && Endzeit > dpDatum.SelectedDate && Startzeit < DateAdd(dpDatum.SelectedDate; 16; TimeUnit.Days))
```

**WARUM:** Heute holt diese Zeile alle Buchungen dieses Tisches, die je existiert haben. 16 Tage liegen sicher über der 14-Tage-Kappung. **Die Untergrenze prüft `Endzeit`, nicht `Startzeit`** — sonst würde eine Buchung übersehen, die am Vortag beginnt und in den Zeitraum hineinreicht, und die gibt es wegen Befund B1 tatsächlich.

### K4.2 — Das Enddatum kann nicht mehr vor dem Startdatum liegen

**ORIGINAL** (Zeile 2733):
```
effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate, dpWiederholenBis.SelectedDate, dpDatum.SelectedDate)
```

**NEU:**
```
effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate > dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate)
```

**WARUM:** `<>` wird zu `>`. Damit ist Befund B4 geschlossen: Ein Bis-Datum vor dem Startdatum wird ignoriert statt eine negative Datumsliste zu erzeugen.

### K4.3 — Ein fehlgeschlagener Schreibvorgang zählt nicht mehr als Erfolg

**ORIGINAL** (Zeilen 2775–2794):
```
With(
  {
    neuerEintrag: Patch(Tischbuchungen, Defaults(Tischbuchungen), {
      Tisch: {Id: varSelectedTisch.ID, Value: varSelectedTisch.Titel},
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
```

**NEU:**
```
IfError(
    Patch(Tischbuchungen; Defaults(Tischbuchungen); {
        Tisch: {Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel};
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
    });
    "fehler";
    "gespeichert"
);
"übersprungen"
```

**WARUM:** Befund B2. Das `With` mit der Konstanten `"gespeichert"` weiß nichts über den Ausgang des `Patch`. `IfError` liefert `"fehler"`, wenn er fehlschlug. **`Defaults(Tischbuchungen)` bleibt stehen** — es liefert die typisierte Satzstruktur mit, und genau deshalb funktioniert das Personenfeld hier ohne `'@odata.type'`.

### K4.4 — Eine Meldung, die alles sagt

**ORIGINAL** (Zeilen 2797–2808):
```
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
```

**NEU:**
```
With(
    {
        anzahlGespeichert: CountRows(Filter(ergebnisse; Value = "gespeichert"));
        anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen"));
        anzahlFehler: CountRows(Filter(ergebnisse; Value = "fehler"))
    };
    Notify(
        anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
        If(anzahlUebersprungen > 0; " " & anzahlUebersprungen & " waren bereits belegt."; "") &
        If(anzahlFehler > 0; " " & anzahlFehler & " konnten nicht gespeichert werden, bitte die Liste prüfen."; "") &
        If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
        If(
            anzahlFehler > 0;
            NotificationType.Error;
            If(
                anzahlUebersprungen > 0 || effektivesBisRoh > effektivesBis;
                NotificationType.Warning;
                NotificationType.Success
            )
        )
    )
)
```

**WARUM:** Befund B3. Heute schlägt die Kappungsmeldung die Kollisionsmeldung, und Schreibfehler kommen gar nicht vor. Diese Fassung nennt alle drei Tatsachen in einer Meldung und wählt die Dringlichkeit nach dem schlimmsten eingetretenen Fall.

### K4.5 — Dasselbe am zweiten Knopf

`btnSpeichernTischePanel.OnSelect` (Zeile 959) enthält denselben Code. Ersetzungen für alle vier Eingriffe:

| im Dialog | im Panel |
|---|---|
| `dpDatum` | `dpDatumTischePanel` |
| `ddStart` | `ddStartTischePanel` |
| `ddEnde` | `ddEndTischePanel` |
| `dpWiederholenBis` | `dpWiederholenBis_1` |
| `varSelectedTisch.ID` | `ddTischePanel.Selected.ID` |
| `varSelectedTisch.Titel` | `ddTischePanel.Selected.Titel` |

**Die beiden Knöpfe sind nur im Rechenteil wortgleich, nicht im Aufräumteil** — der Dialog hat dort 12 Anweisungen, das Panel 23. **Fass den Aufräumteil nicht an**, alle vier Eingriffe liegen davor.

**TEST für K4:** Eine Serie über vier Tage auf einen Tisch legen, an dem an Tag 2 schon jemand sitzt, und als Bis-Datum einen Tag in vier Wochen wählen.
→ Erwartet: eine einzige gelbe Meldung, die **beides** nennt — „3 von 3 Terminen gespeichert. 1 waren bereits belegt. Die Wiederholung wurde auf 2 Wochen begrenzt." Vorher kam nur die Kappungsmeldung.
→ Danach: Ein künftiges Datum wählen, „Wiederholen" anhaken, das Bis-Datum **nicht** anfassen, speichern. Erwartet: eine Buchung wird angelegt. Vorher kam „Bitte mindestens einen Wochentag auswählen".

**RISIKO K4:** mittel — vier Eingriffe an zwei Knöpfen, also acht Stellen. Jeden einzeln einfügen und zwischendurch speichern. K4.1 und K4.2 ändern je eine Zeile, K4.3 und K4.4 je einen Block.

---

## K5 — Doppelklick-Riegel

Vier Knöpfe, je eine **neue** Property `DisplayMode`:

| Steuerelement | Zeile |
|---|---|
| `conBuchungDialog.btnSpeichern` | 2716 |
| `conTischBuchungenPanel.btnSpeichernTischePanel` | 948 |
| `conBuchungen.conVerwaltenDialog_1.btnVerlängern_1` | 3679 |
| `conVerwaltenDialog.btnVerlängern` | 3233 |

**NEU, bei allen vieren gleich:**
```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**WARUM:** Keiner dieser Knöpfe hat heute eine `DisplayMode`-Eigenschaft. Der einzige Schutz gegen den zweiten Klick ist `conLadeOverlay`, und das ist eine Grafik, kein Riegel — zwischen `Set(varIsLoading; true)` und dem nächsten Schritt garantiert Power Apps kein Neuzeichnen. Weil Verlängern ein relatives Delta ist, macht jeder durchkommende Zweitklick aus „+1 Std" ein „+2 Std".

**Achtung:** `btnVerlängern_1` und `btnVerlängern` setzen `varIsLoading` heute gar nicht. Ergänze dort als erste Anweisung `Set(varIsLoading; true);;` und als letzte `Set(varIsLoading; false)` — in K2 und K3 ist das noch nicht enthalten, damit die Blöcke einzeln testbar bleiben.

**TEST:** Eine Buchung verlängern und dabei zweimal schnell auf „Speichern" klicken. Erwartet: eine Meldung, eine Stunde mehr. Vorher: zwei Meldungen, zwei Stunden.

**RISIKO:** niedrig

---
---

# TEIL 4 — Empfehlung

**Nimm K1 bis K5 und baue das Mehrfach-Speichern vorerst nicht.**

Was dafür spricht, ist nicht, dass die Funktion unwichtig wäre, sondern dass acht Entwurfsfamilien an denselben zwei Ausschlusskriterien gescheitert sind — und zwar nicht an Formeldetails, sondern an der Form: Ein Dialog, der auf einer unsichtbaren Menge arbeitet und sein Ergebnis als Zahl meldet, kann nicht ehrlich sein. Jeder künftige Anlauf muss die betroffene Menge **zeigen** statt sie zu zählen und das Ergebnis **pro Zeile** feststellen statt es aus einer lokalen Collection abzuleiten. Das ist keine Formel mehr, das ist eine Galerie mit Vorschau und Zeilenstatus — eine halbe Tagesarbeit, die zehn Tage vor dem Produktivgang nicht hineingehört.

**Was der unterlegene Weg besser kann, und das ist nicht wenig:** Ein funktionierendes Mehrfach-Verlängern spart dem Nutzer echte Klicks. Wer fünf Buchungen um eine Stunde verlängern will, klickt heute fünfmal durch den Dialog. Die Korrekturen K1 bis K5 ändern daran nichts — sie machen das Durchklicken nur korrekt statt gefährlich. Wenn die Mehrfachauswahl in der Praxis oft gebraucht wird, ist das ein echter Verlust, und dann lohnt sich die Vorschau-Galerie nach dem Produktivgang.

**Der Preis dieser Entscheidung:** Du gehst mit einer Oberfläche live, die im Auswahlmodus nur Stornieren anbietet, obwohl der Verwalten-Knopf mehr verspricht. Das ist unschön, aber es lügt nicht. Umgekehrt gingst du mit einer Sammelfunktion live, von der sechs unabhängige Prüfer gesagt haben, dass sie Erfolgsmeldungen für Dinge ausgibt, die nicht passiert sind.

**Und miss.** Wenn Ü5 stimmt, ist die Geschwindigkeitsarbeit an den Schreibpfaden erledigt, bevor sie angefangen hat — dann liegt der nächste echte Gewinn bei den 96 bis 108 `LookUp`-Auswertungen pro Grundriss-Render, nicht hier.

---
---

# TEIL 5 — UNSICHER

Pro Punkt steht, was ich versucht habe, ihn aufzulösen.

**U1 — Zerfällt eine Tabellen-Operation gegen SharePoint wirklich in einen Aufruf je Zeile?** ⏱ *nicht in 30 Sekunden klärbar — messen*
Versucht: Quellcode, `DataSources.json` und `AppCheckerResult.sarif` durchsucht; keine Aussage darüber. Drei Prüfer kommen unabhängig zum selben Schluss, aber alle drei durch Schlussfolgerung, nicht durch Messung. **Das ist die wichtigste offene Frage des Projekts**, weil die Antwort darüber entscheidet, ob Schreibpfad-Umbauten überhaupt Geschwindigkeit bringen. Zu klären mit der Stoppuhr: Serienbuchung über 1, 5 und 14 Tage, dreimal je Größe.

**U2 — Nimmt das Studio das mehrarmige `If` an?** ⏱ *30 Sekunden*
Versucht: Im gesamten Quellcode kommt die Form `If(bed1; erg1; bed2; erg2; …)` nicht vor, nur zweiarmige und verschachtelte. Sie ist gültiges Power Fx, aber diese App läuft mit `powerfxv1 = False`. **Einfach K2 einfügen und schauen, ob die Zeile rot unterstrichen wird.** Falls ja: in verschachtelte zweiarmige `If` auflösen, die Logik bleibt gleich.

**U3 — Delegiert `Filter(Tischbuchungen; Tisch.Value = …)` in K2 und K3?** ⏱ *30 Sekunden*
Versucht: Die App-Prüfung meldet `Tisch.Value` zehnmal als `OpNotSupportedByColumn`, aber nie in einer Galerie-Vorlage. Die neue Abfrage in K2 holt im schlimmsten Fall alle Buchungen dieses einen Tisches — bei 34 Tischen und rund 340 künftigen Buchungen etwa zehn Zeilen. Unkritisch, aber **schau nach, ob neben der Formel ein gelbes Warndreieck erscheint.**

**U4 — Stimmt die Zahl 16 in K4.1?** ⏱ *30 Sekunden*
Versucht: Die Kappung steht als `Min(effektivesBisRoh; dpDatum.SelectedDate + 14)` im Code, die Serie umfasst also höchstens Tag 0 bis Tag 14, das sind 15 Tage. 16 lässt einen Tag Luft. **Falls du die Kappung je änderst, muss diese Zahl mitwandern** — das ist die einzige Stelle in K1 bis K5, an der zwei Zahlen zusammenpassen müssen.

**U5 — Wofür war `SerienID` gedacht?** ⏱ *30 Sekunden*
Versucht: Null Treffer im gesamten Quellcode, in keiner Notiz erwähnt. **Ich habe sie in K1 bis K5 bewusst nicht angefasst**, obwohl die Aufgabe mich dazu anhält — alle Entwürfe, die sie benutzt hätten, sind gefallen, und in eine Spalte zu schreiben, deren Zweck niemand kennt, ohne dass ein überlebender Entwurf davon profitiert, ist unnötiges Risiko. Sie bleibt die richtige Zutat für ein späteres „ganze Serie verwalten".

**U6 — Gibt es außer dem Aufräum-Flow noch etwas, das in `Tischbuchungen` schreibt?** ⏱ *30 Sekunden*
Versucht: Aus dem Quellcode nicht feststellbar, dort steht nur die App. Relevant für K2 und K3: Die Kollisionsprüfung unmittelbar vor dem `Patch` verkleinert das Zeitfenster, schließt es aber nicht. Gibt es weitere Schreiber, ist das Fenster häufiger belegt als gedacht.

**U7 — Wie oft wird die Mehrfachauswahl tatsächlich benutzt?** ⏱ *weißt du selbst*
Versucht: Nicht aus dem Code ableitbar. Davon hängt ab, wie teuer die Empfehlung in Teil 4 wirklich ist. Wenn fast niemand mehr als zwei Buchungen auf einmal anfasst, kostet sie nichts.
