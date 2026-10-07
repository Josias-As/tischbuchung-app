# KORREKTUR.md — vorrangig vor KONTEXT.md lesen

> **Diese Datei sticht `KONTEXT.md`, wo sie sich widersprechen.**

**Stand: 30.09.2026, abends**

„Arbeitsordner" heißt im Folgenden immer der Ordner, in dem diese Datei liegt.

---

## 1. Welche App die richtige ist

In der Umgebung „Personal Productivity" liegen **drei** fast identische Canvas-Apps:

| Name | App-ID | Status |
|---|---|---|
| **Tischbuchung** | `d247d18b-d36f-4a44-975a-7839695b2f12` | **Das ist die richtige. Nur diese zählt.** |
| App | `fc32c6b0-5e8a-4650-a377-8d6e0e02d1b7` | falsche Fährte, ignorieren |
| App – Kopie | unbekannt | ignorieren |

Von Josias am 30.09. ausdrücklich bestätigt: **„die richtige ist tischbuchungen"**.

---

## 2. Abschnitt 2 von KONTEXT.md ist unzuverlässig

`KONTEXT.md` behauptet, Abschnitt 2 sei „direkt im Studio verifiziert". **Das stimmt nicht mehr** — verifiziert wurde in der App **„App"**, nicht in **„Tischbuchung"**.

Die beiden sahen strukturell gleich aus (ein Screen, gleiche Containerliste, gleicher Grundriss), aber **ob die Formeln identisch sind, ist unbekannt.**

**Deshalb gilt:** Alles in Abschnitt 2 von `KONTEXT.md` — Containerliste, Variablennamen, Inhalt von `App.OnStart`, die Liste des toten Codes — ist **Hypothese, nicht Befund.** Prüfe jede dieser Angaben gegen den echten Quellcode und **schreib ausdrücklich hin, wo der Quellcode abweicht.** Eine Abweichung ist ein Ergebnis, kein Fehler.

Was **weiterhin gilt**: Abschnitte 1, 3, 4, 5, 6, 7 und 8 von `KONTEXT.md` — Ziel, Datenmodell, die technischen Kernprobleme, die gemeldeten Bugs, die Power-Fx-Regeln, die Arbeitsweise. Die stammen aus der Projektdokumentation und dem fachlichen Kontext, nicht aus der falschen App.

---

## 3. Die Quelldatei

Statt einer `.msapp` liegt im Download-Ordner ein **Exportpaket**:

```
Tischbuchung_2026-09-30_Analyse.zip
```

Das ist ein ZIP. Darin liegt die `.msapp` der App „Tischbuchung" (üblicherweise unter `Microsoft.PowerApps/apps/<guid>/`). Die `.msapp` ist selbst wieder ein ZIP.

**Vorgehen:**
1. Suche im Download-Ordner nach `Tischbuchung_2026-09-30_Analyse*.zip`. Es kann sein, dass die Datei **zweimal** da ist (einmal automatisch, einmal manuell ausgelöst) — nimm die größte bzw. neueste, die anderen ignorierst du.
2. Kopiere sie in den Arbeitsordner. **Das Original im Download-Ordner lässt du liegen.**
3. Entpacke das Paket, finde darin die `.msapp`, entpacke die nach `./src`.
4. Sieh nach, was drin ist: ein `Src`-Ordner mit YAML wäre ideal; `Controls/*.json` geht auch, ist nur unangenehmer zu lesen.
5. **Sag ehrlich, ob du damit zuverlässig arbeiten kannst.** Wenn das Format unbrauchbar ist, schreib das in `STOPP.md` und hör auf, statt zu raten. Dann wird morgen `pac` installiert.

Eine Datei namens `Tischbuchung_2026-09-30_original.msapp` gibt es **nicht**. Das Exportpaket im Download-Ordner ist der Rückfallpunkt.

---

## 4. Wenn der Arbeitsordner in OneDrive oder einem Obsidian-Tresor liegt

Dann gilt zusätzlich:

- Lege den entpackten Quellcode (`./src`) und die ZIP-Dateien **nicht** dorthin, sondern in einen lokalen Ordner außerhalb der Synchronisierung, zum Beispiel `C:\tischbuchung_work\`. Ein entpacktes `.msapp` besteht aus vielen hundert Dateien; die in einem synchronisierten Ordner zu erzeugen, führt zu Sync-Konflikten und blockierten Dateien.
- **Nur die fertigen Markdown-Ergebnisse** (`INVENTAR.md`, `ENTWURF_MEHRFACHAUSWAHL.md`, `VERWORFEN.md`, ggf. `STOPP.md`) legst du am Ende in den Arbeitsordner.
- Pfade mit Leerzeichen und Sonderzeichen in Anführungszeichen setzen.

---

## 5. Reihenfolge der Arbeit

1. Quellcode entpacken nach `./src` (lokaler Arbeitsbereich, siehe Punkt 4)
2. `INVENTAR.md` nach `AUFGABE_INVENTAR.md`
3. `ENTWURF_MEHRFACHAUSWAHL.md` und `VERWORFEN.md` nach `AUFGABE_SCHLEIFE.md`

`AUFGABE_UMBAU.md` ist **nicht** Teil dieses Laufs. Die Datei liegt im Ordner, wird aber erst später bearbeitet.

---

## 6. Was du nicht tust

- Die App nicht öffnen, nicht bearbeiten, nichts zurückpacken. Der ausgepackte Quellcode ist ein Röntgenbild, kein Bearbeitungsformat.
- Nichts im Download-Ordner löschen oder verschieben.
- Die Apps „App" und „App – Kopie" nicht anfassen und nicht analysieren.
- Keine bestehenden Dateien im Arbeitsordner verändern oder löschen — dort liegen möglicherweise Notizen von Josias.
- Bei Unsicherheit nicht raten, sondern `UNSICHER` schreiben.
