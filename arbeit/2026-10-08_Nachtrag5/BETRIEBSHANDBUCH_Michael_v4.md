# Betriebshandbuch Tischbuchung (für Michael / IT), v4

> v4 (08.10., nach Grundriss-Sperre und Nachtrag 5): Grundriss-Sperre, kein automatisches Aktualisieren, Stornieren mit Bestätigung, Rechte nach Josias’ Entscheidung (nicht gesetzt), Lesezugriff nie einschränken. v1–v3 bleiben erhalten.

Stand 08.10.2026 · Verantwortlich: Josias · Vertretung: Michael/IT · **Michael ist ab 12.10. eine Woche im Urlaub (Go-Live-Woche). Vertretung für diese Woche: ________ (vor dem 12.10. eintragen)**

## 1. Was ist was
| Teil | Wo | Zweck |
|---|---|---|
| App **„Tischbuchung“** (Desktop, 1366 × 768) | Power Apps, Umgebung „Personal Productivity“. App-ID `d247d18b-d36f-4a44-975a-7839695b2f12`. **Nicht verwechseln** mit den Klonen „App“ und „App – Kopie“ | Tische buchen, Grundriss, eigene Buchungen verwalten |
| App **„Tischbuchung Handy“** | Power Apps, ID `e218702e-35cb-4dc8-813a-b9fd860c7f72` | Buchen, Einchecken, Verlängern am Handy (Power Apps Mobile) |
| Liste **`Tischbuchungen`** | SharePoint-Site `IMSKonzept` | eine Zeile pro Buchung: `Tisch` (Lookup), `Person`, `Startzeit`, `Endzeit`, `CheckedIn` (intern `Checkedin`), `SerienID` |
| Liste **`Tische`** | SharePoint-Site `IMSKonzept` | 34 Tische (OG 16, UG 18 inkl. Big Table), Spalte `Gesperrt` (Ja/Nein) |
| Listen `Räume`, `Raumbuchungen` | SharePoint | alter Raumcode, ungenutzt (Räume laufen über Outlook) |
| Aufräum-Flow (täglich 03:00) | Power Automate, Besitzer Josias | löscht Buchungen, deren Ende mehr als 7 Tage zurückliegt (laut Doku). Läuft mit Josias’ Verbindung (Vollzugriff), deshalb von „nur eigene Elemente“ nicht betroffen. Künftige Flows: Verbindung mit Vollzugriff, nicht an ein persönliches Konto binden, das wegfallen kann. **Zeilen, die ein Flow anlegt, gehören dem Konto der Verbindung.** Die Personen können sie dann in der App nicht einchecken, verlängern oder stornieren |
| Repo `tischbuchung-app` | GitHub | Dokumentation, Pläne, Werkzeuge (Python), `CLAUDE.md` mit allen Fakten |

## 2. Regeln, die die App durchsetzt
- Buchbar von **06:00 bis 22:00**, nicht in der Vergangenheit, Serien Mo–Fr für höchstens 14 Tage.
- Kein Tisch doppelt belegt. Keine Person zur selben Zeit an zwei Tischen.
- Einchecken ab 30 Min vor bis 30 Min nach Beginn. **Ohne Check-in verfällt die Buchung 30 Min nach Beginn** (bei später Buchung: 30 Min nach dem Buchungszeitpunkt). Sie bleibt in der Liste stehen, die Apps behandeln den Tisch aber als frei. **Es gibt keinen Flow dafür, die Regel steckt in der App** (`varFreigabeMinuten` in `App.OnStart`).
- Auschecken nach Beginn beendet die Buchung (Ende = jetzt), nach einem zweiten Tippen. Vor Beginn nimmt es nur den Check-in zurück. Andere sehen den Tisch als frei, sobald ihr Grundriss neu geladen ist, **spätestens beim nächsten Bedienen** (der Grundriss sperrt sich nach 2 Minuten bis zum Aktualisieren). Buchbar ist er ab der nächsten halben Stunde.
- **Kein automatisches Aktualisieren:** Die Desktop-App lädt nur beim Tippen (Aktualisieren, Grundriss-Knopf, Buchen, Stornieren, Verlängern, Einchecken). Der Timer zählt nur die Zeit (alle 15 s) und fragt höchstens alle 5 Min nach dem Check-in, wenn eine eigene Buchung ansteht. Die Dashboard-Listen zeigen neue Buchungen (z. B. vom Handy) erst nach „Aktualisieren“. Die Sperrzeit steht in `App.OnStart` (`varGrundrissSperreSekunden`, 120).
- Verlängern nie über 22:00, keine zwei Tische zur selben Zeit. Stornieren mit Bestätigung (zweites Tippen, auch beim Mehrfach-Storno), nur eigene Buchungen.
- Gesperrte Tische (`Tische.Gesperrt = Ja`) sind nicht buchbar. **Sperren/Entsperren: direkt in der Liste `Tische`.**
- **Rechte auf `Tischbuchungen` (Stand 08.10., Josias’ Entscheidung):** „Nur eigene Elemente bearbeiten“ ist **nicht** gesetzt. Grund: Die Liste nutzt nur die App. **Folge:** Wer die Liste im Browser öffnet, kann fremde Buchungen ändern oder löschen. Die App selbst storniert nur eigene Buchungen (Prüfung auf die E-Mail). Wenn das später gewünscht ist: Listeneinstellungen → Erweiterte Einstellungen → Berechtigungen auf Elementebene → **Bearbeiten: nur eigene**. Ausgenommen sind dann nur Konten mit „Listenverhalten außer Kraft setzen“ (Vollzugriff, Entwerfen). Mitglieder besser **Mitwirken** statt Bearbeiten. Auf `Tische` nur **Lesen**, damit nur Josias Tische sperrt.
- **Lesezugriff nie einschränken.** „Lesen: nur eigene Elemente“ darf auf `Tischbuchungen` **nie** gesetzt werden. Beide Apps lesen fremde Buchungen, um belegte Tische zu erkennen (Grundriss, Tischliste, Kollisionsprüfung beim Buchen, Verlängern und Einchecken). Mit eingeschränktem Lesen sähen alle jeden Tisch als frei → Doppelbuchungen.

## 3. Häufige Fälle
| Fall | Was tun |
|---|---|
| „Ich sehe meine Buchung nicht“ / „Status Verfallen“ | App neu laden (Aktualisieren-Symbol). In der Liste `Tischbuchungen` nach Person filtern. „Verfallen“ heißt: nicht bis 30 Min nach Beginn eingecheckt, der Tisch ist frei. Das ist so gewollt. Neu buchen |
| Buchung versehentlich gelöscht | SharePoint-Site → Papierkorb → wiederherstellen |
| Tisch defekt | In `Tische` `Gesperrt = Ja`. Bestehende Buchungen für diesen Tisch in `Tischbuchungen` anpassen und Betroffene informieren |
| Doppelbuchung gemeldet | In `Tischbuchungen` nach Tisch und Zeit filtern. **Überlappung ist normal, wenn die ältere Buchung nicht eingecheckt und verfallen war** (CheckedIn = Nein, **Beginn und Erstellt** der älteren liegen mehr als 30 Min vor dem **Erstellt** der neuen). Sonst ist die Buchung mit der **höheren ID** die spätere → mit der Person klären und löschen |
| App zeigt rote Fehlermeldung | Screenshot und Uhrzeit notieren. App neu laden. Bei Wiederholung: Power Apps → App → **Monitor** öffnen, Aktion wiederholen, Trace exportieren → an Josias |
| App nach einer Änderung kaputt | Power Apps → App → **Versionsverlauf** → letzte funktionierende Version **Wiederherstellen** → veröffentlichen |
| Freigabe falsch (Tisch frei, obwohl jemand da ist) | Hat die Person eingecheckt? In der Liste `CheckedIn` prüfen. Notfalls die Person neu buchen lassen. Bei Häufung Josias informieren |
| Neuer Mitarbeiter | App (und ggf. Handy-App) mit ihm **teilen** (Datei → Teilen), Leserecht auf die Site, Bearbeiten auf `Tischbuchungen` (gilt über die Site-Mitgliedschaft) |
| „Der Grundriss ist blass / lässt sich nicht antippen“ | So gewollt: 2 Minuten nach dem letzten Laden. „Grundriss aktualisieren“ tippen. Kommt die Warnung „Grundriss konnte nicht aktualisiert werden“: Netzwerk prüfen, erneut tippen |
| „Meine Handy-Buchung fehlt am PC“ | Aktualisieren-Symbol tippen. Die Desktop-App lädt nicht von selbst |
| Notbetrieb (App geht gar nicht) | Buchungen direkt in der Liste `Tischbuchungen` anlegen, **CheckedIn = Ja** setzen, sonst verfällt sie 30 Min nach dem Anlegen. Die App zeigt sie an, sobald sie wieder läuft |
| Notbuchung für jemand anderen | In der Liste anlegen, Spalte `Person` = die Person, **CheckedIn = Ja** (sonst verfällt sie 30 Min nach dem Anlegen). Solange „nur eigene Elemente“ **nicht** gesetzt ist, kann die Person sie in der App einchecken, verlängern und stornieren. Wird die Einstellung später gesetzt, zählt der **Ersteller** (du): Dann kann die Person nichts mehr daran ändern. Besser: Die Person bucht selbst |

## 4. Rechte und Besitz (einzurichten)
- Michael als **Mitbesitzer** der App „Tischbuchung“ (Datei → Teilen → Mitbesitzer), der Handy-App, der Listen (Site-Besitzer) und des Aufräum-Flows (Flow → Besitzer hinzufügen).
- Lizenzen: Alle Nutzer brauchen eine M365-Lizenz mit Power-Apps-Nutzungsrecht (nur Standard-Konnektoren).

## 5. Änderungen an der App
- Jede Änderung: vorher **Datei → Speichern unter → Diesen Computer** (`.msapp`), danach App-Prüfung, testen, veröffentlichen.
- Formeln stehen in deutscher Schreibweise (`;` trennt Argumente, `;;` verkettet).
- Hintergrund, Regeln und frühere Fehler stehen im Repo in `CLAUDE.md`. Pläne liegen unter `arbeit/`.

## 6. Bekannte Grenzen
- SharePoint hat keine Transaktionen: Buchen zwei Personen in derselben Sekunde denselben Tisch, erkennt die App das **danach** und meldet es dem Zweiten (rote Meldung). Sie verhindert es nicht.
- Die GoBright-Tischanzeigen sind ohne GoBright-Vertrag nicht nutzbar (Cloud-gebunden).
- Raumbuchung läuft über Outlook, nicht über die App.
