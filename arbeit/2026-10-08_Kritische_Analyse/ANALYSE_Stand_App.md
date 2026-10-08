# Kritische Analyse: Tischbuchungs-App, Stand 08.10.2026

Grundlage: veröffentlichter Export vom 07.10. (vollständig gelesen, 1.994 Properties), App-Prüfung (`AppCheckerResult.sarif`), Monitor-Auswertungen (Trace 3–5), Handy-App-Export und Testprotokoll, alle Übergaben. **Nicht** Grundlage: die laufende App (ich kann sie nicht starten), die Nutzung von GoBright bei Technoform (die kenne ich nicht) und die Berechtigungen der SharePoint-Liste (habe ich nicht gesehen). Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **Einschätzung** (meine Meinung).

## 1. Urteil in fünf Sätzen
1. **Die App läuft** (gemessen: Serie ~4,7 s, 33 Stornierungen ~9 s ohne Fehler, App-Prüfung ohne Formelfehler), aber der **veröffentlichte Stand hat mindestens acht echte Fehler**, die Nutzer in der ersten Woche treffen werden, darunter eine stille Doppelbuchung und Doppelbuchung per Doppelklick.
2. Die Korrekturen dafür liegen als Paket K v2 bereit, sind aber **nicht eingefügt und nicht getestet**. 55 Properties in sechs Tagen einzufügen und sauber zu testen ist machbar, aber knapp für einen Werkstudenten mit anderen Aufgaben.
3. **Go-Live am 14.10. mit 30 Nutzern halte ich für realistisch nur als „Pilot“**, also mit GoBright parallel im Hintergrund, einem klaren Ansprechpartner und der Erwartung, dass in Woche 1 nachgebessert wird. Als „harter Umstieg, GoBright abgeschaltet“ halte ich es für riskant.
4. Gegenüber GoBright ist es **funktional ein spürbares Downgrade** (keine automatische Freigabe nicht genutzter Tische, kein Outlook/Teams, keine Raumbuchung, keine Auswertung, keine fertige Handy-App mit QR/NFC-Check-in, kein Admin-Bereich). Für reine „Ich buche mir einen Tisch“-Nutzer ist es **kein Downgrade, teils sogar besser** (Grundriss klar, schnell nach L2, eigene Regeln).
5. Das größte Risiko ist **nicht der Code, sondern der Betrieb**: eine Person (Werkstudent) als einziger Entwickler, keine Test-Umgebung, App in der persönlichen Standardumgebung, keine Dokumentation für Nachfolger in der Organisation, keine geklärte Mitbestimmung/Datenschutz. Wenn du gehst, steht die App.

## 2. Läuft die App? Was Nutzer heute (ohne Paket K) erleben werden
Alles **belegt** am Export, Häufigkeit = **Einschätzung**.

| # | Fehler im veröffentlichten Stand | Wie ein Nutzer ihn erlebt | Häufigkeit Woche 1 |
|---|---|---|---|
| 1 | **Doppelklick bucht/verlängert doppelt** (keine wirksame Sperre; in der Handy-App gemessen) | „Ich hab einmal geklickt und jetzt hab ich zwei Buchungen / 2 Std statt 1“ | **hoch** – Leute doppelklicken, vor allem wenn die App 2–4 s braucht |
| 2 | **B0: Plus-Knöpfe im Tab „Buchungen“ bewerten die falsche Buchung** → stille Überschneidung mit dem nächsten Kollegen | Zwei Leute haben denselben Tisch zur selben Zeit, keiner hat eine Warnung gesehen | mittel |
| 3 | **Verlängern prüft nicht beim Speichern**, nur beim Einfärben | wie 2, wenn jemand zwischen Öffnen und Klicken bucht | gering |
| 4 | **Verlängern über 22:00 / in den nächsten Tag möglich** | Buchung bis 01:00, blockiert den Morgen nicht, aber sieht kaputt aus | gering |
| 5 | **Stornieren im Dashboard auf veralteten Datensatz** (`Remove(…; varSelectedBuchung)`) → „Item Not Found“ (euer gemeldeter Bug 30.09.) | **englische rohe Fehlermeldung** | mittel |
| 6 | **Eine Person kann zur selben Zeit mehrere Tische buchen** | Tische „gehortet“, andere finden nichts | mittel, sobald es jemand merkt |
| 7 | **Buchen in der Vergangenheit, Einchecken für übermorgen** möglich | verwirrend, Statistik (falls je gemacht) wertlos | gering |
| 8 | **Tischauswahl im Panel zeigt alle 34 Tische**, auch belegte und Big Table, unsortiert; Belegung erfährt man erst über graue Knöpfe/Meldung | „Warum kann ich OG Desk 5 auswählen, wenn er belegt ist?“ – **häufigste Beschwerde, die ich erwarte** | **hoch** |
| 9 | **Meldungen lügen teils**: „Buchung(en) erfolgreich gespeichert“ zählt lokal, nicht was ankam; „Wiederholung auf 2 Wochen begrenzt“ verdrängt die Kollisionsmeldung | Nutzer glaubt 10 Termine, hat 7 | mittel bei Serien |
| 10 | **Buchungen-Tab „manchmal leer“** (euer Bug 30.09., ungeklärt) | „Meine Buchungen sind weg!“ → Panik, Doppelbuchung aus Angst | unbekannt – **gefährlichster, weil Ursache unbekannt** |

**Fazit Abschnitt 2:** Mit dem veröffentlichten Stand würde ich **nicht** live gehen. Mit Paket K v2 (eingefügt und getestet) sind 1–9 behoben (geschlussfolgert), 10 bleibt offen.

## 3. Wie kritische Nutzer auf die App blicken werden (Einschätzung)
Stell dir drei Typen vor:

**Der GoBright-Gewohnte** („früher war alles besser“):
- „Wo ist das in Outlook/Teams?“ – Die App hat **keine Kalender-Integration**. Wer seinen Tisch nicht im Kalender sieht, vergisst ihn.
- „Warum wird mein Tisch nicht freigegeben, wenn der Kollege nicht kommt?“ – **Einchecken hat keine Folge.** Es gibt keine automatische Freigabe (der Aufräum-Flow löscht nur Buchungen älter als 7 Tage, belegt). Damit ist Check-in eine reine Fleißaufgabe, und das merken Leute nach drei Tagen. GoBright gibt nicht eingecheckte Tische automatisch frei ([GoBright Desk Booking](https://gobright.com/work)).
- „Auf dem Handy geht das nicht.“ – Die Desktop-App ist fest 1366 × 768, am Handy unbedienbar. Die Handy-App ist **mit niemandem geteilt** (belegt). Kommt sie nicht zum Go-Live, ist das der größte Rückschritt gegenüber der GoBright-App mit NFC/QR-Check-in ([App Store](https://apps.apple.com/app/id1205856002)).
- „Wo buche ich Besprechungsräume?“ – Raumbuchung ist toter Code (ausgeblendet). Wenn GoBright bei euch auch Räume gemacht hat, ist das ein **echter Verlust** (UNSICHER, kenne eure GoBright-Nutzung nicht).

**Der Ungeduldige:**
- Start ~3–4 s (gemessen), Speichern 2–5 s mit Overlay. **Okay**, nicht toll. Nach L2 kein Grund zur Klage mehr.
- Fixes Tablet-Layout auf einem großen Monitor: viel Rand oder Skalierung. Wirkt „selbstgebaut“.
- Deutsch/Englisch gemischt (belegt): „My personal desk“, „My meetings“, „Dashboard“, Knöpfe „x“ und „<“, „-2std“ klein geschrieben, „+1Std“ ohne Leerzeichen. Kleinigkeiten, aber kritische Nutzer **bewerten Qualität an Kleinigkeiten**.
- Eingecheckt ist im Grundriss **rot**, auf dem Dashboard **grün** (belegt, BD-14). Wird mindestens eine Rückfrage geben.

**Der Datenschutz-/Betriebsrat-Mensch:**
- Jeder sieht im Grundriss **Initialen** und im Details-Popup **den vollen Namen** samt Zeit und Check-in-Status jedes Kollegen (belegt). Das ist eine Anwesenheitsübersicht.
- In Deutschland ist ein System, das Anwesenheit/Verhalten von Mitarbeitenden erfasst und auswertbar macht, regelmäßig **mitbestimmungspflichtig** (§ 87 Abs. 1 Nr. 6 BetrVG). GoBright ist vermutlich mit Betriebsrat und Datenschutz abgestimmt worden; **deine App ist ein neues System** und braucht das wahrscheinlich auch (geschlussfolgert, keine Rechtsberatung). Das kann einen Go-Live **mehr verzögern als jeder Bug**. Frag Michael/Datenschutz **heute**.

## 4. Was außerhalb deiner Fragen kritisch ist (Einschätzung, teils belegt)
1. **Bus-Faktor 1.** Ein Werkstudent baut und betreibt die App. Es gibt keine zweite Person, die Power Fx und diese App kennt. Bei Krankheit, Urlaub oder Vertragsende gibt es niemanden für Fehler. Bei GoBright hattet ihr Support. **Das ist das stärkste Gegenargument gegen die Einsparung.**
2. **Keine Trennung von Entwicklung, Test und Betrieb.** Die App liegt in der **Standardumgebung „Personal Productivity“** (belegt). Es gibt keine Lösung (Solution), keine Test-Umgebung, keine Versionskontrolle außer dem Studio-Versionsverlauf. Getestet wird an der echten Liste mit echten Buchungen (Handy-Testprotokoll belegt das, IDs 495–498). Jede Änderung nach Go-Live ist eine Änderung am offenen Herzen. Dazu gibt es zwei Klone („App“, „App – Kopie“), die schon einmal verwechselt wurden (belegt).
3. **Die Regeln sind umgehbar.** Damit die App schreiben kann, brauchen alle Nutzer Schreibrechte auf die SharePoint-Liste (geschlussfolgert, Berechtigungen nicht gesehen). Jeder kann also die Liste im Browser öffnen und Buchungen anderer **ändern oder löschen**, an jeder Regel vorbei. Für interne Tischbuchung ist das vielleicht vertretbar, aber du solltest es **wissen und entscheiden**, nicht entdecken.
4. **Kein Doppelbuchungsschutz auf Datenebene.** SharePoint kennt keine Transaktion. Zwei Leute, die in derselben Sekunde denselben Tisch buchen, bekommen ihn beide. Paket K **erkennt** das hinterher, **verhindert** es nicht. Bei 30 Nutzern selten, aber Montag 8 Uhr ist genau der Fall.
5. **Code-Qualität** (belegt): eine Screen mit 189 Steuerelementen und absoluten Koordinaten, Tischpositionen fest in `OnStart` einprogrammiert, toter Raumcode (21 Steuerelemente, 36 Abfragen beim Start), 10 tote Variablen, dieselbe Logik 2–4× kopiert (zwei Speichern-, zwei Verlängern-, zwei Storno-Knöpfe). 134 Einträge in der App-Prüfung, davon 64 Barrierefreiheit (fehlende Beschriftungen, Tab-Reihenfolge). Für einen Prototyp normal, **für ein Produkt, das 10.000 €/Jahr ersetzt, wartungsintensiv**.
6. **Kein Admin-Bereich.** Es gibt keine Möglichkeit, einen Tisch zu sperren (Reparatur, Umzug), keine Übersicht „wer ist heute da“ für Empfang oder Brandschutz, keine Auswertung „wie voll ist das Büro“. Genau diese Auswertung ist bei GoBright oft der eigentliche Grund für die Lizenz (Flächenplanung).
7. **Der Grundriss ist starr.** Neue Tische oder ein Umzug heißen: Formel ändern, Koordinaten von Hand einmessen. Die Liste `Tische` hat Spalten `X`/`Y`, die App nutzt sie nicht (belegt).
8. **Die Handy-App duplizert Regeln.** Es gibt jetzt zwei Codebasen mit eigenen Regeln. Paket K gleicht sie an, aber jede künftige Regeländerung muss in zwei Apps passieren.
9. **Positiv** (damit es fair ist): Die Grundidee ist gut und günstig. Der Grundriss ist anschaulich, die Performance-Arbeit (L2) war hervorragend, die Arbeitsweise mit Export, Messung, Übergabe und Prüfung ist professioneller als in vielen IT-Abteilungen. Die Handy-App ist sauberer gebaut als die Desktop-App. **Du bist nicht schlecht, das Projekt ist für eine Person zu groß.**

## 5. GoBright (10.000 €/Jahr) gegen eigene App
| | GoBright | deine App |
|---|---|---|
| Kosten | ~10.000 €/Jahr (deine Angabe) | Lizenz 0 € (M365, Standard-Konnektor). **Aber** deine Arbeitszeit, künftige Wartung, Ausfallrisiko |
| Tisch buchen, Grundriss | ja | ja, gut |
| Automatische Freigabe ohne Check-in | ja ([Quelle](https://gobright.com/work)) | **nein** |
| Outlook/Teams/Exchange | ja ([Quelle](https://gobright.com/?p=1358)) | **nein** |
| Handy-App, NFC/QR-Check-in | ja | Handy-App nicht geteilt, kein QR |
| Raumbuchung | ja | **nein** (toter Code) |
| Auswertungen/Auslastung | ja ([Quelle](https://xchange.avixa.org/posts/gobright-smart-workplace-solutionas)) | **nein** |
| Admin, Tische sperren | ja | **nein** |
| Support, Updates, Sicherheit | Hersteller | **du** |
| Eigene Regeln, schnell anpassbar | begrenzt | **ja** |

**Mein Urteil:** Für die **Kernfunktion „Tisch buchen“** ist es kein spürbares Downgrade, sobald Paket K drin ist. **Als Gesamtsystem ist es ein deutliches Downgrade**, wenn ihr GoBright für mehr als Tische genutzt habt (Räume, Outlook, Auslastung, automatische Freigabe, Displays/Sensoren). Ob sich die 10.000 € lohnen, hängt an **einer** Frage, die ich nicht beantworten kann: **Welche GoBright-Funktionen nutzt Technoform wirklich?** Wenn es nur „Tisch buchen und schauen, wer wo sitzt“ ist, ist die Einsparung gerechtfertigt, **sofern** jemand die App dauerhaft betreut. Rechne ehrlich: Schon 10 Stunden Wartung pro Monat durch eine interne Person sind über ein Jahr ein erheblicher Teil der Lizenz (Einschätzung).

## 6. Realistisch: Go-Live 14.10. mit 30 Nutzern? (Einschätzung)
| Szenario | Wahrscheinlichkeit, dass Woche 1 ohne ernsthaften Ärger läuft |
|---|---|
| Veröffentlichter Stand ohne Paket K | **gering (~30 %)**: Doppelklick, Tischauswahl, rohe Fehlermeldungen |
| Paket K v2 eingefügt **und** mit Testbogen getestet | **mittel bis gut (~65–75 %)** |
| wie oben, **plus** Handy-App geteilt, Pilot mit GoBright parallel, Ansprechpartner benannt | **gut (~80 %)** |

**Technisch** ist der Termin haltbar. **Organisatorisch** ist er wackelig, weil Mitbestimmung/Datenschutz, Berechtigungen und Kommunikation an die Nutzer vermutlich noch offen sind (UNSICHER, ich weiß es nicht).

## 7. Was ich an deiner Stelle diese Woche tun würde (Reihenfolge)
1. **Heute:** Michael/Datenschutz/Betriebsrat fragen: Dürfen Namen und Check-in für alle sichtbar sein? Braucht es eine Abstimmung? **Das ist der einzige Punkt, der den Termin wirklich kippen kann.**
2. **Heute:** GoBright **nicht kündigen bzw. nicht abschalten**, sondern 4 Wochen parallel laufen lassen. Klären, welche GoBright-Funktionen genutzt werden (Räume? Outlook? Auswertung?).
3. **Mi–Fr:** Paket K v2 einfügen, Teil für Teil, mit Testbogen. Wenn die Zeit knapp wird: zuerst **A (Verwalten), B (Speichern), C1 (Tischauswahl)**. D ist kosmetisch.
4. **Fr:** 3–5 Kollegen als Testgruppe einen halben Tag buchen lassen, **bevor** alle 30 kommen. Ein Doppelklick-Test und ein Zwei-Browser-Test mit einem Kollegen.
5. **Bis Go-Live:** Englische Texte ins Deutsche, eine Seite Kurzanleitung, ein Kanal für Fehler (Teams-Chat), Rückfallplan: „Wenn X, dann GoBright“.
6. **Nach Go-Live:** Handy-App teilen; automatische Freigabe nicht eingecheckter Tische entscheiden (sonst Check-in abschaffen); Admin-Funktion „Tisch sperren“; eine zweite Person einarbeiten; App in eine eigene Umgebung/Lösung umziehen.

## 8. Was ich nicht weiß (und was das Urteil ändern würde)
- Welche GoBright-Funktionen Technoform nutzt (Räume, Outlook, Sensoren, Displays, Auswertung).
- Ob Betriebsrat/Datenschutz schon eingebunden sind.
- Berechtigungen der SharePoint-Liste.
- Ob die Handy-App zum Go-Live gehört.
- Ob es nach deiner Werkstudentenzeit jemanden gibt, der die App übernimmt.
- Wie die App auf echten Geräten der Nutzer aussieht (Bildschirmgrößen, Browser, Teams-Einbettung).

Quellen zu GoBright (Herstellerangaben, abgerufen 08.10.2026): [GoBright Desk Booking](https://gobright.com/work), [GoBright × Microsoft Teams](https://gobright.com/?p=1358), [GoBright App (App Store)](https://apps.apple.com/app/id1205856002), [GoBright bei AVIXA](https://xchange.avixa.org/posts/gobright-smart-workplace-solutionas).
