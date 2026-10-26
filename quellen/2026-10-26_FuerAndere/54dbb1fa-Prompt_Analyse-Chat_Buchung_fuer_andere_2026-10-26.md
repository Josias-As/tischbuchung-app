# Auftrag für den Analyse-Chat: „Für andere buchen“ + weicher 2er-Hinweis (Tischbuchungs-App)

Du hast den größten Teil dieser App mitgebaut. Ich schicke dir den aktuellen **App-Export** mit. Was dort steht, gilt als Wahrheit; was ich dir unten schreibe, ist nur das, was der Export nicht beantwortet (Entscheidungen, Rahmenbedingungen, Arbeitsweise). Bei Widerspruch zwischen diesem Text und dem Export gewinnt der Export, sag mir dann kurz Bescheid.

## 1. Aufgabe
Ich bin Josias, Werkstudent Digitalisierung bei Technoform. App: Power-Apps-Canvas-App **„Tischbuchung“** (Umgebung „Personal Productivity“, App-ID d247d18b-d36f-4a44-975a-7839695b2f12), SharePoint-Listen `Tische` und `Tischbuchungen`. Zwei Änderungen:

1. **Der Hinweis bei bereits 2 Buchungen bleibt, sperrt aber nicht mehr.** Wer schon 2 Tische gebucht hat, bekommt einen Dialog („Trotzdem buchen“ / „Abbrechen“) und darf dann einen weiteren buchen.
2. **Alle Mitarbeitenden dürfen einen Tisch für jemand anderen buchen.** Es kommen manchmal Externe, daher Freitext-Name (kein Personenfeld, kein Verzeichnis).

## 2. Bereits entschieden (nicht neu verhandeln)
- Alle dürfen für andere buchen, keine Rollenprüfung, keine Berechtigungsliste.
- Neue SharePoint-Spalte **`GastName`** (eine Textzeile, optional) in `Tischbuchungen`. **Ich lege sie an**, du schlägst nichts anderes vor, außer du findest im Export einen konkreten Grund dagegen.
- `Person` bleibt immer der Buchende. Stornieren und Einchecken laufen weiter über ihn.
- Für andere gebuchte Tische (GastName nicht leer) zählen **nicht** zu den 2 eigenen und lösen keinen Hinweis aus.
- Hinweistext nennt als Ansprechpartner **Axel Krägelius (PC-Admin)** und **Norman Horn (Admin, NHN IT)**. Das ist eine Annahme von mir aus einer knappen Notiz; frag mich, falls im Export etwas dagegen spricht.
- Anzeige überall, wo der Buchende steht: Gastname, dazu „gebucht von <Buchender>“. Altbestand ohne GastName darf sich optisch nicht ändern.

## 3. Rahmenbedingungen, die nicht im Export stehen
- **Keine Premium-Lizenzen**, nur SharePoint. Keine Premium-Connectoren, kein Dataverse. Unternehmensfokus ist Geld sparen.
- Power Apps Studio in **deutscher Locale**: Semikolon als Trennzeichen, Formeln entsprechend.
- Die App ist **live** (Go-Live 14.10.), echte Kollegen nutzen sie. Es gibt keine freie Testumgebung; ich teste in einer Kopie, bevor ich das Original anfasse. Nichts am Original ändern, was nicht ausdrücklich als Änderung ausgewiesen ist.
- Es gibt zusätzlich eine eigene **Handy-App „Tischbuchung Mobil“**. Sie bleibt in diesem Auftrag außen vor und wird erst nach Abnahme der Desktop-Änderung angepasst. Dort gilt bisher: eine Person darf nicht zwei Tische gleichzeitig haben (die Desktop-App prüft das nicht). Ob das für Gast-Buchungen gelockert wird, entscheiden wir später.
- Ein nächtlicher Flow löscht Buchungen mit Endzeit älter als 7 Tage. Er soll von der Änderung unberührt bleiben; bitte bestätigen, dass er nicht auf `GastName` oder die Zählung reagiert.
- **Tenant-/Berechtigungsfragen** gehen an Michael (IT) und weiter an einen externen Dienstleister. Du löst sie nicht, sondern sagst mir, was ich ihm schreiben muss. Hier sollte keine nötig sein.
- **Finale Tischkoordinaten** (colTischPositionen, colTischPositionenUG) und das Grundriss-Layout sind bestätigt und dürfen nicht angefasst werden.

## 4. Was aus der Projekthistorie gilt (kurz)
- Die App hatte mehrfach Probleme durch **toten Code** (alte Raumbuchungs-Reste verursachten einen app-weiten Schema-Cache-Fehler). Bitte prüfe, ob deine Änderung über eigene Variablen mit klarem Präfix läuft und nichts Neues ins Ungenutzte legt.
- Dialoge und Overlays liegen direkt im Screen, nicht in Auto-Layout-Containern (dort werden X/Y ignoriert).
- Das App.OnStart-/Reset-Muster schließt Popups bei Etagen-, Datums-, Tab- und Mehrfachauswahl-Wechsel. `tglFuerAndere` und `txtGastName` müssen dort ebenfalls zurückgesetzt werden.
- Vorhandene Funktionen, die unverändert funktionieren müssen: Mehrfachauswahl-Buchung, Serienbuchung (2-Wochen-Deckel mit Notify), Check-in/Auschecken, Verwalten-Dialog, OG/UG-Wechsel, performanceoptimierte Speicherlogik, Ladeoverlay.
- Schreiboperationen haben bisher kaum Fehlerbehandlung (Bug „Item Not Found“ zeigte den rohen Connector-Fehler). Neue Schreibpfade bitte in `IfError` mit verständlicher Notify-Meldung.

## 5. Arbeitsweise (wichtig)
- **Erst diagnostizieren, dann ändern.** Zeig mir zuerst, wo im Export die heutige 2er-Prüfung liegt, wie gezählt wird und welche Buttons speichern (Einzel, Mehrfach, Serie). Dann der Änderungsplan, dann die Formeln.
- **Spaltennamen nur aus dem Export**, nicht aus dem Gedächtnis (Schreibweisen wie CheckedIn/Checkedin waren uneinheitlich).
- **Jeden Schritt mit Vorher/Nachher und Rückweg dokumentieren**, damit ich alles rückgängig machen kann.
- **Vollständige, direkt einfügbare Formelblöcke**, keine Teilstücke, keine Platzhalter. Ich füge sie selbst im Power Apps Studio ein. Du hast keinen Zugriff darauf.
- Antworten knapp, auf Deutsch, Umlaute normal. Erklärungen nur, wenn ich frage. Schonungslos ehrlich, auch zu meinen Entscheidungen.
- Wenn ein Ansatz scheitert, verwirf ihn ganz und nimm einen anderen, statt ihn zu flicken. Lieber ein Problem unmöglich machen als reparieren.
- Bei Unsicherheit: markiere „[UNSICHER]“ und sag, wie ich es im Studio prüfen kann.

## 6. Reihenfolge
0. Diagnose aus dem Export (siehe oben).
1. Ich lege `GastName` an und aktualisiere die Datenquelle (kein Neuverbinden).
2. UI: Umschalter `tglFuerAndere`, Textfeld `txtGastName` (nur sichtbar wenn an, Pflicht wenn an).
3. Zähl- und Hinweislogik: eigene Buchungen = Person ist ich **und** GastName leer, delegierbarer Filter, Tagesgrenzen als Named Formulas. Dialog statt Sperre.
4. Speichern mit `GastName` für Einzel-, Mehrfach- und Serienbuchung.
5. Anzeige in Grundriss-Info, „Tischbuchungen heute“, Buchungen-Tab, Verwalten-Dialog.
6. Tests (liefere eine Checkliste): 0/1 eigene Buchung ohne Meldung; 2 eigene, dritte mit Dialog (Abbrechen speichert nichts); Gast ohne Namen blockiert; Gast bei bereits 2 eigenen ohne Dialog und ohne Mitzählung; Storno und Check-in durch den Buchenden; Mehrfach und Serie mit Gast; Altbestand unverändert.

## 7. Offene Fragen an mich (stell sie gebündelt, bevor du baust)
- Rolle von Axel Krägelius und Norman Horn, falls im Export ein Hinweis darauf ist.
- Soll der Gastname auch im Grundriss-Tooltip stehen oder nur in den Listen?
- Was soll bei Serienbuchung für Gäste gelten (gleiche Regeln wie für mich)?
