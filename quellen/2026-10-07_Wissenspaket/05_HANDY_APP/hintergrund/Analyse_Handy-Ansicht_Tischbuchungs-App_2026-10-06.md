# Analyse: Handy-Ansicht für die Tischbuchungs-App

**Stand:** 06.10.2026 · **Betrifft:** App „Tischbuchung" (`d247d18b-d36f-4a44-975a-7839695b2f12`), Umgebung „Personal Productivity"
**Art:** Recherche + Architekturentscheidung. **Keine Änderung an der App.**

> **⚠ KORREKTUR (06.10.2026, nachmittags):** Der Quellcode (Export 30.09.) zeigt `ScaleToFit = False`, `MaintainAspectRatio = False`, `LockOrientation = False`. Die Desktop-App ist also NICHT auf 16:9 skaliert. Die Aussage in Abschnitt 0 Punkt 4 und Abschnitt 4 („Variante B funktioniert nicht ohne Variante A") ist damit **falsch**: Ein zusätzlicher Handy-Screen in derselben App ist möglich. Die eigene App bleibt die Empfehlung, aber wegen Go-Live-Risiko und Bauen auf einer Hochformat-Zeichenfläche. Details: `claude/Bauplan_Handy-App_Tischbuchung_2026-10-06.md`, Abschnitt 1.

---

## 0. Kurzfassung (für Eilige)

1. **Power Apps hat keine automatische Handy-Version.** Browser, Power-Apps-Mobile-App und Teams zeigen *dieselbe* App. Wie sie am Handy aussieht, entscheiden allein das **App-Format** (Phone/Tablet) und die **Anzeige-Einstellungen** (*Scale to fit*, *Lock aspect ratio*, *Lock orientation*).
2. **Diese Einstellungen gelten für die ganze App, nicht pro Screen.** Genau das ist das Kernproblem: Die Desktop-App lebt davon, dass sie auf 16:9 fixiert und skaliert wird (Grundriss-Koordinaten stimmen nur dann). Ein Handy-Screen in derselben App bräuchte das Gegenteil (Hochformat, *Scale to fit* aus).
3. **Empfehlung: eigene, kleine Handy-App** („Tischbuchung Mobil") auf denselben SharePoint-Listen. Hochformat, *Scale to fit* aus, vertikale Auto-Layout-Container. Inhalt: Header, „Tisch buchen", „Heute", „Meine Buchungen" — kein Grundriss.
4. **Warum nicht in die bestehende App einbauen:** Es geht technisch nur, wenn man *Scale to fit* app-weit ausschaltet. Dann muss Screen1 inkl. Grundriss komplett responsiv umgebaut werden — genau das Problem, das am 29.09. nur durch die 16:9-Fixierung gelöst wurde. Unter Zeitdruck das größte Risiko im ganzen Projekt.
5. **Preis der Empfehlung:** Die Buchungslogik (v. a. Speichern und Doppelbuchungsprüfung) existiert zweimal. Das ist beherrschbar, wenn die Handy-App bewusst weniger kann (keine Mehrfachauswahl, keine Serie) und die Prüfregeln wortgleich übernommen werden.
6. **Über den Auftrag hinaus:** Der eigentliche Handy-Anwendungsfall ist „am Tisch stehen und einchecken". Ein **QR-Code pro Tisch**, der die Handy-App per Deep Link mit `?tisch=OG-5` öffnet, macht das Einchecken mit einem Scan möglich — und funktioniert auch im Browser, ohne Scanner-Control.

---

## 1. Worum es eigentlich geht

Die Desktop-App ist ein Planungswerkzeug: Grundriss ansehen, Tische auswählen, mehrere Tage buchen. Am Handy braucht das niemand. Am Handy will man in 10 Sekunden eines von vier Dingen:

| Situation | Was das Handy können muss |
|---|---|
| Morgens auf dem Weg ins Büro | „Habe ich heute einen Tisch? Welchen?" |
| Spontan im Büro | „Welcher Tisch ist gerade frei?" → buchen |
| Am Tisch angekommen | Einchecken (sonst verfällt die Buchung) |
| Plan geändert | Stornieren / Ende verkürzen |

Daraus folgt: Die Handy-Ansicht ist **keine verkleinerte Desktop-App**, sondern eine **andere App mit kleinerem Funktionsumfang**. Das deckt sich mit dem, was du beschrieben hast (Panel Tischbuchung, Panel Tischbuchungen heute, Header, abgewandelte Buchungen-Ansicht) — nur konsequent zu Ende gedacht.

---

## 2. Wie Power Apps mit Handys umgeht — die Grundlagen

### 2.1 Es gibt drei „Player", aber nur eine App

| Player | Wie geöffnet | Besonderheiten |
|---|---|---|
| **Handy-Browser** (Safari, Chrome) | Link `apps.powerapps.com/play/e/{Umgebungs-ID}/a/{App-ID}` | Kein Installieren nötig. Anmeldung per Microsoft-Konto. Barcode-Reader-Control funktioniert hier **nicht**. |
| **Power Apps Mobile** (iOS/Android) | App aus dem Store, Tischbuchung in der Liste | Kann die App als Symbol auf den Startbildschirm legen („Pin to Home" bzw. über iOS-Kurzbefehle). Zeigt beim ersten Start Wisch-Gesten-Hinweise. Neue Versionen kommen teils verzögert an (Cache). |
| **Teams Mobile** | Wenn die App als Teams-Tab/App hinzugefügt wurde | Für Technoform ggf. der bequemste Weg, falls Teams auf den Diensthandys ist. |

Alle drei rendern **exakt dieselbe App** mit denselben Einstellungen. Es gibt keinen Schalter „Handy-Layout verwenden".

**Wichtig seit 01.05.2026:** Deep Links müssen die Umgebungs-ID enthalten (`/play/e/{env}/a/{app}`). Alte Links und Startbildschirm-Verknüpfungen ohne Umgebungs-ID funktionieren nicht mehr.

### 2.2 Format: Phone oder Tablet

Das Format wird beim Anlegen einer App gewählt.

| | Phone-Format | Tablet-Format |
|---|---|---|
| Design-Größe | 640 × 1136 (Hochformat) | z. B. 1366 × 768, 16:9, frei wählbar |
| Breakpoints (`App.SizeBreakpoints`) | `[1200; 1800; 2400]` (verdoppelt, wegen Koordinatensystem) | `[600; 900; 1200]` |
| Gedacht für | Smartphones | Desktop, Laptop, Tablet |

Microsoft Learn sagt dazu deutlich: Wer eine Tablet-App am Smartphone öffnet, bekommt eine winzige, schwer lesbare Ansicht oder muss das Handy drehen. Die offizielle Lernmodul-Empfehlung ist **je ein App pro Formfaktor**; eine einzige responsive App sei möglich, aber aufwendiger.

### 2.3 Die vier Anzeige-Einstellungen (Einstellungen → Anzeige)

| Einstellung | Bedeutung | Für Desktop-App heute | Für Handy nötig |
|---|---|---|---|
| **Scale to fit** (An die Größe anpassen) | Die ganze App wird wie ein Bild auf den verfügbaren Platz skaliert. Alles bleibt pixelgenau, wird aber kleiner/größer. | **An** (daran hängt der Grundriss) | **Aus**, damit die App den Platz wirklich nutzt |
| **Lock aspect ratio** | Seitenverhältnis bleibt fix, Rest wird mit Balken gefüllt. Geht automatisch aus, wenn *Scale to fit* aus ist. | vermutlich **an** (16:9) | aus |
| **Lock orientation** | Hoch-/Querformat erzwingen | Querformat | **Hochformat an** |
| Orientation / Size | Hoch oder quer, Seitenverhältnis | Quer, 16:9 | Hoch |

**Kernaussage:** Alle vier gelten **für die gesamte App**. Man kann nicht Screen1 skalieren lassen und einen Handy-Screen responsiv machen.

> ⚠ Bitte in der echten App „Tischbuchung" kurz nachsehen, wie diese Einstellungen *jetzt* stehen. Die Annahme „Scale to fit an, 16:9 fixiert" stammt aus der Notiz vom 29.09. (Tische stimmen nur, wenn die App auf 16:9 festgesetzt ist).

### 2.4 Wie Responsivität in Power Apps funktioniert (wenn *Scale to fit* aus ist)

- `App.Width` / `App.Height` = echte Fenster- bzw. Gerätegröße.
- Screens haben standardmäßig `Width = Max(App.Width; App.MinScreenWidth)` und `Height = Max(App.Height; App.MinScreenHeight)`. Ist das Gerät kleiner als das Minimum, wird der Screen **scrollbar**, nicht kleiner.
- `Screen.Size` liefert automatisch `ScreenSize.Small` (Handy), `.Medium`, `.Large`, `.ExtraLarge` (Desktop) anhand der Breakpoints.
- Steuerelemente bekommen Formeln statt fester Zahlen: `Width = Parent.Width - 32`, `X = 16`, `Y = lblTitel.Y + lblTitel.Height + 12` usw.
- **Auto-Layout-Container** (horizontal/vertikal) nehmen einem das meiste davon ab: Kinder werden automatisch untereinander gestapelt, `X`/`Y` der Kinder werden ignoriert (das kennst du schon vom 10.09.).
- Bekannte Stolpersteine laut Microsoft: Das Studio zeigt Responsivität nicht korrekt an; Ziehen mit der Maus **überschreibt** Formeln in X/Y/Width/Height mit festen Zahlen; echtes Verhalten nur in der Vorschau bzw. veröffentlicht testen.

### 2.5 Gerät erkennen

| Methode | Formel | Taugt für |
|---|---|---|
| Betriebssystem | `Host.OSType` → `"iOS"`, `"Android"`, `"Windows"`, `"Mac OS"`, … | Weiterleitung Desktop-App → Handy-App |
| Bildschirmgröße | `Screen1.Size = ScreenSize.Small` | Layout-Entscheidungen innerhalb einer responsiven App (von Microsoft bevorzugt) |
| Seitenverhältnis | `App.Height > App.Width` | Grobe Hochformat-Erkennung |
| Startparameter | `Param("ansicht") = "mobil"` | Explizit per Link steuern, unabhängig vom Gerät |

Microsoft rät, `Host.OSType` nicht für Funktionsunterschiede zu verwenden, sondern `Screen.Size`. Für eine reine **Weiterleitung** auf eine andere App ist `Host.OSType` aber genau richtig.

`App.StartScreen` kann je nach Bedingung einen anderen Start-Screen wählen (`If(Param("ansicht") = "mobil"; scrMobil; Screen1)`), darf aber **keine** Variablen aus `OnStart` lesen und kein `Navigate`/`Set` ausführen. `Navigate` in `OnStart` ist von Microsoft abgekündigt.

---

## 3. Warum die heutige App am Handy unbrauchbar ist

Mit *Scale to fit* an und 16:9-Querformat passiert am Handy im Hochformat Folgendes: Die gesamte 1920er-Breite wird auf ca. 390 Pixel Handybreite gestaucht. Ergebnis: Ein schmaler Streifen in der Bildschirmmitte, Schrift ca. 4 pt, Buttons nicht treffbar, oben und unten schwarze bzw. leere Balken. Dreht man das Handy, wird es etwas besser, bleibt aber unbedienbar.

Daran ändert **kein** zusätzlicher Container in Screen1 etwas, weil die Skalierung über allem liegt.

---

## 4. Die drei Architektur-Varianten im Vergleich

### Variante A — Eine App, komplett responsiv

*Scale to fit* aus, Screen1 so umbauen, dass bei `ScreenSize.Small` der Grundriss ausgeblendet und die Panels untereinander gestapelt werden.

- ✅ Eine App, eine Logik, ein Link
- ❌ **Alle** Container in Screen1 brauchen Formeln statt fester Koordinaten
- ❌ Der Grundriss ist auf das 16:9-Skalieren der ganzen App angewiesen. Nach der Notiz vom 29.09. verschieben sich Tische, sobald nicht die App selbst auf 16:9 sitzt. Der Grundriss müsste in einen eigenen, festen 16:9-Container mit eigener Skalierung umgebaut werden — die Formel `BasisSkalierung = Min(conGrundriss.Width/1920; conGrundriss.Height/1080)` ist dafür eine gute Basis, wurde aber genau in diesem Szenario als unzuverlässig erlebt.
- ❌ Auch der Desktop sieht danach anders aus: Jedes Browserfenster, jede Monitorgröße, jeder Zoom ergibt ein anderes Layout. Bisher gibt es dafür null Tests.
- **Aufwand:** hoch (Tage) · **Risiko für die laufende App:** hoch

### Variante B — Eine App, zusätzlicher Handy-Screen (`scrMobil`)

`App.StartScreen = If(Host.OSType = "iOS" || Host.OSType = "Android"; scrMobil; Screen1)`.

- ✅ Logik und Variablen liegen in einer App
- ❌ **Funktioniert nicht ohne Variante A.** Weil die Anzeige-Einstellungen app-weit gelten, wird auch `scrMobil` auf 16:9-Querformat skaliert. Am Handy sieht man also einen winzigen, querliegenden Handy-Screen. Um das zu ändern, muss *Scale to fit* aus — und dann gilt für Screen1 alles aus Variante A.
- Der einzige Umweg wäre, `scrMobil` selbst als 16:9-Querformat-Layout zu gestalten (Handy quer halten). Das ist kein Handy-Erlebnis.
- **Fazit:** Variante B ist in Wahrheit Variante A plus ein zusätzlicher Screen. Verwerfen.

> Das korrigiert die Notiz in der Wissensbasis vom 24.09. („Handy-Ansicht: Skalierung desselben Screens, nur Dashboard skalieren oder reduzierter Screen, kein eigener Voll-Screen"): Alle drei dort genannten Wege scheitern an derselben app-weiten Einstellung.

### Variante C — Eigene Handy-App auf denselben Daten ✅ empfohlen

Neue Canvas-App „Tischbuchung Mobil", Hochformat, *Scale to fit* aus, bindet dieselben Listen `Tische` und `Tischbuchungen` an.

- ✅ **Null Risiko für die Desktop-App.** Screen1, Grundriss und Koordinaten bleiben unberührt.
- ✅ Von Grund auf für das Handy gebaut, kein Kompromiss-Layout
- ✅ Klein und übersichtlich: kein Grundriss, keine Mehrfachauswahl, keine Kachelformeln, kurzer Start
- ✅ Passt zu deiner Linie „Problem umgehen statt flicken"
- ✅ Entspricht der Microsoft-Lernmodul-Empfehlung (eine App pro Formfaktor)
- ❌ Buchungslogik existiert zweimal → muss bewusst synchron gehalten werden (siehe Abschnitt 6)
- ❌ Zweiter Link, zweite Freigabe an die Nutzer
- **Aufwand:** ca. 1–2 Arbeitstage für einen sauberen ersten Stand · **Risiko für die laufende App:** keins

**Optional:** Die Desktop-App leitet Handynutzer automatisch weiter. In `Screen1.OnVisible` (nicht in `App.OnStart`):

```
If(
    Host.OSType = "iOS" || Host.OSType = "Android";
    Launch("https://apps.powerapps.com/play/e/<UMGEBUNGS-ID>/a/<APP-ID-MOBIL>"; {}; LaunchTarget.Replace)
)
```

⚠ Ungetestet. Erst bauen, wenn die Handy-App steht. Tablets (iPad) würden dabei ebenfalls weitergeleitet — ggf. zusätzlich `App.Width < 900` prüfen.

---

## 5. Aufbau der Handy-App (Variante C) konkret

### 5.1 Anlegen und Einstellungen

1. Neue Canvas-App „Tischbuchung Mobil", **in derselben Umgebung** wie die Desktop-App.
2. Format: **Phone** — oder Tablet mit benutzerdefiniertem Hochformat. Phone ist der direktere Weg.
3. Einstellungen → Anzeige: **Scale to fit aus**, **Lock orientation an (Hochformat)**.
4. Einstellungen → Updates: moderne Steuerelemente (Fluent 2) aktivieren — sie sind auf Touch ausgelegt.
5. Datenquellen hinzufügen: `Tische`, `Tischbuchungen` (dieselbe SharePoint-Seite). Optional `Office365Users`, falls Namen angezeigt werden.

### 5.2 Struktur: ein Screen, drei Tabs

Bewusst **wie in der Desktop-App** (ein Screen, Tabs per Variable), damit du das Prinzip kennst und Container 1:1 rüberkopieren kannst.

```
scrMobil
└── conRoot                (Vertikaler Auto-Layout-Container, Width = Parent.Width, Height = Parent.Height)
    ├── conHeader          (fixe Höhe ~ 120, Technoform-Blau #171496, App-Titel + Datum + Benutzer-Initialen)
    ├── conInhalt          (FlexibleHeight = true → nimmt den Rest ein, scrollt)
    │   ├── conHeute       (Visible = varTab = "heute")
    │   ├── conBuchen      (Visible = varTab = "buchen")
    │   └── conMeine       (Visible = varTab = "meine")
    └── conTabLeiste       (fixe Höhe ~ 130, unten, drei große Tab-Buttons)
```

**Tab-Leiste unten**, nicht oben: Am Handy wird mit dem Daumen bedient, die untere Bildschirmhälfte ist erreichbar. Das ist das gängige Muster in iOS- und Android-Apps (und in GoBright Mobile).

Mögliche Alternative: drei echte Screens mit `Navigate`. Vorteil: Zurück-Geste des Handys funktioniert natürlicher. Nachteil: Container müssen aufgeteilt werden, Zustand über globale Variablen. Für den ersten Stand: **ein Screen.**

### 5.3 Was in welchen Tab kommt

| Tab | Inhalt | Vorlage aus Desktop-App |
|---|---|---|
| **Heute** (Start-Tab) | Oben eine Karte „Deine Buchung heute": Tisch, Zeit, großer Button **Einchecken** (orange, nur wenn fällig). Darunter Liste aller Tische mit Status frei / belegt / eingecheckt (Farbpunkt + Name). | `conTischBuchungenPanel` + Dashboard-Karte |
| **Buchen** | Datum (Standard heute) → Start/Ende → **Dropdown nur mit freien Tischen** im gewählten Zeitraum → Button „Buchen". Kein Grundriss, deshalb ist der Frei-Filter hier Pflicht, nicht Kür. | `conTischbuchungHinzufügen` (ohne Serie, ohne Mehrfachauswahl) |
| **Meine** | Liste der eigenen kommenden Buchungen, je Zeile Einchecken / Stornieren. Optional Ende verkürzen. | abgewandelter `conBuchungen` / `tabBuchungen` |

**Bewusst weglassen** (Desktop-only): Grundriss, OG/UG-Umschalter, Mehrfachauswahl, Serienbuchung, Detailpopup bei Tischklick, Verlängern-Dialog. Wer das braucht, nimmt den Laptop.

### 5.4 Handy-Bedienung — Best Practices

| Regel | Umsetzung in Power Apps |
|---|---|
| Treffbare Flächen ≥ 44–48 pt | Buttons mindestens ca. 90 px hoch (im Phone-Format, wegen verdoppeltem Koordinatensystem), volle Breite |
| Lesbare Schrift | Fließtext ≥ 24 (Phone-Format), Überschriften 32+ |
| Keine Hover-Effekte | `HoverFill` ist am Handy wirkungslos → Zustand immer über Farbe/Text sichtbar machen, `PressedFill` setzen |
| Eine Spalte | Alles untereinander, nichts nebeneinander außer Zeitpaaren (Start/Ende) |
| Kurze Wege | Häufigste Aktion (Einchecken) direkt auf dem Start-Tab, ein Tipp |
| Wenig Eingabe | Datum standardmäßig heute, Zeiten mit sinnvollen Standardwerten (jetzt gerundet bis 17:00) |
| Rückmeldung | `Notify("Gebucht: OG Desk 5, 08:00–17:00"; NotificationType.Success)` statt Dialog |
| Galerien statt Tabellen | Vertikale Gallery mit `TemplateHeight` ~ 140, Inhalte über `Parent.TemplateWidth` ausrichten |
| Tastatur verdeckt Eingaben | Möglichst keine Texteingabefelder, nur Auswahl |

### 5.5 Performance am Handy

- Mobilnetz statt LAN → **nur laden, was gebraucht wird.** Galerien filtern auf heute bzw. ab heute: `Filter(Tischbuchungen; Endzeit >= Today())` statt ganzer Liste.
- Keine Grundriss-Bilder, keine Koordinaten-Collections → die Handy-App startet von Natur aus schneller.
- `App.OnStart` schlank halten; Werte, die sich ableiten lassen, als **Named Formulas** in `App.Formulas` (z. B. `MeineMail = User().Email;`).
- Delegierungswarnungen ernst nehmen (`Now()`/`DateAdd` in `LookUp` sind nicht delegierbar, siehe Master-Bedingung). Bei kleiner Liste unkritisch, solange der Aufräum-Flow läuft.

---

## 6. Das eigentliche Risiko: doppelte Logik

Zwei Apps schreiben in dieselbe Liste `Tischbuchungen`. SharePoint selbst verhindert **keine** Überschneidungen. Der Schutz vor Doppelbuchungen liegt allein in den App-Formeln.

**Daraus folgen drei Regeln:**

1. **Die Doppelbuchungsprüfung muss in beiden Apps wortgleich sein** — dieselbe Lehre wie bei der Master-Bedingung („an 6 Stellen wortgleich"), jetzt app-übergreifend. Direkt vor jedem `Patch` frisch gegen SharePoint prüfen, nicht gegen eine Collection.
2. **Status-Logik (frei/fällig/eingecheckt, 30-Minuten-Regel) wortgleich übernehmen.** Sonst zeigt das Handy „frei", der Desktop „belegt".
3. **In `KONTEXT.md` für Claude Code einen Abschnitt „Geteilte Regeln" anlegen**, mit der jeweils gültigen Formel. Jede Änderung an einer dieser Formeln = Änderung in beiden Apps.

Die Handy-App braucht **nicht** die optimierte Mehrfach-Speicherlogik aus dem Briefing vom 06.10. — sie bucht immer genau einen Eintrag. Das verkleinert die doppelte Logik erheblich.

---

## 7. Steuerelemente aus der Desktop-App übernehmen

- **Kopieren zwischen Apps:** Beide Apps im Studio in zwei Browser-Tabs öffnen, Container in der Strukturansicht markieren, `Strg+C`, im anderen Tab `Strg+V`. Alternativ Rechtsklick → **Code anzeigen** (YAML) → kopieren → einfügen. Der Browser braucht Zwischenablage-Rechte für `make.powerapps.com`.
- **Vorher** in der Handy-App die Datenquellen hinzufügen, sonst landen beim Einfügen sofort Fehler in jeder Formel.
- **Nach dem Einfügen** prüfen: Alle Verweise auf Variablen aus der Desktop-`OnStart` (`varAusgewaehltesStockwerk`, `varAnsichtsDatum`, `colTischPositionen` …) existieren in der Handy-App nicht → entfernen oder neu definieren.
- **Koordinaten:** Eingefügte Steuerelemente haben feste X/Y/Width aus dem 1920er-Desktop-Raster. Im Auto-Layout-Container werden X/Y ignoriert, Breiten müssen auf `Parent.Width` umgestellt werden.
- Ehrlich: Bei Panels mit vielen festen Koordinaten ist **neu aufbauen und nur die Formeln kopieren** oft schneller als Gestalt-Reparatur.

---

## 8. Verteilung an die Nutzer

| Weg | Wie | Empfehlung |
|---|---|---|
| Link im Browser | `apps.powerapps.com/play/e/<env>/a/<app>` per Mail/Intranet, Nutzer legt Lesezeichen auf Startbildschirm | Einfachster Start, keine Installation |
| Power Apps Mobile | Store-App installieren, App in der Liste antippen, „Pin to Home" (Android) bzw. iOS-Kurzbefehl | Bestes Erlebnis, setzt Installation voraus |
| Teams | App als Teams-App/Tab hinzufügen | Wenn Teams auf allen Diensthandys ist |
| QR-Code-Aushang | QR mit dem Link an Eingang/Tischen | Siehe Abschnitt 10 |

- App mit derselben Gruppe teilen wie die Desktop-App. Falls dafür Rechte fehlen → Michael.
- Nach dem Veröffentlichen kann die Power-Apps-Mobile-App die alte Version noch eine Weile aus dem Cache zeigen.

---

## 9. Testen

1. **Browser-Geräteemulation:** Veröffentlichte App im Edge/Chrome öffnen, `F12` → `Strg+Umschalt+M` → iPhone/Pixel wählen. Schnellster Test ohne Handy. `Host.OSType` meldet dann „iOS"/„Android" — gut, um die Weiterleitung zu testen.
2. **Studio-Vorschau** zeigt Responsivität nur eingeschränkt — nicht darauf verlassen.
3. **Echte Geräte:** mindestens ein iPhone und ein Android, jeweils Browser **und** Power Apps Mobile.
4. Während der Entwicklung ein unsichtbares Debug-Label mit `Host.OSType & " · " & App.Width & "×" & App.Height & " · " & Host.Version` einbauen.
5. Kreuztest Doppelbuchung: am Desktop Tisch X für 10–12 Uhr buchen, gleichzeitig am Handy denselben Tisch 11–13 Uhr versuchen → muss abgewiesen werden.

---

## 10. Über den Auftrag hinaus: QR-Check-in am Tisch

Der stärkste Grund für eine Handy-App ist das Einchecken. GoBright löst das über Codes am Tisch. In Power Apps geht das ohne Scanner-Control:

- Pro Tisch einen QR-Code drucken mit dem Link `https://apps.powerapps.com/play/e/<env>/a/<app>?tisch=OG%20Desk%205`
- Die normale Handykamera öffnet den Link → die Handy-App startet.
- In der App: `Param("tisch")` auslesen. Hat der Nutzer für diesen Tisch eine fällige Buchung → direkt Check-in-Karte zeigen. Ist der Tisch frei → „Jetzt bis 17:00 buchen?" anbieten.
- **Warum nicht das Barcode-Reader-Control?** Es funktioniert laut Microsoft **nicht im Browser**, nur in Power Apps Mobile. Der Deep-Link-Weg funktioniert überall.
- `Param()` ist in `App.StartScreen` und `OnStart` verfügbar.

Das ist kein Muss für den ersten Stand, aber es sollte von Anfang an mitgedacht werden (Tab „Heute" muss einen „Tisch aus Link"-Zustand vertragen).

---

## 11. Vorgeschlagene Reihenfolge

| # | Schritt | Wer |
|---|---|---|
| 1 | In „Tischbuchung" die Anzeige-Einstellungen nachsehen und notieren (Scale to fit, Seitenverhältnis, Lock) | Josias |
| 2 | Entscheidung Variante C bestätigen | Josias |
| 3 | Leere App „Tischbuchung Mobil" anlegen, Einstellungen wie 5.1, Datenquellen | Josias |
| 4 | Gerüst `conRoot` / Header / Tab-Leiste / drei leere Tabs | Claude Code liefert Formeln, Josias fügt ein |
| 5 | Tab „Meine" (nur lesen) → schnellster sichtbarer Erfolg | Claude Code / Josias |
| 6 | Tab „Heute" inkl. Einchecken — Status-Formel wortgleich aus Desktop | Claude Code / Josias |
| 7 | Tab „Buchen" mit Frei-Filter und Doppelbuchungsprüfung | Claude Code / Josias |
| 8 | Test nach Abschnitt 9, dann Freigabe an Testgruppe (Julia) | Josias |
| 9 | Später: QR-Check-in, Weiterleitung aus der Desktop-App | — |

---

## 12. Offene Fragen

1. Wie öffnen die Kollegen die App am Handy: Browser, Power Apps Mobile oder Teams? (Beeinflusst Verteilung und ob QR-Check-in sinnvoll ist.)
2. Gibt es Dienst- oder nur Privathandys? (Bei Privathandys ist der Browser-Link die niedrigste Hürde.)
3. Soll die Handy-App auch Buchungen für andere Tage als heute können oder nur „heute"? (Nur heute = noch kleiner, noch schneller fertig.)

---

## Quellen

- [Microsoft Learn — Create responsive layouts in canvas apps](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout)
- [Microsoft Learn — Responsive design guidelines](https://learn.microsoft.com/en-us/power-apps/guidance/coding-guidelines/responsive-design-guidelines)
- [Microsoft Learn — Change screen size and orientation](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/set-aspect-ratio-portrait-landscape)
- [Microsoft Learn Training — Build for phones or tablets](https://learn.microsoft.com/en-us/training/modules/how-to-build-ui-canvas-app/6-use-table-phone-form-factors)
- [Microsoft Learn — Host object](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/object-host)
- [Microsoft Learn — App object (StartScreen, Formulas)](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/object-app)
- [Microsoft Learn — Run apps on Power Apps mobile](https://learn.microsoft.com/en-us/power-apps/mobile/run-powerapps-on-mobile)
- [Microsoft Learn — Run an app in a web browser](https://learn.microsoft.com/power-apps/user/run-app-browser)
- [Microsoft Learn — Barcode reader control](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-barcodereader)
- [Microsoft Learn — Code view (YAML kopieren/einfügen)](https://learn.microsoft.com/power-apps/maker/canvas-apps/code-view)
- [Tom Riha — How to check if Power App runs on mobile or desktop](https://tomriha.com/how-to-check-if-power-app-runs-on-mobile-or-desktop/)
- [Manuel T. Gomes — Power Apps: Mobile usage](https://manueltgomes.com/microsoft/power-apps-mobile-usage)
