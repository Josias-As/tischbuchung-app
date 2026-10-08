# Handy-Plan: Änderungen Fassung 1 → 2 (08.10.2026)

Nur **H3 `ddTisch.Items`** und **H4 `btnBuchen.OnSelect`** ändern sich (Zeitumstellung, ID aus dem Patch). Alle anderen 15 Properties sind gleich. Der Diff gegen den Export vom 08.10. steht in `UMBAUPLAN_Handy_v2.md`.

## H3 `ddTisch.Items`

Änderung gegenüber Fassung 1:

```diff
@@ -3,3 +3,3 @@
   With(
-    { belegt: Filter(ForAll(Filter(Tischbuchungen; Startzeit < DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes) && Endzeit > DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes)) As X; { TischName: X.Tisch.Value; Aktiv: X.CheckedIn || X.Startzeit > varListeGrenze || IsBlank(X.Erstellt) || X.Erstellt > varListeGrenze }); Aktiv) };
+    { belegt: Filter(ForAll(Filter(Tischbuchungen; Startzeit < DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddEnde.Selected.Min / 60; 0); Mod(ddEnde.Selected.Min; 60); 0) && Endzeit > DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddStart.Selected.Min / 60; 0); Mod(ddStart.Selected.Min; 60); 0)) As X; { TischName: X.Tisch.Value; Aktiv: X.CheckedIn || X.Startzeit > varListeGrenze || IsBlank(X.Erstellt) || X.Erstellt > varListeGrenze }); Aktiv) };
     ForAll(
```

Diff gegen den Export 08.10.:

```diff
@@ -2,8 +2,8 @@
   { neuLaden: varNeuLaden };
   With(
-    { belegt: ForAll(Filter(Tischbuchungen; Startzeit < DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes) && Endzeit > DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes)); Tisch.Value) };
+    { belegt: Filter(ForAll(Filter(Tischbuchungen; Startzeit < DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddEnde.Selected.Min / 60; 0); Mod(ddEnde.Selected.Min; 60); 0) && Endzeit > DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddStart.Selected.Min / 60; 0); Mod(ddStart.Selected.Min; 60); 0)) As X; { TischName: X.Tisch.Value; Aktiv: X.CheckedIn || X.Startzeit > varListeGrenze || IsBlank(X.Erstellt) || X.Erstellt > varListeGrenze }); Aktiv) };
     ForAll(
       Sort(
-        Filter(colTische; !("big table" in Lower(Titel)) && !(Titel in belegt));
+        Filter(colTische; !Gesperrt && !("big table" in Lower(Titel)) && !(Titel in belegt.TischName));
         Geschoss.Value & Left(Titel; Len(Titel) - Len(Last(Split(Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Titel; " ")).Value); 0); "000")
       ) As t;
```

Vollständiger Block (Fassung 2):

```
With(
  { neuLaden: varNeuLaden };
  With(
    { belegt: Filter(ForAll(Filter(Tischbuchungen; Startzeit < DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddEnde.Selected.Min / 60; 0); Mod(ddEnde.Selected.Min; 60); 0) && Endzeit > DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddStart.Selected.Min / 60; 0); Mod(ddStart.Selected.Min; 60); 0)) As X; { TischName: X.Tisch.Value; Aktiv: X.CheckedIn || X.Startzeit > varListeGrenze || IsBlank(X.Erstellt) || X.Erstellt > varListeGrenze }); Aktiv) };
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

## H4 `btnBuchen.OnSelect`

Änderung gegenüber Fassung 1:

```diff
@@ -3,5 +3,5 @@
   Set(varIsLoading; true);;
-  Set(varBuchStart; DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes));;
-  Set(varBuchEnde; DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes));;
-  Set(varTagesEnde; DateAdd(ddDatum.Selected.Tag; 22 * 60; TimeUnit.Minutes));;
+  Set(varBuchStart; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddStart.Selected.Min / 60; 0); Mod(ddStart.Selected.Min; 60); 0));;
+  Set(varBuchEnde; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddEnde.Selected.Min / 60; 0); Mod(ddEnde.Selected.Min; 60); 0));;
+  Set(varTagesEnde; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); 22; 0; 0));;
   Set(varTischName; ddTisch.Selected.Value);;
@@ -18,3 +18,3 @@
     Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
-    varBuchStart < DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes);
+    varBuchStart < DateTime(Year(Now()); Month(Now()); Day(Now()); Hour(Now()); If(Minute(Now()) >= 30; 30; 0); 0);
     Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
@@ -28,20 +28,24 @@
     Notify("Du hast in dieser Zeit schon einen Tisch gebucht."; NotificationType.Warning);
-    IfError(
-      Patch(
-        Tischbuchungen;
-        Defaults(Tischbuchungen);
-        {
-          Tisch: { Id: varTischID; Value: varTischName };
-          Startzeit: varBuchStart;
-          Endzeit: varBuchEnde;
-          Person: {
-            Claims: "i:0#.f|membership|" & Lower(User().Email);
-            Department: "";
-            DisplayName: User().FullName;
-            Email: User().Email;
-            JobTitle: "";
-            Picture: ""
-          }
+    Set(varNeuID; IfError(
+    Patch(
+      Tischbuchungen;
+      Defaults(Tischbuchungen);
+      {
+        Tisch: { Id: varTischID; Value: varTischName };
+        Startzeit: varBuchStart;
+        Endzeit: varBuchEnde;
+        Person: {
+          Claims: "i:0#.f|membership|" & Lower(User().Email);
+          Department: "";
+          DisplayName: User().FullName;
+          Email: User().Email;
+          JobTitle: "";
+          Picture: ""
         }
-      );
+      }
+    ).ID;
+      -1
+    ));;
+    If(
+      varNeuID = -1;
       Notify("Das Buchen ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
@@ -50,13 +54,10 @@
       RemoveIf(colKollision; (!CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze) || Endzeit <= varBuchStart);;
-      Set(varBuchung; LookUp(colKollision; Person.Email = User().Email && Startzeit = varBuchStart && Endzeit = varBuchEnde));;
+      Set(varNeuBuchung; LookUp(colKollision; ID = varNeuID));;
       If(
-        IsBlank(varBuchung.ID);
-        Notify("Die Buchung ist nicht angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
-        Set(varBuchungID; varBuchung.ID);;
-        If(
-          !IsBlank(LookUp(colKollision; ID < varBuchungID).ID);
-          Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
-          Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn einchecken."; NotificationType.Success);;
-          Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
-        )
+        IsBlank(varNeuBuchung.ID) || varNeuBuchung.Startzeit <> varBuchStart || varNeuBuchung.Endzeit <> varBuchEnde || Lower(varNeuBuchung.Person.Email) <> Lower(User().Email);
+        Notify("Die Buchung ist nicht vollständig angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
+        !IsBlank(LookUp(colKollision; ID < varNeuID).ID);
+        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
+        Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn einchecken."; NotificationType.Success);;
+        Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
       )
```

Diff gegen den Export 08.10.:

```diff
@@ -2,9 +2,14 @@
   !varIsLoading && Now() >= varSperreBis;
   Set(varIsLoading; true);;
-  Set(varBuchStart; DateAdd(ddDatum.Selected.Tag; ddStart.Selected.Min; TimeUnit.Minutes));;
-  Set(varBuchEnde; DateAdd(ddDatum.Selected.Tag; ddEnde.Selected.Min; TimeUnit.Minutes));;
-  Set(varTagesEnde; DateAdd(ddDatum.Selected.Tag; 22 * 60; TimeUnit.Minutes));;
+  Set(varBuchStart; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddStart.Selected.Min / 60; 0); Mod(ddStart.Selected.Min; 60); 0));;
+  Set(varBuchEnde; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddEnde.Selected.Min / 60; 0); Mod(ddEnde.Selected.Min; 60); 0));;
+  Set(varTagesEnde; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); 22; 0; 0));;
   Set(varTischName; ddTisch.Selected.Value);;
   Set(varTischID; ddTisch.Selected.ID);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  ClearCollect(colBuchBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
+  RemoveIf(colBuchBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze);;
+  ClearCollect(colBuchIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
+  RemoveIf(colBuchIch; !CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze);;
   If(
     IsBlank(varTischName) || IsBlank(varTischID) || IsBlank(ddStart.Selected.Min) || IsBlank(ddEnde.Selected.Min);
@@ -12,43 +17,48 @@
     varBuchEnde <= varBuchStart;
     Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
-    varBuchStart < DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes);
+    varBuchStart < DateTime(Year(Now()); Month(Now()); Day(Now()); Hour(Now()); If(Minute(Now()) >= 30; 30; 0); 0);
     Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
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
-    IfError(
-      Patch(
-        Tischbuchungen;
-        Defaults(Tischbuchungen);
-        {
-          Tisch: { Id: varTischID; Value: varTischName };
-          Startzeit: varBuchStart;
-          Endzeit: varBuchEnde;
-          Person: {
-            Claims: "i:0#.f|membership|" & Lower(User().Email);
-            Department: "";
-            DisplayName: User().FullName;
-            Email: User().Email;
-            JobTitle: "";
-            Picture: ""
-          }
+    Set(varNeuID; IfError(
+    Patch(
+      Tischbuchungen;
+      Defaults(Tischbuchungen);
+      {
+        Tisch: { Id: varTischID; Value: varTischName };
+        Startzeit: varBuchStart;
+        Endzeit: varBuchEnde;
+        Person: {
+          Claims: "i:0#.f|membership|" & Lower(User().Email);
+          Department: "";
+          DisplayName: User().FullName;
+          Email: User().Email;
+          JobTitle: "";
+          Picture: ""
         }
-      );
+      }
+    ).ID;
+      -1
+    ));;
+    If(
+      varNeuID = -1;
       Notify("Das Buchen ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
-      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
-      Set(varBuchung; LookUp(colKollision; Person.Email = User().Email && Startzeit = varBuchStart && Endzeit = varBuchEnde));;
+      Set(varBuchNachVon; DateAdd(varBuchStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
+      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchNachVon));;
+      RemoveIf(colKollision; (!CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze) || Endzeit <= varBuchStart);;
+      Set(varNeuBuchung; LookUp(colKollision; ID = varNeuID));;
       If(
-        IsBlank(varBuchung.ID);
-        Notify("Die Buchung ist nicht angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
-        Set(varBuchungID; varBuchung.ID);;
-        If(
-          !IsBlank(LookUp(colKollision; ID < varBuchungID).ID);
-          Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
-          Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr"; NotificationType.Success);;
-          Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
-        )
+        IsBlank(varNeuBuchung.ID) || varNeuBuchung.Startzeit <> varBuchStart || varNeuBuchung.Endzeit <> varBuchEnde || Lower(varNeuBuchung.Person.Email) <> Lower(User().Email);
+        Notify("Die Buchung ist nicht vollständig angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
+        !IsBlank(LookUp(colKollision; ID < varNeuID).ID);
+        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
+        Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn einchecken."; NotificationType.Success);;
+        Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
       )
     )
```

Vollständiger Block (Fassung 2):

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varBuchStart; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddStart.Selected.Min / 60; 0); Mod(ddStart.Selected.Min; 60); 0));;
  Set(varBuchEnde; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); RoundDown(ddEnde.Selected.Min / 60; 0); Mod(ddEnde.Selected.Min; 60); 0));;
  Set(varTagesEnde; DateTime(Year(ddDatum.Selected.Tag); Month(ddDatum.Selected.Tag); Day(ddDatum.Selected.Tag); 22; 0; 0));;
  Set(varTischName; ddTisch.Selected.Value);;
  Set(varTischID; ddTisch.Selected.ID);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(colBuchBelegt; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
  RemoveIf(colBuchBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze);;
  ClearCollect(colBuchIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart));;
  RemoveIf(colBuchIch; !CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze);;
  If(
    IsBlank(varTischName) || IsBlank(varTischID) || IsBlank(ddStart.Selected.Min) || IsBlank(ddEnde.Selected.Min);
    Notify("Bitte Datum, Uhrzeit und Tisch auswählen."; NotificationType.Warning);
    varBuchEnde <= varBuchStart;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varBuchStart < DateTime(Year(Now()); Month(Now()); Day(Now()); Hour(Now()); If(Minute(Now()) >= 30; 30; 0); 0);
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    varBuchEnde > varTagesEnde;
    Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    !IsEmpty(colBuchBelegt);
    Notify("Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    !IsEmpty(colBuchIch);
    Notify("Du hast in dieser Zeit schon einen Tisch gebucht."; NotificationType.Warning);
    Set(varNeuID; IfError(
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
    ).ID;
      -1
    ));;
    If(
      varNeuID = -1;
      Notify("Das Buchen ist fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      Set(varBuchNachVon; DateAdd(varBuchStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
      ClearCollect(colKollision; Filter(Tischbuchungen; Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchNachVon));;
      RemoveIf(colKollision; (!CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze) || Endzeit <= varBuchStart);;
      Set(varNeuBuchung; LookUp(colKollision; ID = varNeuID));;
      If(
        IsBlank(varNeuBuchung.ID) || varNeuBuchung.Startzeit <> varBuchStart || varNeuBuchung.Endzeit <> varBuchEnde || Lower(varNeuBuchung.Person.Email) <> Lower(User().Email);
        Notify("Die Buchung ist nicht vollständig angekommen. Bitte unter „Meine“ prüfen."; NotificationType.Warning);
        !IsBlank(LookUp(colKollision; ID < varNeuID).ID);
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch."; NotificationType.Error);
        Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart; "dd.mm.") & ", " & Text(varBuchStart; "hh:mm") & " bis " & Text(varBuchEnde; "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn einchecken."; NotificationType.Success);;
        Set(varTab; If(varBuchStart < DateAdd(Today(); 1; TimeUnit.Days); "heute"; "meine"))
      )
    )
  );;
  Set(varNeuLaden; varNeuLaden + 1);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```
