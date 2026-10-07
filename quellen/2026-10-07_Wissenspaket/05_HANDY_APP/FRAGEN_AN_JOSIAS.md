# FRAGEN_AN_JOSIAS.md

**Kurzfassung:** Hier steht alles, was nur du entscheiden oder tun kannst. Oben das Dringendste. Solange du nichts sagst, arbeite ich mit der jeweils genannten Annahme weiter und baue nichts fest, was sich nicht leicht ändern lässt. Nichts davon blockiert mich gerade. Du hast gesagt, du stimmst meistens einfach zu, deshalb habe ich überall eine Vorentscheidung getroffen und sie begründet.

---

## Brauche ich von dir, damit es weitergeht

Zurzeit nichts. Falls beim Anmelden an make.powerapps.com eine Zwei-Faktor-Bestätigung kommt, melde ich mich hier und im Gespräch.

---

## Entscheidungen, die ich für dich getroffen habe

### F-01 — Neue App statt Kopie
**Meine Wahl:** neue Canvas-App.
**Grund:** Die Desktop-App ist auf Tablet 1366 × 768 mit absoluten Koordinaten gebaut (176 X- und 174 Y-Formeln, alle Container `ManualLayout`). Von 186 Steuerelementen bräuchte die Handy-App etwa 15. Eine Kopie leerzuräumen ist mehr Arbeit als ein Neubau und schleppt den toten Raumcode und Befund B0 mit.
**Umkehrbar?** Ja, aber teuer. Sag früh Bescheid, wenn du es anders willst.
**Ausführlich:** `ENTSCHEIDUNGEN.md` E-01

### F-02 — Welche Statusfarbe hat eine eingecheckte Buchung am Handy?
Deine Desktop-App hat dafür **zwei widersprüchliche Regeln**: Im Grundriss ist eingecheckt **rot**, auf der Dashboard-Karte **grün**. Das Abnahmekriterium A09 verlangt, dass die Handy-App der Grundriss-Logik folgt.

**Meine Wahl:** eingecheckt **grün** („Eingecheckt"), nicht eingecheckt orange („Einchecken") — also wie die Dashboard-Karte, nicht wie der Grundriss.
**Grund:** Eine Karte zeigt deine eigene Buchung. Rot heißt in der App sonst „belegt" oder „Fehler". Wer gerade erfolgreich eingecheckt hat, bekäme ein Warnsignal. Das 30-Minuten-Fenster des Grundrisses übernehme ich trotzdem, aber an der richtigen Stelle: Es entscheidet, ob der Einchecken-Tipp aktiv ist.
**Ausführlich:** `ENTSCHEIDUNGEN.md` E-A09

### F-13 — Die Ausrichtung lässt sich nicht sperren, wenn die App sich an jede Bildschirmgröße anpassen soll
Das Abnahmekriterium A03 verlangt beides: „Scale to fit aus" **und** „Ausrichtung gesperrt". In Power Apps schließt sich das aus. Es gibt nur ein Feld „App-Layout" mit zwei Werten:

- **Fest**: skaliert die App auf jedem Gerät hoch und runter. Dann lässt sich die Ausrichtung sperren.
- **Dynamisch**: kein Skalieren, die App passt sich echt an. Dann ist die Ausrichtungssperre ausgegraut.

**Meine Wahl:** Dynamisch. Der Zweck von A03 steht im zweiten Halbsatz — die App soll bei 390 × 844 und bei 360 × 800 die Breite füllen, ohne horizontal zu scrollen. Das geht nur dynamisch. Mit festem Layout gäbe es bei zwei verschiedenen Seitenverhältnissen Ränder oder Verzerrung.

**Praktische Folge:** Wer das Handy quer dreht, bekommt die App gestaucht und scrollbar zu sehen statt gar nicht. Nichts bricht, es sieht nur schlechter aus.
**Ausführlich:** `ENTSCHEIDUNGEN.md` E-04

### F-03 bis F-11 — die Vorgaben V1 bis V9
Für alle gilt der Standard aus dem Auftrag, bis du etwas anderes sagst:

| | Frage | gilt bei mir |
|---|---|---|
| V1 | Buchen auch für andere Tage? | ja, keine Serie |
| V2 | Check-in-Fenster | ab 30 Min vor Start bis Ende |
| V3 | Zweiter Tipp auf Einchecken | checkt **nicht** aus |
| V4 | Früher gehen | „Jetzt beenden" setzt die Endzeit auf jetzt |
| V5 | Verlängern | +1 und +2 Std, nie über 22:00 |
| V6 | Zwei Tische zur selben Zeit? | nein, wird verhindert |
| V7 | Big Table | am Handy nicht buchbar |
| V8 | Stornieren | mit Bestätigung |
| V9 | Schnellwahl-Knöpfe | erlaubt, aber ohne die teuren Abfragen der Desktop-Knöpfe |

### F-12 — Die Regel bei gleichzeitiger Buchung (D7)
SharePoint hat keine Transaktionen. Zwei Leute, die im selben Moment denselben Tisch buchen, können beide die Prüfung bestehen. Ich baue eine Nachlese ein: Nach dem Schreiben lese ich frisch nach, ob es für diesen Tisch und Zeitraum mehr als eine Buchung gibt.

**Die Frage ist, was dann passieren soll.** Ich lege dir den ausgearbeiteten Vorschlag mit ehrlicher Bewertung vor, sobald die Buchen-Funktion steht. Mögliche Regeln: Wer zuerst geschrieben hat, gewinnt (niedrigere ID). Oder: Die App nimmt die eigene Buchung zurück und sagt es dem Nutzer. Beides hat Nachteile, und eine automatische Rücknahme hat in diesem Projekt schon einmal Schaden angerichtet (Entwurf 2B).

**Vorerst:** Die App meldet den Konflikt ehrlich und nimmt nichts automatisch zurück.

---

## Für dich zum Schluss (zählen nicht für meine Abnahme)

- **J1** Test auf einem echten iPhone und einem echten Android-Gerät
- **J2** Freigabe an eine Testgruppe
- **J3** Deine endgültige Entscheidung zu V1–V9 und zur Regel aus F-12

Die Schritte dazu stehen am Ende in `ANLEITUNG_JOSIAS.md`.

---

## Kurze Rückfragen ohne Eile (blockieren nichts)

### F-14 — Hast du Version 23 der Desktop-App veröffentlicht?
Um 14:35 war in der Versionsliste der produktiven App **Version 20 „Live"**. Um 16:43 ist es **Version 23** (gespeichert um 14:12:58 von dir). Eine neue Version gibt es nicht, die höchste ist weiterhin 23. Das Veröffentlichen muss also zwischen 14:35 und 16:43 passiert sein.
**Von mir stammt es nicht:** Ich hatte die produktive App in diesem Zeitraum in keinem Studio-Fenster offen. Meine einzige Veröffentlichung um 16:41:43 betraf nachweislich „Tischbuchung Handy" (Meldung „Tischbuchung Handy is now available to everyone", Titelzeile des Studios). Beleg: `screenshots\A02_versionsliste_produktiv_ZWISCHENSTAND_2026-10-06_1643_V23_live.jpg`.
**Bitte nur kurz bestätigen**, dass du das warst. Als VERMUTUNG geführt, bis du es bestätigst.

### F-15 — Zustimmungsdialog beim ersten Start der Handy-App
Beim ersten Öffnen der veröffentlichten Handy-App fragt Power Apps: „Möchten Sie Tischbuchung Handy den Zugriff auf Ihre Daten gewähren?" (SharePoint, Datensätze lesen und schreiben). Das ist normal und kommt bei jedem Nutzer einmal. **Ich habe dort nichts angeklickt**, weil das Erteilen von Zugriffsrechten deine Entscheidung ist. Ich teste deshalb weiter in der Studio-Vorschau und nehme für den Zwei-Fenster-Test (A21) die Desktop-App als zweites Fenster, wie A21 es ausdrücklich erlaubt. Für deinen eigenen Test (J1) klickst du beim ersten Start auf „Zulassen".

---

## Hinweise, die dich betreffen, aber nichts von dir brauchen

- Die Befunde zu deiner Desktop-App stehen in `BEFUNDE_DESKTOP.md`. **Ich fasse die produktive App nicht an** (L1). Der wichtigste Befund ist BD-02 (Befund B0): Im Verwalten-Dialog des Buchungen-Tabs können die Verlängern-Knöpfe grün sein, obwohl die Verlängerung kollidiert. Das ist der einzige belegte Weg zu einer stillen Doppelbuchung. Die Korrektur K1 ist eine Zeile und steht in `ENTWURF_SPEICHERN.md`.
- Dein Datenzeilenlimit steht auf **1000**, nicht 2000. Steht so in `Properties.json` des Exports.
