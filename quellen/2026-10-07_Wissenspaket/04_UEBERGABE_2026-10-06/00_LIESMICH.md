# 00 — Liesmich

**Kurzfassung in fünf Sätzen:** Dieses Paket enthält die Power-Apps-Canvas-App „Tischbuchung" vollständig dokumentiert: jedes der 186 Steuerelemente mit allen 1985 gesetzten Properties im Originalwortlaut, jeden der 95 Knöpfe mit Verhaltensformel einmal durchgegangen, alle Variablen, alle Datenquellen und ein Konzept für die geplante Vorprüfung mit Alternativtischen. Alle Formeln wurden **per Skript** aus dem Quellcode gezogen, nichts ist abgetippt; `VERIFIKATION.md` belegt mit Zahlen, dass nichts fehlt. Grundlage ist der Export vom 06.10.2026 (Appstand 05.10.2026). Die App wurde nicht geöffnet, nicht bearbeitet und nicht zurückgepackt. Was ich nicht belegen konnte, steht als `UNSICHER` oder **VERMUTUNG** da.

---

## Herkunft

| | |
|---|---|
| Exportpaket | `TischbuchungApp06.10.2026_20261006112813.zip` |
| Paket erstellt | 06.10.2026, 11:28:12 UTC, von `Josias.Assefaw@technoform.com` |
| Umgebung | Personal Productivity |
| **Appstand im Paket** | **05.10.2026, 11:58 UTC** (`appVersion` 2026-10-05T11:58:19Z) |
| App-Name | Tischbuchung |
| SHA-256 des `.msapp` | `1541C0D319B187A4486F1CE5C8330C3BC599DC52BA0B768176FBE6ED7AE612A7` |

**Zur App-ID (UNSICHER):** Die erwartete ID `d247d18b-d36f-4a44-975a-7839695b2f12` kommt **in keiner Datei des Exports vor** — ein Exportpaket enthält die Portal-App-ID offenbar nicht. Dass es die richtige App und nicht einer der Klone („App", „App – Kopie") ist, stützt sich auf: Anzeigename „Tischbuchung", Ersteller und Umgebung, den Exportzeitpunkt, die inhaltliche Übereinstimmung mit `INVENTAR.md` und darauf, dass die drei seit dem 30.09. erwarteten Änderungen genau an den erwarteten Stellen stehen. Details in `VERIFIKATION.md`, Abschnitt 5.

**Ein erster Export desselben Tages war unbrauchbar:** `TischbuchungApp06.10.2026_20261006110339.zip` (11:03 UTC) enthielt ein `.msapp`, das Byte für Byte mit dem Export vom 30.09. identisch war — der Paket-Export liefert nur die zuletzt **veröffentlichte** Version. Der hier verwendete zweite Export enthält den aktuellen Stand.

---

## Was in diesem Ordner liegt

### Die Dokumentation

| Datei | Inhalt |
|---|---|
| `00_LIESMICH.md` | diese Datei |
| `01_APP_KOMPLETT.md` | **das Herzstück.** Jedes Steuerelement im Baum mit jeder gesetzten Property, wortgetreu. Dazu `App.OnStart`, `App.Formulas`, Screen-Properties und die App-Einstellungen aus den Metadaten. |
| `02_BUTTONS.md` | jeder der 95 Knöpfe mit Verhaltensformel einmal durchgegangen: Klartext, Formeln, Zustands-Properties, Variablen, Datenquellen, Netzwerkschätzung, Befunde. Gruppiert nach Bereich. |
| `03_VARIABLEN.md` | 50 globale Variablen, 5 Collections, 20 Named Formulas; wo geschrieben, wo gelesen, was tot ist. |
| `04_DATENQUELLEN.md` | vier SharePoint-Listen mit Spalten und internen Namen, dann alle 117 Lese- und Schreiboperationen mit Delegierbarkeits-Einschätzung. |
| `05_STAND_DER_AENDERUNGEN.md` | was sich seit dem 30.09. geändert hat (genau drei Properties) und was von K1–K5 und A.1–A.4 **nicht** eingebaut ist. |
| `06_KONZEPT_MEHRFACHBUCHUNG.md` | das Konzept der Vorprüfung mit Alternativtischen, mit den technischen Ankern im vorhandenen Code. Keine fertigen Formeln. |
| `07_OFFENE_FRAGEN.md` | 24 nummerierte Fragen: 11 fachliche Entscheidungen für Josias, 13 technisch ungeklärte Punkte. |
| `VERIFIKATION.md` | die Zahlen, die belegen, dass nichts fehlt. |

### Die Quellen

| Ordner | Inhalt |
|---|---|
| `paket/` | das Exportpaket, wie heruntergeladen, plus `paket/entpackt/` mit dem Inhalt |
| `src/` | der entpackte Quellcode aus dem `.msapp`. Die Formeln stehen in `src/Src/App.pa.yaml` und `src/Src/Screen1.pa.yaml`. |
| `skripte/` | die Skripte, die die Dokumente erzeugt haben, und ihre Zwischendateien |

### Unverändert mit übernommen

`BRIEFING_Mehrfachspeichern.md`, `INVENTAR.md`, `ENTWURF_MEHRFACHAUSWAHL.md`, `VERWORFEN.md`, `ENTWURF_SPEICHERN.md`, `VERWORFEN_SPEICHERN.md`, `ENTWUERFE_ROHFASSUNG.md`, `ARBEITSSTAND_SPEICHERN.md`, `KONTEXT.md`, `KORREKTUR.md`, dazu `KORREKTUR_1.md`, `OFFENE_FUNDE.md`, `AUFGABE_UEBERGABE.md` und `GOAL_Uebergabe.txt`.

**Es fehlt keine der angeforderten Dateien.** `BRIEFING_Mehrfachspeichern.md`, `AUFGABE_UEBERGABE.md` und `GOAL_Uebergabe.txt` lagen nicht in `C:\tischbuchung_work\`, sondern im Download-Ordner; sie sind dort wortgleich mit den Fassungen im Obsidian-Ordner (per Prüfsumme verglichen). Alles andere stammt aus `C:\tischbuchung_work\`.

---

## Wie man das benutzt

- **Du suchst eine bestimmte Formel?** `01_APP_KOMPLETT.md`, nach dem Steuerelementnamen suchen. Die Baumübersicht am Anfang zeigt, wo das Element sitzt.
- **Du willst verstehen, was ein Knopf tut?** `02_BUTTONS.md`. Dort steht neben der Formel auch, was sie bewirkt und was daran kaputt ist.
- **Du willst wissen, woher eine Variable kommt?** `03_VARIABLEN.md`.
- **Du willst eine Abfrage ändern?** `04_DATENQUELLEN.md` nennt Spaltennamen und sagt, ob der Filter delegierbar bleibt.
- **Du fängst mit der Mehrfachbuchung an?** `06`, dann `07`, dann `BRIEFING_Mehrfachspeichern.md` für die Vorgeschichte.

### Eine Sache, die beim Lesen auffällt

Die Formeln stehen hier in der **englischen Schreibweise des Quellcodes**: `,` trennt Argumente, `.` ist Dezimaltrenner, Anweisungen sind mit `;` verkettet, und jede Formel beginnt mit `=`. Power Apps Studio zeigt dieselben Formeln in deutscher Schreibweise: `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet. Das ist nur die Anzeige, nicht der Inhalt. **Wer eine Formel aus diesem Paket in Studio einfügt, muss sie umschreiben.**

---

## Was belegt ist und was nicht

**BELEGT** heißt: steht so im Quellcode, mit Zeilenangabe. Dazu zählen alle Formeln, alle Zahlen in `VERIFIKATION.md`, der Änderungsvergleich in `05` und alle Spaltennamen in `04`.

**VERMUTUNG** heißt: folgt aus dem Code, ist aber nicht geprüft. Das betrifft vor allem Laufzeitverhalten — ob eine Fehlermeldung wirklich erscheint, ob ein `OnCheck` bei einer Default-Änderung feuert, wie Power Apps eine Abfrage zerlegt.

**Nicht geprüft werden konnte überhaupt:** alles, was eine Messung braucht. Die App wurde nicht gestartet. Wie viele Netzwerkaufrufe eine Serienbuchung erzeugt, ob der Sammel-`Patch` schneller ist und ob er `Person` und `Tisch` korrekt schreibt, steht nicht im Quellcode. Das entscheidet nur der Power-Apps-Monitor (`07_OFFENE_FRAGEN.md`, Nummern 12 bis 14). Alle Netzwerkzahlen in `02_BUTTONS.md` sind ausdrücklich als Schätzung gekennzeichnet.

---

## Die drei wichtigsten Befunde

1. **Befund B0 besteht fort.** Im Verwalten-Dialog des Buchungen-Tabs speichern die Knöpfe `varSelectedBuchungTab`, aber alle zwölf Plus-/Minus-Properties lesen `varSelectedBuchung`, also die zuletzt im Grundriss angeklickte Buchung. Ein Knopf kann grün sein, obwohl die Verlängerung kollidiert: der einzige belegte Weg zu einer stillen Doppelbuchung. K1 aus `ENTWURF_SPEICHERN.md` würde das mit einer Zeile beheben und ist nicht eingebaut.
2. **Die beiden Speichern-Wege sind nicht mehr gleich.** `btnSpeichern` hat den Sammel-`Patch` mit `IfError`, `btnSpeichernTischePanel` schreibt weiter je Termin einzeln ohne Fehlerbehandlung. Jede künftige Änderung muss in beide Knöpfe separat (Ü8).
3. **Kein Knopf der App hat eine Doppelklick-Sperre.** K5 ist nirgends eingebaut; keiner der vier Speichern- und Verlängern-Knöpfe hat eine `DisplayMode`-Property.
