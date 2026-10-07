# AUFGABE_SPEICHERN.md — Die Speicher-Knöpfe neu denken

**Stand: 03.10.2026**
**Grundlage:** `INVENTAR.md`, `KORREKTUR.md`, `KORREKTUR_2.md`, Quellcode in `./src`
**Vorlauf:** `ENTWURF_MEHRFACHAUSWAHL.md` — dieselbe Methode, Ergebnis vom Nutzer als sehr gut bewertet

---

## Warum das wichtig ist

Diese App geht in **zehn Tagen** produktiv und ersetzt ein zugekauftes Produkt. Der Entwickler ist eine einzelne Person. Deine letzte Lieferung hat ihm mehrere Tage Ausprobieren erspart — das ist der Maßstab.

Das heißt zweierlei für deine Empfehlungen. Ein Entwurf, der vier Properties ändert und morgen läuft, schlägt einen, der siebzehn ändert und technisch schöner ist. Und ein Entwurf, der eine Sitzung lang halbfertig ist, ist in dieser Lage gefährlicher als einer, der weniger bringt.

---

## Der Unterschied zum letzten Mal: hier steht mehr auf dem Spiel

Beim Stornieren war der schlimmste Fall eine Fehlermeldung. Beim Speichern ist der schlimmste Fall, dass **zwei Leute denselben Tisch gebucht haben und beide eine Erfolgsmeldung gesehen haben.**

Die Kollisionsprüfung der App ist heute ein clientseitiges Lesen-dann-Schreiben: Sie zählt bestehende Buchungen, und erst danach schreibt sie. Zwischen beidem liegt ein Zeitfenster. SharePoint kennt keine Transaktionen.

**Daraus folgt eine harte Regel für diese Aufgabe:** Geschwindigkeit zählt erst, nachdem Korrektheit feststeht. Ein Entwurf, der schneller ist, aber das Doppelbuchungsfenster vergrößert, ist schlechter als der Ist-Zustand und wird verworfen, egal wie gut seine Zahlen sind. Umgekehrt ist ein Entwurf, der das Fenster schließt oder verkleinert, auch dann wertvoll, wenn er kaum schneller ist.

---

## Was in den Umfang gehört

Alle Schreibwege, über die eine Buchung entsteht oder geändert wird. Aus `INVENTAR.md` und dem Quellcode bekannt:

| Knopf | Zeile | Was er tut |
|---|---|---|
| `btnSpeichernTischePanel` | 966 | Buchen aus dem Panel, **inklusive Serienbuchung** |
| `conBuchungDialog.btnSpeichern` | 2734 | Buchen aus dem Grundriss-Dialog |
| `btnVerlängern_1` | 3679 | heißt „Speichern", sitzt im Mehrfachauswahl-Dialog |
| `btnPlus1Std` / `_2` / `_3` und die `_1`-Fassungen | 3292–3850 | Verlängern |
| Verkürzen-Knöpfe | laut Inventar | Verkürzen |
| `btnVerlaengernBestaetigen` | laut Inventar | Verlängern bestätigen |

**Vorrang in dieser Reihenfolge:** erst die Mehrfachauswahl, dann die Serienbuchung, dann der Rest.

---

## Die Frage, die du VOR jeder Optimierung beantwortest

`INVENTAR.md` hält fest: Es gibt kein Mehrfach-Speichern. `btnVerlängern_1` heißt „Speichern", arbeitet aber auf der einzelnen Buchung `varSelectedBuchungTab` und leert danach nur beiläufig `colAusgewaehlteBuchungen` mit.

Der Nutzer will ausdrücklich, dass das Speichern **für die Mehrfachauswahl** effizient wird. Das ergibt nur Sinn, wenn es überhaupt mehrere Datensätze schreibt.

**Beantworte zuerst, belegt aus dem Quellcode:**

1. Was genau passiert heute, wenn jemand fünf Buchungen anhakt, den Verwalten-Dialog öffnet, „+1 Std" wählt und „Speichern" klickt? Wird **eine** Buchung geändert oder fünf? Zitiere die Formeln, die das entscheiden.
2. Falls nur eine: Ist das Absicht oder ein Fehler? Die Oberfläche verspricht eine Sammelaktion — wenn sie nur eine ausführt, ändert der Nutzer vier Buchungen weniger, als er denkt, ohne jede Rückmeldung.
3. Was wäre das erwartete Verhalten? Entwirf danach.

**Optimiere nichts, bevor diese drei Fragen beantwortet sind.** Ein einzelner `Patch` ist bereits schnell; ihn schneller zu machen bringt nichts. Wenn hier eine Funktion fehlt statt langsam zu sein, ist das der eigentliche Befund — und dann ist deine Aufgabe, sie zu bauen, und zwar von Anfang an als Sammeloperation.

---

## Bekannte Zutaten, die du nutzen sollst

**`Tischbuchungen.SerienID`** existiert, ist beschreibbar, mit `eq` und `startswith` filterbar — und wird von der App **nirgends** benutzt. Für die Serienbuchung ist das die fehlende Zutat: eine Serie unter gemeinsamer Kennung anlegen und später mit einer Abfrage finden, ändern oder stornieren, statt mit vierzehn Einzelvorgängen.

**Die Kollisionsprüfung hat keine Zeitgrenze.** Beide Speichern-Knöpfe rechnen mit `bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = …)` — ohne Einschränkung auf den relevanten Zeitraum. Das holt alle Buchungen dieses Tisches, die je existiert haben. Prüfe, ob eine Eingrenzung möglich ist, ohne eine Kollision zu übersehen.

**`app-ForAllWithMutation` meldet Microsofts App-Prüfung dreimal.** Eine davon war das Mehrfach-Stornieren. Finde die anderen und sag, wo sie sitzen.

---

## Die Bewertungskriterien

In dieser Reihenfolge. Die ersten beiden sind Ausschlusskriterien — ein Entwurf, der dort verliert, wird verworfen, egal wie gut der Rest ist.

1. **Doppelbuchung.** Wird das Zeitfenster zwischen Prüfung und Schreiben größer, gleich oder kleiner als heute? Größer heißt verworfen.
2. **Ehrlichkeit der Rückmeldung.** Sieht der Nutzer je eine Erfolgsmeldung für etwas, das nicht passiert ist? Oder eine Sammelmeldung für eine Einzeländerung? Beides heißt verworfen.
3. **Datenquellen-Zugriffe** bei 1, 5, 14 und 50 betroffenen Buchungen. Aus der Formel abgezählt, mit Begründung. 14 ist die Obergrenze einer Serie.
4. **Delegierbarkeit.** Neue Warnung? Wenn ja, wie viele Zeilen werden geholt?
5. **Wartungsfläche.** Wie viele Stellen müssen künftig konsistent gehalten werden? Weniger ist besser.
6. **Einfügeaufwand.** Wie viele Properties an wie vielen Steuerelementen? Braucht es eine neue SharePoint-Spalte oder einen Flow?

---

## Der Ablauf

### Runde 0 — Nullpunkt, mit Belegen

Lies die heutigen Formeln aller oben genannten Knöpfe. Bewerte sie nach allen sechs Kriterien.

**Zeig Belege statt Behauptungen.** Jede Zahl, die du nennst, bekommt die Zeile, aus der sie stammt. „Fünfzig Zugriffe" ohne die Formel daneben ist wertlos. Schreib bei jeder Zählung dazu, wie du gezählt hast.

Prüfe, ob `VORHER_NACHHER.md` oder vergleichbare Messwerte aus dem Stornieren-Umbau im Ordner liegen. Wenn ja, nimm sie als Grundlage dafür, wie viel ein gesparter Zugriff tatsächlich wert ist. Wenn nein, schreib **ganz oben in das Ergebnis**, dass die zentrale Annahme dieser Arbeit — dass weniger Aufrufe spürbar schneller sind — unbestätigt ist und was passiert, falls sie nicht stimmt.

### Runde 1 — Vier grundverschiedene Familien, pro Baustelle

Für die Mehrfachauswahl und für die Serienbuchung je **vier Ansätze, die sich im Prinzip unterscheiden** — nicht vier Varianten derselben Idee.

Denkanstöße, keine Auswahlliste: Sammelaufruf statt Schleife; Vorab-Auflösung der betroffenen Menge wie in Entwurf A beim Stornieren; `SerienID` als gemeinsame Klammer; Schreiben an einen Power-Automate-Flow auslagern; die Kollisionsprüfung serverseitig statt clientseitig; die Operation so umbauen, dass sie wiederholbar ist und ein zweiter Versuch nicht schadet; oder die Funktion ganz anders schneiden, sodass die teure Operation gar nicht erst anfällt.

**Nicht flicken, neu bauen.** Der Nutzer hat beobachtet, dass in diesem Projekt der Neubau regelmäßig besser funktioniert hat als das Reparieren. Ein Entwurf, der ein Problem unmöglich macht, schlägt jeden, der es abfängt.

Pro Entwurf: vollständige, einfügbare Power-Fx-Formeln und die Bewertung nach allen sechs Kriterien.

### Runde 2 — Angriff durch einen Subagenten

**Diesen Schritt machst du nicht selbst.** Starte für jeden Entwurf einen Subagenten in frischem Kontext. Gib ihm den Entwurf, die sechs Kriterien und den Quellcode — aber **nicht** deine Begründung, warum du ihn für gut hältst. Er soll das Ergebnis bewerten, nicht deinen Gedankengang nachvollziehen.

Auftrag an den Subagenten: Finde Szenarien, in denen dieser Entwurf bricht. Mindestens diese prüfen, plus eigene:

- Zwei Nutzer buchen gleichzeitig denselben Tisch für dieselbe Zeit
- Eine Buchung wird zwischen Auswahl und Bestätigung von jemand anderem geändert
- Netzwerk bricht mitten im Vorgang ab
- 14 Serientermine, davon kollidieren drei
- SharePoint drosselt und antwortet mit 429
- Der Nutzer klickt zweimal schnell hintereinander
- Ein Datensatz existiert serverseitig nicht mehr

**Wichtige Anweisung an den Subagenten, wörtlich weitergeben:** *Melde nur Lücken, die Korrektheit oder die genannten Anforderungen betreffen. Keine Stilfragen, keine theoretischen Verbesserungen, keine zusätzlichen Abstraktionsebenen. Ein Prüfer, der Lücken finden soll, findet immer welche — melde nur die, bei denen du benennen kannst, was konkret schiefgeht und für wen.*

Diese Einschränkung ist wichtig: Ohne sie werden gute Entwürfe wegen erfundener Mängel verworfen.

### Runde 3 — Wegwerfen, nicht nachbessern

Jeder Entwurf, der einen Angriff bei Kriterium 1 oder 2 nicht übersteht, ist **verworfen**. Nicht repariert.

Fallen alle vier einer Baustelle: Wirf die ganze Denkrichtung weg und fang mit vier grundsätzlich anderen Familien an. Nicht dieselben Ideen in neuer Verpackung.

### Runde 4 — Nachschub aus anderer Familie

Für jeden verworfenen Entwurf einen neuen **aus einer anderen Familie**. Nicht die verbesserte Fassung des Gescheiterten — der Fehler des Vorgängers sagt etwas über den Suchraum, er ist keine Reparaturanleitung.

Dann zurück zu Runde 2.

### Abbruch

- Pro Baustelle haben **mindestens zwei Entwürfe aus verschiedenen Familien** drei Angriffsrunden überstanden und schlagen den Nullpunkt, **oder**
- acht Familien sind durch und keine übersteht — dann schreib genau das auf, das ist ein echtes Ergebnis, **oder**
- die Rundenbegrenzung greift.

---

## Kontext schonen

Dein Kontextfenster füllt sich schnell, und die Qualität sinkt, wenn es voll wird. Zwei Regeln:

Nutze **Subagenten für das Durchsuchen des Quellcodes**, nicht nur für die Angriffe. Ein Subagent liest die Dateien und berichtet die Zusammenfassung — die gelesenen Dateien landen dann nicht in deinem Hauptkontext.

Schreib Zwischenergebnisse **in Dateien statt sie im Kopf zu behalten**. `VERWORFEN_SPEICHERN.md` wird fortlaufend geführt, nicht am Ende aus der Erinnerung geschrieben.

---

## Das Verwurfsprotokoll

Fortlaufend in `VERWORFEN_SPEICHERN.md`:

```
### Entwurf <Nr> — <Baustelle> — <Familie> — Runde <n>
Idee in einem Satz:
Gescheitert an (Kriterium + Szenario):
Was das über den Suchraum sagt:
```

**Keine Idee zweimal.** Vor jedem neuen Entwurf das Protokoll prüfen.

---

## Das Ergebnis: `ENTWURF_SPEICHERN.md`

### Ganz oben, bevor irgendetwas anderes kommt: Kurzfassung, maximal eine Seite

Der Nutzer hat das letzte Dokument nicht gelesen — es war zu lang. Diese Kurzfassung ist für jemanden geschrieben, der **nur sie** liest und danach handeln können muss:

- Was ist das eigentliche Problem, in drei Sätzen, ohne Fachbegriffe
- Was empfiehlst du, in drei Sätzen
- Die Einfügereihenfolge als nummerierte Liste mit Zeitangabe
- Der eine Test, der beweist, dass es funktioniert hat
- Welche Annahme unbestätigt ist und was passiert, falls sie nicht stimmt

### Danach, pro Baustelle

Nullpunkt mit zitierten Originalformeln und belegter Bewertung. Dann die Überlebenden, je mit:

- Idee in drei Sätzen, einfache Sprache
- Vollständige Formeln zum Einfügen, pro Steuerelement und Property einzeln
- Bewertung nach allen sechs Kriterien, mit Belegen
- Die überstandenen Angriffe und wer sie geführt hat
- Was zusätzlich nötig ist (SharePoint-Spalte, Flow, Steuerelement)
- Einfügereihenfolge mit Zeitangabe
- **Testschritte**: was der Nutzer klickt, was herauskommen muss, und woran er merkt, dass er etwas vergessen hat

### Empfehlung

Welcher Entwurf, in einem Absatz, mit dem Preis der Entscheidung ausgeschrieben. Nenne ausdrücklich, was der unterlegene Entwurf besser kann — der Nutzer will abwägen, nicht überredet werden.

### UNSICHER

Alles, was du nicht aus dem Quellcode belegen konntest, an einer Stelle gesammelt. **Pro Punkt dazuschreiben, was du versucht hast, um ihn aufzulösen.** `UNSICHER` ist kein Ausweg, sondern die Antwort nach einem ernsthaften Versuch.

Markiere, welche Punkte sich in dreißig Sekunden im Studio klären lassen — die beantwortet der Nutzer sofort.

---

## Harte Regeln

- **Deutsche Locale:** `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet Anweisungen.
- **Niemals Kommentare in Power Fx.** Erklärungen gehören in den Fließtext.
- **Keine Platzhalter.** Jede Formel muss so einfügbar sein, wie sie dasteht. Steuerelement- und Spaltennamen aus `./src`, niemals erfunden.
- **Die Spalte heißt `Titel`, nicht `Title`** (79 zu 0 im Quellcode). `Tische.Aktiv` existiert nicht, `Standort` heißt `Geschoss`. Siehe `KORREKTUR_2.md`.
- **Neu anlegen** → `Collect(Quelle; Tabelle)`. **Ändern** → `Patch(Quelle; Tabelle)` mit `ID`-Spalte. **Löschen** → `Remove(Quelle; Tabelle)`.
- `Patch` nie direkt auf eine Variable, immer auf frischem `LookUp(...; ID = ...)`.
- Volles Personenschema, Lookup mit `Id` **und** `Value`.
- Jede Schreiboperation in `IfError` mit deutscher Meldung.
- **Du öffnest, bearbeitest und packst keine App.** Der Quellcode ist ein Röntgenbild. Der Nutzer fügt alles von Hand im Studio ein.
- **Zeig Belege, nicht Behauptungen.** Jede Zählung mit der Zeile, aus der sie stammt.
- **`KORREKTUR_2.md` sticht `KONTEXT.md`.** Abschnitt 2 von `KONTEXT.md` stammt aus der falschen App und ist Hypothese, nicht Befund.
