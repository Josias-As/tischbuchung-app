# Umbauplan Handy-App „Tischbuchung Handy“ (08.10.2026)

Für den Chat, der die Handy-App weiterbaut. Erzeugt von Claude Code (Desktop-Repo `tischbuchung-app`) mit `werkzeuge/handy_plan.py` aus dem **Handy-Export vom 08.10., 11:51** und maschinell geprüft. Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**. Ersetzt `AUFTRAG_Handy_Freigabe.md` (jetzt mit fertigen Formeln).

## 0. Startprompt für den Handy-Chat (so übergeben)
> Du baust mit Josias die Handy-App „Tischbuchung Handy“ (App-ID `e218702e-…`) weiter. Sie nutzt dieselben SharePoint-Listen wie die Desktop-App „Tischbuchung“. Die Desktop-App bekommt gerade dieselben Regeln (Paket F Fassung 2). Damit beide Apps zusammenpassen, setze bitte diesen Umbauplan **Schritt für Schritt** um (H0 → H7). Pro Schritt: ganze Property ersetzen (Block unverändert, deutsche Schreibweise), App-Prüfung, Test, Strg+S. Arbeitest du lieber mit YAML, stehen die englischen Formeln in `handy_bloecke.json` (Feld `yaml`). **Formeln nicht umschreiben.** Passt ein Block nicht zum Stand im Studio (der Diff zeigt, was vorher dort stehen muss), stoppen und Claude Code einen neuen Export geben. Die Handy-App wird erst geteilt, wenn H1–H6 drin und getestet sind. Lege diesen Plan und `handy_bloecke.json` im Vault unter `Tischbuchung/2026-10-08_Handy` ab.

## 1. Kurzfassung
- **Warum jetzt:** Die Desktop-App gibt ab Paket F nicht eingecheckte Buchungen **in der App** frei. Es gibt keinen Flow, und nichts wird gelöscht. Eine Buchung **verfällt**, wenn sie nicht eingecheckt ist und Beginn **und** Buchungszeitpunkt (`Erstellt`) mehr als 30 Minuten zurückliegen. Verfallene Buchungen zählen überall als frei.
- **Ohne denselben Umbau in der Handy-App** passiert Folgendes (geschlussfolgert aus den Formeln):
  1. Die Handy-App zeigt freigegebene Tische weiter als belegt. Das ist harmlos.
  2. Sie lässt **Einchecken auf eine verfallene Buchung** zu, auch wenn der Tisch inzwischen neu vergeben ist. Dann sind zwei Personen am selben Tisch eingecheckt.
  3. **Fehlalarm beim Buchen:** Die Nachprüfung nach dem Patch meldet „Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht“, sobald auf dem Tisch eine verfallene Buchung liegt. Der Grund: Sie zählt jede ältere Zeile mit.
  4. **Falsche Rücknahme beim Verlängern:** Die Nachprüfung nimmt die Verlängerung zurück, sobald irgendeine andere Zeile im Zeitraum liegt, auch eine verfallene.
- **Umfang:** 7 Schritte, **17 Properties**, **kein neues Steuerelement**. Dazu ein Vorab-Test (H0).
- **Enthalten:**
  - Freigabe-Regel.
  - Gesperrte Tische (`Tische.Gesperrt`) ausblenden.
  - Einchecken bis zur Frist, mit dem noch offenen **B5/B8** (eigene Variable `varCheckinID`, Knopfanzeige mit `varJetzt`).
  - Nachprüfungen ohne Fehlalarm und pro Klick eindeutig (kein Zwischenspeicher).
  - Stornieren und Jetzt beenden nur für eigene Buchungen.
  - Startzeiten ab 06:00.
- **Geprüft:** maschinell 0 Fehler (Anhang B) und unabhängig (`pruefung_handy.md`). In Studio nichts getestet.

## 2. Stand der Handy-App (Export 08.10., belegt)
- 69 Steuerelemente, 793 Properties. Gegenüber dem 07.10. sind 18 Properties geändert und 7 neu.
- **Neu: `tmrJetzt`** (setzt `varJetzt` jede Minute) und **`App.OnError`**.
- **Schon drin aus der Prüfung B1–B11** (`05_HANDY_APP/skripte/fix_pruefung.js`):
  - Verlängern +1/+2: 22:00 per `DateTime`, „bereits beendet“, „zwei Tische“, Nachprüfung mit Rücknahme.
  - Jetzt beenden (B1/B4): nicht vor Beginn, nicht nach Ende, Ende auf die halbe Stunde.
  - Stornieren-Knopf mit Sperre (B10).
  - `tmrJetzt`.
- **Noch nicht drin: B5/B8 (Einchecken).** Die Galerie setzt weiter `varBuchungID`, das auch der Verwalten-Dialog nutzt, und die Knopfanzeige rechnet mit `Now()` statt `varJetzt`. **Kommt mit H6.**
- **Was fehlt (für die gemeinsamen Regeln):** Freigabe-Regel, gesperrte Tische, Startzeit 06:00. `colTische` wird nur beim Start geladen: Ein Tisch, den Josias sperrt, erscheint erst nach Neustart als gesperrt. Das behebt H3 beim Aktualisieren.

## 3. Gemeinsame Regeln Desktop + Handy (Stand 08.10.)
| Regel | Desktop | Handy nach diesem Plan |
|---|---|---|
| Buchbar | 06:00–22:00, nicht in der Vergangenheit | gleich (H7, vorhanden) |
| Einchecken | ab 30 Min vor Beginn bis zur Frist (Beginn bzw. Buchungszeitpunkt + 30 Min) | gleich (H6) |
| Verfallen | nicht eingecheckt, Beginn **und** Erstellt > 30 Min her; zählt als frei, nichts gelöscht | gleich (H3–H6) |
| Gesperrte Tische | nicht buchbar | gleich (H3, H4) |
| Keine zwei Tische zur selben Zeit | beim Buchen und Verlängern | vorhanden, jetzt ohne verfallene (H4, H5) |
| Stornieren / Beenden | nur eigene, Desktop ohne Rückfrage (Josias), Auschecken mit zweitem Tippen | nur eigene (H2), Handy behält seine Rückfrage beim Stornieren |
| Auschecken / Jetzt beenden | Desktop: Ende = nächste Minute | Handy: Ende = laufende halbe Stunde (vorhanden, bleibt) |
| Big Table | Desktop: für alle über den Grundriss buchbar | Handy: nicht buchbar (V-Regel, bleibt) |
| Die 30 Minuten | `varFreigabeMinuten` in `App.OnStart` | gleich (H1); beide Apps **gleich halten** |

## 4. So arbeitest du
1. **H0 zuerst** (Vorab-Test), dann H1 → H7. H1 legt `varFreigabeMinuten` und `varFreigabeGrenze` an, alle anderen lesen sie.
2. Je Property: Steuerelement suchen (Ort steht dabei), **ganze Property ersetzen**. Der Diff zeigt, was sich gegenüber dem Export vom 08.10. ändert (`-` alt, `+` neu). **Steht im Studio etwas anderes als die `-`-Zeilen:** stoppen, neuen Export an Claude Code.
3. Nach jedem Schritt App-Prüfung (keine neuen roten Fehler), Test, Strg+S. Nach H1 in Studio **OnStart ausführen**.
4. **Daten aktualisieren:** Vor H3 in Studio Daten → `Tische` → **Aktualisieren**, damit die Spalte `Gesperrt` bekannt ist (gibt es seit Phase 0).
5. **Rückfall:** Anhang A enthält die Fassung vor dem Umbau (Export 08.10.). Ganz zurück nur in umgekehrter Reihenfolge (H7 → H1).
6. **YAML:** Arbeitest du mit YAML (`… → Ansichtscode`), nimm die englischen Formeln aus `handy_bloecke.json` (Feld `yaml`, mit `=` davor).

## 5. Schritte

| Schritt | Was | Properties |
|---|---|---|
| H0 | Vorab-Test „Erstellt“ | – (2 Test-Steuerelemente, danach löschen) |
| H1 | App-Start: Einstellung 30 Minuten | `App.OnStart` |
| H2 | Stornieren und Jetzt beenden: nur eigene Buchungen | `btnStornoJa.OnSelect`, `btnJetztBeenden.OnSelect` |
| H3 | Tischauswahl: verfallene Buchungen frei, gesperrte Tische weg | `ddTisch.Items`, `btnTabBuchen.OnSelect`, `btnZumBuchen.OnSelect`, `icoAktualisieren_1.OnSelect` |
| H4 | Buchen: Regel, gesperrt, Nachprüfung ohne Fehlalarm | `btnBuchen.OnSelect` |
| H5 | Verlängern: Regel, keine falsche Rücknahme | `btnVerl1.OnSelect`, `btnVerl2.OnSelect` |
| H6 | Einchecken bis zur Frist, Status „Verfallen“ (mit B5/B8) | `btnEincheckenH.OnSelect`, `btnEincheckenH.DisplayMode`, `btnEincheckenH.Text`, `lblStatusH.Text`, `lblStatusH.Color` |
| H7 | Startzeiten ab 06:00 | `ddStart.Items`, `ddStart.Default` |

### H0 Vorab-Test „Erstellt“

**Vorab-Test, 2 Minuten:** wie in der Desktop-App (Paket F2, Abschnitt 3), diesmal **in der Handy-App**, weil die Datenquelle dort eine eigene Verbindung ist.
1. Textbeschriftung `lblTestErstellt`, `Text`:
```
"Erstellt: " & Text(First(Tischbuchungen).Erstellt; "dd.mm.yyyy hh:mm")
```
2. Schaltfläche `btnTestErstellt`, `OnSelect`:
```
ClearCollect(colTestErstellt; Filter(Tischbuchungen; Endzeit > DateAdd(Now(); -14; TimeUnit.Days)));; Notify(CountRows(colTestErstellt) & " Zeilen, Erstellt der ersten: " & Text(First(colTestErstellt).Erstellt; "dd.mm.yyyy hh:mm"); NotificationType.Information)
```
- Erwartung: Datum in beiden, mindestens 1 Zeile. Danach **beide löschen**.
- Rot bei `Erstellt` → mit `Created` probieren und an Claude Code melden. Der Plan wird dann neu erzeugt. Nicht selbst ersetzen.

### H1 App-Start: Einstellung 30 Minuten

**Was neu ist:** `Set(varFreigabeMinuten; 30)` und `Set(varFreigabeGrenze; …)` vor dem Laden von `colTische`.
**Danach:** OnStart ausführen.
**Test:** App-Prüfung ohne rote Fehler.

#### `App.OnStart`

Ort: `App` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; ClearCollect(colTische; Tische)
+Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische)
```

Vollständiger Block:

```
Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; Set(varFreigabeMinuten; 30);; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));; ClearCollect(colTische; Tische)
```

**Rückfall H1:** Fassung aus Anhang A wieder einsetzen.

### H2 Stornieren und Jetzt beenden: nur eigene Buchungen

**Was neu ist:**
- Stornieren („Ja, stornieren“) und „Jetzt beenden“ prüfen vor dem Schreiben, ob die Buchung der angemeldeten Person gehört (`Lower(E-Mail)`).
- Meldung beim Beenden: „Andere können den Tisch wieder buchen“ statt „wieder frei“. Andere Apps sehen es erst beim nächsten Laden.
- **Warum:** `varBuchung` kommt heute nur aus den eigenen Listen. Die Prüfung schützt, falls das später anders wird, und entspricht der Desktop-App.

**Test:** eigene Buchung stornieren → „Buchung storniert.“. Laufende eigene Buchung „Jetzt beenden“ → „Buchung beendet …“.

#### `btnStornoJa.OnSelect`

Ort: `Screen1 > conDlgStorno > btnStornoJa` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -8,4 +8,7 @@
     Set(varZeigeStorno; false);;
     Set(varZeigeVerwalten; false);
+    Lower(varBuchung.Person.Email) <> Lower(User().Email);
+    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);;
+    Set(varZeigeStorno; false);
     IfError(
       Remove(Tischbuchungen; varBuchung);
```

Vollständiger Block:

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);;
    Set(varZeigeStorno; false);;
    Set(varZeigeVerwalten; false);
    Lower(varBuchung.Person.Email) <> Lower(User().Email);
    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);;
    Set(varZeigeStorno; false);
    IfError(
      Remove(Tischbuchungen; varBuchung);
      Notify("Das Stornieren ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      If(
        IsBlank(LookUp(Tischbuchungen; ID = varBuchungID).ID);
        Notify("Buchung storniert."; NotificationType.Success);;
        Set(varZeigeStorno; false);;
        Set(varZeigeVerwalten; false);
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnJetztBeenden.OnSelect`

Ort: `Screen1 > conDlgVerwalten > btnJetztBeenden` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -7,4 +7,6 @@
     Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
     If(
+      Lower(varBuchung.Person.Email) <> Lower(User().Email);
+      Notify("Nur eigene Buchungen können beendet werden."; NotificationType.Error);
       Now() <= varBuchung.Startzeit;
       Notify("Diese Buchung hat noch nicht begonnen. Du kannst sie stornieren."; NotificationType.Warning);
@@ -17,5 +19,5 @@
         If(
           LookUp(Tischbuchungen; ID = varBuchungID).Endzeit < varBuchung.Endzeit;
-          Notify("Buchung beendet. Der Tisch ist wieder frei."; NotificationType.Success);;
+          Notify("Buchung beendet. Andere können den Tisch wieder buchen."; NotificationType.Success);;
           Set(varZeigeVerwalten; false);
           Notify("Das Beenden ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
```

Vollständiger Block:

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
    If(
      Lower(varBuchung.Person.Email) <> Lower(User().Email);
      Notify("Nur eigene Buchungen können beendet werden."; NotificationType.Error);
      Now() <= varBuchung.Startzeit;
      Notify("Diese Buchung hat noch nicht begonnen. Du kannst sie stornieren."; NotificationType.Warning);
      Now() >= varBuchung.Endzeit;
      Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
      Set(varNeuEnde; With({ ab: DateTime(Year(Now()); Month(Now()); Day(Now()); Hour(Now()); If(Minute(Now()) >= 30; 30; 0); 0) }; If(ab > varBuchung.Startzeit; ab; Now())));;
      IfError(
        Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
        Notify("Das Beenden ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        If(
          LookUp(Tischbuchungen; ID = varBuchungID).Endzeit < varBuchung.Endzeit;
          Notify("Buchung beendet. Andere können den Tisch wieder buchen."; NotificationType.Success);;
          Set(varZeigeVerwalten; false);
          Notify("Das Beenden ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**Rückfall H2:** Fassung aus Anhang A wieder einsetzen.

### H3 Tischauswahl: verfallene Buchungen frei, gesperrte Tische weg

**Was neu ist:**
- `ddTisch.Items` zählt nur **aktive** Buchungen als belegt. Gesperrte Tische fehlen.
- Die Grenze wird beim Öffnen des Buchen-Tabs (Tab-Knopf, „Zum Buchen“) und beim Aktualisieren gesetzt.
- Aktualisieren lädt `colTische` neu (gesperrte Tische ohne Neustart).
- **Absichtlich nicht im Minutentakt:** Die Grenze ändert sich nur bei diesen Klicks. Sonst würde die Tischliste jede Minute neu abfragen, auch unsichtbar (gemessen: versteckte Steuerelemente fragen trotzdem ab). Eine alte Grenze ist vorsichtig: Es werden höchstens zu wenige Tische als frei gezeigt.

**Test:**
- In SharePoint eine Testzeile anlegen (Tisch X, Beginn vor 1 Std, CheckedIn = Nein). `Erstellt` ist dann „jetzt“: 30 Min warten oder `varFreigabeMinuten` per Testknopf auf 1 setzen (Testknopf danach löschen).
- Tab „Buchen“ öffnen, heute, die Zeit der Testzeile → Tisch X steht in der Liste.
- Tisch Y in `Tische` auf Gesperrt = Ja → Aktualisieren → Tisch Y fehlt.

#### `ddTisch.Items`

Ort: `Screen1 > conRoot > conInhalt > conBuchen > conBuchenForm > ddTisch` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -2,8 +2,8 @@
   { neuLaden: varNeuLaden };
   With(
-    { belegt: ForAll(Filter(Tischbuchungen; Startzeit < DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes) && Endzeit > DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes)); Tisch.Value) };
+    { belegt: Filter(ForAll(Filter(Tischbuchungen; Startzeit < DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes) && Endzeit > DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes)) As X; { TischName: X.Tisch.Value; Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze }); Aktiv) };
     ForAll(
       Sort(
-        Filter(colTische; !("big table" in Lower(Titel)) && !(Titel in belegt));
+        Filter(colTische; !Gesperrt && !("big table" in Lower(Titel)) && !(Titel in belegt.TischName));
         Geschoss.Value & Left(Titel; Len(Titel) - Len(Last(Split(Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Titel; " ")).Value); 0); "000")
       ) As t;
```

Vollständiger Block:

```
With(
  { neuLaden: varNeuLaden };
  With(
    { belegt: Filter(ForAll(Filter(Tischbuchungen; Startzeit < DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes) && Endzeit > DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes)) As X; { TischName: X.Tisch.Value; Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze }); Aktiv) };
    ForAll(
      Sort(
        Filter(colTische; !Gesperrt && !("big table" in Lower(Titel)) && !(Titel in belegt.TischName));
        Geschoss.Value & Left(Titel; Len(Titel) - Len(Last(Split(Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Titel; " ")).Value); 0); "000")
      ) As t;
      { Value: t.Titel; ID: t.ID }
    )
  )
)
```

#### `btnTabBuchen.OnSelect`

Ort: `Screen1 > conRoot > conTabLeiste > btnTabBuchen` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1,3 +1,4 @@
 Set(varTab; "buchen");;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
 Set(varZeigeVerwalten; false);;
 Set(varZeigeStorno; false)
```

Vollständiger Block:

```
Set(varTab; "buchen");;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

#### `btnZumBuchen.OnSelect`

Ort: `Screen1 > conRoot > conInhalt > conHeute > conHeuteLeer > btnZumBuchen` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Set(varTab; "buchen")
+Set(varTab; "buchen");; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes))
```

Vollständiger Block:

```
Set(varTab; "buchen");; Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes))
```

#### `icoAktualisieren_1.OnSelect`

Ort: `Screen1 > conRoot > conHeader > icoAktualisieren_1` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -2,4 +2,6 @@
 Refresh(Tischbuchungen);;
 Refresh(Tische);;
+ClearCollect(colTische; Tische);;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
 Set(varNeuLaden; varNeuLaden + 1);;
 Set(varIsLoading; false);;
```

Vollständiger Block:

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Refresh(Tische);;
ClearCollect(colTische; Tische);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Set(varNeuLaden; varNeuLaden + 1);;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

**Rückfall H3:** Fassung aus Anhang A wieder einsetzen.

### H4 Buchen: Regel, gesperrt, Nachprüfung ohne Fehlalarm

**Was neu ist:**
- **Vorprüfungen** als Collections, verfallene Buchungen entfernt (`colBuchBelegt`, `colBuchIch`).
- **Neu: gesperrter Tisch** → Meldung (falls jemand vor dem Aktualisieren bucht).
- **Nachprüfung pro Klick eindeutig:** untere Grenze um die Sekunden seit Mitternacht verschoben, wie in Desktop-Nachtrag 4. Sonst ist sie wortgleich zur Vorprüfung und könnte aus dem Zwischenspeicher kommen.
- Die Nachprüfung entfernt verfallene Buchungen und die zusätzlich geholten, früher endenden Zeilen. Danach entspricht sie genau der alten. **Kein Fehlalarm mehr bei verfallenen Buchungen.**
- Die Erfolgsmeldung erinnert ans Einchecken.

**Test:** Auf den Tisch der verfallenen Testzeile buchen → „Gebucht: … Bitte bis 30 Minuten nach Beginn einchecken.“, **keine** „Achtung“-Meldung. Gesperrten Tisch (Studio-Vorschau ohne Aktualisieren) → Meldung.

#### `btnBuchen.OnSelect`

Ort: `Screen1 > conRoot > conInhalt > conBuchen > conBuchenForm > btnBuchen` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -7,4 +7,9 @@
   Set(varTischName; ddTisch.Selected.Value);;
   Set(varTischID; ddTisch.Selected.ID);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  ClearCollect(colBuchBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
+  RemoveIf(colBuchBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+  ClearCollect(colBuchIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
+  RemoveIf(colBuchIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
   If(
     IsBlank(varTischName) || IsBlank(varTischID) || IsBlank(ddStart.Selected.Min) || IsBlank(ddEnde.Selected.Min);
@@ -16,7 +21,9 @@
     varBuchEnde > varTagesEnde;
     Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-    !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart).ID);
+    !IsBlank(LookUp(Tische; ID = varTischID && Gesperrt = true).ID);
+    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
+    !IsEmpty(colBuchBelegt);
     Notify("Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
-    !IsBlank(LookUp(Tischbuchungen; Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart).ID);
+    !IsEmpty(colBuchIch);
     Notify("Du hast in dieser Zeit schon einen Tisch gebucht."; NotificationType.Warning);
     IfError(
@@ -39,5 +46,7 @@
       );
       Notify("Das Buchen ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
+      Set(varBuchNachVon; DateAdd(varBuchStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
+      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchNachVon));;
+      RemoveIf(colKollision; (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze) || Endzeit <= varBuchStart);;
       Set(varBuchung; LookUp(colKollision; Person.Email = User().Email && Startzeit = varBuchStart && Endzeit = varBuchEnde));;
       If(
@@ -48,5 +57,5 @@
           !IsBlank(LookUp(colKollision; ID < varBuchungID).ID);
           Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
-          Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr"; NotificationType.Success);;
+          Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn einchecken."; NotificationType.Success);;
           Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
         )
```

Vollständiger Block:

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchStart; DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes));;
  Set(varBuchEnde; DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes));;
  Set(varTagesEnde; DateAdd(ddDatum.Selected.Tag; 22 * 60; TimeUnit.Minutes));;
  Set(varTischName; ddTisch.Selected.Value);;
  Set(varTischID; ddTisch.Selected.ID);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(colBuchBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
  RemoveIf(colBuchBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  ClearCollect(colBuchIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
  RemoveIf(colBuchIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  If(
    IsBlank(varTischName) || IsBlank(varTischID) || IsBlank(ddStart.Selected.Min) || IsBlank(ddEnde.Selected.Min);
    Notify("Bitte Datum, Uhrzeit und Tisch auswählen."; NotificationType.Warning);
    varBuchEnde <= varBuchStart;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varBuchStart < DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes);
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    varBuchEnde > varTagesEnde;
    Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    !IsEmpty(colBuchBelegt);
    Notify("Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    !IsEmpty(colBuchIch);
    Notify("Du hast in dieser Zeit schon einen Tisch gebucht."; NotificationType.Warning);
    IfError(
      Patch(
        Tischbuchungen;
        Defaults(Tischbuchungen);
        {
          Tisch: { Id: varTischID; Value: varTischName };
          Startzeit: varBuchStart;
          Endzeit: varBuchEnde;
          Person: {
            Claims: "i:0#.f|membership|" & Lower(User().Email);
            Department: "";
            DisplayName: User().FullName;
            Email: User().Email;
            JobTitle: "";
            Picture: ""
          }
        }
      );
      Notify("Das Buchen ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      Set(varBuchNachVon; DateAdd(varBuchStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchNachVon));;
      RemoveIf(colKollision; (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze) || Endzeit <= varBuchStart);;
      Set(varBuchung; LookUp(colKollision; Person.Email = User().Email && Startzeit = varBuchStart && Endzeit = varBuchEnde));;
      If(
        IsBlank(varBuchung.ID);
        Notify("Die Buchung ist nicht angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
        Set(varBuchungID; varBuchung.ID);;
        If(
          !IsBlank(LookUp(colKollision; ID < varBuchungID).ID);
          Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
          Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn einchecken."; NotificationType.Success);;
          Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**Rückfall H4:** Fassung aus Anhang A wieder einsetzen.

### H5 Verlängern: Regel, keine falsche Rücknahme

**Was neu ist:**
- Vorprüfungen ohne verfallene Buchungen.
- Eigene verfallene Buchung → „verfallen“, kein Verlängern.
- **Nachprüfung eindeutig und ohne verfallene oder früher endende Zeilen.** Die vorhandene Rücknahme greift damit nur noch bei echten gleichzeitigen Buchungen.

**Test:** Eigene laufende Buchung, die eine verfallene fremde Buchung desselben Tisches überlappt (Testzeile) → +1 Std → „Buchung verlängert.“, **keine** Rücknahme.

#### `btnVerl1.OnSelect`

Ort: `Screen1 > conDlgVerwalten > btnVerl1` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -2,4 +2,5 @@
   !varIsLoading && Now() >= varSperreBis;
   Set(varIsLoading; true);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
   Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
   If(
@@ -10,17 +11,25 @@
     Set(varNeuEnde; DateAdd(varEndeAlt; 60; TimeUnit.Minutes));;
     Set(varTagesEnde; DateTime(Year(varBuchung.Startzeit); Month(varBuchung.Startzeit); Day(varBuchung.Startzeit); 22; 0; 0));;
+    ClearCollect(colVerlBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
+    RemoveIf(colVerlBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
+    RemoveIf(colVerlIch; ID = varBuchungID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
       varEndeAlt <= Now();
       Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
+      !varBuchung.CheckedIn && varBuchung.Startzeit <= varFreigabeGrenze && varBuchung.Erstellt <= varFreigabeGrenze;
+      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
       varNeuEnde > varTagesEnde;
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
+      !IsEmpty(colVerlBelegt);
       Notify("Der Tisch ist in dieser Zeit schon belegt."; NotificationType.Warning);
-      !IsBlank(LookUp(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
+      !IsEmpty(colVerlIch);
       Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
       IfError(
         Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
         Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
+        Set(varVerlNachVon; DateAdd(varEndeAlt; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
+        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varVerlNachVon));;
+        RemoveIf(colKollision; ID <> varBuchungID && ((!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze) || Endzeit <= varEndeAlt));;
         If(
           LookUp(colKollision; ID = varBuchungID).Endzeit <> varNeuEnde;
```

Vollständiger Block:

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
    Set(varTischName; varBuchung.Tisch.Value);;
    Set(varEndeAlt; varBuchung.Endzeit);;
    Set(varNeuEnde; DateAdd(varEndeAlt; 60; TimeUnit.Minutes));;
    Set(varTagesEnde; DateTime(Year(varBuchung.Startzeit); Month(varBuchung.Startzeit); Day(varBuchung.Startzeit); 22; 0; 0));;
    ClearCollect(colVerlBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
    RemoveIf(colVerlBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
    RemoveIf(colVerlIch; ID = varBuchungID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      varEndeAlt <= Now();
      Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
      !varBuchung.CheckedIn && varBuchung.Startzeit <= varFreigabeGrenze && varBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varNeuEnde > varTagesEnde;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      !IsEmpty(colVerlBelegt);
      Notify("Der Tisch ist in dieser Zeit schon belegt."; NotificationType.Warning);
      !IsEmpty(colVerlIch);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      IfError(
        Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
        Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varVerlNachVon; DateAdd(varEndeAlt; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varVerlNachVon));;
        RemoveIf(colKollision; ID <> varBuchungID && ((!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze) || Endzeit <= varEndeAlt));;
        If(
          LookUp(colKollision; ID = varBuchungID).Endzeit <> varNeuEnde;
          Notify("Die Verlängerung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning);
          !IsBlank(LookUp(colKollision; ID <> varBuchungID).ID);
          IfError(
            Patch(Tischbuchungen; LookUp(Tischbuchungen; ID = varBuchungID); { Endzeit: varEndeAlt });
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Bitte deine Buchung prüfen, sie überschneidet sich."; NotificationType.Error);
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Die Verlängerung wurde zurückgenommen."; NotificationType.Error)
          );
          Notify("Buchung verlängert."; NotificationType.Success);;
          Set(varZeigeVerwalten; false)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnVerl2.OnSelect`

Ort: `Screen1 > conDlgVerwalten > btnVerl2` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -2,4 +2,5 @@
   !varIsLoading && Now() >= varSperreBis;
   Set(varIsLoading; true);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
   Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
   If(
@@ -10,17 +11,25 @@
     Set(varNeuEnde; DateAdd(varEndeAlt; 120; TimeUnit.Minutes));;
     Set(varTagesEnde; DateTime(Year(varBuchung.Startzeit); Month(varBuchung.Startzeit); Day(varBuchung.Startzeit); 22; 0; 0));;
+    ClearCollect(colVerlBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
+    RemoveIf(colVerlBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
+    RemoveIf(colVerlIch; ID = varBuchungID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
       varEndeAlt <= Now();
       Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
+      !varBuchung.CheckedIn && varBuchung.Startzeit <= varFreigabeGrenze && varBuchung.Erstellt <= varFreigabeGrenze;
+      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
       varNeuEnde > varTagesEnde;
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
+      !IsEmpty(colVerlBelegt);
       Notify("Der Tisch ist in dieser Zeit schon belegt."; NotificationType.Warning);
-      !IsBlank(LookUp(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
+      !IsEmpty(colVerlIch);
       Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
       IfError(
         Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
         Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
+        Set(varVerlNachVon; DateAdd(varEndeAlt; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
+        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varVerlNachVon));;
+        RemoveIf(colKollision; ID <> varBuchungID && ((!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze) || Endzeit <= varEndeAlt));;
         If(
           LookUp(colKollision; ID = varBuchungID).Endzeit <> varNeuEnde;
```

Vollständiger Block:

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
    Set(varTischName; varBuchung.Tisch.Value);;
    Set(varEndeAlt; varBuchung.Endzeit);;
    Set(varNeuEnde; DateAdd(varEndeAlt; 120; TimeUnit.Minutes));;
    Set(varTagesEnde; DateTime(Year(varBuchung.Startzeit); Month(varBuchung.Startzeit); Day(varBuchung.Startzeit); 22; 0; 0));;
    ClearCollect(colVerlBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
    RemoveIf(colVerlBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
    RemoveIf(colVerlIch; ID = varBuchungID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      varEndeAlt <= Now();
      Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
      !varBuchung.CheckedIn && varBuchung.Startzeit <= varFreigabeGrenze && varBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varNeuEnde > varTagesEnde;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      !IsEmpty(colVerlBelegt);
      Notify("Der Tisch ist in dieser Zeit schon belegt."; NotificationType.Warning);
      !IsEmpty(colVerlIch);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      IfError(
        Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
        Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varVerlNachVon; DateAdd(varEndeAlt; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varVerlNachVon));;
        RemoveIf(colKollision; ID <> varBuchungID && ((!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze) || Endzeit <= varEndeAlt));;
        If(
          LookUp(colKollision; ID = varBuchungID).Endzeit <> varNeuEnde;
          Notify("Die Verlängerung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning);
          !IsBlank(LookUp(colKollision; ID <> varBuchungID).ID);
          IfError(
            Patch(Tischbuchungen; LookUp(Tischbuchungen; ID = varBuchungID); { Endzeit: varEndeAlt });
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Bitte deine Buchung prüfen, sie überschneidet sich."; NotificationType.Error);
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Die Verlängerung wurde zurückgenommen."; NotificationType.Error)
          );
          Notify("Buchung verlängert."; NotificationType.Success);;
          Set(varZeigeVerwalten; false)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**Rückfall H5:** Fassung aus Anhang A wieder einsetzen.

### H6 Einchecken bis zur Frist, Status „Verfallen“ (mit B5/B8)

**Was neu ist:**
- **B5:** eigene Variable `varCheckinID`, nicht mehr `varBuchungID` (die der Verwalten-Dialog nutzt).
- Frisch lesen. Fenster ab 30 Min vor Beginn bis zur **Frist**.
- Vor dem Check-in prüfen, ob der Tisch schon an jemand anderen vergeben ist.
- Nachprüfung (eindeutig): angekommen? Gleichzeitig neu vergeben?
- **B8:** Die Knopfanzeige rechnet mit `varJetzt` (`tmrJetzt`, jede Minute). Der Knopf wird also zur richtigen Zeit aktiv und nach der Frist grau.
- Status „Verfallen“ (grau) in Karte und Knopf.

**Test:** Buchung in 1 Std → Knopf grau. Ab 30 Min vor Beginn aktiv → „Eingecheckt.“. Verfallene Testzeile (eigene) → Status „Verfallen“, Knopf grau. Doppeltipp → eine Meldung.

#### `btnEincheckenH.OnSelect`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnEincheckenH` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -2,25 +2,37 @@
   !varIsLoading && Now() >= varSperreBis;
   Set(varIsLoading; true);;
-  Set(varBuchungID; ThisItem.ID);;
-  With(
-    { frisch: LookUp(Tischbuchungen; ID = varBuchungID) };
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  Set(varCheckinID; ThisItem.ID);;
+  Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varCheckinID));;
+  Set(varCheckinTisch; varCheckinBuchung.Tisch.Value);;
+  Set(varCheckinStart; varCheckinBuchung.Startzeit);;
+  Set(varCheckinEnde; varCheckinBuchung.Endzeit);;
+  If(
+    IsBlank(varCheckinBuchung.ID);
+    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);
+    varCheckinBuchung.CheckedIn;
+    Notify("Du bist bereits eingecheckt."; NotificationType.Information);
+    Now() < DateAdd(varCheckinStart; -30; TimeUnit.Minutes);
+    Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich."; NotificationType.Warning);
+    Now() >= varCheckinEnde;
+    Notify("Diese Buchung ist schon zu Ende."; NotificationType.Warning);
+    varCheckinStart <= varFreigabeGrenze && varCheckinBuchung.Erstellt <= varFreigabeGrenze;
+    Notify("Zu spät: Ohne Check-in bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn verfällt die Buchung. Bitte neu buchen."; NotificationType.Warning);
+    ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
+    RemoveIf(colCheckinAndere; ID = varCheckinID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
-      IsBlank(frisch.ID);
-      Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);
-      If(
-        frisch.CheckedIn;
-        Notify("Du bist bereits eingecheckt."; NotificationType.Information);
+      !IsEmpty(colCheckinAndere);
+      Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen."; NotificationType.Error);
+      IfError(
+        Patch(Tischbuchungen; varCheckinBuchung; { CheckedIn: true });
+        Notify("Einchecken fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+        Set(varCheckinNachVon; DateAdd(varCheckinStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
+        ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinNachVon));;
         If(
-          Now() < DateAdd(frisch.Startzeit; -30; TimeUnit.Minutes) || Now() > frisch.Endzeit;
-          Notify("Einchecken ist erst ab 30 Minuten vor Beginn und nur bis zum Ende moeglich."; NotificationType.Warning);
-          IfError(
-            Patch(Tischbuchungen; frisch; { CheckedIn: true });
-            Notify("Einchecken fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-            If(
-              LookUp(Tischbuchungen; ID = varBuchungID).CheckedIn;
-              Notify("Eingecheckt."; NotificationType.Success);
-              Notify("Der Check-in ist nicht angekommen. Bitte aktualisieren und erneut versuchen."; NotificationType.Warning)
-            )
-          )
+          !LookUp(colCheckinAndere; ID = varCheckinID).CheckedIn;
+          Notify("Der Check-in ist nicht angekommen. Bitte aktualisieren und erneut versuchen."; NotificationType.Warning);
+          !IsBlank(LookUp(colCheckinAndere; ID <> varCheckinID && Endzeit > varCheckinStart && !(!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze)).ID);
+          Notify("Eingecheckt, aber der Tisch wurde gleichzeitig an jemand anderen vergeben. Bitte unter „Meine“ prüfen und klären."; NotificationType.Error);
+          Notify("Eingecheckt."; NotificationType.Success)
         )
       )
```

Vollständiger Block:

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  Set(varCheckinID; ThisItem.ID);;
  Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varCheckinID));;
  Set(varCheckinTisch; varCheckinBuchung.Tisch.Value);;
  Set(varCheckinStart; varCheckinBuchung.Startzeit);;
  Set(varCheckinEnde; varCheckinBuchung.Endzeit);;
  If(
    IsBlank(varCheckinBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);
    varCheckinBuchung.CheckedIn;
    Notify("Du bist bereits eingecheckt."; NotificationType.Information);
    Now() < DateAdd(varCheckinStart; -30; TimeUnit.Minutes);
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich."; NotificationType.Warning);
    Now() >= varCheckinEnde;
    Notify("Diese Buchung ist schon zu Ende."; NotificationType.Warning);
    varCheckinStart <= varFreigabeGrenze && varCheckinBuchung.Erstellt <= varFreigabeGrenze;
    Notify("Zu spät: Ohne Check-in bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn verfällt die Buchung. Bitte neu buchen."; NotificationType.Warning);
    ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
    RemoveIf(colCheckinAndere; ID = varCheckinID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !IsEmpty(colCheckinAndere);
      Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen."; NotificationType.Error);
      IfError(
        Patch(Tischbuchungen; varCheckinBuchung; { CheckedIn: true });
        Notify("Einchecken fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varCheckinNachVon; DateAdd(varCheckinStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
        ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinNachVon));;
        If(
          !LookUp(colCheckinAndere; ID = varCheckinID).CheckedIn;
          Notify("Der Check-in ist nicht angekommen. Bitte aktualisieren und erneut versuchen."; NotificationType.Warning);
          !IsBlank(LookUp(colCheckinAndere; ID <> varCheckinID && Endzeit > varCheckinStart && !(!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze)).ID);
          Notify("Eingecheckt, aber der Tisch wurde gleichzeitig an jemand anderen vergeben. Bitte unter „Meine“ prüfen und klären."; NotificationType.Error);
          Notify("Eingecheckt."; NotificationType.Success)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnEincheckenH.DisplayMode`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnEincheckenH` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1,13 +1,7 @@
 If(
-  ThisItem.CheckedIn;
+  ThisItem.CheckedIn || varIsLoading;
   DisplayMode.Disabled;
-  If(
-    varIsLoading;
-    DisplayMode.Disabled;
-    If(
-      Now() >= DateAdd(ThisItem.Startzeit; -30; TimeUnit.Minutes) && Now() <= ThisItem.Endzeit;
-      DisplayMode.Edit;
-      DisplayMode.Disabled
-    )
-  )
+  varJetzt >= DateAdd(ThisItem.Startzeit; -30; TimeUnit.Minutes) && varJetzt < ThisItem.Endzeit && !(!ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt);
+  DisplayMode.Edit;
+  DisplayMode.Disabled
 )
```

Vollständiger Block:

```
If(
  ThisItem.CheckedIn || varIsLoading;
  DisplayMode.Disabled;
  varJetzt >= DateAdd(ThisItem.Startzeit; -30; TimeUnit.Minutes) && varJetzt < ThisItem.Endzeit && !(!ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt);
  DisplayMode.Edit;
  DisplayMode.Disabled
)
```

#### `btnEincheckenH.Text`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > btnEincheckenH` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; "Eingecheckt"; "Einchecken")
+If(ThisItem.CheckedIn; "Eingecheckt"; !ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt; "Verfallen"; "Einchecken")
```

Vollständiger Block:

```
If(ThisItem.CheckedIn; "Eingecheckt"; !ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt; "Verfallen"; "Einchecken")
```

#### `lblStatusH.Text`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > lblStatusH` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; "Eingecheckt"; "Nicht eingecheckt")
+If(ThisItem.CheckedIn; "Eingecheckt"; !ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt; "Verfallen"; "Nicht eingecheckt")
```

Vollständiger Block:

```
If(ThisItem.CheckedIn; "Eingecheckt"; !ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt; "Verfallen"; "Nicht eingecheckt")
```

#### `lblStatusH.Color`

Ort: `Screen1 > conRoot > conInhalt > conHeute > galHeute > conKarteH > lblStatusH` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; RGBA(0; 169; 107; 1); RGBA(255; 165; 0; 1))
+If(ThisItem.CheckedIn; RGBA(0; 169; 107; 1); !ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt; RGBA(166; 166; 166; 1); RGBA(255; 165; 0; 1))
```

Vollständiger Block:

```
If(ThisItem.CheckedIn; RGBA(0; 169; 107; 1); !ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt && DateAdd(ThisItem.Erstellt; Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) <= varJetzt; RGBA(166; 166; 166; 1); RGBA(255; 165; 0; 1))
```

**Rückfall H6:** Fassung aus Anhang A wieder einsetzen.

### H7 Startzeiten ab 06:00

**Was neu ist:** Startliste ab 06:00 (heute ab der laufenden halben Stunde, nicht vor 06:00). Neu ist eine **Vorgabe**: heute die erste mögliche Zeit, an anderen Tagen 08:00. Bisher nahm die Liste den ersten Eintrag, das wäre 06:00.
**Test:** Morgen → 08:00 vorgeschlagen, Liste ab 06:00.

#### `ddStart.Items`

Ort: `Screen1 > conRoot > conInhalt > conBuchen > conBuchenForm > conZeiten > conVon > ddStart` · **ganze Property ersetzen**

Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):

```diff
@@ -1,4 +1,4 @@
 With(
-  { ab: If(ddDatum.Selected.Tag = Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); 8 * 60) };
+  { ab: If(ddDatum.Selected.Tag = Today(); Max(6 * 60; 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0)); 6 * 60) };
   ForAll(
     Sequence(Max(0; (21 * 60 + 30 - ab) / 30 + 1); 0) As n;
```

Vollständiger Block:

```
With(
  { ab: If(ddDatum.Selected.Tag = Today(); Max(6 * 60; 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0)); 6 * 60) };
  ForAll(
    Sequence(Max(0; (21 * 60 + 30 - ab) / 30 + 1); 0) As n;
    {
      Value: Text(Time(RoundDown((ab + n.Value * 30) / 60; 0); Mod(ab + n.Value * 30; 60); 0); "hh:mm");
      Min: ab + n.Value * 30
    }
  )
)
```

#### `ddStart.Default`

Ort: `Screen1 > conRoot > conInhalt > conBuchen > conBuchenForm > conZeiten > conVon > ddStart` · **neu setzen**

Vollständiger Block:

```
If(
  ddDatum.Selected.Tag = Today();
  With(
    { ab: Max(6 * 60; 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0)) };
    Text(Time(RoundDown(ab / 60; 0); Mod(ab; 60); 0); "hh:mm")
  );
  "08:00"
)
```

**Rückfall H7:** Fassung aus Anhang A wieder einsetzen (`ddStart.Default` leeren).

## 6. Offen, später, Hinweise
- **`App.OnError` (neu im Export):** Die Formel zeigt bei **jedem** nicht abgefangenen Fehler „Die Verbindung zu SharePoint hat nicht geklappt …“, auch bei Formelfehlern. Die Fehlersuche wird dadurch schwer. Vorschlag (optional): `Notify("Fehler: " & FirstError.Message; NotificationType.Error)`. **UNSICHER**, ob die englischen Meldungen für Kollegen verständlich sind. Entscheidung bei Josias.
- **Startlisten mit `Now()`** (`ddDatum`, `ddStart`): Sie veralten, wenn die App stundenlang offen bleibt. Speichern prüft aber „Vergangenheit“ frisch. `varJetzt` dort einzusetzen würde die Listen jede Minute neu bauen und kann die Auswahl zurücksetzen. Deshalb bewusst nicht.
- **QR-Check-in am Tisch** (`Param("tisch")`) wäre der nächste sinnvolle Schritt gegen Einchecken von zu Hause. Eigenes Konzept nach dem Go-Live.
- **Rechte „nur eigene Elemente“:** Die Handy-App schreibt als angemeldete Person. Das passt.

## 7. Testbogen
| ✓ | Test | Ergebnis |
|---|---|---|
| ☐ | H0 Vorab-Test, Test-Steuerelemente gelöscht | |
| ☐ | H1 App-Prüfung, OnStart ausgeführt | |
| ☐ | H2 eigene Buchung stornieren / beenden | |
| ☐ | H3 Liste zeigt Tisch mit verfallener Buchung, gesperrter Tisch fehlt | |
| ☐ | H4 Buchen über verfallene Buchung ohne „Achtung“, gesperrt → Meldung | |
| ☐ | H5 Verlängern über verfallene Buchung ohne Rücknahme | |
| ☐ | H6 Knopf aktiv/grau nach Zeit, Einchecken, „Verfallen“, Doppeltipp | |
| ☐ | H7 Startzeiten 06:00, Vorgabe 08:00 | |
| ☐ | Gegenprobe Desktop: dieselbe Testzeile zeigt dort dasselbe (grün, buchbar) | |
| ☐ | Testknopf gelöscht, `Set(varFreigabeMinuten; 30)` in `App.OnStart`; veröffentlichen, erst dann teilen | |

## Anhang A: Fassungen im Export 08.10. (Rückfall)

**`App.OnStart`** (H1)

```
Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varNeuBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varCheckinID; 0);; Set(varNeuID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0);; Set(varNeuEnde; Now());; Set(varTagesEnde; Now());; Set(varTischName; "");; Set(varEndeAlt; Now());; Set(varBuchStart; Now());; Set(varBuchEnde; Now());; Set(varTischID; 0);; Set(varSperreBis; Now());; Set(varJetzt; Now());; ClearCollect(colTische; Tische)
```

**`btnStornoJa.OnSelect`** (H2)

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);;
    Set(varZeigeStorno; false);;
    Set(varZeigeVerwalten; false);
    IfError(
      Remove(Tischbuchungen; varBuchung);
      Notify("Das Stornieren ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      If(
        IsBlank(LookUp(Tischbuchungen; ID = varBuchungID).ID);
        Notify("Buchung storniert."; NotificationType.Success);;
        Set(varZeigeStorno; false);;
        Set(varZeigeVerwalten; false);
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnJetztBeenden.OnSelect`** (H2)

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
    If(
      Now() <= varBuchung.Startzeit;
      Notify("Diese Buchung hat noch nicht begonnen. Du kannst sie stornieren."; NotificationType.Warning);
      Now() >= varBuchung.Endzeit;
      Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
      Set(varNeuEnde; With({ ab: DateTime(Year(Now()); Month(Now()); Day(Now()); Hour(Now()); If(Minute(Now()) >= 30; 30; 0); 0) }; If(ab > varBuchung.Startzeit; ab; Now())));;
      IfError(
        Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
        Notify("Das Beenden ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        If(
          LookUp(Tischbuchungen; ID = varBuchungID).Endzeit < varBuchung.Endzeit;
          Notify("Buchung beendet. Der Tisch ist wieder frei."; NotificationType.Success);;
          Set(varZeigeVerwalten; false);
          Notify("Das Beenden ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`ddTisch.Items`** (H3)

```
With(
  { neuLaden: varNeuLaden };
  With(
    { belegt: ForAll(Filter(Tischbuchungen; Startzeit < DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes) && Endzeit > DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes)); Tisch.Value) };
    ForAll(
      Sort(
        Filter(colTische; !("big table" in Lower(Titel)) && !(Titel in belegt));
        Geschoss.Value & Left(Titel; Len(Titel) - Len(Last(Split(Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Titel; " ")).Value); 0); "000")
      ) As t;
      { Value: t.Titel; ID: t.ID }
    )
  )
)
```

**`btnTabBuchen.OnSelect`** (H3)

```
Set(varTab; "buchen");;
Set(varZeigeVerwalten; false);;
Set(varZeigeStorno; false)
```

**`btnZumBuchen.OnSelect`** (H3)

```
Set(varTab; "buchen")
```

**`icoAktualisieren_1.OnSelect`** (H3)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Refresh(Tische);;
Set(varNeuLaden; varNeuLaden + 1);;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

**`btnBuchen.OnSelect`** (H4)

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchStart; DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes));;
  Set(varBuchEnde; DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes));;
  Set(varTagesEnde; DateAdd(ddDatum.Selected.Tag; 22 * 60; TimeUnit.Minutes));;
  Set(varTischName; ddTisch.Selected.Value);;
  Set(varTischID; ddTisch.Selected.ID);;
  If(
    IsBlank(varTischName) || IsBlank(varTischID) || IsBlank(ddStart.Selected.Min) || IsBlank(ddEnde.Selected.Min);
    Notify("Bitte Datum, Uhrzeit und Tisch auswählen."; NotificationType.Warning);
    varBuchEnde <= varBuchStart;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varBuchStart < DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes);
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    varBuchEnde > varTagesEnde;
    Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
    !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart).ID);
    Notify("Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    !IsBlank(LookUp(Tischbuchungen; Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart).ID);
    Notify("Du hast in dieser Zeit schon einen Tisch gebucht."; NotificationType.Warning);
    IfError(
      Patch(
        Tischbuchungen;
        Defaults(Tischbuchungen);
        {
          Tisch: { Id: varTischID; Value: varTischName };
          Startzeit: varBuchStart;
          Endzeit: varBuchEnde;
          Person: {
            Claims: "i:0#.f|membership|" & Lower(User().Email);
            Department: "";
            DisplayName: User().FullName;
            Email: User().Email;
            JobTitle: "";
            Picture: ""
          }
        }
      );
      Notify("Das Buchen ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
      Set(varBuchung; LookUp(colKollision; Person.Email = User().Email && Startzeit = varBuchStart && Endzeit = varBuchEnde));;
      If(
        IsBlank(varBuchung.ID);
        Notify("Die Buchung ist nicht angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
        Set(varBuchungID; varBuchung.ID);;
        If(
          !IsBlank(LookUp(colKollision; ID < varBuchungID).ID);
          Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
          Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr"; NotificationType.Success);;
          Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerl1.OnSelect`** (H5)

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
    Set(varTischName; varBuchung.Tisch.Value);;
    Set(varEndeAlt; varBuchung.Endzeit);;
    Set(varNeuEnde; DateAdd(varEndeAlt; 60; TimeUnit.Minutes));;
    Set(varTagesEnde; DateTime(Year(varBuchung.Startzeit); Month(varBuchung.Startzeit); Day(varBuchung.Startzeit); 22; 0; 0));;
    If(
      varEndeAlt <= Now();
      Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
      varNeuEnde > varTagesEnde;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
      Notify("Der Tisch ist in dieser Zeit schon belegt."; NotificationType.Warning);
      !IsBlank(LookUp(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      IfError(
        Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
        Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
        If(
          LookUp(colKollision; ID = varBuchungID).Endzeit <> varNeuEnde;
          Notify("Die Verlängerung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning);
          !IsBlank(LookUp(colKollision; ID <> varBuchungID).ID);
          IfError(
            Patch(Tischbuchungen; LookUp(Tischbuchungen; ID = varBuchungID); { Endzeit: varEndeAlt });
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Bitte deine Buchung prüfen, sie überschneidet sich."; NotificationType.Error);
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Die Verlängerung wurde zurückgenommen."; NotificationType.Error)
          );
          Notify("Buchung verlängert."; NotificationType.Success);;
          Set(varZeigeVerwalten; false)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerl2.OnSelect`** (H5)

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchung; LookUp(Tischbuchungen; ID = varBuchungID));;
  If(
    IsBlank(varBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wird aktualisiert."; NotificationType.Warning);; Set(varZeigeVerwalten; false);
    Set(varTischName; varBuchung.Tisch.Value);;
    Set(varEndeAlt; varBuchung.Endzeit);;
    Set(varNeuEnde; DateAdd(varEndeAlt; 120; TimeUnit.Minutes));;
    Set(varTagesEnde; DateTime(Year(varBuchung.Startzeit); Month(varBuchung.Startzeit); Day(varBuchung.Startzeit); 22; 0; 0));;
    If(
      varEndeAlt <= Now();
      Notify("Diese Buchung ist bereits beendet."; NotificationType.Information);; Set(varZeigeVerwalten; false);
      varNeuEnde > varTagesEnde;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
      Notify("Der Tisch ist in dieser Zeit schon belegt."; NotificationType.Warning);
      !IsBlank(LookUp(Tischbuchungen; Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      IfError(
        Patch(Tischbuchungen; varBuchung; { Endzeit: varNeuEnde });
        Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));;
        If(
          LookUp(colKollision; ID = varBuchungID).Endzeit <> varNeuEnde;
          Notify("Die Verlängerung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning);
          !IsBlank(LookUp(colKollision; ID <> varBuchungID).ID);
          IfError(
            Patch(Tischbuchungen; LookUp(Tischbuchungen; ID = varBuchungID); { Endzeit: varEndeAlt });
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Bitte deine Buchung prüfen, sie überschneidet sich."; NotificationType.Error);
            Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Die Verlängerung wurde zurückgenommen."; NotificationType.Error)
          );
          Notify("Buchung verlängert."; NotificationType.Success);;
          Set(varZeigeVerwalten; false)
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnEincheckenH.OnSelect`** (H6)

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchungID; ThisItem.ID);;
  With(
    { frisch: LookUp(Tischbuchungen; ID = varBuchungID) };
    If(
      IsBlank(frisch.ID);
      Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);
      If(
        frisch.CheckedIn;
        Notify("Du bist bereits eingecheckt."; NotificationType.Information);
        If(
          Now() < DateAdd(frisch.Startzeit; -30; TimeUnit.Minutes) || Now() > frisch.Endzeit;
          Notify("Einchecken ist erst ab 30 Minuten vor Beginn und nur bis zum Ende moeglich."; NotificationType.Warning);
          IfError(
            Patch(Tischbuchungen; frisch; { CheckedIn: true });
            Notify("Einchecken fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
            If(
              LookUp(Tischbuchungen; ID = varBuchungID).CheckedIn;
              Notify("Eingecheckt."; NotificationType.Success);
              Notify("Der Check-in ist nicht angekommen. Bitte aktualisieren und erneut versuchen."; NotificationType.Warning)
            )
          )
        )
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnEincheckenH.DisplayMode`** (H6)

```
If(
  ThisItem.CheckedIn;
  DisplayMode.Disabled;
  If(
    varIsLoading;
    DisplayMode.Disabled;
    If(
      Now() >= DateAdd(ThisItem.Startzeit; -30; TimeUnit.Minutes) && Now() <= ThisItem.Endzeit;
      DisplayMode.Edit;
      DisplayMode.Disabled
    )
  )
)
```

**`btnEincheckenH.Text`** (H6)

```
If(ThisItem.CheckedIn; "Eingecheckt"; "Einchecken")
```

**`lblStatusH.Text`** (H6)

```
If(ThisItem.CheckedIn; "Eingecheckt"; "Nicht eingecheckt")
```

**`lblStatusH.Color`** (H6)

```
If(ThisItem.CheckedIn; RGBA(0; 169; 107; 1); RGBA(255; 165; 0; 1))
```

**`ddStart.Items`** (H7)

```
With(
  { ab: If(ddDatum.Selected.Tag = Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); 8 * 60) };
  ForAll(
    Sequence(Max(0; (21 * 60 + 30 - ab) / 30 + 1); 0) As n;
    {
      Value: Text(Time(RoundDown((ab + n.Value * 30) / 60; 0); Mod(ab + n.Value * 30; 60); 0); "hh:mm");
      Min: ab + n.Value * 30
    }
  )
)
```

## Anhang B: Maschinelle Prüfung

```
17 Properties in 7 Schritten, kein neues Steuerelement. Ausgangslage: Handy-Export 08.10. (11:51).
Je Property: Klammern, Rückübersetzung, keine Kommentare, Steuerelemente vorhanden, jede var/col wird gesetzt, varFreigabeGrenze vor Gebrauch gesetzt.
Jedes Patch/Remove hinter der Sperre. Stornieren/Beenden mit Eigentümerprüfung davor. Nachprüfungen (Buchen, Verlängern, Einchecken) pro Klick eindeutig und ohne verfallene Buchungen.
Abfragen auf Tischbuchungen (ohne reine ID-Abfragen): 14, jede eingeordnet (Freigabe-Regel lokal oder begründet ausgenommen: galHeute.Items, galMeine.Items).
Prüfung: 0 Fehler
```

Bewusst ohne Freigabe-Regel:

- `galHeute.Items`: eigene Buchungen heute; verfallene bleiben sichtbar (Status „Verfallen“)
- `galMeine.Items`: eigene Buchungen; verfallene dürfen storniert werden
