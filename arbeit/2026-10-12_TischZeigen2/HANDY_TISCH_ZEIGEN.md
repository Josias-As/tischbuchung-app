# Handy „Tisch zeigen“: alle Properties (12.10.2026)

Für den Handy-Chat. Grundlage ist der **echte Handy-Export 12.10. 12:05** („handy echt“). Jeder Diff rechnet gegen diesen Export. Erzeugt und geprüft mit `werkzeuge/handy_tisch_zeigen.py`, die Daten mit `werkzeuge/tisch_zeigen_v2.py`. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Achtung, Export verwechselt (belegt):** `handytischbuchungegrundrisseinbauen12.10.` enthält die **Desktop-App** „Tischbuchung“. Sie hat dieselbe App-ID und ist zeichengleich mit dem Desktop-Export 11:52. Der echte Handy-Export ist `handy echt 12.10.` (12:05). Gegen den rechnet dieses Dokument.
- **Stand Handy-Export (belegt):**
  - `lblTischH.Width` ist korrigiert (`Parent.Width - 360`).
  - **H8 ist nur zu drei Vierteln drin:** `tmrJetzt`, `ddDatum.Items` und `lblHeuteTitel.Text` ja, **`App.OnStart` nein**. Damit ist `varHeute` beim Start leer.
  - Folge: Beim ersten Timer-Takt, etwa 1 Minute nach dem Start, setzt die App `ddDatum` zurück und lädt die Listen neu. Wer in dieser Minute „Morgen“ gewählt hat, steht plötzlich auf „Heute“.
  - **T0 holt das nach.** Der Block ist zeichengleich mit H8, die Vorher-Fassung passt zum Export (maschinell geprüft).
- **Daten gegengeprüft (belegt):**
  - Ich habe alle 35 Tische aus dem Desktop-Export 11:52 und der REST-Reihenfolge unabhängig nachgerechnet. Ergebnis: **0 Abweichungen** zur `tabelle_handy_de.txt`.
  - Jedes Rechteck liegt in `handy_plan_OG/UG.jpg` auf seinem Tisch (Überlagerung, `pruef_overlay_*.png`).
  - Meine Tabelle vom Vormittag (`tabelle_hoch_de.txt`) war für OG 6–13 falsch, weil ich die falsche Reihenfolge angenommen hatte. Sie ist überholt.
- **Aufbau wie vorgeschlagen, mit drei Verbesserungen:**
  1. **Eine** benannte Formel `TischPlan` als Datensatz (`Farbe`, `Fuellung`, `Tische`).
     - Es gibt nur eine Formel, also braucht es **kein Trennzeichen**. Die Frage nach `;` oder `;;` (T-U2) entfällt.
     - Die Farbe ändert man **an einer Stelle**: `Farbe` und `Fuellung` in `App.Formulas`. Vorgabe ist Orange.
  2. Ein **Vollbild-Hintergrundknopf** `btnTischPlanHintergrund` hinter dem Plan.
     - Er fängt alle Klicks ab, damit darunter nichts bedienbar ist. Ein Container allein fängt keine Klicks.
     - Ein Tipp daneben schließt den Plan.
  3. Der Knopf ist in beiden Karten so gesetzt, dass er nichts überlappt. Dafür werden `lblZeitH` und `lblZeitM` etwas schmaler (maschinell geprüft bei Layoutbreite 640).
- **Aufklappen in der Karte: weiterhin nein.**
  - Die Karten haben feste Höhen (`TemplateSize` 300 und 260, belegt). Aufklappen hieße eine Galerie mit variabler Höhe und ein Bild je Karte.
  - Das Overlay rendert genau **ein** Bild, nur wenn es offen ist.
- **Umfang:** 6 Schritte, 123 Properties, 8 neue Steuerelemente. **0 SharePoint-Abfragen** durch das Feature (maschinell geprüft). Maschinell 0 Fehler, in Studio nichts getestet. Nicht unabhängig geprüft.

## 1. Vorbereitung (vor T1)
1. Sicherung: Datei → Speichern unter → Dieser Computer (`.msapp`).
2. **Bilder hochladen:** Medien → Hochladen → `handy_plan_OG.jpg` und `handy_plan_UG.jpg`. In der Medienliste müssen sie **`handy_plan_OG`** und **`handy_plan_UG`** heißen. Sonst bleibt `imgTischPlan.Image` rot.
3. Reihenfolge: T0 → T1 → T2 → T3 → T4 → T5. Nach jedem Schritt die App-Prüfung ansehen: keine roten Fehler.

## 2. Schritte

**Neue Steuerelemente:**

| Name | Typ | liegt in | Schritt |
|---|---|---|---|
| `btnTischZeigenH` | Schaltfläche (klassisch) | `conKarteH` | T2 |
| `btnTischZeigenM` | Schaltfläche (klassisch) | `conKarteM` | T3 |
| `btnTischPlanHintergrund` | Schaltfläche (klassisch) | `Screen1` | T4 |
| `conTischPlan` | Container (Layout → Container) | `Screen1` | T4 |
| `lblTischPlanTitel` | Textbeschriftung | `conTischPlan` | T4 |
| `imgTischPlan` | Bild (Medien → Bild) | `conTischPlan` | T4 |
| `recTischMarke` | Rechteck (Formen → Rechteck) | `conTischPlan` | T4 |
| `btnTischPlanSchliessen` | Schaltfläche (klassisch) | `conTischPlan` | T4 |

### T0 H8 vervollständigen: varHeute beim Start

Nur die Zeile `Set(varHeute; Today());;` kommt dazu. Der Rest ist der Export (Diff).

**Test:**
1. App neu öffnen (Vorschau neu starten).
2. Sofort im Tab „Buchen“ „Morgen“ wählen und 70 Sekunden warten. Die Auswahl bleibt auf „Morgen“.

#### `App.OnStart`

Ort: `App` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1,2 +1,2 @@
-Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische);;
+Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varHeute; Today());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische);;
 Set(
```

```
Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varHeute; Today());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische);;
Set(
  varProfilFarbe;
  Switch(
    RandBetween(1; 8);
    1; ColorValue("#8CAFF4");
    2; ColorValue("#82C7B3");
    3; ColorValue("#EFA897");
    4; ColorValue("#B59EDC");
    5; ColorValue("#82CCC5");
    6; ColorValue("#F5C295");
    7; ColorValue("#A1AADB");
    ColorValue("#A1B1BA")
  )
)
```

### T1 Daten: benannte Formel TischPlan

**Einfügen:** `App` markieren → Property **`Formulas`** → den ganzen Block einfügen. Die Property ist im Export leer.
- Ist `Formulas` in Studio nicht auswählbar, die App-Einstellung „Benannte Formeln“ prüfen. In der Desktop-App laufen benannte Formeln mit denselben App-Einstellungen (belegt).

**Farbe ändern:** nur hier.
- `Farbe` ist der Rand.
- `Fuellung` ist dieselbe Farbe mit Transparenz: Der letzte Wert 0,3 heißt 30 % deckend, die Tischnummer bleibt lesbar.

**Test:** Die App-Prüfung zeigt an `App.Formulas` nichts Rotes.

#### `App.Formulas`

Ort: `App` · **neu setzen**

```
TischPlan = {
  Farbe: RGBA(255; 140; 0; 1);
  Fuellung: RGBA(255; 140; 0; 0,3);
  Tische:
  Table(
    {Tisch: "OG Desk 1"; Geschoss: "OG"; X: 0,7625; Y: 0,7333; B: 0,1403; H: 0,0333};
    {Tisch: "OG Desk 2"; Geschoss: "OG"; X: 0,7886; Y: 0,8717; B: 0,0833; H: 0,0561};
    {Tisch: "OG Desk 3"; Geschoss: "OG"; X: 0,7884; Y: 0,9289; B: 0,0833; H: 0,0561};
    {Tisch: "OG Desk 4"; Geschoss: "OG"; X: 0,702; Y: 0,8717; B: 0,0833; H: 0,0561};
    {Tisch: "OG Desk 5"; Geschoss: "OG"; X: 0,7018; Y: 0,9289; B: 0,0833; H: 0,0561};
    {Tisch: "OG Desk 6"; Geschoss: "OG"; X: 0,4197; Y: 0,93; B: 0,0833; H: 0,0561};
    {Tisch: "OG Desk 7"; Geschoss: "OG"; X: 0,3334; Y: 0,93; B: 0,0833; H: 0,0561};
    {Tisch: "OG Desk 8"; Geschoss: "OG"; X: 0,4501; Y: 0,8; B: 0,1403; H: 0,0333};
    {Tisch: "OG Desk 9"; Geschoss: "OG"; X: 0,3082; Y: 0,8; B: 0,1403; H: 0,0333};
    {Tisch: "OG Desk 10"; Geschoss: "OG"; X: 0,1647; Y: 0,8; B: 0,1403; H: 0,0333};
    {Tisch: "OG Desk 11"; Geschoss: "OG"; X: 0,4512; Y: 0,8333; B: 0,1403; H: 0,0333};
    {Tisch: "OG Desk 12"; Geschoss: "OG"; X: 0,308; Y: 0,8333; B: 0,1403; H: 0,0333};
    {Tisch: "OG Desk 13"; Geschoss: "OG"; X: 0,1644; Y: 0,8333; B: 0,1403; H: 0,0333};
    {Tisch: "Quiet Desk 3"; Geschoss: "OG"; X: 0,1537; Y: 0,45; B: 0,1306; H: 0,0278};
    {Tisch: "Quiet Desk 2"; Geschoss: "OG"; X: 0,2798; Y: 0,45; B: 0,1306; H: 0,0278};
    {Tisch: "Quiet Desk 1"; Geschoss: "OG"; X: 0,406; Y: 0,45; B: 0,1306; H: 0,0278};
    {Tisch: "UG Desk 1"; Geschoss: "UG"; X: 0,3319; Y: 0,2611; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 2"; Geschoss: "UG"; X: 0,2081; Y: 0,2611; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 3"; Geschoss: "UG"; X: 0,3314; Y: 0,29; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 4"; Geschoss: "UG"; X: 0,2076; Y: 0,29; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 5"; Geschoss: "UG"; X: 0,3309; Y: 0,3767; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 6"; Geschoss: "UG"; X: 0,2071; Y: 0,3767; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 7"; Geschoss: "UG"; X: 0,3318; Y: 0,4056; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 8"; Geschoss: "UG"; X: 0,208; Y: 0,4056; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 9"; Geschoss: "UG"; X: 0,3313; Y: 0,5283; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 10"; Geschoss: "UG"; X: 0,2075; Y: 0,5283; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 11"; Geschoss: "UG"; X: 0,3308; Y: 0,5572; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 12"; Geschoss: "UG"; X: 0,207; Y: 0,5572; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 13"; Geschoss: "UG"; X: 0,7567; Y: 0,6344; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 14"; Geschoss: "UG"; X: 0,6316; Y: 0,6344; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 16"; Geschoss: "UG"; X: 0,6312; Y: 0,6639; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 15"; Geschoss: "UG"; X: 0,7565; Y: 0,6639; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 17"; Geschoss: "UG"; X: 0,756; Y: 0,7222; B: 0,1236; H: 0,0289};
    {Tisch: "UG Desk 18"; Geschoss: "UG"; X: 0,7557; Y: 0,75; B: 0,1236; H: 0,0289};
    {Tisch: "Big Table"; Geschoss: "UG"; X: 0,2791; Y: 0,6633; B: 0,0722; H: 0,1222}
  )
}
```

### T2 Knopf in der Karte „Heute“

**Neu anlegen:**
1. `galHeute` → Vorlage der ersten Karte → **`conKarteH`** markieren.
2. Einfügen → Schaltfläche (klassisch).
3. Umbenennen in **`btnTischZeigenH`**. Er muss **in** `conKarteH` liegen.

Lage: rechts neben der Uhrzeit, unter dem Status (X wie „Verwalten“ in „Meine“, 200 breit, Y 80–130). Die Knöpfe „Einchecken“ und „Verwalten“ beginnen bei Y 150. `lblZeitH` wird 220 schmaler. Bei Layout 640 bleiben etwa 316 für „hh:mm bis hh:mm“, gebraucht werden etwa 290 (geschätzt, siehe Selbstprüfung).

#### `btnTischZeigenH.Text`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
"Tisch zeigen"
```

#### `btnTischZeigenH.X`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
Parent.Width - 228
```

#### `btnTischZeigenH.Y`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
80
```

#### `btnTischZeigenH.Width`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
200
```

#### `btnTischZeigenH.Height`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
50
```

#### `btnTischZeigenH.Size`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
20
```

#### `btnTischZeigenH.Font`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
Font.'Open Sans'
```

#### `btnTischZeigenH.FontWeight`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
FontWeight.Semibold
```

#### `btnTischZeigenH.Fill`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `btnTischZeigenH.Color`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenH.BorderColor`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenH.BorderThickness`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
2
```

#### `btnTischZeigenH.HoverFill`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `btnTischZeigenH.HoverColor`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenH.PressedFill`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(232; 232; 245; 1)
```

#### `btnTischZeigenH.PressedColor`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenH.RadiusTopLeft`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
12
```

#### `btnTischZeigenH.RadiusTopRight`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
12
```

#### `btnTischZeigenH.RadiusBottomLeft`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
12
```

#### `btnTischZeigenH.RadiusBottomRight`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
12
```

#### `btnTischZeigenH.AccessibleLabel`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
"Tisch " & ThisItem.Tisch.Value & " im Grundriss zeigen"
```

#### `btnTischZeigenH.OnSelect`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnTischZeigenH` · **neu setzen**

```
Set(varTischBild; LookUp(TischPlan.Tische; Tisch = ThisItem.Tisch.Value));;
If(
  IsBlank(varTischBild.Tisch);
  Notify("Für diesen Tisch gibt es noch keinen Plan."; NotificationType.Warning);
  Set(varZeigeTisch; true)
)
```

#### `lblZeitH.Width`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > lblZeitH` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Parent.Width - 56
+Parent.Width - 276
```

```
Parent.Width - 276
```

### T3 Knopf in der Karte „Meine“

**Neu anlegen:**
1. `galMeine` → Vorlage der ersten Karte → **`conKarteM`** markieren.
2. Einfügen → Schaltfläche (klassisch).
3. Umbenennen in **`btnTischZeigenM`**.

Lage: rechts unter „Verwalten“ (Y 176–224, Kartenhöhe 236). `lblZeitM` wird 10 schmaler, damit es den Knopf nicht berührt.

#### `btnTischZeigenM.Text`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
"Tisch zeigen"
```

#### `btnTischZeigenM.X`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
Parent.Width - 228
```

#### `btnTischZeigenM.Y`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
176
```

#### `btnTischZeigenM.Width`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
200
```

#### `btnTischZeigenM.Height`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
48
```

#### `btnTischZeigenM.Size`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
20
```

#### `btnTischZeigenM.Font`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
Font.'Open Sans'
```

#### `btnTischZeigenM.FontWeight`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
FontWeight.Semibold
```

#### `btnTischZeigenM.Fill`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `btnTischZeigenM.Color`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenM.BorderColor`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenM.BorderThickness`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
2
```

#### `btnTischZeigenM.HoverFill`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `btnTischZeigenM.HoverColor`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenM.PressedFill`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(232; 232; 245; 1)
```

#### `btnTischZeigenM.PressedColor`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
RGBA(23; 20; 150; 1)
```

#### `btnTischZeigenM.RadiusTopLeft`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
12
```

#### `btnTischZeigenM.RadiusTopRight`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
12
```

#### `btnTischZeigenM.RadiusBottomLeft`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
12
```

#### `btnTischZeigenM.RadiusBottomRight`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
12
```

#### `btnTischZeigenM.AccessibleLabel`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
"Tisch " & ThisItem.Tisch.Value & " im Grundriss zeigen"
```

#### `btnTischZeigenM.OnSelect`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > btnTischZeigenM` · **neu setzen**

```
Set(varTischBild; LookUp(TischPlan.Tische; Tisch = ThisItem.Tisch.Value));;
If(
  IsBlank(varTischBild.Tisch);
  Notify("Für diesen Tisch gibt es noch keinen Plan."; NotificationType.Warning);
  Set(varZeigeTisch; true)
)
```

#### `lblZeitM.Width`

Ort: `Screen1 > conRoot > conInhalt > conMeine > galMeine > conKarteM > lblZeitM` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Parent.Width - 250
+Parent.Width - 260
```

```
Parent.Width - 260
```

### T4 Overlay mit Plan (neu)

**Neu anlegen, Namen exakt so, in dieser Reihenfolge:**
1. `Screen1` markieren → Einfügen → Schaltfläche (klassisch) → **`btnTischPlanHintergrund`**.
2. `Screen1` markieren → Einfügen → Layout → **Container** → **`conTischPlan`**.
3. `conTischPlan` markieren → Einfügen → Textbeschriftung → **`lblTischPlanTitel`**.
4. `conTischPlan` markieren → Einfügen → Medien → Bild → **`imgTischPlan`**.
5. `conTischPlan` markieren → Einfügen → Formen → Rechteck → **`recTischMarke`**. Es muss in der Strukturansicht **über** `imgTischPlan` liegen.
6. `conTischPlan` markieren → Einfügen → Schaltfläche (klassisch) → **`btnTischPlanSchliessen`**.
7. **Ebenen:** `conLadeOverlay` markieren → Neu anordnen → **Ganz nach vorne**. Danach ist die Reihenfolge der `Screen1`-Kinder von unten nach oben:
   - `conRoot`, `tmrJetzt`, `conDlgHintergrund`, `conDlgVerwalten`, `conDlgStorno`
   - `btnTischPlanHintergrund`, `conTischPlan`
   - `conLadeOverlay`

**Warum diese Ebenen:**
- Der Plan liegt über den Dialogen. Er kann aber nie zusammen mit ihnen offen sein: Der Hintergrundknopf deckt alles ab, und die Tab-Knöpfe schließen beides (T5).
- Das Lade-Overlay bleibt ganz oben. „Aktualisieren“ schließt den Plan vorher (T5).

**Größe (geschlussfolgert, Layout 640 × 1136 hochkant, belegt):**
- Bildhöhe = Platz zwischen Titel und Schließen-Knopf, höchstens Breite × 2,5. Breite = Höhe ÷ 2,5.
- Bei 640 × 1136 ist das etwa 812 × 325. Ein Tisch ist dann etwa 27 × 45 bis 45 × 27 Einheiten groß.
- Auf kleineren und größeren Handys passt sich das an, weil alles über `Parent` rechnet. Die Anteile gelten genau, weil das Bild kein Rand hat (Seitenverhältnis 2,5 geprüft).

#### `btnTischPlanHintergrund.Text`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
""
```

#### `btnTischPlanHintergrund.X`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.Y`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.Width`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
Parent.Width
```

#### `btnTischPlanHintergrund.Height`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
Parent.Height
```

#### `btnTischPlanHintergrund.Fill`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
RGBA(0; 0; 0; 0,45)
```

#### `btnTischPlanHintergrund.HoverFill`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
RGBA(0; 0; 0; 0,45)
```

#### `btnTischPlanHintergrund.PressedFill`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
RGBA(0; 0; 0; 0,45)
```

#### `btnTischPlanHintergrund.BorderThickness`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.FocusedBorderThickness`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.TabIndex`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
-1
```

#### `btnTischPlanHintergrund.RadiusTopLeft`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.RadiusTopRight`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.RadiusBottomLeft`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.RadiusBottomRight`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
0
```

#### `btnTischPlanHintergrund.Visible`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
varZeigeTisch
```

#### `btnTischPlanHintergrund.OnSelect`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
Set(varZeigeTisch; false)
```

#### `btnTischPlanHintergrund.AccessibleLabel`

Ort: `Screen1 > btnTischPlanHintergrund` · **neu setzen**

```
"Plan schließen"
```

#### `conTischPlan.X`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
20
```

#### `conTischPlan.Y`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
40
```

#### `conTischPlan.Width`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
Parent.Width - 40
```

#### `conTischPlan.Height`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
Parent.Height - 80
```

#### `conTischPlan.Fill`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `conTischPlan.RadiusTopLeft`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
28
```

#### `conTischPlan.RadiusTopRight`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
28
```

#### `conTischPlan.RadiusBottomLeft`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
28
```

#### `conTischPlan.RadiusBottomRight`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
28
```

#### `conTischPlan.Visible`

Ort: `Screen1 > conTischPlan` · **neu setzen**

```
varZeigeTisch
```

#### `lblTischPlanTitel.Text`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
varTischBild.Tisch & "  ·  " & If(varTischBild.Geschoss = "OG"; "Obergeschoss"; "Untergeschoss")
```

#### `lblTischPlanTitel.X`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
28
```

#### `lblTischPlanTitel.Y`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
20
```

#### `lblTischPlanTitel.Width`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
Parent.Width - 56
```

#### `lblTischPlanTitel.Height`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
60
```

#### `lblTischPlanTitel.Size`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
22
```

#### `lblTischPlanTitel.Font`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
Font.'Open Sans'
```

#### `lblTischPlanTitel.FontWeight`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
FontWeight.Semibold
```

#### `lblTischPlanTitel.Color`

Ort: `Screen1 > conTischPlan > lblTischPlanTitel` · **neu setzen**

```
RGBA(32; 54; 71; 1)
```

#### `imgTischPlan.Image`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
If(varTischBild.Geschoss = "OG"; handy_plan_OG; handy_plan_UG)
```

#### `imgTischPlan.Height`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
Min(Parent.Height - 244; (Parent.Width - 40) * 2,5)
```

#### `imgTischPlan.Width`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
Self.Height / 2,5
```

#### `imgTischPlan.X`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
(Parent.Width - Self.Width) / 2
```

#### `imgTischPlan.Y`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
96
```

#### `imgTischPlan.ImagePosition`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
ImagePosition.Fit
```

#### `imgTischPlan.AccessibleLabel`

Ort: `Screen1 > conTischPlan > imgTischPlan` · **neu setzen**

```
"Grundriss " & If(varTischBild.Geschoss = "OG"; "Obergeschoss"; "Untergeschoss") & ", " & varTischBild.Tisch & " ist markiert"
```

#### `recTischMarke.X`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
imgTischPlan.X + varTischBild.X * imgTischPlan.Width
```

#### `recTischMarke.Y`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
imgTischPlan.Y + varTischBild.Y * imgTischPlan.Height
```

#### `recTischMarke.Width`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
varTischBild.B * imgTischPlan.Width
```

#### `recTischMarke.Height`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
varTischBild.H * imgTischPlan.Height
```

#### `recTischMarke.Fill`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
TischPlan.Fuellung
```

#### `recTischMarke.BorderColor`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
TischPlan.Farbe
```

#### `recTischMarke.BorderThickness`

Ort: `Screen1 > conTischPlan > recTischMarke` · **neu setzen**

```
6
```

#### `btnTischPlanSchliessen.Text`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
"Schließen"
```

#### `btnTischPlanSchliessen.X`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
36
```

#### `btnTischPlanSchliessen.Y`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
Parent.Height - 124
```

#### `btnTischPlanSchliessen.Width`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
Parent.Width - 72
```

#### `btnTischPlanSchliessen.Height`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
100
```

#### `btnTischPlanSchliessen.Size`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
26
```

#### `btnTischPlanSchliessen.Font`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
Font.'Open Sans'
```

#### `btnTischPlanSchliessen.Fill`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `btnTischPlanSchliessen.Color`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(90; 90; 90; 1)
```

#### `btnTischPlanSchliessen.BorderColor`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(190; 190; 190; 1)
```

#### `btnTischPlanSchliessen.HoverFill`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(255; 255; 255; 1)
```

#### `btnTischPlanSchliessen.HoverColor`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(90; 90; 90; 1)
```

#### `btnTischPlanSchliessen.PressedFill`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(240; 240; 240; 1)
```

#### `btnTischPlanSchliessen.PressedColor`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
RGBA(90; 90; 90; 1)
```

#### `btnTischPlanSchliessen.RadiusTopLeft`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
16
```

#### `btnTischPlanSchliessen.RadiusTopRight`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
16
```

#### `btnTischPlanSchliessen.RadiusBottomLeft`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
16
```

#### `btnTischPlanSchliessen.RadiusBottomRight`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
16
```

#### `btnTischPlanSchliessen.OnSelect`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
Set(varZeigeTisch; false)
```

#### `btnTischPlanSchliessen.AccessibleLabel`

Ort: `Screen1 > conTischPlan > btnTischPlanSchliessen` · **neu setzen**

```
"Plan schließen"
```

### T5 Schließen beim Tab-Wechsel und Aktualisieren

Nur `Set(varZeigeTisch; false);;` vorne. Der Rest ist der Export (maschinell geprüft).

#### `btnTabHeute.OnSelect`

Ort: `Screen1 > conRoot > conTabLeiste > btnTabHeute` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1 +1,2 @@
+Set(varZeigeTisch; false);;
 Set(varTab; "heute");;
```

```
Set(varZeigeTisch; false);;
Set(varTab; "heute");;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

#### `btnTabBuchen.OnSelect`

Ort: `Screen1 > conRoot > conTabLeiste > btnTabBuchen` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1 +1,2 @@
+Set(varZeigeTisch; false);;
 Set(varTab; "buchen");;
```

```
Set(varZeigeTisch; false);;
Set(varTab; "buchen");;
Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

#### `btnTabMeine.OnSelect`

Ort: `Screen1 > conRoot > conTabLeiste > btnTabMeine` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1 +1,2 @@
+Set(varZeigeTisch; false);;
 Set(varTab; "meine");;
```

```
Set(varZeigeTisch; false);;
Set(varTab; "meine");;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

#### `icoAktualisieren_1.OnSelect`

Ort: `Screen1 > conRoot > conHeader > icoAktualisieren_1` · **ganze Property ersetzen**

Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):

```diff
@@ -1 +1,2 @@
+Set(varZeigeTisch; false);;
 Set(varIsLoading; true);;
```

```
Set(varZeigeTisch; false);;
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Refresh(Tische);;
ClearCollect(colTische; Tische);;
Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Set(varNeuLaden; varNeuLaden + 1);;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

## 3. Testablauf
Vorher: T0–T5 eingefügt, Bilder hochgeladen, App-Prüfung ohne rote Fehler. Vorschau, dann am echten Handy.

| ✓ | Test | Erwartung |
|---|---|---|
| ☐ | 1 Eigene Buchungen anlegen, nacheinander (keine zwei Tische zur selben Zeit): **OG Desk 3**, **Quiet Desk 1**, **UG Desk 14**, **UG Desk 18**. **Big Table** am PC über den Grundriss buchen, weil die Handy-App ihn nicht anbietet | Alle stehen unter „Meine“ (und unter „Heute“, wenn heute) |
| ☐ | 2 Bei jeder Buchung **„Tisch zeigen“** | Plan des richtigen Geschosses, hochkant. Titel z. B. „OG Desk 3 · Obergeschoss“. Das orange Rechteck liegt **genau** auf dem Tisch mit der Nummer. Kein anderer Tisch ist markiert |
| ☐ | 3 Schließen über „Schließen“, über einen Tipp neben den Plan, über einen Tab-Knopf | Der Plan ist zu, die App ist normal bedienbar |
| ☐ | 4 OG-Buchung zeigen, schließen, dann UG-Buchung zeigen | Das Bild wechselt aufs UG, das Rechteck sitzt richtig. Kein Rest vom OG |
| ☐ | 5 Plan offen: Die Kopfzeile mit „Aktualisieren“ ist abgedeckt, ein Tipp dort schließt nur den Plan. Danach „Aktualisieren“ | „Aktualisiert.“, der Plan bleibt zu |
| ☐ | 6 Plan offen, auf „Verwalten“ einer Karte tippen geht nicht, weil der Hintergrund abdeckt | kein Verwalten-Dialog unter dem Plan |
| ☐ | 7 Karten ansehen | „Tisch zeigen“ überlappt weder Status, Uhrzeit noch Knöpfe. Die Uhrzeit ist vollständig lesbar |
| ☐ | 8 Kleines Handy (z. B. iPhone SE) und großes Handy | Der Plan passt ganz auf den Bildschirm, „Schließen“ ist sichtbar, das Rechteck sitzt |
| ☐ | 9 Monitor (optional): „Tisch zeigen“ und Schließen | **keine** `getRows` |
| ☐ | 10 T0: App neu öffnen, „Morgen“ wählen, 70 s warten | bleibt „Morgen“ |
| ☐ | 11 Testbuchungen stornieren, veröffentlichen, Sicherung | |

## 4. UNSICHER
| Nr | Was | Prüfen |
|---|---|---|
| H-U1 | Benannte Formel als Datensatz mit `Table` in der Handy-App (`App.Formulas` ist dort neu). Die Desktop-App nutzt `App.Formulas` mit **denselben App-Einstellungen** (`AppPreviewFlagsMap` gleich, belegt), ein Datensatz mit Tabelle als benannte Formel ist dort aber nicht belegt | App-Prüfung nach T1. Wenn rot: dasselbe als `Set(varTischPlan; { … })` am Ende von `App.OnStart` und in den Formeln `TischPlan` durch `varTischPlan` ersetzen. Dann melden, ich erzeuge die Blöcke neu |
| H-U2 | Medienname nach dem Hochladen genau `handy_plan_OG`/`handy_plan_UG` | Test 2 |
| H-U3 | Tippen auf `btnTischPlanHintergrund` über den Galerien wird abgefangen (klassische Schaltfläche, Muster wie Desktop `btnHitArea`) | Test 6 |

## Selbstprüfung (12.10., auf Josias' Wunsch)
**Gefunden und behoben:**
1. **„Tisch zeigen“ passte nicht in 170 Breite** (Größe 20, etwa 184 nötig). Der Text wäre umgebrochen und in der Höhe 50 abgeschnitten worden. Jetzt 200 breit, bündig mit „Verwalten“ in „Meine“, `lblZeitH` dafür 220 schmaler statt 190.
2. **Titel zu breit** bei Größe 26: „Quiet Desk 3 · Untergeschoss“ braucht etwa 551 bei 544 Platz. Jetzt Größe 22.
3. **Meine Prüfung vom Vormittag war zirkulär:** Ich hatte das Rechteck auf ein Bild gelegt, das ich aus denselben, falsch geordneten Daten selbst gezeichnet hatte. Deshalb fiel der Fehler bei OG 6–13 nicht auf. Die Gegenprüfung jetzt ist unabhängig: aus dem Desktop-Export plus REST-Reihenfolge nachgerechnet und auf **deine** Bilder gelegt.
4. **Neue Prüfung im Generator:** Textbreiten werden je Zeichenart geschätzt (Open Sans). Eine Gegenprobe mit den alten Werten meldet alle drei Fehler (Knopf, Überlappung, Titel).

**Nachgeprüft, in Ordnung (belegt):**
- `Screen1.Width = Max(App.Width; App.MinScreenWidth)`, `MinScreenWidth` 640. Die Layoutprüfung bei 640 ist also der schmalste Fall, auf breiteren Geräten wächst alles über `Parent.Width`.
- `MinScreenHeight` ist 640. Selbst dann passt der Plan: Bildhöhe 316, Schließen-Knopf darunter.
- Bild und Schließen-Knopf überlappen nicht. Das Bild endet bei `Parent.Height − 148`, der Knopf beginnt bei `Parent.Height − 124`.
- T0 ist zeichengleich mit H8, die Vorher-Fassung ist zeichengleich mit dem Export.
- T5 stellt nur `Set(varZeigeTisch; false);;` voran (maschinell geprüft). Die Tabs liegen bei offenem Plan unter dem Hintergrund, T5 ist also eine Absicherung, falls H-U3 nicht hält.
- Die Tabelle in T1 ist zahlengleich mit `tabelle_handy_de.txt`, und die ist unabhängig nachgerechnet (0 Abweichungen).

**Bleibt UNSICHER:** H-U1 bis H-U3. Die Textbreiten sind geschätzt, Test 7 und Test 8 entscheiden.

## 5. Rückfall
1. Die 8 neuen Steuerelemente löschen: `btnTischZeigenH`, `btnTischZeigenM`, `btnTischPlanHintergrund`, `conTischPlan` samt Inhalt.
2. `App.Formulas` leeren.
3. `lblZeitH.Width`, `lblZeitM.Width`, `btnTabHeute/Buchen/Meine.OnSelect` und `icoAktualisieren_1.OnSelect` auf Anhang A zurücksetzen.
4. Medien `handy_plan_OG`/`handy_plan_UG` löschen.
5. **T0 bleibt.** Es ist der fehlende Teil von H8 und unabhängig vom Feature.

## 6. Bei neuem Tisch oder Umbenennung
1. Tische in SharePoint ändern, dann in der Desktop-App die Positionen (`colTischPositionen`/`colTischPositionenUG`) anpassen. Der Desktop-Grundriss verschiebt sich sonst, siehe Hinweis 7.
2. Neuen Desktop-Export und die neue Reihenfolge der Liste `Tische` (REST) an den Handy-Chat. Sein Skript erzeugt Bilder und `tabelle_handy_de.txt` neu.
3. Gegenprüfung durch mich mit `werkzeuge/tisch_zeigen_v2.py`, dann nur zwei Dinge in der App ersetzen: den Teil `Tische:` in `App.Formulas` und die zwei Bilder (gleiche Namen hochladen, alte vorher löschen). Kein anderer Block ändert sich.

## 7. Zum Hinweis Desktop (Galerie-Versatz)
- Bestätigt (belegt, `Rectangle1.Y`): Der Versatz hängt an der ID-Reihenfolge in `Tische`. Ein neuer oder gelöschter Tisch verschiebt Kacheln im Desktop-Grundriss.
- Der Vorschlag ist richtig: echtes Bild-Y in die Positionstabellen und `Rectangle1.Y` vereinfachen. Das wird nach dem Go-Live bewertet und ist im Backlog vermerkt.

## Anhang A: Fassungen im Handy-Export 12.10. 12:05 (Rückfall)

**`App.OnStart`** (T0)

```
Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische);;
Set(
  varProfilFarbe;
  Switch(
    RandBetween(1; 8);
    1; ColorValue("#8CAFF4");
    2; ColorValue("#82C7B3");
    3; ColorValue("#EFA897");
    4; ColorValue("#B59EDC");
    5; ColorValue("#82CCC5");
    6; ColorValue("#F5C295");
    7; ColorValue("#A1AADB");
    ColorValue("#A1B1BA")
  )
)
```

**`lblZeitH.Width`** (T2)

```
Parent.Width - 56
```

**`lblZeitM.Width`** (T3)

```
Parent.Width - 250
```

**`btnTabHeute.OnSelect`** (T5)

```
Set(varTab; "heute");;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

**`btnTabBuchen.OnSelect`** (T5)

```
Set(varTab; "buchen");;
Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

**`btnTabMeine.OnSelect`** (T5)

```
Set(varTab; "meine");;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

**`icoAktualisieren_1.OnSelect`** (T5)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Refresh(Tische);;
ClearCollect(colTische; Tische);;
Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Set(varNeuLaden; varNeuLaden + 1);;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

`App.Formulas` ist im Export leer.

## Anhang B: Maschinelle Prüfung

```
123 Properties in 6 Schritten, 8 neue Steuerelemente. Grundlage: Handy-Export 12.10. 12:05 („handy echt“).
Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, keine neue Abfrage.
T1: Tabelle zahlengleich mit tabelle_handy_de.txt (35 Tische); diese ist gegen den Desktop-Export 11:52 + Reihenfolge nachgerechnet (pruefung_tabelle.txt).
Textbreiten (Schätzung je Zeichenart, Open Sans, halbfett +5 %, Innenabstand 20): alle Texte passen bei Layoutbreite 640.
Bilder: Seitenverhältnis 2,5. Karten: der neue Knopf überlappt nichts bei Layoutbreite 640 (btnVerwaltenM überlappt lblTischM/lblTagM schon im Export um 6 px, unverändert).
T5: an den vier Knöpfen nur das Schließen vorangestellt.
Prüfung: 0 Fehler
```

```
Tische: Handy-Chat 35, nachgerechnet 35 (Desktop-Export 12.10. 11:52, Reihenfolge per REST).
Vergleich je Wert mit Toleranz 0,0006 (Rundung auf 4 Stellen).
Gegenprüfung: 0 Abweichungen
```
