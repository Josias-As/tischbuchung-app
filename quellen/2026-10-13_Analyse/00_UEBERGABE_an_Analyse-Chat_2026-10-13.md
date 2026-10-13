# ÜBERGABE an den Analyse-Chat: Grundriss-Ladeverhalten (Punkt 2) und Prüfstand vom 13.10.

Stand: 13.10.2026 · Von: Claude Code (Sitzung mit Josias) · Für: Claude im Chat (Analyse) + Josias
**Go-Live der Desktop-App ist Mittwoch, 14.10.2026.** Lies zuerst diese Datei, dann `NACHTRAG_5.md` und `ABSCHLUSSANALYSE.md` (stammen von dir) und prüfe gegen den Export vom 13.10. (`TischbuchungApp13.10.2026959_….zip`, Quelle der Wahrheit, nur lesen).

## 0. Feedback von Josias
Deine bisherigen Analysen und Übergabedateien (L2 v0.3, Nachtrag 5, Abschlussanalyse, Betriebshandbuch) fand er **sehr gut**. Bitte denselben Stil: maschinell aus dem Export erzeugte **vollständige Properties**, je Schritt Ort/Diff/Block/Test/Rückfall, Kennzeichnung **belegt / gemessen / geschlussfolgert / UNSICHER**, Anhang mit Originalen, unabhängige Prüfung, Kurzfassung zuerst, Deutsch mit Umlauten.

## 1. Aufträge
| # | Auftrag | Dringlichkeit |
|---|---|---|
| A | **Grundriss-Ladeverhalten** (Abschnitt 3): fertige, geprüfte Blöcke für die Änderung „Positionen als benannte Formeln, Tische lokal laden“ als Übergabedatei `UEBERGABE_Grundriss_Laden_v1.md` im L2-Stil | **nach** dem Go-Live empfohlen, aber einfügebereit vorbereiten |
| B | **Stand-Abgleich 13.10.** (Abschnitt 2): Befunde bewerten, offene Entscheidungen zu Nachtrag 5 und Dokumenten sauber aufbereiten | vor dem Go-Live |
| C | Kleinigkeiten (Abschnitt 4) | mit B |

## 2. Prüfstand des Exports vom 13.10. (von Claude Code, maschinell, belegt)
Verglichen mit dem Export vom 07.10. (82 neue, 121 geänderte Properties, 4 neue Steuerelemente: `Timer1`, `btnGrundrissSperre`, `btnGrundrissAktualisieren`, `icoAktualisierenGrundriss`). Den Export vom 08.10. 14:26 hat Claude Code **nicht**.
- **App-Prüfung:** 94 Hinweise, **keine Fehler** (38 `AccessibleLabelNeeded`, 22 `TabIndex`, 11 `UnusedVariables`, 9 `FocusBorder`, 8+2 Delegation, 2 `CollectingReadOnlyTable`, 1 `ScreenHasManyControls`, 1 `ReadableScreenName`). Klammern/Strings ausgeglichen, keine doppelten Steuerelementnamen, keine Testreste, `varFreigabeMinuten = 30`, `varGrundrissSperreSekunden = 120`, `Timer1` 15000 ms, Wiederholen, unsichtbar.
- **Alle 8 Schreibstellen** (`btnSpeichern`, `btnSpeichernTischePanel`, `btnStornieren`, `btnStornieren_1`, `btnStornierenKlein`, `btnVerlängern`, `btnVerlängern_1`, `btnEinchecken`) haben `varIsLoading`, `varSperreBis`, `IfError`; die Knöpfe außer Speichern/StornierenKlein zusätzlich Nachlese per `LookUp`.
- **L2-Ladezeile** steht 11× zeichengleich (Länge 688) da, alle mit `Set(varGrundrissStand; Now())`.
- **Start im UG ist umgesetzt:** `App.OnStart` setzt `varAusgewaehltesStockwerk` auf `"UG"`, `ddStockwerk.Default` = `"MMS Untergeschoss"`, `imgGrundrissOG/UG.Visible` hängen an der Variablen. Rest: `Label3.Text` enthält ein festes `"OG"` (prüfen).
- **UG-Positionen (App.OnStart):** Desk 13 `(1202; 260)`, Desk 14 neu `(1202; 337)`, Desk 15 `(1255; 258)`, Desk 16 `(1255; 346)`, Desk 17 `(1360; 254)`, Desk 18 `(1410; 252)`, alle vertikal. Josias hat sie visuell angepasst.

### Befunde
1. **`ddStockwerk.SelectionColor` ist noch weiß** (`RGBA(255; 255; 255; 1)`) bei `SelectionFill = RGBA(196; 196; 203; 1)`: weiße Schrift auf Hellgrau. Soll `RGBA(32; 54; 71; 1)` werden. Aktuelle Farben: `Fill RGBA(233; 233; 235; 1)`, `HoverFill RGBA(218; 218; 223; 1)`.
2. **Nachtrag 5 ist NICHT eingefügt:** `varStornoFrageID`/`varStornoFrageAuswahl` kommen nicht vor (N1–N3 fehlen). N4/N5: `recBuchungDanach1.Visible` ohne Schutz (fragt `Raumbuchungen` beim Start ab), `lblStatusHeute.Text` in der alten Fassung. N6: `Timer1.OnTimerEnd` sucht über `User().FullName`. N7: `galAlleTischbuchungen.Items` unbedingt. `btnStornieren.Text` ist `"Stornieren"`. `btn5Std.Fill` ist in einer neueren Fassung (mit `varPanelJetzt`), ob das F5 ist, ist unklar.
3. **Dokument-Widerspruch:** Kurzanleitung v4 und Betriebshandbuch v4 beschreiben „Stornieren mit Bestätigung“ (und den Grundriss-Aufbau). Die App hat das nicht. Entweder N1–N3 einfügen oder die Dokumente anpassen, **bevor sie an Nutzer gehen**.
4. Nicht prüfbar mit dem Export: Liste `Tische` in SharePoint (passen die Namen Desk 14–18 zu den Positionen?), Rechte (Lesen = alle), Test 17 (Spätbuchung, echte 30 Minuten), Handy-Gerätetest, Handy-App (kein Export dabei).

**Einschätzung von Claude Code (Josias wollte kritisch):** Nichts in Nachtrag 5 ist für die Richtigkeit der Buchungen zwingend. Empfohlen: N4, N1–N3 (wegen der Dokumente), H8 (Handy-Tageswechsel); N6 nur nach Konten-Test; N5 und N7 nach dem Go-Live. Zwingend sind die Betriebspunkte aus deiner Abschlussanalyse (Rechte, Test 17, Tische/Positionen, Gerätetest, Sicherung, Vertretung für Michael ab 12.10., Check-in-Pflicht in der Mail). **Bitte bewerte das unabhängig und sage Josias, was du davon anders siehst.**

## 3. Auftrag A: Grundriss-Ladeverhalten
**Wunsch von Josias:** (1) Die Tische sollen beim App-Start **nicht kurz bei X=0, Y=0** stehen. (2) Der Grundriss soll im UG starten (erledigt). (3) Der Wechsel OG↔UG soll **von Anfang an** sofort sein; heute lädt er nur beim ersten Mal.

**Ursache (geschlussfolgert aus dem Export, nicht gemessen):**
- `usenonblockingonstartrule` ist **an** (belegt). `App.OnStart` läuft parallel zum Zeichnen. Der Grundriss wird gezeichnet, bevor `ClearCollect(colTischPositionen; …)`/`colTischPositionenUG` gefüllt sind → `LookUp` leer → Kacheln bei 0/0.
- UG langsam beim ersten Ansehen: `Gallery1.Items = Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)` und die benannten Formeln `TischNrOG`/`TischNrUG` (in `App.Formulas`, lesen `Tische`) werden erst beim ersten Bedarf ausgewertet; danach liegen sie im Zwischenspeicher.

**Plan (Vorschlag von Claude Code, bitte prüfen und verbessern):**
1. `colTischPositionen` und `colTischPositionenUG` als **benannte Formeln** in `App.Formulas` (`Table({…}; …)`), die zwei `ClearCollect`-Blöcke aus `App.OnStart` entfernen. Namen bleiben, die Kachel-Formeln ändern sich nicht.
2. `ClearCollect(colTische; Tische)` als **erste** Anweisung in `App.OnStart`; `Gallery1.Items`, `TischNrOG`, `TischNrUG` lesen aus `colTische`.
3. Betroffene Properties: `App.Formulas` (ganz ersetzen), `App.OnStart` (ganz ersetzen), `Gallery1.Items`.

**Fakten aus dem Export 13.10. (belegt):**
- `colTischPositionen`/`…UG` werden nur in `App.OnStart` geschrieben; gelesen in `Rectangle1.X/Y/Width/Height` und `conDetailsPopup.X/Y`.
- `TischNrOG/UG` werden nur in `App.Formulas` definiert und in `Rectangle1.Y` gelesen. `colTische` existiert in der Desktop-App **nicht** (kein Namenskonflikt; die Handy-App nutzt den Namen separat).
- `Tische` wird außerdem direkt gelesen in `ddTischePanel.Items` (`Tische As Ti`) und in `btnSpeichern`/`btnSpeichernTischePanel` (`LookUp(Tische; ID = varNeuTischID && Gesperrt = true)`, **frisch am Server, soll so bleiben**). `Refresh(Tische)` gibt es nirgends: Die App lädt `Tische` nur beim Start (Betriebshandbuch sagt dasselbe).
- **Schreibweise in `App.Formulas` (deutsch):** Definitionen enden mit `;;`, wie im Export (`BasisBreite = 1920;;`). Kommentare `//` sind dort erlaubt (und vorhanden). Aktueller `App.Formulas` enthält u. a. `BasisSkalierung`, `BasisKachel…`, `TischNrOG/UG`, `BasisSkalierungReferenz = Min(881 / BasisBreite; 678 / BasisHoehe)`.
- **Y-Formel (`Rectangle1.Y`):** Die Galerie (`TemplateSize = 1`, also Höhe 1 px, Padding ungesetzt) schiebt jede Kachel um `Nr − 1` px nach unten; die Formel `(Y_Liste + (Nr−1)·v/BasisSkalierungReferenz)·BasisSkalierung − (Nr−1)·v` mit `v = TemplateHeight + TemplatePadding` gleicht das aus. Die Werte in `colTischPositionen(UG)` wurden **mit der jeweiligen `Nr`** eingemessen (Y fällt um ca. 2,2 Listeneinheiten je Nummer, z. B. UG Desk 13 → 15 → 17 → 18: 260, 258, 254, 252). **Konsequenz für die Änderung:** `Nr` bleibt nur gleich, wenn `colTische` dieselbe Reihenfolge hat wie die Abfrage `Tische`. `ClearCollect(colTische; Tische)` liefert die Zeilen der Liste (Reihenfolge nach ID, Datenzeilenlimit 2000, 34 Tische). Bitte prüfen, ob `Filter(colTische; …)` und die bisherige delegierte Abfrage dieselbe Reihenfolge liefern. **Neue Tische stehen am Ende der Liste** (höchste `Nr`).
- Die Josias-Anpassung am neuen UG Desk 14: Y 348 → 337 (Nr-Versatz).

**Zu prüfen / zu entscheiden (bitte beantworten):**
- Ist der Plan tragfähig? Gibt es Fallen bei benannten Formeln (Tabellenliteral mit Texten/Zahlen, Reihenfolge der Auswertung, Zugriff aus `LookUp` in `Rectangle1.*`, `conDetailsPopup`)?
- Was passiert beim Start, solange `colTische` noch leer ist (Galerie leer, `TischNr` leer, Positionen vorhanden)? Gibt es einen Zwischenzustand, der Fehler wirft oder falsche Kacheln zeigt?
- Reicht `ClearCollect(colTische; Tische)` als erste Anweisung, oder braucht es Schutz (z. B. `Gallery1.Visible`)?
- Änderung der Wirkung auf **Gesperrt** (Kachelfarbe lesen aus `colTische` statt live)? Aktuelles Verhalten ist „nur beim Start“, also gleich.
- Alternative zum Plan: nur `colTische` ohne benannte Positionen? Nur Positionen als benannte Formeln? Aufwand/Nutzen gegen das Risiko vor dem Go-Live bewerten.
- Test-Bogen (Start, OG↔UG, Datum wechseln, Buchen, gesperrter Tisch, Tab „Buchungen“, Handy-Gegenprobe).
- **Empfehlung von Claude Code:** erst nach dem Go-Live einfügen (ca. 1 Sekunde Gewinn gegen drei Properties, von denen `App.Formulas` den ganzen Grundriss trägt). Sag Josias deine Einschätzung.

## 4. Kleinigkeiten (Auftrag C)
- `ddStockwerk.SelectionColor` auf `RGBA(32; 54; 71; 1)` (Befund 1).
- `Label3.Text` mit festem `"OG"` prüfen, wenn das UG offen ist.
- Neue Tische/Umbenennung (UG): Es gibt jetzt 18 UG-Desks; die Positionsliste ist bereits angepasst. Der GoBright-Import (~237 Buchungen per Flow) muss die alten Nummern 14–17 auf 15–18 umstellen, **bevor** der Flow läuft. Flow-Zeilen gehören dem Konto der Verbindung (siehe Betriebshandbuch); importierte Buchungen haben `CheckedIn = Nein`, künftige verfallen ohne Check-in. Die Go-Live-Mail v4 geht davon aus, dass GoBright-Buchungen **nicht** übernommen werden: Widerspruch klären.
- **Nicht** Teil dieser Übergabe: Handy-App (H8 ist von dir), Paket K (veraltet, nicht mehr einfügen).

## 5. Arbeitsregeln (verbindlich)
Josias fügt jede Formel selbst in Power Apps Studio ein, du bearbeitest keine App. **Immer die ganze Property ersetzen.** Deutsche Schreibweise (`;` trennt Argumente, `;;` verkettet, `,` Dezimaltrenner), in Verhaltensformeln keine Kommentare, `powerfxv1 = false`. Namen nur aus dem Quellcode. Kleine Schritte, ein Studio-Fenster, vorher `.msapp`-Export. Ehrlich und kritisch. Berechtigungs-/Tenant-Probleme an Michael (IT, ab 12.10. im Urlaub, Vertretung noch nicht eingetragen).

## 6. Lieferung
`UEBERGABE_Grundriss_Laden_v1.md` im Stil von L2 v0.3 / Nachtrag 5 (Kurzfassung, Einfügeschritte, Diff, vollständige Blöcke, Test, Rückfall, UNSICHER-Tabelle, unabhängige Prüfung) **plus** eine kurze Antwort an Josias zu Abschnitt 2 (Befunde, Nachtrag 5, Dokumente, Importfrage). Wenn dir Informationen fehlen, sag es konkret.

## 7. Dateien in diesem Paket
`TischbuchungApp13.10.2026959_….zip` (Export), `props_de.json` (alle Properties des 13.10.-Exports in deutscher Schreibweise, Schlüssel `Steuerelement.Property`), `exportiere_props.ps1` (erzeugt die JSON aus einem entpackten Export, PowerShell), `NACHTRAG_5.md`, `ABSCHLUSSANALYSE.md`, `BETRIEBSHANDBUCH_Michael_v4.md`, `KURZANLEITUNG_und_GoLive_Mail_v4.md`, `HANDY_H8_Tageswechsel.md`, `UEBERGABE_Grundriss_L2_v0.3_1.md` (Stilvorlage).
