# ANLEITUNG_JOSIAS.md — Handy-App testen, freigeben, zurückrollen

**Kurzfassung:** Die Handy-App heißt **„Tischbuchung Handy"**. Sie ist veröffentlicht, aber noch mit niemandem geteilt. Du testest sie zuerst selbst auf einem iPhone und einem Android-Gerät (J1), gibst sie dann einer kleinen Testgruppe frei (J2) und entscheidest zum Schluss die offenen Regeln (J3). Deine Desktop-App „Tischbuchung" bleibt davon völlig unberührt; beide Apps arbeiten auf denselben SharePoint-Listen.

---

## 1. Die App

| | |
|---|---|
| Name | Tischbuchung Handy |
| App-ID | `e218702e-35cb-4dc8-813a-b9fd860c7f72` |
| Umgebung | Personal Productivity (`Default-84e2e900-49ec-4416-85fb-299b258a5227`) |
| **Link zum Öffnen** | https://apps.powerapps.com/play/e/default-84e2e900-49ec-4416-85fb-299b258a5227/a/e218702e-35cb-4dc8-813a-b9fd860c7f72 |
| Bearbeiten | make.powerapps.com → Apps → „Tischbuchung Handy" → Bearbeiten |
| Datenquellen | SharePoint `IMSKonzept`: Listen `Tischbuchungen` und `Tische` (dieselben wie die Desktop-App) |
| Lizenz | Standard, kein Premium-Konnektor |

**Beim allerersten Öffnen** fragt Power Apps: „Möchten Sie Tischbuchung Handy den Zugriff auf Ihre Daten gewähren?" → **„Zulassen"**. Das kommt bei jedem Nutzer genau einmal und ist normal. (Ich habe das bewusst nicht für dich angeklickt, siehe `FRAGEN_AN_JOSIAS.md` F-15.)

---

## 2. Selbst testen (J1)

Teste beide Wege auf **beiden** Geräten. Die App ist für Hochformat gebaut.

### iPhone
**A — im Browser (Safari):** Link oben öffnen → mit deinem Technoform-Konto anmelden → „Zulassen". Tipp: „Teilen" → „Zum Home-Bildschirm" legt ein Symbol an.
**B — Power Apps Mobile:** App „Power Apps" aus dem App Store installieren → mit dem Technoform-Konto anmelden → unter „Alle Apps" erscheint „Tischbuchung Handy" (eventuell erst nach „Aktualisieren"). Mit dem Stern als Favorit markieren.

### Android
**A — im Browser (Chrome):** Link öffnen → anmelden → „Zulassen". Menü ⋮ → „Zum Startbildschirm hinzufügen".
**B — Power Apps Mobile:** App „Power Apps" aus dem Play Store → anmelden → „Tischbuchung Handy" öffnen.

### Prüfliste für deinen Test (je Gerät abhaken)

| | Was | Erwartung |
|---|---|---|
| ☐ | App öffnen | Logo, „Tischbuchung", Aktualisieren-Symbol, deine Initialen; unten drei Reiter |
| ☐ | Reiter „Heute" | deine heutigen Buchungen mit Status; ohne Buchung ein Hinweis und „Zum Buchen" |
| ☐ | Reiter „Buchen" | Datum → Von/Bis → nur **freie** Tische, kein Big Table → Zusammenfassung → „Jetzt buchen" |
| ☐ | Buchung erscheint | in „Meine" **und** in der Desktop-App |
| ☐ | Einchecken | ab 30 Min vor Beginn bis zum Ende möglich, zweiter Tipp checkt **nicht** aus |
| ☐ | Verwalten → +1 / +2 Std | verlängert genau einmal, nie über 22:00 |
| ☐ | Verwalten → Jetzt beenden | Buchung endet jetzt, Tisch ist wieder frei |
| ☐ | Verwalten → Stornieren | mit Rückfrage, danach weg |
| ☐ | Schneller Doppeltipp auf Buchen/Verlängern | genau **eine** Wirkung |
| ☐ | Handy kurz quer drehen | App wird gestaucht, bleibt bedienbar (kein Absturz; siehe E-04) |
| ☐ | Auswahllisten (Von/Bis) | Die Einträge zeigen die richtigen Uhrzeiten. In der Studio-Vorschau zeigte die Bis-Liste einmal fälschlich überall „15:00" — bitte bei dir darauf achten (VERMUTUNG: nur Vorschau) |

**Bitte nur mit eigenen Testbuchungen** und hinterher stornieren.

---

## 3. Freigeben an eine Testgruppe (J2)

1. make.powerapps.com → Apps → Zeile „Tischbuchung Handy" → ⋯ → **Freigeben**.
2. Namen oder E-Mail der Testpersonen eingeben (oder eine Microsoft-365-Gruppe).
3. **Nicht** „Miteigentümer" anhaken — nur Benutzer.
4. Den Hinweis zu den Datenberechtigungen beachten: Die Personen brauchen in der SharePoint-Site `IMSKonzept` Leserechte auf `Tische` und Bearbeitungsrechte auf `Tischbuchungen`. Wer die Desktop-App schon nutzt, hat das bereits.
5. Haken „Einladung per E-Mail senden" nach Wunsch. Speichern.
6. Den Link aus Abschnitt 1 weitergeben, oder die Personen finden die App in Power Apps Mobile unter „Alle Apps".

**Rücknahme der Freigabe:** dieselbe Maske → Person entfernen.

---

## 4. Zurückrollen

**Eine ältere Version der Handy-App wiederherstellen:** make.powerapps.com → Apps → „Tischbuchung Handy" → ⋯ → Details → Reiter **Versionen** → bei der gewünschten Version ⋯ → **Wiederherstellen** → danach in Studio öffnen und **Veröffentlichen**. Die Version, die ich zuletzt geprüft habe, steht in `ABNAHME.md`.

**Die Handy-App ganz abschalten:** Freigaben entfernen (Abschnitt 3). Löschen ist nicht nötig. Auf die Desktop-App hat das keinen Einfluss.

**Daten:** Die Handy-App legt Buchungen genauso an wie die Desktop-App (gleiches Schema, siehe `APP_WISSEN.md` Abschnitt 3). Es gibt nichts zurückzurollen; einzelne Buchungen storniert man wie gewohnt.

**Ändern selbst:** Alle Steuerelemente liegen als YAML in `MOBIL\yaml\`. Studio nimmt sie über die Zwischenablage an (Container in der Strukturansicht auswählen, Strg+V). Wie das geht und welche Fallen es gibt, steht in `APP_WISSEN.md` Abschnitt 8a und 9.

---

## 5. Deine Entscheidungen (J3)

Für alle gilt bisher meine Vorentscheidung (Begründung in `FRAGEN_AN_JOSIAS.md` und `ENTSCHEIDUNGEN.md`):

| | Frage | jetzt so gebaut | dein Wunsch |
|---|---|---|---|
| V1 | Buchen für andere Tage | ja, bis 59 Tage voraus, keine Serien | |
| V2 | Check-in-Fenster | 30 Min vor Beginn bis Ende | |
| V3 | zweiter Tipp auf Einchecken | checkt nicht aus | |
| V4 | früher gehen | „Jetzt beenden" setzt Ende auf jetzt | |
| V5 | Verlängern | +1 / +2 Std, nie über 22:00 | |
| V6 | zwei Tische gleichzeitig | verhindert | |
| V7 | Big Table | am Handy nicht buchbar | |
| V8 | Stornieren | mit Rückfrage | |
| V9 | Schnellwahl | Ende mit 17:00 vorbelegt statt eigener Knöpfe | |
| F-12 | gleichzeitige Buchung (D7) | ehrliche Warnung, keine automatische Rücknahme | |
| E-05 | Start heute | ab der laufenden halben Stunde (Desktop: ab der nächsten) | |
| F-13 | Ausrichtung | dynamisches Layout, Ausrichtung nicht sperrbar | |
