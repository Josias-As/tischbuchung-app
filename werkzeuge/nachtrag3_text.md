# Nachtrag 3 (08.10.): Speichern ohne das erste `Refresh`

> Für den Chat, der Josias führt. Gilt für **G6** (Gesamtplan) und **F4** (Paket F). Im Vault ablegen.

## Kurzfassung
- **Wo das erste `Refresh` wirklich steht (belegt):** **nicht** vor dem Sammel-Patch. Es steht im Zweig **„nichts gebucht“**: Alle gewählten Termine sind belegt, oder du hast zu der Zeit schon einen Tisch. In diesem Zweig wird gar nicht gepatcht. Im Buchungsweg gibt es nur **ein** `Refresh`, das vor der Nachlese (H6), und das bleibt.
- **Entfernen ist sicher:**
  - `colNeuBelegt` und `colNeuIch` sind eigene, gefilterte Abfragen beim Klick, sie hängen nicht von diesem `Refresh` ab.
  - Die Nachlese liegt in einem anderen Zweig und behält ihr `Refresh`.
  - Den Grundriss lädt die Ladezeile am Ende ohnehin neu.
- **Wirkung auf die Abfragen (geschlussfolgert aus den Formeln, im Monitor nachprüfbar):**
  - `Refresh(Tischbuchungen)` fragt jede Anzeige neu ab, die direkt an der Liste hängt.
  - Im Endstand sind das `galTischbuchungenHeute` und `galAlleTischbuchungen`, also **2 Abfragen**.
  - Beim Speichern aus dem Panel „Tisch buchen“ (Panel offen) kommen bis zu **5** dazu: `ddTischePanel.Items` und die Knöpfe 5 Std / 9 Std (je `DisplayMode` und `Fill`, nur wenn ein Tisch gewählt ist).
  - **Ersparnis: 2 bis 7 Abfragen, aber nur im Zweig „nichts gebucht“.** Bei einer normalen, erfolgreichen Buchung ändert sich **nichts**.
- **Was du verlierst:** Ist „nichts gebucht“, aktualisieren sich die eigenen Listen und die Tischliste im Panel nicht sofort. Das holt der nächste Speichervorgang, das Aktualisieren-Symbol oder der 5-Minuten-Timer nach. Der Grundriss ist wegen der Ladezeile trotzdem aktuell.
- **Doppelbuchung?** Nein. Selbst wenn eine wiederholte, gleiche Abfrage einmal aus einem Zwischenspeicher käme (UNSICHER, H6), meldet die Nachlese nach dem Patch eine gleichzeitige Buchung.
- **Auf die Nachlese:** keine Wirkung.

## Wo die echte Last beim Speichern liegt (zum Abwägen, nicht geändert)
Eine **erfolgreiche** Buchung (Ergebnis geschlussfolgert, im Monitor prüfen) läuft so:
1. `colNeuBelegt`, `colNeuIch` und `LookUp(Tische…Gesperrt)`: je 1 Abfrage, zusammen 3.
2. Sammel-Patch: 1 Schreibvorgang je Termin.
3. `Refresh` vor der Nachlese: 2 Abfragen, im Panel bis 7, weil das Panel erst **nach** der Nachlese schließt.
4. Nachlese: 1 Abfrage.
5. Ladezeile: 1 Abfrage.

Das `Refresh` vor der Nachlese ist damit der größte Posten. Es bleibt, wie gewünscht (H6). Eine spätere Möglichkeit: die Nachlese mit einer **anders geformten** Abfrage machen (z. B. `Filter(Tischbuchungen; SerienID = varSerienID)`). Dann kann sie nicht aus dem Zwischenspeicher der Vorprüfung kommen, und das `Refresh` wäre unnötig. Das ist **ungetestet**, deshalb hier nur als Idee.

## So einfügen
- **G6 noch nicht eingefügt:** die beiden G6-Blöcke unten statt der Blöcke in `GESAMTPLAN.md` nehmen.
- **G6 schon eingefügt:** die beiden G6-Blöcke unten noch einmal einfügen (ganze Property ersetzen).
- **Paket F, Schritt F4:** die beiden F4-Blöcke unten statt der F4-Blöcke in `UEBERGABE_PaketF.md` nehmen. Sonst bringt F4 das `Refresh` zurück.

**Test:** einen Tisch zu einer Zeit buchen, zu der er schon belegt ist → Meldung „Der Tisch ist in dieser Zeit schon belegt …“, keine rote Fehlermeldung, Dialog bleibt offen. Danach normal buchen → „Gebucht: …“ wie bisher. Optional im Monitor: Bei „nichts gebucht“ erscheinen keine `getRows` für die beiden Galerien mehr.
**Rückfall:** die Blöcke aus `GESAMTPLAN.md` (G6) bzw. `UEBERGABE_PaketF.md` (F4) wieder einsetzen.
