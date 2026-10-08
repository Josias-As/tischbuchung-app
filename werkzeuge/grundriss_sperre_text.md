# Grundriss-Sperre nach 2 Minuten (08.10.2026)

Für den Desktop-Chat. Grundlage: Paket F Fassung 2.1 (F1–F8) im Studio. Erzeugt und geprüft mit `werkzeuge/grundriss_sperre.py`. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Was passiert:** 2 Minuten nach dem letzten Laden des Grundrisses legt sich eine halb durchsichtige weiße Fläche über `conGrundriss`. Darauf erscheint mittig der Knopf **„Grundriss aktualisieren“**.
  - Kacheln und `ddStockwerk` sind dann nicht bedienbar.
  - Der Knopf macht dasselbe wie das Aktualisieren-Symbol (`Icon1_1`): `Refresh`, Freigabe-Grenze, Ladezeile. Danach verschwinden Fläche und Knopf, und die 2 Minuten laufen neu.
- **Einstellung:** `Set(varGrundrissSperreSekunden; 120)` in `App.OnStart`.
- **Zeitstempel:** Jede Stelle, die `colGrundriss` erfolgreich lädt, setzt `varGrundrissStand` (direkt hinter dem `ClearCollect`, also nur bei Erfolg). Das sind **15 Stellen + der neue Knopf**, vollständige Liste unten. Schlägt das Laden fehl, bleibt der alte Stempel, und der Knopf erscheint zum erneuten Versuch.
- **Zeitprüfung ohne Abfrage:** `tmrAktualisieren` setzt alle 15 Sekunden nur `varJetztTakt`. Die Sichtbarkeit vergleicht zwei Variablen. Erscheinen nach 2:00 bis 2:15 Minuten.
- **Umfang:** 4 Schritte, 50 Properties, davon 34 an den 2 neuen Steuerelementen. Die 15 Ladestellen ändern sich nur um `; Set(varGrundrissStand; Now())` (maschinell geprüft: sonst nichts). Maschinell 0 Fehler, in Studio nichts getestet.

## Alle Stellen, die `colGrundriss` laden (Stand F2.1, belegt durch Suche im Gesamtstand)
| Stelle | Schritt |
|---|---|
| `App.OnStart` | S1 (Stempel + 2 Variablen) |
| `ddStockwerk.OnChange`, `dpAnsichtsDatum.OnChange` | S2 |
| `Icon1.OnSelect`, `Icon1_1.OnSelect`, `Image6.OnSelect`, `btnHitArea_1.OnSelect` (Aktualisieren-Symbole) | S2 |
| `btnSpeichern.OnSelect`, `btnSpeichernTischePanel.OnSelect` | S2 |
| `btnVerlängern.OnSelect`, `btnVerlängern_1.OnSelect` | S2 |
| `btnStornieren.OnSelect`, `btnStornieren_1.OnSelect`, `btnStornierenKlein.OnSelect` | S2 |
| `btnEinchecken.OnSelect` | S2 |
| `tmrAktualisieren.OnTimerEnd` | S3: **lädt nicht mehr** |
| `btnGrundrissAktualisieren.OnSelect` (neu) | S4 |

## Wie `tmrAktualisieren` (F8) dazu passt: anpassen, nicht entfernen
- **Bisher (F8):** alle 5 Minuten `Refresh` (2 Galerien) und Ladezeile, also **3 Abfragen je 5 Minuten je offener App**, auch wenn niemand am Platz ist (geschlussfolgert aus den Formeln). Bei 30 offenen Apps sind das etwa 18 Abfragen pro Minute.
- **Mit der Sperre** würde das automatische Laden den Grundriss nach 5 Minuten wieder freigeben. Der Knopf wäre also abwechselnd da und weg, und die Abfragen liefen trotzdem.
- **Vorschlag (umgesetzt in S3):** Der Timer **lädt nicht mehr**. Er läuft alle 15 Sekunden und macht nur noch:
  1. `varJetztTakt` setzen (keine Abfrage).
  2. Den Tageswechsel: Datum auf heute, Stempel leeren, also erscheint der Knopf sofort.
  3. Die Check-in-Erinnerung aus F8. Sie fragt **nur**, wenn der Grundriss lokal eine eigene, nicht eingecheckte Buchung zeigt, die bald beginnt, und dann **höchstens alle 5 Minuten** (`varErinnerungAb`). Das ist die einzige Abfrage ohne Tippen.
- **Ergebnis:** Ohne Tippen gibt es **0 Abfragen**, außer der gedrosselten Erinnerung. Neu geladen wird nur, wenn jemand den Knopf oder ein Aktualisieren-Symbol tippt, bucht, storniert, verlängert oder eincheckt.
- **Was dadurch wegfällt:** Die Dashboard-Listen (eigene Buchungen) werden nicht mehr alle 5 Minuten automatisch aufgefrischt, nur noch durch Tippen auf Aktualisieren oder durch eigene Aktionen. Eine Buchung, die man am Handy gemacht hat, erscheint am PC also erst nach „Aktualisieren“. Die Check-in-Erinnerung stützt sich auf den zuletzt geladenen Grundriss.
- **Entfernen wäre schlechter:** Der Takt für die Sperre braucht ohnehin einen Timer. Ein zweiter Timer wäre ein weiteres Steuerelement.

## Was passiert bei offenen Dialogen (belegt: Ebenen-Reihenfolge der Screen-Kinder im Export)
`conGrundriss` ist das **unterste** Kind von `Screen1`. Buchungsdialog (`conBuchungDialog`), Panel (`conTischBuchungenPanel`), Verwalten-Dialoge, Check-in-Frage (`conCheckinDialog`), Details-Popup (`conDetailsPopup`) und Lade-Overlay liegen **darüber** auf `Screen1`. Fläche und Knopf liegen **in** `conGrundriss`. Deshalb:
- **Buchungsdialog, Panel, Verwalten, Check-in-Frage, Details offen:** Sie bleiben voll bedienbar. Die Fläche erscheint höchstens dahinter. Nichts verspringt: Der Container ist frei angeordnet, die neuen Steuerelemente liegen fest auf X/Y 0 und verschieben nichts. Speichern lädt den Grundriss, die Sperre verschwindet.
- **Während des Speicherns (`varIsLoading`):** Das Lade-Overlay liegt oben. Erscheint die Sperre in dieser Zeit, verschwindet sie mit dem Laden am Ende. Der Knopf ist dann grau (`DisplayMode`).
- **Aufgeklappte Stockwerk-Auswahl:** Sie liegt in `conGrundriss` unter der Fläche. Nach dem Aktualisieren ist sie wieder bedienbar.
- **Außerhalb von `conGrundriss`** (Dashboard, Kopfzeile, Tabs) wird nichts gesperrt.

## Warum Fläche + Knopf (schlankste Lösung)
- **`DisplayMode` am Container:** **UNSICHER**, ob Kinder in klassischen Containern den `DisplayMode` erben. Außerdem müsste jede Kachel umgebaut werden.
- **Ein Rechteck:** Ob es Klicks zuverlässig abfängt, ist **UNSICHER**.
- **Eine klassische Schaltfläche** fängt Klicks immer ab. Sie hat `OnSelect`, die Fläche macht beim Tippen nichts (`false`). `TabIndex = -1`, damit sie per Tastatur nicht angesprungen wird.
- Also zwei neue Steuerelemente: Fläche und Knopf.

## UNSICHER (mit Test)
| Nr | Was | Test |
|---|---|---|
| S-U1 | Die halb durchsichtige Schaltfläche fängt alle Klicks ab, auch über der Kachel-Galerie (**geschlussfolgert**) | Test 3 |
| S-U2 | `Reset(dpAnsichtsDatum)` im Timer löst kein `OnChange` aus. Deshalb leert der Timer den Stempel, damit der Knopf erscheint | nur um Mitternacht prüfbar; der Knopf lädt dann den neuen Tag |

## Testablauf
1. S1–S4 einfügen, App-Prüfung ohne rote Fehler, **OnStart ausführen**, Vorschau starten.
2. 2:15 Minuten warten → Fläche und Knopf erscheinen, Grundriss blass.
3. Kachel und `ddStockwerk` antippen → **nichts** passiert. Dashboard-Knöpfe (außerhalb) funktionieren.
4. Knopf antippen → „Aktualisiert.“, Fläche weg. Nach 2 Minuten wieder da.
5. Buchungsdialog über eine Kachel öffnen, 2:15 Minuten warten → Dialog bleibt bedienbar, Fläche nur dahinter. Speichern → „Gebucht …“, Fläche weg.
6. Optional Monitor: App 6 Minuten unberührt lassen → **keine** `getRows`. Ausnahme: Es gibt eine eigene, nicht eingecheckte Buchung, die bald beginnt (Erinnerung).
7. Zum schnellen Testen in Studio einen Testknopf mit `Set(varGrundrissSperreSekunden; 20)` → dann reichen 35 Sekunden. **Testknopf vor dem Veröffentlichen löschen.**

## Rückfall
- S4: die zwei neuen Steuerelemente löschen.
- S3: `tmrAktualisieren.Duration` auf `300000` und `OnTimerEnd` aus F2.1 (Anhang A dort).
- S1/S2: die F2.1-Fassungen (`UEBERGABE_PaketF2_1.md`). Der zusätzliche Stempel stört allein nicht, Zurücksetzen ist also nicht nötig.
