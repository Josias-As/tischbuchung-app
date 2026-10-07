# Erzeugt UEBERGABE_PaketK.md aus einem entpackten Export (nur lesen).
# Aufruf: powershell -NoProfile -File erzeuge_konzept.ps1 [-Export <Ordner mit props_de.json und manifest.json>]
# props_de.json vorher mit exportiere_props.ps1 erzeugen.
param([string]$Export = 'C:\tischbuchung_work\export_07.10_veroeffentlicht')
$ErrorActionPreference = 'Stop'
$base = 'C:\tischbuchung_work'
$p = Get-Content "$Export\props_de.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$manifest = Get-Content "$Export\manifest.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$fehler = New-Object Collections.Generic.List[string]
$log = New-Object Collections.Generic.List[string]

function P([string]$n) { $v = $p.$n; if ($null -eq $v) { throw "Property fehlt im Export: $n" }; return ($v -replace "`r`n", "`n").TrimEnd() }
function Ersetze1([string]$text, [string]$alt, [string]$neu, [string]$was) {
    $c = ([regex]::Matches($text, [regex]::Escape($alt))).Count
    if ($c -ne 1) { throw "$was : Anker $c-mal gefunden (erwartet 1)" }
    $log.Add("OK  $was : Anker genau 1x gefunden")
    return $text.Replace($alt, $neu)
}
function Klammerende([string]$t, [int]$start) {
    $i = $t.IndexOf('(', $start); $tiefe = 0; $n = $t.Length
    while ($i -lt $n) {
        $c = $t[$i]
        if ($c -eq '"') { $j = $i + 1; while ($j -lt $n) { if ($t[$j] -eq '"') { if ($j + 1 -lt $n -and $t[$j + 1] -eq '"') { $j += 2; continue }; break }; $j++ }; $i = $j + 1; continue }
        if ($c -eq "'") { $i = $t.IndexOf("'", $i + 1) + 1; continue }
        if ($c -eq '(') { $tiefe++ } elseif ($c -eq ')') { $tiefe--; if ($tiefe -eq 0) { return $i } }
        $i++
    }
    throw "keine schliessende Klammer ab Position $start"
}
function Einruecken([string]$block, [int]$spalte) {
    $pre = ' ' * $spalte
    $z = $block -split "`n"
    return ($z[0] + $(if ($z.Count -gt 1) { "`n" + (($z[1..($z.Count - 1)] | ForEach-Object { $pre + $_ }) -join "`n") } else { '' }))
}
function ErsetzeBlock([string]$text, [string]$anfangRegex, [string]$neu, [string]$was) {
    $m = [regex]::Matches($text, $anfangRegex)
    if ($m.Count -ne 1) { throw "$was : Blockanfang $($m.Count)-mal gefunden (erwartet 1)" }
    $s = $m[0].Index; $e = Klammerende $text $s
    $spalte = $s - ($text.LastIndexOf("`n", [Math]::Max(0, $s - 1)) + 1)
    $log.Add("OK  $was : Block genau 1x gefunden")
    return $text.Substring(0, $s) + (Einruecken $neu $spalte) + $text.Substring($e + 1)
}
function Pruefe([string]$name, [string]$f) {
    $st = New-Object Collections.Stack; $i = 0; $n = $f.Length; $komma = 0
    $paar = @{ ')' = '('; '}' = '{'; ']' = '[' }
    while ($i -lt $n) {
        $c = $f[$i]
        if ($c -eq '"') { $j = $i + 1; while ($j -lt $n) { if ($f[$j] -eq '"') { if ($j + 1 -lt $n -and $f[$j + 1] -eq '"') { $j += 2; continue }; break }; $j++ }; if ($j -ge $n) { $fehler.Add("$name : offener String"); return }; $i = $j + 1; continue }
        if ($c -eq "'") { $j = $f.IndexOf("'", $i + 1); if ($j -lt 0) { $fehler.Add("$name : offenes '"); return }; $i = $j + 1; continue }
        if ('({['.Contains([string]$c)) { $st.Push([string]$c) }
        elseif (')}]'.Contains([string]$c)) { if ($st.Count -eq 0 -or $st.Pop() -ne $paar[[string]$c]) { $fehler.Add("$name : Klammer passt nicht bei Position $i"); return } }
        elseif ($c -eq ',') { $komma++ }
        $i++
    }
    if ($st.Count -ne 0) { $fehler.Add("$name : $($st.Count) Klammer(n) nicht geschlossen"); return }
    if ($komma -gt 0) { $fehler.Add("$name : $komma Komma(s) ausserhalb von Strings (deutsche Schreibweise verletzt)"); return }
    if ($f -match '//') { $fehler.Add("$name : Kommentar in Verhaltensformel"); return }
    # Jeder var/col-Name muss im Export schon vorkommen (keine erfundenen Namen)
    $alle = ($p.PSObject.Properties | ForEach-Object { $_.Value }) -join "`n"
    foreach ($t in ([regex]::Matches($f, '\b(var\w+|col\w+|btn\w+|dd\w+|dp\w+|tgl\w+)\b') | ForEach-Object { $_.Value } | Sort-Object -Unique)) {
        if ($alle -notmatch "\b$([regex]::Escape($t))\b" -and -not ($p.PSObject.Properties.Name | Where-Object { $_ -like "$t.*" })) { $fehler.Add("$name : Name '$t' kommt im Export nicht vor") }
    }
    $log.Add("OK  $name : Klammern, Strings, Kommas, Namen geprueft")
}
function Zeilendiff([string]$textAlt, [string]$textNeu) {
    $A = @($textAlt -split "`n"); $B = @($textNeu -split "`n"); $n = $A.Count; $m = $B.Count
    $L = New-Object 'int[,]' ($n + 1), ($m + 1)
    for ($i = $n - 1; $i -ge 0; $i--) { for ($j = $m - 1; $j -ge 0; $j--) { if ($A[$i] -ceq $B[$j]) { $L[$i, $j] = $L[($i + 1), ($j + 1)] + 1 } else { $u = $L[($i + 1), $j]; $r = $L[$i, ($j + 1)]; $L[$i, $j] = [Math]::Max($u, $r) } } }
    $z = New-Object Collections.Generic.List[object]; $i = 0; $j = 0
    while ($i -lt $n -and $j -lt $m) {
        if ($A[$i] -ceq $B[$j]) { $z.Add(@(' ', $A[$i])); $i++; $j++ }
        elseif ($L[($i + 1), $j] -ge $L[$i, ($j + 1)]) { $z.Add(@('-', $A[$i])); $i++ }
        else { $z.Add(@('+', $B[$j])); $j++ }
    }
    while ($i -lt $n) { $z.Add(@('-', $A[$i])); $i++ }; while ($j -lt $m) { $z.Add(@('+', $B[$j])); $j++ }
    $keep = New-Object bool[] $z.Count
    for ($k = 0; $k -lt $z.Count; $k++) { if ($z[$k][0] -ne ' ') { for ($d = -1; $d -le 1; $d++) { if ($k + $d -ge 0 -and $k + $d -lt $z.Count) { $keep[$k + $d] = $true } } } }
    $out = New-Object Collections.Generic.List[string]; $luecke = $false
    for ($k = 0; $k -lt $z.Count; $k++) {
        if ($keep[$k]) { $zeile = $z[$k][1]; $out.Add("$($z[$k][0]) $zeile"); $luecke = $false }
        elseif (-not $luecke) { $out.Add('  ...'); $luecke = $true }
    }
    return ($out -join "`n")
}

# ---------- Ausgangsformeln aus dem Export ----------
$orig = [ordered]@{}
foreach ($n in 'btnVerwalten_2.OnSelect', 'btnSpeichern.OnSelect', 'btnSpeichernTischePanel.OnSelect', 'btnVerlängern_1.OnSelect', 'btnVerlängern.OnSelect') { $orig[$n] = P $n }
$lade = [regex]::Match($orig['btnVerlängern.OnSelect'], 'With\(\{neu: ForAll\(Filter\(Tischbuchungen;.*?ClearCollect\(colGrundriss; neu\)\)\)').Value
if (-not $lade) { throw 'Ladezeile (L2) nicht gefunden' }
foreach ($n in 'btnSpeichern.OnSelect', 'btnSpeichernTischePanel.OnSelect', 'btnVerlängern_1.OnSelect') { if (-not $orig[$n].Contains($lade)) { throw "Ladezeile fehlt in $n - Export ist nicht der L2-Stand" } }
$log.Add("OK  L2-Ladezeile in allen Verlaengern/Speichern-Knoepfen vorhanden (Export = L2-Stand)")
foreach ($n in 'btnSpeichern', 'btnSpeichernTischePanel', 'btnVerlängern', 'btnVerlängern_1') { if ($p.PSObject.Properties.Name -contains "$n.DisplayMode") { throw "$n hat schon DisplayMode" } }
if ($p.PSObject.Properties.Name -contains 'tglAuswahlModus.Visible') { throw 'tglAuswahlModus hat schon Visible' }
$log.Add("OK  Die 4 Knoepfe haben noch kein DisplayMode, tglAuswahlModus kein Visible")

$neu = [ordered]@{}

# ---------- A1: K1 ----------
$neu['A1'] = Ersetze1 $orig['btnVerwalten_2.OnSelect'] 'Set(varSelectedBuchungTab; ThisItem);;' "Set(varSelectedBuchungTab; ThisItem);;`n  Set(varSelectedBuchung; ThisItem);;" 'A1 K1'

# ---------- K4.1 (Zwischenstand, nur fuer C1/C2) ----------
$t = $orig['btnSpeichern.OnSelect']
$k41Dialog = Ersetze1 $t 'bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel)' 'bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel && Endzeit > dpDatum.SelectedDate && Startzeit < DateAdd(dpDatum.SelectedDate; 16; TimeUnit.Days))' 'C1 K4.1'
$t = $orig['btnSpeichernTischePanel.OnSelect']
$k41Panel = Ersetze1 $t 'bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel)' 'bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Endzeit > dpDatumTischePanel.SelectedDate && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; 16; TimeUnit.Days))' 'C2 K4.1'

# ---------- A4/A5/B2/B4: K5 ----------
$riegel = 'If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)'

# ---------- B1/B3: Verlaengern neu (K2/K3 angepasst) ----------
$vorlage = @'
Set(varIsLoading; true);;
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = {SEL}.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    If(
      IsBlank(aktuelleBuchung);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set({ZEIGE}; false);
      With(
        {
          neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes);
          tagesEnde: Date(Year(aktuelleBuchung.Startzeit); Month(aktuelleBuchung.Startzeit); Day(aktuelleBuchung.Startzeit)) + Time(22; 0; 0)
        };
        If(
          neueEndzeit <= aktuelleBuchung.Startzeit;
          Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
          If(
            varAusgewaehltePlusDauer > 0 && neueEndzeit > tagesEnde;
            Notify("Über 22:00 Uhr hinaus kann nicht verlängert werden."; NotificationType.Warning);
            If(
              varAusgewaehltePlusDauer > 0 && CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
              Notify("Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen."; NotificationType.Warning);
              With(
                { speicherStatus: IfError(Patch(Tischbuchungen; aktuelleBuchung; { Endzeit: neueEndzeit }); "fehler"; "ok") };
                If(
                  speicherStatus = "fehler";
                  Notify("Speichern fehlgeschlagen. Bitte die Buchung in der Liste prüfen."; NotificationType.Error);
                  Set({SEL}; LookUp(Tischbuchungen; ID = aktuelleBuchung.ID));;
                  Notify("Buchung geändert, neues Ende " & Text(neueEndzeit; "hh:mm") & " Uhr."; NotificationType.Success);;
                  Set({ZEIGE}; false){EXTRA}
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
{LADE};;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varIsLoading; false)
'@ -replace "`r`n", "`n"
$neu['B1'] = $vorlage.Replace('{SEL}', 'varSelectedBuchungTab').Replace('{ZEIGE}', 'varZeigeVerwaltenTab').Replace('{EXTRA}', ";;`n                  Clear(colAusgewaehlteBuchungen);;`n                  Set(varMehrfachAuswahlModus; false)").Replace('{LADE}', $lade).TrimEnd()
$neu['B3'] = $vorlage.Replace('{SEL}', 'varSelectedBuchung').Replace('{ZEIGE}', 'varZeigeVerwalten').Replace('{EXTRA}', '').Replace('{LADE}', $lade).TrimEnd()
# Plausibilitaet: im Grundriss-Block darf kein Tab-Name stehen und umgekehrt
if ($neu['B3'] -match 'varSelectedBuchungTab|varZeigeVerwaltenTab') { throw 'B3 enthaelt Tab-Variablen' }
if (([regex]::Matches($neu['B1'], 'varSelectedBuchung\b')).Count -ne 0) { throw 'B1 enthaelt Grundriss-Variable varSelectedBuchung' }
$log.Add("OK  B1 nutzt nur Tab-Variablen, B3 nur Grundriss-Variablen")

# ---------- C1: Meldung Grundriss-Dialog (Sammel-Patch), baut auf A2 auf ----------
$c1Block = @'
With(
  {
    anzahlGespeichert: If(speicherStatus = "ok"; CountRows(neueDatensaetze); 0);
    anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze)
  };
  If(
    speicherStatus = "fehler";
    Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen."; NotificationType.Error);
    If(
      anzahlUebersprungen = 0 && !(effektivesBisRoh > effektivesBis);
      Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success);
      Notify(
        anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
        If(anzahlUebersprungen > 0; " Wegen Kollision nicht gebucht: " & anzahlUebersprungen & "."; "") &
        If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
        NotificationType.Warning
      )
    )
  )
)
'@ -replace "`r`n", "`n"
$neu['C1'] = ErsetzeBlock $k41Dialog 'With\(\s*\{ anzahlUebersprungen: CountRows\(datumsListe\) - CountRows\(neueDatensaetze\) \};' $c1Block.TrimEnd() 'C1 Meldung Dialog'

# ---------- C2: IfError + Meldung Tische-Panel, baut auf A3 auf ----------
$t = $k41Panel
$m = [regex]::Matches($t, 'With\(\s*\{\s*neuerEintrag: Patch\(')
if ($m.Count -ne 1) { throw "C2 K4.3: Block $($m.Count)-mal gefunden" }
$s = $m[0].Index; $e = Klammerende $t $s
$ps = $t.IndexOf('Patch(', $s); $pe = Klammerende $t $ps
$patch = $t.Substring($ps, $pe - $ps + 1)
$alt = $t.Substring($s, $e - $s + 1)
if ($alt -notmatch '"gespeichert"\s*\)$') { throw 'C2 K4.3: Block endet nicht mit "gespeichert")' }
$spalte = $s - ($t.LastIndexOf("`n", $s - 1) + 1)
$patchZeilen = $patch -split "`n"
$patchNeu = ($patchZeilen[0]) + $(if ($patchZeilen.Count -gt 1) { "`n" + (($patchZeilen[1..($patchZeilen.Count - 1)] | ForEach-Object { if ($_.StartsWith('  ')) { $_.Substring(2) } else { $_ } }) -join "`n") } else { '' })
$c2a = "IfError(`n" + (' ' * ($spalte + 2)) + $patchNeu + ";`n" + (' ' * ($spalte + 2)) + '"fehler";' + "`n" + (' ' * ($spalte + 2)) + '"gespeichert"' + "`n" + (' ' * $spalte) + ')'
$t = $t.Substring(0, $s) + $c2a + $t.Substring($e + 1)
$log.Add("OK  C2 K4.3 : Patch-Block genau 1x gefunden und in IfError gesetzt")
$c2Block = @'
With(
  {
    anzahlGespeichert: CountRows(Filter(ergebnisse; Value = "gespeichert"));
    anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen"));
    anzahlFehler: CountRows(Filter(ergebnisse; Value = "fehler"))
  };
  If(
    anzahlFehler = 0 && anzahlUebersprungen = 0 && !(effektivesBisRoh > effektivesBis);
    Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success);
    Notify(
      anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
      If(anzahlUebersprungen > 0; " Wegen Kollision nicht gebucht: " & anzahlUebersprungen & "."; "") &
      If(anzahlFehler > 0; " Fehler beim Speichern: " & anzahlFehler & ", bitte unter Meine Buchungen prüfen."; "") &
      If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
      If(anzahlFehler > 0; NotificationType.Error; NotificationType.Warning)
    )
  )
)
'@ -replace "`r`n", "`n"
$neu['C2'] = ErsetzeBlock $t 'With\(\s*\{ anzahlUebersprungen: CountRows\(Filter\(ergebnisse; Value = "übersprungen"\)\) \};' $c2Block.TrimEnd() 'C2 K4.4 Meldung Panel'

# ---------- Pruefungen ----------
foreach ($k in $neu.Keys) { Pruefe $k $neu[$k] }
Pruefe 'K5' $riegel
# Unveraendert-Pruefung: ausser den gewollten Stellen darf sich nichts aendern
function Gleich-ausser([string]$name, [string]$a, [string]$b, [string[]]$erlaubt) {
    $d = (Zeilendiff $a $b) -split "`n" | Where-Object { $_ -match '^[+-] ' }
    foreach ($z in $d) { $ok = $false; foreach ($e in $erlaubt) { if ($z -match $e) { $ok = $true } }; if (-not $ok) { $fehler.Add("$name : unerwartete Aenderung: $z") } }
    $log.Add("OK  $name : nur erlaubte Zeilen geaendert ($($d.Count) Zeilen)")
}
Gleich-ausser 'A1' $orig['btnVerwalten_2.OnSelect'] $neu['A1'] @('^\+   Set\(varSelectedBuchung; ThisItem\);;$')
Gleich-ausser 'K4.1 Dialog' $orig['btnSpeichern.OnSelect'] $k41Dialog @('bestehendeBuchungenTisch:')
Gleich-ausser 'K4.1 Panel' $orig['btnSpeichernTischePanel.OnSelect'] $k41Panel @('bestehendeBuchungenTisch:')

# ---------- Markdown ----------
$stand = $manifest.details.createdTime
$sb = New-Object Text.StringBuilder
function W([string]$s) { [void]$sb.AppendLine($s) }
function Block([string]$id, [string]$ctrl, [string]$titel, [string]$alt, [string]$neuF, [string]$was, [string]$test) {
    W "### $id ``$ctrl``"
    W "**$titel**"
    W ''
    W $was
    W ''
    if ($alt) { W 'Änderung (rot = weg, grün = neu, `...` = unverändert):'; W '```diff'; W (Zeilendiff $alt $neuF); W '```' }
    W "**Einfügen: ganze Property ``$ctrl`` ersetzen durch**"
    W ''
    W '```'
    W $neuF
    W '```'
    W "**Test:** $test"
    W ''
}
$md = Get-Content "$base\konzept_text.md" -Raw -Encoding UTF8
$teile = $md -split '<<<BLOECKE>>>'
W ($teile[0].Replace('{STAND}', $stand).TrimEnd()); W ''

W '## 3. Teil A: klein, vor dem Go-Live (empfohlen)'
W 'Reihenfolge einhalten. Nach jedem Schritt: App-Prüfung (Baseline 134 Einträge, keine Formelfehler), kurz testen, Ergebnis melden.'
W ''
Block 'A1' 'btnVerwalten_2.OnSelect' 'K1: Dauer-Knöpfe im Buchungen-Tab bewerten die richtige Buchung' $orig['btnVerwalten_2.OnSelect'] $neu['A1'] 'Eine Zeile neu. Behebt Befund B0: Die 12 Plus-/Minus-Properties lesen `varSelectedBuchung`, der Tab-Dialog setzte bisher nur `varSelectedBuchungTab`. Danach ist der Plus-Knopf nur grün, wenn **diese** Buchung verlängert werden kann.' 'Im Grundriss eine Buchung A verwalten, Dialog schließen. Im Tab „Meine Buchungen“ eine andere Buchung B verwalten: Plus-/Minus-Knöpfe passen zu B (z. B. Plus grau, wenn hinter B direkt jemand gebucht hat). Danach umgekehrt (erst Tab, dann Grundriss).'
W '### A2 `btnSpeichern.DisplayMode` und A3 `btnSpeichernTischePanel.DisplayMode`'
W '**K5: Doppelklick-Riegel beim Speichern**'
W ''
W 'Die Property `DisplayMode` ist bei beiden Knöpfen heute nicht gesetzt (Standard = bedienbar). Neu wird der Knopf gesperrt, solange `varIsLoading` wahr ist. Beide Knöpfe setzen `varIsLoading` schon am Anfang auf wahr und am Ende auf falsch, auf jedem Weg.'
W ''
W '**Einfügen: bei beiden Knöpfen die Property `DisplayMode` setzen auf**'
W ''
W '```'
W $riegel
W '```'
W '**Test:** Buchen und dabei zweimal schnell auf Speichern klicken → nur eine Buchung, nur eine Meldung. Danach ist der Knopf wieder bedienbar.'
W ''

W '## 4. Teil B: Verlängern sicher machen (vor dem Go-Live, wenn Teil A ok)'
W 'Ersetzt K2/K3 aus `ENTWURF_SPEICHERN.md` (dort fehlte die L2-Ladezeile, und die Prüfung mit `ID <>` ist nicht delegierbar). Die Kollisionsprüfung ist **wortgleich** mit der, die die Plus-Knöpfe heute schon benutzen (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`, delegierbar, die eigene Buchung fällt automatisch raus). Nur zweiarmige `If`, das Speichermuster `IfError(Patch(...); "fehler"; "ok")` ist aus `btnSpeichern` übernommen und dort gemessen.'
W ''
W 'Was der neue Knopf tut, in dieser Reihenfolge: Ladeanzeige an → Buchung frisch vom Server → keine Dauer gewählt? / Buchung gelöscht? / Buchung würde leer? / über 22:00? / Tisch inzwischen belegt? → jeweils Meldung, nichts schreiben → sonst speichern, bei Fehler ehrliche Meldung, bei Erfolg Meldung mit neuem Ende und Dialog schließen → immer: Liste neu laden, Grundriss neu laden, Dauer-Auswahl leeren, Ladeanzeige aus.'
W ''
Block 'B1' 'btnVerlängern_1.OnSelect' 'K2 neu: Verlängern/Verkürzen im Buchungen-Tab' $orig['btnVerlängern_1.OnSelect'] $neu['B1'] 'Ganze Property neu (Ablauf siehe oben). Bleibt gleich: frische Buchung per `LookUp`, `varSelectedBuchungTab` wird nach dem Speichern aktualisiert, `Refresh`, L2-Ladezeile, `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus; false)` beim Erfolg. Neu: `varIsLoading`, die Prüfungen, Erfolgs-/Fehlermeldung. Die Dauer-Auswahl wird jetzt auch nach einer Warnung geleert (man wählt neu).' '(1) Buchung im Tab um +1 Std verlängern → Meldung „Buchung geändert, neues Ende …“, Liste und Grundriss stimmen. (2) Verkürzen −1 Std → ok. (3) Buchung 19:00–21:30, +1 Std → „Über 22:00 Uhr …“, nichts geändert. (4) Zwei-Tab-Test: in Tab 2 direkt hinter die Buchung buchen, in Tab 1 (Dialog war schon offen, Knopf noch grün) +1 Std → „Der Tisch ist … inzwischen belegt“. (5) In Tab 2 die Buchung stornieren, in Tab 1 verlängern → „Diese Buchung gibt es nicht mehr“, Dialog zu.'
W '### B2 `btnVerlängern_1.DisplayMode`'
W '**K5 für Verlängern im Tab** (erst nach B1, denn erst B1 setzt `varIsLoading`)'
W ''
W '```'
W $riegel
W '```'
W '**Test:** Zweimal schnell auf Verlängern (+1 Std) → genau +1 Std, eine Meldung.'
W ''
Block 'B3' 'btnVerlängern.OnSelect' 'K3 neu: Verlängern im Grundriss-Dialog' $orig['btnVerlängern.OnSelect'] $neu['B3'] 'Dieselbe Formel wie B1, nur mit den Grundriss-Namen: `varSelectedBuchung` statt `varSelectedBuchungTab`, `varZeigeVerwalten` statt `varZeigeVerwaltenTab`, ohne die zwei Mehrfachauswahl-Zeilen (die hatte der Grundriss-Knopf auch heute nicht). Neu gegenüber heute zusätzlich `Refresh(Tischbuchungen)` (fehlte hier bisher). Die Namen sind maschinell geprüft: B3 enthält keine Tab-Variable, B1 keine Grundriss-Variable.' 'Wie B1 Punkt (1), (3), (4), (5), aber über den Grundriss (Kachel anklicken → Verwalten). Verkürzen gibt es im Grundriss-Dialog nicht (nur Plus-Knöpfe), der Zweig ist harmlos. Zusätzlich: Nach dem Verlängern stimmen Kachelfarbe und, beim erneuten Öffnen, die angezeigte Endzeit (`lblZeit`).'
W '### B4 `btnVerlängern.DisplayMode`'
W '**K5 für Verlängern im Grundriss** (erst nach B3)'
W ''
W '```'
W $riegel
W '```'
W '**Test:** wie B2 im Grundriss.'
W ''

W '## 5. Teil C: ehrliche Meldungen bei Serien (optional, auch nach dem Go-Live möglich)'
W '**Jeder Speichern-Knopf wird hier nur einmal angefasst.** C1/C2 enthalten zusätzlich K4.1: Die Kollisionsabfrage holt nur noch die Buchungen dieses Tisches im Serienzeitraum (Startdatum bis +16 Tage) statt aller, die es je gab. Das spart Daten und schützt vor dem Datenzeilenlimit. Der Rest der Formel ist wortgleich mit heute (inkl. L2-Ladezeile).'
W ''
Block 'C1' 'btnSpeichern.OnSelect' 'K4.1 + K4.4 (angepasst an den Sammel-Patch): weniger Daten, eine Meldung, die alles sagt' $orig['btnSpeichern.OnSelect'] $neu['C1'] 'Zwei Stellen: (1) Zeile `bestehendeBuchungenTisch` mit Zeitfenster. (2) Meldungsteil: Heute verdrängt „auf 2 Wochen begrenzt“ die Kollisionsmeldung (Befund B3). Neu: Normalfall unverändert „Buchung(en) erfolgreich gespeichert.“, sonst **eine** gelbe Meldung mit allem, z. B. „8 von 11 Terminen gespeichert. Wegen Kollision nicht gebucht: 3. Die Wiederholung wurde auf 2 Wochen begrenzt.“ Fehlerfall wie bisher.' 'Einzelbuchung → „Buchung(en) erfolgreich gespeichert.“ Serie mit Bis-Datum in 4 Wochen (wird gekappt) auf einen Tisch mit einer fremden Buchung im Zeitraum → eine Meldung nennt Anzahl, Kollision und Kappung; die fremde Buchung wurde nicht doppelt belegt.'
Block 'C2' 'btnSpeichernTischePanel.OnSelect' 'K4.1 + K4.3 + K4.4: Panel mit weniger Daten, erkennt Schreibfehler, eine Meldung' $orig['btnSpeichernTischePanel.OnSelect'] $neu['C2'] 'Drei Stellen: (1) `bestehendeBuchungenTisch` mit Zeitfenster wie C1. (2) Der einzelne `Patch` steht in `IfError`: Schlägt ein Termin fehl, zählt er als „fehler“ statt als „gespeichert“ (Befund B2). (3) Meldung wie C1, zusätzlich mit Fehleranzahl (dann rot). Aufräumteil unverändert.' 'Wie C1 über das Tische-Panel. Den Fehlerfall kann man nicht gezielt auslösen (UNSICHER, siehe U-K6).'

W '## 6. Teil E: Entscheidung Mehrfachauswahl (nur falls du sie zum Go-Live ausblenden willst)'
W '### E2 `tglAuswahlModus.Visible`'
W 'Der Schalter hat heute keine `Visible`-Property (= sichtbar). Ausblenden genügt: Ohne Schalter bleibt `varAuswahlModusAktiv` falsch (`App.OnStart`), alle Einzel-Funktionen bleiben.'
W ''
W '```'
W 'false'
W '```'
W '**Rückgängig:** `true`. **Test:** Tab „Meine Buchungen“: kein Auswahlschalter, Verwalten-Knopf öffnet den normalen Dialog.'
W ''
W $teile[1].TrimEnd()
W ''
W '## Anhang 1: Originale (für den Rückfall, aus dem Export)'
foreach ($n in $orig.Keys) { W "**``$n``**"; W ''; W '```'; W $orig[$n]; W '```' }
W '**`btnSpeichern.DisplayMode`, `btnSpeichernTischePanel.DisplayMode`, `btnVerlängern.DisplayMode`, `btnVerlängern_1.DisplayMode`**: im Export nicht gesetzt. Rückgängig: `DisplayMode.Edit`.'
W ''
W '## Anhang 2: Maschinelle Prüfung (erzeugt von `erzeuge_konzept.ps1`)'
W '```'
foreach ($z in $log) { W $z }
if ($fehler.Count) { foreach ($z in $fehler) { W "FEHLER $z" } } else { W 'Keine Fehler.' }
W '```'
[IO.File]::WriteAllText("$base\UEBERGABE_PaketK_v1.md", $sb.ToString(), (New-Object Text.UTF8Encoding $false))
foreach ($z in $log) { Write-Host $z }
if ($fehler.Count) { foreach ($z in $fehler) { Write-Host "FEHLER $z" }; exit 1 } else { Write-Host 'Keine Fehler. Datei: UEBERGABE_PaketK_v1.md' }
