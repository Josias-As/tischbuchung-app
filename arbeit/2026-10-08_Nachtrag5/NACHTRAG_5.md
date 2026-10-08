# Nachtrag 5: Stornieren mit Bestätigung und Nachholen nach dem Abgleich mit dem Export (08.10.2026)

Für den Desktop-Chat. **Grundlage ist der Export „PCAppfertig“ vom 08.10., 14:26** (= Studio-Stand). Jeder Diff rechnet gegen diesen Export, nicht gegen einen Plan. Erzeugt und geprüft mit `werkzeuge/nachtrag5.py`. Kennzeichnung: **belegt** (Export), **gemessen** (Monitor 07.10.), **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **N1/N2 Stornieren mit Bestätigung** (Auftrag 2a). Gilt für alle drei Knöpfe, ohne neues Steuerelement und ohne zusätzliche Abfrage:
  - Der erste Tipp schreibt nichts. Der Knopf zeigt dann „Ja, stornieren“ bzw. „Ja, 3 stornieren“, dazu kommt eine Meldung.
  - Erst ein zweiter Tipp frühestens nach 1 Sekunde storniert. Ein Doppelklick bestätigt also nicht.
  - Die Bestätigung führt die Export-Fassung **unverändert** aus. Maschinell geprüft: Sie ist nur eingerückt.
- **N3:** Die Frage wird beim Öffnen eines Verwalten-Dialogs zurückgesetzt. Beim Mehrfach-Storno gilt sie nur für genau die Auswahl, für die gefragt wurde. Ändert sich die Auswahl, fragt die App neu.
- **N4 Nachholen:** Drei Teile, die laut Rückmeldung eingefügt sind, fehlen im Export (**belegt**):
  - **S3b** (`lblStatusHeute`, „Verfallen“ ohne Tippen).
  - **F5** an `btn5Std.Fill`: Die Farbe zählt verfallene Buchungen noch als belegt, der Knopf selbst ist aber bedienbar.
  - **G25** an `recBuchungDanach1.Visible`: eine Abfrage beim Start.
- **N5 Raumcode:** Die letzten 3 Abfragen auf `Raumbuchungen` beim Start (**gemessen** 07.10.: `recBuchungDavor1.X`, `recBuchungDanach1.X`/`.Width`) und `recBuchungDavor1.Width` laufen nur noch, wenn die Raumbestätigung offen ist. Zusammen mit N4 fragt die App beim Start den Raumcode **gar nicht mehr** ab (geschlussfolgert aus den Formeln).
- **Umfang:** 16 Properties, kein neues Steuerelement. Maschinell 0 Fehler. In Studio ist nichts getestet.
- **Einzel-Storno auch mit Bestätigung, Begründung:**
  - `Remove` löscht endgültig, zurück geht es nur über den SharePoint-Papierkorb.
  - Der Knopf liegt neben „Verlängern“.
  - Die Handy-App fragt vor dem Stornieren (Regel V8, von Josias bestätigt).
  - Beide Apps sollen sich gleich verhalten. Der Aufwand pro Knopf sind 2 Properties.
- **Abweichung vom Auftrag:** Der Knopftext ist „Ja, stornieren“ statt „Wirklich stornieren?“. `btnStornieren` ist etwa 137 px breit (`(450 − 40) / 3`, belegt), „Wirklich stornieren?“ würde dort umbrechen (geschlussfolgert). Die Frage steht in der Meldung.

## 1. Abgleich Export ↔ gemeldeter Stand (belegt)
Verglichen wurde jede Property des Exports mit dem Stand, den die Rückmeldung als eingefügt nennt: Export 07.10. + G1 G2 G3 G6 (Nachtrag 4) G7 G9–G13 G15–G20 G23 G24 G25 + F2.1 F1–F7 + Grundriss-Sperre S1–S4.

| Abweichung | Bewertung | Was tun |
|---|---|---|
| `lblStatusHeute.Text`/`.Color` in F7-Fassung statt S3b | „Verfallen“ erscheint erst nach dem nächsten Laden. Einchecken prüft frisch und meldet „Zu spät“, es entsteht also kein falscher Check-in | **N4** |
| `btn5Std.Fill` in G-Fassung statt F5 (`DisplayMode` ist F5) | Der Knopf ist bedienbar, sieht aber belegt aus, wenn dort nur eine verfallene Buchung liegt | **N4** |
| `recBuchungDanach1.Visible` ohne G25-Bedingung (die anderen 5 G25-Properties sind drin) | 1 Abfrage auf `Raumbuchungen` beim Start | **N4** |
| Timer heißt `Timer1`, nicht `tmrAktualisieren` | Funktion gleich: `OnTimerEnd` = S3, `Duration` 15000. Keine Formel liest den Namen. Nur die Dokumente sagen `tmrAktualisieren` | nichts. Umbenennen ist optional |
| Zusätzliches Symbol `icoAktualisierenGrundriss` in `conGrundriss` (17. Ladestelle) | `OnSelect` ist **zeichengleich mit `Icon1_1`** (S2-Fassung, mit Stempel). Es liegt unter der Sperrfläche | **behalten**, passt so |
| `btnGrundrissSperre`: Ecken 10 (Standard), kein `AccessibleLabel`. `btnGrundrissAktualisieren` ist 240 × 30 statt 280 × 56 | Nur Optik. Die Fläche hat runde Ecken | optional |
| G23 (Farben), Minuszeichen, Texte „Keine Buchungen“, Positionen im Panel | Josias' bewusste Entscheidungen | nichts |

**Handy-App:** Der Export 08.10. 14:25 entspricht Umbauplan v2 H1–H7 **genau**. Die einzige Ausnahme ist die zusammengeführte Profilfarbe (`App.OnStart`, `btnInitialen_1`), wie gemeldet.

## 2. Schritte (Reihenfolge N1 → N5)

### N1 Stornieren mit Bestätigung: Dashboard und Tab

#### `btnStornieren.OnSelect`

Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **ganze Property ersetzen** · Herkunft: N1

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -2,26 +2,33 @@
   !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
-  Set(varIsLoading; true);;
-  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
   If(
-    IsBlank(varStornoBuchung.ID);
-    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
-    Set(varZeigeVerwalten; false);
-    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
-    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
-    IfError(
-      Remove(Tischbuchungen; varStornoBuchung);
-      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-      If(
-        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
-        Notify("Buchung storniert."; NotificationType.Success);;
-        Set(varZeigeVerwalten; false);
-        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+    !(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchung.ID);
+    Set(varStornoFrageID; varSelectedBuchung.ID);;
+    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
+    Notify("Wirklich stornieren? Zum Bestätigen auf „Ja, stornieren“ tippen."; NotificationType.Information);
+    Set(varStornoFrageID; 0);;
+    Set(varIsLoading; true);;
+    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
+    If(
+      IsBlank(varStornoBuchung.ID);
+      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+      Set(varZeigeVerwalten; false);
+      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
+      Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
+      IfError(
+        Remove(Tischbuchungen; varStornoBuchung);
+        Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+        If(
+          IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
+          Notify("Buchung storniert."; NotificationType.Success);;
+          Set(varZeigeVerwalten; false);
+          Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+        )
       )
-    )
-  );;
-  Refresh(Tischbuchungen);;
-  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
-  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
-  Set(varIsLoading; false)
+    );;
+    Refresh(Tischbuchungen);;
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
+    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+    Set(varIsLoading; false)
+  )
 )
```

Vollständiger Block zum Einfügen:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  If(
    !(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchung.ID);
    Set(varStornoFrageID; varSelectedBuchung.ID);;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Notify("Wirklich stornieren? Zum Bestätigen auf „Ja, stornieren“ tippen."; NotificationType.Information);
    Set(varStornoFrageID; 0);;
    Set(varIsLoading; true);;
    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
    If(
      IsBlank(varStornoBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwalten; false);
      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
      Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
      IfError(
        Remove(Tischbuchungen; varStornoBuchung);
        Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        If(
          IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
          Notify("Buchung storniert."; NotificationType.Success);;
          Set(varZeigeVerwalten; false);
          Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
        )
      )
    );;
    Refresh(Tischbuchungen);;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  )
)
```

#### `btnStornieren.Text`

Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **ganze Property ersetzen** · Herkunft: N1

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-"Stornieren"
+If(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchung.ID; "Ja, stornieren"; "Stornieren")
```

Vollständiger Block zum Einfügen:

```
If(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchung.ID; "Ja, stornieren"; "Stornieren")
```

#### `btnStornieren_1.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **ganze Property ersetzen** · Herkunft: N1

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -2,26 +2,33 @@
   !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
-  Set(varIsLoading; true);;
-  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
   If(
-    IsBlank(varStornoBuchung.ID);
-    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
-    Set(varZeigeVerwaltenTab; false);
-    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
-    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
-    IfError(
-      Remove(Tischbuchungen; varStornoBuchung);
-      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-      If(
-        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
-        Notify("Buchung storniert."; NotificationType.Success);;
-        Set(varZeigeVerwaltenTab; false);
-        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+    !(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchungTab.ID);
+    Set(varStornoFrageID; varSelectedBuchungTab.ID);;
+    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
+    Notify("Wirklich stornieren? Zum Bestätigen auf „Ja, stornieren“ tippen."; NotificationType.Information);
+    Set(varStornoFrageID; 0);;
+    Set(varIsLoading; true);;
+    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
+    If(
+      IsBlank(varStornoBuchung.ID);
+      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+      Set(varZeigeVerwaltenTab; false);
+      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
+      Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
+      IfError(
+        Remove(Tischbuchungen; varStornoBuchung);
+        Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+        If(
+          IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
+          Notify("Buchung storniert."; NotificationType.Success);;
+          Set(varZeigeVerwaltenTab; false);
+          Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+        )
       )
-    )
-  );;
-  Refresh(Tischbuchungen);;
-  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
-  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
-  Set(varIsLoading; false)
+    );;
+    Refresh(Tischbuchungen);;
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
+    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+    Set(varIsLoading; false)
+  )
 )
```

Vollständiger Block zum Einfügen:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  If(
    !(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchungTab.ID);
    Set(varStornoFrageID; varSelectedBuchungTab.ID);;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Notify("Wirklich stornieren? Zum Bestätigen auf „Ja, stornieren“ tippen."; NotificationType.Information);
    Set(varStornoFrageID; 0);;
    Set(varIsLoading; true);;
    Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
    If(
      IsBlank(varStornoBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwaltenTab; false);
      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
      Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
      IfError(
        Remove(Tischbuchungen; varStornoBuchung);
        Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        If(
          IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
          Notify("Buchung storniert."; NotificationType.Success);;
          Set(varZeigeVerwaltenTab; false);
          Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
        )
      )
    );;
    Refresh(Tischbuchungen);;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  )
)
```

#### `btnStornieren_1.Text`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **ganze Property ersetzen** · Herkunft: N1

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-"Stornieren"
+If(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchungTab.ID; "Ja, stornieren"; "Stornieren")
```

Vollständiger Block zum Einfügen:

```
If(varStornoFrageID > 0 && varStornoFrageID = varSelectedBuchungTab.ID; "Ja, stornieren"; "Stornieren")
```

**Ablauf beim Tippen:**
1. **Erster Tipp:** Er setzt `varStornoFrageID` auf die ID der offenen Buchung und sperrt 1 Sekunde. Dazu kommt die Meldung „Wirklich stornieren? …“, und der Knopf zeigt „Ja, stornieren“. Es gibt keine Abfrage und kein Schreiben.
2. **Zweiter Tipp** (nach 1 s, gleiche Buchung): Er setzt die Frage zurück und führt die Export-Fassung aus: frisch lesen, nur eigene, `IfError`, Nachlese, Ladezeile mit Stempel.
3. **Doppelklick:** Der zweite Klick fällt in die 1-s-Sperre und tut nichts.

**Test:**
1. Dashboard → Pfeil bei einer eigenen Buchung → „Stornieren“ → Meldung, Knopf „Ja, stornieren“, die Buchung ist noch da.
2. „Ja, stornieren“ → „Buchung storniert.“
3. Neu buchen, Dialog öffnen, „Stornieren“ doppelklicken → nur die Frage, nichts gelöscht.
4. Dasselbe im Tab „Buchungen“ (`btnStornieren_1`).

### N2 Mehrfach-Stornieren mit Bestätigung

#### `btnStornierenKlein.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein` · **ganze Property ersetzen** · Herkunft: N2

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -2,40 +2,47 @@
   !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
-  Set(varIsLoading; true);;
-  ClearCollect(
-      colStornoFrisch;
-      Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
-  );;
-  ClearCollect(
-      colStornoZiele;
-      Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
-  );;
   If(
-      CountRows(colAusgewaehlteBuchungen) = 0;
-      Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
-      If(
-          CountRows(colStornoZiele) = 0;
-          Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
-          IfError(
-              Remove(Tischbuchungen; colStornoZiele);
-              Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
-              If(
-                  CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
-                  Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
-                  Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
-              )
-          )
-      )
-  );;
-  Refresh(Tischbuchungen);;
-  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
-  Clear(colStornoFrisch);;
-  Clear(colStornoZiele);;
-  Clear(colAusgewaehlteBuchungen);;
-  Set(varGeklickteBuchungKlein; Blank());;
-  Set(varZeigeVerwaltenKlein; false);;
-  Set(varAuswahlModusAktiv; false);;
-  Reset(tglAuswahlModus);;
-  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
-  Set(varIsLoading; false)
+    CountRows(colAusgewaehlteBuchungen) > 0 && varStornoFrageAuswahl <> Concat(colAusgewaehlteBuchungen; Text(ID); ",");
+    Set(varStornoFrageAuswahl; Concat(colAusgewaehlteBuchungen; Text(ID); ","));;
+    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
+    Notify("Wirklich " & CountRows(colAusgewaehlteBuchungen) & If(CountRows(colAusgewaehlteBuchungen) = 1; " Buchung"; " Buchungen") & " stornieren? Zum Bestätigen noch einmal tippen."; NotificationType.Information);
+    Set(varStornoFrageAuswahl; "");;
+    Set(varIsLoading; true);;
+    ClearCollect(
+        colStornoFrisch;
+        Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
+    );;
+    ClearCollect(
+        colStornoZiele;
+        Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
+    );;
+    If(
+        CountRows(colAusgewaehlteBuchungen) = 0;
+        Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
+        If(
+            CountRows(colStornoZiele) = 0;
+            Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
+            IfError(
+                Remove(Tischbuchungen; colStornoZiele);
+                Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
+                If(
+                    CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
+                    Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
+                    Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
+                )
+            )
+        )
+    );;
+    Refresh(Tischbuchungen);;
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
+    Clear(colStornoFrisch);;
+    Clear(colStornoZiele);;
+    Clear(colAusgewaehlteBuchungen);;
+    Set(varGeklickteBuchungKlein; Blank());;
+    Set(varZeigeVerwaltenKlein; false);;
+    Set(varAuswahlModusAktiv; false);;
+    Reset(tglAuswahlModus);;
+    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+    Set(varIsLoading; false)
+  )
 )
```

Vollständiger Block zum Einfügen:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  If(
    CountRows(colAusgewaehlteBuchungen) > 0 && varStornoFrageAuswahl <> Concat(colAusgewaehlteBuchungen; Text(ID); ",");
    Set(varStornoFrageAuswahl; Concat(colAusgewaehlteBuchungen; Text(ID); ","));;
    Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
    Notify("Wirklich " & CountRows(colAusgewaehlteBuchungen) & If(CountRows(colAusgewaehlteBuchungen) = 1; " Buchung"; " Buchungen") & " stornieren? Zum Bestätigen noch einmal tippen."; NotificationType.Information);
    Set(varStornoFrageAuswahl; "");;
    Set(varIsLoading; true);;
    ClearCollect(
        colStornoFrisch;
        Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
    );;
    ClearCollect(
        colStornoZiele;
        Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
    );;
    If(
        CountRows(colAusgewaehlteBuchungen) = 0;
        Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
        If(
            CountRows(colStornoZiele) = 0;
            Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
            IfError(
                Remove(Tischbuchungen; colStornoZiele);
                Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
                If(
                    CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
                    Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
                    Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
                )
            )
        )
    );;
    Refresh(Tischbuchungen);;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
    Clear(colStornoFrisch);;
    Clear(colStornoZiele);;
    Clear(colAusgewaehlteBuchungen);;
    Set(varGeklickteBuchungKlein; Blank());;
    Set(varZeigeVerwaltenKlein; false);;
    Set(varAuswahlModusAktiv; false);;
    Reset(tglAuswahlModus);;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  )
)
```

#### `btnStornierenKlein.Text`

Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein` · **ganze Property ersetzen** · Herkunft: N2

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-"Stornieren"
+If(CountRows(colAusgewaehlteBuchungen) > 0 && varStornoFrageAuswahl = Concat(colAusgewaehlteBuchungen; Text(ID); ","); "Ja, " & CountRows(colAusgewaehlteBuchungen) & " stornieren"; "Stornieren")
```

Vollständiger Block zum Einfügen:

```
If(CountRows(colAusgewaehlteBuchungen) > 0 && varStornoFrageAuswahl = Concat(colAusgewaehlteBuchungen; Text(ID); ","); "Ja, " & CountRows(colAusgewaehlteBuchungen) & " stornieren"; "Stornieren")
```

**Ablauf beim Tippen:**
1. **Erster Tipp:** Er merkt sich die Auswahl als Text der IDs (`Concat`, lokal, ohne Abfrage) und sperrt 1 Sekunde. Meldung: „Wirklich 3 Buchungen stornieren? …“, der Knopf zeigt „Ja, 3 stornieren“.
2. **Zweiter Tipp** bei **gleicher** Auswahl: Die Export-Fassung läuft unverändert.
3. **Auswahl geändert** (Haken gesetzt oder entfernt, „Alle auswählen“): Der Text passt nicht mehr, der Knopf zeigt wieder „Stornieren“, und der nächste Tipp fragt neu (belegt aus der Formel).
4. **Keine Auswahl:** keine Frage, die bisherige Meldung „Keine Buchungen ausgewählt.“

**Test:**
1. Tab „Buchungen“ → Mehrfachauswahl → 3 Buchungen anhaken → eine antippen → „Stornieren“ → Meldung mit „3“, Knopf „Ja, 3 stornieren“.
2. Einen vierten Haken setzen → der Knopf zeigt „Stornieren“. Tippen → neue Frage mit „4“.
3. „Ja, 4 stornieren“ → „4 Buchungen storniert.“
4. Doppelklick auf „Stornieren“ bei neuer Auswahl → nur die Frage.

### N3 Frage beim Öffnen zurücksetzen

#### `btnVerwalten.OnSelect`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten` · **ganze Property ersetzen** · Herkunft: N3

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1,2 @@
+Set(varStornoFrageID; 0);;
 Set(varSelectedBuchung; ThisItem);;
```

Vollständiger Block zum Einfügen:

```
Set(varStornoFrageID; 0);;
Set(varSelectedBuchung; ThisItem);;
Set(varVerlTisch; ThisItem.Tisch.Value);;
Set(varVerlEndeAlt; ThisItem.Endzeit);;
Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false)
```

#### `btnVerwalten_2.OnSelect`

Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2` · **ganze Property ersetzen** · Herkunft: N3

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1,3 @@
+Set(varStornoFrageID; 0);;
+Set(varStornoFrageAuswahl; "");;
 If(
```

Vollständiger Block zum Einfügen:

```
Set(varStornoFrageID; 0);;
Set(varStornoFrageAuswahl; "");;
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varVerlTisch; ThisItem.Tisch.Value);;
  Set(varVerlEndeAlt; ThisItem.Endzeit);;
  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
  RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

Beide Formeln bekommen nur vorne die Rücksetzung, der Rest ist der Export (maschinell geprüft).

**Test:** Dashboard: „Stornieren“ (Frage), Dialog schließen, **dieselbe** Buchung wieder öffnen → der Knopf zeigt „Stornieren“, der erste Tipp fragt erneut.

### N4 Nachholen: im Export fehlende Teile (S3b, F5, G25)

#### `lblStatusHeute.Text`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **ganze Property ersetzen** · Herkunft: N4 (= Grundriss-Sperre S3b)

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; "Verfallen"; "Einchecken")
+If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes); "Verfallen"; "Einchecken")
```

Vollständiger Block zum Einfügen:

```
If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes); "Verfallen"; "Einchecken")
```

#### `lblStatusHeute.Color`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **ganze Property ersetzen** · Herkunft: N4 (= Grundriss-Sperre S3b)

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; ColorValue("#A6A6A6"); ColorValue("#FFA500"))
+If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes); ColorValue("#A6A6A6"); ColorValue("#FFA500"))
```

Vollständiger Block zum Einfügen:

```
If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes); ColorValue("#A6A6A6"); ColorValue("#FFA500"))
```

#### `btn5Std.Fill`

Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · Herkunft: N4 (= Paket F2.1 F5)

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -18,3 +18,3 @@
           If(
-            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
+            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
             ColorFade(ColorValue("#00A96B"); 70%);
```

Vollständiger Block zum Einfügen:

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

#### `recBuchungDanach1.Visible`

Ort: `Screen1 > conRaumBestätigen > recBuchungDanach1` · **ganze Property ersetzen** · Herkunft: N4 (= Gesamtplan G25)

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes))) > 0
+varZeigeRaumBestätigung && CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes))) > 0
```

Vollständiger Block zum Einfügen:

```
varZeigeRaumBestätigung && CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes))) > 0
```

Die Blöcke sind **zeichengleich** mit S3b (Grundriss-Sperre), F5 (F2.1) und G25 (Gesamtplan). Die Diffs zeigen, was im Export noch alt ist.

**Test:**
- **S3b:** Siehe Testbogen Punkt 9.
- **F5:** Panel „Tisch buchen“, Tisch mit nur einer verfallenen Buchung (Testmodus) → „5 Std“ blau und bedienbar.
- **G25:** Monitor beim Start: keine Zeile `recBuchungDanach1`.

### N5 Raumcode: letzte Startabfragen abschalten

#### `recBuchungDavor1.X`

Ort: `Screen1 > conRaumBestätigen > recBuchungDavor1` · **ganze Property ersetzen** · Herkunft: N5

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1,10 +1,14 @@
-With(
-  {
-    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
-    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
-  };
+If(
+  varZeigeRaumBestätigung;
   With(
-    { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
-    recZeitleisteBg.X + Max(0; DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes)) / gesamtFenster * recZeitleisteBg.Width
-  )
+    {
+      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
+      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
+    };
+    With(
+      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
+      recZeitleisteBg.X + Max(0; DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes)) / gesamtFenster * recZeitleisteBg.Width
+    )
+  );
+  0
 )
```

Vollständiger Block zum Einfügen:

```
If(
  varZeigeRaumBestätigung;
  With(
    {
      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
    };
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
      recZeitleisteBg.X + Max(0; DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes)) / gesamtFenster * recZeitleisteBg.Width
    )
  );
  0
)
```

#### `recBuchungDavor1.Width`

Ort: `Screen1 > conRaumBestätigen > recBuchungDavor1` · **ganze Property ersetzen** · Herkunft: N5

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1,10 +1,14 @@
-With(
-  {
-    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
-    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
-  };
+If(
+  varZeigeRaumBestätigung;
   With(
-    { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
-    (DateDiff(Max(fensterStart; buchung.Startzeit); buchung.Endzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
-  )
+    {
+      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
+      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
+    };
+    With(
+      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
+      (DateDiff(Max(fensterStart; buchung.Startzeit); buchung.Endzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
+    )
+  );
+  0
 )
```

Vollständiger Block zum Einfügen:

```
If(
  varZeigeRaumBestätigung;
  With(
    {
      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
    };
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
      (DateDiff(Max(fensterStart; buchung.Startzeit); buchung.Endzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
    )
  );
  0
)
```

#### `recBuchungDanach1.X`

Ort: `Screen1 > conRaumBestätigen > recBuchungDanach1` · **ganze Property ersetzen** · Herkunft: N5

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1,13 +1,17 @@
-With(
-  {
-    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
-    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
-  };
+If(
+  varZeigeRaumBestätigung;
   With(
-    { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
+    {
+      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
+      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
+    };
     With(
-      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
-      recZeitleisteBg.X + (DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
+      { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
+      With(
+        { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
+        recZeitleisteBg.X + (DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
+      )
     )
-  )
+  );
+  0
 )
```

Vollständiger Block zum Einfügen:

```
If(
  varZeigeRaumBestätigung;
  With(
    {
      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
    };
    With(
      { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
      With(
        { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
        recZeitleisteBg.X + (DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
      )
    )
  );
  0
)
```

#### `recBuchungDanach1.Width`

Ort: `Screen1 > conRaumBestätigen > recBuchungDanach1` · **ganze Property ersetzen** · Herkunft: N5

Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):

```diff
@@ -1,13 +1,17 @@
-With(
-  {
-    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
-    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
-  };
+If(
+  varZeigeRaumBestätigung;
   With(
-    { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
+    {
+      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
+      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
+    };
     With(
-      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
-      (DateDiff(buchung.Startzeit; Min(buchung.Endzeit; fensterEnde); TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
+      { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
+      With(
+        { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
+        (DateDiff(buchung.Startzeit; Min(buchung.Endzeit; fensterEnde); TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
+      )
     )
-  )
+  );
+  0
 )
```

Vollständiger Block zum Einfügen:

```
If(
  varZeigeRaumBestätigung;
  With(
    {
      fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
      gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
    };
    With(
      { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
      With(
        { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
        (DateDiff(buchung.Startzeit; Min(buchung.Endzeit; fensterEnde); TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
      )
    )
  );
  0
)
```

Jede der 4 Formeln steht unverändert in `If(varZeigeRaumBestätigung; …; 0)`. Ist die Raumbestätigung zu, sind die Rechtecke ohnehin unsichtbar (`Visible` mit derselben Bedingung, belegt). Breite und Position 0 sieht also niemand.

**Test:** Monitor beim Start: keine Abfrage auf `Raumbuchungen` oder `Räume`. Der Raumcode ist nicht erreichbar, ein Funktionstest entfällt.

## 3. Abschluss-Testbogen (ersetzt F2.1 Abschnitt 6, Auftrag 2b)
Stand: F2.1 F1–F7, Grundriss-Sperre S1–S4, Nachtrag 5. **F8 gibt es nicht mehr**, der Timer (`Timer1`) ist S3.

**Vorbereitung:**
1. Testknopf `btnTestFreigabe` **außerhalb** von `conGrundriss` anlegen, `OnSelect`: `Set(varFreigabeMinuten; 1)`. In der Vorschau tippen. **`App.OnStart` nicht ändern.**
2. Testbuchungen immer zur **nächsten halben Stunde** anlegen. Die Startliste hat nur halbe Stunden.
3. „Verfallen“ heißt im Testmodus: Beginn **und** Buchungszeitpunkt liegen mehr als 1 Minute zurück.
4. Tests 2–5 bauen aufeinander auf. Wartezeit bis T + 1 Min: bis zu 30 Minuten. Tests 6–11 können in dieser Zeit laufen.
5. Verlängern über eine **folgende** verfallene Buchung lässt sich nicht testen: Eine Buchung, die schon begonnen hat, kann nicht hinter einer noch laufenden eigenen liegen. Test 5 verlängert deshalb in eine **lange** verfallene Buchung hinein, die schon läuft.

| ✓ | Test | Erwartung |
|---|---|---|
| ☐ | 1 App-Prüfung, OnStart ausführen, Vorschau | keine roten Fehler, kein Aufblitzen der Grundriss-Sperre, Check-in-Frage beim Start, wenn eine eigene Buchung ansteht |
| ☐ | 2 Kollege (oder zweites Konto) bucht Tisch X von **T** (nächste halbe Stunde) bis **T + 3 Std** und checkt nicht ein. Testknopf tippen. Ab T + 1 Min: Aktualisieren | Kachel X **grün**, Klick → Buchungsdialog (F3) |
| ☐ | 3 Du buchst X von T + 30 Min bis T + 60 Min | „Gebucht …“, die Buchung steht **ohne Aktualisieren** in der Liste (F4, Nachtrag 4) |
| ☐ | 4 Panel „Tisch buchen“: heute, Beginn T + 60 Min | X steht in der Liste, „5 Std“ blau und bedienbar, solange bis 22:00 Platz ist (F5, N4) |
| ☐ | 5 Deine Buchung aus 3 im Dashboard verlängern (+1 Std). Danach eine zweite eigene Buchung an einem anderen Tisch von T + 90 bis T + 120 Min anlegen und die Buchung aus 3 noch einmal verlängern | erst „verlängert“, weil die Buchung des Kollegen verfallen ist (F6), dann die Meldung „zwei Tische“ |
| ☐ | 6 Einchecken: eigene Buchung zur nächsten halben Stunde. Mehr als 30 Min vorher, dann im Fenster, dann (im Testmodus) ab 1 Min nach Beginn ohne Check-in | „erst ab 30 Minuten vor Beginn“ → „Eingecheckt.“ bzw. „**Zu spät** …“ (F7) |
| ☐ | 7 Auschecken nach Beginn: „Auschecken“ → „Wirklich auschecken?“ → tippen. Doppelklick testen | Ende = jetzt. Ein Doppelklick checkt nicht aus (F7) |
| ☐ | 8 Erinnerung (ersetzt „F8 Timer aktualisiert“): eigene Buchung zur nächsten halben Stunde, auf dem Dashboard bleiben, kein Dialog offen | Check-in-Frage nach höchstens 15 s, nur einmal (Grundriss-Sperre Test 8) |
| ☐ | 9 Status ohne Tippen: eigene Buchung zur nächsten halben Stunde, nicht einchecken, Testknopf | ab 1 Min nach Beginn „Verfallen“ (grau) **ohne Tippen**, nach höchstens 15 s (Grundriss-Sperre Test 9, braucht N4) |
| ☐ | 10 Grundriss-Sperre: 2:15 Min warten, Kachel und Stockwerk tippen, dann „Grundriss aktualisieren“ | Fläche und Knopf erscheinen, darunter passiert nichts, nach dem Tippen ist die Fläche weg |
| ☐ | 11 Stornieren Dashboard, Tab, Mehrfach mit Bestätigung, Doppelklick (N1–N3) | siehe Tests N1–N3 |
| ☐ | 12 **Testknopf löschen.** In `App.OnStart` steht `Set(varFreigabeMinuten; 30)` und `Set(varGrundrissSperreSekunden; 120)`. Keine Test-Steuerelemente mehr in der Strukturansicht | |
| ☐ | 13 Alle Testbuchungen stornieren (eigene über den Mehrfach-Storno, die des Kollegen durch ihn) | Grundriss und Listen ohne Testbuchungen |
| ☐ | 14 Sicherung (Datei → Speichern unter → Dieser Computer, `.msapp`), App-Prüfung ohne rote Fehler, **Veröffentlichen** | |

## 4. UNSICHER
| Nr | Was | Test |
|---|---|---|
| N-U1 | Passt „Ja, stornieren“ in `btnStornieren` (etwa 137 px) ohne Umbruch? (geschlussfolgert) | Test N1. Wenn es umbricht: `btnStornieren.Size` auf 13 |
| N-U2 | `Concat(…; Text(ID); ",")` ist in dieser App zulässig (powerfxv1 aus). Geschlussfolgert, `Concat` ist eine Standardfunktion | App-Prüfung nach N2 |

## 5. Rückfall
- N1–N3 **zusammen** auf die Fassungen in Anhang A zurücksetzen. Ohne N3 bleibt eine alte Frage beim erneuten Öffnen bestehen. Harmlos, weil der Knopf dann „Ja, stornieren“ zeigt.
- N4 und N5 einzeln auf Anhang A zurücksetzen.

## Anhang A: Fassungen im Export 08.10. 14:26 (Rückfall)

**`btnStornieren.OnSelect`** (N1)

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varStornoBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwalten; false);
    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
    IfError(
      Remove(Tischbuchungen; varStornoBuchung);
      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      If(
        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
        Notify("Buchung storniert."; NotificationType.Success);;
        Set(varZeigeVerwalten; false);
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
      )
    )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnStornieren.Text`** (N1)

```
"Stornieren"
```

**`btnStornieren_1.OnSelect`** (N1)

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
  If(
    IsBlank(varStornoBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwaltenTab; false);
    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
    IfError(
      Remove(Tischbuchungen; varStornoBuchung);
      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      If(
        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
        Notify("Buchung storniert."; NotificationType.Success);;
        Set(varZeigeVerwaltenTab; false);
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
      )
    )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnStornieren_1.Text`** (N1)

```
"Stornieren"
```

**`btnStornierenKlein.OnSelect`** (N2)

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  ClearCollect(
      colStornoFrisch;
      Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
  );;
  ClearCollect(
      colStornoZiele;
      Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
  );;
  If(
      CountRows(colAusgewaehlteBuchungen) = 0;
      Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
      If(
          CountRows(colStornoZiele) = 0;
          Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
          IfError(
              Remove(Tischbuchungen; colStornoZiele);
              Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
              If(
                  CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
                  Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
                  Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
              )
          )
      )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  Clear(colStornoFrisch);;
  Clear(colStornoZiele);;
  Clear(colAusgewaehlteBuchungen);;
  Set(varGeklickteBuchungKlein; Blank());;
  Set(varZeigeVerwaltenKlein; false);;
  Set(varAuswahlModusAktiv; false);;
  Reset(tglAuswahlModus);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnStornierenKlein.Text`** (N2)

```
"Stornieren"
```

**`btnVerwalten.OnSelect`** (N3)

```
Set(varSelectedBuchung; ThisItem);;
Set(varVerlTisch; ThisItem.Tisch.Value);;
Set(varVerlEndeAlt; ThisItem.Endzeit);;
Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false)
```

**`btnVerwalten_2.OnSelect`** (N3)

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varVerlTisch; ThisItem.Tisch.Value);;
  Set(varVerlEndeAlt; ThisItem.Endzeit);;
  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
  RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

**`lblStatusHeute.Text`** (N4)

```
If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; "Verfallen"; "Einchecken")
```

**`lblStatusHeute.Color`** (N4)

```
If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; ColorValue("#A6A6A6"); ColorValue("#FFA500"))
```

**`btn5Std.Fill`** (N4)

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`recBuchungDanach1.Visible`** (N4)

```
CountRows(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes))) > 0
```

**`recBuchungDavor1.X`** (N5)

```
With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
  };
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
    recZeitleisteBg.X + Max(0; DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes)) / gesamtFenster * recZeitleisteBg.Width
  )
)
```

**`recBuchungDavor1.Width`** (N5)

```
With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
  };
  With(
    { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart); "Startzeit"; SortOrder.Descending)) };
    (DateDiff(Max(fensterStart; buchung.Startzeit); buchung.Endzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
  )
)
```

**`recBuchungDanach1.X`** (N5)

```
With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
  };
  With(
    { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
      recZeitleisteBg.X + (DateDiff(fensterStart; buchung.Startzeit; TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
    )
  )
)
```

**`recBuchungDanach1.Width`** (N5)

```
With(
  {
    fensterStart: DateAdd(varAusgewählteStartzeit; -90; TimeUnit.Minutes);
    gesamtFenster: 180 + DateDiff(varAusgewählteStartzeit; varAusgewählteEndzeit; TimeUnit.Minutes)
  };
  With(
    { fensterEnde: DateAdd(varAusgewählteEndzeit; 90; TimeUnit.Minutes) };
    With(
      { buchung: First(SortByColumns(Filter(Raumbuchungen; Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde); "Startzeit"; SortOrder.Ascending)) };
      (DateDiff(buchung.Startzeit; Min(buchung.Endzeit; fensterEnde); TimeUnit.Minutes) / gesamtFenster) * recZeitleisteBg.Width
    )
  )
)
```

## Anhang B: Maschinelle Prüfung

```
16 Properties in 5 Schritten, kein neues Steuerelement. Grundlage: Export 08.10. 14:26 (PCAppfertig).
Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, Schreibstellen mit Sperre, Ladezeile mit Stempel, Spaltennamen als Bezeichner.
Storno: Frage-Zweig schreibt und fragt nicht ab, setzt 1-s-Sperre; Bestätigungs-Zweig = Export-Fassung unverändert (nur eingerückt); Frage wird vor dem Schreiben zurückgesetzt.
Öffnen: an btnVerwalten/btnVerwalten_2 nur das Rücksetzen vorangestellt.
Raumcode: danach keine Raum-Abfrage außerhalb von Verhaltensformeln ohne Bedingung.
Prüfung: 0 Fehler
```
