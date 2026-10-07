# VERIFIKATION — Belegt die Vollständigkeit mit Zahlen

**Kurzfassung:** Alle Prüfungen stimmen. Die Zahl der Steuerelemente, die Zahl der gesetzten Properties und die Zahl der Steuerelemente mit Verhaltensformel sind im Quellcode und in den Dokumenten gleich, und 15 zufällig gezogene Formeln sind Zeichen für Zeichen identisch. Erzeugt von `skripte/verifiziere.js` am 2026-10-06. Die Zählung im Quellcode läuft unabhängig vom Extraktionsparser direkt über die YAML-Zeilen, damit ein Parserfehler nicht beide Seiten gleich falsch macht.

## 1. Die Zahlen

| Prüfung | Quellcode | Dokument | Ergebnis |
|---|---|---|---|
| Steuerelemente im Quellcode = Steuerelemente in 01 | 186 | 186 | **stimmt** |
| Properties im Quellcode = Properties in 01 | 1985 | 1985 | **stimmt** |
| Properties im Quellcode = Properties im Extraktionsmodell | 1985 | 1985 | **stimmt** |
| Steuerelemente mit Verhaltensformel im Quellcode = Eintraege in 02 | 95 | 95 | **stimmt** |

- *Steuerelemente im Quellcode = Steuerelemente in 01:* Quellcode: Zeilen `Control:` in Screen1.pa.yaml. Dokument: Abschnitte `### [C###]`.
- *Properties im Quellcode = Properties in 01:* Quellcode: Zeilen direkt unter einem `Properties:`-Block in App.pa.yaml und Screen1.pa.yaml. Dokument: fettgedruckte Property-Namen.
- *Properties im Quellcode = Properties im Extraktionsmodell:* Gegenprobe: unabhaengige Zaehlung in der YAML gegen das vom Parser gebaute Modell.
- *Steuerelemente mit Verhaltensformel im Quellcode = Eintraege in 02:* Quellcode: Steuerelemente, unter deren `Properties:` mindestens eine `On…`-Property steht (auch leer gesetzte).

Aufschlüsselung der Properties: 3 in `App.pa.yaml` (App) und 1982 in `Screen1.pa.yaml` (3 am Screen, 1979 an den 186 Steuerelementen).

Von den 95 Steuerelementen mit Verhaltensformel haben 92 eine inhaltliche Formel; bei drei (`Rectangle1`, `Circle1`, `Label1`) ist die `OnSelect`-Property gesetzt, aber leer. Alle 95 sind in `02_BUTTONS.md` aufgeführt.

## 2. 15 zufällige Formeln, Zeichen für Zeichen

Zufallsziehung mit festem Startwert (20261006), damit die Prüfung wiederholbar ist. „in 01" heißt: Der Wert steht als Codeblock wortgetreu in `01_APP_KOMPLETT.md`, einschließlich führendem `=`, Zeilenumbrüchen und Leerzeichen. „im Quellcode" heißt: Jede Zeile des Wertes kommt im YAML-Text vor.

| Nr. | Steuerelement | Property | Zeichen | in 01 | im Quellcode | auch in 02 | Ergebnis |
|---|---|---|---|---|---|---|---|
| 1 | `btnSlot2` | `OnSelect` | 782 | identisch | identisch | ja | **stimmt** |
| 2 | `lblÜberschriftBuchungen` | `Width` | 4 | identisch | identisch | nicht enthalten | **stimmt** |
| 3 | `ddStartTischePanel` | `PressedFill` | 20 | identisch | identisch | ja | **stimmt** |
| 4 | `btnSpeichernRaumPanel` | `Y` | 48 | identisch | identisch | nicht enthalten | **stimmt** |
| 5 | `ddStartTischePanel` | `HoverFill` | 23 | identisch | identisch | nicht enthalten | **stimmt** |
| 6 | `btnHitArea_1` | `BorderColor` | 27 | identisch | identisch | ja | **stimmt** |
| 7 | `ddEndTischePanel` | `BorderColor` | 20 | identisch | identisch | ja | **stimmt** |
| 8 | `dpWiederholenBis_1` | `OnSelect` | 56 | identisch | identisch | ja | **stimmt** |
| 9 | `btnMinus1Std` | `Color` | 23 | identisch | identisch | ja | **stimmt** |
| 10 | `btnPlus1Std_1` | `HoverBorderColor` | 33 | identisch | identisch | nicht enthalten | **stimmt** |
| 11 | `btnMinus1Std` | `Fill` | 491 | identisch | identisch | ja | **stimmt** |
| 12 | `lblTischeBuchenPanel` | `Text` | 15 | identisch | identisch | ja | **stimmt** |
| 13 | `imgGrundrissUG` | `Y` | 50 | identisch | identisch | nicht enthalten | **stimmt** |
| 14 | `btnSlot3` | `PressedColor` | 10 | identisch | identisch | nicht enthalten | **stimmt** |
| 15 | `ddStartTischePanel` | `ChevronFill` | 23 | identisch | identisch | ja | **stimmt** |

Die Spalte „auch in 02" ist nur eine Zusatzangabe: `02_BUTTONS.md` enthält nicht alle Properties, sondern nur die Verhaltens- und Zustands-Properties der Steuerelemente mit Verhaltensformel.

## 3. Gelesene Quelldateien

Vollständig gelesen und ausgewertet:

- `paket/entpackt/Microsoft.PowerApps/apps/1516988942138200528/1516988942138200528.json`
- `paket/manifest.json`
- `src/AppCheckerResult.sarif`
- `src/Header.json`
- `src/Properties.json`
- `src/References/DataSources.json`
- `src/Src/App.pa.yaml`
- `src/Src/Screen1.pa.yaml`
- `src/Src/_EditorState.pa.yaml`

## 4. Nicht gelesene Dateien

Diese Dateien liegen im entpackten Quellcode, wurden aber nicht ausgewertet. Sie enthalten keine Formeln:

- `paket/TischbuchungApp06.10.2026_20261006112813.zip` — keine Formeln
- `paket/entpackt/Microsoft.PowerApps/apps/1516988942138200528/N2392ebf5-6046-4245-a450-550349017614-document.msapp` — das Archiv selbst (daraus stammt `src/`)
- `paket/entpackt/Microsoft.PowerApps/apps/1516988942138200528/N4e69722d-e46a-4681-8af6-b67ea378a3ef-logoSmallFile` — Bilddatei (App-Logo)
- `paket/entpackt/Microsoft.PowerApps/apps/1516988942138200528/N7acce795-4eff-4128-b3ff-718b48bae5f1-identity.json` — Identitäts-/Signaturdaten des Pakets
- `paket/entpackt/manifest.json` — keine Formeln
- `src/Assets/Images/28a1eaca-ef5f-4471-9013-389860261717.png` — Bilddatei
- `src/Assets/Images/3fa86700-d646-46cb-896c-9fe3851d4ec2.gif` — Bilddatei
- `src/Assets/Images/614892e2-99dd-4e89-b19e-46fcb794d182.png` — Bilddatei
- `src/Assets/Images/71b737fa-52ea-4652-a52f-04ebf653d7ec.png` — Bilddatei
- `src/Assets/Images/a055a453-256a-42f6-a41e-e2e8e4dc6627.png` — Bilddatei
- `src/Assets/Images/bd64726c-c5da-4328-b19b-5a88482f2864.png` — Bilddatei
- `src/Assets/Images/bf2ca541-db54-4425-8b23-0036937f3688.png` — Bilddatei
- `src/Assets/Images/c09abd68-db7b-43a1-b9af-d631cfc365fa.png` — Bilddatei
- `src/Assets/Images/cd6cc243-9bbf-48ec-8cdb-d25558c54dd7.png` — Bilddatei
- `src/Controls/1.json` — Editor-Zustand der Steuerelemente (Positionen im Studio); die Formeln stehen in den `.pa.yaml`-Dateien
- `src/Controls/4.json` — Editor-Zustand der Steuerelemente (Positionen im Studio); die Formeln stehen in den `.pa.yaml`-Dateien
- `src/References/ModernThemes.json` — Vorlagen- und Designdefinitionen von Power Apps, nicht app-spezifisch
- `src/References/QualifiedValues.json` — interne Wertzuordnungen
- `src/References/Resources.json` — Verweise auf Medien und Veröffentlichungsdaten
- `src/References/Templates.json` — Vorlagen- und Designdefinitionen von Power Apps, nicht app-spezifisch
- `src/References/Themes.json` — Vorlagen- und Designdefinitionen von Power Apps, nicht app-spezifisch
- `src/Resources/PublishInfo.json` — Verweise auf Medien und Veröffentlichungsdaten
- `src/Resources/kkupxyht.jpg` — Bilddatei

Es gab **keine** Datei, die nicht gelesen werden konnte (kein Lesefehler, kein Entschlüsselungsproblem).

## 5. Herkunft

- Exportpaket: `TischbuchungApp06.10.2026_20261006112813.zip`, erstellt am 06.10.2026 um 11:28:12 UTC von `Josias.Assefaw@technoform.com`, Umgebung „Personal Productivity"
- Appstand im Paket: `appVersion` 2026-10-05T11:58:19Z, `LastSavedDateTimeUTC` 10/05/2026 11:58:18
- App-Name im Paket: „Tischbuchung"
- SHA-256 des `.msapp`: `1541C0D319B187A4486F1CE5C8330C3BC599DC52BA0B768176FBE6ED7AE612A7`

**UNSICHER — die App-ID:** Die erwartete App-ID `d247d18b-d36f-4a44-975a-7839695b2f12` kommt in keiner Datei des Pakets vor. Das Paket führt stattdessen `3d782261-b998-4e60-8b95-455c57214f29` (Ressourcen-ID im Manifest), `1516988942138200528` (Ordnername) und `e61d887c-84cf-4e0b-839c-79dbc3c333f8` (`Id`/`FileID` in `Properties.json`). Ein Exportpaket enthält die App-ID des Portals offenbar nicht. **Dass es die richtige App ist, stützt sich daher auf andere Merkmale:** Anzeigename „Tischbuchung" (Manifest und App-JSON), Umgebung „Personal Productivity", Ersteller Josias, der Exportzeitpunkt 06.10.2026, und inhaltlich auf die Übereinstimmung mit `INVENTAR.md` (ein Screen `Screen1`, `Titel` statt `Title`, `Tische.Geschoss`, `Checkedin`) sowie darauf, dass die drei erwarteten Änderungen seit dem 30.09. genau dort stehen, wo sie laut Briefing sein sollen.