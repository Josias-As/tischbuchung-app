# Aufruf: powershell -File pruefe_formeln.ps1 <Ordner mit App.pa.yaml und Screen1.pa.yaml> <UEBERGABE_Grundriss_L2_v0.3.md>
# PowerShell-Port von pruefe_formeln.py (nur lesen, kein Python/PyYAML noetig).
param([string]$Src, [string]$Md)
$props = @{}
function Read-Props([string]$file) {
    $lines = [IO.File]::ReadAllLines($file, [Text.Encoding]::UTF8)
    $stack = @()   # Eintraege: @{indent=..; name=..}
    $i = 0; $n = $lines.Count
    while ($i -lt $n) {
        $l = $lines[$i]
        if ($l -match '^(\s*)(- )?(.+?)(?: As [^:]+)?:\s*$' -and $l -notmatch '^\s*#') {
            $ind = $Matches[1].Length + $(if ($Matches[2]) { 2 } else { 0 })
            $key = $Matches[3]
            if ($key -ne 'Properties' -and $key -ne 'Children' -and $key -ne 'Control') {
                while ($stack.Count -gt 0 -and $stack[-1].indent -ge $ind) { $stack = @($stack | Select-Object -SkipLast 1) }
                $stack += @{indent=$ind; name=$key}
            } elseif ($key -eq 'Properties') {
                $owner = if ($stack.Count) { $stack[-1].name } else { '?' }
                $pind = $Matches[1].Length + 2
                $i++
                while ($i -lt $n) {
                    $pl = $lines[$i]
                    if ($pl.Trim() -eq '') { $i++; continue }
                    $cur = ($pl.Length - $pl.TrimStart().Length)
                    if ($cur -lt $pind) { break }
                    if ($cur -eq $pind -and $pl -match '^\s*([^\s:]+): ?(.*)$') {
                        $pn = $Matches[1]; $val = $Matches[2]
                        if ($val -match '^\|[-+]?$') {
                            $buf = New-Object Collections.Generic.List[string]
                            $i++
                            while ($i -lt $n) {
                                $bl = $lines[$i]
                                $bc = ($bl.Length - $bl.TrimStart().Length)
                                if ($bl.Trim() -ne '' -and $bc -le $pind) { break }
                                $buf.Add($bl); $i++
                            }
                            $ni = ($buf | Where-Object { $_.Trim() -ne '' } | Select-Object -First 1)
                            $base = if ($ni) { $ni.Length - $ni.TrimStart().Length } else { 0 }
                            $txt = ($buf | ForEach-Object { if ($_.Length -ge $base) { $_.Substring($base) } else { $_.TrimStart() } }) -join "`n"
                            $props["$owner.$pn"] = $txt.TrimEnd()
                            continue
                        } else {
                            $props["$owner.$pn"] = $val
                        }
                    }
                    $i++
                }
                continue
            }
        }
        $i++
    }
}
function De([string]$f) {
    if ($f.StartsWith('=')) { $f = $f.Substring(1) }
    $sb = New-Object Text.StringBuilder; $i = 0; $n = $f.Length
    while ($i -lt $n) {
        $c = $f[$i]
        if ($c -eq '"') {
            $j = $i + 1
            while ($j -lt $n) { if ($f[$j] -eq '"') { if ($j + 1 -lt $n -and $f[$j+1] -eq '"') { $j += 2; continue }; break }; $j++ }
            [void]$sb.Append($f.Substring($i, $j - $i + 1)); $i = $j + 1; continue
        }
        if ($c -eq "'") { $j = $f.IndexOf("'", $i + 1); [void]$sb.Append($f.Substring($i, $j - $i + 1)); $i = $j + 1; continue }
        if ($c -eq '/' -and $i + 1 -lt $n -and $f[$i+1] -eq '/') {
            $j = $f.IndexOf("`n", $i); if ($j -lt 0) { $j = $n }
            [void]$sb.Append($f.Substring($i, $j - $i)); $i = $j; continue
        }
        if ($c -eq ';') { [void]$sb.Append(';;') }
        elseif ($c -eq ',') { [void]$sb.Append(';') }
        elseif ($c -eq '.' -and $i -gt 0 -and [char]::IsDigit($f[$i-1]) -and $i + 1 -lt $n -and [char]::IsDigit($f[$i+1])) { [void]$sb.Append(',') }
        else { [void]$sb.Append($c) }
        $i++
    }
    $sb.ToString()
}
function Ws([string]$s) { $s -replace '\s+', '' }

foreach ($fn in 'App.pa.yaml', 'Screen1.pa.yaml') { Read-Props (Join-Path $Src $fn) }
Write-Host "Properties im Export gelesen:" $props.Count

$text = [IO.File]::ReadAllText($Md, [Text.Encoding]::UTF8) -replace "`r`n", "`n"
$m = [regex]::Match($text, '\*\*Die Ladezeile\*\*.*?```\n(.*?)\n```', 'Singleline'); $LOAD = $m.Groups[1].Value
$rx = '\*\*`([\w]+\.\w+)`\*\*[^\n]*\n\n```\n(.*?)\n```'
$parts = $text -split '## Anhang 1', 2
$blocksA = [regex]::Matches($parts[0], $rx, 'Singleline')
$anhang = @{}; foreach ($b in [regex]::Matches($parts[1], $rx, 'Singleline')) { $anhang[$b.Groups[1].Value] = $b.Groups[2].Value }
Write-Host "Ladezeile:" $LOAD.Length "Zeichen; Formelbloecke Hauptteil:" $blocksA.Count "; Anhang:" $anhang.Count
$bad = 0
foreach ($b in $blocksA) {
    $name = $b.Groups[1].Value; $f = $b.Groups[2].Value
    if (-not $props.ContainsKey($name)) { Write-Host "$name : NICHT IM EXPORT"; $bad++; continue }
    $curde = De $props[$name]
    if ($f.Contains($LOAD)) {
        $cnt = ([regex]::Matches($f, [regex]::Escape($LOAD))).Count
        $s = $f.Replace($LOAD + ";;`n", '').Replace($LOAD + ';;', '').Replace("`n" + $LOAD, '').Replace($LOAD, '')
        $ex = $s.TrimEnd() -ceq $curde.TrimEnd(); $okws = (Ws $s) -ceq (Ws $curde); if (-not $okws) { $t=(Ws $s); if ($t.EndsWith(";;")) { $t=$t.Substring(0,$t.Length-2) }; if ($t -ceq (Ws $curde)) { $okws=$true; Write-Host "   (nur zusaetzliches ;; vor der Ladezeile)" } }
        Write-Host "A $name : Ladezeile x$cnt; Rest==Export exakt:$ex ohneLeerzeichen:$okws"
        if (-not $okws) { $bad++ }
    } else {
        $o = $anhang[$name]; $okws = $o -and ((Ws $o) -ceq (Ws $curde)); $ex = $o -and ($o.TrimEnd() -ceq $curde.TrimEnd())
        Write-Host "B $name : Anhang-Original==Export exakt:$ex ohneLeerzeichen:$okws"
        if (-not $okws) { $bad++ }
    }
}
Write-Host "Abweichungen (ohne Leerzeichen):" $bad

