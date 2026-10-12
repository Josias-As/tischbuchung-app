# Beide Apps online bringen und die Handy-App auf den Home-Bildschirm (12.10.2026)

Kennzeichnung:
- **belegt**: Microsoft-Dokumentation, über die Websuche gelesen. `learn.microsoft.com` direkt war aus der Arbeitsumgebung gesperrt.
- **Community**: Forenberichte.
- **geschlussfolgert** und **UNSICHER** wie gewohnt.

## Kurzfassung
- **Empfehlung Handy: Power-Apps-App + Verknüpfung auf dem Home-Bildschirm.** Das ist der einzige Weg, der
  1. von Microsoft für Handys empfohlen ist,
  2. mit dem Firmenkonto per Single Sign-on läuft,
  3. **ohne Admin** geht. Michael ist ab heute im Urlaub.
  - Android: in der Power-Apps-App „An Startseite anheften“ (Pin to Home).
  - iPhone: über Siri-Kurzbefehle → App „Kurzbefehle“ → „Zum Home-Bildschirm“ (belegt).
- **Nicht** über den Handy-Browser (Safari/Chrome) als Lesezeichen.
  - Microsoft empfiehlt dafür ausdrücklich die Power-Apps-App (belegt).
  - Safari kann seit iOS 14 Power Apps nicht mehr an den Home-Bildschirm heften (belegt).
  - Im Forum gibt es Anmeldeprobleme im Handy-Browser (Community).
- **Nicht vor dem Go-Live:**
  - „Wrap“ als eigene App: braucht Entra-App-Registrierung, Azure Key Vault und Verteilung über Intune.
  - Automatisch angeheftete Teams-App: braucht Teams-Admin.
  - Beides geht nur mit Michael. Nach seinem Urlaub kann man es neu bewerten.
- **Desktop-App:** teilen, Link verteilen und als Browser-Favorit oder in Teams anheften. Dafür ist kein Admin nötig.
- **Firmenkonto und Firmenhandy:**
  - Beide Apps lesen die SharePoint-Listen mit dem angemeldeten Firmenkonto.
  - Läuft die Anmeldung auf dem Firmenhandy schon für Outlook und Teams, läuft sie auch in der Power-Apps-App (geschlussfolgert).
  - **Am Montag beim Gerätetest prüfen.** Ist die Anmeldung auf Firmenhandys an verwaltete Geräte gebunden (Conditional Access/Intune), muss die Power-Apps-App dort erlaubt sein (UNSICHER, nur IT kann das sehen).

## 1. Die Wege im Vergleich
| Weg | Was der Nutzer sieht | Voraussetzungen | Bewertung |
|---|---|---|---|
| **A Power-Apps-App + Home-Symbol** | Symbol auf dem Home-Bildschirm, öffnet direkt „Tischbuchung Handy“ | Power-Apps-App aus App Store/Play Store (oder Firmenportal), Anmeldung mit Firmenkonto | **Empfohlen.** Kein Admin nötig. iPhone: generisches Kurzbefehl-Symbol, das Bild lässt sich beim Anlegen ändern (Community) |
| B Teams (Handy) | App in Teams unter „Mehr“ | Teams-App erstellen. Für automatisches Anheften eine Teams-Richtlinie (Admin) | später. Laut Forum taucht die App mobil teils nur unter „Mehr“ auf. Läuft innerhalb von Teams, ein Klick mehr |
| C Handy-Browser + Lesezeichen | Safari-/Chrome-Lesezeichen | nur der Link | **nicht empfohlen.** Canvas-Apps im Handy-Browser sind unsicher, Microsoft empfiehlt die App (belegt). Anmeldeprobleme im Forum |
| D Wrap (eigene App mit eigenem Symbol) | echte App „Tischbuchung“ | Entra-App-Registrierung, Azure-Abo (Key Vault, Blob), Signierung, Verteilung über Intune oder Apple Business Manager (belegt) | sauberste Lösung, aber Tage Aufwand und nur mit IT. **Nach dem Go-Live** prüfen |

## 2. Reihenfolge vor dem Go-Live (Josias, ohne Admin)
1. **Beide Apps veröffentlichen.** In Studio Datei → Speichern → Veröffentlichen, vorher die Sicherung `.msapp`.
2. **Beide Apps teilen** (Power Apps → App → Teilen):
   - Am einfachsten mit einer Gruppe, die alle Nutzer enthält, z. B. der Mitgliedergruppe der SharePoint-Site oder einer Verteilerliste/Microsoft-365-Gruppe. Rolle **Benutzer**, nicht Mitbesitzer.
   - Beim Teilen fragt Power Apps nach den Datenverbindungen. SharePoint läuft mit dem eigenen Konto jedes Nutzers.
3. **SharePoint-Rechte prüfen** (siehe Betriebshandbuch v4):
   - Alle Nutzer müssen `Tischbuchungen` **lesen und bearbeiten** und `Tische` **lesen** können.
   - **Lesen nie auf „nur eigene Elemente“**, sonst sind alle Tische frei.
4. **Links holen:** Power Apps → App → … → Details → **Web-Link**. Bitte genau diesen Link verwenden.
   - Er enthält Umgebung und Mandant (Format `apps.powerapps.com/play/e/<Umgebung>/a/<App-ID>?tenantId=…`).
   - Mobile Deep-Links ohne Umgebungs-ID werden laut Microsoft nicht mehr unterstützt (belegt). Also keine alten oder selbst gebauten Links.
5. **Test mit einem Kollegen** (Montag): Firmenhandy, Power-Apps-App, Home-Symbol nach Abschnitt 3, buchen und am PC gegenprüfen.
6. **Go-Live-Mail** (Kurzanleitung v4) mit beiden Links und dem Abschnitt „Handy“ unten.

## 3. Anleitung für die Kollegen: Handy-App auf den Home-Bildschirm
**Einmalig:**
1. App **„Power Apps“** von Microsoft installieren. Sie kommt aus dem App Store bzw. Google Play, auf verwalteten Firmenhandys ggf. aus dem **Firmenportal**.
2. Öffnen und mit der **Firmen-E-Mail** anmelden.
3. In der Liste **„Tischbuchung Handy“** suchen. Nicht „Tischbuchung“, das ist die PC-Fassung und auf dem Handy winzig.
4. Optional: Stern = Favorit, dann steht die App immer oben.

**Android** (die Schritte unterscheiden sich je nach Hersteller etwas):
1. In der Power-Apps-App bei „Tischbuchung Handy“ auf **…** tippen.
2. **„An Startseite anheften“ / „Pin to Home“** wählen und bestätigen.

**iPhone** (iOS 14 oder neuer, Power-Apps-App aktuell):
1. In der Power-Apps-App „Tischbuchung Handy“ **nach rechts wischen** → **„Kurzbefehl“** (Shortcut).
2. **„Zu Siri hinzufügen“** tippen. Der Satz ist egal, z. B. „Tisch buchen“.
3. App **„Kurzbefehle“** öffnen → beim neuen Kurzbefehl auf **…** → Teilen-Symbol → **„Zum Home-Bildschirm“**.
4. Name „Tischbuchung“ eintragen, auf das Symbol tippen, falls ein eigenes Bild gewünscht ist → **Hinzufügen**.

Nach dem Tippen auf das Symbol öffnet sich zuerst kurz die Power-Apps-App, dann direkt die Tischbuchung. Das ist normal.

**Klappt die Anmeldung nicht** („erfüllt nicht die Kriterien“): Screenshot an Josias. Dann blockiert eine Firmenrichtlinie die Power-Apps-App auf diesem Gerät. Das kann nur die IT freigeben.

## 4. Desktop-App
- Den **Web-Link** in die Go-Live-Mail aufnehmen und als Browser-Favorit empfehlen. Die Desktop-App ist für 1366 × 768 gebaut.
- **Optional in Teams** (ohne Admin, wenn eigene Apps erlaubt sind): Power Apps → App → … → **Zu Teams hinzufügen**.
  - Alternativ in einem Teams-Kanal als **Registerkarte** „Power Apps“ einfügen.
  - Das automatische Anheften für alle braucht eine Teams-Richtlinie (Admin) und kommt später.
- **Optional auf einer SharePoint-Seite:** ein Link oder Knopf „Tisch buchen“ zum Web-Link. Eine eingebettete App ist auf 1366 × 768 zu klein.

## 5. Nach dem Go-Live mit Michael (optional)
- **App hervorheben:** In der Power-Apps-App kann der Admin eine App als „hervorgehoben“ bzw. „Hero“ markieren. Dann steht sie für alle ganz oben.
  - Das geht per PowerShell (`Set-AdminPowerAppAsFeatured` / `Set-AdminPowerAppAsHero`). Geschlussfolgert aus den Admin-Befehlen, vor Gebrauch prüfen.
- **Power-Apps-App per Intune verteilen.** Wenn die Firmenhandys über Intune laufen, kann die IT die App direkt auf alle Firmenhandys schieben.
- **Wrap** für eine echte „Tischbuchung“-App mit eigenem Symbol. Der Aufwand steht in Abschnitt 1, Weg D.
- **Teams-Richtlinie:** „Tischbuchung“ für alle in Teams anheften.

## Quellen
- [Microsoft Learn: Power-Apps-App installieren und Apps an den Home-Bildschirm heften (iOS-Kurzbefehle, Android)](https://learn.microsoft.com/en-us/power-apps/mobile/run-powerapps-on-mobile)
- [Microsoft Learn: Troubleshooting Power-Apps-App (Safari-„Pin to Home“ ab iOS 14 nicht mehr)](https://learn.microsoft.com/en-us/power-apps/mobile/powerapps-mobile-troubleshoot)
- [Microsoft Learn: Systemvoraussetzungen und Browser](https://learn.microsoft.com/en-us/power-apps/limits-and-config)
- [Microsoft Learn: App im Browser ausführen](https://learn.microsoft.com/en-us/powerapps/run-app-browser)
- [Microsoft Learn: Mobile Deep-Links (Umgebungs-ID Pflicht)](https://learn.microsoft.com/power-apps/mobile/mobile-deep-links)
- [Microsoft Learn: Wrap – Übersicht](https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/overview), [Wrap – FAQ](https://learn.microsoft.com/power-apps/maker/common/wrap/faq)
- [Microsoft Learn: Canvas-App in Teams einbetten](https://learn.microsoft.com/en-us/power-apps/teams/embed-teams-app)
- [Microsoft Learn: Intune und Conditional Access (gerätebasiert)](https://learn.microsoft.com/en-us/intune/device-security/conditional-access-integration/device-based-policies)
- Community: [Add to Home Screen entfernt? (Siri-Weg, Symbol)](https://community.powerplatform.com/forums/thread/details/?threadid=83110c2d-9b68-43a6-8487-e7fb1e3dc544), [Power Apps im iPhone-Browser öffnet nicht](https://powerusers.microsoft.com/t5/Building-Power-Apps/PowerApps-web-not-opening-in-iPhone/m-p/1447888), [Power Apps in Teams mobile](https://powerusers.microsoft.com/t5/Building-Power-Apps/Embed-and-Open-Powerapps-from-Microsoft-teams-mobile-client/m-p/512107/highlight/true), [Power Apps: Mobile usage (Pin to Home, Android)](https://manueltgomes.com/microsoft/powerapps/power-apps-mobile-usage/)
