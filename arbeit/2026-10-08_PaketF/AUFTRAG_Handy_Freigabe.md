# Auftrag an den Handy-Chat: Freigabe-Regel aus Paket F übernehmen

Stand 08.10.2026, von Claude Code (Desktop-App). Grundlage: Export „Tischbuchung Handy“ vom 07.10. Die Befunde B1–B11 (YAML) sind dort **nicht** enthalten. Wenn du sie schon eingebaut hast, gelten die Namen unten sinngemäß.

## Warum
Die Desktop-App gibt ab Paket F nicht eingecheckte Buchungen **in der App** frei, ohne Flow und ohne etwas zu löschen. Die Handy-App liest dieselbe Liste. Ohne dieselbe Regel passiert Folgendes:
- Sie zeigt freigegebene Tische weiter als belegt und lässt dort keine Buchung zu. Das ist harmlos, aber ärgerlich.
- Sie lässt **Einchecken auf eine verfallene Buchung** zu, auch wenn der Tisch inzwischen an jemand anderen vergeben ist. **Dann sitzen zwei Personen „eingecheckt“ am selben Tisch.**

**Deshalb: die Handy-App erst teilen, wenn die Regel drin ist.**

## Die Regel (wörtlich wie in der Desktop-App)
- **Verfallen** = nicht eingecheckt **und** `Startzeit <= jetzt − 30 Min` **und** `Erstellt <= jetzt − 30 Min`.
  - `Erstellt` ist die SharePoint-Systemspalte „Created“, Anzeigename „Erstellt“, lesbar und nach `gt/lt` filterbar (belegt im Export).
  - Formel: `!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze` mit `Set(varFreigabeGrenze; DateAdd(Now(); -varFreigabeMinuten; TimeUnit.Minutes))` und `Set(varFreigabeMinuten; 30)` in `App.OnStart`.
- **Verfallene Buchungen zählen überall als frei.** Gelöscht wird nichts.
- **Serverseitig nicht nach `CheckedIn` filtern** (Ja/Nein gilt als unzuverlässig delegierbar). Erst delegierbar nach Zeit/Tisch/Person holen (`ClearCollect`), dann lokal `RemoveIf(col; <verfallen>)`. Wo eine Collection nicht geht (Items), `ForAll(Filter(...) As X; {...; Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze})` und nur `Aktiv` zählen.
- **Einchecken** ab 30 Min vor Beginn **bis zur Frist** (nicht mehr bis zum Ende). Vor dem Patch frisch prüfen, ob eine andere, nicht verfallene Buchung denselben Tisch in der Zeit hat. Wenn ja: „Der Tisch ist in dieser Zeit schon an jemand anderen vergeben.“
- **Auschecken / Jetzt beenden** = Ende auf jetzt. Die Handy-App macht das schon mit `btnJetztBeenden`.

## Was in der Handy-App betroffen ist (Export 07.10.)
| Stelle | Heute | Ändern |
|---|---|---|
| `ddTisch.Items` | `Filter(Tischbuchungen; Startzeit < … && Endzeit > …)` → belegte Tische | nur nicht verfallene Buchungen zählen |
| `btnBuchen.OnSelect` | `LookUp` Tisch belegt / ich habe schon einen Tisch, danach Nachprüfung `Filter(...)` | verfallene ausnehmen (ClearCollect + RemoveIf), Nachprüfung ebenso, sonst falsche „doppelt“-Meldung |
| `btnEincheckenH.OnSelect` | Fenster bis Ende | Fenster bis Frist + Prüfung „schon vergeben“ |
| `btnVerl1/btnVerl2.OnSelect` | `LookUp` Kollision | verfallene ausnehmen; eigene verfallene Buchung nicht verlängern |
| `galHeute` / `galMeine` | eigene Buchungen | Status „Verfallen“ anzeigen (grau) statt „Einchecken“ |
| Grundriss/Kacheln (falls vorhanden) | | wie Desktop: verfallene als frei |

## Prüfen
- Testzeile direkt in SharePoint anlegen (Beginn vor 1 Std, CheckedIn = Nein). `Erstellt` ist dann „jetzt“, die Frist läuft also erst 30 Min später ab. Für schnelle Tests `varFreigabeMinuten` vorübergehend auf 1 setzen.
- Dann am Handy: Tisch ist buchbar. Einchecken der alten Buchung geht nicht („zu spät“).
- Gegenprobe Desktop: dieselbe Situation, dasselbe Ergebnis.

Fragen dazu an Claude Code (Desktop-Repo `tischbuchung-app`, `arbeit/2026-10-08_PaketF/UEBERGABE_PaketF.md`).
