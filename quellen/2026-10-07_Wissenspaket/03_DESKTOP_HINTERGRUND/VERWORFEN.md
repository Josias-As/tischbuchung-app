# VERWORFEN.md — Verwurfsprotokoll Mehrfachauswahl

**Erstellt:** 01.10.2026
**Grundlage:** `INVENTAR.md` Abschnitt 8, Quellcode `./src/Src/Screen1.pa.yaml`

Dieses Protokoll ist die Sperrliste. **Keine Idee, die hier steht, wird ein zweites Mal probiert.**

Durchlaufene Familien: **sechs.** Überlebt: **zwei** (A — Sammelaufruf, C — Weich löschen). Verworfen: **vier.**

---

### Entwurf B — Bedingungsbasiert (`RemoveIf` über ein fachliches Kriterium) — Runde 2

**Idee in einem Satz:**
Statt eine Liste von Datensätzen zu löschen, löscht man eine *Bedingung* — `RemoveIf(Tischbuchungen; Person.Email = User().Email && Startzeit >= varTagStart && Startzeit < varTagEnde)` — und ersetzt die Zeilenauswahl durch die Auswahl eines Tages oder Zeitraums.

**Gescheitert an:** Angriff 6 — „Eine Buchung wird zwischen Auswahl und Bestätigung von jemand anderem angelegt oder verlängert."

Der Server wertet die Bedingung im Moment des Löschens aus, nicht im Moment der Auswahl. Legt der Nutzer in einem zweiten Browser-Tab, oder ein Kollege mit Zugriff auf dieselbe Liste, zwischen dem Öffnen des Dialogs und dem Klick auf „Stornieren" eine Buchung an, die in den Zeitraum fällt, **wird sie mitgelöscht, obwohl der Nutzer sie nie gesehen und nie angehakt hat.** Dasselbe gilt für eine Buchung, die durch Verlängern erst in das Fenster hineinwächst.

Das ist stiller Datenverlust ohne Fehlermeldung. Bei den Entwürfen A, C und D kann im schlimmsten Fall ein Löschvorgang fehlschlagen — hier geht etwas verloren, das niemand löschen wollte, und niemand merkt es.

Verschärfend: `Person.Email` als Filterbedingung ist in `INVENTAR.md` Abschnitt 3 als ungeklärt markiert. Wenn `RemoveIf` nicht delegiert, arbeitet es auf den ersten 2000 Zeilen — bei einer Löschoperation ist „arbeitet auf einer Teilmenge" ungleich schlimmer als bei einer Anzeige.

**Was das über den Suchraum sagt:**
Die Trennung von *Auswahlzeitpunkt* und *Auswertungszeitpunkt* ist bei Leseoperationen harmlos und bei Löschoperationen gefährlich. Genau die Eigenschaft, die `RemoveIf` bei Angriff 1 und 2 stark macht (der Server entscheidet, nichts kann veralten), macht es bei Angriff 6 untragbar. **Eine Löschoperation muss an eine geschlossene Menge gebunden sein, die der Nutzer gesehen hat — an IDs, nicht an ein Kriterium.** Diese Einsicht gilt für jeden weiteren Entwurf: Wer die Menge erst zur Laufzeit bestimmt, löscht irgendwann etwas Fremdes.

---

### Entwurf D — Schreiben an einen Power-Automate-Flow auslagern — Runde 2

**Idee in einem Satz:**
Die App übergibt nur die Liste der IDs an einen Flow (`Concat(colAusgewaehlteBuchungen; ID; ",")`), der Flow löscht sie über die SharePoint-Batch-Schnittstelle, und die App wartet auf ein Ergebnis.

**Gescheitert an:** Angriff 3 — „Netzwerk bricht mitten im Vorgang ab."

Der Aufruf `<Flow>.Run(...)` ist aus Sicht der App synchron, aus Sicht des Systems aber ein Auftrag an einen Dienst, der eigenständig weiterläuft. Bricht die Verbindung nach dem Absenden und vor der Antwort ab, bekommt die App einen Fehler — **der Flow löscht trotzdem weiter.** Die App zeigt „Stornieren fehlgeschlagen", und die Buchungen sind weg. Der Nutzer klickt erneut, sieht erneut einen Fehler oder eine leere Liste, und hat keine Möglichkeit festzustellen, was tatsächlich passiert ist. Bei A und C bleibt die Wahrheit nach einem Abbruch immer in der Liste ablesbar — hier nicht.

Zwei weitere Gründe, die allein nicht zum Verwurf gereicht hätten, zusammen aber dagegen sprechen:

- **Nicht lieferbar.** Der Flow existiert nicht. Jede Formel, die ich dafür schriebe, enthielte einen erfundenen Namen — das ist in `AUFGABE_SCHLEIFE.md` ausdrücklich ausgeschlossen, und zwar aus gutem Grund.
- **Zwei Systeme statt einem.** Power Apps Studio hat keinen Debugger. Der Flow-Designer hat einen eigenen, getrennten Ausführungsverlauf. Ein Fehler kann ab dann in beiden Systemen liegen, und niemand sieht beide gleichzeitig. Für eine Person, die diese App allein pflegt, ist das ein dauerhafter Aufschlag auf jede künftige Fehlersuche.

**Was das über den Suchraum sagt:**
Auslagern verschiebt die Arbeit, aber es verschiebt auch die Wahrheit. Sobald der Schreibvorgang außerhalb der App stattfindet, verliert die App die Fähigkeit, nach einem Abbruch zu sagen, was geschehen ist — es sei denn, man baut einen Rückkanal, und der ist teurer als das Problem. **Die Lösung muss innerhalb der App bleiben, damit ein Abbruch immer durch ein Neuladen der Liste geklärt werden kann.** Das ist das stärkste Argument für A und C: beide hinterlassen nach jedem Abbruch einen Zustand, den `Refresh` sichtbar macht.

---

### Entwurf E — Optimistische Oberfläche — Runde 4 (Nachschub für B)

**Idee in einem Satz:**
Die Zeilen sofort aus einer lokalen Anzeige-Collection entfernen, damit die Oberfläche augenblicklich reagiert, und den Schreibvorgang gegen SharePoint im Hintergrund laufen lassen.

**Gescheitert an:** der Prämisse — noch vor dem ersten Angriff.

**Power Fx kennt keinen Hintergrundschreibvorgang.** Es gibt kein `Async`, kein Fire-and-forget, keinen Rückruf. `Concurrent()` führt Ausdrücke parallel aus, blockiert die Formel aber bis zum letzten Ergebnis. Die Oberfläche kann also lokal sofort aktualisiert werden, aber der Nutzer wartet trotzdem — er sieht die Zeile verschwinden und kann danach nichts anfassen, bis der Schreibvorgang durch ist. Der einzige echte Gewinn wäre, dass das Verschwinden *vor* der Wartezeit kommt statt danach. Das ist Kosmetik, kein Entwurf.

Schlimmer: Weicht der lokale Stand vom Server ab, weil ein Schreibvorgang fehlschlug, zeigt die App dauerhaft etwas Falsches an, und zwar genau in die Richtung, die am meisten schadet — die Buchung ist noch da, der Nutzer glaubt, sie sei storniert, und erscheint nicht zur Arbeit an einem Tisch, den er weiterhin blockiert.

**Was das über den Suchraum sagt:**
Die Suche nach „gefühlt schneller" ist in dieser Umgebung eine Sackgasse. Power Fx gibt keine Nebenläufigkeit her, mit der man echte Wartezeit verstecken könnte. **Der einzige Weg zu „schneller" ist „weniger Zugriffe", nicht „Zugriffe verstecken".** Damit ist Kriterium 1 aus `AUFGABE_SCHLEIFE.md` nicht nur das wichtigste, sondern faktisch das einzige, an dem sich Geschwindigkeit überhaupt bewegen lässt.

---

### Entwurf F — Mehrfachauswahl abschaffen, durch „Serie stornieren" über `SerienID` ersetzen — Runde 4 (Nachschub für D)

**Idee in einem Satz:**
Die Zeilenauswahl ganz streichen; stattdessen bei der Serienbuchung die bereits vorhandene, ungenutzte Spalte `Tischbuchungen.SerienID` befüllen und einen einzigen Knopf „Diese Serie ab heute stornieren" anbieten, der mit `RemoveIf(Tischbuchungen; SerienID = varSerie && Startzeit >= varAbDatum)` auskommt.

**Gescheitert an:** Angriff 4 — „50 statt 5 Einträge" — allerdings in umgekehrter Richtung als erwartet.

Der Entwurf ist bei einer Serie unschlagbar: ein Aufruf, konstante Kosten, keine ID-Liste, nichts kann veralten. Er deckt aber **den Anwendungsfall nicht ab, um den es hier geht.** `galAlleTischbuchungen.Items` zeigt *alle* künftigen Buchungen des Nutzers, quer über beliebig viele Serien und Einzelbuchungen hinweg. Will jemand fünf Buchungen stornieren, die aus drei verschiedenen Serien und zwei Einzelbuchungen stammen — der typische Fall bei 20 bis 50 Einträgen — leistet dieser Entwurf gar nichts. Er ersetzt die Mehrfachauswahl nicht, er beantwortet eine andere Frage.

Zusätzlich erbt er die Schwäche von Entwurf B: `RemoveIf` wertet zur Laufzeit aus. Wächst eine Serie zwischen Anzeige und Klick, löscht er mehr als gezeigt.

**Was das über den Suchraum sagt:**
Das Bedürfnis hinter der Mehrfachauswahl ist **nicht** „Serien verwalten", sondern „mehrere beliebige eigene Buchungen auf einmal loswerden". Diese Beliebigkeit ist der Kern der Anforderung und lässt sich nicht wegdefinieren.

**Trotzdem ist hier etwas Wertvolles entstanden, das nicht verloren gehen darf:** `SerienID` existiert bereits in `Tischbuchungen` (Typ `string`, read-write, filterbar mit `eq` und `startswith`) und wird von der App nirgends benutzt. Für die **Serienbuchung** — Punkt 2.d in `AUFGABE_UMBAU.md`, nicht Teil dieses Laufs — ist das genau die fehlende Zutat: Beim Anlegen einer Serie ein `GUID()` in alle Datensätze schreiben, dann ist die Serie später als geschlossene Menge adressierbar, ohne dass man sie aus Datum und Uhrzeit rekonstruieren muss. Das gehört in Schritt 3 der Umbauliste.

---

## Was ich über das Problem gelernt habe

**Erstens: Das Problem ist nicht die Schleife, sondern die Herkunft der Datensätze.** Die naheliegende Lesart war „`ForAll` raus, Sammelaufruf rein, fertig". Das halbiert zwar die Zugriffszahl auf eine Konstante, lässt aber den gemeldeten Fehler „Item Not Found bei sichtbarem Eintrag" unberührt — denn `colAusgewaehlteBuchungen` ist eine Kopie, die beim Anhaken entstand und beliebig alt sein kann. Jeder Entwurf, der diese Kopie direkt an `Remove` weiterreicht, erbt den Bug, egal wie elegant er sonst ist.

**Zweitens: Bei Löschoperationen schlägt eine geschlossene Menge jede Bedingung.** Das hat zwei Entwürfe gekostet (B und F). Was bei einer Anzeige ein Vorteil ist — der Server entscheidet frisch —, ist beim Löschen das Risiko, Fremdes zu treffen.

**Drittens: Die beiden Überlebenden lösen unterschiedliche Hälften desselben Problems.** A macht das Löschen schnell und ehrlich, lässt die Gleichzeitigkeit aber ein kleines Zeitfenster offen. C schließt die Gleichzeitigkeit vollständig, weil zweimal „storniert" setzen harmlos ist, bezahlt das aber mit einer neuen Spalte und rund fünfzehn Abfragen, die alle angepasst werden müssen. Das ist keine Geschmacksfrage, sondern eine echte Abwägung — sie steht in `ENTWURF_MEHRFACHAUSWAHL.md` unter „Empfehlung".
