# Konzept: Wie zwei Chats eine App sicher und günstig umbauen

Von Claude (Analyse-Chat Tischbuchung, 07.–20.10.2026) an den Chat, der für Josias eine neue App baut.

**Das ist ein Konzept, keine Anweisung.** Es beschreibt, was sich in zwei Wochen Tischbuchung (Power Apps Canvas, SharePoint, Desktop- und Handy-App) bewährt hat und was schiefging. Übernimm, was zu deiner App passt. Wo du einen besseren Weg siehst, nimm ihn und begründe ihn Josias gegenüber kurz.

## Kurzfassung
- **Zwei Rollen:**
  - Der **Bau-Chat** denkt gründlich, erzeugt jede Formel maschinell aus dem Export und lässt sie zweimal prüfen.
  - Der **Einsetz-Chat** führt Josias in Studio Schritt für Schritt durch die fertigen Blöcke, ohne neu nachzudenken.
  - Beide laufen auf **verschiedenen Accounts**. Das teure Denken passiert einmal, das Einsetzen kostet wenig.
- **Die Schnittstelle ist eine Übergabedatei**, kein Gespräch. Sie enthält vollständige Properties, Diff, Test und Rückfall je Schritt. Wer sie liest, muss nichts mehr entscheiden.
- **Quelle der Wahrheit ist immer der Export**, nie eine Rückmeldung wie „passt“. Nach jedem Einfügeblock kommt ein neuer Export, und der Bau-Chat gleicht ihn maschinell ab.
- **Der größte Hebel war nicht das Formelwissen, sondern der Prozess:** Generator statt Abtippen, unabhängige Prüfung, Export-Abgleich. Die teuersten Fehler waren Prozessfehler: zu groß geplant, gemeldeten Stand geglaubt, Texte vor dem Code geschrieben.

## 1. Wie Josias arbeitet
- **Rolle:** Werkstudent Digitalisierung bei Technoform, einziger Entwickler. Er fügt **jede Formel selbst** in Power Apps Studio ein. Claude ändert nie App, Listen oder Flows, sondern liest Exporte und liefert Text.
- **Freiheit unter zwei Bedingungen:** alles **dokumentieren** und **nichts kaputt machen**.
  - Handeln statt fragen: begründete Annahmen treffen und kennzeichnen.
  - Fragen nur, wenn die Entscheidung fachlich bei ihm liegt (Regeln, Betrieb, Datenübernahme, Rechte).
  - Das Interview-Format („interview mich step by step“, eine Frage nach der anderen, mit Empfehlung) hat er gut angenommen.
- **Er will Ehrlichkeit statt Beruhigung.** Er hat ausdrücklich „knallhart“ und „kritisch“ verlangt, weil frühere Chats zu nett waren. Gemeint ist: klare Urteile mit Begründung, eigene Fehler offen benennen, keine Prozentzahlen aus dem Bauch.
- **Leistung ist ihm sehr wichtig.** Zu jeder Änderung will er wissen, wie viele Abfragen sie kostet oder spart.
- **Stil, den er gelobt hat:**
  - Kurzfassung zuerst.
  - Deutsch mit Umlauten, kurze Sätze.
  - Je Schritt `Steuerelement.Property`, vollständiger Block, Test, Rückfall.
  - Originale im Anhang.
  - Jede Aussage gekennzeichnet: **belegt** (Export/Datei), **gemessen** (Monitor/Test), **geschlussfolgert**, **UNSICHER** (mit Prüftest).
- **Dateien:**
  - Er braucht **echte Download-Links**. Bewährt: im Repo committen und die GitHub-Raw-Links schicken.
  - Datei-Karten im Chat konnte er nicht herunterladen. Artifact-Links können andere Chats nicht lesen.
  - Er pflegt einen Obsidian-Vault. Ein Cloud-Chat erreicht ihn nicht, Josias lädt die Dateien dann hoch.
- **Er entscheidet manchmal, eine Prüfung wegzulassen** (Zeit, Guthaben). Dann sofort abbrechen und im Dokument sichtbar „nicht unabhängig geprüft“ schreiben.
- **Er spart Nutzungsguthaben.** Daher die zwei Accounts und ein Einsetz-Chat, der möglichst wenig selbst denkt.
- **Berechtigungen und Tenant** liegen bei der IT. Bei der Tischbuchung war das Michael, und der war genau in der Go-Live-Woche im Urlaub. Solche Abhängigkeiten früh klären.

## 2. Die zwei Rollen

| | Bau-Chat (vorsichtig, teuer) | Einsetz-Chat (schnell, günstig) |
|---|---|---|
| Account | eigener, z. B. Claude Code mit Repo und Werkzeugen | anderer Account, normaler Chat |
| Liest | Export, Monitor-Auswertung, Projektwissen, Rückmeldungen | nur die Übergabedatei und den Startprompt |
| Tut | analysieren, Umbau planen, Blöcke **maschinell** erzeugen, selbst prüfen, unabhängig prüfen lassen, Übergabe schreiben, neuen Export abgleichen | Josias Schritt für Schritt führen: wo klicken, Block **unverändert** geben, Test nennen, Ergebnis notieren |
| Tut nicht | in Studio klicken, Formeln „aus dem Kopf“ liefern | Formeln umschreiben, kürzen oder „verbessern“, neue Lösungen erfinden |
| Bei Fehlern | neue Fassung erzeugen (neue Datei, alte bleibt) | Fehler **wörtlich** festhalten, Rückfall aus dem Dokument nennen, mit dem nächsten unabhängigen Schritt weitermachen |

**Warum das spart:** Die Denkarbeit steckt in der Übergabe. Der Einsetz-Chat liest eine Datei und reicht Blöcke durch. Er braucht keinen großen Kontext und keine Analyse. Wenn er anfängt mitzudenken, wird es teurer und unsicherer, denn eine „verbesserte“ Formel ist ungeprüft.

**Der Weg zwischen beiden läuft über Josias:**
1. Bau-Chat → Übergabedatei (+ Startprompt beim ersten Mal) → Josias → Einsetz-Chat.
2. Einsetz-Chat → **strukturierte Rückmeldung** → Josias → Bau-Chat. Bewährtes Format:
   > F1 eingefügt: App-Prüfung meldet an `DropColumns` „Erwarteter Name des Bezeichners“. F1 ist zurückgenommen. Bitte neu erzeugen und prüfen, ob dieselbe Schreibweise noch an anderen Stellen steckt.
   Schritt-ID, Property, wörtlicher Fehlertext, was zurückgenommen wurde, was gebraucht wird.
3. Nach jedem Einfügeblock: Josias **speichert** in Studio, **exportiert den Studio-Stand** (nicht die veröffentlichte Fassung) und gibt den Export dem Bau-Chat. Der gleicht ihn Property für Property mit dem Soll ab.

**Ein Fehler, der genau an dieser Naht passiert ist:**
- Der Einsetz-Chat meldete „passt“ für Schritte, die im Export dann fehlten (drei Teile).
- Ein Export trug den Namen „Einchecken“, war aber zeichengleich mit dem Stand von vier Tagen davor.
- Ein „Handy“-Export enthielt die Desktop-App.

Deshalb prüft der Bau-Chat bei jedem Export App-ID, Name und den Unterschied zum letzten Stand, bevor er rechnet.

## 3. Aufbau einer Übergabedatei (Beispiel)
Jede Übergabe hatte dieselbe Gliederung:

1. **Kopf:** Wofür (App), Grundlage (Export-Datei mit Datum und Uhrzeit), mit welchem Skript erzeugt, Prüfstatus. Der Prüfstatus besteht aus drei getrennten Angaben: maschinell / unabhängig / in Studio getestet. Dazu die Kennzeichnung.
2. **Voraussetzung:** „Jeder Block ersetzt die ganze Property. Wurde nach dem Export etwas gespeichert, erst neu exportieren.“
3. **Kurzfassung:** was, warum, Umfang (Properties, neue Steuerelemente, Abfragen mehr oder weniger), Risiko, Zeitpunkt.
4. **Einfügen:** Reihenfolge der Schritte, neue Steuerelemente mit **exaktem Namen und Ort**, Hinweise zu Studio („Ganz nach vorne“, nicht „Nach vorne“).
5. **Je Schritt:** Ort (Pfad), „ganze Property ersetzen“ bzw. „neu setzen“, **Diff gegen den Ausgangsstand**, **vollständiger Block** in deutscher Schreibweise, Test, Rückfall.
6. **Testbogen als Zeitachse:** getrennte Testbuchungen, Testmodus mit ausdrücklichem Ende, jeder Test mit den Eingabemöglichkeiten der App ausführbar.
7. **Rückfall gesamt.**
8. **UNSICHER-Tabelle:** jede offene Annahme mit dem Test, der sie klärt.
9. **Unabhängige Prüfung:** Befunde und was daraus wurde, oder ausdrücklich „nicht unabhängig geprüft“.
10. **Anhang A:** Originale aller geänderten Properties aus dem Export. **Anhang B:** Ausgabe der maschinellen Prüfung.

**Echter Ausschnitt** (Nachtrag 6, R1, gekürzt):

````markdown
### R1 Karte öffnet bei verfallener oder beendeter Buchung keinen Check-in-Dialog

**Regel:** gesperrt, wenn `Endzeit` erreicht ist **oder** die Buchung verfallen ist (nicht eingecheckt,
Beginn und Buchungszeitpunkt älter als 30 Min).
- Es ist dieselbe Verfallsregel wie in `lblStatusHeute`, zeichengleich (maschinell geprüft).

**Test:**
1. Testknopf `Set(varFreigabeMinuten; 1)`.
2. Eigene Buchung zur nächsten halben Stunde, nicht einchecken.
3. Ab 1 Min nach Beginn ist die Karte nicht mehr anklickbar und nicht grau.
4. Eine eingecheckte, laufende Buchung öffnet weiter den Dialog.

#### `btnEincheckenHeute.DisplayMode`
Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute` · **neu setzen**

Vollständiger Block:
```
If(
  ThisItem.Endzeit <= Coalesce(varJetztTakt; Now()) || (!ThisItem.CheckedIn && ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));
  DisplayMode.Disabled;
  DisplayMode.Edit
)
```

#### `btnEincheckenHeute.DisabledBorderColor`
Ort: … · **ganze Property ersetzen**

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):
```diff
-RGBA(166; 166; 166; 1)
+Color.Transparent
```
````

Ganze Beispiele liegen im Repo: `arbeit/2026-10-12_Nachtrag6/NACHTRAG_6.md` (klein), `arbeit/2026-10-08_Nachtrag5/NACHTRAG_5.md` (mit Prüfung und Testbogen), `arbeit/2026-10-19_HeuteButton/HEUTE_BUTTON.md` (ein neuer Knopf).

## 4. Wie die Blöcke entstehen (Werkzeugkette)
Bewährt hat sich, **keine Formel von Hand zu schreiben, die in Studio landet**. Jede Übergabe kam aus zwei kleinen Python-Skripten:

1. **Export lesen:** ZIP → `.msapp` entpacken → alle Properties als `"Steuerelement.Property" → Formel` (englische Schreibweise), dazu Eltern, Typ, Pfad (`werkzeuge/app.py`).
2. **Ändern per Anker:** Die neue Fassung entsteht aus dem Original durch gezielte Ersetzung. Der Anker muss **genau einmal** vorkommen, sonst bricht das Skript ab. So kann sich keine Zeile „nebenbei“ ändern.
3. **Schreibweise übersetzen:** englisch → deutsch (`,`→`;`, `;`→`;;`, Dezimalpunkt → Komma), und **zurück**. Die Rückübersetzung muss zeichengleich sein.
4. **Prüfen, maschinell, im selben Skript:**
   - Klammern, Zeichenketten.
   - Jede gelesene Variable wird irgendwo gesetzt, jedes Steuerelement existiert.
   - Keine Kommentare in Verhaltensformeln.
   - Projekteinstellungen beachtet (z. B. Spaltennamen als Bezeichner).
   - Regeln an allen Schreibstellen gleich (Sperre, Freigabe-Regel, Ladezeile).
   - Textbreite neuer Beschriftungen und Kontrast neuer Farben.
5. **Mutationstest:** Absichtlich eingebaute Fehler müssen von den Prüfungen erkannt werden.
   - Erst dann weiß man, dass eine Prüfung überhaupt greift.
   - Mehrmals fiel dabei auf, dass eine Prüfung gegen eine Konstante statt gegen den erzeugten Text lief.
6. **Ausgabe:** `bloecke.json` (alt, neu, deutsch, Diff, Pfad) und `pruefung.txt`. Ein zweites Skript baut daraus das Dokument mit Texten aus einer Vorlage.
7. **Versionen:** neue Fassung = neuer Ordner oder neue Datei mit Datum, alte bleiben. Ein Projektwissen-Dokument (`CLAUDE.md`) hält Fakten, Entscheidungen, Stand und eine **Fehlerliste** fest. Sie hat drei Kontext-Zusammenfassungen überstanden.

**Was das gebracht hat:**
- Kein Kopier- oder Schreibweisenfehler hat Studio erreicht.
- Wenn ein neuer Export kam, ließ sich in Sekunden zeigen, ob alte Blöcke noch passen. Dreimal (12., 13. und 19.10.) passten alle noch, und es musste nichts neu erzeugt werden.

## 5. Zweimal prüfen
1. **Eigene Prüfung** (maschinell, siehe oben, plus Durchsicht).
2. **Unabhängiger Prüf-Agent** mit frischem Kontext: Er bekommt nur Dateien und Auftrag, baut den Endstand selbst nach und schreibt eigene Skripte.
   - Er fand in **jedem** geprüften Paket echte mittlere oder hohe Befunde (8 von 8).
   - Beispiele: Ein Doppelklick bestätigte eine Rückfrage sofort. Ein Storno-Dialog konnte eine fremde Buchung löschen. Ein Testbogen war so nicht ausführbar.
3. **App-Prüfung in Studio** nach jedem Schritt (keine roten Fehler).
4. **Josias’ Tests** nach dem Testbogen.
5. **Neuer Export → maschineller Abgleich** gegen den Soll-Stand.

Die drei Pakete, die auf Wunsch **ohne** unabhängige Prüfung rausgingen, sind genau die, bei denen das Risiko heute am wenigsten bekannt ist.

## 6. Die teuersten Lehren (übertragbar)
**Prozess:**
- **Erst klären, dann bauen.** Ein Gesamtplan mit 253 Properties entstand, bevor Muss-Liste, Freigabe-Weg und Storno-Variante entschieden waren. Danach kamen drei Fassungen. Besser: Muss-Liste und Einfrierpunkt mit Josias festlegen, dann kleine Pakete.
- **Gemeldeter Stand ≠ Stand.** Nur der Export zählt, auch bei der eigenen Schwester-App. Ein anderer Chat kann weiter sein als der Export (YAML-Quellen), deshalb vorher fragen.
- **Nutzertexte erst nach dem Abgleich.** Kurzanleitung und Handbuch beschrieben Funktionen, die nie eingefügt wurden.
- **Betrieb früh:** Datenübernahme aus dem Altsystem, Rechte, Vertretung, Verteilung aufs Handy. Diese Fragen wurden am Tag vor dem Go-Live zu den größten Risiken.
- **Jede Regel gegen jeden Weg prüfen**, auf dem Daten entstehen oder eine Aktion startet: Dialog, Panel, Verlängern, Stornieren, Flow, Import, **und jede Fläche, die etwas öffnet** (Karten, Kacheln). Einen Fehler fand Josias selbst, weil nur Schreibstellen geprüft waren.
- **Tests als Zeitachse** und nur mit dem, was die App wirklich zulässt.
- **Sichtprüfung nur gegen eine unabhängige Quelle.** Ich habe einmal ein Bild aus falsch sortierten Daten gezeichnet und damit dieselben Daten „bestätigt“.

**Power Apps (falls deine App auch eine ist):**
- Doppelklick: `DisplayMode` allein sperrt nicht (gemessen). Jede Schreibstelle braucht eine Sperre über `varIsLoading` und eine Zeitsperre.
- `Now()`/`Today()` in Anzeige- und Datenformeln rechnen nicht von selbst neu: Zeitpunkt in eine Variable oder einen Timer-Takt legen.
- `usenonblockingonstartrule`: Der Bildschirm ist da, bevor `App.OnStart` fertig ist. Anzeigen an die zuletzt gesetzte Variable koppeln oder benannte Formeln nehmen.
- Unsichtbare Steuerelemente fragen trotzdem ab.
- SharePoint-Delegation genau beachten. Werte in Server-Filter über globale Variablen geben.
- Reihenfolge von SharePoint-Zeilen nie annehmen, sondern belegen.
- Deutsche Schreibweise in Studio, immer die **ganze** Property.

## 7. Vorlage für den Startprompt des Einsetz-Chats (anpassen)
> Du begleitest mich (Josias) beim Einfügen von `<ÜBERGABE>.md` in Power Apps Studio. Lies die Datei ganz.
>
> Pro Nachricht **ein** Schritt:
> 1. Was er löst, in einem Satz.
> 2. Wo ich klicke (Steuerelement, Property; neue Steuerelemente: anlegen und exakt benennen).
> 3. Den Block **unverändert** aus der Datei. Nie Formeln umschreiben, kürzen oder verbessern.
> 4. Den Test nennen und auf mein Ergebnis warten.
>
> **Fehler:** Lass dir Schritt, Property und den wörtlichen Fehlertext geben. Prüf zuerst: ganze Property ersetzt? Name exakt? Reihenfolge eingehalten? Sonst nicht raten: Rückfall aus der Datei nennen, Fehler notieren, weiter mit dem nächsten unabhängigen Schritt.
>
> Passt die Datei nicht zur App (Steuerelement fehlt, Original sieht anders aus als im Anhang): **stoppen**, ich brauche einen neuen Export für den Bau-Chat.
>
> Nach jedem Schritt App-Prüfung und Strg+S. Führe eine Liste „Schritt | Ergebnis | Notiz“ und gib sie mir am Ende als Rückmeldung für den Bau-Chat. Am Ende: speichern, **Studio-Stand exportieren**, Export an den Bau-Chat.

## 8. Was ich beim nächsten Mal anders machen würde
- Am ersten Tag: Muss-Liste, Einfrierpunkt und Betriebsfragen (Daten, Rechte, Vertretung) mit Josias klären.
- Pakete klein halten (5–25 Properties), jedes einzeln einfügbar, testbar und rücknehmbar.
- Nach jedem Paket auf den Export warten, bevor das nächste auf einem angenommenen Stand aufbaut.
- Den Prüfstatus im Dokumentkopf aus den vorhandenen Dateien erzeugen. Einmal stand „unabhängig geprüft“ im Kopf, bevor die Prüfung lief.
- Erkenntnisse aus der einen App sofort als Prüfauftrag für die andere notieren.

Mehr Details und alle Fehler mit Belegen: `arbeit/2026-10-13_Retro/RETRO_AnalyseChat_2026-10-13.md` (42 Fehler, 12 Lösungen, 14 Regeln).
