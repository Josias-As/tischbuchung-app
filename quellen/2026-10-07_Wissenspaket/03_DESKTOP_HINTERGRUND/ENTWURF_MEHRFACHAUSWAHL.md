# ENTWURF_MEHRFACHAUSWAHL.md — Speichern und Stornieren mit Mehrfachauswahl

**Erstellt:** 01.10.2026
**Grundlage:** `INVENTAR.md` Abschnitt 8, Quellcode `./src/Src/Screen1.pa.yaml`
**Verwurfsprotokoll:** `VERWORFEN.md` — vier verworfene Familien, zwei Überlebende

> **Schreibweise:** Alle `ORIGINAL`-Zitate stammen wortgetreu aus dem YAML-Export und stehen deshalb in invarianter Locale, also mit **Komma**. Alle `NEU`-Formeln sind für dein deutsches Studio geschrieben, also mit **Semikolon** als Argumenttrenner und **`;;`** als Anweisungsverkettung. Keine Kommentare, keine Platzhalter.

---

## Vorbemerkung: ein Teil der Aufgabe entfällt

`AUFGABE_UMBAU.md` Punkt 2.c verlangt ein „Mehrfachauswahl Speichern". **Das gibt es im Quellcode nicht.** Die Mehrfachauswahl kennt genau eine Sammelaktion: Stornieren. Der Knopf, der im Mehrfach-Dialog „Speichern" heißt (`btnVerlängern_1`, Zeile 3679), gehört zu `conVerwaltenDialog_1`, arbeitet auf der einzelnen Buchung `varSelectedBuchungTab` und leert danach nur beiläufig `colAusgewaehlteBuchungen` mit.

Dieses Dokument behandelt deshalb ausschließlich das **Mehrfach-Stornieren**. Das ist nach Kriterium 1 ohnehin der teuerste Vorgang der App.

---

# 1. Nullpunkt

## Die heutige Formel

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 4074–4087
**Steuerelement:** `Screen1.conBuchungen.conVerwaltenKlein.btnStornierenKlein`
**Property:** `OnSelect`

```
=Set(varIsLoading, true);
If(
  CountRows(colAusgewaehlteBuchungen) = 0,
  Notify("Keine Buchungen ausgewählt.", NotificationType.Warning),
  ForAll(colAusgewaehlteBuchungen, Remove(Tischbuchungen, ThisRecord));
  Refresh(Tischbuchungen);
  Notify("Buchungen storniert.", NotificationType.Success)
);
Clear(colAusgewaehlteBuchungen);
Set(varGeklickteBuchungKlein, Blank());
Set(varZeigeVerwaltenKlein, false);
Set(varAuswahlModusAktiv, false);
Set(varIsLoading, false); Reset(tglAuswahlModus)
```

Dazu gehören, weil sie die Menge füllen, die hier gelöscht wird:

**`Screen1.conBuchungen.galAlleTischbuchungen.chkAuswahl`**, Zeile 3574 ff.
```
Default: =!IsBlank(LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
OnCheck: =Collect(colAusgewaehlteBuchungen, ThisItem)
OnUncheck: =Remove(colAusgewaehlteBuchungen, LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
Visible: =varAuswahlModusAktiv
X: =btnVerwalten_2.X - btnVerwalten.Width - 10
```

**`Screen1.conBuchungen.chkAlleAuswählen`**, Zeile 4149 ff.
```
Default: =CountRows(colAusgewaehlteBuchungen) > 0 && CountRows(colAusgewaehlteBuchungen) = galAlleTischbuchungen.AllItemsCount
OnCheck: =ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)
OnUncheck: =Clear(colAusgewaehlteBuchungen)
Visible: =varAuswahlModusAktiv
```

**`Screen1.conBuchungen.galAlleTischbuchungen`**, Zeile 3452
```
Items: |-
  =With(
    { erzwingeNeuaufbau: varGalleryNeuAufbauen },
    SortByColumns(
      Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()),
      "Startzeit",
      SortOrder.Ascending
    )
  )
```

## Bewertung des Nullpunkts nach den sechs Kriterien

### Kriterium 1 — Datenquellen-Zugriffe

| Ausgewählte Buchungen | Zugriffe | Zusammensetzung |
|---|---|---|
| 1 | **2** | 1 × `Remove` + 1 × `Refresh` |
| 5 | **6** | 5 × `Remove` + 1 × `Refresh` |
| 20 | **21** | 20 × `Remove` + 1 × `Refresh` |
| 50 | **51** | 50 × `Remove` + 1 × `Refresh` |

**Wächst linear mit der Auswahl.** Jedes `Remove` innerhalb der `ForAll` ist ein eigener Aufruf; sie laufen nacheinander, nicht parallel. Microsofts App-Prüfung meldet genau diese Stelle als `app-ForAllWithMutation`.

Dazu kommt, was `Refresh` auslöst: `galAlleTischbuchungen.Items` wird neu abgefragt, und falls der Grundriss sichtbar ist, laufen dessen 96 bis 108 `LookUp`-Auswertungen erneut.

Die Zugriffe beim Auswählen selbst sind rein lokal (`Collect` in eine Collection) und kosten nichts — mit einer Ausnahme, siehe Kriterium 2.

### Kriterium 2 — Delegierbarkeit

`Remove` auf einem Datensatz ist keine Abfrage und löst keine Delegierungswarnung aus. Keine der 56 Warnungen aus `AppCheckerResult.sarif` betrifft diese Formel.

**Aber:** `chkAlleAuswählen.OnCheck` benutzt `galAlleTischbuchungen.AllItems`. `AllItems` enthält **nur die bereits in die Galerie geladenen Zeilen**, nicht alle Treffer der Abfrage. Eine Galerie lädt standardmäßig in Blöcken nach, während der Nutzer scrollt. „Alle auswählen" markiert also bei vielen Buchungen stillschweigend nur die geladenen — und `chkAlleAuswählen.Default` vergleicht danach mit `AllItemsCount`, das dieselbe Teilmenge zählt, sodass der Haken trotzdem als „alles markiert" erscheint. **Das ist ein eigenständiger Bug, unabhängig vom Löschvorgang.**

Zusätzlich ist `galAlleTischbuchungen.Items` mit `Person.Email = User().Email && Endzeit >= Now()` **ohne Datumsobergrenze** gefiltert. Ob `Person.Email` delegiert, ist in `INVENTAR.md` Abschnitt 3 als offene Frage markiert.

### Kriterium 3 — Verhalten bei Gleichzeitigkeit

**Hier liegt der gemeldete Bug 4.** `colAusgewaehlteBuchungen` ist eine lokale Kopie, die in dem Moment entstand, als der Nutzer den Haken setzte. `ThisRecord` in der `ForAll` ist diese Kopie. Zwischen Anhaken und Klick auf „Stornieren" kann beliebig viel Zeit liegen.

Ist eine Buchung inzwischen serverseitig weg — weil ein Kollege sie gelöscht hat, weil der nächtliche Aufräum-Flow lief, oder weil der Nutzer sie in einem zweiten Tab storniert hat — wirft `Remove` **„Item Not Found"** für einen Eintrag, den die Galerie noch anzeigt. Genau das gemeldete Symptom.

Verschärfend: Die Erfolgsmeldung `Notify("Buchungen storniert."; NotificationType.Success)` steht **unbedingt** hinter der Schleife. Sie erscheint auch dann, wenn jedes einzelne `Remove` fehlgeschlagen ist. Der Nutzer liest „storniert", und nichts ist storniert.

`UNSICHER:` Ob ein fehlgeschlagenes `Remove` die restlichen Durchläufe der `ForAll` abbricht oder ob sie weiterlaufen, kann ich aus dem Quellcode nicht belegen. Beide Fälle sind schlecht: entweder bleibt die Hälfte stehen, oder der Nutzer weiß nicht, welche Hälfte.

### Kriterium 4 — Wartungsfläche

Die Auswahllogik liegt an **fünf Stellen**, die konsistent gehalten werden müssen:
`chkAuswahl` (3 Properties), `chkAlleAuswählen` (3 Properties), `tglAuswahlModus.OnChange`, `btnStornierenKlein.OnSelect`, `btnSchließenKlein.OnSelect`. Dazu `btnVerlängern_1.OnSelect`, das `colAusgewaehlteBuchungen` ebenfalls leert, obwohl es keine Mehrfachoperation ist.

Das Aufräumen am Ende (`Clear`, `Set(…, Blank())`, `Set(…, false)`, `Reset`) steht **wortgleich doppelt** — in `btnStornierenKlein` und in `btnSchließenKlein`. Zwei Stellen, die auseinanderlaufen können.

Beleg für Formula Drift, der bereits eingetreten ist: `chkAuswahl.X` lautet `=btnVerwalten_2.X - btnVerwalten.Width - 10`. `btnVerwalten` ist der Knopf in `conDashboard.galTischbuchungenHeute`, nicht `btnVerwalten_2` in dieser Galerie. Fällt nur deshalb nicht auf, weil beide 50 breit sind.

### Kriterium 5 — Was der Nutzer bei einem Fehler sieht

Kein `IfError` — weder hier noch sonst irgendwo in der App (null Treffer im gesamten Quellcode). Bei einem Fehler erscheint die rohe Connector-Meldung samt `clientRequestId`, **und zusätzlich** die grüne Erfolgsmeldung.

### Kriterium 6 — Einfügeaufwand

Entfällt, das ist der Ist-Zustand.

### Zusammenfassung Nullpunkt

| Kriterium | Bewertung |
|---|---|
| 1 Zugriffe | **schlecht** — N+1, linear |
| 2 Delegierbarkeit | **mittel** — keine Warnung, aber `AllItems` ist unvollständig |
| 3 Gleichzeitigkeit | **schlecht** — Bug 4, plus falsche Erfolgsmeldung |
| 4 Wartungsfläche | **schlecht** — 5 Stellen, Doppelung, bereits ein Kopierfehler drin |
| 5 Fehleranzeige | **schlecht** — roher Connector-Fehler |
| 6 Einfügeaufwand | — |

**Jeder Entwurf muss diesen Nullpunkt bei Kriterium 1 deutlich schlagen, sonst fliegt er raus.**

---

# 2. Die Überlebenden

Sechs Familien wurden entworfen und angegriffen, vier sind verworfen (`VERWORFEN.md`). Es überleben zwei, aus deutlich verschiedenen Familien.

---

## Entwurf A — Sammelaufruf auf frisch aufgelöster Menge

### Die Idee in drei Sätzen

Vor dem Löschen liest die App einmal nach, welche der angehakten Buchungen es auf dem Server überhaupt noch gibt, und arbeitet ab da nur noch mit diesen frischen Datensätzen. Gelöscht wird dann mit einem einzigen `Remove(Tischbuchungen; <Tabelle>)` statt mit einer Schleife aus Einzellöschungen. Was zwischen Anhaken und Klick verschwunden ist, wird gar nicht erst angefasst — der Fehler „Item Not Found" kann damit nicht mehr entstehen, statt dass man ihn abfängt.

### A.1 — `btnStornierenKlein.OnSelect`

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 4074
**Steuerelement:** `Screen1.conBuchungen.conVerwaltenKlein.btnStornierenKlein`
**Property:** `OnSelect`

**ORIGINAL:**
```
=Set(varIsLoading, true);
If(
  CountRows(colAusgewaehlteBuchungen) = 0,
  Notify("Keine Buchungen ausgewählt.", NotificationType.Warning),
  ForAll(colAusgewaehlteBuchungen, Remove(Tischbuchungen, ThisRecord));
  Refresh(Tischbuchungen);
  Notify("Buchungen storniert.", NotificationType.Success)
);
Clear(colAusgewaehlteBuchungen);
Set(varGeklickteBuchungKlein, Blank());
Set(varZeigeVerwaltenKlein, false);
Set(varAuswahlModusAktiv, false);
Set(varIsLoading, false); Reset(tglAuswahlModus)
```

**NEU:**
```
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
Clear(colStornoFrisch);;
Clear(colStornoZiele);;
Clear(colAusgewaehlteBuchungen);;
Set(varGeklickteBuchungKlein; Blank());;
Set(varZeigeVerwaltenKlein; false);;
Set(varAuswahlModusAktiv; false);;
Reset(tglAuswahlModus);;
Set(varIsLoading; false)
```

**WARUM:** Ein Sammelaufruf statt N Einzelaufrufen, und die zu löschenden Datensätze stammen aus einem frischen Serverlesevorgang statt aus einer womöglich Minuten alten lokalen Kopie.

**TEST:** Zwei Buchungen anhaken, stornieren. Erwartung: Meldung „2 Buchungen storniert.", beide verschwinden, spürbar schneller als vorher. Dann der eigentliche Test — siehe Testschritte unten.

**RISIKO:** mittel — `Remove` mit einer Tabelle ist eine andere Aufrufform als bisher, und der Vorab-Lesevorgang hängt an derselben Filterbedingung wie `galAlleTischbuchungen.Items`.

### A.2 — `btnSchließenKlein.OnSelect` nachziehen

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 4106
**Steuerelement:** `Screen1.conBuchungen.conVerwaltenKlein.btnSchließenKlein`
**Property:** `OnSelect`

**ORIGINAL:**
```
=Set(varZeigeVerwaltenKlein, false);
Set(varGeklickteBuchungKlein, Blank());
Clear(colAusgewaehlteBuchungen);
Set(varAuswahlModusAktiv, false); Reset(tglAuswahlModus)
```

**NEU:**
```
Set(varZeigeVerwaltenKlein; false);;
Set(varGeklickteBuchungKlein; Blank());;
Clear(colAusgewaehlteBuchungen);;
Clear(colStornoFrisch);;
Clear(colStornoZiele);;
Set(varAuswahlModusAktiv; false);;
Reset(tglAuswahlModus)
```

**WARUM:** Die zwei neuen Hilfs-Collections müssen auch beim Abbrechen geleert werden, sonst bleiben veraltete Datensätze im Speicher der Sitzung liegen.

**TEST:** Auswahlmodus an, drei Haken setzen, „Schließen" klicken, Auswahlmodus erneut an. Erwartung: keine Haken gesetzt.

**RISIKO:** niedrig

### A.3 — „Alle auswählen" reparieren

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 4149
**Steuerelement:** `Screen1.conBuchungen.chkAlleAuswählen`
**Property:** `OnCheck`

**ORIGINAL:**
```
=ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)
```

**NEU:**
```
ClearCollect(
    colAusgewaehlteBuchungen;
    SortByColumns(
        Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now());
        "Startzeit";
        SortOrder.Ascending
    )
)
```

**WARUM:** `AllItems` enthält nur die bereits in die Galerie geladenen Zeilen, nicht alle Treffer — „Alle auswählen" markiert heute stillschweigend eine Teilmenge.

**TEST:** Mehr als 100 künftige eigene Buchungen anlegen (oder in der Galerie `galAlleTischbuchungen` die Eigenschaft für die Ladegröße nachsehen), ohne zu scrollen „Alle auswählen" klicken und `CountRows(colAusgewaehlteBuchungen)` prüfen. Erwartung: entspricht der Gesamtzahl, nicht der geladenen.

**RISIKO:** mittel — kostet einen zusätzlichen Lesevorgang beim Anhaken. Wenn du heute nie mehr als ein oder zwei Dutzend künftige Buchungen hast, kannst du diesen Block überspringen; dann bleibt der Fehler bestehen, tritt aber nicht auf.

`UNSICHER:` Die Standard-Ladegröße einer Galerie steht nicht im Quellcode. Wenn du weißt, dass die Liste nie lang wird, ist A.3 verzichtbar.

### A.4 — Kopierfehler in `chkAuswahl.X`

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 3589
**Steuerelement:** `Screen1.conBuchungen.galAlleTischbuchungen.chkAuswahl`
**Property:** `X`

**ORIGINAL:**
```
=btnVerwalten_2.X - btnVerwalten.Width - 10
```

**NEU:**
```
btnVerwalten_2.X - btnVerwalten_2.Width - 10
```

**WARUM:** `btnVerwalten` liegt in `conDashboard.galTischbuchungenHeute`, nicht in dieser Galerie; die Formel funktioniert nur zufällig, weil beide Knöpfe 50 breit sind.

**TEST:** Auswahlmodus an. Erwartung: Der Haken sitzt unverändert links neben dem Verwalten-Knopf.

**RISIKO:** niedrig

### Bewertung von Entwurf A

**Kriterium 1 — Zugriffe**

| Auswahl | Nullpunkt | Entwurf A |
|---|---|---|
| 1 | 2 | **3** |
| 5 | 6 | **3** |
| 20 | 21 | **3** |
| 50 | 51 | **3** |

Zusammensetzung: 1 × `Filter` (Vorab-Lesen) + 1 × `Remove` + 1 × `Refresh` = **konstant 3, unabhängig von der Anzahl.**

Bei einer einzelnen Buchung ist A also um einen Zugriff teurer als heute. Ab zwei Buchungen gewinnt A, ab fünf deutlich, bei fünfzig um den Faktor 17.

`UNSICHER:` **Wie viele HTTP-Anfragen `Remove(Tischbuchungen; <Tabelle>)` intern erzeugt, kann ich aus dem Quellcode nicht belegen.** Auf Formelebene ist es eine Operation statt N; dass der SharePoint-Konnektor daraus intern mehrere Anfragen macht, ist möglich. Entscheidend ist der Unterschied zwischen *nacheinander, jede mit voller Wartezeit* (heute) und *einer Sammeloperation* (A). Das muss gemessen werden: Stoppuhr bei 1, 5 und 20 Buchungen, vorher und nachher.

**Kriterium 2 — Delegierbarkeit**
Der Vorab-Lesevorgang benutzt exakt dieselbe Bedingung wie `galAlleTischbuchungen.Items` — `Person.Email = User().Email && Endzeit >= Now()`. Er erbt damit deren Delegationsverhalten, gut oder schlecht. **Das ist Absicht:** Beide sehen immer dieselbe Menge, die Galerie kann also nichts anzeigen, was der Vorab-Lesevorgang übersieht. Keine neue Warnung. Siehe offene Frage 1.

**Kriterium 3 — Gleichzeitigkeit**
Der Abstand zwischen Lesen und Löschen schrumpft von „seit dem Anhaken" (Minuten) auf „zwei aufeinanderfolgende Anweisungen" (Millisekunden). Eine zwischenzeitlich gelöschte Buchung landet gar nicht erst in `colStornoZiele`. Der verbleibende Rest ist durch `IfError` abgedeckt. **Bug 4 ist damit geschlossen**, das theoretische Zeitfenster bleibt winzig offen.

**Kriterium 4 — Wartungsfläche**
Die Filterbedingung `Person.Email = User().Email && Endzeit >= Now()` steht nach dem Umbau an **drei** Stellen: `galAlleTischbuchungen.Items`, `btnStornierenKlein.OnSelect`, `chkAlleAuswählen.OnCheck`. Heute an einer. Das ist eine Verschlechterung.

**Gegenmittel, falls dich das stört:** Die Bedingung in eine Named Formula in `App.Formulas` auslegen. `App.Formulas` existiert bereits mit 19 Definitionen und darf `Now()` sowie Steuerelement-Properties verwenden:
```
MeineBuchungen = SortByColumns(Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now()); "Startzeit"; SortOrder.Ascending);
```
Danach steht an allen drei Stellen nur noch `MeineBuchungen`. `UNSICHER:` Named Formulas werden bei jeder Auswertung neu berechnet und nicht zwischengespeichert — ob das hier zu mehr Abfragen führt als die drei ausgeschriebenen Stellen, kann ich nicht aus dem Quellcode belegen. **Mach das nicht im selben Schritt**, sondern erst, wenn A läuft und gemessen ist.

**Kriterium 5 — Fehleranzeige**
Drei unterscheidbare, deutsche Meldungen: nichts ausgewählt, alles bereits weg, teilweise bereits weg. Dazu `IfError` um den Schreibvorgang. Die Erfolgsmeldung steht jetzt im `DefaultResult` von `IfError` und kann nicht mehr neben einem Fehler erscheinen.

**Kriterium 6 — Einfügeaufwand**
Vier Steuerelemente, fünf Properties. A.3 und A.4 sind optional beziehungsweise kosmetisch. Kein neues Steuerelement, keine Änderung an SharePoint.

### Die überstandenen Angriffe

| Angriff | Ergebnis |
|---|---|
| **Zwei Nutzer gleichzeitig** | Überstanden. Löscht der andere zwischen Vorab-Lesen und `Remove`, fängt `IfError` den Fehler und die Liste wird aktualisiert. Zeitfenster: Millisekunden. |
| **Datensatz existiert serverseitig nicht mehr** | Überstanden, und zwar ohne Fehler. Der Datensatz steht nicht in `colStornoFrisch`, fällt aus `colStornoZiele` heraus und wird nicht angefasst. Der Nutzer liest „3 von 5 Buchungen storniert. Die übrigen waren bereits storniert." **Das ist Bug 4.** |
| **Netzwerk bricht mitten im Vorgang ab** | Überstanden. Teilweise gelöscht ist möglich, aber die Wahrheit steht danach in der Liste; `Refresh` läuft außerhalb des `If` und damit auch im Fehlerfall. Kein widersprüchlicher Zustand. |
| **50 statt 5 Einträge** | Überstanden. 3 Zugriffe statt 51. |
| **SharePoint drosselt mit 429** | Überstanden. Weniger Anfragen bedeuten weniger Drosselungsrisiko; was trotzdem schiefgeht, fängt `IfError`. |
| **Buchung wird zwischen Auswahl und Bestätigung verlängert** | Überstanden. `Remove` adressiert über die ID. Die Buchung ist dieselbe, nur länger; der Nutzer wollte sie stornieren, sie wird storniert. |

### Was zusätzlich nötig ist

**Nichts.** Keine neue SharePoint-Spalte, kein Flow, kein neues Steuerelement. `colStornoFrisch` und `colStornoZiele` entstehen zur Laufzeit und müssen nicht in `App.OnStart` angelegt werden.

**Optional, aber empfohlen:** In `App.OnStart` hinter `Clear(colAusgewaehlteBuchungen);` zwei Zeilen ergänzen:
```
Clear(colStornoFrisch);;
Clear(colStornoZiele);;
```
**Achte darauf, dass die Zeile davor mit `;;` endet.** In `App.OnStart` steht heute `Clear(colAusgewaehlteBuchungen);` — im Studio also mit einem Verkettungszeichen am Zeilenende. Prüfe das vor dem Einfügen.

### Einfügereihenfolge für A

1. **A.4** (`chkAuswahl.X`) — kosmetisch, risikofrei, bringt dich in den Rhythmus. 2 Minuten.
2. **A.1** (`btnStornierenKlein.OnSelect`) — der Kern. Danach **sofort testen**, bevor irgendetwas anderes angefasst wird. 15 Minuten inklusive Test.
3. **A.2** (`btnSchließenKlein.OnSelect`) — das Aufräumen nachziehen. 3 Minuten.
4. **A.3** (`chkAlleAuswählen.OnCheck`) — nur, wenn Testschritt 5 unten den Fehler bestätigt. 5 Minuten.

### Testschritte für A

**Test 1 — Normalfall.**
Buchungen-Tab, Auswahlmodus an, zwei Buchungen anhaken, auf einen Verwalten-Knopf klicken, „Stornieren".
→ Erwartet: Meldung **„2 Buchungen storniert."** in Grün. Beide verschwinden. Auswahlmodus schaltet sich ab.

**Test 2 — leere Auswahl.**
Auswahlmodus an, keinen Haken setzen, einen Verwalten-Knopf klicken, „Stornieren".
→ Erwartet: Meldung **„Keine Buchungen ausgewählt."** in Gelb. Nichts verschwindet.

**Test 3 — der eigentliche Test, Bug 4.**
Die App in **zwei Browser-Tabs** öffnen. In Tab 1 den Auswahlmodus einschalten und drei Buchungen anhaken, aber **noch nicht stornieren**. In Tab 2 eine dieser drei Buchungen einzeln stornieren. Zurück in Tab 1, ohne zu aktualisieren, auf „Stornieren" klicken.
→ Erwartet: Meldung **„2 von 3 Buchungen storniert. Die übrigen waren bereits storniert."** in Gelb.
→ **Kein** „Item Not Found". **Keine** rohe Fehlermeldung. Nach dem Vorgang sind alle drei weg.
Das ist der Nachweis, dass Bug 4 geschlossen ist. Vorher hättest du hier einen Connector-Fehler **und** eine grüne Erfolgsmeldung gesehen.

**Test 4 — alles bereits weg.**
Wie Test 3, aber in Tab 2 **alle drei** stornieren.
→ Erwartet: **„Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."** in Gelb.

**Test 5 — Geschwindigkeit, mit Stoppuhr.**
Je zehn Buchungen für morgen anlegen, dann alle zehn anhaken und stornieren. **Vorher und nachher messen**, also einmal mit dem alten Stand (`Tischbuchung_2026-09-30_Analyse.zip` ist dein Rückfallpunkt) und einmal mit dem neuen.
→ Erwartet: deutlich kürzer. Ohne Zahl ist diese Arbeit nicht abgeschlossen.

**Test 6 — „Alle auswählen", nur wenn du A.3 einfügst.**
Mehr künftige Buchungen anlegen, als die Galerie auf einmal lädt. Ohne zu scrollen „Alle auswählen" klicken, dann nach ganz unten scrollen.
→ Erwartet: Auch die untersten Zeilen sind angehakt. Vor A.3 sind sie es nicht.

---

## Entwurf C — Weich löschen über eine Statusspalte

### Die Idee in drei Sätzen

Stornieren löscht nichts mehr, sondern setzt mit einem einzigen Sammel-`Patch` ein Kennzeichen `Storniert` auf allen ausgewählten Buchungen. Alle Abfragen der App blenden stornierte Buchungen aus, sodass sie für den Nutzer verschwunden sind; das tatsächliche Löschen übernimmt der nächtliche Aufräum-Flow, der ohnehin schon läuft. Dadurch kann zweimaliges Stornieren derselben Buchung gar nicht mehr fehlschlagen — ein Kennzeichen zweimal zu setzen ist harmlos, während ein zweites Löschen immer ein Fehler ist.

### Voraussetzung in SharePoint

In der Liste `Tischbuchungen` eine neue Spalte anlegen:

| Eigenschaft | Wert |
|---|---|
| Anzeigename | `Storniert` |
| Typ | Ja/Nein |
| Standardwert | **Nein** |

**Wichtig:** Nach dem Anlegen alle bestehenden Datensätze einmal auf `Nein` setzen, nicht auf leer. Leere Werte verhalten sich bei Vergleichen anders als `false`, und genau daran scheitert sonst die Filterbedingung. In der SharePoint-Listenansicht lässt sich das in der Rasteransicht in einem Zug erledigen.

Danach in Power Apps die Datenquelle `Tischbuchungen` aktualisieren, damit die Spalte im Schema erscheint.

`UNSICHER:` **Der Anzeigename muss `Storniert` lauten, der interne Name darf abweichen** — SharePoint erzeugt bei deutschen Namen oft kryptische interne Namen. Für Power Apps zählt der Anzeigename, für den Aufräum-Flow der interne. Siehe auch `INVENTAR.md` Vorbemerkung B: bei `CheckedIn` ist genau das passiert (intern `Checkedin`, Anzeigename `CheckedIn`).

### C.1 — `btnStornierenKlein.OnSelect`

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 4074
**Steuerelement:** `Screen1.conBuchungen.conVerwaltenKlein.btnStornierenKlein`
**Property:** `OnSelect`

**ORIGINAL:** wie bei A.1 oben.

**NEU:**
```
Set(varIsLoading; true);;
If(
    CountRows(colAusgewaehlteBuchungen) = 0;
    Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
    IfError(
        Patch(
            Tischbuchungen;
            colAusgewaehlteBuchungen;
            ForAll(colAusgewaehlteBuchungen; {Storniert: true})
        );
        Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
        Notify(CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert."; NotificationType.Success)
    )
);;
Refresh(Tischbuchungen);;
Clear(colAusgewaehlteBuchungen);;
Set(varGeklickteBuchungKlein; Blank());;
Set(varZeigeVerwaltenKlein; false);;
Set(varAuswahlModusAktiv; false);;
Reset(tglAuswahlModus);;
Set(varIsLoading; false)
```

**WARUM:** Ein einziger Sammel-`Patch` statt N Löschaufrufen, und das wiederholte Setzen desselben Kennzeichens ist im Gegensatz zum wiederholten Löschen kein Fehler.

**TEST:** Zwei Buchungen anhaken, stornieren. Erwartung: Meldung „2 Buchungen storniert.", beide verschwinden aus der Liste, stehen aber in SharePoint noch mit `Storniert = Ja`.

**RISIKO:** hoch — wirkt erst zusammen mit C.2 bis C.5. Zwischen C.1 und C.2 sind stornierte Buchungen in der App weiterhin sichtbar und blockieren weiterhin Tische. **Diese Blöcke müssen in einer Sitzung durchgezogen werden.**

`UNSICHER:` Ich verwende hier die dokumentierte Form `Patch(Datenquelle; Basistabelle; Änderungstabelle)`. `AUFGABE_SCHLEIFE.md` nennt die kürzere Form `Patch(Quelle; Tabelle)` mit `ID`-Spalte, also:
```
Patch(Tischbuchungen; ForAll(colAusgewaehlteBuchungen As A; {ID: A.ID; Storniert: true}))
```
**Nimm die kürzere nur, wenn das Studio sie ohne roten Unterstrich annimmt.** Falls nicht, steht oben die Form, die sicher funktioniert.

### C.2 — `galAlleTischbuchungen.Items`

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 3452
**Steuerelement:** `Screen1.conBuchungen.galAlleTischbuchungen`
**Property:** `Items`

**ORIGINAL:**
```
=With(
  { erzwingeNeuaufbau: varGalleryNeuAufbauen },
  SortByColumns(
    Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()),
    "Startzeit",
    SortOrder.Ascending
  )
)
```

**NEU:**
```
With(
    { erzwingeNeuaufbau: varGalleryNeuAufbauen };
    SortByColumns(
        Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now() && Storniert = false);
        "Startzeit";
        SortOrder.Ascending
    )
)
```

**WARUM:** Ohne diesen Filter bleiben stornierte Buchungen in der Liste stehen.

**TEST:** Eine Buchung stornieren. Erwartung: Sie verschwindet aus dem Buchungen-Tab.

**RISIKO:** mittel — `Storniert = false` trifft **nicht** auf Datensätze mit leerem Wert zu. Deshalb die Nachbefüllung in der Voraussetzung oben.

### C.3 — `galTischbuchungenHeute.Items`

**Datei:** `./src/Src/Screen1.pa.yaml`, Zeile 363
**Steuerelement:** `Screen1.conDashboard.galTischbuchungenHeute`
**Property:** `Items`

**ORIGINAL:**
```
=Filter(
  Tischbuchungen,
  Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
)
```

**NEU:**
```
Filter(
    Tischbuchungen;
    Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now()) && Storniert = false
)
```

**WARUM:** Dasselbe für das Dashboard.

**TEST:** Eine heutige Buchung stornieren. Erwartung: Sie verschwindet auch aus „My personal desk".

**RISIKO:** niedrig

### C.4 — Die sechs Stellen der Master-Bedingung

Jede der sechs in `INVENTAR.md` Abschnitt 1 aufgeführten Properties braucht in **jedem** `LookUp(Tischbuchungen; …)` den Zusatz `&& Storniert = false`. Das sind zwölf `LookUp`-Aufrufe in sechs Properties:

| Steuerelement | Property | `LookUp`-Aufrufe |
|---|---|---|
| `conGrundriss.Gallery1.Rectangle1` | `Fill` | 2 |
| `conGrundriss.Gallery1.Circle1` | `BorderColor` | 1 |
| `conGrundriss.Gallery1.Circle1` | `BorderStyle` | 3 |
| `conGrundriss.Gallery1.Circle1` | `Fill` | 2 |
| `conGrundriss.Gallery1.Label1` | `Text` | 2 |
| `conGrundriss.Gallery1.btnHitArea` | `OnSelect` | 2 |

Beispielhaft für `Rectangle1.Fill` ausgeschrieben:

**NEU:**
```
With(
    {
        relevanteBuchung:
            If(
                varAnsichtsDatum = Today();
                LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Storniert = false);
                LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days) && Storniert = false)
            )
    };
    If(
        IsBlank(relevanteBuchung);
        ColorValue("#00A96B");
        If(
            relevanteBuchung.CheckedIn;
            ColorValue("#EB3951");
            ColorValue("#FFA500")
        )
    )
)
```

**WARUM:** Sonst zeigt der Grundriss stornierte Tische weiterhin als belegt.

**TEST:** Eine Buchung für den gerade angezeigten Tag stornieren, dann auf den Grundriss wechseln. Erwartung: Die Kachel ist grün.

**RISIKO:** **hoch** — hier sind in diesem Projekt mehrfach Fehler beim Kopieren passiert. Die zwölf `LookUp`-Aufrufe sind **nicht wortgleich**: `Circle1.BorderColor` hat keinen `varAnsichtsDatum`-Zweig, und `Circle1.BorderStyle` benutzt in `istBesetzt` ein anderes Zeitfenster (`Now() >= Startzeit && Now() <= Endzeit`). **Jede Property einzeln öffnen, den Zusatz am Ende jeder Bedingung einfügen, nicht die ganze Formel überschreiben.**

### C.5 — Kollisionsprüfungen beim Buchen und Verlängern

Acht weitere Stellen prüfen auf Kollisionen und würden eine stornierte Buchung als Blockade behandeln:

| Steuerelement | Properties | Zeile |
|---|---|---|
| `conTischBuchungenPanel.btn5Std` | `DisplayMode`, `Fill` | 1226, 1251 |
| `conTischBuchungenPanel.btn9Std` | `DisplayMode`, `Fill` | 1311, 1336 |
| `conTischBuchungenPanel.btnSpeichernTischePanel` | `OnSelect` (`bestehendeBuchungenTisch`) | 966 |
| `conBuchungDialog.btnSpeichern` | `OnSelect` (`bestehendeBuchungenTisch`) | 2734 |
| `conVerwaltenDialog.btnPlus1Std` / `btnPlus2Std` / `btnPlus3Std` | je `DisplayMode`, `Fill` | 3292–3406 |
| `conBuchungen.conVerwaltenDialog_1.btnPlus1Std_1` / `btnPlus2Std_1` / `btnPlus3Std_1` | je `DisplayMode`, `Fill` | 3741–3850 |

Die beiden wichtigsten, weil sie die Doppelbuchung verhindern:

**NEU für `btnSpeichernTischePanel.OnSelect`, nur diese eine Zeile im äußeren `With`:**
```
bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Storniert = false)
```

**NEU für `btnSpeichern.OnSelect`, nur diese eine Zeile im äußeren `With`:**
```
bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel && Storniert = false)
```

**WARUM:** Ohne diesen Zusatz blockiert eine stornierte Buchung den Tisch weiter — der schlimmstmögliche Fehler dieses Entwurfs, weil er das Gegenteil dessen bewirkt, was der Nutzer wollte.

**TEST:** Eine Buchung für morgen 10–12 Uhr anlegen, stornieren, dann denselben Tisch für morgen 10–12 Uhr erneut buchen. Erwartung: funktioniert. Ohne C.5 bekommst du „konnten wegen Kollision nicht gebucht werden".

**RISIKO:** **hoch** — insgesamt 16 Properties über acht Steuerelemente, mit variierenden Offsets (60/120/180 Minuten) und zwei Fassungen desselben Knopfs (`btnPlus3Std` und `btnPlus3Std_1` sind unterschiedlich geschrieben, siehe `INVENTAR.md`). Hier passieren Übersehen-Fehler.

### C.6 — Aufräum-Flow erweitern

Der bestehende Power-Automate-Flow (täglich 03:00) löscht Buchungen, deren `Endzeit` mehr als 7 Tage zurückliegt. Er muss zusätzlich alle Datensätze mit `Storniert = Ja` löschen, deren `Endzeit` vorbei ist.

`UNSICHER:` **Für den Flow gilt der interne Spaltenname, nicht der Anzeigename.** Welcher das ist, siehst du in den Listeneinstellungen am Ende der Spalten-URL (`Field=…`). Bei `CheckedIn` ist der interne Name `Checkedin` — rechne mit einer ähnlichen Abweichung.

**WARUM:** Ohne diesen Schritt wächst die Liste unbegrenzt, und genau das sollte der Flow verhindern.

**RISIKO:** mittel — ein Fehler hier löscht zu viel. Vor dem Scharfschalten einmal mit deaktiviertem Löschschritt laufen lassen und die Trefferliste ansehen.

### Bewertung von Entwurf C

**Kriterium 1 — Zugriffe**

| Auswahl | Nullpunkt | Entwurf A | Entwurf C |
|---|---|---|---|
| 1 | 2 | 3 | **2** |
| 5 | 6 | 3 | **2** |
| 20 | 21 | 3 | **2** |
| 50 | 51 | 3 | **2** |

Zusammensetzung: 1 × `Patch` + 1 × `Refresh` = **konstant 2.** Kein Vorab-Lesen nötig, weil ein doppeltes Setzen nicht schaden kann. **Bester Wert aller Entwürfe.**

Derselbe `UNSICHER`-Vorbehalt wie bei A: Wie viele HTTP-Anfragen ein Sammel-`Patch` intern erzeugt, kann ich nicht aus dem Quellcode belegen.

**Kriterium 2 — Delegierbarkeit**
Der Zusatz `Storniert = false` ist ein Gleichheitsvergleich auf einer Ja/Nein-Spalte. `References/DataSources.json` weist für Ja/Nein-Spalten `filterFunctions: ["eq"]` aus — Gleichheit ist also delegierbar. **Keine neue Warnung.** Wichtig: `= false` verwenden, nicht `<> true`, weil Ungleichheit nicht gesichert unterstützt ist.

**Kriterium 3 — Gleichzeitigkeit**
**Hier ist C stärker als A.** Stornieren zwei Nutzer dieselbe Buchung gleichzeitig, setzen beide dasselbe Kennzeichen — beide erfolgreich, kein Fehler, kein Widerspruch. Die Operation ist wiederholbar, und damit ist eine ganze Fehlerklasse verschwunden statt abgefangen.

Bleibt eine schmale Lücke: Hat der Aufräum-Flow den Datensatz hart gelöscht, schlägt auch der `Patch` fehl. Der Flow löscht aber nur Vergangenes, und die Galerie zeigt nur `Endzeit >= Now()`. Die Lücke ist damit praktisch geschlossen.

**Kriterium 4 — Wartungsfläche**
**Hier ist C deutlich schwächer als A.** Nach dem Umbau muss `Storniert = false` in **rund 24 Abfragen** über **17 Properties** stehen (C.2 bis C.5). Jede künftige Abfrage auf `Tischbuchungen` muss daran denken. Vergisst man es an einer Stelle, entsteht ein Fehler, der sich als „Tisch ist belegt, obwohl niemand ihn gebucht hat" zeigt — und genau diese Art Fehler hat dich in diesem Projekt schon Tage gekostet.

**Kriterium 5 — Fehleranzeige**
`IfError` um den `Patch`, deutsche Meldung, Erfolgsmeldung im `DefaultResult`. Gleichwertig zu A, aber mit weniger Fallunterscheidungen, weil weniger Fälle übrig sind.

**Kriterium 6 — Einfügeaufwand**
**Mit Abstand der höchste.** Eine neue SharePoint-Spalte plus Nachbefüllung, eine Flow-Änderung, 17 Properties über neun Steuerelemente. Realistisch zwei bis drei Stunden mit Tests, und C.4 und C.5 sind genau die Sorte Fließbandarbeit, bei der in diesem Projekt schon Offsets übersehen wurden.

### Die überstandenen Angriffe

| Angriff | Ergebnis |
|---|---|
| **Zwei Nutzer gleichzeitig** | Überstanden, und zwar restlos. Zweimal `Storniert = true` zu setzen ist kein Fehler. **Stärker als A.** |
| **Datensatz existiert serverseitig nicht mehr** | Überstanden mit Einschränkung. Hart gelöschte Datensätze lassen auch den `Patch` scheitern; `IfError` fängt das. Praktisch tritt der Fall nicht auf, weil der Aufräum-Flow nur Vergangenes anfasst und die Galerie nur Künftiges zeigt. |
| **Netzwerk bricht mitten im Vorgang ab** | Überstanden. Teilweise gesetzt ist möglich, die Wahrheit steht danach in der Liste, kein Datenverlust. **Stärker als A**, weil nichts unwiederbringlich weg ist — ein versehentlich gesetztes Kennzeichen lässt sich in SharePoint zurücknehmen, eine gelöschte Zeile nicht. |
| **50 statt 5 Einträge** | Überstanden. 2 Zugriffe statt 51. **Bester Wert.** |
| **SharePoint drosselt mit 429** | Überstanden. Eine Schreiboperation statt 50. |
| **Buchung wird zwischen Auswahl und Bestätigung verlängert** | Überstanden, und sauberer als bei A. Der `Patch` schreibt nur `Storniert` und fasst `Endzeit` nicht an — die Änderung des anderen Nutzers geht nicht verloren. |

### Was zusätzlich nötig ist

- **Neue SharePoint-Spalte** `Storniert` (Ja/Nein, Standard Nein) in `Tischbuchungen`, plus Nachbefüllung aller bestehenden Zeilen auf `Nein`.
- **Änderung am Aufräum-Flow** (C.6).
- **Kein neues Steuerelement**, keine neue Variable.

### Einfügereihenfolge für C

**Diese Reihenfolge ist zwingend.** Zwischen Schritt 2 und Schritt 6 ist die App in einem widersprüchlichen Zustand.

1. SharePoint-Spalte `Storniert` anlegen und alle bestehenden Zeilen auf `Nein` setzen. In Power Apps die Datenquelle aktualisieren. **20 Min.**
2. **C.2** (`galAlleTischbuchungen.Items`) und **C.3** (`galTischbuchungenHeute.Items`). **10 Min.**
3. **C.5**, zuerst nur die beiden `bestehendeBuchungenTisch`-Zeilen. **10 Min.**
4. **C.1** (`btnStornierenKlein.OnSelect`). Danach Test 1 bis 3. **20 Min.**
5. **C.4**, die sechs Grundriss-Properties, **einzeln, mit Blick auf den Grundriss nach jeder**. **45 Min.**
6. **C.5** vollständig, die restlichen 14 Properties der Plus- und Dauer-Knöpfe. **40 Min.**
7. **C.6**, Flow erweitern. **30 Min.**
8. `btnSchließenKlein.OnSelect` bleibt unverändert — C braucht keine Hilfs-Collections.

### Testschritte für C

**Test 1 — Normalfall.** Zwei Buchungen anhaken, stornieren. → „2 Buchungen storniert.", beide verschwinden aus dem Buchungen-Tab.

**Test 2 — SharePoint-Gegenprobe.** Die Liste `Tischbuchungen` in SharePoint öffnen. → Die beiden Zeilen stehen noch da, `Storniert` = `Ja`. Das ist der Nachweis, dass weich gelöscht wurde.

**Test 3 — Gleichzeitigkeit, zwei Tabs.** In Tab 1 drei Buchungen anhaken. In Tab 2 eine davon einzeln stornieren. In Tab 1 „Stornieren".
→ Erwartet: **„3 Buchungen storniert."** in Grün, **ohne jede Fehlermeldung.** Das ist der Unterschied zu A, wo hier eine gelbe Teilmeldung käme.

**Test 4 — der kritische Test, Tisch wieder frei.** Buchung für morgen 10–12 Uhr anlegen, stornieren, denselben Tisch für morgen 10–12 Uhr erneut buchen.
→ Erwartet: funktioniert, Meldung „Buchung(en) erfolgreich gespeichert."
→ Kommt stattdessen „konnten wegen Kollision nicht gebucht werden", hast du C.5 unvollständig eingefügt.

**Test 5 — Grundriss.** Eine Buchung für den heute angezeigten Tag im laufenden Zeitfenster stornieren, auf den Grundriss wechseln.
→ Erwartet: Kachel grün, Kreis hellgrün, keine Initialen im Kreis, kein schwarzer Kreisrand.
→ Jede dieser vier Eigenschaften, die noch „belegt" zeigt, verweist auf eine vergessene Stelle in C.4. Der Kreisrand gehört zu `Circle1.BorderColor`, der Rahmenstil zu `Circle1.BorderStyle`, die Kreisfüllung zu `Circle1.Fill`, die Initialen zu `Label1.Text`, die Kachelfarbe zu `Rectangle1.Fill`.

**Test 6 — Verlängern-Knöpfe.** Buchung A für morgen 10–12 Uhr, Buchung B für morgen 13–14 Uhr auf demselben Tisch anlegen. B stornieren. A verwalten, „+1 Std" ansehen.
→ Erwartet: grün und anklickbar. Bleibt er rot, fehlt `Storniert = false` bei `btnPlus1Std_1`.

**Test 7 — Geschwindigkeit.** Wie Test 5 bei Entwurf A: zehn Buchungen, Stoppuhr, vorher und nachher.

---

# 3. Empfehlung

**Nimm Entwurf A.**

Beide schlagen den Nullpunkt bei Kriterium 1 um Größenordnungen — 3 beziehungsweise 2 konstante Zugriffe statt 51 bei fünfzig Buchungen. Der Unterschied liegt nicht in der Geschwindigkeit, sondern im Preis: A kostet dich **vier Properties an vier Steuerelementen und etwa eine halbe Stunde**, C kostet **eine neue SharePoint-Spalte, eine Flow-Änderung, 17 Properties über neun Steuerelemente und zwei bis drei Stunden** — und danach muss jede künftige Abfrage auf `Tischbuchungen` für immer daran denken, `Storniert = false` mitzuführen. Das ist genau die Art von stiller Dauerverpflichtung, die in diesem Projekt schon einmal teuer war: Vergisst du sie an einer Stelle, zeigt die App einen Tisch als belegt, den niemand gebucht hat, und SharePoint sagt dir nichts.

C ist technisch der sauberere Entwurf, und das sollst du wissen statt es überredet zu bekommen. Er macht das Stornieren wiederholbar, womit eine ganze Fehlerklasse nicht abgefangen, sondern unmöglich wird; er schreibt nur ein Feld und zerstört deshalb keine parallele Änderung; und er macht jeden Fehlgriff rücknehmbar, weil nichts wirklich gelöscht wird. Wäre die App fertig und stabil, würde ich C nehmen.

Sie ist es aber nicht. Vor dir liegen noch die Delegationsarbeit, der Schreibpfad der Serienbuchung, die Doppelbuchungsprüfung und das Ausräumen von 51 toten Steuerelementen. Ein Entwurf, der jetzt sechzehn weitere Properties an Bedingungen bindet, die du bei jeder dieser Arbeiten mitschleppen musst, macht alles Folgende schwerer. A ändert vier Properties, fasst das Datenmodell nicht an und schließt Bug 4 vollständig — und er schließt ihn auf die richtige Art: nicht indem er den Fehler abfängt, sondern indem die Ursache verschwindet, weil nur noch Datensätze gelöscht werden, deren Existenz eine Anweisung zuvor bestätigt wurde.

**Der Preis dieser Entscheidung:** Du behältst ein theoretisches Zeitfenster von wenigen Millisekunden zwischen Vorab-Lesen und `Remove`, das `IfError` abfängt statt ausschließt. Du behältst das harte Löschen, also keine Rücknahme bei einem Fehlgriff. Und du führst dieselbe Filterbedingung an einer dritten Stelle. Die ersten beiden Punkte sind in dieser App vertretbar — es geht um Schreibtischbuchungen, nicht um Buchhaltung. Der dritte ist mit einer Named Formula heilbar, aber erst nachdem A läuft und gemessen ist, nicht im selben Schritt.

**Wenn du dich doch für C entscheidest**, dann nicht, weil es schneller ist — es ist nur um einen Zugriff schneller —, sondern weil du Stornieren rücknehmbar machen willst. Das ist ein fachlicher Grund, kein technischer, und er ist gut. Dann aber bitte vollständig in einer Sitzung bis einschließlich C.5, denn ein halb eingebautes C ist schlechter als der Nullpunkt.

---

# 4. Verworfen

Vollständig in `VERWORFEN.md`. Vier Familien sind gefallen: **B** (bedingungsbasiertes `RemoveIf` über einen Zeitraum — löscht Buchungen mit, die der Nutzer nie gesehen hat), **D** (Auslagern an einen Power-Automate-Flow — nach einem Verbindungsabbruch kann die App nicht mehr sagen, was geschehen ist), **E** (optimistische Oberfläche — Power Fx kennt keinen Hintergrundschreibvorgang, die Prämisse existiert nicht), **F** (Mehrfachauswahl durch „Serie stornieren" über `SerienID` ersetzen — beantwortet eine andere Frage als die gestellte).

**Drei Sätze, was ich über das Problem gelernt habe.** Das Problem war nie die Schleife, sondern die Herkunft der Datensätze: `colAusgewaehlteBuchungen` ist eine Kopie von unbestimmtem Alter, und jeder Entwurf, der sie unbesehen an `Remove` weiterreicht, erbt „Item Not Found", egal wie elegant er sonst ist. Bei Löschoperationen schlägt eine geschlossene, vom Nutzer gesehene Menge jede zur Laufzeit ausgewertete Bedingung — das hat zwei Entwürfe gekostet, und es ist dieselbe Eigenschaft, die bei Leseabfragen ein Vorteil wäre. Und: In Power Fx führt der einzige Weg zu „schneller" über „weniger Zugriffe", weil es keine Nebenläufigkeit gibt, mit der sich Wartezeit verstecken ließe — damit ist Kriterium 1 nicht nur das wichtigste, sondern faktisch das einzige, an dem Geschwindigkeit überhaupt hängt.

**Aus Entwurf F ist etwas übrig geblieben, das nicht verloren gehen darf:** `Tischbuchungen.SerienID` existiert bereits, ist read-write, mit `eq` und `startswith` filterbar — und wird von der App nirgends benutzt. Für die Serienbuchung in Schritt 3 der Umbauliste ist das die fehlende Zutat.

---

# 5. UNSICHER — alles an einer Stelle

Sechs Punkte, in fünf Minuten zu beantworten.

**1. Wie viele HTTP-Anfragen erzeugt ein Sammelaufruf wirklich?**
Betrifft A und C gleichermaßen. Auf Formelebene ist `Remove(Tischbuchungen; <Tabelle>)` eine Operation statt N; was der SharePoint-Konnektor daraus macht, steht nicht im Quellcode. **Nicht beantwortbar durch Nachdenken — nur durch Messen.** Deshalb Test 5 beziehungsweise Test 7 mit der Stoppuhr, vorher und nachher, bei 1, 5 und 20 Buchungen.

**2. Delegiert `Person.Email = User().Email`?**
Betrifft A direkt: Der Vorab-Lesevorgang in A.1 benutzt dieselbe Bedingung wie `galAlleTischbuchungen.Items`. **Steht im Studio ein gelbes Warndreieck neben `galAlleTischbuchungen.Items`?** Wenn ja, sehen Galerie und Vorab-Lesevorgang beide nur die ersten 2000 Zeilen — immerhin dieselben 2000, A wird dadurch nicht falsch. Aber dann hängt auch Bug 3 daran, und das gehört in Schritt 2 der Umbauliste.

**3. Verarbeitet `Remove` mit einer Tabelle die restlichen Zeilen weiter, wenn eine fehlschlägt?**
Betrifft A. Für den Normalfall irrelevant, weil A.1 verschwundene Datensätze vorher aussortiert. Relevant nur für die Millisekundenlücke. Falls du es wissen willst: Test 3 so abwandeln, dass du in Tab 2 löschst, **während** Tab 1 schon storniert.

**4. Akzeptiert dein Studio die Kurzform `Patch(Quelle; Tabelle)` mit `ID`-Spalte?**
Betrifft nur C.1. Beide Fassungen stehen oben. Einfach einfügen und schauen, ob die Formelzeile rot unterstrichen wird.

**5. Wie lautet der interne Name der neuen Spalte `Storniert`?**
Betrifft nur C.6, also den Flow. In den Listeneinstellungen am Ende der Spalten-URL ablesen (`Field=…`). Bei `CheckedIn` weicht er ab (intern `Checkedin`), rechne also damit.

**6. Wie viele Zeilen lädt `galAlleTischbuchungen` auf einmal?**
Betrifft nur A.3. Wenn du nie mehr als ein oder zwei Dutzend künftige Buchungen hast, kannst du A.3 weglassen und den einen zusätzlichen Lesevorgang sparen.

---

**Nicht in diesem Lauf bearbeitet:** `AUFGABE_UMBAU.md` bleibt wie vereinbart offen. Zwei Funde aus dem Inventar greifen aber direkt dort ein und sollten vorher gelesen werden: `Tische.Aktiv` existiert nicht und `Tische.Standort` heißt `Geschoss` (betrifft Punkt 5), und es steht kein `Refresh` in einer `ForAll` (betrifft Punkt 2.a).
