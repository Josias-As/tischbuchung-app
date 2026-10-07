# TESTDATEN.md — Angelegte Testbuchungen und ihr Löschnachweis

**Kurzfassung:** Jede Buchung, die ich zum Testen in der echten Liste `Tischbuchungen` anlege, steht hier mit ID, Tisch, Zeitraum und Zweck. Am Ende muss jede Zeile als gelöscht nachgewiesen sein (Abnahmekriterium A31). **Stand 16:38: zwei Testbuchungen offen (496, 497), beide am Sa 31.10.2026.** Testbuchungen lege ich nach Möglichkeit auf ein Wochenende mindestens drei Wochen in der Zukunft, damit niemand blockiert wird; Tests, die „jetzt" brauchen, halte ich kurz und lösche sofort.

**Bevorzugter Testzeitraum:** Samstag/Sonntag ab dem 31.10.2026 (mehr als drei Wochen nach heute, 06.10.2026). Bevorzugter Testtisch: ein Tisch, der an diesem Wochenende nachweislich leer ist; den Tisch wähle ich erst nach einer Abfrage, nicht vorab.

---

## Offene Testbuchungen

**Vorabprüfung 06.10.2026, 16:26 (REST-GET):** Zwischen Sa 31.10.2026 00:00 und So 01.11.2026 24:00 steht **keine einzige Buchung** in `Tischbuchungen`. Höchste ID in der Liste: **495**. Jede Zeile mit ID > 495 und Startzeit am 31.10./01.11. stammt also aus meinen Tests.

| Nr | ID | Tisch | Von | Bis | Zweck | angelegt | gelöscht | Nachweis |
|---|---|---|---|---|---|---|---|---|
| TB-1 | **496** | UG Desk 17 | Sa 31.10.2026 08:00 | 12:00 | A14/D6 Anlegen und Nachlese; Grundlage für D5-Test (A24) | 06.10. 16:27:32 über Handy-App (Vorschau) | | REST: Tisch {Id 30, UG Desk 17}, Person Josias, Start 07:00Z |
| TB-2 | **497** | UG Desk 15 | Sa 31.10.2026 14:00 | 15:00 (nach Tests 18:00) | D3 Doppeltipp (A22); danach Verlängern +1/+2 (A17), Stornieren (A19) | 06.10. 16:29 über Handy-App, Doppeltipp | | REST: genau eine Zeile; 16:31 Ende 17:00 (Fehler D3), 16:37 Ende 18:00 |
| TB-3 | *(geplant)* | UG Desk 14 | Sa 31.10.2026 20:30 | 21:30 | Verlängern über 22:00 muss abgelehnt werden (A17, V5) | | | |
| TB-4 | **498** | UG Desk 13 | Sa 31.10.2026 09:00 | 10:00 | D2 zweites Fenster (A21): Fenster B = **Desktop-App** (Wiedergabe, nicht Studio), danach in Fenster A (Handy) denselben Tisch | 06.10. ca. 16:55 über die **Desktop-App** („Buchung(en) erfolgreich gespeichert") | | REST 16:56: ID 498 UG Desk 13 09–10, Josias. **Gelöscht** 16:57 über die Desktop-App (Test T-22), REST 16:57:36: 498 nicht mehr vorhanden |
| — | **nicht anlegen** | UG Desk 16 | Sa 31.10.2026 10:00 | 14:00 | D5-Gegenprobe: muss abgelehnt werden, darf **nicht** entstehen | | | |

Tests, die „jetzt" brauchen (Einchecken, Jetzt beenden), plane ich getrennt und kurz, sobald die Wochenend-Tests durch sind.

---

## Abgeschlossene Testbuchungen

*(keine)*

---

## Nachlese am Ende

Steht aus. Geplant: Abfrage auf `Tischbuchungen` mit `Person.Email = User().Email` über den gesamten Testzeitraum, Abgleich gegen die Tabelle oben, Ergebnis mit Datum und Uhrzeit hier eintragen.

---

## Regeln, die ich mir selbst gebe

- Jede Testbuchung wird **vor** dem Anlegen hier eingetragen, nicht danach. Wenn der Schreibvorgang abbricht, steht die Zeile trotzdem schon da und geht nicht verloren.
- Fremde Einträge werden nie geändert oder gelöscht (L2).
- Keine Spalten, keine Listeneinstellungen anfassen (L2).
- Wenn ich eine Buchung nicht löschen kann, bleibt die Zeile offen stehen und wandert nach `FRAGEN_AN_JOSIAS.md`.
