# OFFENE_FUNDE.md — gefunden, noch nicht eingeplant

Kleinfunde aus dem Quellcode, die in keinem der drei Ergebnisdokumente stehen und noch keiner Umbaustufe zugeordnet sind. **Keine Priorität gesetzt.**

**Stand: 03.10.2026**

---

## F1 — `Label14` liest den falschen Datumswähler

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 1187–1208
**Steuerelement:** `Screen1.conTischBuchungenPanel.Label14`
**Properties:** `Color` (Z. 1191–1196) und `Text` (Z. 1199–1204)

Beide Formeln lauten im Kern:
```
DateDiff(dpDatum.SelectedDate, dpWiederholenBis_1.SelectedDate, TimeUnit.Days) > 14
```

`Label14` sitzt in `conTischBuchungenPanel`. Dort heißt der Datumswähler **`dpDatumTischePanel`**. `dpDatum` gehört zu `conBuchungDialog`, einem völlig anderen Dialog.

**Folge:** Der Warnhinweis „Zu weit gewählt — es werden 2 Wochen gespeichert" vergleicht das Enddatum aus dem Panel gegen das Startdatum aus dem Grundriss-Dialog. Er erscheint also zum falschen Zeitpunkt oder gar nicht. Die tatsächliche Begrenzung im Speichern-Knopf rechnet richtig (`Min(effektivesBisRoh, dpDatumTischePanel.SelectedDate + 14)`), nur die Anzeige lügt.

**Gegenstück:** `conBuchungDialog.Label12` (Z. 2595–2616) hat dieselbe Formel und liest dort korrekt `dpDatum` und `dpWiederholenBis`. Das ist die Vorlage, aus der `Label14` kopiert wurde — beim Kopieren wurde `dpWiederholenBis` auf `dpWiederholenBis_1` angepasst, `dpDatum` aber nicht.

**Vermutete Korrektur** (nicht getestet, gehört in einen eigenen Block):
`dpDatum.SelectedDate` → `dpDatumTischePanel.SelectedDate`, in **beiden** Properties.

---

## F2 — `btnVerlängern_1` fasst die Mehrfachauswahl an, obwohl er einzeln arbeitet

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 3679–3712
**Steuerelement:** `Screen1.conBuchungen.conVerwaltenDialog_1.btnVerlängern_1`
**Property:** `OnSelect`, Zeilen 3702–3703

```
Clear(colAusgewaehlteBuchungen);
Set(varMehrfachAuswahlModus, false)
```

Der Knopf trägt die Beschriftung „Speichern" und verlängert genau eine Buchung (`varSelectedBuchungTab`). Er leert trotzdem die Mehrfachauswahl mit und setzt `varMehrfachAuswahlModus`.

Zwei Probleme:
- `varMehrfachAuswahlModus` wird **nirgends gelesen** — die echte Variable ist `varAuswahlModusAktiv`. Das ist die einzige Fundstelle außerhalb von `App.OnStart`. Von der App-Prüfung als `app-UnusedVariables` gemeldet.
- `Clear(colAusgewaehlteBuchungen)` verwirft eine Auswahl, die der Nutzer möglicherweise noch braucht. Da `btnVerwalten_2.OnSelect` im Auswahlmodus aber gar nicht in diesen Dialog führt (sondern in `conVerwaltenKlein`), ist der Fall praktisch unerreichbar. Reste einer früheren Fassung.

**Beide Zeilen sind ersatzlos streichbar**, sobald geprüft ist, dass `conVerwaltenDialog_1` im Auswahlmodus wirklich nie sichtbar wird.

---

## F3 — Leere `PressedFill`-Properties

**Datei:** `./src/Src/Screen1.pa.yaml`

| Steuerelement | Zeile |
|---|---|
| `conVerwaltenDialog.btnStornieren` | 3228 |
| `conBuchungen.conVerwaltenDialog_1.btnStornieren_1` | 3674 |
| `conBuchungen.conVerwaltenDialog_1.btnVerlängern_1` | 3708 |
| `conDashboard.btnRaumHinzufügen` | 701 |
| `conDashboard.btnTischHinzufügen` | 746 |
| `conHeader.btnTabDashboard` | 4222 |
| `conHeader.btnTabBuchungen` | 4248 |

Alle stehen als `PressedFill: =` ohne Wert. Keine funktionale Auswirkung — Power Apps fällt auf den Standard zurück. Nur Kosmetik, der Vollständigkeit halber festgehalten. Fällt beim Aufräumen in Schritt 5 ohnehin mit auf.
