# Grundriss-Sperre nach 2 Minuten (08.10.2026, Fassung nach Prüfung)

Für den Desktop-Chat. Grundlage: Paket F Fassung 2.1 (F1–F8) im Studio. Erzeugt und geprüft mit `werkzeuge/grundriss_sperre.py`, unabhängig geprüft (`pruefung_grundriss_sperre.md`, 3 mittlere und 7 niedrige Befunde, alle eingearbeitet). Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Was passiert:** 2 Minuten nach dem letzten Laden des Grundrisses legt sich eine halb durchsichtige weiße Fläche über `conGrundriss`. Mittig erscheint der Knopf **„Grundriss aktualisieren“**.
  - Kacheln und `ddStockwerk` sind dann nicht bedienbar. Alles außerhalb von `conGrundriss` bleibt bedienbar.
  - Der Knopf macht dasselbe wie das Aktualisieren-Symbol `Icon1_1` (F3-Fassung): `Refresh`, Freigabe-Grenze, Ladezeile. Danach verschwinden Fläche und Knopf, und die 2 Minuten laufen neu.
- **Einstellung:** `Set(varGrundrissSperreSekunden; 120)` in `App.OnStart`.
- **Zeitstempel:** Jede Stelle, die `colGrundriss` lädt, setzt `varGrundrissStand`, direkt hinter dem `ClearCollect`, also nur bei Erfolg. Das sind **15 Stellen und der neue Knopf**, die vollständige Liste steht unten. Schlägt das Laden fehl, bleibt der alte Stempel, und der Knopf bleibt für den nächsten Versuch.
- **Zeit ohne Abfrage:** `tmrAktualisieren` setzt alle 15 Sekunden nur `varJetztTakt`. Die Sichtbarkeit vergleicht zwei Variablen. Die Sperre erscheint nach **2:00 bis 2:15 Minuten**.
- **Umfang:** 5 Schritte (S1, S2, S3, S3b, S4) mit **53 Properties**, davon 34 an den 2 neuen Steuerelementen.
  - Die 14 Ladestellen in S2 ändern sich nur um `;; Set(varGrundrissStand; Now())`. Maschinell geprüft: sonst nichts.
  - Maschinell 0 Fehler. In Studio ist nichts getestet.
- **Eine Entscheidung für Josias (Abschnitt „Entscheidung“):** Der Timer lädt nicht mehr automatisch. Das folgt aus deiner Vorgabe „keine Abfrage, solange niemand tippt“, ändert aber das Verhalten aus F8.

## Alle Stellen, die `colGrundriss` laden
Belegt durch Suche nach der Ladezeile im Gesamtstand: Export + eingefügte G-Schritte + Nachtrag 4 + F2.1. Der Generator bricht ab, wenn es nicht genau 16 sind.

| Stelle | Schritt |
|---|---|
| `App.OnStart` | S1 (Stempel und 2 Variablen) |
| `ddStockwerk.OnChange`, `dpAnsichtsDatum.OnChange` | S2 |
| `Icon1.OnSelect`, `Icon1_1.OnSelect`, `Image6.OnSelect`, `btnHitArea_1.OnSelect` (Aktualisieren-Symbole) | S2 |
| `btnSpeichern.OnSelect`, `btnSpeichernTischePanel.OnSelect` | S2 |
| `btnVerlängern.OnSelect`, `btnVerlängern_1.OnSelect` | S2 |
| `btnStornieren.OnSelect`, `btnStornieren_1.OnSelect`, `btnStornierenKlein.OnSelect` | S2 |
| `btnEinchecken.OnSelect` | S2 |
| `tmrAktualisieren.OnTimerEnd` | S3: **lädt nicht mehr** |
| `btnGrundrissAktualisieren.OnSelect` (neu) | S4 |

**Notweg aus F2.1 Anhang D:** Er lädt ohne Stempel. Er ist nicht mehr nötig, weil F2 eingefügt ist. Wer ihn trotzdem einsetzt, bei dem bleibt die Sperre nach dem Stornieren stehen, bis jemand auf den Knopf tippt. Das ist harmlos.

## Wie `tmrAktualisieren` (F8) dazu passt: anpassen, nicht entfernen
- **Bisher (F8, belegt aus der Formel):** alle 5 Minuten `Refresh` (2 Galerien) und Ladezeile, also **3 Abfragen je 5 Minuten je offener App**, auch wenn niemand am Platz ist. Bei 30 offenen Apps sind das etwa 18 Abfragen pro Minute (F2.1, Abfragetabelle).
- **Mit der Sperre** würde das automatische Laden den Grundriss alle 5 Minuten wieder freigeben. Der Knopf wäre also abwechselnd da und weg, und die Abfragen liefen trotzdem.
- **Umgesetzt in S3:** Der Timer **lädt nicht mehr**. Er läuft alle 15 Sekunden und macht nur Folgendes:
  1. `varJetztTakt` setzen, immer und auch bei offenem Dialog. Das ist keine Abfrage.
  2. Den Tageswechsel wie in F8: Datum auf heute. Neu ist, dass er den Stempel leert, damit der Knopf sofort erscheint.
  3. Die Check-in-Erinnerung aus F8 mit zwei Zusätzen:
     - Sie fragt **nur**, wenn der Grundriss lokal eine eigene, nicht eingecheckte und noch nicht verfallene Buchung zeigt, die in höchstens 30 Minuten beginnt.
     - Sie fragt dann **höchstens alle 5 Minuten** (`varErinnerungAb`). In F8 war das bei jedem Tick der Fall, also ebenfalls alle 5 Minuten.
     - Das ist die **einzige** Abfrage ohne Tippen. Wer sie auch nicht will, nimmt die **Variante „streng“** (Anhang B). Dann fragt die App nur beim Start nach dem Check-in.
- **Ergebnis:** Ohne Tippen gibt es **0 Abfragen**, außer der gedrosselten Erinnerung. Zwei kleine Ausnahmen kommen dazu (geschlussfolgert):
  - Um Mitternacht fragt `galTischbuchungenHeute` einmal neu, weil der Timer `varAnsichtsDatum` umstellt.
  - Die Statusanzeige (S3b) rechnet alle 15 Sekunden lokal neu.
- **Entfernen wäre schlechter:** Der Takt für die Sperre braucht ohnehin einen Timer. Ohne ihn wäre ein anderes Steuerelement nötig.

## Entscheidung für Josias: kein automatisches Aktualisieren mehr
Das folgt aus der Vorgabe „keine SharePoint-Abfrage, solange niemand tippt“. Es ändert F8 so:
- **Grundriss:** Er ist nie älter als 2:15 Minuten, wenn man ihn bedient. Das ist besser als die bisherigen bis zu 5 Minuten, weil die Sperre vorher zum Aktualisieren zwingt.
- **Dashboard-Listen (eigene Buchungen):** Sie werden nicht mehr alle 5 Minuten aufgefrischt, sondern nur noch durch ein Aktualisieren-Symbol, den Sperr-Knopf oder eine eigene Aktion.
  - Eine Buchung, die am Handy gemacht wurde, erscheint am PC erst danach.
  - Eine beendete Buchung bleibt bis dahin in der Liste stehen.
- **Statusanzeige „Verfallen“:** Sie wird trotzdem rechtzeitig grau, ohne Abfrage. Dafür ist S3b da.
- **F2.1 ändert sich an zwei Stellen:**
  - Der Testbogen-Punkt „F8 Timer aktualisiert, Erinnerung einmal“ wird durch Test 8 unten ersetzt.
  - F2.1-Unsicherheit U11 (der Timer überschreibt beim Speichern) entfällt, weil der Timer nicht mehr lädt.
- **Text für Kurzanleitung und Betriebshandbuch:** „Andere sehen den freien Tisch, sobald ihr Grundriss neu geladen ist, **spätestens beim nächsten Bedienen** (der Grundriss sperrt sich nach 2 Minuten bis zum Aktualisieren).“ Bisher hieß es „meist innerhalb von 5 Minuten“.
- **Wenn Josias das automatische Aktualisieren behalten will:** S3 nicht einfügen. Dann verschwindet die Sperre alle 5 Minuten von selbst, und die Abfragen bleiben bei 3 je 5 Minuten. S1, S2 und S4 funktionieren auch ohne S3, aber `varJetztTakt` wird dann nur beim Start gesetzt, und die Sperre erscheint **nie**. **Also: S3 ist für die Sperre nötig.**

## Was bei offenen Dialogen und beim Speichern passiert
Ebenen (**belegt** im Export):
- `conGrundriss` ist das **unterste** Kind von `Screen1`.
- Buchungsdialog (`conBuchungDialog`), Panel (`conTischBuchungenPanel`), Verwalten-Dialoge, Check-in-Frage (`conCheckinDialog`), Details-Popup (`conDetailsPopup`) und Lade-Overlay liegen **darüber** auf `Screen1`.
- Fläche und Knopf liegen **in** `conGrundriss`.

Daraus folgt (**geschlussfolgert**):
- **Dialog, Panel, Verwalten, Check-in-Frage oder Details offen:**
  - Alles bleibt voll bedienbar. Die Fläche erscheint höchstens dahinter.
  - Nichts verspringt: Der Container ist frei angeordnet, und die neuen Steuerelemente liegen fest auf X/Y 0 oder mittig. Sie verschieben nichts.
  - Speichern lädt den Grundriss, damit verschwindet die Sperre.
  - Abbrechen lässt sie stehen, dann tippt man auf den Knopf.
- **Während des Speicherns (`varIsLoading`):** Das Lade-Overlay liegt oben. Der Knopf ist grau (`DisplayMode`). Mit dem Laden am Ende verschwindet die Sperre.
- **Aufgeklappte Stockwerk-Auswahl:** `ddStockwerk` liegt in `conGrundriss` (belegt). Wahrscheinlich bleibt die offene Liste über der Fläche bedienbar oder klappt beim Tippen zu (geschlussfolgert, nicht getestet). Wählt man dort ein Stockwerk, lädt `OnChange` den Grundriss und die Sperre verschwindet. Es entsteht also kein falscher Zustand.
- **Außerhalb von `conGrundriss`** (Dashboard, Kopfzeile, Tabs) wird nichts gesperrt.
- **Beim Start:** `usenonblockingonstartrule` ist an (belegt). Der Screen ist also sichtbar, bevor OnStart fertig ist. Damit die Sperre dabei nicht aufblitzt, setzt OnStart `varJetztTakt` erst **ganz am Ende**, nach der Ladezeile. Die Sichtbarkeit verlangt `!IsBlank(varJetztTakt)`.

## Warum Fläche + Knopf (schlankste Lösung)
- **`DisplayMode` am Container:** Ob Kinder in klassischen Containern den `DisplayMode` erben, ist **UNSICHER**. Außerdem müsste jede Kachel umgebaut werden.
- **Ein Rechteck:** Ob es Klicks zuverlässig abfängt, ist **UNSICHER**.
- **Eine klassische Schaltfläche** fängt Klicks ab, auch wenn sie durchsichtig ist. Das stützt die App selbst: `btnHitArea` ist eine transparente Schaltfläche über den Kacheln (belegt).
  - `OnSelect` ist `false`, die Fläche macht beim Tippen also nichts.
  - `TabIndex = -1`, damit sie per Tastatur nicht angesprungen wird.
  - `AccessibleLabel` erklärt sie dem Bildschirmleser.
- Also zwei neue Steuerelemente, Fläche und Knopf, ohne Umbau bestehender Steuerelemente.
- **Grenze (geschlussfolgert):** Die Fläche sperrt Maus und Touch. Per Tab-Taste bleiben `ddStockwerk` und die Kacheln darunter erreichbar. Das ist unkritisch: `btnHitArea` liest beim Öffnen frisch, und `ddStockwerk.OnChange` lädt neu und stempelt.

## Statusanzeige ohne Abfrage (S3b)
- `lblStatusHeute` in `galTischbuchungenHeute` zeigt „Verfallen“ bisher nach `varFreigabeGrenze`. Diese Variable setzte F8 alle 5 Minuten neu, S3 tut das nur noch in der Erinnerung.
- S3b rechnet stattdessen mit `varJetztTakt` (alle 15 s). Das ist keine Abfrage.
- `varFreigabeGrenze` bleibt bewusst unverändert. Würde der Timer sie alle 15 s setzen, rechnete `ddTischePanel.Items` (`ForAll` über `Tische` mit Abfragen) jedes Mal neu.

## UNSICHER (mit Test)
| Nr | Was | Test |
|---|---|---|
| S-U1 | Die halb durchsichtige Schaltfläche fängt alle Klicks ab, auch über der Kachel-Galerie. Gestützt durch die transparente `btnHitArea` (belegt), selbst nicht getestet | Test 3 |
| S-U2 | `Reset(dpAnsichtsDatum)` im Timer löst kein `OnChange` aus. Deshalb leert der Timer den Stempel, damit der Knopf erscheint | nur um Mitternacht prüfbar, der Knopf lädt dann den neuen Tag |
| S-U3 | Im Browser-Hintergrund drosseln Browser Timer (geschlussfolgert). Die Sperre erscheint dann erst beim nächsten Tick nach der Rückkehr, spätestens 15 s später | Test 9 |

## Hinweise für Studio
- In Studio deckt die Fläche den Grundriss ab, sobald sie sichtbar ist. Steuerelemente darunter dann **über die Strukturansicht** auswählen, nicht auf der Leinwand.
- Reihenfolge: S1 → S2 → S3 → S3b → S4. Danach App-Prüfung, **OnStart ausführen**, Vorschau.

## Testablauf
1. S1–S4 einfügen. App-Prüfung ohne rote Fehler, **OnStart ausführen**, Vorschau starten.
2. **Start:** Beim Laden blitzt keine Fläche auf.
3. 2:15 Minuten warten → Fläche und Knopf erscheinen, der Grundriss ist blass. Kachel und `ddStockwerk` antippen → **nichts** passiert. Dashboard-Knöpfe (außerhalb) funktionieren.
4. Knopf antippen → „Aktualisiert.“, die Fläche ist weg. Nach 2 Minuten ist sie wieder da.
5. Buchungsdialog über eine Kachel öffnen, 2:15 Minuten warten → der Dialog bleibt bedienbar, die Fläche liegt nur dahinter. Speichern → „Gebucht …“, die Fläche ist weg.
6. **Offline:** Sperre abwarten, Netzwerk trennen (Browser-Entwicklertools → Offline), Knopf tippen → Warnung „Grundriss konnte nicht aktualisiert werden …“, der **Knopf bleibt**. Wieder online, tippen → weg.
7. **Monitor:** App 6 Minuten unberührt lassen, ohne eigene anstehende Buchung → **keine** `getRows`.
8. **Erinnerung (ersetzt F2.1-Testpunkt „F8 Timer aktualisiert“):** Eigene Buchung zur nächsten halben Stunde anlegen (die Startliste hat nur halbe Stunden, Beginn also in höchstens 30 Minuten). Auf dem Dashboard bleiben, keinen Dialog offen → Check-in-Frage nach **höchstens 15 s**, nur einmal. Hat die App schon nach dem Speichern gefragt, gilt der Test als bestanden, wenn sie **nicht** ein zweites Mal fragt.
9. **Status ohne Tippen:** Eigene Buchung zur nächsten halben Stunde, nicht einchecken. Testknopf `Set(varFreigabeMinuten; 1)` tippen. Ab 1 Minute nach Beginn wird der Status in der Dashboard-Liste ohne Tippen **„Verfallen“ (grau)**, nach höchstens 15 s. Dazu den Browser-Tab kurz wechseln und zurückkommen → die Sperre erscheint nach spätestens 15 s, falls fällig.
10. Zum schnellen Testen in Studio einen Testknopf (außerhalb von `conGrundriss`) mit `Set(varGrundrissSperreSekunden; 20)` → dann reichen 35 Sekunden. **Testknopf vor dem Veröffentlichen löschen**, `varFreigabeMinuten` zurück auf 30 (OnStart erneut ausführen).

## Rückfall
- **S4 nur zusammen mit S3 zurücknehmen, und nie S3 allein:**
  - Ohne S3 (alter Timer) blinkt die Sperre alle 5 Minuten weg.
  - Ohne S4 laufen S1–S3 harmlos weiter, aber ohne Sperre und ohne automatisches Aktualisieren.
- **S4:** die zwei neuen Steuerelemente löschen.
- **S3, S3b:** `tmrAktualisieren.Duration`, `tmrAktualisieren.OnTimerEnd`, `lblStatusHeute.Text` und `lblStatusHeute.Color` auf die Fassungen aus **Anhang A** zurücksetzen. Sie entsprechen F2.1, Abschnitte F8 und F7.
- **S1, S2:** Die Fassungen stehen ebenfalls in Anhang A. Der zusätzliche Stempel stört allein nicht, Zurücksetzen ist also nicht nötig.
