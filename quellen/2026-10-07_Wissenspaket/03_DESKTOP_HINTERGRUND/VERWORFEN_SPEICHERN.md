# VERWORFEN_SPEICHERN.md — Verwurfsprotokoll Speichern

Fortlaufend geführt. **Keine Idee, die hier steht, wird ein zweites Mal probiert.**

**Stand: 03.10.2026**

---

## Vorab ausgeschlossen, ohne eigene Runde

### Power-Automate-Flow als Schreibweg

**Idee in einem Satz:** Die App übergibt die zu schreibenden Datensätze an einen Flow, der sie über die SharePoint-Batch-Schnittstelle anlegt.

**Nicht erneut geprüft.** Diese Familie wurde im Stornieren-Lauf angegriffen und verworfen (`VERWORFEN.md`, Entwurf D). Begründung dort: Bricht die Verbindung nach dem Absenden und vor der Antwort ab, bekommt die App einen Fehler, während der Flow weiterarbeitet — die App kann danach nicht mehr feststellen, was tatsächlich geschehen ist. Beim Schreiben wiegt das schwerer als beim Löschen, weil ein verlorener Schreibvorgang nicht am leeren Platz erkennbar ist. Dazu die unveränderten Nebengründe: ein Flow lässt sich aus der Quellcode-Analyse nicht als einfügefertige Formel liefern, und er verteilt die Fehlersuche auf zwei Werkzeuge mit getrennten Ausführungsverläufen.

---

## Runde 1 — vor der Angriffsrunde strukturell ausgeschieden

Diese zwei Entwürfe scheitern an ihrer Struktur, nicht an Formeldetails. Formeln wurden deshalb nicht ausgearbeitet — jede Formel hätte denselben Mangel, und ein Angriff hätte nur bestätigt, was schon aus dem Aufbau folgt. Das ist ausdrücklich vermerkt, damit später niemand denkt, sie seien übersehen worden.

---

### Entwurf 1D — Baustelle 1 — „Ersetzen statt ändern" — Runde 1

**Idee in einem Satz:** Die ausgewählten Buchungen werden in einem `Remove` storniert und in einem `Collect` mit den neuen Zeiten neu angelegt, sodass Verlängern und Verkürzen auf den bereits gebauten Sammel-Löschweg zurückfallen.

**Gescheitert an: Kriterium 1, Doppelbuchung — und zwar unmittelbar durch den Aufbau.**

Zwischen `Remove` und `Collect` ist der Tisch **nachweislich frei**. Das ist kein schmales Zeitfenster wie bei einem Lesen-dann-Schreiben, sondern ein Zustand, der tatsächlich in SharePoint steht und den jeder andere Nutzer in seinem Grundriss als grüne Kachel sieht. Bricht die Verbindung dazwischen ab, ist die Buchung **ersatzlos weg** — der Nutzer wollte sie um eine Stunde verlängern und hat sie verloren. Das ist schlechter als der Ist-Zustand, in dem gar nichts passiert.

Drei weitere Folgen, die jede für sich schon gegen den Entwurf sprechen:
- **`CheckedIn` geht verloren.** Wer bereits eingecheckt war, ist nach dem Verlängern ausgecheckt. Die Anzeige im Dashboard springt von „Eingecheckt" zurück auf „Einchecken".
- **Die `ID` ändert sich.** Jede Variable, die noch auf die alte Buchung zeigt — `varSelectedBuchung`, `varSelectedBuchungTab`, `varGeklickteBuchungKlein`, `colAusgewaehlteBuchungen` — zeigt danach ins Leere. Genau das erzeugt den bereits bekannten Fehler „Item Not Found".
- **`SerienID` und `Titel` müssten von Hand mitkopiert werden.** Jedes Feld, das später dazukommt, muss hier nachgetragen werden, sonst verschwindet es beim Verlängern still.

**Was das über den Suchraum sagt:** Eine Änderung in Löschen-plus-Neuanlegen zu zerlegen ist in einem System ohne Transaktionen immer ein Rückschritt, egal wie bequem die Wiederverwendung des vorhandenen Löschwegs wirkt. Der Unterschied zwischen „ein Feld ändern" und „einen Datensatz ersetzen" ist nicht Geschmack, sondern die Frage, ob zwischendurch ein Zustand existiert, den niemand gewollt hat. **Für Baustelle 1 bleibt damit nur der Weg über `Patch` auf bestehende Datensätze** — alle drei verbleibenden Entwürfe gehen ihn.

---

### Entwurf 2D — Baustelle 2 — „Die Serie als ein Datensatz" — Runde 1

**Idee in einem Satz:** Statt bis zu 14 Zeilen wird eine einzige Zeile mit einer Wiederholungsregel gespeichert (Startdatum, Enddatum, Uhrzeiten, Wochentagsmuster), die beim Lesen zu einzelnen Terminen aufgefächert wird.

**Gescheitert an: Kriterium 5, Wartungsfläche — in einem Ausmaß, das den gesamten übrigen Umbau blockiert.**

Der Schreibvorgang wäre unschlagbar: ein `Patch`, konstant, unabhängig von der Serienlänge. Der Preis fällt aber vollständig auf der Leseseite an, und dort steht er quer zu allem, was sonst auf der Liste steht.

Im Quellcode lesen **mindestens 24 Abfragen** `Tischbuchungen` als flache Liste von Einzelterminen. Jede davon müsste die Auffächerung beherrschen: die sechs Properties der Master-Bedingung mit ihren zwölf `LookUp`-Aufrufen, `galAlleTischbuchungen.Items`, `galTischbuchungenHeute.Items`, die Kollisionsprüfungen in `btn5Std`, `btn9Std` und den sechs Plus-Knöpfen, und beide Speichern-Knöpfe. Eine Wiederholungsregel lässt sich in SharePoint nicht serverseitig filtern, also wäre **jede** dieser Abfragen nicht mehr delegierbar — und Delegation ist der nächste Punkt auf der Umbauliste. Der Entwurf macht die unmittelbar folgende Arbeit unmöglich.

Dazu kommt ein fachlicher Bruch: Ein einzelner Termin einer Serie ließe sich nicht mehr einzeln stornieren, verlängern oder einchecken, ohne die Regel in Ausnahmen zu zerlegen. `CheckedIn` ist ein Feld pro Zeile — bei einer Regelzeile gäbe es nichts, worauf es sich beziehen könnte. Die Check-in-Funktion der App wäre damit für Serienbuchungen nicht mehr abbildbar.

**Was das über den Suchraum sagt:** Die Schreibkosten zu senken, indem man die Datenstruktur verdichtet, verschiebt die Kosten nur auf die Leseseite — und die ist in dieser App zwanzigmal so groß wie die Schreibseite. Bei einer App mit 24 Leseabfragen und zwei Schreibwegen gilt: **die Zeile bleibt die Einheit, und die Serie wird über eine Kennung zusammengehalten, nicht über eine Regel.** Genau das macht `SerienID`, und genau deshalb ist sie in 2B die richtige Zutat statt einer Regelspalte.

---

## Runde 2 — Angriffe durch Subagenten

Sechs Entwürfe wurden je einem Subagenten in frischem Kontext zur Prüfung gegeben: 1A, 1B, 1C, 2A, 2B, 2C. Die Subagenten kennen die Entwürfe und die sechs Kriterien, aber nicht die Begründung, warum ich sie für tragfähig halte.

---

### Entwurf 1C — Baustelle 1 — „Absolute Zielzeit statt Delta" — Runde 2

**Idee in einem Satz:** Die sechs Dauer-Knöpfe weichen einem Dropdown „neues Ende: 15:00 / 16:00 / …", wodurch die Operation wiederholbar wird — zweimal „bis 17:00" ändert beim zweiten Mal nichts.

**Gescheitert an: Kriterium 2, Ehrlichkeit — fünffach.** Dazu ein Blocker, der noch vor den Kriterien liegt.

Der Prüfer hat dreizehn Befunde geliefert. Die, die den Entwurf erledigen:

**Der Blocker: 1C speichert nie.** 1C ersetzt die sechs Dauer-Knöpfe, lässt aber den aus 1A geerbten Wächter `If(IsBlank(varDauerKlein); Notify("Bitte eine Dauer auswählen."; …); …)` stehen. Die einzigen Setzer von `varDauerKlein` waren eben jene sechs Knöpfe. Die Variable ist damit dauerhaft `Blank()`, der Speichern-Zweig unerreichbar. Mein Fehler beim Ableiten von 1A — und genau die Art Fehler, die der Nutzer morgens nicht suchen soll.

**Eine Zielzeit in der Vergangenheit löscht die Buchung faktisch.** Die Prüfung lautet nur `PlanEndeNeu > PlanStart`, eine Bedingung gegen `Now()` fehlt. Es ist 16:00, eine Buchung läuft 09:00–18:00, der Nutzer wählt „09:30": die Prüfung besteht, es wird geschrieben, und die Buchung fällt aus `Filter(Tischbuchungen; Endzeit >= Now())` heraus. Sie verschwindet aus der Galerie, der Tisch gilt als frei, der Nutzer sitzt daran, und die Meldung sagt „1 Buchungen geändert." Verschärfend: Der erste Dropdown-Eintrag „08:00" steht als Vorauswahl da.

**Eine absolute Zielzeit passt nicht zu einer Auswahl über mehrere Tage.** `galAlleTischbuchungen` liefert alle künftigen Buchungen über beliebig viele Tage, und `chkAlleAuswählen` sammelt sie alle ein. „17:00" bedeutet dann „17:00 an je anderem Tag". Der Dialog zeigt aber nur ein einziges Datum (`lblVerwaltenKleinDatum` liest `varGeklickteBuchungKlein.Startzeit`). Der Nutzer sieht Donnerstag, wählt 17:00 und ändert ungesehen Buchungen in der übernächsten Woche mit.

**Verlängern und Verkürzen werden ununterscheidbar.** Fünf Buchungen, drei enden 18:00, zwei enden 12:00, Ziel 17:00 — drei werden gekürzt, zwei verlängert, Meldung „5 Buchungen geändert." Weil 1C die sechs Knöpfe streicht, entfällt zugleich deren Farb- und `DisplayMode`-Vorschau ersatzlos. Der Nutzer wählt blind.

**Eingecheckte Buchungen werden ohne Hinweis gekürzt.** `CheckedIn` wird nirgends gelesen. Wer um 13:00 eingecheckt ist und bis 19:00 gebucht hat, bekommt seine laufende Buchung auf 17:00 gekürzt, wenn er nebenbei vier andere verlängern wollte.

**Und die Wiederholbarkeit, das einzige Argument für 1C, liefert sie nicht.** Beim zweiten Durchlauf besteht eine bereits auf 17:00 stehende Buchung alle Prüfungen erneut und wird erneut gepatcht. Vier Datenquellen-Zugriffe, `Modified` und `Editor` werden in SharePoint neu gesetzt, und der Nutzer liest „5 Buchungen geändert." für fünf Buchungen, bei denen sich nichts geändert hat. **Idempotent ist das Ergebnis, nicht die Operation** — und die Meldung ist falsch.

Nicht beanstandet wurde Kriterium 1: Das Fenster zwischen Lesen und Schreiben umfasst drei lokale `ClearCollect` und einen Rundlauf und ist damit kleiner als im Ist-Zustand. Daran lag es nicht.

**Was das über den Suchraum sagt:** Eine Operation wiederholbar zu machen, indem man von einem Delta auf einen absoluten Zielwert umstellt, funktioniert nur, wenn **alle** betroffenen Datensätze denselben Bezugsrahmen haben. Hier haben sie das nicht: verschiedene Tage, verschiedene Startzeiten, verschiedene Check-in-Zustände. Der absolute Wert erzwingt eine Gleichbehandlung, die fachlich falsch ist, und verwandelt eine Verlängerung nebenbei in eine Verkürzung. **Ein Delta respektiert die Unterschiede zwischen den ausgewählten Datensätzen, ein Zielwert plättet sie.** Für eine Auswahl heterogener Datensätze ist das relative Verfahren das richtige — die Wiederholbarkeit muss anders kommen, nämlich über eine Sperre gegen den zweiten Klick, nicht über die Rechenvorschrift.

**Zusätzlich gelernt, mit Folgen für die anderen Entwürfe dieser Baustelle:** Der Prüfer hat drei Mängel gefunden, die 1C aus 1A geerbt hat und die damit auch 1A und 1B betreffen. Sie sind unter „Übergreifende Befunde" unten festgehalten und werden dort behandelt, nicht hier.

---

### Entwurf 1A — Baustelle 1 — „Sammel-`Patch`, Teilerfolg erlaubt" — Runde 2

**Idee in einem Satz:** Ein Lesevorgang beim Öffnen des Dialogs versorgt Knopffarben und Kollisionsprüfung, beim Speichern ein zweiter Lesevorgang, dann ein `Patch` für alle Betroffenen; Kollidierende werden übersprungen und gezählt.

**Gescheitert an: Kriterium 2 (Ehrlichkeit) und Kriterium 3 (Zugriffe).**

**Die Meldung lügt in beide Richtungen.** Grün für eine geschriebene Doppelbuchung, wenn der Bestand abgeschnitten wurde. Grün für ein anderes Ergebnis als im Dialog zugesagt, wenn jemand die Buchung zwischenzeitlich verlängert hat — der Dialog zeigt die eingefrorene Zeit aus `varGeklickteBuchungKlein`, gerechnet wird auf dem frischen Wert. Grün unter Nennung einer Buchung, die gar nicht angefasst wurde. Und „Keine der ausgewählten Buchungen lässt sich so ändern" sowohl bei einem reinen Leseabbruch als auch bei tatsächlich änderbaren Buchungen.

**Die Kollisionsprüfung weist zu viel ab.** `colNachher` schreibt **jeder** geplanten Buchung ihr neues Ende zu, auch denen, die danach durchfallen. Tisch X, Buchung A 08:00–09:00 und B 09:00–10:00, beide angehakt, „+1 Std": A→10:00 kollidiert echt mit B und wird richtig abgelehnt; B→11:00 wird abgelehnt, weil `colNachher` A bereits mit dem **hypothetischen** Ende 10:00 führt — tatsächlich bleibt A bei 09:00, und B ließe sich einwandfrei verlängern. Die Auswertung ist einstufig und wird nicht bis zum Fixpunkt iteriert. Mein eigener Hinweis „Die Farbe ist ein Hinweis, die Meldung ist die Wahrheit" ist hier genau verkehrt herum.

**Die drei `ClearCollect` haben kein `IfError`.** Bricht der Lesevorgang ab, ist die Collection leer, und der Nutzer bekommt eine fachliche Begründung („belegt oder zu kurz") für ein reines Verbindungsproblem.

**Die Zugriffszahl „4 konstant" ist falsch.** Dazu unten unter Ü5 mehr — das ist der Befund mit den weitesten Folgen.

---

### Entwurf 1B — Baustelle 1 — „Sammel-`Patch`, alles oder nichts" — Runde 2

**Idee in einem Satz:** Wie 1A, aber bei auch nur einer Kollision wird nichts geschrieben und die Zahl der betroffenen Buchungen genannt.

**Gescheitert an: Kriterium 2 (Ehrlichkeit) und Kriterium 3 (Zugriffe).** Dazu ein Blocker.

**Der Blocker: Die App bleibt gesperrt.** Weil 1B den Aufräumblock in den Erfolgszweig verschiebt, ist das abschließende `Set(varIsLoading; false)` in **vier von fünf** Pfaden unerreichbar — Verweigerung, `IfError`-Fehlerzweig, fehlende Dauer, leere Auswahl. `conLadeOverlay` ist ein bildschirmfüllender Container mit `Visible: =varIsLoading`, der über allem liegt. Der häufigste Auslöser ist trivial: Dialog öffnen, „Speichern" drücken, ohne eine Dauer gewählt zu haben. Danach hilft nur ein Neustart der App. Die Verschiebung des Aufräumblocks, die Ü2 hätte heilen sollen, erzeugt einen schlimmeren Fehler als den, den sie behebt.

**Die Alles-oder-nichts-Schranke greift am falschen Zähler.** 1B streicht die 1A-Abfrage `CountRows(colPlanOk) = 0` und prüft nur noch `CountRows(colPlanOk) < CountRows(colPlan)`. Verschwindet eine ausgewählte Buchung serverseitig, schrumpfen Zähler und Nenner gemeinsam — die Prüfung merkt nichts. Sind alle weg, ist `0 < 0` falsch, `Patch` bekommt eine leere Tabelle, und der Nutzer liest „0 Buchungen geändert." in Grün.

**Die Verweigerungsmeldung führt in eine Sackgasse.** Sie nennt nur Zahlen, keine Buchung. Welche drei von vierzehn kollidieren, steht nirgends, und der Nutzer kann es auch nicht nachsehen: `galAlleTischbuchungen` filtert auf `Person.Email = User().Email`, die fremde Buchung erscheint also nie. Bei zwanzig Haken und einem Störenfried bleibt blindes Abhaken — und nach Befund 1 liegt dabei schon der Ladeschleier über der Galerie.

**Die Fehlermeldung behauptet eine Aktualisierung, die nicht stattfand.** „Die Liste wurde aktualisiert, bitte prüfen" — das `Refresh` steckt im verschobenen Aufräumblock und läuft in diesem Zweig gerade nicht.

---

### Entwurf 2A — Baustelle 2 — „Sammel-`Collect`, Teilerfolg wie heute" — Runde 2

**Idee in einem Satz:** Ein Kollisions-Lesevorgang mit Zeitgrenze, lokale Prüfung aller Serientermine, ein `Collect` für die Überlebenden.

**Gescheitert an: Kriterium 2 (Ehrlichkeit) und Kriterium 3 (Zugriffe).** Dazu zwei Blocker.

**Nach einem Teilausfall beschuldigt die App den Nutzer seiner eigenen Buchungen.** Bricht die Verbindung nach dem sechsten von vierzehn Datensätzen ab, stehen sechs Zeilen in SharePoint, `IfError` meldet aber „Speichern fehlgeschlagen." Der Nutzer versucht es erneut, der frische Lesevorgang findet jetzt seine eigenen sechs Zeilen, und er liest „8 von 14 Terminen gespeichert. **Die übrigen waren belegt.**" Die App schreibt ihm seine eigenen erfolgreichen Buchungen als fremde Kollision an.

**Die neue Zeitgrenze öffnet einen Doppelbuchungsweg, den der heutige unbegrenzte Filter schließt.** Die Untergrenze `Startzeit >= dpDatum.SelectedDate` übersieht eine bestehende Buchung, die am Vortag beginnt und in den Serienzeitraum hineinreicht. Solche Buchungen sind erreichbar, weil die Verlängern-Knöpfe weder bei 22:00 kappen noch wiederholtes Klicken verhindern — aus 19:00–22:00 werden in vier Klicks 19:00 bis 10:00 des Folgetags. Der zweite Nutzer bekommt dann grün „1 von 1 Terminen gespeichert" auf einen belegten Tisch.

**Die Zweiwochenkappung verschwindet in zwei von drei Ausgängen.** Sie steht nur im Erfolgszweig. Wer „bis in drei Monaten" eingestellt hatte und „Alle 11 Termine sind bereits belegt" liest, glaubt, drei Monate seien geprüft worden. Genau dann wäre der Hinweis wichtig.

**Blocker 1:** `Set(varSerienID; "")` in `App.OnStart` legt die Variable als Text an, `Set(varSerienID; GUID())` im Knopf weist ihr einen GUID zu — Power Apps verlangt über alle `Set` hinweg denselben Typ. Die Formel lässt sich nicht einfügen. Richtig wäre `Text(GUID())`, weil `SerienID` laut Schema eine Textspalte ist.

**Blocker 2: Die beiden Speichern-Knöpfe sind nicht wortgleich.** Meine Ersetzungstabelle nennt fünf Steuerelementnamen. Die Aufräumblöcke unterscheiden sich aber: der Grundriss-Dialog hat 12 Anweisungen, das Panel 23. Es fehlen `varZeigeDialog` → `varZeigeTischBuchungForm`, `Set(varAktiverTab; "dashboard")`, `Reset(chkWiederholenPanel)`, `Reset(tglTagMo_1)` bis `Reset(tglTagFr_1)`, `Set(varAusgewaehltePanelDauer; Blank())`, `Set(varStartOverridePanel; "")`, `Set(varEndeOverridePanel; "")` — elf Anweisungen. Wer 2A buchstäblich mit nur den fünf Ersetzungen einsetzt, lässt das Buchungsformular offen stehen und die Wochentags-Schalter sichtbar auf „an", während die Variablen dahinter auf `false` stehen. Der nächste Klick bringt „Bitte mindestens einen Wochentag auswählen", obwohl fünf Schalter grün leuchten.

**Ein geerbter Fehler, den 2A nicht behebt, obwohl es die Stelle neu schreibt:** `dpWiederholenBis` hat **kein `DefaultDate`** und steht damit auf heute. Wählt der Nutzer in `dpDatum` einen künftigen Tag und hakt „Wiederholen" an, ohne den Bis-Picker anzufassen, liegt `varBisRoh` **vor** dem Startdatum, `DateDiff + 1` wird negativ, und `Sequence(negativ; 0)` ist in Power Fx ein Fehler. Der Nutzer bekommt „Bitte mindestens einen Wochentag auswählen" — während die Wochentags-Schalter im Modus „Taeglich" gar nicht sichtbar sind. Er bekommt eine Anweisung, die er nicht befolgen kann, und erfährt nie, dass sein Bis-Datum das Problem ist.

Nicht beanstandet: Die Datumsliste ist korrekt, die Syntax ist sauber, die `As`-Aliasse beseitigen tatsächlich die heutige Mehrdeutigkeit, kein erfundener Name, und das Zeitzonenverhalten über die Zeitumstellung ist richtig.

---

### Entwurf 2B — Baustelle 2 — „`SerienID`, Nachprüfung und Rücknahme" — Runde 2

**Idee in einem Satz:** Jede Serie bekommt eine gemeinsame Kennung, nach dem Schreiben wird nachgelesen, und eigene Datensätze, die sich mit fremden überschneiden, werden nach der Regel „niedrigste ID gewinnt" wieder entfernt.

**Gescheitert an: Kriterium 2 (Ehrlichkeit), auf vier unabhängigen Wegen.**

Das war der ehrgeizigste Entwurf — der einzige, der das Doppelbuchungsfenster wirklich schließen wollte. Er scheitert daran, dass **das Sicherheitsnetz genau in den Lagen ausfällt, für die es gebaut wurde.**

**Der Nachprüfblock liegt im `DefaultResult` des `IfError`** und wird damit selbst nicht fehlerüberwacht. Bricht die Verbindung beim Nachlesen ab, bleibt `colKontrolle` leer oder liefert den gecachten Vorzustand, `colVerlierer` ist leer, und der Nutzer liest „14 von 14 Terminen gespeichert" — für einen Abgleich, der nie stattgefunden hat.

**Bei 429 läuft die Nachprüfung überhaupt nicht.** Schlägt eine Einzelanlage fehl, nimmt `IfError` den Fallback-Zweig, und der gesamte 2B-Block im `DefaultResult` wird übersprungen. Die bereits geschriebenen Zeilen bleiben unabgeglichen stehen, eine echte Doppelbuchung bleibt dauerhaft bestehen. Ausgerechnet im beobachteten Drosselungsfall ist das Netz abgeschaltet.

**Oberhalb des Datenzeilenlimits fällt es deterministisch aus.** Das Nachlesen filtert über `Tisch.Value` und ist damit nicht delegierbar; Power Apps holt nach ID aufsteigend bis zum Limit. Die gerade geschriebenen Zeilen tragen die **höchsten** IDs — sie fallen als erste heraus. Je voller die Liste, desto sicherer versagt die Prüfung, und zwar unsichtbar.

**Und die Regel „niedrigste ID gewinnt" kann gültige Buchungen löschen.** Die ID ist ein Stellvertreter für die Reihenfolge der *Erstellung*, nicht für den Anspruch auf das Zeitfenster. Nutzer A bucht einen freien Tisch 13:00–15:00 (neue Zeile, hohe ID); Nutzer C verlängert danach seine bestehende Buchung 11:00–13:00 (alte Zeile, niedrige ID) auf 15:00 — was er wegen B0 ungeprüft kann. A's Nachprüfung erklärt die **eigene korrekte Buchung** zur Verliererin und löscht sie, mit der Meldung „zeitgleich von jemand anderem gebucht". **Der Ist-Zustand lässt eine Doppelbuchung bestehen; 2B vernichtet eine gültige Buchung.** Das ist die schwerere Schadensart.

Dazu: derselbe GUID-Typkonflikt wie 2A, und bei zwei überlappenden Serien verschränken sich die IDs so, dass beide Nutzer zufällig verteilte Bruchstücke behalten — eine zerrissene Serie ist für den Nutzer schlechter als eine abgelehnte, und der Dialog schließt, ohne die Lücken zu nennen.

**Was das über den Suchraum sagt:** Eine Nachprüfung ist nur so verlässlich wie ihr schwächstes Glied, und hier liegen gleich drei davon außerhalb des Entwurfs — Netzverbindung, Drosselung, Delegationsgrenze. **Ein Sicherheitsnetz, das still ausfällt, ist schlechter als keines**, weil es eine Erfolgsmeldung rechtfertigt, die sonst niemand gegeben hätte. Optimistisches Schreiben mit nachträglicher Rücknahme braucht eine Garantie, dass die Rücknahme stattfindet — und die kann eine Canvas-App gegen SharePoint nicht geben.

---

### Entwurf 2C — Baustelle 2 — „Alles oder nichts" — Runde 2

**Idee in einem Satz:** Kollidiert auch nur ein Serientermin, wird nichts gespeichert und dem Nutzer gesagt, wie viele belegt sind.

**Gescheitert an: Kriterium 6 (Einfügeaufwand) und Kriterium 5 (Wartungsfläche).** Die beiden Ausschlusskriterien hat er als einziger Entwurf bestanden — und ist trotzdem der für den Nutzer schlechteste.

**Die Verweigerung nennt keinen einzigen Tag.** Mein eigener Entwurfsvorsatz lautete „die betroffenen Tage werden genannt"; die ausgearbeitete Formel nennt nur eine Zahl. Und der Nutzer kann es auch nicht nachsehen: Beide Galerien filtern auf `Person.Email = User().Email`, zeigen also nur eigene Buchungen. Fremdbelegung ist nur als Kachelfarbe im Grundriss sichtbar, und die ist **tagesgenau, nicht zeitfenstergenau** — sie färbt orange, sobald irgendwer an dem Tag irgendwann am Tisch sitzt. Der Nutzer müsste vierzehnmal das Datum durchklicken und bekäme dabei eine Antwort auf die falsche Frage.

**Es gibt keinen Weg, die Kollision zu umgehen.** Liegt sie an Tag 5 von 14, hilft weder „Zeitraum anpassen" (Verkürzen auf Tag 1–4 verliert Tag 6–14; eine Ausnahme pro Tag gibt es nicht) noch „Uhrzeit anpassen" (das verschiebt alle vierzehn). Heute bekäme er dreizehn Buchungen, mit 2C bekommt er null.

**Ein abgebrochener Schreibvorgang wird zur Dauersperre.** Bricht das Netz nach sechs von vierzehn Zeilen ab, liest der nächste Versuch die **eigenen** sechs Zeilen als Bestand und verweigert mit „6 von 14 Terminen sind belegt" — ohne zu sagen, dass es die eigenen sind. Die Serie lässt sich nie zu Ende buchen.

**Und die wörtliche Umsetzung friert die App ein.** „Der Aufräumblock wandert in den Erfolgszweig" — dieser Block endet mit `Set(varIsLoading; false)`. Im Verweigerungsfall bleibt `varIsLoading` auf `true`, und `conLadeOverlay` liegt bildschirmfüllend über allem. Der Nutzer liest seine Warnung über einem abgedunkelten, nicht mehr bedienbaren Bildschirm. Derselbe Fehler wie bei 1B, aus derselben unausbuchstabierten Anweisung.

**Was das über den Suchraum sagt:** „Alles oder nichts" ist nur dann eine Verbesserung, wenn der Nutzer mit dem „nichts" etwas anfangen kann. Ohne die Angabe, **welcher** Termin blockiert, ist die Verweigerung eine Sackgasse, und ohne die Möglichkeit, einen einzelnen Tag auszunehmen, ist sie ein reiner Verlust gegenüber dem Teilerfolg. **Eine strengere Zusage verpflichtet zu einer genaueren Auskunft** — wer weniger liefert, muss mehr erklären. Zusätzlich gilt: Der Name verspricht eine Atomizität, die der Schreibvorgang gar nicht hat; zwei gleichzeitige Nutzer bestehen beide ihre Vorprüfung und schreiben beide.

---

## Alle vier Entwürfe der Baustelle 1 sind gefallen

1A, 1B und 1C sind an Kriterium 2 durchgefallen, 1D strukturell. Nach den Regeln aus `AUFGABE_SPEICHERN.md` heißt das: **die ganze Denkrichtung wird weggeworfen, nicht nachgebessert**, und Baustelle 1 beginnt mit vier grundsätzlich anderen Familien neu.

**Was allen vier gemeinsam war und sie zu Fall gebracht hat:** Ein Dialog, der auf einer **unsichtbaren Menge** arbeitet und das Ergebnis als **Zahl** meldet. Der Nutzer sieht eine Buchung benannt, geändert werden andere; er wählt eine Dauer, ohne zu sehen, was sie bei jeder einzelnen Buchung bewirkt; und am Ende bekommt er „N Buchungen geändert", wobei N aus einer Collection stammt, nicht aus dem, was SharePoint tatsächlich angenommen hat. Jede einzelne Falschmeldung der drei Prüfberichte lässt sich auf diese zwei Eigenschaften zurückführen.

**Die Schlussfolgerung für die zweite Generation:** Nicht die Zählung verbessern, sondern sie abschaffen. Die zweite Generation muss die betroffene Menge **zeigen** statt sie zu zählen, und das Ergebnis **pro Zeile** feststellen statt es aus einer lokalen Collection abzuleiten.

---

## Übergreifende Befunde aus Runde 2

Diese drei Mängel stammen aus dem 1C-Angriff, betreffen aber die gemeinsame Basis und damit auch 1A und 1B. Sie werden **nicht** als Reparatur an 1C verbucht — 1C ist und bleibt verworfen —, sondern fließen in die Bewertung der übrigen Entwürfe ein, sobald deren eigene Prüfberichte vorliegen.

**Ü1 — Ein Teilerfolg wird als Totalausfall gemeldet.** Schreibt `Patch` mit einer Tabelle neun von vierzehn Zeilen und bricht dann ab, meldet `IfError` „Speichern fehlgeschlagen", obwohl neun Zeilen geändert wurden. Die Zahl der tatsächlich geschriebenen Zeilen wird nie ermittelt.

**Ü2 — Der Aufräumblock läuft unbedingt, auch im Fehlerfall.** `Clear(colAusgewaehlteBuchungen)`, `Set(varZeigeVerwaltenKlein; false)` und `Reset(tglAuswahlModus)` stehen hinter dem `If` und laufen damit auch nach einem Fehlschlag. Der Dialog schließt, die Auswahl von vierzehn Buchungen ist weg, und der Nutzer müsste sie von Hand rekonstruieren. 1B verschiebt diesen Block bereits in den Erfolgszweig, 1A nicht.

**Ü3 — Ein serverseitig gelöschter Datensatz bekommt eine falsche Begründung.** Die Teilerfolgsmeldung vergleicht gegen `CountRows(colAusgewaehlteBuchungen)` und sagt „Bei den übrigen war die Zeit belegt oder die Buchung zu kurz." Eine inzwischen von jemand anderem stornierte Buchung fehlt aber schon in `colPruefBestand` — sie war weder belegt noch zu kurz, sie existiert nicht mehr. Der Nutzer wird auf eine Zeitanpassung verwiesen, die ihm nicht helfen kann.

**Ü5 — Der Sammelaufruf spart gegen SharePoint keine Aufrufe. Das ist der wichtigste Befund dieses Laufs.**

Drei Prüfer, die einander nicht kannten, haben unabhängig voneinander dasselbe festgestellt: `Collect(Quelle; Tabelle)`, `Patch(Quelle; Tabelle)` und `Remove(Quelle; Tabelle)` sind gegenüber dem SharePoint-Konnektor **keine Sammelvorgänge**. Der Konnektor kennt keine Stapelschnittstelle für diese Operationen; eine Tabellen-Operation zerfällt in einen Aufruf je Zeile. Was sich ändert, ist die Verpackung — die Aufrufe gehen als Bündel hinaus statt nacheinander —, nicht ihre Zahl.

Damit sind sämtliche Zugriffszahlen falsch, die ich in `ENTWUERFE_ROHFASSUNG.md` als „konstant" ausgewiesen habe. Richtig gezählt, nach derselben Zählweise wie beim Nullpunkt:

| | 1 | 5 | 14 | 50 |
|---|---|---|---|---|
| Nullpunkt Serienbuchung | 3 | 7 | 16 | — |
| Entwurf 2A, behauptet | 3 | 3 | 3 | — |
| Entwurf 2A, tatsächlich | 3 | 7 | 16 | — |
| Entwurf 1A/1B, behauptet | 4 | 4 | 4 | 4 |
| Entwurf 1A/1B, tatsächlich | 4 | 8 | 17 | 53 |

**Schlimmer noch:** Ein Bündel aus vierzehn gleichzeitigen Schreibanforderungen ist für eine Drosselung mit 429 **anfälliger** als vierzehn nacheinander abgesetzte. Das beobachtete Muster — bei zehn Wiederholungen waren Durchlauf 6 und 7 deutlich langsamer — würde durch den Umbau eher verschärft als entschärft.

**Das trifft nicht nur diesen Lauf.** Die Empfehlung aus dem Stornieren-Lauf (`ENTWURF_MEHRFACHAUSWAHL.md`, Entwurf A) beruht auf derselben Annahme. Dort steht sie als `UNSICHER` markiert — diese Unsicherheit ist jetzt in Richtung „die Annahme trägt nicht" aufgelöst, allerdings weiterhin durch Schlussfolgerung und nicht durch Messung. **Vor jedem weiteren Umbau, der mit Geschwindigkeit begründet wird, muss einmal gemessen werden.**

Was vom Sammelaufruf bleibt: Er ist kürzer, besser lesbar und beseitigt die `app-ForAllWithMutation`-Warnung. Das sind Wartungsgründe, keine Geschwindigkeitsgründe.

**Ü6 — `Collect` aus Satzliteralen verliert die Spaltentypen, die `Defaults()` mitbringt.**

Der heutige Schreibweg ist `Patch(Tischbuchungen; Defaults(Tischbuchungen); {…})`. `Defaults()` liefert die vollständige, typisierte Zielsatzstruktur mit — deshalb funktioniert das Personenfeld dort auch ohne `'@odata.type'`. Baut man die Datensätze stattdessen als lokale Collection aus Satzliteralen auf und übergibt sie an `Collect`, fehlt diese Typinformation. `Tisch` ist dann nur noch ein Satz aus Zahl und Text, `Person` nur noch ein Satz aus Claims und Namen.

**Beleg aus dem eigenen Projekt:** Die Raumbuchung (Zeile 2306) schreibt `'@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser"` ausdrücklich mit — dort war es offenbar nötig.

Fällt `Person` deshalb leer aus, steht „14 von 14 Terminen gespeichert" über vierzehn Buchungen, die der Nutzer anschließend **in keiner Ansicht wiederfindet** — „Meine Buchungen" filtert auf `Person.Email = User().Email`, und die Tischkacheln ziehen die Initialen aus `Person.DisplayName`. Jeder `Collect`-Entwurf braucht `'@odata.type'` für `Person` (`…SPListExpandedUser`) und für `Tisch` (`…SPListExpandedReference`).

**Ü4 — Doppelklick erzeugt zwei widersprüchliche Meldungen.** Der erste Lauf leert `colAusgewaehlteBuchungen`, der zweite schiebt unmittelbar nach „5 Buchungen geändert." die Warnung „Keine Buchungen ausgewählt." nach. Eine `DisplayMode`-Sperre für den Speichern-Knopf ist nicht vorgesehen. Das deckende `conLadeOverlay` verhindert nur teilweise, weil `varIsLoading` erst nach dem ersten `Set` greift.

**Ü7 — Zustand aus `With()`-Locals in globale Variablen zu verlagern macht die Knöpfe mehrfachaufruf-unsicher.** Heute liegt der gesamte Zwischenzustand der Speichern-Knöpfe in `With()`-Geltungsbereichen und kann zwischen zwei Durchläufen nicht kollidieren. Meine Umstellung auf `Set`-Variablen und globale Collections — gedacht als Ausweg um die `With()`-Gleichzeitigkeit — gibt diese Eigenschaft auf: Ein zweiter, parallel gestarteter Lauf überschreibt `varSerienID` und `colNeueBuchungen`, während der erste noch schreibt. Der Ausweg um ein Sprachproblem hat ein Nebenläufigkeitsproblem erzeugt.

**Ü8 — Zwei identisch aussehende Knöpfe sind es nicht.** `btnSpeichern` und `btnSpeichernTischePanel` sind im Rechenteil wortgleich, im Aufräumteil nicht: 12 gegen 23 Anweisungen. Jede Ersetzungstabelle, die nur die Steuerelementnamen auflistet, ist unvollständig. Meine hatte fünf Zeilen, nötig wären sechzehn gewesen.

---

## Abbruch nach Regel 2

`AUFGABE_SPEICHERN.md` nennt drei Abbruchbedingungen. Eingetreten ist die zweite: **acht Familien sind durch und keine übersteht die Angriffe.**

| | Baustelle 1 | Baustelle 2 |
|---|---|---|
| Runde 1 | 1A, 1B, 1C, 1D | 2A, 2B, 2C, 2D |
| Strukturell vor Runde 2 raus | 1D | 2D |
| Im Angriff gefallen | 1A, 1B, 1C | 2A, 2B, 2C |
| Überlebt | **keiner** | **keiner** |

Die Regel sagt dazu: „dann schreib genau das auf, das ist ein echtes Ergebnis."

**Ich habe keine neunte Familie begonnen, und das ist eine bewusste Entscheidung.** Nach Ü5 beruhten alle acht auf einer Annahme, die nicht trägt — der Sammelaufruf spart gegen SharePoint keine Aufrufe. Eine neunte Familie derselben Denkrichtung wäre gegen dieselbe Wand gelaufen. Und eine Denkrichtung, die trägt, gibt es: Zeige die betroffene Menge, statt sie zu zählen, und stelle das Ergebnis pro Zeile fest. Das ist aber keine Formel mehr, sondern eine Vorschau-Galerie mit Zeilenstatus — ein Umbau von einem halben Tag, der zehn Tage vor dem Produktivgang nicht hineingehört.

**Was stattdessen geliefert wird**, steht in `ENTWURF_SPEICHERN.md`: fünf kleine, voneinander unabhängige Korrekturen, die je einen im Quellcode belegten Fehler schließen und nicht an der widerlegten Geschwindigkeitsannahme hängen. Das ist weniger, als die Aufgabe verlangt hat, und mehr, als ein überlebender Entwurf gebracht hätte.
