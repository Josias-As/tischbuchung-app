# AUFGABE_UMBAU.md

> **Nicht Teil des nächtlichen Laufs.** Diese Datei liegt im Arbeitsordner bereit und wird erst bearbeitet, wenn `INVENTAR.md` fertig ist und Josias sie ausdrücklich anfordert.

## Was du produzierst

Eine Datei `UMBAU.md`. Sie enthält für **jede** unten genannte Änderung einen Block in genau dieser Form:

```
### <Nummer>.<Buchstabe> — <kurze Bezeichnung>
Datei:           <Pfad in ./src>
Steuerelement:   <Name>
Property:        <Name>
ORIGINAL:
<vollständige aktuelle Formel, unverändert>
NEU:
<vollständige neue Formel, direkt kopierbar>
WARUM:           <ein Satz>
TEST:            <was Josias nach dem Einfügen prüft>
RISIKO:          <niedrig | mittel | hoch> — <ein Satz, falls nicht niedrig>
```

**Alles aus dem echten Quellcode in `./src`.** Wenn Quellcode und Notizen sich widersprechen, gilt der Quellcode, und du schreibst den Widerspruch hin.

**Wo du unsicher bist, schreibst du das hin statt zu raten.** Ein Block mit `UNSICHER: <Frage>` ist tausendmal besser als eine erfundene Formel. Eine falsche Formel kostet eine halbe Stunde Fehlersuche.

**Reihenfolge einhalten.** Die Blöcke stehen in der Reihenfolge, in der sie eingefügt werden sollen. Abhängigkeiten zuerst.

---

## Harte Regeln für jede Formel

- **Deutsche Locale:** `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet.
- **Niemals Kommentare in Power Fx.** Erklärungen gehören ins Feld WARUM.
- **Keine Platzhalter.** Jede Formel muss so einfügbar sein, wie sie dasteht.
- **`With()`-Felder werden gleichzeitig ausgewertet.** Abhängige Werte brauchen verschachtelte `With`.
- **Lookup-Feld:** immer `{Id: ...; Value: ...}`. **Personenfeld:** immer volles Schema (siehe `KONTEXT.md`).
- **Kein eigener `TimeZoneOffset`-Workaround.**
- **`Patch` immer auf frischem `LookUp(...; ID = ...)`**, nie direkt auf eine Variable.
- **Named Formulas können keine `Set()`-Variablen referenzieren** und keine Verhaltensfunktionen enthalten. Jede Definition endet mit `;`.
- Interner Spaltenname ist **`Title`**, nie `Titel`.

---

## 1 — Delegation und zentrale Datenbasis

Der wichtigste Block. Ziel: Der Server filtert, nicht der Client.

**1.a — Datumsvariablen.** Finde jede Stelle, an der `varAnsichtsDatum` gesetzt wird. Ergänze dort:
```
Set(varTagStart; varAnsichtsDatum);;
Set(varTagEnde; DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
```
Gib die vollständige neue Formel jeder betroffenen Stelle, nicht nur die Ergänzung.

**1.b — Tages-Collection.**
```
ClearCollect(colBuchungenTag;
    Filter(Tischbuchungen; Startzeit >= varTagStart && Startzeit < varTagEnde))
```
Schlag vor, wo genau das hingehört, und begründe es.

Hintergrund: Ein Vergleich Datumsspalte gegen **Variable** ist delegierbar, `Today()`/`Now()` direkt in der Formel nicht.

**1.c — Master-Bedingung umstellen.** Für **jede** in `INVENTAR.md` gefundene Fundstelle ein eigener Block. `LookUp(Tischbuchungen; …)` wird zu `LookUp(colBuchungenTag; …)`, Bedingung inhaltlich gleich.

Ein Block pro Fundstelle, keine Sammelanweisung — es wird einzeln umgestellt und dazwischen getestet.

**1.d — Aktualisierungspunkte.** Liste **alle** Stellen, an denen `colBuchungenTag` neu aufgebaut werden muss: App-Start, Datumswechsel, Stockwerkwechsel, nach jedem erfolgreichen Schreibvorgang, beim Öffnen des Buchungen-Tabs. Prüfe im Quellcode, wo diese Ereignisse liegen, und gib pro Stelle die vollständige neue Formel.

Das ist der gefährlichste Teil: Eine Collection, die nicht nachgezogen wird, zeigt **falsche Daten schnell** — schlimmer als richtige Daten langsam. Sei hier vollständig.

---

## 2 — Schreibpfad

**2.a — `Refresh` aus Schleifen.** Für jede gefundene `Refresh`-Stelle innerhalb einer `ForAll`: die korrigierte Formel. Genau ein `Refresh` am Ende des Vorgangs.

**2.b — Mehrfachauswahl Stornieren.** `Remove` nimmt eine **Tabelle**: ein Aufruf statt N.

**2.c — Mehrfachauswahl Speichern.** Analog. **Neu anlegen** → `Collect(Tischbuchungen; colNeue)`. **Ändern** → `Patch(Tischbuchungen; colAenderungen)` mit `ID`-Spalte.

**2.d — Serienbuchung.** Datensätze erst lokal aufbauen, dann **ein** `Collect`.

**2.e — `IfError` überall.** Um jede `Patch`-, `Collect`-, `Remove`- und `RemoveIf`-Operation, mit deutscher `Notify`-Meldung. Beim Stornieren zusätzlich vorher prüfen, ob der Datensatz noch existiert.

---

## 3 — Korrektheit

**3.a — Doppelbuchung.** Nach erfolgreichem Anlegen sofort erneut prüfen, ob eine Überschneidung existiert; bei Kollision die eigene neue Buchung zurücknehmen plus verständliche Meldung. Mindestens für die Einzelbuchung.

**3.b — Check-in-Spaltenname.** Aus `INVENTAR.md` ist bekannt, ob `CheckedIn` oder `Checkedin` gilt. Falls gemischt: alle Stellen mit korrigierter Formel. **Falls unklar, `UNSICHER` schreiben** — ein falscher Feldname wird still ignoriert.

**3.c — Verlängern-Buttons.** Laut Notizen wurde nur `btnPlus3Std` auf die Vollzeitraum-Kollisionsprüfung korrigiert. Prüfe das. Korrekte Bedingung pro Button mit eigenem Offset:
```
Startzeit < DateAdd(aktuelleEndzeit; <60|120|180>; TimeUnit.Minutes) && Endzeit > aktuelleEndzeit
```
Prüfe **jede** Property jedes Buttons auf die richtige Offset-Zahl, nicht nur `Fill`.

---

## 4 — Ballast

**4.a — Löschliste.** Alle toten Raum-Steuerelemente und -Variablen plus `varZoom`, `varPanX`, `varPanY`. Gib eine **Reihenfolge**, in der gefahrlos gelöscht werden kann, und markiere alles noch Referenzierte als „erst prüfen".

**4.b — Bereinigtes `App.OnStart`.** Die vollständige neue Fassung zum Ersetzen. Achte auf die `;;` zwischen den Zeilen.

**4.c — Spinner.** Schlag eine Lösung für den Bug „Ladesymbol doppelt" vor — oder sag, dass die Ursache nicht sicher bestimmbar ist.

---

## 5 — Nur freie Tische im Dropdown

`ddTischePanel.Items` soll nur im gewählten Zeitfenster freie Tische zeigen. Richtung: **Zeit → Tisch**. Das löst den bekannten Zirkelverweis.

```
Filter(Tische As T;
    T.Aktiv &&
    T.Standort = varAusgewaehltesStockwerk &&
    CountRows(Filter(colBuchungenTag;
        Tisch.Value = T.Title && Startzeit < <neuEnde> && Endzeit > <neuStart>)) = 0)
```

Das `As T` ist nötig, sonst ist `Title` im inneren `Filter` mehrdeutig. Setze `<neuStart>`/`<neuEnde>` gegen die echten Steuerelemente aus `./src` ein. Ergänze eine verständliche Anzeige für den Fall, dass kein Tisch frei ist.

---

## Zum Schluss in UMBAU.md

**Reihenfolgenliste:** nummeriert, in Einfügereihenfolge, mit geschätzter Dauer pro Block.

**Offene Fragen:** alles mit `UNSICHER` markierte, gesammelt an einer Stelle.

**Kritisches Fazit, max. 10 Sätze:** Was hat im Quellcode am meisten überrascht? Wo ist das größte Problem, das in dieser Aufgabenliste **nicht** vorkommt? Keine Beschönigung.
