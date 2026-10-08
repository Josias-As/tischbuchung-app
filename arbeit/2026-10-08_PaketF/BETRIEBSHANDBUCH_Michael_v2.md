# Betriebshandbuch Tischbuchung (für Michael / IT), v2

> v2 (08.10., Paket F): kein Freigabe-Flow mehr, „verfallene“ Buchungen, Notbuchungen. v1 bleibt im Ordner `2026-10-08_Gesamtplan`.

Stand 08.10.2026 · Verantwortlich: Josias · Vertretung: Michael/IT

## 1. Was ist was
| Teil | Wo | Zweck |
|---|---|---|
| App **„Tischbuchung“** (Desktop, 1366 × 768) | Power Apps, Umgebung „Personal Productivity“. App-ID `d247d18b-d36f-4a44-975a-7839695b2f12`. **Nicht verwechseln** mit den Klonen „App“ und „App – Kopie“ | Tische buchen, Grundriss, eigene Buchungen verwalten |
| App **„Tischbuchung Handy“** | Power Apps, ID `e218702e-35cb-4dc8-813a-b9fd860c7f72` | Buchen, Einchecken, Verlängern am Handy (Power Apps Mobile) |
| Liste **`Tischbuchungen`** | SharePoint-Site `IMSKonzept` | eine Zeile pro Buchung: `Tisch` (Lookup), `Person`, `Startzeit`, `Endzeit`, `CheckedIn` (intern `Checkedin`), `SerienID` |
| Liste **`Tische`** | SharePoint-Site `IMSKonzept` | 34 Tische (OG 16, UG 18 inkl. Big Table), Spalte `Gesperrt` (Ja/Nein) |
| Listen `Räume`, `Raumbuchungen` | SharePoint | alter Raumcode, ungenutzt (Räume laufen über Outlook) |
| Aufräum-Flow (täglich 03:00) | Power Automate, Besitzer Josias | löscht Buchungen, deren Ende mehr als 7 Tage zurückliegt (laut Doku) |
| Repo `tischbuchung-app` | GitHub | Dokumentation, Pläne, Werkzeuge (Python), `CLAUDE.md` mit allen Fakten |

## 2. Regeln, die die App durchsetzt
- Buchbar von **06:00 bis 22:00**, nicht in der Vergangenheit, Serien Mo–Fr für höchstens 14 Tage.
- Kein Tisch doppelt belegt. Keine Person zur selben Zeit an zwei Tischen.
- Einchecken ab 30 Min vor bis 30 Min nach Beginn. **Ohne Check-in verfällt die Buchung 30 Min nach Beginn** (bei später Buchung: 30 Min nach dem Buchungszeitpunkt). Sie bleibt in der Liste stehen, die Apps behandeln den Tisch aber als frei. **Es gibt keinen Flow dafür, die Regel steckt in der App** (`varFreigabeMinuten` in `App.OnStart`).
- Auschecken nach Beginn beendet die Buchung (Ende = jetzt). Vor Beginn nimmt es nur den Check-in zurück.
- Verlängern nie über 22:00. Stornieren nur mit Rückfrage.
- Gesperrte Tische (`Tische.Gesperrt = Ja`) sind nicht buchbar. **Sperren/Entsperren: direkt in der Liste `Tische`.**
- Liste `Tischbuchungen`: Jeder darf nur **eigene** Einträge bearbeiten. Besitzer dürfen alles.

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
| Notbetrieb (App geht gar nicht) | Buchungen direkt in der Liste `Tischbuchungen` anlegen, **CheckedIn = Ja** setzen, sonst verfällt sie 30 Min nach dem Anlegen. Die App zeigt sie an, sobald sie wieder läuft |
| Notbuchung für jemand anderen | Mit „nur eigene Elemente“ zählt der **Ersteller** (du), nicht die Spalte `Person`. Die Person kann diese Buchung in der App **weder einchecken noch stornieren oder verlängern**, das ist alles eine Änderung an deinem Element. Deshalb: beim Anlegen **CheckedIn = Ja** setzen (sonst verfällt sie), Änderungen machst du in der Liste. Besser: Die Person bucht selbst, sobald sie die App öffnen kann |

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
