# AUFGABE_SCHLEIFE.md — Mehrfachauswahl neu denken

**Voraussetzung:** `./src` existiert und ist lesbar, `INVENTAR.md` ist fertig. Ohne die echten aktuellen Formeln arbeitet diese Schleife im Blindflug — dann `STOPP.md` schreiben und abbrechen.

---

## Worum es geht

Speichern und Stornieren mit Mehrfachauswahl sind zu langsam. Das ist der wichtigste Performance-Punkt der ganzen App.

**Du sollst nicht die bestehende Lösung reparieren. Du sollst sie mehrfach komplett neu erfinden und die schlechten Entwürfe wegwerfen.**

Josias hat beobachtet, dass in diesem Projekt der Neubau regelmäßig besser funktioniert hat als das Flicken — bei den Buttons war „komplett neu bauen und das Problem umgehen" jedes Mal erfolgreicher als „den Fehler suchen". Genau diese Haltung ist hier gefragt: **Ein Entwurf, der ein Problem unmöglich macht, schlägt jeden Entwurf, der es abfängt.**

---

## Warum das keine gewöhnliche Optimierungsschleife ist

Du kannst die App nicht ausführen und nichts messen. Eine Schleife „ausprobieren, messen, verbessern" ist hier unmöglich, und so zu tun als ob wäre Selbstbetrug.

Was du **stattdessen** kannst, und das reicht völlig: Entwürfe **gegeneinander antreten lassen und sie angreifen**. Die Bewertung ist nicht Messung, sondern Beweisführung — du kannst an der Formel ablesen, wie viele Datenzugriffe sie erzeugt, ob sie delegierbar ist und woran sie zerbricht.

---

## Die Bewertungskriterien

Nach diesen sechs Punkten bewertest du jeden Entwurf. Sie sind alle **ohne Ausführen** beurteilbar.

1. **Anzahl der Datenquellen-Zugriffe** bei 1, 5, 20 und 50 ausgewählten Buchungen. Zähl sie aus der Formel ab. Weniger ist besser. **Das ist das wichtigste Kriterium.**
2. **Delegierbarkeit** — löst der Entwurf eine Delegierungswarnung aus? Wenn ja, wie viele Zeilen zieht er dann herunter?
3. **Verhalten bei Gleichzeitigkeit** — was passiert, wenn ein anderer Nutzer im selben Moment dieselbe Buchung ändert oder löscht? Der bekannte Fehler „Item Not Found bei sichtbarem Eintrag" muss hier beantwortet sein.
4. **Wartungsfläche** — an wie vielen Stellen muss dieselbe Logik gepflegt werden? Weniger ist besser. Formula Drift ist der Dauerbrenner dieses Projekts.
5. **Was der Nutzer bei einem Fehler sieht.** Nie ein roher Connector-Fehler.
6. **Einfügeaufwand** — wie viele Steuerelemente muss Josias anfassen? Jede Änderung kostet ihn Zeit im Studio.

---

## Der Ablauf

### Runde 0 — Bestandsaufnahme

Lies die aktuellen Formeln für Mehrfachauswahl-Speichern und -Stornieren aus `./src`. Bewerte sie nach den sechs Kriterien. **Das ist dein Nullpunkt** — jeder Entwurf muss ihn schlagen, sonst fliegt er raus.

Schreib den Nullpunkt vollständig auf, inklusive der Originalformeln.

### Runde 1 — Vier grundverschiedene Familien

Entwirf **vier Ansätze, die sich im Prinzip unterscheiden**, nicht in Details. Vier Varianten derselben Idee sind keine vier Ansätze.

Der Suchraum, damit du nicht zu eng denkst — das ist keine Auswahlliste, sondern ein Anstoß:

- Sammelaufruf statt Schleife (`Remove` und `Patch` nehmen Tabellen, `Collect` auch)
- Bedingungsbasiert statt datensatzbasiert (`RemoveIf` über ein Kriterium)
- **Weich löschen statt hart löschen** — eine Statusspalte per Sammel-`Patch` setzen, das tatsächliche Löschen macht nachts der bestehende Aufräum-Flow. Umgeht die Lösch-Race-Condition vollständig, statt sie abzufangen.
- Schreiben auslagern an einen Power-Automate-Flow, der die SharePoint-Batch-Schnittstelle nutzt
- Optimistische Oberfläche: lokale Collection sofort aktualisieren, Datenquelle im Hintergrund
- Die Mehrfachauswahl abschaffen und durch etwas ersetzen, das dasselbe Bedürfnis anders löst

Pro Familie: vollständige, einfügbare Power-Fx-Formeln und die Bewertung nach allen sechs Kriterien.

### Runde 2 — Angriff

Jetzt wechselst du die Rolle. **Greife jeden der vier Entwürfe an, als wolltest du ihn zerstören.** Für jeden mindestens drei konkrete Szenarien, in denen er bricht:

- Zwei Nutzer gleichzeitig
- Der Datensatz existiert serverseitig nicht mehr
- Netzwerk bricht mitten im Vorgang ab
- 50 statt 5 Einträge
- SharePoint drosselt und antwortet mit 429
- Eine Buchung wird zwischen Auswahl und Bestätigung von jemand anderem verlängert

Schreib die Angriffe und ihr Ergebnis auf. Nicht beschönigen — einen Entwurf, den du selbst gebaut hast, verteidigst du nicht.

### Runde 3 — Wegwerfen

**Jeder Entwurf, der einen Angriff nicht übersteht, wird verworfen — nicht nachgebessert.**

Das ist der Kern dieser Aufgabe. Widersteh dem Reflex, einen kaputten Entwurf zu retten. Wenn drei von vier fallen, fallen drei von vier.

Wenn **alle vier** fallen: Wirf die gesamte Denkrichtung weg und fang bei Runde 1 mit vier grundsätzlich anderen Familien neu an. Nicht dieselben Ideen in neuer Verpackung.

### Runde 4 — Nachschub

Für jeden verworfenen Entwurf entwirfst du einen neuen, der **aus einer anderen Familie** kommt. Nicht die verbesserte Fassung des Gescheiterten. Der Fehler des Vorgängers ist eine Information über den Suchraum, keine Reparaturanleitung.

Dann zurück zu Runde 2.

### Abbruch

Hör auf, wenn eines davon eintritt:

- **Mindestens zwei Entwürfe aus verschiedenen Familien haben drei Angriffsrunden überstanden** und schlagen den Nullpunkt deutlich bei Kriterium 1, **oder**
- du hast **acht Familien** durch und keine übersteht die Angriffe — dann schreib genau das auf, das ist ein wertvolles Ergebnis, **oder**
- die Rundenbegrenzung greift.

---

## Das Verwurfsprotokoll

Führe durchgehend `VERWORFEN.md` mit:

```
### Entwurf <Nr> — <Familie> — Runde <n>
Idee in einem Satz:
Gescheitert an:
Was das über den Suchraum sagt:
```

**Kein Entwurf wird zweimal probiert.** Vor jedem neuen Entwurf prüfst du dieses Protokoll. Wenn eine Idee darin schon steht, ist sie erledigt.

---

## Das Ergebnis

Eine Datei `ENTWURF_MEHRFACHAUSWAHL.md`:

1. **Nullpunkt** — die heutigen Formeln, vollständig zitiert, mit Bewertung
2. **Die Überlebenden** — mindestens zwei, aus verschiedenen Familien. Pro Entwurf:
   - Idee in drei Sätzen, in einfacher Sprache
   - Vollständige Formeln zum Einfügen, pro Steuerelement und Property getrennt
   - Bewertung nach allen sechs Kriterien
   - Die überstandenen Angriffe
   - Was zusätzlich nötig ist (neue Spalte in SharePoint, Flow, neues Steuerelement)
   - Einfügereihenfolge Schritt für Schritt
   - **Testschritte für Josias** — was er klickt und was dabei herauskommen muss
3. **Empfehlung** — welcher der beiden, in einem Absatz, mit dem Preis der Entscheidung
4. **Verworfen** — Verweis auf `VERWORFEN.md`, plus drei Sätze, was du über das Problem gelernt hast
5. **UNSICHER** — alles, was du nicht aus dem Quellcode belegen konntest, gesammelt

---

## Harte Regeln

- **Deutsche Locale:** `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet.
- **Niemals Kommentare in Power Fx.** Erklärungen gehören in den Fließtext.
- **Keine Platzhalter.** Jede Formel muss so einfügbar sein, wie sie dasteht. Steuerelementnamen aus `./src`, nicht erfunden.
- **Neu anlegen** → `Collect(Quelle; Tabelle)`. **Ändern** → `Patch(Quelle; Tabelle)` mit `ID`-Spalte. **Löschen** → `Remove(Quelle; Tabelle)`.
- `Patch` nie direkt auf eine Variable, immer auf frischem `LookUp(...; ID = ...)`.
- Volles Personenschema, Lookup mit `Id` **und** `Value`.
- **Du öffnest, bearbeitest und packst keine App.** Der Quellcode ist ein Röntgenbild. Josias fügt alles selbst im Studio ein.
- **Wo du etwas nicht belegen kannst, schreibst du `UNSICHER`.** Eine erfundene Formel kostet ihn morgen eine halbe Stunde Fehlersuche. Eine ehrliche Frage kostet ihn dreißig Sekunden.
