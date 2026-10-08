# Handy H8: Tageswechsel bei offener App (08.10.2026)

Für den Handy-Chat. Grundlage ist der **Handy-Export 08.10. 14:25** (veröffentlicht, = Umbauplan v2 + Profilfarbe). Erzeugt mit `werkzeuge/handy_h8.py`, unabhängig geprüft (keine Befunde über niedrig). Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Problem (belegt aus den Formeln, mittel):** `ddDatum.Items` und `lblHeuteTitel.Text` rechnen mit `Today()`. Sie werden nicht neu berechnet, solange die App offen ist.
  - Bleibt die App über Nacht in Power Apps Mobile offen, steht morgens „Heute“ noch auf gestern.
  - Wer „Morgen“ wählt, bucht in Wahrheit für **heute**.
  - `galHeute` und `galMeine` werden erst nach einer Aktion neu geladen.
- **Lösung:** `varHeute` merkt sich den Tag. Bei einem neuen Tag macht `tmrJetzt` (läuft jede Minute) drei Dinge:
  - `varHeute` neu setzen,
  - `ddDatum` zurücksetzen,
  - die Listen neu laden (`varNeuLaden + 1`).
  - Keine zusätzliche Abfrage außer diesem einen Neuladen pro Tag.
- **Umfang:** 4 Properties, kein neues Steuerelement. Maschinell 0 Fehler.

## Einfügen
**Wichtig zu `App.OnStart` (Prüfung B10):** Deine YAML-Quelle kann neuer sein als der Export.
- Vergleiche zuerst dein `App.OnStart` mit „Fassung im Export“ unten.
- **Ist sie gleich**, ganze Property ersetzen.
- **Ist sie anders**, nur `Set(varHeute; Today());;` direkt hinter `Set(varJetzt; Now());;` einfügen.


### `App.OnStart`

Ort: `App` · **ganze Property ersetzen**

Änderung gegenüber dem Export (`-` alt, `+` neu):

```diff
@@ -1,2 +1,2 @@
-Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische);;
+Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varHeute; Today());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; Set(varListeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische);;
 Set(
```

Vollständiger Block:

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

### `tmrJetzt.OnTimerEnd`

Ort: `Screen1 > tmrJetzt` · **ganze Property ersetzen**

Änderung gegenüber dem Export (`-` alt, `+` neu):

```diff
@@ -1 +1,7 @@
-Set(varJetzt; Now())
+Set(varJetzt; Now());;
+If(
+  !varIsLoading && Today() <> varHeute;
+  Set(varHeute; Today());;
+  Reset(ddDatum);;
+  Set(varNeuLaden; varNeuLaden + 1)
+)
```

Vollständiger Block:

```
Set(varJetzt; Now());;
If(
  !varIsLoading && Today() <> varHeute;
  Set(varHeute; Today());;
  Reset(ddDatum);;
  Set(varNeuLaden; varNeuLaden + 1)
)
```

### `ddDatum.Items`

Ort: `Screen1 > conRoot > conInhalt > conBuchen > conBuchenForm > ddDatum` · **ganze Property ersetzen**

Änderung gegenüber dem Export (`-` alt, `+` neu):

```diff
@@ -3,4 +3,4 @@
   {
-    Value: If(n.Value = 0; "Heute, "; n.Value = 1; "Morgen, "; "") & Text(DateAdd(Today(); n.Value; TimeUnit.Days); "dddd, dd.mm.yyyy");
-    Tag: DateAdd(Today(); n.Value; TimeUnit.Days)
+    Value: If(n.Value = 0; "Heute, "; n.Value = 1; "Morgen, "; "") & Text(DateAdd(Coalesce(varHeute; Today()); n.Value; TimeUnit.Days); "dddd, dd.mm.yyyy");
+    Tag: DateAdd(Coalesce(varHeute; Today()); n.Value; TimeUnit.Days)
   }
```

Vollständiger Block:

```
ForAll(
  Sequence(60; If(Hour(Now()) >= 22; 1; 0)) As n;
  {
    Value: If(n.Value = 0; "Heute, "; n.Value = 1; "Morgen, "; "") & Text(DateAdd(Coalesce(varHeute; Today()); n.Value; TimeUnit.Days); "dddd, dd.mm.yyyy");
    Tag: DateAdd(Coalesce(varHeute; Today()); n.Value; TimeUnit.Days)
  }
)
```

### `lblHeuteTitel.Text`

Ort: `Screen1 > conRoot > conInhalt > conHeute > lblHeuteTitel` · **ganze Property ersetzen**

Änderung gegenüber dem Export (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-"Heute, " & Text(Today(); "dddd dd.mm.")
+"Heute, " & Text(Coalesce(varHeute; Today()); "dddd dd.mm.")
```

Vollständiger Block:

```
"Heute, " & Text(Coalesce(varHeute; Today()); "dddd dd.mm.")
```

## Test (etwa 3 Minuten)
1. Vorübergehend einen Knopf `btnTestTag` anlegen, `OnSelect`: `Set(varHeute; DateAdd(Today(); -1; TimeUnit.Days))`.
2. In der Vorschau tippen. Titel „Heute, …“ und die Datumsliste zeigen jetzt **gestern** (so sähe die App morgens ohne H8 aus).
3. Höchstens 1 Minute warten (`tmrJetzt` hat keine `Duration`, Standard 60 s, geschlussfolgert).
   - Erwartet: Titel und Datumsliste zeigen wieder **heute**.
   - Im Buchen-Tab ist „Heute, <Datum>“ ausgewählt, und der Beginn steht bei der laufenden halben Stunde.
   - Die Listen „Heute“ und „Meine“ laden neu.
4. **`btnTestTag` löschen.**

## Bekannt und gewollt
- Um Mitternacht verwirft `Reset(ddDatum)` auch ein bewusst gewähltes späteres Datum. Das ist selten, nach dem Zurücksetzen wählt man neu.
- `Hour(Now()) >= 22` in `ddDatum.Items` wird weiter nicht neu berechnet (ab 22:00 „Heute“ ausblenden). Das ist harmlos, weil `btnBuchen` das 22:00-Ende ohnehin prüft.
- Ist die App im Hintergrund, laufen keine Timer. Nach dem Zurückholen greift H8 beim nächsten Takt, also nach höchstens 1 Minute. Wer in dieser Minute bucht, sieht noch den alten Tag (UNSICHER, ob Power Apps Mobile die App nach einer Nacht ohnehin neu startet).

## Rückfall
Die vier Fassungen im Export (unten) wieder einsetzen. `varHeute` stört dann nicht.

## Anhang: Fassungen im Export 08.10. 14:25

**`App.OnStart`**

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

**`tmrJetzt.OnTimerEnd`**

```
Set(varJetzt; Now())
```

**`ddDatum.Items`**

```
ForAll(
  Sequence(60; If(Hour(Now()) >= 22; 1; 0)) As n;
  {
    Value: If(n.Value = 0; "Heute, "; n.Value = 1; "Morgen, "; "") & Text(DateAdd(Today(); n.Value; TimeUnit.Days); "dddd, dd.mm.yyyy");
    Tag: DateAdd(Today(); n.Value; TimeUnit.Days)
  }
)
```

**`lblHeuteTitel.Text`**

```
"Heute, " & Text(Today(); "dddd dd.mm.")
```
