# BRIEFING: Mehrfachspeichern in der Tischbuchungs-App — Übergabe an einen anderen Claude

Stand: 06.10.2026. Geschrieben von dem Claude, der Josias bisher begleitet hat. Alles hier ist aus dem Projekt "Technoform Share Point" und aus der laufenden Arbeit zusammengetragen. Wo etwas nur geschlussfolgert und nicht gemessen oder in der Doku belegt ist, steht es ausdrücklich dabei (UNSICHER / NICHT GEMESSEN).

---

## 0. Dein Auftrag und die Kurzfassung

**Auftrag:** Entwirf eine Lösung für das "Mehrfachspeichern" in einer Power-Apps-Canvas-App (SharePoint-Listen als Datenquelle). Josias will das ausdrücklich gebaut haben. Ein anderer Claude hat vorgeschlagen, es vor dem Go-Live (14.10.2026) nicht zu bauen. Josias besteht trotzdem darauf. Deine Aufgabe ist also nicht, ihm das auszureden, sondern die beste mögliche, ehrlich bewertete Lösung zu liefern, inklusive der Risiken.

**Kurzfassung der Lage in zehn Sätzen:**

1. "Mehrfachspeichern" meint zwei verschiedene Dinge (siehe Abschnitt 2): (A) die Serienbuchung, die bis zu 14 Einzelbuchungen anlegt, und (B) das Ändern (Verlängern/Verkürzen) mehrerer ausgewählter Buchungen auf einmal. (B) existiert in der App noch gar nicht.
2. (A) ist langsam, vermutlich weil pro Termin ein eigener Schreibaufruf an SharePoint geht. Das ist nicht gemessen.
3. Acht Entwurfsfamilien wurden von Claude Code entworfen und von unabhängigen Prüf-Agenten angegriffen. Keine hat überlebt. Die Gründe stehen in Abschnitt 8.
4. Der Hauptfehler aller acht: Der Dialog arbeitet auf einer unsichtbaren Menge und meldet am Ende nur eine Zahl ("N Buchungen geändert"), die aus einer lokalen Collection kommt statt aus dem, was SharePoint tatsächlich angenommen hat.
5. Die zweite Erkenntnis, die als wichtigste galt, war: Sammelaufrufe (`Collect/Patch/Remove` mit Tabelle) sparen gegen SharePoint keine Netzwerkaufrufe, weil der Konnektor pro Zeile einen Aufruf macht. Das haben drei Prüfer geschlussfolgert, nicht gemessen.
6. Neu aus einer Recherche vom 05.10.: Ein Blog (Matthew Devaney) behauptet, `Patch(Quelle; Collection)` sei bei SharePoint deutlich schneller als `ForAll(...; Patch(...))`, weil die Aufrufe gleichzeitig statt nacheinander laufen. Das ist nur ein Einzelbeleg und nicht an dieser App gemessen. "Weniger Aufrufe" und "schneller" sind zwei verschiedene Fragen.
7. Josias hat deshalb die Serienbuchung (`btnSpeichern.OnSelect`) bereits auf `Patch(Tischbuchungen; ForAll(neueDatensaetze; Defaults(Tischbuchungen)); neueDatensaetze)` umgebaut. Die App-Prüfung zeigt dabei keinen Fehler. **Zur Laufzeit ist es NICHT getestet.**
8. Offene Hauptunsicherheit: Ob das Personenfeld (`Person`) und das Nachschlagefeld (`Tisch`) bei diesem Schreibweg korrekt gespeichert werden (Typinformation, `'@odata.type'`).
9. Es wurde nie im Power-Apps-Monitor gemessen. Das ist die einzige Messung, die die Streitfrage "ein Aufruf oder N Aufrufe, sequenziell oder parallel" entscheiden würde.
10. Rahmen: Go-Live am 14.10.2026, 240 Einträge in der Liste, Josias ist der einzige Entwickler, Claude Code kann die App nicht bearbeiten, Josias fügt jede Formel selbst in Power Apps Studio ein.

---

## 1. Rahmen und Person

- **Person:** Josias, Werkstudent im Bereich Digitalisierung bei Technoform (Technoform Caprano + Brunnhofer GmbH / Kunststoffprofile), studiert Wirtschaftsinformatik, einziger Entwickler dieser App.
- **App:** Power-Apps-Canvas-App "Tischbuchung" (Desk Booking, ersetzt das zugekaufte GoBright). Umgebung "Personal Productivity" (die Standardumgebung des Tenants). App-ID `d247d18b-d36f-4a44-975a-7839695b2f12` ist die RICHTIGE. Es gibt zwei fast identische Klone ("App" `fc32c6b0-5e8a-4650-a377-8d6e0e02d1b7` und "App – Kopie"). Die waren schon einmal Verwechslungsursache.
- **Datenquelle:** SharePoint-Listen `Tischbuchungen` und `Tische`. Aktuell **240 Einträge** in `Tischbuchungen` (echte Liste, Stand 06.10.). Ein Aufräum-Flow (Power Automate) existiert bereits und löscht alte Buchungen. Datenzeilenlimit der App steht auf 2000.
- **Go-Live:** ca. 14.10.2026. Erwartete Last: 200–400 Einträge, Spitzen 600–800 durch Serienbuchungen. Eine Serie erzeugt bis zu 14 Einträge. Montagmorgen ca. 8 Uhr buchen viele gleichzeitig.
- **Prioritäten (Josias, in dieser Reihenfolge):** (1) funktionale Korrektheit: keine Doppelbuchungen, keine Lags, keine rohen Connector-Fehler; (2) Ladezeit beim App-Start; (3) Speicher- und Stornierzeit bei Mehrfachauswahl.
- **Wichtigster Satz von Josias zum Thema:** Speichern und Stornieren bei Mehrfachauswahl seien "sehr sehr wichtig". Der Ansatz "komplett neu bauen und das Problem umgehen" war in diesem Projekt bisher immer erfolgreicher als "den Fehler suchen".
- **Arbeitsweise:** Josias will ehrliche, kritische Rückmeldung ohne Beschönigung, kleine Schritte, vollständigen einfügefertigen Code, kurze Antworten. Er liest lange Dokumente nicht gern. Er macht vor jeder Änderung einen `.msapp`-Export als Backup.
- **Arbeitsteilung:** Claude Code kann Power Apps Studio nicht bedienen. Es kann ein exportiertes `.msapp` mit `pac canvas unpack` lesen (nur lesen, Zurückpacken ist riskant/deprecated). Josias fügt jede Formel selbst im Studio ein und testet. Du lieferst Formeln und Begründungen.

---

## 2. Was "Mehrfachspeichern" bedeutet — zwei Dinge, bitte getrennt behandeln

### (A) Serienbuchung ("wiederholte Buchung") — existiert, ist das akute Performanceproblem

Im Buchungsdialog kann der Nutzer "Wiederholen" anhaken, Modus "Täglich" oder "Wochentage" (Mo–So), ein Enddatum wählen (maximal 14 Tage ab Startdatum, sonst Kappung auf 2 Wochen). Beim Speichern entstehen bis zu 14 Einträge in `Tischbuchungen`.

Gemeldetes Verhalten (30.09.): Einzelbuchung schnell, Serienbuchung "extrem extrem lange". Unregelmäßig: Bei 8 Wiederholungen lief alles zügig, bei 10 waren die ersten 5 schnell, Nr. 6 und 7 spürbar langsamer, danach wieder schnell. Der Spinner dreht dabei teils weiter, obwohl der Eintrag längst da ist. Einchecken (einzelner Statusupdate) dauert manchmal ebenfalls sehr lange.

Zwei Speichern-Knöpfe, **nicht wortgleich**:
- `btnSpeichern` in `conBuchungDialog` (Grundriss-Dialog), laut Claude Code Zeile ca. 2716/2727
- `btnSpeichernTischePanel` in `conTischBuchungenPanel`, Zeile ca. 948

Rechenteil identisch, aber die Aufräumblöcke am Ende unterscheiden sich (12 gegen 23 Anweisungen) und die Steuerelementnamen sind andere (Mapping: `dpDatum`→`dpDatumTischePanel`, `ddStart`→`ddStartTischePanel`, `ddEnde`→`ddEndeTischePanel`, `dpWiederholenBis`→`dpWiederholenBis_1`, `varSelectedTisch.ID/Titel`→`ddTischePanel.Selected.ID/Titel`). Jede Änderung muss in beiden Knöpfen separat gemacht werden, nie die Formel komplett kopieren.

### (B) Mehrfachauswahl-Speichern ("Mehrfach-Verlängern/Verkürzen") — existiert NICHT

Im Buchungen-Tab gibt es einen Auswahlmodus (`tglAuswahlModus`, Checkboxen `chkAuswahl`, `chkAlleAuswählen`, Collection `colAusgewaehlteBuchungen`). Im Auswahlmodus öffnet der Stift-Knopf den Dialog `conVerwaltenKlein` mit nur **"Stornieren"** und **"Schließen"**. Das Stornieren mehrerer Buchungen funktioniert (und wurde bereits neu gebaut, siehe Abschnitt 5). **Ein Mehrfach-Verlängern/Verkürzen gibt es nicht.** Der Knopf mit dem Namen "Speichern" im Verwalten-Dialog ändert immer nur EINE Buchung.

Josias' Wunsch: Mehrere Buchungen auswählen und ihre Dauer gemeinsam ändern können (z. B. alle ausgewählten um eine Stunde verlängern), schnell und ohne dass eine Fehlmeldung lügt. Diese Funktion wurde in den acht Entwürfen (Familien 1A–1D) durchgespielt und verworfen. Claude Code empfahl, sie vor dem Go-Live nicht zu bauen.

**Frage an dich:** Welche der beiden Funktionen soll die Lösung abdecken, oder beide? Josias hat beide Wörter als "Mehrfachspeichern" benutzt. Liefere bitte für (A) eine konkrete, einfügefertige Lösung und für (B) einen ehrlich bewerteten Entwurf.

---

## 3. Verifizierte Fakten aus dem Quellcode (INVENTAR.md von Claude Code, aus dem echten `.msapp`)

- Genau ein Screen: `Screen1`. Kein `Screen2`.
- **Spaltenname `Titel`** (79 Vorkommen im Quellcode, 0× `Title`). Eine ältere Regel "immer `Title`" war für diese App FALSCH.
- Liste `Tische` hat `Geschoss` (nicht `Standort`) und KEIN `Aktiv`.
- Check-in-Spalte: interner Name `Checkedin`, Anzeigename `CheckedIn`. Die App ist korrekt; nur Flows müssen `Checkedin` verwenden.
- `Tischbuchungen.SerienID` existiert, ist lesbar/schreibbar/filterbar und wird **nirgends** in der App benutzt. Das ist eine ungenutzte Zutat für Serien (eine Serie über eine Kennung zusammenhalten, finden, stornieren).
- Neun `Refresh`-Aufrufe, **keiner in einer `ForAll`-Schleife**. Alle stehen am Ende ihres Vorgangs. (Eine frühere Hauptvermutung "Refresh in der Schleife" war falsch.)
- Drei Warnungen `app-ForAllWithMutation` von der App-Prüfung (Schleifen mit Schreiboperationen).
- 56 Delegationswarnungen, alle auf `CountRows(Filter(...))` in den Verlängern-/Dauer-Knöpfen (10 davon auf totem Raumcode). Die Master-Bedingung der Grundriss-Kacheln wird NICHT beanstandet. Die Galerie-Vorlage kostet 96–108 `LookUp` pro Grundriss-Render.
- `galAlleTischbuchungen.Items` hat ein gelbes Delegationsdreieck (von Josias bestätigt). Ursache nicht abschließend geklärt (`Person.Email`? `Now()`?).
- App läuft mit `powerfxv1 = False`. Es gibt in der ganzen App kein `IfError` (vor den jüngsten Änderungen) und keine mehrarmige `If(bed1; erg1; bed2; erg2; ...)`-Form.
- `Screen1.LoadingSpinner = LoadingSpinner.Data` (Zeile 13) verursacht den doppelten Spinner neben `conLadeOverlay`. `varSpinnerWinkel` hat keinen Timer (tot).
- Variablen: `varIsLoading` (Overlay `conLadeOverlay`, bildschirmfüllend, `Visible: =varIsLoading`), `varSelectedBuchung` (Grundriss-Dialog), `varSelectedBuchungTab` (Buchungen-Tab-Dialog), `varZeigeVerwalten`, `varZeigeVerwaltenTab`, `varAusgewaehltePlusDauer`, `varAuswahlModusAktiv`, `varMehrfachAuswahlModus` (möglicherweise tot, nicht geprüft), `colAusgewaehlteBuchungen`, `varWiederholen`, `varWiederholenModus`, `varTagMo…varTagSo`.
- Wichtig für Schreibwege: Eine **Person**-Spalte wird bei `Patch(Tischbuchungen; Defaults(Tischbuchungen); {...})` mit diesem Schema geschrieben: `{Claims: "i:0#.f|membership|" & Lower(User().Email); Department: ""; DisplayName: User().FullName; Email: User().Email; JobTitle: ""; Picture: ""}`. Eine **Lookup**-Spalte immer als `{Id: ...; Value: ...}`. Die alte Raumbuchung (toter Code, Zeile ca. 2306) schreibt zusätzlich `'@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser"` mit — dort war es offenbar nötig.

---

## 4. Der Original-Code der Serienbuchung (`btnSpeichern.OnSelect`, Zustand VOR Josias' Umbau)

```powerfx
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel)
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatum.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatum.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatum.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatum.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                ergebnisse:
                  ForAll(
                    datumsListe As Eintrag;
                    If(
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0;
                      With(
                        {
                          neuerEintrag: Patch(Tischbuchungen; Defaults(Tischbuchungen); {
                            Tisch: {Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel};
                            Startzeit: Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                            Endzeit: Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                            Person: {
                              Claims: "i:0#.f|membership|" & Lower(User().Email);
                              Department: "";
                              DisplayName: User().FullName;
                              Email: User().Email;
                              JobTitle: "";
                              Picture: ""
                            }
                          })
                        };
                        "gespeichert"
                      );
                      "übersprungen"
                    )
                  )
              };
              With(
                { anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen")) };
                If(
                  effektivesBisRoh > effektivesBis;
                  Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
                  If(
                    anzahlUebersprungen > 0;
                    Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
                    Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
Set(varZeigeDialog; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varIsLoading; false)
```

Bekannte Schwächen dieses Originals (aus der Prüfung): (1) Kollisionsabfrage `Filter(Tischbuchungen; Tisch.Value = ...)` ohne Zeitgrenze, nicht delegierbar, bei vielen Zeilen schneidet Power Apps nach dem Datenzeilenlimit ab; (2) `dpWiederholenBis` hat kein `DefaultDate` und steht auf heute: Wählt der Nutzer ein künftiges Startdatum und hakt "Wiederholen" an, ohne den Bis-Picker anzufassen, ist `effektivesBisRoh` vor dem Startdatum, `Sequence` bekommt eine negative Zahl und die Meldung "Bitte mindestens einen Wochentag auswählen" erscheint irreführend; (3) Der Hinweis "Wiederholung wurde auf 2 Wochen begrenzt" verdrängt per `If` alle anderen Meldungen (Kollisionsmeldung/Erfolg); (4) kein `IfError` um `Patch`: bricht ein Aufruf ab, meldet die App trotzdem "gespeichert" oder rohe Fehler; (5) Der Dialog schließt unbedingt, auch bei Fehlern.

---

## 5. Aktueller Stand in der App (06.10.2026)

### 5.1 Serienbuchung: von Josias bereits umgebaut auf Sammel-`Patch`, ungetestet

Josias hat in `btnSpeichern.OnSelect` den Block `With({ergebnisse: ForAll(...Patch...)} ...)` ersetzt durch (alles andere in der Formel blieb gleich):

```powerfx
With(
  {
    neueDatensaetze:
      ForAll(
        Filter(
          datumsListe As Eintrag;
          CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0
        ) As Frei;
        {
          Tisch: {Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel};
          Startzeit: Frei.Value + Time(Hour(neuStart); Minute(neuStart); 0);
          Endzeit: Frei.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
          Person: {
            Claims: "i:0#.f|membership|" & Lower(User().Email);
            Department: "";
            DisplayName: User().FullName;
            Email: User().Email;
            JobTitle: "";
            Picture: ""
          }
        }
      )
  };
  With(
    {
      speicherStatus:
        If(
          CountRows(neueDatensaetze) = 0;
          "keine";
          IfError(
            Patch(Tischbuchungen; ForAll(neueDatensaetze; Defaults(Tischbuchungen)); neueDatensaetze);
            "fehler";
            "ok"
          )
        )
    };
    With(
      { anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze) };
      If(
        speicherStatus = "fehler";
        Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen."; NotificationType.Error);
        If(
          effektivesBisRoh > effektivesBis;
          Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
          If(
            anzahlUebersprungen > 0;
            Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
            Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
          )
        )
      )
    )
  )
)
```

Status: Die App-Prüfung in Power Apps Studio zeigte danach 56 Formelwarnungen (wie vorher) und KEINE Fehler. Unter "Leistung" sank die Zahl von 15 auf 14 (die ForAll-mit-Patch-Warnung dieses Knopfs verschwand). **Nicht getestet:** ob die Datensätze zur Laufzeit korrekt angelegt werden (Spalten `Person` und `Tisch` gefüllt?), ob das schneller ist, wie viele Netzwerkaufrufe im Monitor entstehen, was bei Teilausfall passiert. Ob Josias die Änderung gespeichert hat, ist nicht bestätigt. `btnSpeichernTischePanel` ist noch auf dem alten Stand.

### 5.2 Stornieren mit Mehrfachauswahl: neu gebaut (Entwurf A), von Josias eingefügt

`btnStornierenKlein.OnSelect` (Zwei-Tab-Test und Monitor-Messung stehen noch aus):

```powerfx
Set(varIsLoading; true);;
ClearCollect(colStornoFrisch; Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now()));;
ClearCollect(colStornoZiele; Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID))));;
If(CountRows(colAusgewaehlteBuchungen) = 0; Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
   If(CountRows(colStornoZiele) = 0; Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
      IfError(Remove(Tischbuchungen; colStornoZiele); Notify("Stornieren fehlgeschlagen. …"; NotificationType.Error);
         If(CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen); Notify(… " von " … " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning); Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)))));;
Refresh(Tischbuchungen);; Clear(colStornoFrisch);; Clear(colStornoZiele);; Clear(colAusgewaehlteBuchungen);;
Set(varGeklickteBuchungKlein; Blank());; Set(varZeigeVerwaltenKlein; false);; Set(varAuswahlModusAktiv; false);; Reset(tglAuswahlModus);; Set(varIsLoading; false)
```

(Die Meldungstexte mit "…" sind hier gekürzt; Struktur ist wortgetreu.) Die Idee: frisch lesen, Schnittmenge mit der Auswahl bilden, ein `Remove` mit Tabelle in `IfError`, Meldung nach dem Ergebnis, Aufräumen, Overlay aus.

### 5.3 Verlängern/Verkürzen (EINZELNE Buchung) — der heutige Code, an dem (B) aufbauen müsste

`conVerwaltenDialog.btnVerlängern.OnSelect` (Grundriss, Variable `varSelectedBuchung`):

```powerfx
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
    }));;
    Set(varZeigeVerwalten; false);;
    Set(varAusgewaehltePlusDauer; Blank())
  )
)
```

`btnVerlängern_1.OnSelect` (Buchungen-Tab, Variable `varSelectedBuchungTab`) ist analog, endet aber mit `Refresh(Tischbuchungen);; Set(varZeigeVerwaltenTab; false);; Set(varAusgewaehltePlusDauer; Blank());; Clear(colAusgewaehlteBuchungen);; Set(varMehrfachAuswahlModus; false)`.

Ein Plus-Knopf (OnSelect): `Set(varAusgewaehltePlusDauer; If(varAusgewaehltePlusDauer = 60; Blank(); 60))`. Ein Minus-Knopf analog mit -120.

Plus-Knopf `DisplayMode` (Kollisionsprüfung nur gegen das NEUE Stück, kein `ID <>` nötig):

```powerfx
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

Minus-Knopf `DisplayMode`: `If(neueEndzeit <= aktuelleBuchung.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)` mit `neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes)`.

Bekannte Lücken: Beim Speichern selbst wird nicht auf Kollision geprüft, nur beim Färben/Sperren der Knöpfe mit dem Stand vom Öffnen des Dialogs; kein `IfError`; keine 22:00-Kappung; keine Prüfung "Buchung wurde inzwischen gelöscht". **B0 (aktiv, still):** Im Buchungen-Tab speichert der Dialog `varSelectedBuchungTab`, aber 12 Plus-/Minus-Properties (Zeilen ca. 3741–3984) lesen `varSelectedBuchung`, also die zuletzt im Grundriss angeklickte Buchung. Ein Knopf kann deshalb grün sein, obwohl die Verlängerung kollidiert: stille Doppelbuchung.

---

## 6. Die fünf Korrekturen K1–K5 (Claude Code, ENTWURF_SPEICHERN.md) und meine Prüfung

Claude Code empfahl: Mehrfach-Speichern vorerst nicht bauen, K1–K5 einbauen (ca. 1 Stunde). Der vollständige Wortlaut der Formeln liegt in `ENTWURF_SPEICHERN.md` auf Josias' Rechner (bitte von ihm als Anhang anfordern). Inhalt in Kurzform:

- **K1:** `btnVerwalten_2.OnSelect` (Galerie `galAlleTischbuchungen`): im Nicht-Auswahlmodus-Zweig zusätzlich `Set(varSelectedBuchung; ThisItem);;` neben dem vorhandenen `Set(varSelectedBuchungTab; ThisItem)`. Behebt B0 mit einer Zeile statt 12 Properties. Risiko: Eine Variable bedient danach zwei Dialoge (dieses Muster hat am 15.09. schon einen Debugging-Tag gekostet). Test in beide Richtungen nötig.
- **K2:** neues `btnVerlängern_1.OnSelect`: Prüfreihenfolge (keine Dauer gewählt; Buchung existiert nicht mehr; neue Endzeit <= Startzeit; über 22:00 per `tagesEnde`; Kollisionsprüfung `CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && ID <> aktuelleBuchung.ID && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Startzeit)) > 0`), dann `IfError(Patch(...))` mit deutschen Meldungen, danach `Refresh(Tischbuchungen);; Set(varAusgewaehltePlusDauer; Blank())`. Die beiden Zeilen `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus; false)` wurden bewusst entfernt. Risiko: mehrarmiges `If(bed1; erg1; bed2; erg2; ...)`, im Quellcode bisher nirgends benutzt, in `powerfxv1 = False` vielleicht nicht akzeptiert (Fallback: verschachtelte zweiarmige `If`).
- **K3:** dasselbe für `conVerwaltenDialog.btnVerlängern` (Variablen `varSelectedBuchung`, `varZeigeVerwalten`).
- **K4:** in beiden Speichern-Knöpfen: K4.1 Zeitgrenze der Kollisionsabfrage `Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel && Endzeit > dpDatum.SelectedDate && Startzeit < DateAdd(dpDatum.SelectedDate; 16; TimeUnit.Days))`; K4.2 `effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate > dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate)` (statt `<>`); K4.3 `IfError` um den Patch je Termin ("gespeichert"/"übersprungen"/"fehler"); K4.4 eine kombinierte Meldung mit Zählern, Schwere nach schlimmstem Fall, Kappungshinweis nicht mehr verdrängend.
- **K5:** `DisplayMode: If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)` bei `btnSpeichern`, `btnSpeichernTischePanel`, `btnVerlängern_1`, `btnVerlängern`; bei den zwei Verlängern-Knöpfen muss zusätzlich `Set(varIsLoading; true);;` an den Anfang und `Set(varIsLoading; false)` ans Ende. Sonst wirkungslos.

**Meine Prüfung (Korrekturen/Ergänzungen, noch nicht von Claude Code bestätigt):**
- Die Kollisionsbedingung in K2/K3 sollte NICHT `ID <>` enthalten. Laut Microsoft ist bei SharePoint auf dem ID-Feld nur `=` delegierbar, `<>` nicht. Besser (und wie die vorhandenen Plus-Knöpfe es schon machen): nur das NEUE Stück prüfen, `Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`. Das schließt die eigene Buchung automatisch aus.
- Beim Verkürzen nicht auf Kollision prüfen (Bedingung mit `varAusgewaehltePlusDauer > 0` voran), sonst blockiert eine bereits bestehende Überlappung das Verkürzen.
- Eine `Now()`-Sperre beim Minus-Knopf (Endzeit nicht in der Vergangenheit) ist eine fachliche Entscheidung und kein Fehler: Wer früher geht und verkürzt, gibt den Tisch frei. `Now()` in einer `DisplayMode`-Eigenschaft ist außerdem nicht laufend aktuell.
- Das Beispiel in K4 ("3 von 3 Terminen gespeichert. 1 waren bereits belegt.") ist in sich falsch, es müsste "3 von 4" heißen; die Formel rechnet richtig.
- K3 nennt "drei Ersetzungen", aufgezählt sind zwei.

---

## 7. Performance: Beobachtungen und Hypothesen (alles NICHT GEMESSEN)

- Hypothese 1: Pro Termin ein eigener sequenzieller `Patch` an SharePoint, also N Roundtrips.
- Hypothese 2: SharePoint-Drosselung (HTTP 429, stiller Retry in Power Apps) erklärt das Muster "Nr. 6/7 langsam". Die Grenze des SharePoint-Konnektors liegt laut Microsoft bei **600 API-Aufrufen pro Verbindung in 60 Sekunden**. 14 Schreibaufrufe liegen weit darunter; Drosselung wäre nur plausibel, wenn nebenbei viel anderes läuft (Galerien, Refresh, mehrere Nutzer, Flows). Nicht belegt.
- Hypothese 3 (verworfen durch Inventar): `Refresh` in der Schleife. Gibt es nicht.
- Weitere Zeitverbraucher bei der Serienbuchung neben dem Schreiben: die Kollisionsabfrage über `Filter(Tischbuchungen; Tisch.Value = ...)` (nicht delegierbar), `Refresh(Tischbuchungen)` am Ende, danach das Neuaufbauen der Galerien.
- Josias hat nie im Power-Apps-Monitor gemessen. Empfohlene Messung: Serie mit 1, 5 und 14 Tagen speichern; im Monitor die `createRow`/`patchRow`-Einträge zählen, Dauer pro Eintrag, Status (429?), starten sie nacheinander oder gleichzeitig? Danach dasselbe mit dem neuen Sammel-`Patch`.

---

## 8. Alles, was bereits verworfen wurde (Verwurfsprotokoll von Claude Code, 03.10.2026)

Methode: Claude Code entwarf vier grundverschiedene Familien je Baustelle, ließ jeden Entwurf von einem unabhängigen Prüf-Agenten in frischem Kontext angreifen und verwarf, was an Korrektheitskriterien scheiterte. Kriterien: 1 Doppelbuchung, 2 Ehrlichkeit (Meldung stimmt mit dem Datenbestand überein), 3 Zugriffe, 4 Delegation/Gleichzeitigkeit, 5 Wartungsfläche, 6 Einfügeaufwand. Baustelle 1 = Mehrfachauswahl Verlängern/Verkürzen (B), Baustelle 2 = Serienbuchung (A).

**Vorab ausgeschlossen:** Power-Automate-Flow als Schreibweg (SharePoint-`$batch` über einen Flow). Begründung: Bricht die Verbindung nach dem Absenden ab, bekommt die App einen Fehler, während der Flow weiterarbeitet; die App kann danach nicht feststellen, was tatsächlich geschrieben wurde. Beim Schreiben wiegt das schwerer als beim Löschen. Dazu: nicht als einfügefertige Formel lieferbar, verteilt die Fehlersuche auf zwei Werkzeuge. (Hinweis von mir: Diese Familie wurde nicht im Detail angegriffen, sondern aus dem Stornieren-Lauf übernommen. Ob man das Abbruchrisiko mit einer SerienID und einer Nachlese in der App beherrschbar machen kann, wurde nicht untersucht.)

**Runde 1 (strukturell ausgeschieden, vor dem Angriff):**
- **1D "Ersetzen statt ändern"** (Remove + Collect mit neuen Zeiten): Zwischen Remove und Collect ist der Tisch nachweislich frei, bei Verbindungsabbruch ist die Buchung weg; CheckedIn geht verloren; die ID ändert sich ("Item Not Found" für alle Variablen, die auf die alte ID zeigen); SerienID/Titel müssen von Hand mitkopiert werden. Lehre: In einem System ohne Transaktionen ist Zerlegen in Löschen+Neuanlegen immer ein Rückschritt. Nur `Patch` auf bestehende Datensätze kommt in Frage.
- **2D "Die Serie als ein Datensatz"** (eine Zeile mit Wiederholungsregel, beim Lesen aufgefächert): Mindestens 24 Abfragen lesen `Tischbuchungen` als flache Liste von Einzelterminen; jede müsste auffächern; eine Wiederholungsregel lässt sich nicht serverseitig filtern, also nicht delegierbar; Einzel-Storno/-Verlängern/-Check-in pro Termin nicht mehr abbildbar. Lehre: Die Zeile bleibt die Einheit; die Serie wird über eine Kennung (SerienID) zusammengehalten, nicht über eine Regel.

**Runde 2 (Angriff, alle gefallen):**
- **1C "Absolute Zielzeit statt Delta"** (Dropdown "neues Ende: 15:00/16:00…"): speichert nie (der geerbte Wächter `If(IsBlank(varDauerKlein)…)` bleibt unerreichbar, weil die Setzer-Knöpfe gestrichen wurden); eine Zielzeit in der Vergangenheit löscht die Buchung faktisch (fällt aus `Endzeit >= Now()`); eine absolute Zielzeit passt nicht zu Buchungen über mehrere Tage (Dialog zeigt nur ein Datum); Verlängern und Verkürzen werden ununterscheidbar; eingecheckte Buchungen werden ungewarnt gekürzt; die versprochene Wiederholbarkeit liefert er nicht (zweiter Durchlauf schreibt erneut und meldet "5 geändert" für unveränderte Buchungen). Lehre: Ein Delta respektiert die Unterschiede zwischen ausgewählten Datensätzen, ein Zielwert plättet sie. Wiederholbarkeit muss über Sperre gegen den zweiten Klick kommen.
- **1A "Sammel-Patch, Teilerfolg erlaubt"**: Meldung lügt in beide Richtungen (grün trotz geschriebener Doppelbuchung bei abgeschnittenem Bestand; anderes Ergebnis als im Dialog zugesagt, weil der Dialog eingefrorene Zeiten zeigt; nennt Buchungen, die gar nicht angefasst wurden); Kollisionsprüfung weist zu viel ab (A 08–09, B 09–10, beide angehakt, +1 Std: B wird abgelehnt, weil die Vorschau A mit hypothetischem Ende 10:00 führt, obwohl A abgelehnt wurde; Auswertung einstufig, nicht bis zum Fixpunkt); die drei `ClearCollect` ohne `IfError`; die Zugriffszahl "4 konstant" ist falsch.
- **1B "Sammel-Patch, alles oder nichts"**: Blocker: das abschließende `Set(varIsLoading; false)` landet im Erfolgszweig und ist in vier von fünf Pfaden unerreichbar, `conLadeOverlay` bleibt bildschirmfüllend, die App ist bis zum Neustart gesperrt; die Alles-oder-nichts-Schranke prüft am falschen Zähler (Zähler und Nenner schrumpfen gemeinsam, "0 Buchungen geändert" in Grün); die Verweigerungsmeldung nennt keine Buchung und der Nutzer kann die fremde kollidierende Buchung nicht einsehen (beide Galerien filtern auf `Person.Email = User().Email`); die Fehlermeldung behauptet eine Aktualisierung, die nicht stattfand.
- **2A "Sammel-Collect, Teilerfolg wie heute"**: nach einem Teilausfall (z. B. 6 von 14 geschrieben, Meldung "fehlgeschlagen") findet der Neuversuch die eigenen sechs Zeilen und schreibt sie dem Nutzer als fremde Kollision an; die neue Zeitgrenze `Startzeit >= dpDatum.SelectedDate` übersieht Buchungen, die am Vortag beginnen und hineinreichen (erreichbar, weil die Verlängern-Knöpfe nicht bei 22:00 kappen); die Zweiwochenkappung verschwindet in zwei von drei Ausgängen; `Set(varSerienID; "")` in `OnStart` und `Set(varSerienID; GUID())` im Knopf: Typkonflikt (richtig: `Text(GUID())`); die zwei Speichern-Knöpfe sind nicht wortgleich (12 gegen 23 Aufräum-Anweisungen). Nicht beanstandet: Datumsliste, Syntax, As-Aliasse, Zeitzonenverhalten über die Zeitumstellung.
- **2B "SerienID, Nachprüfung und Rücknahme"** (nach dem Schreiben nachlesen, bei Überschneidung "niedrigste ID gewinnt", eigene Datensätze zurücknehmen): Der Nachprüfblock liegt im `DefaultResult` von `IfError` und wird selbst nicht überwacht (bricht das Nachlesen ab, steht "14 von 14 gespeichert" für einen nie erfolgten Abgleich); bei 429 läuft die Nachprüfung gar nicht (Fallback-Zweig); oberhalb des Datenzeilenlimits fällt sie deterministisch aus, weil die neuen Zeilen die höchsten IDs haben und zuerst herausfallen; "niedrigste ID gewinnt" kann gültige Buchungen löschen (A bucht frei, C verlängert danach eine ältere Buchung mit niedriger ID in A's Fenster, A's Buchung wird gelöscht); Typkonflikt `GUID()`; überlappende Serien verschränken IDs, eine zerrissene Serie ist schlechter als eine abgelehnte. Lehre: Ein stilles Sicherheitsnetz ist schlechter als keines, weil es eine Erfolgsmeldung rechtfertigt, die sonst niemand gegeben hätte.
- **2C "Alles oder nichts"** (kollidiert ein Termin, wird nichts gespeichert): Meldung nennt keinen einzigen Tag und der Nutzer kann es nicht nachsehen; keine Umgehung (kein Einzeltag ausnehmbar); abgebrochener Schreibvorgang wird zur Dauersperre (die eigenen Zeilen blockieren den Neuversuch); wörtliche Umsetzung friert die App ein (gleicher `varIsLoading`-Fehler wie 1B); der Name verspricht Atomizität, die der Schreibvorgang gar nicht hat.

**Übergreifende Befunde (Ü1–Ü8), die jeder neue Entwurf beachten muss:**
- **Ü1** Ein Teilerfolg wird als Totalausfall gemeldet: neun von vierzehn Zeilen geschrieben, dann Abbruch, `IfError` meldet "fehlgeschlagen"; die Zahl tatsächlich geschriebener Zeilen wird nie ermittelt.
- **Ü2** Der Aufräumblock läuft unbedingt, auch im Fehlerfall (Auswahl weg, Dialog zu). Nur im Erfolgszweig aufräumen, aber `varIsLoading` auf JEDEM Pfad zurücksetzen.
- **Ü3** Ein serverseitig gelöschter Datensatz bekommt eine falsche Begründung ("belegt oder zu kurz" statt "existiert nicht mehr").
- **Ü4** Doppelklick erzeugt zwei widersprüchliche Meldungen; eine `DisplayMode`-Sperre gehört an den Knopf.
- **Ü5** Der Sammelaufruf spart gegen SharePoint keine Aufrufe (nach Aussage von drei Prüfern; NICHT GEMESSEN; siehe Abschnitt 9). Gerechnete Zugriffe: Serienbuchung 1/5/14 Tage nach Zählweise Nullpunkt 3/7/16; Entwurf 1A/1B "tatsächlich" 4/8/17/53 bei 1/5/14/50 ausgewählten Buchungen. Ein Bündel gleichzeitiger Schreibanforderungen ist außerdem für 429 anfälliger als nacheinander abgesetzte.
- **Ü6** `Collect` aus Satzliteralen verliert die Spaltentypen, die `Defaults()` mitbringt. `Tisch` wäre nur ein Satz aus Zahl und Text, `Person` nur ein Satz aus Claims und Namen. Jeder Collect-Entwurf braucht `'@odata.type'` für Person (`…SPListExpandedUser`) und für Tisch (`…SPListExpandedReference`). Folge sonst: "14 von 14 gespeichert" über Buchungen, die der Nutzer nirgends wiederfindet (die Ansichten filtern auf `Person.Email = User().Email`).
- **Ü7** Zustand aus `With()`-Locals in globale Variablen/Collections zu verlagern macht die Knöpfe mehrfachaufruf-unsicher (zweiter Lauf überschreibt `varSerienID`/`colNeueBuchungen`, während der erste noch schreibt).
- **Ü8** `btnSpeichern` und `btnSpeichernTischePanel` sind im Rechenteil wortgleich, im Aufräumteil nicht (12 gegen 23). Jede Ersetzungstabelle, die nur Steuerelementnamen auflistet, ist unvollständig (nötig wären 16 Zeilen gewesen).

**Das Fazit von Claude Code:** Nicht die Zählung verbessern, sondern sie abschaffen. Die betroffene Menge **zeigen statt zählen**, und das Ergebnis **pro Zeile aus dem tatsächlichen Schreibergebnis feststellen**. Das ist keine Formelfrage mehr, sondern eine Vorschau-Galerie mit Zeilenstatus (Ergebnis-Collection pro Buchung, im Dialog sichtbar). Aufwand laut Claude Code: ein halber Tag; laut mir: ein bis zwei Stunden, wenn die Prüflogik aus K2 wiederverwendet wird (Schätzung, nicht belegt).

**Mein eigener, bisher nicht angegriffener Gegenentwurf für (B) ("Zeile für Zeile, jede Zeile einzeln gemeldet"):**
1. Dialog listet die ausgewählten Buchungen mit aktueller und neuer Zeit.
2. "Speichern" arbeitet die Liste zeilenweise ab: pro Zeile frisch lesen, Kollision prüfen (nur das neue Stück), 22:00-Grenze, `IfError(Patch(...))`.
3. Das Ergebnis jeder Zeile (✓/✗ mit Grund) kommt in eine Collection und wird angezeigt. Keine gezählte Gesamtmeldung.
4. Der Dialog bleibt bei Fehlern offen; nur die fehlgeschlagenen Buchungen bleiben ausgewählt, die geglückten fallen raus.
5. `varIsLoading` wird auf jedem Pfad zurückgesetzt. Doppelklick wird per `DisplayMode` gesperrt.
Schwachstellen, die ich selbst sehe: `ForAll` mit `Patch` wird als `app-ForAllWithMutation` gemeldet; jede Zeile kostet einen Lesezugriff mehr; `ForAll` garantiert keine Reihenfolge (A→B-Kollision im selben Lauf); unklar, ob `ForAll` im Verhalten-Kontext Ergebnisse sammeln kann, ohne `Collect` in der Schleife (das ist in `ForAll` erlaubt, aber nicht in `With`-Records). Das ist nur ein Entwurf, kein geprüfter Vorschlag.

---

## 9. Recherchestand (Stand 05./06.10.2026)

| Aussage | Beleg | Status |
|---|---|---|
| `Patch(Quelle; Tabelle)` ist laut Doku ein "single call" | Microsoft Learn, Patch-Funktion | Doku sagt nichts, ob das ein oder N Netzwerkaufrufe sind |
| `Patch(Quelle; Collection)` ist bei SharePoint ~"10x schneller" als `ForAll(...; Patch(...))` ("all of the updates simultaneously") | matthewdevaney.com "PATCH Multiple Records In Power Apps 10x Faster"; Kommentare: bei SQL-Server 500 Datensätze nur ca. 33 % schneller (ca. 1,5 min → 1 min) | Einzelbeleg aus einem Blog, nicht an dieser App gemessen. Bedingungen: Spaltennamen müssen exakt passen, ID-Spalte nötig (für Updates), komplexe SharePoint-Spalten (Choice/Lookup) brauchen spezielle Formate |
| Forum-Lösung: Sammel-`Patch` mit einer Tabelle aus `ForAll` statt Schleife bringt "substantielle" Verbesserung | powerusers.microsoft.com "Capture results of ForAll Patch" | Einzelaussage |
| SharePoint-Konnektor-Limit: 600 API-Aufrufe pro Verbindung pro 60 Sekunden; 1000 MB Daten pro Verbindung pro 60 Sekunden | Microsoft Learn, SharePoint-Konnektor | belegt |
| Delegation SharePoint: `=` auf Text/Lookup/Number/DateTime ja; `<, <=, <>, >, >=` auf Number ja, aber auf dem **ID-Feld nur `=`**; `<`/`>` auf DateTime ja; `IsBlank` nicht delegierbar; Person: nur `Email` und `DisplayName` delegierbar; `Not` nicht delegierbar; `Today()` wird als Konstante gesendet und blockiert nicht | Microsoft Learn, SharePoint-Verbindung und Delegations-Übersicht | belegt |
| `CountRows(Filter(...))`: innerer Filter läuft auf dem Server, Zählung lokal | in der Doku nicht gefunden; in Foren so beschrieben | NICHT in der offiziellen Doku belegt |
| Excel/SharePoint begrenzte Delegation; SQL Server/Dataverse sehr gute Delegation; beide Premium-Lizenz pro Nutzer | powerappsguide.com Vergleich (Stand 2021, Preise veraltet) | Einordnung belegt, Preise nicht aktuell |
| Dataverse for Teams ist in M365-/Teams-Lizenz enthalten; "Broad distribution" erlaubt Freigabe per Sicherheitsgruppe außerhalb des Teams | Projektdokument `Analyse_Kostenlose_Datenbank_Alternativen_2026-10-05.md` | nicht für diesen Tenant geprüft; ob Alternate Keys (Unique Constraints) in Dataverse for Teams verfügbar sind: UNSICHER |
| Custom Connector, SQL-Server-Connector, Azure Table Storage: Premium | selbes Dokument | belegt |

---

## 10. Ausdrücklich offene Fragen (bitte beantworten oder als Annahme kennzeichnen)

1. Läuft die Serienbuchung bei der aktuellen App sequenziell oder parallel, und macht der neue Sammel-`Patch` bei SharePoint einen oder N Aufrufe? (Nur im Monitor messbar.)
2. Werden bei `Patch(Tischbuchungen; ForAll(neu; Defaults(Tischbuchungen)); neu)` `Person` und `Tisch` korrekt geschrieben, oder braucht es `'@odata.type'`-Angaben?
3. Was passiert bei Teilausfall mitten im Sammel-`Patch`? Gibt es eine zuverlässige Möglichkeit, die Zahl tatsächlich geschriebener Zeilen zu ermitteln (z. B. SerienID setzen und nachlesen)? SerienID wird bisher nicht geschrieben.
4. Wie kann man die 22:00-Regel entscheiden: ablehnen oder auf 22:00 kappen? (Fachliche Entscheidung von Josias, bisher offen.)
5. Lohnt für (B) die Zeile-für-Zeile-Variante, oder ist Stornieren-only bis nach dem Go-Live besser? (Der andere Claude und Claude Code empfehlen: nicht bauen. Josias möchte es.)
6. Bleibt `varMehrfachAuswahlModus` irgendwo gelesen oder ist sie tot? Nicht geprüft.
7. Warum hat `galAlleTischbuchungen.Items` ein Delegationsdreieck bei nur 240 Zeilen (Person.Email? Now()?).

---

## 11. Regeln für jede Formel in diesem Projekt (alle schon einmal verletzt worden)

- Deutsche Locale: `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet Anweisungen.
- Keine Kommentare in Power Fx (`//` erzeugt app-weite Fehler).
- `With()`-Felder werden gleichzeitig ausgewertet; abhängige Werte brauchen verschachtelte `With`.
- Lookup-Feld schreiben immer `{Id: ...; Value: ...}`; Personenfeld mit vollem Schema.
- Kein eigener `TimeZoneOffset`-Workaround (Power Apps rechnet lokal→UTC beim Patch selbst).
- `Patch` auf frischem `LookUp(...; ID = ...)`, nicht direkt auf eine Variable.
- Eine Variable nie mit zwei verschiedenen Record-Typen befüllen (Typ wird app-weit aus allen `Set` abgeleitet).
- `Set(var; false)` setzt eine Checkbox nicht zurück: zusätzlich `Reset(control)`.
- Nach dem Kopieren einer Formel die variierende Zahl in ALLEN Properties prüfen.
- Named Formulas (`App.Formulas`) dürfen keine `Set()`-Variablen referenzieren und keine Verhaltensfunktionen enthalten.
- `Host.OSType`, nicht `Host.OSName`. Steuerelementnamen/Spaltennamen nie raten.
- `;;` in `If`-Zweigen ist ein bekanntes Kollisionsrisiko; mehrarmiges `If` ist in dieser App bisher nicht erprobt.
- Kleine Schritte, `.msapp`-Export vor jeder Änderung; Studio hat keinen Debugger und keine Diff-Ansicht.
- Zwei Studio-Fenster derselben Person auf derselben App führen zu Schreibschutz. Nur ein Fenster bearbeiten.

---

## 12. Fehler früherer Arbeit (bitte nicht wiederholen)

- Aussagen aus alter Dokumentation statt aus dem Quellcode wurden mit zu viel Bestimmtheit vorgetragen: "Title statt Titel", `Tische.Aktiv`/`Standort`, Refresh-in-ForAll als Hauptverdacht, Master-Bedingung als Hauptdelegationsproblem, "3 statt 51 Zugriffe". Alle wurden später korrigiert.
- Es wurde zeitweise in der falschen App gelesen (Klon "App" statt "Tischbuchung").
- Sammelaufruf-Behauptung (spart keine Aufrufe) und ihre Gegenbehauptung (spart Aufrufe) sind BEIDE nur geschlussfolgert. Bitte nicht als Fakt übernehmen.
- Meine eigene Behauptung vom 05.10., `IsBlank(LookUp(...))` ersetze `CountRows(Filter(...))` delegierbar, war falsch (`IsBlank` ist laut Doku nicht delegierbar, und `ID <>` ist es auch nicht).
- Ein Einfügeunfall: Beim ersten Einbau des neuen Sammel-`Patch`-Blocks ersetzte Josias versehentlich die GANZE Formel statt nur den inneren Block. Die App-Prüfung zeigte "Name ungültig: bestehendeBuchungenTisch". Deshalb liefere Änderungen immer als **vollständige** Ersatzformel für die gesamte Property, nicht als Teilstück.

---

## 13. Was Josias von dir bekommen soll

1. Eine **klare Antwort**, welche der zwei Funktionen (A, B) mit welcher Lösung gebaut werden soll, begründet mit den Verwurfsgründen oben (jede Lösung muss die Ü1–Ü8-Fallen und die Kriterien 1–6 ausdrücklich beantworten).
2. **Vollständige, einfügefertige Formeln** je Steuerelement und Property (nicht nur Teilstücke), in deutscher Locale, ohne Kommentare, mit Einfügereihenfolge und konkreten Testschritten.
3. Für jede Aussage über Geschwindigkeit: kennzeichnen, ob **belegt** (Quelle), **geschlussfolgert** oder **ungemessen**. Dazu die Monitor-Messung, die es entscheidet.
4. Ein ehrliches **Risikourteil** zum Go-Live am 14.10.2026 und einen **Rückfallplan** (welche Zeilen bleiben unverändert, wie kommt man auf den alten Stand zurück).
5. Kurze Zusammenfassung zuerst (Josias liest lange Texte ungern), Details danach.
