# 02 — Jeder Knopf einmal durchgegangen

**Kurzfassung:** Diese Datei geht jedes Steuerelement mit einer Verhaltensformel (`OnSelect`, `OnChange`, `OnCheck`, `OnUncheck`) einmal vollständig durch: Pfad, Klartext, alle Verhaltensformeln wortgetreu, die Zustands-Properties (`DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`), gelesene und geschriebene Variablen, berührte Datenquellen und Befunde. Es sind 95 Steuerelemente. Jeder Befund ist als **BELEGT** (mit Fundstelle) oder **VERMUTUNG** markiert. Formeln stehen in der englischen Schreibweise des Quellcodes (`,` statt `;`), Studio zeigt sie in deutscher Schreibweise.

Davon haben 92 eine inhaltliche Formel. Bei drei Steuerelementen (`Rectangle1`, `Circle1`, `Label1` in `Gallery1`) ist die `OnSelect`-Property gesetzt, aber leer (`OnSelect: =`); sie sind unter „Grundriss" mitgeführt, weil der Klick dort vom darüberliegenden `btnHitArea` aufgefangen wird.

## Inhalt

- Header/Tabs (4)
- Dashboard (12)
- Grundriss (5)
- Buchungsdialog (10)
- Tische-Panel (12)
- Buchungen-Tab inkl. Mehrfachauswahl (13)
- Verwalten-Dialoge (15)
- Check-in (2)
- Details-Popup (1)
- Toter Raumcode (21)

## Header/Tabs

### 1. Screen1 / conHeader / Image6

**Typ:** `Image@2.2.3` · **Eltern:** `conHeader` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4231

**Was er tut:** Aktualisiert die Buchungsdaten: Lade-Overlay an, `Refresh(Tischbuchungen)`, Overlay aus, Meldung „Aktualisiert.“. Das Logo im Header ist der Aktualisieren-Knopf.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`
- Gelesen: nichts
- Datenquellen: Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** 1 Aufruf (Refresh der Liste `Tischbuchungen`, wird als Abfrage mit dem Datenzeilenlimit neu geladen). Danach rechnen alle Galerien und Kacheln neu; das löst weitere Abfragen aus (Schätzung: bei sichtbarem Grundriss 96 bis 108 `LookUp`, dazu die Galerie-Abfragen).

**Befunde**

- **BELEGT** — Dieselbe Formel steht wortgleich in `Image6`, `btnHitArea_1`, `Icon1` und `Icon1_1` (Wartungsfläche: vier Stellen).
- **BELEGT** — Es wird nur `Tischbuchungen` aktualisiert, nicht `Tische` (kein `Refresh(Tische)` im ganzen Quellcode).
- **VERMUTUNG** — Kein `IfError` um `Refresh`: Schlägt der Abruf fehl, erscheint trotzdem „Aktualisiert.“ (Success-Meldung steht unbedingt nach dem Refresh).
- **VERMUTUNG** — Über dem Logo liegt der transparente Knopf `btnHitArea_1` mit gleicher Position und Größe und gleicher Formel; Mausklicks treffen vermutlich zuerst den Knopf.

### 2. Screen1 / conHeader / btnTabDashboard

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conHeader` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4245

**Was er tut:** Wechselt zum Tab „Dashboard“. Setzt nur `varAktiverTab` auf `"dashboard"`; `conDashboard.Visible` und `conBuchungen.Visible` lesen diese Variable.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAktiverTab, "dashboard")
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Dashboard"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAktiverTab`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Set(varAktiverTab, "dashboard")` schließt keinen Dialog (anders als `btnTabBuchungen`, der fünf `varZeige…`-Variablen zurücksetzt).
- **VERMUTUNG** — Offene Zustände von `conBuchungen` (`varZeigeVerwaltenTab`, `varZeigeVerwaltenKlein`, Auswahlmodus) bleiben beim Tabwechsel erhalten; beim Zurückwechseln erscheint der alte Zustand.

### 3. Screen1 / conHeader / btnTabBuchungen

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conHeader` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4264

**Was er tut:** Wechselt zum Tab „Buchungen“ und schließt dabei die Dialoge des Dashboards und Grundrisses (Verwalten, Buchen, Details, Check-in).

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAktiverTab, "buchungen");
Set(varZeigeRaumVerwalten, false);
Set(varZeigeVerwalten, false);
Set(varZeigeDialog, false);
Set(varZeigeDetails, false);
Set(varZeigeCheckin, false);
Set(varZeigeVerlaengern, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Buchungen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAktiverTab`, `varZeigeRaumVerwalten`, `varZeigeVerwalten`, `varZeigeDialog`, `varZeigeDetails`, `varZeigeCheckin`, `varZeigeVerlaengern`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Setzt `varZeigeRaumVerwalten` und `varZeigeVerlaengern` zurück; beide Variablen werden nirgends gelesen (App-Prüfung: `app-UnusedVariables`).
- **BELEGT** — Setzt `varZeigeTischBuchungForm` nicht zurück. `conTischBuchungenPanel.Visible` ist `=varZeigeTischBuchungForm` (Z. 797) ohne Tab-Bedingung.
- **VERMUTUNG** — Das Tische-Panel kann beim Tabwechsel „offen“ bleiben (vermutlich von `conBuchungen`, das im Baum weiter hinten liegt, verdeckt).

### 4. Screen1 / conHeader / btnHitArea_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conHeader` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4317

**Was er tut:** Aktualisiert die Buchungsdaten: Lade-Overlay an, `Refresh(Tischbuchungen)`, Overlay aus, Meldung „Aktualisiert.“. Transparenter Knopf über dem Logo (`X`, `Y`, `Width` = `Image6`).

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Transparent
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.08)
```

`PressedFill`:
```powerfx
=ColorFade(Image6.Fill, -30%)
```

`Text`:
```powerfx
=
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`
- Gelesen: nichts
- Datenquellen: Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** 1 Aufruf (Refresh der Liste `Tischbuchungen`, wird als Abfrage mit dem Datenzeilenlimit neu geladen). Danach rechnen alle Galerien und Kacheln neu; das löst weitere Abfragen aus (Schätzung: bei sichtbarem Grundriss 96 bis 108 `LookUp`, dazu die Galerie-Abfragen).

**Befunde**

- **BELEGT** — Dieselbe Formel steht wortgleich in `Image6`, `btnHitArea_1`, `Icon1` und `Icon1_1` (Wartungsfläche: vier Stellen).
- **BELEGT** — Es wird nur `Tischbuchungen` aktualisiert, nicht `Tische` (kein `Refresh(Tische)` im ganzen Quellcode).
- **VERMUTUNG** — Kein `IfError` um `Refresh`: Schlägt der Abruf fehl, erscheint trotzdem „Aktualisiert.“ (Success-Meldung steht unbedingt nach dem Refresh).

## Dashboard

### 5. Screen1 / conDashboard / galTischbuchungenHeute / Rectangle4

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 372

**Was er tut:** Klick auf die Zeilenfläche wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=ColorValue("#F0F0F0")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 6. Screen1 / conDashboard / galTischbuchungenHeute / Image1_1

**Typ:** `Image@2.2.3` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 382

**Was er tut:** Klick auf das Tischbild wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 7. Screen1 / conDashboard / galTischbuchungenHeute / Image3

**Typ:** `Image@2.2.3` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 392

**Was er tut:** Klick auf das Bearbeiten-Symbol wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 8. Screen1 / conDashboard / galTischbuchungenHeute / lblTischHeute

**Typ:** `Label@2.5.1` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 403

**Was er tut:** Klick auf den Tischnamen wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(50, 49, 48, 1)
```

`Text`:
```powerfx
="Tisch " & ThisItem.Tisch.Value
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 9. Screen1 / conDashboard / galTischbuchungenHeute / lblZeitHeute

**Typ:** `Label@2.5.1` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 422

**Was er tut:** Klick auf die Zeitangabe wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Text`:
```powerfx
=Text(ThisItem.Startzeit, "hh:mm") & " – " & Text(ThisItem.Endzeit, "hh:mm")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 10. Screen1 / conDashboard / galTischbuchungenHeute / lblStatusHeute

**Typ:** `Label@2.5.1` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 440

**Was er tut:** Klick auf die Statusangabe („Einchecken“/„Eingecheckt“) wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=If(ThisItem.CheckedIn, ColorValue("#00A96B"), ColorValue("#FFA500"))
```

`Text`:
```powerfx
=If(ThisItem.CheckedIn, "Eingecheckt", "Einchecken")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 11. Screen1 / conDashboard / galTischbuchungenHeute / Rectangle3

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 450

**Was er tut:** Klick auf den Auswahlbalken wählt die Galeriezeile aus (hebt sie über `ThisItem.IsSelected` hervor). Die Galerie selbst hat kein `OnSelect`, es folgt also keine weitere Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=RGBA(100, 118, 132, 1)
```

`PressedFill`:
```powerfx
=Color.Transparent
```

`Visible`:
```powerfx
=ThisItem.IsSelected
```

Nicht gesetzt: `DisplayMode`, `DisabledFill`, `HoverFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat keine eigene `OnSelect`-Property, der Klick bewirkt nur die Hervorhebung.

### 12. Screen1 / conDashboard / galTischbuchungenHeute / btnEincheckenHeute

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 460

**Was er tut:** Transparenter Knopf über der ganzen Buchungszeile in „My personal desk“. Öffnet den Check-in-Dialog für diese Buchung: merkt sich die Zeile in `varSelectedBuchung` und blendet Details, Buchen und Verwalten aus.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varSelectedBuchung, ThisItem); Set(varZeigeCheckin, true); Set(varZeigeDetails, false); Set(varZeigeDialog, false); Set(varZeigeVerwalten, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Transparent
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.04)
```

`PressedFill`:
```powerfx
=RGBA(0, 0, 0, 0.1)
```

`Text`:
```powerfx
=
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varSelectedBuchung`, `varZeigeCheckin`, `varZeigeDetails`, `varZeigeDialog`, `varZeigeVerwalten`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine (reine Variablenzuweisung). Der Dialog selbst liest `varSelectedBuchung` ohne neue Abfrage.

**Befunde**

- **BELEGT** — Kein Zeitfenster: `OnSelect` (Z. 472) prüft nichts. Die Galerie `galTischbuchungenHeute` listet bei `varAnsichtsDatum <> Today()` alle eigenen Buchungen des gewählten Tages (Items, Z. 366), also lässt sich auch für künftige Tage ein-/auschecken.
- **BELEGT** — `varSelectedBuchung` wird mit `ThisItem` der Galerie (Typ `Tischbuchungen`) belegt, derselbe Datensatztyp wie in `btnHitArea` (`LookUp`-Ergebnis).

### 13. Screen1 / conDashboard / galTischbuchungenHeute / btnVerwalten

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galTischbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 480

**Was er tut:** Stift-Knopf rechts in der Zeile in „My personal desk“. Öffnet den Grundriss-Verwalten-Dialog `conVerwaltenDialog` (Stornieren/Verlängern) für diese Buchung und setzt die Dauerauswahl zurück.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varSelectedBuchung, ThisItem);
Set(varZeigeVerwalten, true);
Set(varZeigeCheckin, false);
Set(varZeigeDetails, false);
Set(varZeigeDialog, false);
Set(varAusgewaehltePlusDauer, Blank())
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Transparent
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.2)
```

`PressedFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`Text`:
```powerfx
=
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varSelectedBuchung`, `varZeigeVerwalten`, `varZeigeCheckin`, `varZeigeDetails`, `varZeigeDialog`, `varAusgewaehltePlusDauer`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine beim Klick. Der geöffnete Dialog rechnet danach pro Plus-Knopf 2 Abfragen (siehe `btnPlus1Std`).

**Befunde**

- **BELEGT** — Setzt `varSelectedBuchung`. Dieselbe Variable bedient auch den Details-Popup, den Check-in-Dialog und (fälschlich) die Dauer-Knöpfe des Buchungen-Tabs (siehe `btnPlus1Std_1`, Befund B0).
- **BELEGT** — Setzt `varAusgewaehltePlusDauer` auf `Blank()`; `ddStockwerk.OnSelect` setzt dieselbe Variable auf `0` (uneinheitlich).

### 14. Screen1 / conDashboard / btnTischHinzufügen

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conDashboard` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 713

**Was er tut:** Knopf „Tisch Buchen“ im Dashboard. Öffnet das Tische-Panel `conTischBuchungenPanel` und setzt dessen Wiederholungs- und Schnellwahl-Zustand zurück.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeTischBuchungForm, true);
Set(varWiederholen, false);
Reset(chkWiederholenPanel);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Reset(tglTagMo_1);
Reset(tglTagDi_1);
Reset(tglTagMi_1);
Reset(tglTagDo_1);
Reset(tglTagFr_1);
Set(varAusgewaehltePanelDauer, Blank());
Set(varStartOverridePanel, "");
Set(varEndeOverridePanel, "")
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#D0D0D0")
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.2)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Tisch Buchen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeTischBuchungForm`, `varWiederholen`, `varWiederholenModus`, `varTagMo`, `varTagDi`, `varTagMi`, `varTagDo`, `varTagFr`, `varTagSa`, `varTagSo`, `varAusgewaehltePanelDauer`, `varStartOverridePanel`, `varEndeOverridePanel`, `Reset(chkWiederholenPanel)`, `Reset(tglTagMo_1)`, `Reset(tglTagDi_1)`, `Reset(tglTagMi_1)`, `Reset(tglTagDo_1)`, `Reset(tglTagFr_1)`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine beim Klick. Das geöffnete Panel berechnet Dropdowns und die 5-/9-Std-Knöpfe mit eigenen Abfragen (siehe `btn5Std`).

**Befunde**

- **BELEGT** — Setzt Dropdown und Datum nicht zurück: kein `Reset(ddTischePanel)`, `Reset(dpDatumTischePanel)`, `Reset(dpWiederholenBis_1)`. `ddTischePanel` hat kein `Default` und behält nach dem ersten Gebrauch die zuletzt gewählte Auswahl (nicht belegt, ob dies beim erneuten Einblenden tatsächlich passiert).
- **BELEGT** — Setzt `varTagSa` und `varTagSo` zurück, aber nur fünf Toggles (`tglTagMo_1` bis `tglTagFr_1`). Im Tische-Panel gibt es keine Toggles für Sa/So (Quellcode: nur diese fünf `tglTag…_1`).
- **BELEGT** — Setzt dieselben Variablen (`varWiederholen`, `varWiederholenModus`, `varTagMo`…`varTagSo`) wie der Buchungsdialog; beide Speichern-Wege teilen sich diese Variablen.

### 15. Screen1 / conDashboard / dpAnsichtsDatum

**Typ:** `Classic/DatePicker@2.6.0` · **Eltern:** `conDashboard` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 757

**Was er tut:** Datumswähler für die Ansicht (Dashboard und Grundriss). Übernimmt das gewählte Datum nach `varAnsichtsDatum`; alle Kacheln und die Galerie „My personal desk“ rechnen daraufhin für diesen Tag.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varAnsichtsDatum, dpAnsichtsDatum.SelectedDate)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=Color.Transparent
```

`Fill`:
```powerfx
=Color.Transparent
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAnsichtsDatum`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Auslöser für ca. 96 bis 108 `LookUp` auf `Tischbuchungen` im Grundriss (Kacheln lesen `varAnsichtsDatum`) plus die Abfrage von `galTischbuchungenHeute` (Schätzung).

**Befunde**

- **BELEGT** — Kein `DefaultDate`, kein Mindestdatum: Auch vergangene Tage sind wählbar. `varAnsichtsDatum` (OnStart: `Today()`) und der Picker-Anzeigewert können auseinanderlaufen, weil nur `OnChange` die Variable setzt.
- **BELEGT** — `dpDatum` und `dpDatumTischePanel` nehmen `varAnsichtsDatum` als `DefaultDate`; ein vergangenes Ansichtsdatum würde als Buchungsdatum vorbelegt. Der Quellcode von `btnSpeichern`/`btnSpeichernTischePanel` hat keine Sperre gegen Zeiträume in der Vergangenheit.

### 16. Screen1 / conDashboard / Icon1_1

**Typ:** `Classic/Icon@2.5.0` · **Eltern:** `conDashboard` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 772

**Was er tut:** Aktualisiert die Buchungsdaten: Lade-Overlay an, `Refresh(Tischbuchungen)`, Overlay aus, Meldung „Aktualisiert.“. 

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(32, 54, 71, 1)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`
- Gelesen: nichts
- Datenquellen: Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** 1 Aufruf (Refresh der Liste `Tischbuchungen`, wird als Abfrage mit dem Datenzeilenlimit neu geladen). Danach rechnen alle Galerien und Kacheln neu; das löst weitere Abfragen aus (Schätzung: bei sichtbarem Grundriss 96 bis 108 `LookUp`, dazu die Galerie-Abfragen).

**Befunde**

- **BELEGT** — Dieselbe Formel steht wortgleich in `Image6`, `btnHitArea_1`, `Icon1` und `Icon1_1` (Wartungsfläche: vier Stellen).
- **BELEGT** — Es wird nur `Tischbuchungen` aktualisiert, nicht `Tische` (kein `Refresh(Tische)` im ganzen Quellcode).
- **VERMUTUNG** — Kein `IfError` um `Refresh`: Schlägt der Abruf fehl, erscheint trotzdem „Aktualisiert.“ (Success-Meldung steht unbedingt nach dem Refresh).

## Grundriss

### 17. Screen1 / conGrundriss / Gallery1 / Rectangle1

**Typ:** `Rectangle@2.3.0` · **Eltern:** `Gallery1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 61

**Was er tut:** Kachel-Rechteck eines Tisches in `Gallery1`. Es trägt die Belegungsfarbe (grün frei, orange gebucht, rot eingecheckt). `OnSelect` ist leer gesetzt (`=`); der Klick wird vom darüberliegenden `btnHitArea` aufgefangen.

**Verhaltensformel**

`OnSelect`: leer gesetzt (im Quellcode steht `OnSelect: =` ohne Inhalt).

**Zustand und Aussehen**

`Fill`:
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
    ColorValue("#00A96B"),
    If(
      relevanteBuchung.CheckedIn,
      ColorValue("#EB3951"),
      ColorValue("#FFA500")
    )
  )
)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: `varAnsichtsDatum`, `varAusgewaehltesStockwerk`, `colTischPositionen`, `colTischPositionenUG`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine beim Klick. Die `Fill`-Formel macht pro Kachel 1 `LookUp` auf `Tischbuchungen` bei jedem Neuberechnen.

**Befunde**

- **BELEGT** — `OnSelect: =` (Z. 105): Die Property ist gesetzt, aber leer. Kein Verhalten.
- **BELEGT** — Pro Kachel lesen `Rectangle1.Fill`, `Circle1.BorderColor`, `Circle1.BorderStyle` (zwei Abfragen), `Circle1.Fill` und `Label1.Text` jeweils neu in `Tischbuchungen` (rund 6 `LookUp` je Kachel, bei 16 OG-/18 UG-Tischen etwa 96 bis 108).

### 18. Screen1 / conGrundriss / Gallery1 / Circle1

**Typ:** `Circle@2.3.0` · **Eltern:** `Gallery1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 146

**Was er tut:** Runder Marker in der Kachel (Initialen-Hintergrund). `OnSelect` ist leer gesetzt; der Klick geht an `btnHitArea`.

**Verhaltensformel**

`OnSelect`: leer gesetzt (im Quellcode steht `OnSelect: =` ohne Inhalt).

**Zustand und Aussehen**

`Fill`:
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(IsBlank(relevanteBuchung), ColorValue("#4DC398"), Color.White)
)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: `varAnsichtsDatum`, `varAusgewaehltesStockwerk`, `varZoom`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, BorderColor); LookUp auf `Tischbuchungen` (lesen, BorderStyle); LookUp auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine beim Klick. `BorderColor`, `BorderStyle` und `Fill` enthalten je ein oder zwei `LookUp` auf `Tischbuchungen` (insgesamt 5 pro Kachel).

**Befunde**

- **BELEGT** — `OnSelect: =` (Z. 188) leer gesetzt.

### 19. Screen1 / conGrundriss / Gallery1 / Label1

**Typ:** `Label@2.5.1` · **Eltern:** `Gallery1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 197

**Was er tut:** Beschriftung der Kachel: Initialen der buchenden Person. `OnSelect` ist leer gesetzt; der Klick geht an `btnHitArea`.

**Verhaltensformel**

`OnSelect`: leer gesetzt (im Quellcode steht `OnSelect: =` ohne Inhalt).

**Zustand und Aussehen**

`Text`:
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
    "",
    Upper(Left(First(Split(relevanteBuchung.Person.DisplayName, " ")).Value, 1) &
          Left(Last(Split(relevanteBuchung.Person.DisplayName, " ")).Value, 1))
  )
)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: `varAusgewaehltesStockwerk`, `varAnsichtsDatum`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, Text)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine beim Klick. `Text` enthält 1 `LookUp` auf `Tischbuchungen`.

**Befunde**

- **BELEGT** — `OnSelect: =` (Z. 205) leer gesetzt.
- **BELEGT** — Die Initialen werden aus `relevanteBuchung.Person.DisplayName` gebildet (`Split(..., " ")`, erstes und letztes Wort). Jeder Nutzer sieht damit die Initialen fremder Buchungen (Datenschutzfrage, siehe `07_OFFENE_FRAGEN.md`).

### 20. Screen1 / conGrundriss / Gallery1 / btnHitArea

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `Gallery1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 233

**Was er tut:** Transparenter Klickbereich über jeder Tischkachel. Ist der Tisch zurzeit (bzw. am Ansichtstag) frei, öffnet er den Buchungsdialog für diesen Tisch und setzt die Wiederholungsoptionen zurück; ist er besetzt, öffnet er das Details-Popup mit der Buchung.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today(),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)),
        LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days))
      )
  },
  If(
    IsBlank(relevanteBuchung),
      Set(varSelectedTisch, ThisItem);
      Set(varZeigeDialog, true);
      Set(varZeigeDetails, false);
      Set(varZeigeCheckin, false);
      Set(varZeigeVerwalten, false);
      Set(varWiederholen, false);
      Set(varWiederholenModus, "Wochentage");
      Set(varTagMo, false);
      Set(varTagDi, false);
      Set(varTagMi, false);
      Set(varTagDo, false);
      Set(varTagFr, false);
      Set(varTagSa, false);
      Set(varTagSo, false),
      Set(varDetailsTisch, ThisItem); Set(varSelectedBuchung, relevanteBuchung);
      Set(varZeigeDetails, true);
      Set(varZeigeDialog, false);
      Set(varZeigeCheckin, false);
      Set(varZeigeVerwalten, false)
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Transparent
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.15)
```

`PressedFill`:
```powerfx
=ColorFade(Rectangle1.Fill, -30%)
```

`Text`:
```powerfx
=
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varSelectedTisch`, `varZeigeDialog`, `varZeigeDetails`, `varZeigeCheckin`, `varZeigeVerwalten`, `varWiederholen`, `varWiederholenModus`, `varTagMo`, `varTagDi`, `varTagMi`, `varTagDo`, `varTagFr`, `varTagSa`, `varTagSo`, `varDetailsTisch`, `varSelectedBuchung`
- Gelesen: `varAnsichtsDatum`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** 1 `LookUp` auf `Tischbuchungen` beim Klick (Einschätzung der Delegierbarkeit siehe `04_DATENQUELLEN.md`).

**Befunde**

- **BELEGT** — Frei/besetzt wird nur im Fenster „läuft jetzt oder beginnt in den nächsten 30 Minuten“ bestimmt (`Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)`, Z. 251). Eine Buchung, die später am Tag beginnt, macht die Kachel „frei“; die Kollision wird erst im Speichern geprüft.
- **BELEGT** — Setzt im Frei-Zweig `varWiederholen` und `varTagMo`…`varTagSo` zurück, aber weder `chkWiederholen` (hat `Default: =varWiederholen`, wird also mitgesetzt) noch `ddStart`/`ddEnde`/`dpDatum`.
- **BELEGT** — Setzt im Besetzt-Zweig `varSelectedBuchung` mit dem `LookUp`-Ergebnis und `varDetailsTisch` (wird sonst nirgends gesetzt, nur in `conDetailsPopup.X/Y` gelesen).
- **BELEGT** — `varDetailsTisch` und `varZeigeTischBuchungForm` werden in `App.OnStart` nicht initialisiert.

### 21. Screen1 / conGrundriss / ddStockwerk

**Typ:** `Classic/DropDown@2.3.1` · **Eltern:** `conGrundriss` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 303

**Was er tut:** Dropdown „MMS Obergeschoss/Untergeschoss“ oben links im Grundriss. `OnSelect` (beim Öffnen) schließt alle Dialoge, `OnChange` setzt das gewählte Stockwerk (`"OG"`/`"UG"`) in `varAusgewaehltesStockwerk`; danach lädt `Gallery1` die Tische des Geschosses.

**Verhaltensformeln**

`OnChange`:
```powerfx
=Set(varAusgewaehltesStockwerk, ddStockwerk.Selected.Kurz);
Set(varStockwerkDropdownOffen, false)
```

`OnSelect`:
```powerfx
=Set(varStockwerkDropdownOffen, true);
Set(varZeigeDialog, false);
Set(varZeigeDetails, false);
Set(varZeigeCheckin, false);
Set(varZeigeVerwalten, false);
Set(varZeigeVerlaengern, false);
Set(varSelectedTisch, Blank());
Set(varSelectedBuchung, Blank());
Set(varAusgewaehltePlusDauer, 0)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=Color.Black
```

`Fill`:
```powerfx
=RGBA(0, 0, 0, 0)
```

`HoverFill`:
```powerfx
=RGBA(23, 20, 150, 0.08)
```

`PressedFill`:
```powerfx
=RGBA(32, 54, 71, 1)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltesStockwerk`, `varStockwerkDropdownOffen`, `varZeigeDialog`, `varZeigeDetails`, `varZeigeCheckin`, `varZeigeVerwalten`, `varZeigeVerlaengern`, `varSelectedTisch`, `varSelectedBuchung`, `varAusgewaehltePlusDauer`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Auslöser: `Gallery1.Items` (`Filter(Tische, Geschoss.Value = ...)`, 1 Abfrage) und alle Kachel-`LookUp` für das neue Geschoss (ca. 96 bis 108).

**Befunde**

- **BELEGT** — `OnSelect` setzt `Set(varAusgewaehltePlusDauer, 0)` (Z. 333). Überall sonst steht `Blank()` für „keine Dauer“. `btnVerlängern` und `btnVerlängern_1` prüfen nur `IsBlank(varAusgewaehltePlusDauer)`; `0` gilt nicht als leer.
- **VERMUTUNG** — Folge: Wer das Stockwerk wechselt, danach im Buchungen-Tab ohne Dauerwahl „Speichern“ im Verwalten-Dialog drückt, bekäme `Endzeit + 0 Minuten` gepatcht statt der Warnung „Bitte eine Dauer auswählen.“ (`btnVerwalten_2` setzt die Variable beim Öffnen nicht zurück).
- **BELEGT** — `varStockwerkDropdownOffen` wird gesetzt (`OnSelect` true, `OnChange` false) und nirgends gelesen (App-Prüfung: `app-UnusedVariables`). Wird die Auswahl ohne Änderung geschlossen, bleibt sie `true`.
- **BELEGT** — Setzt `varSelectedTisch` und `varSelectedBuchung` auf `Blank()`; `varSelectedBuchungTab` wird nicht berührt.

## Buchungsdialog

### 22. Screen1 / conBuchungDialog / btnSpeichern

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2716

**Was er tut:** Knopf „Speichern“ im Buchungsdialog des Grundrisses. Berechnet Start und Ende aus Datum und Dropdowns, bildet bei „Wiederholen“ die Liste der Termine (höchstens 14 Tage ab Startdatum), prüft jeden Termin gegen die vorab geladenen Buchungen des Tisches und schreibt alle freien Termine mit einem Sammel-`Patch`. Danach folgt eine Meldung, `Refresh`, Dialog schließen und Zurücksetzen der Wiederholungs-Variablen.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
With(
  {
    neuStart: dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value, 2)), Value(Mid(ddStart.Selected.Value, 4, 2)), 0),
    neuEnde: dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value, 2)), Value(Mid(ddEnde.Selected.Value, 4, 2)), 0),
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate, dpWiederholenBis.SelectedDate, dpDatum.SelectedDate),
    bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)
  },
  With(
    { effektivesBis: Min(effektivesBisRoh, dpDatum.SelectedDate + 14) },
    With(
      { anzahlTage: DateDiff(dpDatum.SelectedDate, effektivesBis, TimeUnit.Days) + 1 },
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage, 0), DateAdd(dpDatum.SelectedDate, Value, TimeUnit.Days)) },
        With(
          {
            datumsListe:
              If(
                !varWiederholen,
                [dpDatum.SelectedDate],
                If(
                  varWiederholenModus = "Taeglich",
                  alleDatumsWerte,
                  Filter(
                    alleDatumsWerte,
                    Switch(
                      Weekday(Value, StartOfWeek.Monday),
                      1, varTagMo, 2, varTagDi, 3, varTagMi, 4, varTagDo, 5, varTagFr, 6, varTagSa, 7, varTagSo
                    )
                  )
                )
              )
          },
          If(
            varWiederholen && CountRows(datumsListe) = 0,
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo,
              Notify("Bitte mindestens einen Wochentag auswählen.", NotificationType.Warning),
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen.", NotificationType.Warning)
            ),
            With(
              {
                neueDatensaetze:
                  ForAll(
                    Filter(
                      datumsListe As Eintrag,
                      CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0)))) = 0
                    ) As Frei,
                    {
                      Tisch: {Id: varSelectedTisch.ID, Value: varSelectedTisch.Titel},
                      Startzeit: Frei.Value + Time(Hour(neuStart), Minute(neuStart), 0),
                      Endzeit: Frei.Value + Time(Hour(neuEnde), Minute(neuEnde), 0),
                      Person: {
                        Claims: "i:0#.f|membership|" & Lower(User().Email),
                        Department: "",
                        DisplayName: User().FullName,
                        Email: User().Email,
                        JobTitle: "",
                        Picture: ""
                      }
                    }
                  )
              },
              With(
                {
                  speicherStatus:
                    If(
                      CountRows(neueDatensaetze) = 0,
                      "keine",
                      IfError(
                        Patch(Tischbuchungen, ForAll(neueDatensaetze, Defaults(Tischbuchungen)), neueDatensaetze),
                        "fehler",
                        "ok"
                      )
                    )
                },
                With(
                  { anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze) },
                  If(
                    speicherStatus = "fehler",
                    Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen.", NotificationType.Error),
                    If(
                      effektivesBisRoh > effektivesBis,
                      Notify("Wiederholung wurde auf 2 Wochen begrenzt.", NotificationType.Warning),
                      If(
                        anzahlUebersprungen > 0,
                        Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden.", NotificationType.Warning),
                        Notify("Buchung(en) erfolgreich gespeichert.", NotificationType.Success)
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);
Refresh(Tischbuchungen);
Set(varZeigeDialog, false);
Set(varWiederholen, false);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Set(varIsLoading, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#00A96B")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=ColorValue("#00a96b")
```

`Text`:
```powerfx
="Speichern"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`, `varZeigeDialog`, `varWiederholen`, `varWiederholenModus`, `varTagMo`, `varTagDi`, `varTagMi`, `varTagDo`, `varTagFr`, `varTagSa`, `varTagSo`
- Gelesen: `varSelectedTisch`
- Datenquellen: Patch auf `Tischbuchungen` (schreiben/steuern, OnSelect); Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect); Filter auf `Tischbuchungen` (lesen, OnSelect); Defaults auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 Abfrage `Filter(Tischbuchungen, Tisch.Value = …)` (`bestehendeBuchungenTisch`, ohne Zeitgrenze) plus entweder 1 (Sammelaufruf) oder N Schreibaufrufe (je Termin eins, falls der Konnektor den Sammel-`Patch` zeilenweise sendet; nicht gemessen), 1 `Refresh`. Die Abfrage `bestehendeBuchungenTisch` wird je Termin in `CountRows(Filter(...))` benutzt; ob Power Apps die Tabelle einmal lädt oder bei jedem Zugriff neu abfragt, ist hier nicht belegt (UNSICHER). Bei 14 Terminen: 3 bis 16 Aufrufe.

**Befunde**

- **BELEGT** — Sammel-`Patch` steht im Quellcode: `Patch(Tischbuchungen, ForAll(neueDatensaetze, Defaults(Tischbuchungen)), neueDatensaetze)` in `IfError` (Z. 2798). Laufzeitverhalten (Spalten `Person`, `Tisch`, Zahl der Netzwerkaufrufe, Teilausfall) ist im Quellcode nicht prüfbar: UNSICHER.
- **BELEGT** — `Person` wird ohne `'@odata.type'` geschrieben (Z. 2780 ff.: `Claims`, `Department`, `DisplayName`, `Email`, `JobTitle`, `Picture`; `Tisch` steht in Z. 2777 als `{Id, Value}`). Der alte Raumcode `btnSpeichernRaumPanel` schreibt zusätzlich `'@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser"` (Z. 2306). Ob das beim Sammel-`Patch` nötig ist, ist offen (Ü6).
- **BELEGT** — K4.2 nicht umgesetzt: `effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate, …)` (Z. 2733) benutzt `<>` statt `>`. `dpWiederholenBis` hat kein `DefaultDate` und zeigt heute; bei künftigem Startdatum liegt „bis“ vor „von“, `anzahlTage` ist ≤ 0 und es erscheint die irreführende Meldung „Bitte mindestens einen Wochentag auswählen.“
- **BELEGT** — K4.1 nicht umgesetzt: `bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = varSelectedTisch.Titel)` (Z. 2734) hat keine Zeitgrenze und lädt alle Buchungen des Tisches (bis zum Datenzeilenlimit).
- **BELEGT** — K5 nicht umgesetzt: `btnSpeichern` hat keine `DisplayMode`-Property; der Knopf ist während des Schreibens nicht gesperrt (Ü4). Das Lade-Overlay `conLadeOverlay` deckt den Schirm erst nach `Set(varIsLoading, true)`.
- **BELEGT** — Der Aufräumblock (Z. 2828 bis 2839: `Refresh`, `Set(varZeigeDialog, false)`, Zurücksetzen von `varWiederholen`, `varWiederholenModus`, `varTagMo`…`varTagSo`) läuft unbedingt, auch wenn `speicherStatus = "fehler"`: Der Dialog schließt, die Eingaben sind verloren (Ü2). `Set(varIsLoading, false)` steht am Ende der Sequenz, nicht in einem `If`-Zweig, wird also auf jedem Pfad erreicht.
- **BELEGT** — Meldung: Der Hinweis „Wiederholung wurde auf 2 Wochen begrenzt.“ steht vor der Kollisions- und Erfolgsmeldung im `If` (Z. 2810) und verdrängt sie (Schwäche 3 aus dem Briefing).
- **BELEGT** — Die Zahl `anzahlUebersprungen` ist `CountRows(datumsListe) - CountRows(neueDatensaetze)` (Z. 2805), also aus lokalen Collections berechnet. Was SharePoint tatsächlich angenommen hat, wird nicht nachgelesen (Ü1). Bei `"fehler"` sagt die Meldung nur „Möglicherweise wurden einzelne Termine gespeichert“.
- **BELEGT** — Kein Feld `SerienID` im geschriebenen Datensatz (Z. 2777 bis 2789: `Tisch`, `Startzeit`, `Endzeit`, `Person`); die Spalte `SerienID` existiert (`DataSources.json`), wird in der App nicht benutzt.
- **BELEGT** — Prüfung und Schreiben sind nicht atomar: Zwischen `Filter(Tischbuchungen, …)` und `Patch` können Sekunden vergehen. Zwei Nutzer, die zugleich denselben Tisch buchen, können beide die Prüfung bestehen (Doppelbuchungsweg). Eintritt in der Praxis: VERMUTUNG.
- **BELEGT** — Vergangenheit: Es gibt keine Prüfung `Startzeit >= Now()`. Nur `ddStart.Items` begrenzt heute auf „ab jetzt, auf 30 Minuten gerundet“; für andere Daten (auch vergangene) beginnt die Liste bei 08:00.

### 23. Screen1 / conBuchungDialog / btnAbbrechen

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2846

**Was er tut:** Knopf „Abbrechen“ im Buchungsdialog. Schließt den Dialog und setzt die Wiederholungs-Variablen zurück, ohne zu speichern.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeDialog, false);
Set(varWiederholen, false);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, 30%)
```

`PressedFill`:
```powerfx
=Color.Black
```

`Text`:
```powerfx
="Abbrechen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeDialog`, `varWiederholen`, `varWiederholenModus`, `varTagMo`, `varTagDi`, `varTagMi`, `varTagDo`, `varTagFr`, `varTagSa`, `varTagSo`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Setzt `dpDatum`, `ddStart`, `ddEnde`, `dpWiederholenBis` nicht zurück (kein `Reset`). Die Dropdowns setzt nur `dpDatum.OnChange` zurück.
- **BELEGT** — Kein `varIsLoading`, keine Datenoperation: kein Risiko.

### 24. Screen1 / conBuchungDialog / dpDatum

**Typ:** `Classic/DatePicker@2.6.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2874

**Was er tut:** Datumswähler im Buchungsdialog (vorbelegt mit `varAnsichtsDatum`). Beim Ändern werden Start- und Ende-Dropdown neu auf ihre Standardwerte gesetzt, weil sich die auswählbaren Zeiten (heute: ab jetzt, sonst ab 08:00) ändern.

**Verhaltensformel**

`OnChange`:
```powerfx
=Reset(ddStart);
Reset(ddEnde)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: `Reset(ddStart)`, `Reset(ddEnde)`
- Gelesen: `varAnsichtsDatum`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine Datenzugriffe.

**Befunde**

- **BELEGT** — `ddStart.Default` und `ddEnde.Default` lesen `varStartOverride` und `varEndeOverride` (Z. 2627, 2685). Diese zwei Variablen werden nur in `App.OnStart` auf `""` gesetzt und sonst nirgends; die Dialog-Variante hat keine Schnellwahl-Knöpfe. Die Bedingung ist also immer „kein Override“ (toter Zweig).

### 25. Screen1 / conBuchungDialog / chkWiederholen

**Typ:** `Classic/CheckBox@2.1.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2887

**Was er tut:** Kontrollkästchen „Wiederholen“ im Buchungsdialog. Schaltet `varWiederholen` und damit die Wochentags-Schalter, den „Wiederholen bis“-Picker und die Dialoghöhe (350 oder 500).

**Verhaltensformeln**

`OnCheck`:
```powerfx
=Set(varWiederholen, true)
```

`OnUncheck`:
```powerfx
=Set(varWiederholen, false)
```

**Zustand und Aussehen**

`Text`:
```powerfx
="Wiederholen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varWiederholen`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Default: =varWiederholen`; der Zustand folgt der Variablen. Das Tische-Panel hat dagegen kein `Default` und braucht `Reset(chkWiederholenPanel)`.
- **BELEGT** — `varWiederholenModus` wird nirgends auf `"Taeglich"` gesetzt (nur auf `"Wochentage"`). Der Zweig `varWiederholenModus = "Taeglich"` in `btnSpeichern` (Z. 2749) und `btnSpeichernTischePanel` (Z. 981) ist nicht erreichbar.

### 26. Screen1 / conBuchungDialog / tglTagMo

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2901

**Was er tut:** Wochentags-Schalter „Mo“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagMo`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagMo, tglTagMo.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagMo`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Default: =varTagMo`: Der Schalter folgt der Variablen und wird beim Zurücksetzen der Variablen mitgesetzt (anders als im Tische-Panel).
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 27. Screen1 / conBuchungDialog / tglTagDi

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2914

**Was er tut:** Wochentags-Schalter „Di“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagDi`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagDi, tglTagDi.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagDi`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Default: =varTagDi`: Der Schalter folgt der Variablen und wird beim Zurücksetzen der Variablen mitgesetzt (anders als im Tische-Panel).
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 28. Screen1 / conBuchungDialog / tglTagMi

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2927

**Was er tut:** Wochentags-Schalter „Mi“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagMi`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagMi, tglTagMi.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagMi`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Default: =varTagMi`: Der Schalter folgt der Variablen und wird beim Zurücksetzen der Variablen mitgesetzt (anders als im Tische-Panel).
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 29. Screen1 / conBuchungDialog / tglTagDo

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2940

**Was er tut:** Wochentags-Schalter „Do“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagDo`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagDo, tglTagDo.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagDo`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Default: =varTagDo`: Der Schalter folgt der Variablen und wird beim Zurücksetzen der Variablen mitgesetzt (anders als im Tische-Panel).
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 30. Screen1 / conBuchungDialog / tglTagFr

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2953

**Was er tut:** Wochentags-Schalter „Fr“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagFr`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagFr, tglTagFr.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagFr`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Default: =varTagFr`: Der Schalter folgt der Variablen und wird beim Zurücksetzen der Variablen mitgesetzt (anders als im Tische-Panel).
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 31. Screen1 / conBuchungDialog / dpWiederholenBis

**Typ:** `Classic/DatePicker@2.6.0` · **Eltern:** `conBuchungDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2966

**Was er tut:** Datumswähler „Wiederholen bis“ im Buchungsdialog, nur sichtbar bei angehaktem „Wiederholen“. Die Formeln hier setzen nur Hilfsvariablen; `btnSpeichern` liest den Wert direkt über `dpWiederholenBis.SelectedDate`.

**Verhaltensformeln**

`OnChange`:
```powerfx
=Set(varWiederholenBisGewaehlt, true)
```

`OnSelect`:
```powerfx
=Set(varWiederholenBis, dpWiederholenBis.SelectedDate)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varWiederholenBisGewaehlt`, `varWiederholenBis`
- Gelesen: `varWiederholen`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnChange: =Set(varWiederholenBisGewaehlt, true)` und `OnSelect: =Set(varWiederholenBis, …)`: Beide Variablen werden nirgends gelesen (App-Prüfung `app-UnusedVariables`).
- **BELEGT** — Kein `DefaultDate` (siehe `btnSpeichern`): Der Picker zeigt heute, auch wenn das Startdatum in der Zukunft liegt.

## Tische-Panel

### 32. Screen1 / conTischBuchungenPanel / dpDatumTischePanel

**Typ:** `Classic/DatePicker@2.6.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 892

**Was er tut:** Datumswähler im Tische-Panel (vorbelegt mit `varAnsichtsDatum`). Beim Ändern werden Start- und Ende-Dropdown zurückgesetzt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Reset(ddStartTischePanel);
Reset(ddEndTischePanel)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: `Reset(ddStartTischePanel)`, `Reset(ddEndTischePanel)`
- Gelesen: `varAnsichtsDatum`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine Datenzugriffe.

**Befunde**

- **BELEGT** — Setzt `varStartOverridePanel`/`varEndeOverridePanel` und `varAusgewaehltePanelDauer` nicht zurück; eine zuvor gewählte „5 Std“/„9 Std“-Schnellwahl bleibt aktiv und überschreibt über `varStartOverridePanel` die Dropdown-Standardwerte, auch wenn das Datum wechselt.

### 33. Screen1 / conTischBuchungenPanel / btnSpeichernTischePanel

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 948

**Was er tut:** Knopf „Speichern“ im Tische-Panel. Berechnet Datumsliste und Termine wie `btnSpeichern`, schreibt aber **je Termin einen eigenen `Patch`** (`ForAll … Patch`), zählt „gespeichert“/„übersprungen“, meldet das Ergebnis und räumt umfangreich auf (Panel schließen, Wiederholung, Toggles, Dauerwahl, Overrides zurück).

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
With(
  {
    neuStart: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddStartTischePanel.Selected.Value, 2)), Value(Mid(ddStartTischePanel.Selected.Value, 4, 2)), 0),
    neuEnde: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddEndTischePanel.Selected.Value, 2)), Value(Mid(ddEndTischePanel.Selected.Value, 4, 2)), 0),
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate),
    bestehendeBuchungenTisch: Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel)
  },
  With(
    { effektivesBis: Min(effektivesBisRoh, dpDatumTischePanel.SelectedDate + 14) },
    With(
      { anzahlTage: DateDiff(dpDatumTischePanel.SelectedDate, effektivesBis, TimeUnit.Days) + 1 },
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage, 0), DateAdd(dpDatumTischePanel.SelectedDate, Value, TimeUnit.Days)) },
        With(
          {
            datumsListe:
              If(
                !varWiederholen,
                [dpDatumTischePanel.SelectedDate],
                If(
                  varWiederholenModus = "Taeglich",
                  alleDatumsWerte,
                  Filter(
                    alleDatumsWerte,
                    Switch(
                      Weekday(Value, StartOfWeek.Monday),
                      1, varTagMo, 2, varTagDi, 3, varTagMi, 4, varTagDo, 5, varTagFr, 6, varTagSa, 7, varTagSo
                    )
                  )
                )
              )
          },
          If(
            varWiederholen && CountRows(datumsListe) = 0,
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo,
              Notify("Bitte mindestens einen Wochentag auswählen.", NotificationType.Warning),
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen.", NotificationType.Warning)
            ),
            With(
              {
                ergebnisse:
                  ForAll(
                    datumsListe As Eintrag,
                    If(
                      CountRows(Filter(bestehendeBuchungenTisch, Startzeit < (Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0)))) = 0,
                      With(
                        {
                          neuerEintrag: Patch(Tischbuchungen, Defaults(Tischbuchungen), {
                            Tisch: {Id: ddTischePanel.Selected.ID, Value: ddTischePanel.Selected.Titel},
                            Startzeit: Eintrag.Value + Time(Hour(neuStart), Minute(neuStart), 0),
                            Endzeit: Eintrag.Value + Time(Hour(neuEnde), Minute(neuEnde), 0),
                            Person: {
                              Claims: "i:0#.f|membership|" & Lower(User().Email),
                              Department: "",
                              DisplayName: User().FullName,
                              Email: User().Email,
                              JobTitle: "",
                              Picture: ""
                            }
                          })
                        },
                        "gespeichert"
                      ),
                      "übersprungen"
                    )
                  )
              },
              With(
                { anzahlUebersprungen: CountRows(Filter(ergebnisse, Value = "übersprungen")) },
                If(
                  effektivesBisRoh > effektivesBis,
                  Notify("Wiederholung wurde auf 2 Wochen begrenzt.", NotificationType.Warning),
                  If(
                    anzahlUebersprungen > 0,
                    Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden.", NotificationType.Warning),
                    Notify("Buchung(en) erfolgreich gespeichert.", NotificationType.Success)
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);
Refresh(Tischbuchungen);
Set(varZeigeTischBuchungForm, false);
Set(varAktiverTab, "dashboard");
Set(varWiederholen, false);
Reset(chkWiederholenPanel);
Set(varWiederholenModus, "Wochentage");
Set(varTagMo, false);
Set(varTagDi, false);
Set(varTagMi, false);
Set(varTagDo, false);
Set(varTagFr, false);
Set(varTagSa, false);
Set(varTagSo, false);
Reset(tglTagMo_1);
Reset(tglTagDi_1);
Reset(tglTagMi_1);
Reset(tglTagDo_1);
Reset(tglTagFr_1);
Set(varAusgewaehltePanelDauer, Blank());
Set(varStartOverridePanel, "");
Set(varEndeOverridePanel, "");
Set(varIsLoading, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="Speichern"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`, `varZeigeTischBuchungForm`, `varAktiverTab`, `varWiederholen`, `varWiederholenModus`, `varTagMo`, `varTagDi`, `varTagMi`, `varTagDo`, `varTagFr`, `varTagSa`, `varTagSo`, `varAusgewaehltePanelDauer`, `varStartOverridePanel`, `varEndeOverridePanel`, `Reset(chkWiederholenPanel)`, `Reset(tglTagMo_1)`, `Reset(tglTagDi_1)`, `Reset(tglTagMi_1)`, `Reset(tglTagDo_1)`, `Reset(tglTagFr_1)`
- Gelesen: nichts
- Datenquellen: Patch auf `Tischbuchungen` (schreiben/steuern, OnSelect); Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect); Filter auf `Tischbuchungen` (lesen, OnSelect); Defaults auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 Abfrage `Filter(Tischbuchungen, Tisch.Value = …)` ohne Zeitgrenze, danach 1 `Patch` pro freiem Termin (1 bis 14, nacheinander), 1 `Refresh`. Bei 14 Terminen: 16 Aufrufe (nicht gemessen).

**Befunde**

- **BELEGT** — Noch auf dem alten Stand: `ForAll(datumsListe As Eintrag, If(CountRows(Filter(bestehendeBuchungenTisch, …)) = 0, With({neuerEintrag: Patch(Tischbuchungen, Defaults(Tischbuchungen), {…})}, "gespeichert"), "übersprungen"))` (Z. 1003 ff.). Das ist die einzige Stelle mit der Warnung `app-ForAllWithMutation` der App-Prüfung.
- **BELEGT** — Kein `IfError` um den `Patch`: Das Ergebnis `"gespeichert"` hängt nicht vom Ergebnis des `Patch` ab (die Variable `neuerEintrag` wird im Rumpf nicht benutzt). Schlägt ein `Patch` fehl, kann trotzdem „Buchung(en) erfolgreich gespeichert.“ erscheinen (Briefing Schwäche 4; Laufzeitverhalten nicht geprüft: VERMUTUNG).
- **BELEGT** — K4.1 und K4.2 nicht umgesetzt: `<>` in `effektivesBisRoh` (Z. 965) und `Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel)` ohne Zeitgrenze (Z. 966).
- **BELEGT** — K5 nicht umgesetzt: keine `DisplayMode`-Property am Knopf (Ü4).
- **BELEGT** — Aufräumblock (Z. 1048 bis 1069) läuft unbedingt und ist länger als in `btnSpeichern` (`Reset` von Checkbox und fünf Toggles, `varAusgewaehltePanelDauer`, Overrides, `varAktiverTab`). `Set(varIsLoading, false)` steht am Ende der Sequenz (Ü8: beide Speichern-Wege sind im Rechenteil gleich, im Aufräumteil verschieden).
- **BELEGT** — Kein Check, ob in `ddTischePanel` ein Tisch gewählt ist (`IsBlank(ddTischePanel.Selected)`); `btn5Std`/`btn9Std` prüfen das für ihre Schnellwahl, dieser Knopf nicht. `ddTischePanel` hat kein `Default` (Items = `Tische`).
- **BELEGT** — `ddTischePanel.Items: =Tische` mit `Items.Value: =Title` (Z. 825), während die App sonst `Titel` schreibt. Die App-Prüfung meldet keinen Bindungsfehler (`BindingErrorCount: 0` in `Properties.json`); `usedisplaynamemetadata` ist `true`.
- **BELEGT** — Person ohne `'@odata.type'` wie in `btnSpeichern`. `SerienID` wird nicht geschrieben.
- **BELEGT** — Zeitgleichheit wie bei `btnSpeichern`: Prüfung und Schreiben sind nicht atomar (Doppelbuchungsweg; Eintritt VERMUTUNG).

### 34. Screen1 / conTischBuchungenPanel / btnAbbrechenTischePanel

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1076

**Was er tut:** Zurück-Pfeil „<“ im Tische-Panel. Schließt das Panel, setzt „Wiederholen“ zurück und leert die Checkbox.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeTischBuchungForm, false);
Set(varZeigeTischBuchungForm, false);
Set(varWiederholen, false);
Reset(chkWiederholenPanel)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=RGBA(150, 150, 150, 1)
```

`HoverFill`:
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="<"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeTischBuchungForm`, `varWiederholen`, `Reset(chkWiederholenPanel)`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Set(varZeigeTischBuchungForm, false)` steht zweimal hintereinander (Z. 1088 und 1089).
- **BELEGT** — Setzt Toggles, `varTag…`, `varStartOverridePanel`, `varEndeOverridePanel` und `varAusgewaehltePanelDauer` nicht zurück (macht erst `btnTischHinzufügen` beim nächsten Öffnen).

### 35. Screen1 / conTischBuchungenPanel / tglTagMo_1

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1099

**Was er tut:** Wochentags-Schalter „Mo“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagMo`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagMo, tglTagMo_1.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagMo`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Kein `Default`: Der Zustand wird nur über `Reset(tglTagMo_1)` zurückgesetzt (in `btnTischHinzufügen` und `btnSpeichernTischePanel`), nicht über die Variable.
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 36. Screen1 / conTischBuchungenPanel / tglTagDi_1

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1111

**Was er tut:** Wochentags-Schalter „Di“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagDi`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagDi, tglTagDi_1.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagDi`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Kein `Default`: Der Zustand wird nur über `Reset(tglTagDi_1)` zurückgesetzt (in `btnTischHinzufügen` und `btnSpeichernTischePanel`), nicht über die Variable.
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 37. Screen1 / conTischBuchungenPanel / tglTagMi_1

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1123

**Was er tut:** Wochentags-Schalter „Mi“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagMi`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagMi, tglTagMi_1.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagMi`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Kein `Default`: Der Zustand wird nur über `Reset(tglTagMi_1)` zurückgesetzt (in `btnTischHinzufügen` und `btnSpeichernTischePanel`), nicht über die Variable.
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 38. Screen1 / conTischBuchungenPanel / tglTagDo_1

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1135

**Was er tut:** Wochentags-Schalter „Do“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagDo`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagDo, tglTagDo_1.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagDo`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Kein `Default`: Der Zustand wird nur über `Reset(tglTagDo_1)` zurückgesetzt (in `btnTischHinzufügen` und `btnSpeichernTischePanel`), nicht über die Variable.
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 39. Screen1 / conTischBuchungenPanel / tglTagFr_1

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1147

**Was er tut:** Wochentags-Schalter „Fr“ für die Serienbuchung. Übernimmt den Schaltzustand in `varTagFr`; nur sichtbar, wenn „Wiederholen“ angehakt ist und der Modus `"Wochentage"` gilt.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varTagFr, tglTagFr_1.Value)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen && varWiederholenModus = "Wochentage"
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varTagFr`
- Gelesen: `varWiederholen`, `varWiederholenModus`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Kein `Default`: Der Zustand wird nur über `Reset(tglTagFr_1)` zurückgesetzt (in `btnTischHinzufügen` und `btnSpeichernTischePanel`), nicht über die Variable.
- **BELEGT** — Es gibt nur Schalter für Mo bis Fr. `varTagSa` und `varTagSo` werden nur auf `false` gesetzt, nie auf `true`; Samstag und Sonntag können in einer Serie nicht gebucht werden.

### 40. Screen1 / conTischBuchungenPanel / chkWiederholenPanel

**Typ:** `Classic/CheckBox@2.1.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1159

**Was er tut:** Kontrollkästchen „Wiederholen“ im Tische-Panel. Schaltet `varWiederholen`.

**Verhaltensformeln**

`OnCheck`:
```powerfx
=Set(varWiederholen, true)
```

`OnUncheck`:
```powerfx
=Set(varWiederholen, false)
```

**Zustand und Aussehen**

`Text`:
```powerfx
="Wiederholen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varWiederholen`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Kein `Default`; der Zustand wird nur über `Reset(chkWiederholenPanel)` zurückgesetzt (`btnTischHinzufügen`, `btnAbbrechenTischePanel`, `btnSpeichernTischePanel`). `varWiederholen` ist zugleich die Variable des Buchungsdialogs.

### 41. Screen1 / conTischBuchungenPanel / dpWiederholenBis_1

**Typ:** `Classic/DatePicker@2.6.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1172

**Was er tut:** Datumswähler „Wiederholen bis“ im Tische-Panel. `OnSelect` merkt das Datum in `varWiederholenBis`; `OnChange` enthält eine Formel, die nichts bewirkt.

**Verhaltensformeln**

`OnChange`:
```powerfx
=If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate)
```

`OnSelect`:
```powerfx
=Set(varWiederholenBis, dpWiederholenBis_1.SelectedDate)
```

**Zustand und Aussehen**

`Visible`:
```powerfx
=varWiederholen
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varWiederholenBis`
- Gelesen: `varWiederholen`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnChange: =If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate)` liefert nur einen Wert und setzt nichts; toter Code.
- **BELEGT** — `varWiederholenBis` wird nirgends gelesen (`app-UnusedVariables`).
- **BELEGT** — Kopierfehler im Nachbarelement `Label14` (Hinweis „max. 2 Wochen“): `Color` und `Text` vergleichen `dpDatum.SelectedDate` (Buchungsdialog) statt `dpDatumTischePanel.SelectedDate` (Z. 1193, 1201). Steuerelement des falschen Dialogs.
- **BELEGT** — Kein `DefaultDate`: zeigt heute.

### 42. Screen1 / conTischBuchungenPanel / btn5Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1209

**Was er tut:** Schnellwahl „5 Std“: legt Start auf die aktuelle Uhrzeit (auf 30 Minuten aufgerundet) und Ende fünf Stunden später fest, markiert den Knopf grün und setzt die Dropdowns darauf. Ein zweiter Klick nimmt die Wahl zurück. Der Knopf ist gesperrt (rot), wenn der Tag nicht reicht (nach 22:00), kein Tisch gewählt ist oder der Zeitraum belegt ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 5 },
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 5, TimeUnit.Hours),
        tagesEnde: Time(22, 0, 0)
      },
      If(
        !warAusgewaehlt && endeZeit > tagesEnde,
        Notify("Für 5 Std. ab jetzt reicht der Tag nicht mehr aus.", NotificationType.Warning),
        Set(varAusgewaehltePanelDauer, If(warAusgewaehlt, Blank(), 5));
        Set(varStartOverridePanel, If(warAusgewaehlt, "", Text(startZeit, "hh:mm")));
        Set(varEndeOverridePanel, If(warAusgewaehlt, "", Text(endeZeit, "hh:mm")))
      )
    )
  )
);
Reset(ddStartTischePanel);
Reset(ddEndTischePanel)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 5, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 5, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      varAusgewaehltePanelDauer = 5,
      ColorValue("#00A96B"),
      If(
        endeZeit > tagesEnde,
        ColorFade(ColorValue("#EB3951"), 70%),
        If(
          IsBlank(ddTischePanel.Selected),
          ColorFade(ColorValue("#00A96B"), 70%),
          If(
            CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0,
            ColorFade(ColorValue("#00A96B"), 70%),
            ColorFade(ColorValue("#EB3951"), 70%)
          )
        )
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="5 Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePanelDauer`, `varStartOverridePanel`, `varEndeOverridePanel`, `Reset(ddStartTischePanel)`, `Reset(ddEndTischePanel)`
- Gelesen: nichts
- Datenquellen: Filter auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` enthalten je 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen (2 Abfragen je Knopf, 4 für beide Schnellwahl-Knöpfe). Der Klick selbst macht keine Datenabfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Stundenzahl 5 steht konsistent in `DisplayMode`, `Fill`, `OnSelect` (Vergleich `= 5`, `DateAdd(…, 5, TimeUnit.Hours)`, Meldungstext „5 Std.“) und `Text`; kein Kopierfehler gegenüber `btn9Std`.
- **BELEGT** — Start ist immer die aktuelle Uhrzeit, auch wenn in `dpDatumTischePanel` ein anderer Tag gewählt ist (`startZeit: dpDatumTischePanel.SelectedDate + Time(…minutenJetzt…)`).
- **VERMUTUNG** — Für künftige Tage kann der Override (z. B. „06:30“) vor 08:00 liegen, also nicht in der Liste `ddStartTischePanel.Items` stehen (ab 08:00); wie das Dropdown dann reagiert, ist nicht belegt.
- **BELEGT** — `Reset(ddStartTischePanel); Reset(ddEndTischePanel)` am Ende laufen auch, wenn die Warnung „reicht der Tag nicht mehr aus“ gezeigt wurde.

### 43. Screen1 / conTischBuchungenPanel / btn9Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conTischBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1294

**Was er tut:** Schnellwahl „9 Std“, wie `btn5Std` mit neun Stunden Dauer (ganzer Arbeitstag ab jetzt).

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 9 },
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 9, TimeUnit.Hours),
        tagesEnde: Time(22, 0, 0)
      },
      If(
        !warAusgewaehlt && endeZeit > tagesEnde,
        Notify("Für 9 Std. ab jetzt reicht der Tag nicht mehr aus.", NotificationType.Warning),
        Set(varAusgewaehltePanelDauer, If(warAusgewaehlt, Blank(), 9));
        Set(varStartOverridePanel, If(warAusgewaehlt, "", Text(startZeit, "hh:mm")));
        Set(varEndeOverridePanel, If(warAusgewaehlt, "", Text(endeZeit, "hh:mm")))
      )
    )
  )
);
Reset(ddStartTischePanel);
Reset(ddEndTischePanel)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 9, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) },
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60, 0), Mod(minutenJetzt, 60), 0), 9, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    },
    If(
      varAusgewaehltePanelDauer = 9,
      ColorValue("#00A96B"),
      If(
        endeZeit > tagesEnde,
        ColorFade(ColorValue("#EB3951"), 70%),
        If(
          IsBlank(ddTischePanel.Selected),
          ColorFade(ColorValue("#00A96B"), 70%),
          If(
            CountRows(Filter(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0,
            ColorFade(ColorValue("#00A96B"), 70%),
            ColorFade(ColorValue("#EB3951"), 70%)
          )
        )
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="9 Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePanelDauer`, `varStartOverridePanel`, `varEndeOverridePanel`, `Reset(ddStartTischePanel)`, `Reset(ddEndTischePanel)`
- Gelesen: nichts
- Datenquellen: Filter auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Wie `btn5Std`: 2 Abfragen je Neuberechnen (`DisplayMode`, `Fill`), keine beim Klick.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Stundenzahl 9 steht konsistent in allen Properties (`DisplayMode`, `Fill`, `OnSelect`, Meldungstext, `Text`).
- **VERMUTUNG** — Wegen der aktuellen Uhrzeit als Startpunkt ist die 9-Std-Wahl meist nur vor etwa 13:00 verfügbar (`endeZeit > tagesEnde` sperrt sie danach); ob das so gewollt ist, ist nicht belegt.

## Buchungen-Tab inkl. Mehrfachauswahl

### 44. Screen1 / conBuchungen / galAlleTischbuchungen / Rectangle4_2

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3478

**Was er tut:** Klick auf die Zeilenfläche wählt die Galeriezeile aus (Hervorhebung über `ThisItem.IsSelected`). Die Galerie `galAlleTischbuchungen` hat kein `OnSelect`; es folgt keine Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=RGBA(234, 234, 236, 1)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; reine Hervorhebung.

### 45. Screen1 / conBuchungen / galAlleTischbuchungen / Image1_3

**Typ:** `Image@2.2.3` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3488

**Was er tut:** Klick auf das Tischbild wählt die Galeriezeile aus (Hervorhebung über `ThisItem.IsSelected`). Die Galerie `galAlleTischbuchungen` hat kein `OnSelect`; es folgt keine Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; reine Hervorhebung.

### 46. Screen1 / conBuchungen / galAlleTischbuchungen / Image3_2

**Typ:** `Image@2.2.3` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3498

**Was er tut:** Klick auf das Bearbeiten-Symbol wählt die Galeriezeile aus (Hervorhebung über `ThisItem.IsSelected`). Die Galerie `galAlleTischbuchungen` hat kein `OnSelect`; es folgt keine Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; reine Hervorhebung.

### 47. Screen1 / conBuchungen / galAlleTischbuchungen / lblTischName

**Typ:** `Label@2.5.1` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3509

**Was er tut:** Klick auf den Tischnamen wählt die Galeriezeile aus (Hervorhebung über `ThisItem.IsSelected`). Die Galerie `galAlleTischbuchungen` hat kein `OnSelect`; es folgt keine Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(50, 49, 48, 1)
```

`Text`:
```powerfx
=ThisItem.Tisch.Value
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; reine Hervorhebung.

### 48. Screen1 / conBuchungen / galAlleTischbuchungen / lblRaumZeit

**Typ:** `Label@2.5.1` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3528

**Was er tut:** Klick auf die Zeitangabe wählt die Galeriezeile aus (Hervorhebung über `ThisItem.IsSelected`). Die Galerie `galAlleTischbuchungen` hat kein `OnSelect`; es folgt keine Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Text`:
```powerfx
=Text(ThisItem.Startzeit, "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit, "hh:mm") & " – " & Text(ThisItem.Endzeit, "hh:mm")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; reine Hervorhebung.

### 49. Screen1 / conBuchungen / galAlleTischbuchungen / Rectangle3_2

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3546

**Was er tut:** Klick auf den Auswahlbalken wählt die Galeriezeile aus (Hervorhebung über `ThisItem.IsSelected`). Die Galerie `galAlleTischbuchungen` hat kein `OnSelect`; es folgt keine Aktion und kein Datenzugriff.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=RGBA(100, 118, 132, 1)
```

`PressedFill`:
```powerfx
=Color.Transparent
```

`Visible`:
```powerfx
=ThisItem.IsSelected
```

Nicht gesetzt: `DisplayMode`, `DisabledFill`, `HoverFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `OnSelect: =Select(Parent)`; reine Hervorhebung.

### 50. Screen1 / conBuchungen / galAlleTischbuchungen / btnVerwalten_2

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3556

**Was er tut:** Stift-Knopf in jeder Zeile der Galerie „Tischbuchungen“. Ohne Auswahlmodus öffnet er den Verwalten-Dialog `conVerwaltenDialog_1` (Verlängern/Verkürzen/Stornieren einer Buchung) für diese Zeile; im Auswahlmodus öffnet er den kleinen Dialog `conVerwaltenKlein` (Sammel-Stornieren).

**Verhaltensformel**

`OnSelect`:
```powerfx
=If(
  varAuswahlModusAktiv,
  Set(varGeklickteBuchungKlein, ThisItem);
  Set(varZeigeVerwaltenKlein, true),
  Set(varSelectedBuchungTab, ThisItem);
  Set(varZeigeVerwaltenTab, true);
  Set(varZeigeCheckin, false);
  Set(varZeigeDetails, false);
  Set(varZeigeDialog, false)
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Transparent
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.2)
```

`PressedFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`Text`:
```powerfx
=
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varGeklickteBuchungKlein`, `varZeigeVerwaltenKlein`, `varSelectedBuchungTab`, `varZeigeVerwaltenTab`, `varZeigeCheckin`, `varZeigeDetails`, `varZeigeDialog`
- Gelesen: `varAuswahlModusAktiv`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine beim Klick. Der geöffnete Dialog `conVerwaltenDialog_1` rechnet danach 24 Abfragen je Neuberechnen (6 Dauer-Knöpfe, siehe `btnPlus1Std_1`).

**Befunde**

- **BELEGT** — K1 nicht umgesetzt: Im Nicht-Auswahlmodus-Zweig steht nur `Set(varSelectedBuchungTab, ThisItem)` (Z. 3573), nicht zusätzlich `Set(varSelectedBuchung, ThisItem)`. Die zwölf Dauer-Knopf-Properties lesen aber `varSelectedBuchung` (Befund B0, siehe `btnPlus1Std_1`).
- **BELEGT** — Setzt `varAusgewaehltePlusDauer` nicht zurück; eine zuvor gewählte Dauer (auch `0` aus `ddStockwerk.OnSelect`) bleibt beim Öffnen des Dialogs für eine andere Buchung erhalten.
- **BELEGT** — Im Auswahlmodus wird `varGeklickteBuchungKlein` gesetzt. Sie dient nur der Anzeige im kleinen Dialog (`lblVerwaltenKleinDatum`, `lblVerwaltenKleinZeit`, `lblVerwaltenKleinTitel`); `btnStornierenKlein` storniert die Buchungen aus `colAusgewaehlteBuchungen`. Wird der Stift an einer nicht angehakten Zeile gedrückt, zeigt der Dialog diese Zeile, storniert aber die angehakten.

### 51. Screen1 / conBuchungen / galAlleTischbuchungen / chkAuswahl

**Typ:** `Classic/CheckBox@2.1.0` · **Eltern:** `galAlleTischbuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3586

**Was er tut:** Kontrollkästchen vor jeder Zeile (nur im Auswahlmodus sichtbar). Haken setzen legt die Buchung (`ThisItem`) in `colAusgewaehlteBuchungen`, Haken entfernen löscht sie wieder daraus.

**Verhaltensformeln**

`OnCheck`:
```powerfx
=Collect(colAusgewaehlteBuchungen, ThisItem)
```

`OnUncheck`:
```powerfx
=Remove(colAusgewaehlteBuchungen, LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))
```

**Zustand und Aussehen**

`Text`:
```powerfx
=
```

`Visible`:
```powerfx
=varAuswahlModusAktiv
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `colAusgewaehlteBuchungen (Collect)`, `colAusgewaehlteBuchungen (Remove)`
- Gelesen: `varAuswahlModusAktiv`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine Netzwerkaufrufe; reine Collection-Operationen. `Default` macht ein lokales `LookUp` in der Collection.

**Befunde**

- **BELEGT** — A.4 nicht umgesetzt: `X: =btnVerwalten_2.X - btnVerwalten.Width - 10` (Z. 3601). `btnVerwalten` liegt in `conDashboard.galTischbuchungenHeute`, nicht in dieser Galerie. Funktioniert nur, weil beide Knöpfe 50 breit sind (Steuerelement des falschen Containers).
- **BELEGT** — `OnCheck: =Collect(colAusgewaehlteBuchungen, ThisItem)` ohne Duplikatprüfung.
- **VERMUTUNG** — Wenn `OnCheck` auch feuert, sobald `Default` (`!IsBlank(LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))`) beim Neuaufbau der Galerie auf `true` wechselt, entstünden Dubletten in der Collection. Ob Power Apps `OnCheck` bei Default-Änderungen auslöst, ist hier nicht belegt.
- **BELEGT** — Die Collection enthält Momentaufnahmen vollständiger Datensätze; `btnStornierenKlein` liest vor dem Löschen frisch nach (Entwurf A).

### 52. Screen1 / conBuchungen / conVerwaltenKlein / btnStornierenKlein

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenKlein` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4075

**Was er tut:** Knopf „Stornieren“ im kleinen Dialog der Mehrfachauswahl. Liest die eigenen künftigen Buchungen frisch aus SharePoint, bildet die Schnittmenge mit den angehakten Buchungen, löscht diese mit einem einzigen `Remove`, meldet das Ergebnis und räumt die Auswahl auf.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
ClearCollect(
    colStornoFrisch,
    Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now())
);
ClearCollect(
    colStornoZiele,
    Filter(colStornoFrisch As F, !IsBlank(LookUp(colAusgewaehlteBuchungen As A, A.ID = F.ID)))
);
If(
    CountRows(colAusgewaehlteBuchungen) = 0,
    Notify("Keine Buchungen ausgewählt.", NotificationType.Warning),
    If(
        CountRows(colStornoZiele) = 0,
        Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert.", NotificationType.Warning),
        IfError(
            Remove(Tischbuchungen, colStornoZiele),
            Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen.", NotificationType.Error),
            If(
                CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen),
                Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert.", NotificationType.Warning),
                Notify(CountRows(colStornoZiele) & " Buchungen storniert.", NotificationType.Success)
            )
        )
    )
);
Refresh(Tischbuchungen);
Clear(colStornoFrisch);
Clear(colStornoZiele);
Clear(colAusgewaehlteBuchungen);
Set(varGeklickteBuchungKlein, Blank());
Set(varZeigeVerwaltenKlein, false);
Set(varAuswahlModusAktiv, false);
Reset(tglAuswahlModus);
Set(varIsLoading, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Stornieren"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`, `varGeklickteBuchungKlein`, `varZeigeVerwaltenKlein`, `varAuswahlModusAktiv`, `colStornoFrisch (ClearCollect)`, `colStornoZiele (ClearCollect)`, `colStornoFrisch (Clear)`, `colStornoZiele (Clear)`, `colAusgewaehlteBuchungen (Clear)`, `Reset(tglAuswahlModus)`
- Gelesen: nichts
- Datenquellen: Remove auf `Tischbuchungen` (schreiben/steuern, OnSelect); Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect); Filter auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 Lesezugriff `ClearCollect(colStornoFrisch, Filter(…))`, danach `Remove(Tischbuchungen, colStornoZiele)` (1 Aufruf, falls der Konnektor den Sammelaufruf bündelt, sonst 1 je Zeile) und 1 `Refresh`. Bei 1/5/50 Buchungen: 3 bis 3+N Aufrufe (nicht gemessen).

**Befunde**

- **BELEGT** — Entwurf A.1 ist im Quellcode (`colStornoFrisch`, `colStornoZiele`, `IfError(Remove(Tischbuchungen, colStornoZiele), …)`, Z. 4086 bis 4121).
- **BELEGT** — Die Zahl in der Erfolgsmeldung ist `CountRows(colStornoZiele)`, also lokal berechnet. Was SharePoint tatsächlich gelöscht hat, wird nicht nachgelesen. Bei einem Teilausfall mitten im Sammel-`Remove` sagt die Fehlermeldung nur „Stornieren fehlgeschlagen“ ohne Zahl (Ü1).
- **BELEGT** — Der Aufräumblock (`Refresh`, `Clear`, `Set(varZeigeVerwaltenKlein, false)`, …) läuft unbedingt, auch nach einem Fehler: Der Dialog schließt und die Auswahl ist weg (Ü2). `Set(varIsLoading, false)` steht am Ende der Sequenz und wird auf jedem Pfad erreicht.
- **BELEGT** — Nur eigene künftige Buchungen werden berücksichtigt (`Person.Email = User().Email && Endzeit >= Now()`); `colStornoFrisch` lädt bis zum Datenzeilenlimit (`DefaultConnectedDataSourceMaxGetRowsCount: 1000` in `Properties.json`).
- **BELEGT** — Keine `DisplayMode`-Sperre gegen Doppelklick (Ü4); das Overlay `conLadeOverlay` deckt nach `Set(varIsLoading, true)` den Bildschirm.
- **BELEGT** — Die Buchung, die zum Öffnen des Dialogs geklickt wurde (`varGeklickteBuchungKlein`), geht nicht in die Löschmenge ein; maßgeblich ist `colAusgewaehlteBuchungen` (siehe `btnVerwalten_2`).

### 53. Screen1 / conBuchungen / conVerwaltenKlein / btnSchließenKlein

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenKlein` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4129

**Was er tut:** Knopf „Schließen“ im kleinen Dialog der Mehrfachauswahl. Schließt den Dialog, leert die Auswahl und die beiden Hilfs-Collections und schaltet den Auswahlmodus aus.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeVerwaltenKlein, false);
Set(varGeklickteBuchungKlein, Blank());
Clear(colAusgewaehlteBuchungen);
Clear(colStornoFrisch);
Clear(colStornoZiele);
Set(varAuswahlModusAktiv, false);
Reset(tglAuswahlModus)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, 30%)
```

`PressedFill`:
```powerfx
=Color.Black
```

`Text`:
```powerfx
="Schließen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeVerwaltenKlein`, `varGeklickteBuchungKlein`, `varAuswahlModusAktiv`, `colAusgewaehlteBuchungen (Clear)`, `colStornoFrisch (Clear)`, `colStornoZiele (Clear)`, `Reset(tglAuswahlModus)`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — A.2 ist umgesetzt: `Clear(colStornoFrisch); Clear(colStornoZiele);` stehen in Z. 4144 und 4145.
- **BELEGT** — Schaltet den Auswahlmodus über `Set(varAuswahlModusAktiv, false); Reset(tglAuswahlModus)` aus. Ob `Reset` den `OnChange` des Schalters auslöst (der dann nochmals `Clear` und `varGalleryNeuAufbauen + 1` ausführt), ist hier nicht belegt (UNSICHER).

### 54. Screen1 / conBuchungen / tglAuswahlModus

**Typ:** `Classic/Toggle@2.1.0` · **Eltern:** `conBuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4164

**Was er tut:** Schalter „Auswahlmodus“ oben rechts in der Buchungsliste. An: Haken und „Alle auswählen“ erscheinen, der Stift öffnet den Sammel-Dialog. Aus: Auswahl und kleiner Dialog werden geleert. Der Schalter ist gesperrt, solange höchstens eine Buchung vorhanden ist.

**Verhaltensformel**

`OnChange`:
```powerfx
=Set(varAuswahlModusAktiv, tglAuswahlModus.Value);
If(
  !tglAuswahlModus.Value,
  Clear(colAusgewaehlteBuchungen);
  Set(varZeigeVerwaltenKlein, false);
  Set(varGeklickteBuchungKlein, Blank())
);
Set(varGalleryNeuAufbauen, varGalleryNeuAufbauen + 1);
If(
  tglAuswahlModus.Value,
  Set(varZeigeVerwaltenTab, false)
)
```

**Zustand und Aussehen**

`DisplayMode`:
```powerfx
=If(galAlleTischbuchungen.AllItemsCount <= 1, DisplayMode.Disabled, DisplayMode.Edit)
```

Nicht gesetzt: `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAuswahlModusAktiv`, `varZeigeVerwaltenKlein`, `varGeklickteBuchungKlein`, `varGalleryNeuAufbauen`, `varZeigeVerwaltenTab`, `colAusgewaehlteBuchungen (Clear)`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Auslöser: Neuaufbau von `galAlleTischbuchungen` über `varGalleryNeuAufbauen` (1 Abfrage `Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now())`).

**Befunde**

- **BELEGT** — Zwei Variablen für denselben Zweck: `varAuswahlModusAktiv` (wird gelesen) und `varMehrfachAuswahlModus` (wird nur in `App.OnStart` und `btnVerlängern_1` geschrieben, nie gelesen).
- **BELEGT** — `varGalleryNeuAufbauen` wird hochgezählt, damit `galAlleTischbuchungen.Items` (über `With({erzwingeNeuaufbau: varGalleryNeuAufbauen}, …)`) neu rechnet. Die Variable steht nur in dieser Formel.
- **BELEGT** — Einschalten setzt `varZeigeVerwaltenTab` auf `false`, schließt also einen offenen Einzel-Dialog.

### 55. Screen1 / conBuchungen / chkAlleAuswählen

**Typ:** `Classic/CheckBox@2.1.0` · **Eltern:** `conBuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4186

**Was er tut:** Kontrollkästchen „Alle auswählen“ (nur im Auswahlmodus). Anhaken füllt `colAusgewaehlteBuchungen` mit allen Zeilen der Galerie, Abhaken leert die Collection. `Default` steht auf „alle ausgewählt“, wenn die Zahl der Auswahl der Zahl der Galerie-Zeilen entspricht.

**Verhaltensformeln**

`OnCheck`:
```powerfx
=ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)
```

`OnUncheck`:
```powerfx
=Clear(colAusgewaehlteBuchungen)
```

**Zustand und Aussehen**

`Text`:
```powerfx
=
```

`Visible`:
```powerfx
=varAuswahlModusAktiv
```

Nicht gesetzt: `DisplayMode`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `colAusgewaehlteBuchungen (ClearCollect)`, `colAusgewaehlteBuchungen (Clear)`
- Gelesen: `varAuswahlModusAktiv`
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine Netzwerkaufrufe (liest `galAlleTischbuchungen.AllItems`, die schon geladene Menge).

**Befunde**

- **BELEGT** — A.3 nicht umgesetzt: `OnCheck: =ClearCollect(colAusgewaehlteBuchungen, galAlleTischbuchungen.AllItems)`. `AllItems` ist die geladene Menge der Galerie.
- **VERMUTUNG** — Wenn die Galerie weniger Zeilen geladen hat, als es künftige eigene Buchungen gibt, markiert „Alle auswählen“ nur eine Teilmenge. Ladegröße der Galerie: im Quellcode nicht belegt (UNSICHER).
- **VERMUTUNG** — `Default` hängt von der Auswahl ab. Feuert `OnUncheck`, wenn `Default` auf `false` wechselt (Abwählen einer einzelnen Zeile bei vollständiger Auswahl), würde `Clear(colAusgewaehlteBuchungen)` die gesamte Auswahl löschen. Ob das auftritt, ist hier nicht belegt; mit Test klären.

### 56. Screen1 / conBuchungen / Icon1

**Typ:** `Classic/Icon@2.5.0` · **Eltern:** `conBuchungen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 4202

**Was er tut:** Aktualisieren-Symbol oben links in der Buchungsliste. Gleiche Formel wie am Logo und im Dashboard.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
Refresh(Tischbuchungen);
Set(varIsLoading, false);
Notify("Aktualisiert.", NotificationType.Success)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(32, 54, 71, 1)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`
- Gelesen: nichts
- Datenquellen: Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** 1 Aufruf (`Refresh(Tischbuchungen`) plus Folgeabfragen der Galerie).

**Befunde**

- **BELEGT** — Wortgleiche Formel wie `Image6`, `btnHitArea_1`, `Icon1_1`.
- **VERMUTUNG** — Kein `IfError`; „Aktualisiert.“ erscheint auch, wenn `Refresh` fehlschlägt.

## Verwalten-Dialoge

### 57. Screen1 / conVerwaltenDialog / btnStornieren

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3226

**Was er tut:** Knopf „Stornieren“ im Verwalten-Dialog des Grundrisses/Dashboards (`conVerwaltenDialog`). Löscht die in `varSelectedBuchung` gemerkte Buchung und schließt den Dialog.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Remove(Tischbuchungen, varSelectedBuchung); Set(varZeigeVerwalten, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Stornieren"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeVerwalten`
- Gelesen: `varSelectedBuchung`
- Datenquellen: Remove auf `Tischbuchungen` (schreiben/steuern, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 `Remove`-Aufruf.

**Befunde**

- **BELEGT** — `OnSelect: =Remove(Tischbuchungen, varSelectedBuchung); Set(varZeigeVerwalten, false)` (Z. 3237): kein `IfError`, kein `Refresh`, keine Meldung, keine Rückfrage, kein `varIsLoading`.
- **BELEGT** — Löscht über die Variable (Momentaufnahme), nicht über frisch gelesenen Datensatz; Prüfung auf bereits gelöschte Buchung fehlt (anders als in `btnStornierenKlein`).
- **VERMUTUNG** — Wurde die Buchung inzwischen von jemand anderem gelöscht oder geändert, erzeugt `Remove` einen Fehler, der nicht abgefangen wird; ob der Nutzer dann eine rohe Fehlermeldung sieht, ist nicht belegt.

### 58. Screen1 / conVerwaltenDialog / btnVerlängern

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3245

**Was er tut:** Knopf „Verlängern“ im Verwalten-Dialog des Grundrisses/Dashboards. Verlängert die in `varSelectedBuchung` gemerkte Buchung um die gewählte Dauer (+1/+2/+3 Std) und schließt den Dialog.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  If(
    IsBlank(varAusgewaehltePlusDauer),
    Notify("Bitte eine Dauer auswählen.", NotificationType.Warning),
    Set(varSelectedBuchung, Patch(Tischbuchungen, aktuelleBuchung, {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit, varAusgewaehltePlusDauer, TimeUnit.Minutes)
    }));
    Set(varZeigeVerwalten, false);
    Set(varAusgewaehltePlusDauer, Blank())
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Verlängern"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varSelectedBuchung`, `varZeigeVerwalten`, `varAusgewaehltePlusDauer`
- Gelesen: nichts
- Datenquellen: Patch auf `Tischbuchungen` (schreiben/steuern, OnSelect); LookUp auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 `LookUp` und 1 `Patch` (2 Aufrufe).

**Befunde**

- **BELEGT** — K3 nicht umgesetzt: Die Formel ist der Stand aus dem Briefing (Abschnitt 5.3): `With({aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID)}, If(IsBlank(varAusgewaehltePlusDauer), Notify(…), Set(varSelectedBuchung, Patch(…)); Set(varZeigeVerwalten, false); Set(varAusgewaehltePlusDauer, Blank())))`.
- **BELEGT** — Keine Kollisionsprüfung beim Speichern; nur die Plus-Knöpfe prüfen beim Anzeigen mit dem Stand beim Öffnen. Keine 22:00-Kappung, keine Prüfung, ob die Buchung noch existiert (`aktuelleBuchung` kann leer sein), kein `IfError`, kein `varIsLoading`, kein `DisplayMode` (K5 nicht umgesetzt).
- **BELEGT** — Der Dialog schließt unbedingt; kein `Refresh`.
- **BELEGT** — `IsBlank(varAusgewaehltePlusDauer)` lässt den Wert `0` durch (siehe `ddStockwerk`).

### 59. Screen1 / conVerwaltenDialog / btnSchließen4

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3276

**Was er tut:** Knopf „Schließen“ im Verwalten-Dialog des Grundrisses/Dashboards. Schließt den Dialog.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeVerwalten, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, 30%)
```

`PressedFill`:
```powerfx
=Color.Black
```

`Text`:
```powerfx
="Schließen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeVerwalten`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Set(varZeigeVerwalten, false)`; `varAusgewaehltePlusDauer` bleibt gesetzt (wird erst von `btnVerwalten` beim nächsten Öffnen zurückgesetzt).

### 60. Screen1 / conVerwaltenDialog / btnPlus1Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3295

**Was er tut:** Wählbare Dauer „+1 Std“ im Verwalten-Dialog. Ein Klick merkt die Dauer in `varAusgewaehltePlusDauer` (zweiter Klick nimmt sie zurück); der Knopf wird grün, wenn gewählt, rot und gesperrt, wenn das neue Stück der Buchung am selben Tisch mit einer anderen Buchung kollidiert.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 60, Blank(), 60))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 60,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="+1Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` (aktuelle Buchung) und 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen, also 4 Abfragen je Knopf, 12 für die drei Plus-Knöpfe. Der Klick selbst macht keine Abfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl 60 steht konsistent in `DisplayMode`, `Fill` (Vergleich `varAusgewaehltePlusDauer = 60`, `DateAdd`) und `OnSelect`; kein Kopierfehler bei der Offset-Zahl.
- **BELEGT** — Die Kollisionsprüfung prüft nur das neue Stück (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`), kein `ID <>` nötig.
- **BELEGT** — Die Sperre gilt nur für die Anzeige; `btnVerlängern`/`btnVerlängern_1` prüfen beim Speichern nicht noch einmal.

### 61. Screen1 / conVerwaltenDialog / btnPlus2Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3344

**Was er tut:** Wählbare Dauer „+2 Std“ im Verwalten-Dialog. Ein Klick merkt die Dauer in `varAusgewaehltePlusDauer` (zweiter Klick nimmt sie zurück); der Knopf wird grün, wenn gewählt, rot und gesperrt, wenn das neue Stück der Buchung am selben Tisch mit einer anderen Buchung kollidiert.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 120, Blank(), 120))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 120,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="+2Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` (aktuelle Buchung) und 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen, also 4 Abfragen je Knopf, 12 für die drei Plus-Knöpfe. Der Klick selbst macht keine Abfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl 120 steht konsistent in `DisplayMode`, `Fill` (Vergleich `varAusgewaehltePlusDauer = 120`, `DateAdd`) und `OnSelect`; kein Kopierfehler bei der Offset-Zahl.
- **BELEGT** — Die Kollisionsprüfung prüft nur das neue Stück (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`), kein `ID <>` nötig.
- **BELEGT** — Die Sperre gilt nur für die Anzeige; `btnVerlängern`/`btnVerlängern_1` prüfen beim Speichern nicht noch einmal.

### 62. Screen1 / conVerwaltenDialog / btnPlus3Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3393

**Was er tut:** Wählbare Dauer „+3 Std“ im Verwalten-Dialog. Ein Klick merkt die Dauer in `varAusgewaehltePlusDauer` (zweiter Klick nimmt sie zurück); der Knopf wird grün, wenn gewählt, rot und gesperrt, wenn das neue Stück der Buchung am selben Tisch mit einer anderen Buchung kollidiert.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 180, Blank(), 180))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes),
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 180,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="+3Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` (aktuelle Buchung) und 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen, also 4 Abfragen je Knopf, 12 für die drei Plus-Knöpfe. Der Klick selbst macht keine Abfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl 180 steht konsistent in `DisplayMode`, `Fill` (Vergleich `varAusgewaehltePlusDauer = 180`, `DateAdd`) und `OnSelect`; kein Kopierfehler bei der Offset-Zahl.
- **BELEGT** — Die Kollisionsprüfung prüft nur das neue Stück (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`), kein `ID <>` nötig.
- **BELEGT** — Die Sperre gilt nur für die Anzeige; `btnVerlängern`/`btnVerlängern_1` prüfen beim Speichern nicht noch einmal.

### 63. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnStornieren_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3662

**Was er tut:** Knopf „Stornieren“ im Verwalten-Dialog des Buchungen-Tabs (`conVerwaltenDialog_1`). Löscht die in `varSelectedBuchungTab` gemerkte Buchung, aktualisiert die Liste und meldet „Buchung storniert.“

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varIsLoading, true);
If(
  IsBlank(varSelectedBuchungTab),
  Notify("Keine Buchung ausgewählt.", NotificationType.Warning),
  Remove(Tischbuchungen, varSelectedBuchungTab);
  Refresh(Tischbuchungen);
  Notify("Buchung storniert.", NotificationType.Success)
);
Set(varZeigeVerwaltenTab, false);
Set(varIsLoading, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Stornieren"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varIsLoading`, `varZeigeVerwaltenTab`
- Gelesen: `varSelectedBuchungTab`
- Datenquellen: Remove auf `Tischbuchungen` (schreiben/steuern, OnSelect); Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 `Remove` und 1 `Refresh` (2 Aufrufe) plus Folgeabfragen der Galerie.

**Befunde**

- **BELEGT** — Kein `IfError`: „Buchung storniert.“ (Z. 3680) steht unbedingt nach `Remove` und `Refresh`. Bei einem Fehler im `Remove` kann die Erfolgsmeldung trotzdem erscheinen (Laufzeitverhalten: VERMUTUNG).
- **BELEGT** — `Set(varIsLoading, false)` steht außerhalb des `If` am Ende der Sequenz und wird auf jedem Pfad erreicht.
- **BELEGT** — Löscht mit der Variablen `varSelectedBuchungTab` (Momentaufnahme); keine frische Prüfung. Die Plus-/Minus-Knöpfe im selben Dialog lesen dagegen `varSelectedBuchung` (Befund B0).

### 64. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnVerlängern_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3691

**Was er tut:** Knopf „Speichern“ (Name `btnVerlängern_1`) im Verwalten-Dialog des Buchungen-Tabs. Ändert die Endzeit der in `varSelectedBuchungTab` gemerkten Buchung um die gewählte Dauer (+1/+2/+3 oder -1/-2/-3 Std), aktualisiert die Liste und schließt den Dialog. Es ändert immer nur eine Buchung.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchungTab.ID) },
  If(
    IsBlank(varAusgewaehltePlusDauer),
    Notify("Bitte eine Dauer auswählen.", NotificationType.Warning),
    Set(varSelectedBuchungTab, Patch(Tischbuchungen, aktuelleBuchung, {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit, varAusgewaehltePlusDauer, TimeUnit.Minutes)
    }));
    Refresh(Tischbuchungen);
    Set(varZeigeVerwaltenTab, false);
    Set(varAusgewaehltePlusDauer, Blank());
    Clear(colAusgewaehlteBuchungen);
    Set(varMehrfachAuswahlModus, false)
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -20%)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Speichern"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varSelectedBuchungTab`, `varZeigeVerwaltenTab`, `varAusgewaehltePlusDauer`, `varMehrfachAuswahlModus`, `colAusgewaehlteBuchungen (Clear)`
- Gelesen: nichts
- Datenquellen: Patch auf `Tischbuchungen` (schreiben/steuern, OnSelect); Refresh auf `Tischbuchungen` (schreiben/steuern, OnSelect); LookUp auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 `LookUp`, 1 `Patch`, 1 `Refresh` (3 Aufrufe) plus Folgeabfragen.

**Befunde**

- **BELEGT** — K2 nicht umgesetzt: kein `IfError`, keine Prüfung auf bereits gelöschte Buchung, keine 22:00-Kappung, keine Kollisionsprüfung beim Speichern (Z. 3703 bis 3716).
- **BELEGT** — Befund B0: Der Dialog speichert `varSelectedBuchungTab`, aber alle zwölf Dauer-Knopf-Properties lesen `varSelectedBuchung` (Z. 3753 bis 3996). Zusammen: stille Doppelbuchung bei Verlängerung möglich; bei Verkürzung kann `Endzeit <= Startzeit` entstehen.
- **BELEGT** — `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus, false)` am Ende (Z. 3714 und 3715): `varMehrfachAuswahlModus` wird nirgends gelesen. Das `Clear` ist wirkungslos, solange der Auswahlmodus aus ist (der Dialog wird nur dort geöffnet).
- **BELEGT** — Kein `varIsLoading` und kein `DisplayMode` (K5 nicht umgesetzt): Doppelklick kann zweimal `Patch` auslösen (zweimal +1 Std).
- **BELEGT** — Der Dialog schließt unbedingt (Ü2).

### 65. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnSchließen4_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3725

**Was er tut:** Knopf „Schließen“ im Verwalten-Dialog des Buchungen-Tabs. Schließt den Dialog.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeVerwaltenTab, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, 30%)
```

`PressedFill`:
```powerfx
=Color.Black
```

`Text`:
```powerfx
="Schließen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeVerwaltenTab`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Set(varZeigeVerwaltenTab, false)`; `varAusgewaehltePlusDauer` bleibt gesetzt.

### 66. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnPlus1Std_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3744

**Was er tut:** Wählbare Dauer „+1 Std“ im Verwalten-Dialog. Ein Klick merkt die Dauer in `varAusgewaehltePlusDauer` (zweiter Klick nimmt sie zurück); der Knopf wird grün, wenn gewählt, rot und gesperrt, wenn das neue Stück der Buchung am selben Tisch mit einer anderen Buchung kollidiert.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 60, Blank(), 60))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 60,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="+1Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` (aktuelle Buchung) und 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen, also 4 Abfragen je Knopf, 12 für die drei Plus-Knöpfe. Der Klick selbst macht keine Abfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl 60 steht konsistent in `DisplayMode`, `Fill` (Vergleich `varAusgewaehltePlusDauer = 60`, `DateAdd`) und `OnSelect`; kein Kopierfehler bei der Offset-Zahl.
- **BELEGT** — Die Kollisionsprüfung prüft nur das neue Stück (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`), kein `ID <>` nötig.
- **BELEGT** — Die Sperre gilt nur für die Anzeige; `btnVerlängern`/`btnVerlängern_1` prüfen beim Speichern nicht noch einmal.
- **BELEGT** — Befund B0: `DisplayMode` und `Fill` lesen `varSelectedBuchung.ID` (Z. 3753), also die zuletzt im Grundriss angeklickte Buchung. Der Dialog gehört zu `varSelectedBuchungTab` (gesetzt in `btnVerwalten_2`, gespeichert in `btnVerlängern_1`). Der Knopf kann grün sein, obwohl die Verlängerung der angezeigten Buchung kollidiert: stille Doppelbuchungsmöglichkeit. K1 ist nicht umgesetzt.

### 67. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnPlus2Std_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3793

**Was er tut:** Wählbare Dauer „+2 Std“ im Verwalten-Dialog. Ein Klick merkt die Dauer in `varAusgewaehltePlusDauer` (zweiter Klick nimmt sie zurück); der Knopf wird grün, wenn gewählt, rot und gesperrt, wenn das neue Stück der Buchung am selben Tisch mit einer anderen Buchung kollidiert.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 120, Blank(), 120))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    },
    If(
      varAusgewaehltePlusDauer = 120,
      ColorValue("#00A96B"),
      If(
        direktBesetzt,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="+2Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` (aktuelle Buchung) und 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen, also 4 Abfragen je Knopf, 12 für die drei Plus-Knöpfe. Der Klick selbst macht keine Abfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl 120 steht konsistent in `DisplayMode`, `Fill` (Vergleich `varAusgewaehltePlusDauer = 120`, `DateAdd`) und `OnSelect`; kein Kopierfehler bei der Offset-Zahl.
- **BELEGT** — Die Kollisionsprüfung prüft nur das neue Stück (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`), kein `ID <>` nötig.
- **BELEGT** — Die Sperre gilt nur für die Anzeige; `btnVerlängern`/`btnVerlängern_1` prüfen beim Speichern nicht noch einmal.
- **BELEGT** — Befund B0: `DisplayMode` und `Fill` lesen `varSelectedBuchung.ID` (Z. 3802), also die zuletzt im Grundriss angeklickte Buchung. Der Dialog gehört zu `varSelectedBuchungTab` (gesetzt in `btnVerwalten_2`, gespeichert in `btnVerlängern_1`). Der Knopf kann grün sein, obwohl die Verlängerung der angezeigten Buchung kollidiert: stille Doppelbuchungsmöglichkeit. K1 ist nicht umgesetzt.

### 68. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnPlus3Std_1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3842

**Was er tut:** Wählbare Dauer „+3 Std“ im Verwalten-Dialog. Ein Klick merkt die Dauer in `varAusgewaehltePlusDauer` (zweiter Klick nimmt sie zurück); der Knopf wird grün, wenn gewählt, rot und gesperrt, wenn das neue Stück der Buchung am selben Tisch mit einer anderen Buchung kollidiert.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = 180, Blank(), 180))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes), tischWert: aktuelleBuchung.Tisch.Value, endeAlt: aktuelleBuchung.Endzeit },
    If(
      CountRows(Filter(Tischbuchungen, Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With({ aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) }, With({ tischWert: aktuelleBuchung.Tisch.Value, endeAlt: aktuelleBuchung.Endzeit, neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) }, With({ direktBesetzt: CountRows(Filter(Tischbuchungen, Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0 }, If(varAusgewaehltePlusDauer = 180, ColorValue("#00A96B"), If(direktBesetzt, ColorFade(ColorValue("#EB3951"), 70%), ColorFade(ColorValue("#00A96B"), 70%))))))
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="+3Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); Filter auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill); Filter auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` (aktuelle Buchung) und 1 `CountRows(Filter(Tischbuchungen, …))` bei jedem Neuberechnen, also 4 Abfragen je Knopf, 12 für die drei Plus-Knöpfe. Der Klick selbst macht keine Abfrage.

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl 180 steht konsistent in `DisplayMode`, `Fill` (Vergleich `varAusgewaehltePlusDauer = 180`, `DateAdd`) und `OnSelect`; kein Kopierfehler bei der Offset-Zahl.
- **BELEGT** — Die Kollisionsprüfung prüft nur das neue Stück (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`), kein `ID <>` nötig.
- **BELEGT** — Die Sperre gilt nur für die Anzeige; `btnVerlängern`/`btnVerlängern_1` prüfen beim Speichern nicht noch einmal.
- **BELEGT** — Befund B0: `DisplayMode` und `Fill` lesen `varSelectedBuchung.ID` (Z. 3851), also die zuletzt im Grundriss angeklickte Buchung. Der Dialog gehört zu `varSelectedBuchungTab` (gesetzt in `btnVerwalten_2`, gespeichert in `btnVerlängern_1`). Der Knopf kann grün sein, obwohl die Verlängerung der angezeigten Buchung kollidiert: stille Doppelbuchungsmöglichkeit. K1 ist nicht umgesetzt.

### 69. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnMinus1Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3875

**Was er tut:** Wählbare Verkürzung „-1 Std“ im Verwalten-Dialog des Buchungen-Tabs. Ein Klick merkt `-60` in `varAusgewaehltePlusDauer`; der Knopf ist gesperrt, wenn die neue Endzeit nicht nach dem Start liegt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = -60, Blank(), -60))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -60, TimeUnit.Minutes) },
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -60, TimeUnit.Minutes),
      zuKurz: DateAdd(aktuelleBuchung.Endzeit, -60, TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    },
    If(
      varAusgewaehltePlusDauer = -60,
      ColorValue("#00A96B"),
      If(
        zuKurz,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="-1Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` bei jedem Neuberechnen (2 Abfragen je Knopf).

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl -60 steht konsistent in `DisplayMode`, `Fill` (`varAusgewaehltePlusDauer = -60`) und `OnSelect`.
- **BELEGT** — Befund B0: `DisplayMode` und `Fill` lesen `varSelectedBuchung.ID` (Z. 3884) statt `varSelectedBuchungTab`. Die Sperre „zu kurz“ gilt für eine andere Buchung als die, die gespeichert wird; `Endzeit <= Startzeit` bei der angezeigten Buchung ist möglich.
- **BELEGT** — Keine `Now()`-Grenze: Auch bereits laufende Buchungen lassen sich bis zum Start verkürzen (fachliche Entscheidung, siehe `07_OFFENE_FRAGEN.md`).

### 70. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnMinus2Std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3925

**Was er tut:** Wählbare Verkürzung „-2 Std“ im Verwalten-Dialog des Buchungen-Tabs. Ein Klick merkt `-120` in `varAusgewaehltePlusDauer`; der Knopf ist gesperrt, wenn die neue Endzeit nicht nach dem Start liegt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = -120, Blank(), -120))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -120, TimeUnit.Minutes) },
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -120, TimeUnit.Minutes),
      zuKurz: DateAdd(aktuelleBuchung.Endzeit, -120, TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    },
    If(
      varAusgewaehltePlusDauer = -120,
      ColorValue("#00A96B"),
      If(
        zuKurz,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="-2std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` bei jedem Neuberechnen (2 Abfragen je Knopf).

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl -120 steht konsistent in `DisplayMode`, `Fill` (`varAusgewaehltePlusDauer = -120`) und `OnSelect`.
- **BELEGT** — Befund B0: `DisplayMode` und `Fill` lesen `varSelectedBuchung.ID` (Z. 3934) statt `varSelectedBuchungTab`. Die Sperre „zu kurz“ gilt für eine andere Buchung als die, die gespeichert wird; `Endzeit <= Startzeit` bei der angezeigten Buchung ist möglich.
- **BELEGT** — Keine `Now()`-Grenze: Auch bereits laufende Buchungen lassen sich bis zum Start verkürzen (fachliche Entscheidung, siehe `07_OFFENE_FRAGEN.md`).

### 71. Screen1 / conBuchungen / conVerwaltenDialog_1 / btnMinus3std

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conVerwaltenDialog_1` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3975

**Was er tut:** Wählbare Verkürzung „-3 Std“ im Verwalten-Dialog des Buchungen-Tabs. Ein Klick merkt `-180` in `varAusgewaehltePlusDauer`; der Knopf ist gesperrt, wenn die neue Endzeit nicht nach dem Start liegt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varAusgewaehltePlusDauer, If(varAusgewaehltePlusDauer = -180, Blank(), -180))
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 70%)
```

`DisplayMode`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -180, TimeUnit.Minutes) },
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit,
      DisplayMode.Disabled,
      DisplayMode.Edit
    )
  )
)
```

`Fill`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit, -180, TimeUnit.Minutes),
      zuKurz: DateAdd(aktuelleBuchung.Endzeit, -180, TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    },
    If(
      varAusgewaehltePlusDauer = -180,
      ColorValue("#00A96B"),
      If(
        zuKurz,
        ColorFade(ColorValue("#EB3951"), 70%),
        ColorFade(ColorValue("#00A96B"), 70%)
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="-3Std"
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewaehltePlusDauer`
- Gelesen: `varSelectedBuchung`
- Datenquellen: LookUp auf `Tischbuchungen` (lesen, DisplayMode); LookUp auf `Tischbuchungen` (lesen, Fill)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: `DisplayMode` und `Fill` je 1 `LookUp` bei jedem Neuberechnen (2 Abfragen je Knopf).

**Befunde**

- **BELEGT** — Kopierprüfung: Die Zahl -180 steht konsistent in `DisplayMode`, `Fill` (`varAusgewaehltePlusDauer = -180`) und `OnSelect`.
- **BELEGT** — Befund B0: `DisplayMode` und `Fill` lesen `varSelectedBuchung.ID` (Z. 3984) statt `varSelectedBuchungTab`. Die Sperre „zu kurz“ gilt für eine andere Buchung als die, die gespeichert wird; `Endzeit <= Startzeit` bei der angezeigten Buchung ist möglich.
- **BELEGT** — Keine `Now()`-Grenze: Auch bereits laufende Buchungen lassen sich bis zum Start verkürzen (fachliche Entscheidung, siehe `07_OFFENE_FRAGEN.md`).

## Check-in

### 72. Screen1 / conCheckinDialog / btnEinchecken

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conCheckinDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3052

**Was er tut:** Knopf „Einchecken“/„Auschecken“ im Check-in-Dialog. Liest die Buchung frisch, kehrt ihren `CheckedIn`-Wert um und schließt den Dialog.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { aktuelleBuchung: LookUp(Tischbuchungen, ID = varSelectedBuchung.ID) },
  Set(varSelectedBuchung, Patch(Tischbuchungen, aktuelleBuchung, {CheckedIn: !aktuelleBuchung.CheckedIn}))
);
Set(varZeigeCheckin, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=Color.White
```

`Fill`:
```powerfx
=If(varSelectedBuchung.CheckedIn, ColorValue("#EB3951"), ColorValue("#00a96b"))
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -30%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
=If(varSelectedBuchung.CheckedIn, "Auschecken", "Einchecken")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varSelectedBuchung`, `varZeigeCheckin`
- Gelesen: nichts
- Datenquellen: Patch auf `Tischbuchungen` (schreiben/steuern, OnSelect); LookUp auf `Tischbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 `LookUp` und 1 `Patch` (2 Aufrufe).

**Befunde**

- **BELEGT** — Kein `IfError`; der Dialog schließt unbedingt (`Set(varZeigeCheckin, false)` am Ende, Z. 3068).
- **BELEGT** — Kein Zeitfenster: Ein- und Auschecken ist jederzeit möglich, auch für künftige Tage (siehe `btnEincheckenHeute`).
- **BELEGT** — `aktuelleBuchung` kann leer sein (Buchung inzwischen gelöscht); `Patch(Tischbuchungen, aktuelleBuchung, …)` hat dafür keine Prüfung.
- **BELEGT** — Die Spalte wird als `CheckedIn` angesprochen (Anzeigename); der interne Name ist `Checkedin` (`DataSources.json`). Das funktioniert, weil `usedisplaynamemetadata` aktiv ist.
- **BELEGT** — `Set(varSelectedBuchung, Patch(…))` überschreibt die Variable mit dem Rückgabewert von `Patch`.

### 73. Screen1 / conCheckinDialog / btnSchließen2

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conCheckinDialog` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3077

**Was er tut:** Knopf „Schließen“ im Check-in-Dialog. Schließt den Dialog.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeCheckin, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, 30%)
```

`PressedFill`:
```powerfx
=Color.Black
```

`Text`:
```powerfx
="Schließen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeCheckin`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Set(varZeigeCheckin, false)`; keine weiteren Seiteneffekte.

## Details-Popup

### 74. Screen1 / conDetailsPopup / btnSchließen3

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conDetailsPopup` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 3169

**Was er tut:** Kleines „x“ oben rechts im Details-Popup einer belegten Kachel. Schließt das Popup.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeDetails, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, 30%)
```

`PressedFill`:
```powerfx
=Color.Black
```

`Text`:
```powerfx
="x"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeDetails`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Das Popup zeigt `varSelectedBuchung.Person.DisplayName` (`lblPerson`, Z. 3155) und Zeiten fremder Buchungen: jeder Nutzer sieht, wer einen Tisch gebucht hat (Datenschutzfrage in `07_OFFENE_FRAGEN.md`).

## Toter Raumcode

### 75. Screen1 / conDashboard / galRaumbuchungenHeute / Rectangle4_1

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 518

**Was er tut:** Klick auf die Zeilenfläche wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=ColorValue("#F0F0F0")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 76. Screen1 / conDashboard / galRaumbuchungenHeute / Image1_2

**Typ:** `Image@2.2.3` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 528

**Was er tut:** Klick auf das Meeting-Bild wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 77. Screen1 / conDashboard / galRaumbuchungenHeute / Image3_1

**Typ:** `Image@2.2.3` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 538

**Was er tut:** Klick auf das Bearbeiten-Symbol wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 78. Screen1 / conDashboard / galRaumbuchungenHeute / Rectangle3_1

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 548

**Was er tut:** Klick auf den Auswahlbalken wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=RGBA(100, 118, 132, 1)
```

`Visible`:
```powerfx
=ThisItem.IsSelected
```

Nicht gesetzt: `DisplayMode`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 79. Screen1 / conDashboard / galRaumbuchungenHeute / lblTischHeute_1

**Typ:** `Label@2.5.1` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 557

**Was er tut:** Klick auf den Raumnamen wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Text`:
```powerfx
="Raum " & ThisItem.Raum.Value
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 80. Screen1 / conDashboard / galRaumbuchungenHeute / lblZeitHeute_1

**Typ:** `Label@2.5.1` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 568

**Was er tut:** Klick auf die Zeitangabe wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Text`:
```powerfx
=Text(ThisItem.Startzeit, "hh:mm") & " – " & Text(ThisItem.Endzeit, "hh:mm")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 81. Screen1 / conDashboard / galRaumbuchungenHeute / btnInfoRaum

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galRaumbuchungenHeute` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 579

**Was er tut:** Klick auf die Zeilenfläche (transparenter Knopf) wählt die Zeile in „My meetings“ aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Transparent
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.04)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
=
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; es gibt kein Raum-Info-Fenster, das er öffnen würde. `varZeigeRaumInfo` wird nur in `App.OnStart` gesetzt und nirgends gelesen.

### 82. Screen1 / conDashboard / btnRaumHinzufügen

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conDashboard` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 687

**Was er tut:** Knopf „Raum Buchen“ im Dashboard. Würde das Raum-Panel öffnen, ist aber dauerhaft unsichtbar.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeRaumBuchungForm, true)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#D0D0D0")
```

`HoverFill`:
```powerfx
=RGBA(0, 0, 0, 0.2)
```

`PressedFill`:
```powerfx
=
```

`Text`:
```powerfx
="Raum Buchen"
```

`Visible`:
```powerfx
=false
```

Nicht gesetzt: `DisplayMode`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeRaumBuchungForm`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — `Visible: =false` (Z. 704). Damit ist der ganze Raumbereich unerreichbar.
- **BELEGT** — `OnSelect: =Set(varZeigeRaumBuchungForm, true)`.

### 83. Screen1 / conRaumBuchungenPanel / btnAbbrechenRaumPanel

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conRaumBuchungenPanel` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1459

**Was er tut:** Zurück-Pfeil „<“ im Raum-Panel. Schließt das Panel.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeRaumBuchungForm, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=Color.Black
```

`Fill`:
```powerfx
=RGBA(241, 241, 241, 1)
```

`HoverFill`:
```powerfx
=ColorFade(Self.Fill, -15%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="<"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeRaumBuchungForm`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Set(varZeigeRaumBuchungForm, false)`.

### 84. Screen1 / conRaumBuchungenPanel / galRäume / Rectangle7

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1532

**Was er tut:** Klick auf die Zeilenfläche wählt die Zeile in der Raumliste `galRäume` aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=ColorValue("#F0F0F0")
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 85. Screen1 / conRaumBuchungenPanel / galRäume / Image1

**Typ:** `Image@2.2.3` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1552

**Was er tut:** Klick auf das Raumbild wählt die Zeile in der Raumliste `galRäume` aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

Keine dieser Properties ist gesetzt (DisplayMode, Visible, Fill, DisabledFill, HoverFill, PressedFill, Color, Text); es gelten die Standardwerte des Steuerelementtyps.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 86. Screen1 / conRaumBuchungenPanel / galRäume / Title1

**Typ:** `Label@2.5.1` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1566

**Was er tut:** Klick auf den Raumnamen wählt die Zeile in der Raumliste `galRäume` aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(50, 49, 48, 1)
```

`Text`:
```powerfx
=ThisItem.Titel
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 87. Screen1 / conRaumBuchungenPanel / galRäume / Subtitle1

**Typ:** `Label@2.5.1` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1585

**Was er tut:** Klick auf die Adresszeile wählt die Zeile in der Raumliste `galRäume` aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Text`:
```powerfx
="Matthäus-Merian-Strasse 6 / Lohfelden  MMS Obergeschoss"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 88. Screen1 / conRaumBuchungenPanel / galRäume / NextArrow1

**Typ:** `Classic/Icon@2.5.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1811

**Was er tut:** Klick auf den Pfeil rechts wählt die Zeile in der Raumliste `galRäume` aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(166, 166, 166, 1)
```

Nicht gesetzt: `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 89. Screen1 / conRaumBuchungenPanel / galRäume / Rectangle2

**Typ:** `Rectangle@2.3.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1828

**Was er tut:** Klick auf den Auswahlbalken wählt die Zeile in der Raumliste `galRäume` aus. Nicht erreichbar, weil die Galerie unsichtbar ist.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Select(Parent)
```

**Zustand und Aussehen**

`Fill`:
```powerfx
=ColorValue("#171496")
```

`Visible`:
```powerfx
=ThisItem.IsSelected
```

Nicht gesetzt: `DisplayMode`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text`.

**Variablen, Collections, Datenquellen**

- Geschrieben: nichts
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Select(Parent)`; die Galerie hat kein eigenes `OnSelect`.

### 90. Screen1 / conRaumBuchungenPanel / galRäume / btnSlot1

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1837

**Was er tut:** Zeitfenster-Knopf 1 in der Raumliste (gewählte Startzeit). Merkt Raum, Start und Ende in Variablen und öffnet das Bestätigen-Fenster. Die Endzeit wird auf die nächste fremde Buchung gekappt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        {
          vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes),
          slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis)
        },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

`DisplayMode`:
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

`Fill`:
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { istBesetzt: CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0 },
    With(
      { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
      With(
        { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
        With(
          { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
          If(
            istBesetzt,
            ColorFade(ColorValue("#EB3951"), 85%),
            If(
              vollDauerEnde <= maxVerfuegbarBis,
              ColorFade(ColorValue("#00A96B"), 70%),
              ColorFade(ColorValue("#FFA500"), 70%)
            )
          )
        )
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=With(
  { slotStart: dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
=Text(
  dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0),
  "hh:mm"
)
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewähltRaum`, `varAusgewählteStartzeit`, `varAusgewählteEndzeit`, `varZeigeRaumBestätigung`
- Gelesen: nichts
- Datenquellen: Filter auf `Raumbuchungen` (lesen, DisplayMode); Filter auf `Raumbuchungen` (lesen, Fill); Filter auf `Raumbuchungen` (lesen, HoverFill); Filter auf `Raumbuchungen` (lesen, OnSelect); Filter auf `Raumbuchungen` (lesen, Y)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung bei sichtbarem Panel: `DisplayMode`, `Fill`, `HoverFill`, `Text`, `X`, `Y` und das Info-Label enthalten mehrere `Filter`/`CountRows` auf `Raumbuchungen` je Zeile; der Klick selbst liest 1 `Filter` (nächste Buchung).

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — Vier fast gleiche Knöpfe (`btnSlot1` bis `btnSlot4`) mit den Offsets 0, 30, 60, 90 Minuten; die Zahlen stehen in `DisplayMode`, `Fill`, `OnSelect`, `Text`, `X`, `Y` je mehrfach (hohe Wartungsfläche).
- **BELEGT** — `galRäume.Items` enthält ein verschachteltes `Filter` über `Table({Offset: 0}, …)` mit `CountRows(Filter(Raumbuchungen, …))` je Slot: 4 Unterabfragen je Raum, nicht delegierbar (`app-SuggestRemoteExecutionHint` in der App-Prüfung).

### 91. Screen1 / conRaumBuchungenPanel / galRäume / btnSlot2

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 1948

**Was er tut:** Zeitfenster-Knopf 2 in der Raumliste (30 Minuten später). Merkt Raum, Start und Ende in Variablen und öffnet das Bestätigen-Fenster. Die Endzeit wird auf die nächste fremde Buchung gekappt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis) },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

`DisplayMode`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

`Fill`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 70%),
          ColorFade(ColorValue("#FFA500"), 70%)
        )
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
=Text(
  DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 30, TimeUnit.Minutes),
  "hh:mm"
)
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewähltRaum`, `varAusgewählteStartzeit`, `varAusgewählteEndzeit`, `varZeigeRaumBestätigung`
- Gelesen: nichts
- Datenquellen: Filter auf `Raumbuchungen` (lesen, DisplayMode); Filter auf `Raumbuchungen` (lesen, Fill); Filter auf `Raumbuchungen` (lesen, HoverFill); Filter auf `Raumbuchungen` (lesen, OnSelect); Filter auf `Raumbuchungen` (lesen, Y)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung bei sichtbarem Panel: `DisplayMode`, `Fill`, `HoverFill`, `Text`, `X`, `Y` und das Info-Label enthalten mehrere `Filter`/`CountRows` auf `Raumbuchungen` je Zeile; der Klick selbst liest 1 `Filter` (nächste Buchung).

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — Vier fast gleiche Knöpfe (`btnSlot1` bis `btnSlot4`) mit den Offsets 0, 30, 60, 90 Minuten; die Zahlen stehen in `DisplayMode`, `Fill`, `OnSelect`, `Text`, `X`, `Y` je mehrfach (hohe Wartungsfläche).
- **BELEGT** — `galRäume.Items` enthält ein verschachteltes `Filter` über `Table({Offset: 0}, …)` mit `CountRows(Filter(Raumbuchungen, …))` je Slot: 4 Unterabfragen je Raum, nicht delegierbar (`app-SuggestRemoteExecutionHint` in der App-Prüfung).

### 92. Screen1 / conRaumBuchungenPanel / galRäume / btnSlot3

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2048

**Was er tut:** Zeitfenster-Knopf 3 in der Raumliste (60 Minuten später). Merkt Raum, Start und Ende in Variablen und öffnet das Bestätigen-Fenster. Die Endzeit wird auf die nächste fremde Buchung gekappt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis) },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

`DisplayMode`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

`Fill`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 70%),
          ColorFade(ColorValue("#FFA500"), 70%)
        )
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
=Text(
  DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 60, TimeUnit.Minutes),
  "hh:mm"
)
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewähltRaum`, `varAusgewählteStartzeit`, `varAusgewählteEndzeit`, `varZeigeRaumBestätigung`
- Gelesen: nichts
- Datenquellen: Filter auf `Raumbuchungen` (lesen, DisplayMode); Filter auf `Raumbuchungen` (lesen, Fill); Filter auf `Raumbuchungen` (lesen, HoverFill); Filter auf `Raumbuchungen` (lesen, OnSelect); Filter auf `Raumbuchungen` (lesen, Y)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung bei sichtbarem Panel: `DisplayMode`, `Fill`, `HoverFill`, `Text`, `X`, `Y` und das Info-Label enthalten mehrere `Filter`/`CountRows` auf `Raumbuchungen` je Zeile; der Klick selbst liest 1 `Filter` (nächste Buchung).

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — Vier fast gleiche Knöpfe (`btnSlot1` bis `btnSlot4`) mit den Offsets 0, 30, 60, 90 Minuten; die Zahlen stehen in `DisplayMode`, `Fill`, `OnSelect`, `Text`, `X`, `Y` je mehrfach (hohe Wartungsfläche).
- **BELEGT** — `galRäume.Items` enthält ein verschachteltes `Filter` über `Table({Offset: 0}, …)` mit `CountRows(Filter(Raumbuchungen, …))` je Slot: 4 Unterabfragen je Raum, nicht delegierbar (`app-SuggestRemoteExecutionHint` in der App-Prüfung).

### 93. Screen1 / conRaumBuchungenPanel / galRäume / btnSlot4

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `galRäume` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2148

**Was er tut:** Zeitfenster-Knopf 4 in der Raumliste (90 Minuten später). Merkt Raum, Start und Ende in Variablen und öffnet das Bestätigen-Fenster. Die Endzeit wird auf die nächste fremde Buchung gekappt.

**Verhaltensformel**

`OnSelect`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { slotEnde: Min(DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes), maxVerfuegbarBis) },
        Set(varAusgewähltRaum, ThisItem);
        Set(varAusgewählteStartzeit, slotStart);
        Set(varAusgewählteEndzeit, slotEnde);
        Set(varZeigeRaumBestätigung, true)
      )
    )
  )
)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`DisabledFill`:
```powerfx
=ColorFade(ColorValue("#EB3951"), 85%)
```

`DisplayMode`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  If(
    CountRows(Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart)) > 0,
    DisplayMode.Disabled,
    DisplayMode.Edit
  )
)
```

`Fill`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 70%),
          ColorFade(ColorValue("#FFA500"), 70%)
        )
      )
    )
  )
)
```

`HoverFill`:
```powerfx
=With(
  { slotStart: DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes) },
  With(
    { naechsteBuchung: Filter(Raumbuchungen, Raum.Value = ThisItem.Titel && Startzeit > slotStart) },
    With(
      { maxVerfuegbarBis: If(CountRows(naechsteBuchung) = 0, dpDatumRaum.SelectedDate + Time(22, 0, 0), Min(naechsteBuchung, Startzeit)) },
      With(
        { vollDauerEnde: DateAdd(slotStart, ddDauerRaumPanel.Selected.Minuten, TimeUnit.Minutes) },
        If(
          vollDauerEnde <= maxVerfuegbarBis,
          ColorFade(ColorValue("#00A96B"), 50%),
          ColorFade(ColorValue("#FFA500"), 50%)
        )
      )
    )
  )
)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
=Text(
  DateAdd(dpDatumRaum.SelectedDate + Time(Value(Left(ddBeginnRaumPanel.Selected.Value, 2)), Value(Mid(ddBeginnRaumPanel.Selected.Value, 4, 2)), 0), 90, TimeUnit.Minutes),
  "hh:mm"
)
```

Nicht gesetzt: `Visible`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varAusgewähltRaum`, `varAusgewählteStartzeit`, `varAusgewählteEndzeit`, `varZeigeRaumBestätigung`
- Gelesen: nichts
- Datenquellen: Filter auf `Raumbuchungen` (lesen, DisplayMode); Filter auf `Raumbuchungen` (lesen, Fill); Filter auf `Raumbuchungen` (lesen, HoverFill); Filter auf `Raumbuchungen` (lesen, OnSelect); Filter auf `Raumbuchungen` (lesen, Y)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung bei sichtbarem Panel: `DisplayMode`, `Fill`, `HoverFill`, `Text`, `X`, `Y` und das Info-Label enthalten mehrere `Filter`/`CountRows` auf `Raumbuchungen` je Zeile; der Klick selbst liest 1 `Filter` (nächste Buchung).

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — Vier fast gleiche Knöpfe (`btnSlot1` bis `btnSlot4`) mit den Offsets 0, 30, 60, 90 Minuten; die Zahlen stehen in `DisplayMode`, `Fill`, `OnSelect`, `Text`, `X`, `Y` je mehrfach (hohe Wartungsfläche).
- **BELEGT** — `galRäume.Items` enthält ein verschachteltes `Filter` über `Table({Offset: 0}, …)` mit `CountRows(Filter(Raumbuchungen, …))` je Slot: 4 Unterabfragen je Raum, nicht delegierbar (`app-SuggestRemoteExecutionHint` in der App-Prüfung).

### 94. Screen1 / conRaumBestätigen / btnSpeichernRaumPanel

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conRaumBestätigen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2289

**Was er tut:** Knopf „Speichern“ im Raum-Bestätigen-Fenster. Legt eine Raumbuchung an und schließt Fenster und Panel.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Patch(Raumbuchungen, Defaults(Raumbuchungen), {
  Raum: {Id: varAusgewähltRaum.ID, Value: varAusgewähltRaum.Titel},
  Startzeit: varAusgewählteStartzeit,
  Endzeit: varAusgewählteEndzeit,
  Person: {
    '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
    Claims: "i:0#.f|membership|" & Lower(User().Email),
    DisplayName: User().FullName,
    Email: User().Email,
    JobTitle: "",
    Department: "",
    Picture: ""
  }
});
Set(varZeigeRaumBestätigung, false);
Set(varZeigeRaumBuchungForm, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=ColorValue("#171496")
```

`HoverFill`:
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="Speichern"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeRaumBestätigung`, `varZeigeRaumBuchungForm`
- Gelesen: `varAusgewähltRaum`, `varAusgewählteStartzeit`, `varAusgewählteEndzeit`
- Datenquellen: Patch auf `Raumbuchungen` (schreiben/steuern, OnSelect); Defaults auf `Raumbuchungen` (lesen, OnSelect)

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Schätzung: 1 `Patch`-Aufruf.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — Dies ist die einzige Stelle im Quellcode, die `'@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser"` beim Personenfeld mitschreibt (Z. 2306). Die Tischbuchungs-Knöpfe schreiben `Person` ohne diese Angabe (Ü6, offene Frage 2 des Briefings).
- **BELEGT** — `Raum` wird als `{Id, Value}` geschrieben, ohne `'@odata.type'`.
- **BELEGT** — Kein `IfError`, kein `Refresh`, keine Meldung, kein `varIsLoading`, keine Kollisionsprüfung beim Speichern (nur in `DisplayMode` der Slot-Knöpfe).

### 95. Screen1 / conRaumBestätigen / Button7

**Typ:** `Classic/Button@2.2.0` · **Eltern:** `conRaumBestätigen` · **Quelle:** `src/Src/Screen1.pa.yaml`, Z. 2323

**Was er tut:** Knopf „Abbrechen“ im Raum-Bestätigen-Fenster. Schließt das Fenster ohne zu speichern.

**Verhaltensformel**

`OnSelect`:
```powerfx
=Set(varZeigeRaumBestätigung, false)
```

**Zustand und Aussehen**

`Color`:
```powerfx
=RGBA(255, 255, 255, 1)
```

`Fill`:
```powerfx
=Color.Black
```

`HoverFill`:
```powerfx
=ColorFade(RGBA(100, 118, 132, 1), -20%)
```

`PressedFill`:
```powerfx
=Self.Color
```

`Text`:
```powerfx
="Abbrechen"
```

Nicht gesetzt: `DisplayMode`, `Visible`, `DisabledFill`.

**Variablen, Collections, Datenquellen**

- Geschrieben: `varZeigeRaumBestätigung`
- Gelesen: nichts
- Datenquellen: keine

**Netzwerkzugriffe je Klick (Schätzung, nicht gemessen):** Keine.

**Befunde**

- **BELEGT** — Toter Code: Der Raumbereich ist unerreichbar. `btnRaumHinzufügen` (der einzige Weg in `conRaumBuchungenPanel`) hat `Visible: =false` (Z. 704), `galRaumbuchungenHeute` hat `Visible: =false` (Z. 513), ebenso `lblMyMeetings` und `lblRaumLeer`.
- **BELEGT** — `OnSelect: =Set(varZeigeRaumBestätigung, false)`; das Raum-Panel bleibt offen.
