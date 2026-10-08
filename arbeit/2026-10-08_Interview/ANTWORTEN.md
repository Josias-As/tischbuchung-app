# Interview mit Josias (08.10.2026): Antworten

## Runde 1: Rahmen
| Frage | Antwort (Josias) |
|---|---|
| Welche GoBright-Funktionen werden genutzt? | Die meisten buchen nur Tische. Räume buchen die meisten selbst über Outlook. Am Tisch sind **kleine Anzeigen eingebaut** (frei / besetzt / orange = nicht eingecheckt). Sie laufen über ein **Gateway im Büro** und sollen mit der neuen App **ausgeschaltet** werden, weil es noch keinen Weg zur Anbindung gibt. „Wenn du einen Weg findest, das umzusetzen, wäre das top.“ |
| Betriebsrat / Datenschutz | Weiß ich nicht |
| Was geht am 14.10. live? | **Harter Umstieg** (GoBright wird abgeschaltet) |
| Zeit zum Einfügen und Testen | 3–4 Tage |

## Runde 2: Anzeigen, Vertrag, Check-in, Regeln
| Frage | Antwort (Josias) |
|---|---|
| Tisch-Anzeigen / Gateway: welches Modell? | Weiß ich nicht |
| Warum harter Umstieg? | **GoBright-Vertrag endet am 14.10.** Danach ist kein Parallelbetrieb möglich |
| Check-in | **Automatische Freigabe** (nicht eingecheckte Tische werden nach Beginn frei, per Flow) |
| Regeln E1–E7 wie in der Handy-App? | „Wie du es für sinnvoll hältst.“ → Claude übernimmt die Vorschläge aus Paket K v2 Abschnitt 2 (E1–E7) |

## Runde 3: Freigabe und Betrieb
| Frage | Antwort (Josias) |
|---|---|
| Freigabe nach wie vielen Minuten ohne Check-in? | **30 Minuten** nach Beginn |
| Was passiert mit der Buchung? | **Nur löschen** (keine Mail) |
| Wer besitzt den Freigabe-Flow? | **Josias** (läuft unter seinem Konto) |
| Handy-App zum Go-Live? | „Es sind nur ein paar Kollegen mit Firmenhandy, die das nutzen würden.“ (Zeitpunkt noch offen, Nachfrage in Runde 4) |

## Runde 4: Handy-App, Raumcode, Namen, Rechte
| Frage | Antwort (Josias) |
|---|---|
| Handy-App für die Kollegen mit Firmenhandy ab 14.10.? | „Wie wir es für sinnvoll halten“ → Entscheidung Claude (siehe Auswertung) |
| Toten Raumcode löschen? | **Nein, behalten** |
| Namen im Grundriss sichtbar? | **Ja, wie bisher** (Initialen und Name im Popup) |
| Wer darf fremde Buchungen in SharePoint ändern? | **Nur eigene** (Listeneinstellung „nur eigene Elemente bearbeiten“) |

## Runde 5: Testen, Rückmeldung, Reihenfolge, Vertretung
| Frage | Antwort (Josias) |
|---|---|
| Test mit echten Kollegen vor dem 14.10.? | **Ja, 3–5 Kollegen** |
| Neuer Export nach Paket K? | **Ja, Export und Monitor-Trace** |
| Was nach dem Go-Live? | „Ich möchte nicht in vor oder nach Go-Live denken. Ich möchte versuchen, **alles nach Wichtigkeit abzuarbeiten**, und das so gut es geht vor dem Go-Live. **Nicht sparen.**“ |
| Vertretung, wenn Josias ausfällt | **Michael/IT** |

## Runde 6: Zeiten, Rechte, Zuständigkeiten
| Frage | Antwort (Josias) |
|---|---|
| Buchungszeiten | Früher anfangen: **frühester Start 06:00**. Spätestes Ende 22:00 bleibt |
| Serien am Wochenende? | **Nein, Mo–Fr reicht** |
| Darf Josias SharePoint-Spalten und neue Steuerelemente anlegen? | **Ja, beides** |
| Wer darf Tische sperren? | **Nur Josias** |
| Big Table | **Alle dürfen buchen, über den Grundriss** (wie heute; in der Panel-Liste nicht) |

## Auswertung: Was daraus folgt (Claude, 08.10.)
1. **Harter Umstieg am 14.10. (Vertragsende):** Ein Parallelbetrieb oder Rückfall auf GoBright ist **nicht möglich**. Deshalb muss die App am 14.10. stabil sein. **Alle Muss-Teile, ein Test mit 3–5 Kollegen vorher und ein eigener Rückfallplan** sind Pflicht (Rückfall = Studio-Versionsverlauf, plus notfalls Buchung per SharePoint-Liste von Hand).
2. **Tisch-Anzeigen am Tisch:** Mit dem Vertragsende verlieren sie wahrscheinlich ihre Datenquelle (GoBright-Cloud über das Gateway). Eine Anbindung an die eigene App wäre nur möglich, wenn die Geräte oder das Gateway eine offene Schnittstelle haben (UNSICHER, wird recherchiert). **Aufgabe Josias:** Typenschild von einer Tisch-Anzeige und vom Gateway fotografieren (Hersteller, Modell).
3. **Automatische Freigabe:** Power-Automate-Flow unter Josias’ Konto, alle 5 Minuten. Er löscht Buchungen von heute, die seit **30 Minuten** begonnen haben und nicht eingecheckt sind, **ohne Mail**. Spalte intern `Checkedin`, Zeiten in UTC. Folge für die App: Check-in wird wichtig. Hinweis in der App „Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben“.
4. **Regeln (E1–E7):** Claude übernimmt die Vorschläge aus Paket K v2 (Regeln der Handy-App).
5. **Frühester Start 06:00 statt 08:00:** betrifft die Startlisten (L1), den Startvorschlag an anderen Tagen, die Knöpfe 5/9 Std (K v2 C3/C4) und die Handy-App (`ddStart.Items`: `8 * 60`). Vorschlag: Die Liste beginnt um 06:00, der **Vorschlag** an anderen Tagen bleibt 08:00. Heute vor 06:00 beginnt die Liste ebenfalls bei 06:00.
6. **Handy-App (Entscheidung Claude):** Zum Go-Live **mit den wenigen Firmenhandy-Kollegen teilen**. Begründung: Ihre GoBright-App fällt am 14.10. ebenfalls weg, die Handy-App ist getestet (Testprotokoll), und sie kann einchecken, was mit der automatischen Freigabe wichtig wird. Vorher die Regel 06:00 angleichen und kurz gegen Paket K prüfen (gleiche Regeln).
7. **Raumcode bleibt:** Er wird nicht gelöscht. Optional kann er aber **aufhören, beim Start abzufragen** (36 Abfragen), ohne gelöscht zu werden (nur ausgeblendete Abfragen hinter `If(varZeigeRaumBuchungForm; …)`).
8. **Namen bleiben sichtbar.** Datenschutz/Betriebsrat ist trotzdem bei Michael anzufragen (eine Mail).
9. **Rechte:** Listeneinstellung „nur eigene Elemente bearbeiten“ auf `Tischbuchungen`. Prüfen, dass Freigabe-Flow und Aufräum-Flow (beide unter Josias) weiter löschen dürfen.
10. **Reihenfolge:** Alles nach Wichtigkeit, so viel wie möglich vor dem Go-Live, nicht sparen.
11. **Vertretung Michael/IT:** Es braucht ein **Betriebshandbuch für Michael** (Was tun bei Fehler X, wo liegt was, wie zurückrollen, Flows, Listen, Rechte). Michael sollte Mitbesitzer von App, Listen und Flows werden.
12. **Sperren nur durch Josias, Big Table über den Grundriss für alle:** P4 als Ja/Nein-Spalte „Gesperrt“ in `Tische`, gepflegt in SharePoint. Der Big Table wird **nicht** gesperrt.
