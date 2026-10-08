@@ kopf
# Paket F: Freigabe in der App statt Flow, dazu der Storno-Fix

Stand 08.10.2026 · erzeugt aus dem Export 07.10. und den Endfassungen des Gesamtplans (`werkzeuge/paket_f.py`, `doc_paket_f.py`) · ersetzt Schritt **G-F** (Flow) des Gesamtplans · Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**

@@ kurzfassung
## 0. Kurzfassung
- **Was passiert:** Wer nicht bis 30 Minuten nach Beginn eingecheckt hat, **verliert den Tisch**. Die Buchung bleibt aber in der Liste stehen, sie heißt jetzt **„verfallen“**, und die App behandelt sie überall wie „frei“. **Es wird nichts gelöscht, und es gibt keinen Flow.**
- **Spät gebucht ist kein Problem:** Die 30 Minuten zählen ab dem späteren der beiden Zeitpunkte **Beginn** und **Buchungszeitpunkt** (SharePoint-Spalte `Erstellt`). Wer um 09:29 für 09:00 bucht, hat bis 09:59 Zeit.
- **Auschecken** beendet die Buchung jetzt (Ende = jetzt), der Tisch ist sofort wieder frei. Vor dem Beginn nimmt Auschecken nur den Check-in zurück.
- **Einchecken** geht ab 30 Minuten vor Beginn bis 30 Minuten nach Beginn (bisher: bis zum Ende).
- **Neu:** Die App **fragt nach dem Check-in**, beim Öffnen und alle 5 Minuten, wenn eine eigene Buchung gerade ansteht. Das gilt einmal je Buchung. Ein Klick genügt, ohne neues Steuerelement.
- **Storno-Fix:** Die Rückfrage merkt sich die Buchung beim Öffnen. Gelöscht werden nur eigene Buchungen. Ein dunkler Hintergrund sperrt alle anderen Klicks.
- **Umfang:** 8 Schritte, 44 Properties, 1 neues Steuerelement (`btnStornoHintergrund`). Einfügen **nach** dem Gesamtplan (Phasen 1–7). Jeder Block ist die **ganze Property** in ihrer Endfassung, inklusive aller Gesamtplan-Änderungen.
- **Ehrlich:**
  - Nichts davon ist in Studio getestet.
  - Alles ist aus dem Export erzeugt und maschinell geprüft: 0 Fehler, jede der 39 Abfragen auf `Tischbuchungen` einzeln eingeordnet.
  - Die Spalte `Erstellt` ist im Export **belegt** (lesbar, filterbar).
  - Ob Studio sie unter dem Namen `Erstellt` annimmt, steht unter UNSICHER (Test U1).

@@ regel
## 1. Die Regel (eine Zeile, überall gleich)
Eine Buchung ist **verfallen**, wenn alle drei Bedingungen gelten:
1. **nicht eingecheckt**,
2. **Beginn** liegt mehr als 30 Minuten zurück,
3. **Buchungszeitpunkt** (`Erstellt`) liegt mehr als 30 Minuten zurück.

In der App steht das als `!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze`, mit `varFreigabeGrenze = jetzt − varFreigabeMinuten`. Die 30 stehen **einmal** in `App.OnStart` (`Set(varFreigabeMinuten; 30)`). Willst du später 15 oder 45 Minuten, änderst du nur diese Zahl.

**Beispiele** (Buchung 09:00–17:00, heute um 08:00 angelegt):

| Uhrzeit | Was passiert |
|---|---|
| 08:30 | Einchecken möglich. Beim Öffnen der App fragt sie: „Check-in: OG Desk 5“ |
| 09:10 | Noch nicht eingecheckt → Kachel **orange** |
| 09:30 | Frist abgelaufen. Ab dem nächsten Laden (spätestens 5 Min, Timer) ist die Kachel **grün**. Ein Klick auf die Kachel prüft sofort frisch und öffnet den Buchungsdialog |
| 09:40 | Kollegin bucht den Tisch 10:00–12:00 → klappt. Die verfallene Buchung blockiert nicht |
| 09:45 | Du willst einchecken → „Zu spät: … verfällt die Buchung … Bitte neu buchen.“ Im Dashboard steht bei deiner Buchung **„Verfallen“** (grau) |

| Sonderfall | Ergebnis |
|---|---|
| Um 09:29 für 09:00 gebucht | Frist bis 09:59 (ab Buchungszeitpunkt) |
| Eingecheckt, um 11:17 ausgecheckt | Ende wird 11:18, der Tisch ist frei, die Buchung ist korrekt erledigt |
| Vor 09:00 eingecheckt und wieder ausgecheckt | Nur der Check-in wird zurückgenommen, die Buchung bleibt |
| Serie Mo–Fr | Jeder Termin für sich: Wer am Dienstag nicht eincheckt, verliert nur Dienstag |
| Verfallene eigene Buchung verlängern | geht nicht („Diese Buchung ist verfallen …“), stornieren geht |
| Eigene verfallene Buchung, neu buchen zur selben Zeit (anderer Tisch) | geht, die verfallene zählt nicht als „du hast schon einen Tisch“ |

@@ varianten
## 2. Wege, die ich geprüft habe

| Weg | Bewertung |
|---|---|
| **A. Flow löscht** (Gesamtplan G-F) | verworfen. Löscht in zwei Fällen falsch (spät gebucht, Auschecken). Läuft unter einem Konto. Daten sind weg. Josias will es nicht |
| **B. Die App löscht fremde Buchungen**, sobald sie verfallen sind | verworfen. Mit „nur eigene Elemente“ (G-R) darf niemand fremde Einträge löschen. Jede offene App würde gleichzeitig löschen (Konflikte) |
| **C. „Verfallen“ berechnen, nichts löschen** | **gewählt.** Kein Flow, keine Rechte-Probleme, keine zusätzlichen Anfragen für die Anzeige. Die No-Shows bleiben als Zahl erhalten (Auswertung möglich) |
| D. Neue Spalte `FreigabeAb` beim Buchen schreiben | verworfen. Alte Buchungen und die Handy-App hätten sie nicht. `Erstellt` setzt SharePoint immer selbst |
| E. Berechnete SharePoint-Spalte | verworfen. Kennt kein „jetzt“, und Power Apps kann danach nicht serverseitig filtern |
| F. Serverseitig nach `CheckedIn` filtern | verworfen. Ja/Nein-Spalten gelten in SharePoint als unzuverlässig delegierbar ([Community](https://powerappsguide.com/blog/post/sharepoint---filtering-data)). **Der Server filtert nur nach Zeit, Tisch und Person (delegierbar, belegt). `CheckedIn` und `Erstellt` prüft die App lokal auf dem kleinen Ergebnis.** Das ist dasselbe Muster wie die gemessene L2-Ladezeile |
| G. Check-in-Frage beim Öffnen und per Timer | **gewählt.** Nutzt den vorhandenen Check-in-Dialog, kein neues Steuerelement. Fragt nur einmal je Buchung |
| H. Automatisch einchecken, wenn jemand „für jetzt“ bucht | verworfen. Man kann auch von zu Hause buchen |
| I. QR-Code am Tisch → Handy-App checkt ein (`Param("tisch")`) | **später** (Handy-App). Würde „Einchecken von zu Hause“ verhindern. GoBright bietet dasselbe mit NFC/QR ([GoBright](https://gobright.com/?p=2189)) |
| J. Mail an No-Shows | später, braucht einen Flow. GoBright hat das als Option ([GoBright](https://gobright.com/new-features-and-innovation/new-features-improved-notifications-for-bookings/)) |

**Vergleich mit GoBright:** GoBright arbeitet mit einem Check-in-Fenster vor und nach Beginn. Ohne Check-in wird die Buchung beendet und als No-Show gezählt ([GoBright, Desk-Profil](https://gobright.com/?p=2189)). Paket F macht dasselbe, nur ohne Server-Dienst.

@@ nutzung
## 3. So arbeitest du das Paket ab
1. **Erst den Gesamtplan** (Phasen 1–7, ohne G-F) einfügen und testen. Paket F baut auf dessen Endfassungen auf. Die Blöcke enthalten alle Gesamtplan-Änderungen, ein vergessener Gesamtplan-Schritt bei diesen Properties wird also mit erledigt.
2. **Reihenfolge F1 → F8 einhalten.** F1 legt `varFreigabeMinuten` an, alle anderen lesen sie.
3. Je Property: Steuerelement suchen (Ort steht dabei), **ganze Property ersetzen**, Enter. Nach jedem Schritt App-Prüfung (keine neuen roten Fehler), Test, Strg+S.
4. Zwischen den Schritten bleibt die App lauffähig. Die Ladestellen können einzeln umgestellt werden, weil `colGrundriss` dieselben Spalten behält.
5. **Veröffentlichen** erst nach F8 und bestandenem Testbogen (Abschnitt 6).
6. **Rückfall:** Anhang A enthält die Fassung **vor** Paket F (Gesamtplan bzw. Export). Neues Steuerelement löschen.
7. Alle Blöcke sind deutsch (`;` trennt, `;;` verkettet). Nichts umschreiben.

@@ F1
**Problem:** Die 30 Minuten standen bisher nirgends. Die App fragte nie nach dem Check-in.
**Lösung:** `Set(varFreigabeMinuten; 30)` steht ganz oben (die eine Zahl zum Ändern). Am Ende, **vor** der Ladezeile, sucht die App die eigene Buchung, bei der gerade eingecheckt werden kann (Beginn in höchstens 30 Min, noch nicht zu Ende, nicht eingecheckt, nicht verfallen). Gibt es eine, öffnet sich der vorhandene Check-in-Dialog. Die Ladezeile lädt `Erstellt` mit und lässt verfallene Buchungen weg.
**Test (U1 zuerst):** Nach dem Einfügen: App-Prüfung ohne roten Fehler bei `Erstellt` (sonst siehe UNSICHER U1). Eigene Buchung „jetzt bis +1 Std“ anlegen, App schließen und neu öffnen (bzw. in Studio „App.OnStart ausführen“) → Check-in-Dialog erscheint. Ohne passende Buchung erscheint nichts.

@@ F2
**Problem (aus der unabhängigen Durchsicht, nachgeprüft):** Bei offener Storno-Frage war der Rest der App klickbar. Ein Klick auf eine Grundriss-Kachel setzte `varSelectedBuchung` auf deren Buchung, eventuell die eines Kollegen. „Ja, stornieren“ löschte dann diese.
**Lösung:**
1. Beim Klick auf „Stornieren“ wird die ID in `varStornoID` festgehalten. „Ja“ löscht nur diese.
2. Vor dem Löschen prüft die App, ob die Buchung der angemeldeten Person gehört (`Lower(E-Mail)`, weil Groß-/Kleinschreibung abweichen kann). Sonst: „Nur eigene Buchungen können storniert werden.“
3. Neuer Knopf `btnStornoHintergrund` über den ganzen Bildschirm, halb dunkel. Er fängt alle Klicks ab. Ein Klick daneben heißt „Nein“.

**Anlegen:** `Screen1` markieren → Einfügen → Schaltfläche (klassisch) → umbenennen in `btnStornoHintergrund`. Danach **`conStornoFrage` markieren → … → Nach vorne bringen**. Die Frage muss **über** dem Hintergrund liegen.
**Test:** Dashboard → Verwalten → Stornieren → die Frage erscheint auf dunklem Hintergrund. Klick auf eine Kachel → nichts passiert, die Frage schließt sich (= Nein). Nochmal → „Ja, stornieren“ → genau die gewählte Buchung ist weg. Dasselbe im Tab „Buchungen“ und mit Mehrfachauswahl.

@@ F3
**Problem:** Der Grundriss zeigt jede Buchung als belegt, auch wenn niemand gekommen ist.
**Lösung:**
- **Ladezeile** (an allen Stellen, die nur laden: Stockwerk, Datum, die vier Aktualisieren-Symbole): lädt `Erstellt` mit und übernimmt nur nicht verfallene Buchungen in `colGrundriss`. Kachel, Kreis, Initialen und „Belegt:“-Hinweis folgen automatisch.
- **Kachel-Klick (`btnHitArea`)** fragt frisch: Buchungen des Tisches holen, verfallene entfernen. Ist nichts übrig, öffnet sich der Buchungsdialog, sonst das Details-Popup.

**Test:** Testbuchung mit Beginn vor über 30 Min, ohne Check-in, z. B. direkt in der SharePoint-Liste angelegt (dann ist auch `Erstellt` alt genug, siehe Testbogen) → Aktualisieren → Kachel grün. Klick → Buchungsdialog.

@@ F4
**Problem:** Beide Speichern-Knöpfe würden eine verfallene Buchung als Kollision zählen. Die Nachlese hätte den eigenen neuen Termin sogar als „fast gleichzeitig vor dir gebucht“ gemeldet.
**Lösung:** Nach den beiden Abfragen „Tisch belegt“ und „ich habe schon einen Tisch“ entfernt die App verfallene Buchungen (`RemoveIf`). Die Nachlese ignoriert verfallene **fremde** Buchungen. Der eigene neue Termin (gleiche `SerienID`) bleibt immer drin. Die Erfolgsmeldung nennt die Minuten aus `varFreigabeMinuten`.
**Test:** Auf einen Tisch mit verfallener Buchung buchen → „Gebucht: …“ ohne Warnung. In SharePoint stehen beide Zeilen, die alte unverändert.

@@ F5
**Problem:** Die Tischliste im Panel und die Knöpfe 5 Std / 9 Std halten verfallene Buchungen für belegt.
**Lösung:** Beim Öffnen des Panels wird `varFreigabeGrenze` gesetzt. Die Liste rechnet für jede Buchung `Aktiv` aus und zählt nur aktive. Die beiden Knöpfe ebenso.
**Test:** Panel öffnen, heute, Zeit der verfallenen Buchung → der Tisch steht ohne „(an … belegt)“ in der Liste. 5 Std ist wählbar.

@@ F6
**Problem:** Wer an einem Tisch verlängern will, an dem eine verfallene Buchung hängt (z. B. weil man selbst darüber gebucht hat), wird fälschlich blockiert. Die eigene verfallene Buchung ließ sich verlängern.
**Lösung:** Beim Öffnen der Verwalten-Dialoge: die nächste Buchung am Tisch ohne verfallene bestimmen (Grenze für die Dauer-Knöpfe). Beim Verlängern: Kollisionen ohne verfallene. Eigene verfallene Buchung → „Diese Buchung ist verfallen … Bitte neu buchen.“
**Test:** Eigene Buchung, die eine verfallene fremde überlappt → +1 Std geht. Eigene verfallene Buchung → +1 Std → Meldung.

@@ F7
**Problem:** Einchecken ging bis zum Ende der Buchung. Mit der Freigabe könnte man um 11:00 einchecken, obwohl der Tisch seit 09:40 jemand anderem gehört. Auschecken setzte nur `CheckedIn` zurück, die Buchung blieb belegt.
**Lösung:**
- Einchecken nur von 30 Min vor Beginn bis zur Frist.
- Zusätzlich frisch prüfen, ob der Tisch in der Zeit schon an jemand anderen vergeben ist. Das schützt bei falsch gehender Uhr auf einem Gerät.
- Auschecken nach Beginn: Ende = jetzt (auf die nächste Minute), der Tisch ist frei. Vor Beginn: nur Check-in zurücknehmen.
- Im Dashboard steht bei verfallenen Buchungen „Verfallen“ in Grau.

**Test:** Buchung in 1 Std → „erst ab 30 Minuten vor Beginn“. Laufende Buchung → „Eingecheckt.“, Kachel rot. Danach Auschecken → „endet um hh:mm, der Tisch ist wieder frei“, Kachel grün. Verfallene Buchung → „Zu spät …“, Status „Verfallen“.

@@ F8
**Problem:** Wer die App morgens öffnet und offen lässt, bekommt keinen Hinweis, wenn die nächste Buchung ansteht.
**Lösung:** Der vorhandene 5-Minuten-Timer fragt zusätzlich nach dem Check-in. Bedingungen: Dashboard sichtbar, heutiger Tag, kein Dialog offen, und nur einmal je Buchung (`varCheckinGefragtID`).
**Test:** App offen lassen, eigene Buchung mit Beginn in 20 Min (vorher angelegt) → spätestens nach 5 Min erscheint der Check-in-Dialog. Schließen → er kommt für diese Buchung nicht wieder.

@@ handy
## 5. Für den Handy-Chat (bitte weitergeben)
Die Handy-App liest dieselbe Liste. **Ohne dieselbe Regel passt es nicht zusammen:**
- Die Handy-App zeigt einen freigegebenen Tisch weiter als belegt. Das ist harmlos.
- Sie lässt aber das Einchecken einer verfallenen Buchung zu, auch wenn der Tisch schon neu vergeben ist. **Dann sitzen zwei Personen „eingecheckt“ am selben Tisch.**

Deshalb muss die Handy-App vor dem Teilen dasselbe tun. Die Einzelheiten stehen in `AUFTRAG_Handy_Freigabe.md`.

@@ texte
## 7. Texte für Nutzer und Betrieb
Die neuen Fassungen liegen als eigene Dateien daneben, die alten bleiben erhalten:
- `KURZANLEITUNG_und_GoLive_Mail_v2.md`: Regel „bis 30 Min nach Beginn einchecken, sonst ist der Tisch weg“. Auschecken gibt den Tisch frei. „Ab sofort für den 14.10. buchen“. Kontakt per Mail statt Teams-Chat (solange es den Chat nicht gibt).
- `BETRIEBSHANDBUCH_Michael_v2.md`: kein Freigabe-Flow, „Verfallen“ erklärt. Überlappende Buchungen sind normal, wenn die ältere verfallen ist. Notbuchungen durch Michael kann die Person nicht selbst ändern.

@@ unsicher
## 8. UNSICHER (mit Test)

| Nr | Was | Test / Abhilfe |
|---|---|---|
| U1 | Studio nimmt die Spalte unter dem Anzeigenamen **`Erstellt`** an. Der Export führt `Created` mit Anzeigename „Erstellt“, und die App schreibt auch sonst Anzeigenamen (`CheckedIn` statt intern `Checkedin`), das ist belegt | Nach F1: App-Prüfung. Ist `Erstellt` rot, Claude Code melden: Der Generator setzt dann überall `Created` ein (ein Wort im Skript) |
| U2 | `DropColumns(…; "Erstellt")` mit Spaltenname als Text gilt bei `powerfxv1 = false` (wie `SortByColumns(…; "Startzeit")` in derselben App) | App-Prüfung nach F1. Rot → melden |
| U3 | Uhrzeiten der Geräte: Die Regel rechnet mit der Uhr des jeweiligen Geräts. Weicht sie ab, verschiebt sich die Freigabe um diese Abweichung. Abgesichert: Einchecken prüft frisch, ob der Tisch schon an jemand anderen vergeben ist | Firmengeräte gehen per Zeitserver richtig. Kein Test nötig |
| U4 | Position des Check-in-Dialogs beim App-Start: `conCheckinDialog.Y` richtet sich nach der Zeile in der Dashboard-Liste. Beim Start könnte die Liste noch laden | Test F1. Sitzt der Dialog falsch, wird er nach dem Laden richtig gesetzt (Formel reagiert). Sonst melden |
| U5 | Die Anzeige wechselt erst beim nächsten Laden von orange auf grün (Timer 5 Min, Aktualisieren-Symbol, jede Buchung). Der Klick auf die Kachel prüft immer frisch | gewollt, wie beim Flow (5 Min) |
| U7 | „Explizite Spaltenauswahl“: Power Apps lädt nur Spalten, die irgendwo benutzt werden. `Erstellt` wird überall direkt benutzt (`RemoveIf(col; … Erstellt …)`, `B.Erstellt`, `ThisItem.Erstellt`), sollte also geladen werden. Fehlt die Spalte doch, ist sie leer, und nur der Sonderfall „spät gebucht“ verliert seine Schonfrist (leer zählt wie „lange her“). Alles andere funktioniert | Testbogen: um hh:20 für hh:00 buchen, nicht einchecken → nach hh:30 muss die Kachel **orange** bleiben bis hh:50 |
| U6 | Testbuchungen „in der Vergangenheit“ kann die App nicht anlegen (Sperre). Für die Tests F3–F7 eine Zeile **direkt in der SharePoint-Liste** anlegen (Beginn vor 1 Std). `Erstellt` ist dann jetzt, die Frist läuft also erst 30 Min nach dem Anlegen ab | Testbogen: Testzeile anlegen, 30 Min warten oder `varFreigabeMinuten` in Studio vorübergehend auf 1 setzen (danach zurück auf 30!) |

@@ testbogen
## 6. Testbogen Paket F

| ✓ | Test | Ergebnis | Notiz |
|---|---|---|---|
| ☐ | Vorbereitung: in Studio `varFreigabeMinuten` in `App.OnStart` vorübergehend auf **1** setzen (schnelle Tests), am Ende **zurück auf 30** | | |
| ☐ | F1 App-Prüfung ohne rote Fehler (U1, U2) | | |
| ☐ | F1 Check-in-Frage beim Start erscheint bei anstehender Buchung, sonst nicht | | |
| ☐ | F2 Storno: Hintergrund dunkel, Klick daneben = Nein, richtige Buchung gelöscht (Dashboard, Tab, Mehrfach) | | |
| ☐ | F3 Verfallene Buchung (in SharePoint angelegt, Beginn vor 1 Std) → Kachel grün, Klick öffnet Buchungsdialog | | |
| ☐ | F4 Über die verfallene Buchung buchen → „Gebucht“, keine Warnung | | |
| ☐ | F5 Panel: Tisch ohne „belegt“, 5 Std wählbar | | |
| ☐ | F6 Verlängern über verfallene fremde Buchung geht, eigene verfallene → Meldung | | |
| ☐ | F7 Einchecken zu früh → Meldung; laufend → eingecheckt; Auschecken → Ende jetzt, Kachel grün; verfallen → „Zu spät“, Status grau | | |
| ☐ | F8 Erinnerung nach ≤ 5 Min, nur einmal | | |
| ☐ | U7 spät gebucht (mit 30 Min): um hh:20 für hh:00 buchen → Kachel bleibt bis hh:50 orange, erst danach grün | | |
| ☐ | **`varFreigabeMinuten` wieder 30** | | |
| ☐ | Doppelklick auf Einchecken → eine Änderung | | |
| ☐ | Veröffentlichen | | |

@@ spaeter
## 9. Später (nicht in diesem Paket)
- **QR-Check-in** am Tisch über die Handy-App (`Param("tisch")`): verhindert das Einchecken von zu Hause. Braucht Aufkleber je Tisch.
- **No-Show-Auswertung:** In SharePoint eine Ansicht „Verfallen“ anlegen (Filter: CheckedIn = Nein, Startzeit < heute). Damit siehst du, wie oft Tische ungenutzt blockiert wurden.
- **Mail an No-Shows** (nur mit Flow, wenn gewünscht).
- **Aufräum-Flow (täglich 03:00, laut Doku vorhanden):** löscht Buchungen, die älter als 7 Tage sind, also auch die verfallenen. Wer No-Shows auswerten will, setzt die Frist dort hoch.
