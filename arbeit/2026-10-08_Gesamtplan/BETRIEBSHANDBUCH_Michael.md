# Betriebshandbuch Tischbuchung (für Michael / IT)

Stand 08.10.2026 · Verantwortlich: Josias · Vertretung: Michael/IT

## 1. Was ist was
| Teil | Wo | Zweck |
|---|---|---|
| App **„Tischbuchung“** (Desktop, 1366 × 768) | Power Apps, Umgebung „Personal Productivity“. App-ID `d247d18b-d36f-4a44-975a-7839695b2f12`. **Nicht verwechseln** mit den Klonen „App“ und „App – Kopie“ | Tische buchen, Grundriss, eigene Buchungen verwalten |
| App **„Tischbuchung Handy“** | Power Apps, ID `e218702e-35cb-4dc8-813a-b9fd860c7f72` | Buchen, Einchecken, Verlängern am Handy (Power Apps Mobile) |
| Liste **`Tischbuchungen`** | SharePoint-Site `IMSKonzept` | eine Zeile pro Buchung: `Tisch` (Lookup), `Person`, `Startzeit`, `Endzeit`, `CheckedIn` (intern `Checkedin`), `SerienID` |
| Liste **`Tische`** | SharePoint-Site `IMSKonzept` | 34 Tische (OG 16, UG 18 inkl. Big Table), Spalte `Gesperrt` (Ja/Nein) |
| Listen `Räume`, `Raumbuchungen` | SharePoint | alter Raumcode, ungenutzt (Räume laufen über Outlook) |
| Flow **„Tischbuchung – Freigabe ohne Check-in“** | Power Automate, Besitzer Josias | alle 5 Min: löscht laufende Buchungen, die 30 Min nach Beginn nicht eingecheckt sind |
| Aufräum-Flow (täglich 03:00) | Power Automate, Besitzer Josias | löscht Buchungen, deren Ende mehr als 7 Tage zurückliegt (laut Doku) |
| Repo `tischbuchung-app` | GitHub | Dokumentation, Pläne, Werkzeuge (Python), `CLAUDE.md` mit allen Fakten |

## 2. Regeln, die die App durchsetzt
- Buchbar von **06:00 bis 22:00**, nicht in der Vergangenheit, Serien Mo–Fr für höchstens 14 Tage.
- Kein Tisch doppelt belegt. Keine Person zur selben Zeit an zwei Tischen.
- Einchecken ab 30 Min vor Beginn bis Ende. **Ohne Check-in wird die Buchung 30 Min nach Beginn gelöscht** (Flow).
- Verlängern nie über 22:00. Stornieren nur mit Rückfrage.
- Gesperrte Tische (`Tische.Gesperrt = Ja`) sind nicht buchbar. **Sperren/Entsperren: direkt in der Liste `Tische`.**
- Liste `Tischbuchungen`: Jeder darf nur **eigene** Einträge bearbeiten. Besitzer dürfen alles.

## 3. Häufige Fälle
| Fall | Was tun |
|---|---|
| „Ich sehe meine Buchung nicht“ | App neu laden (Aktualisieren-Symbol). In der Liste `Tischbuchungen` nach Person filtern. Ohne Check-in hat der Freigabe-Flow sie evtl. gelöscht → **Papierkorb** der Site (93 Tage) |
| Buchung versehentlich gelöscht | SharePoint-Site → Papierkorb → wiederherstellen |
| Tisch defekt | In `Tische` `Gesperrt = Ja`. Bestehende Buchungen für diesen Tisch in `Tischbuchungen` anpassen und Betroffene informieren |
| Doppelbuchung gemeldet | In `Tischbuchungen` nach Tisch und Zeit filtern. Die Buchung mit der **höheren ID** ist die spätere → mit der Person klären und löschen |
| App zeigt rote Fehlermeldung | Screenshot und Uhrzeit notieren. App neu laden. Bei Wiederholung: Power Apps → App → **Monitor** öffnen, Aktion wiederholen, Trace exportieren → an Josias |
| App nach einer Änderung kaputt | Power Apps → App → **Versionsverlauf** → letzte funktionierende Version **Wiederherstellen** → veröffentlichen |
| Flow löscht falsch | Flow **ausschalten**. Gelöschtes aus dem Papierkorb holen. Josias informieren |
| Neuer Mitarbeiter | App (und ggf. Handy-App) mit ihm **teilen** (Datei → Teilen), Leserecht auf die Site, Bearbeiten auf `Tischbuchungen` (gilt über die Site-Mitgliedschaft) |
| Notbetrieb (App geht gar nicht) | Buchungen direkt in der Liste `Tischbuchungen` anlegen. Die App zeigt sie an, sobald sie wieder läuft |

## 4. Rechte und Besitz (einzurichten)
- Michael als **Mitbesitzer** der App „Tischbuchung“ (Datei → Teilen → Mitbesitzer), der Handy-App, der Listen (Site-Besitzer) und der beiden Flows (Flow → Besitzer hinzufügen).
- Lizenzen: Alle Nutzer brauchen eine M365-Lizenz mit Power-Apps-Nutzungsrecht (nur Standard-Konnektoren).

## 5. Änderungen an der App
- Jede Änderung: vorher **Datei → Speichern unter → Diesen Computer** (`.msapp`), danach App-Prüfung, testen, veröffentlichen.
- Formeln stehen in deutscher Schreibweise (`;` trennt Argumente, `;;` verkettet).
- Hintergrund, Regeln und frühere Fehler stehen im Repo in `CLAUDE.md`. Pläne liegen unter `arbeit/`.

## 6. Bekannte Grenzen
- SharePoint hat keine Transaktionen: Buchen zwei Personen in derselben Sekunde denselben Tisch, erkennt die App das **danach** und meldet es dem Zweiten (rote Meldung). Sie verhindert es nicht.
- Die GoBright-Tischanzeigen sind ohne GoBright-Vertrag nicht nutzbar (Cloud-gebunden).
- Raumbuchung läuft über Outlook, nicht über die App.
