# Handy H8 (08.10.2026): Tageswechsel bei offener App. Grundlage: Handy-Export 08.10. 14:25 (veröffentlicht, = Umbauplan v2).
# Aufruf: python3 -I werkzeuge/handy_h8.py -> arbeit/2026-10-08_Nachtrag5/handy_h8_bloecke.json
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

h = A.lade_handy_fertig()
ist = h.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag5")
final = {}

k = "App.OnStart"
alt = "Set(varJetzt, Now());"
assert ist[k].count(alt) == 1
final[k] = ist[k].replace(alt, alt + " Set(varHeute, Today());")

k = "tmrJetzt.OnTimerEnd"
assert ist[k] == "Set(varJetzt, Now())"
final[k] = ("Set(varJetzt, Now());\n"
            "If(\n  !varIsLoading && Today() <> varHeute,\n"
            "  Set(varHeute, Today());\n  Reset(ddDatum);\n  Set(varNeuLaden, varNeuLaden + 1)\n)")

k = "ddDatum.Items"
assert ist[k].count("Today()") == 2
final[k] = ist[k].replace("Today()", "Coalesce(varHeute, Today())")

k = "lblHeuteTitel.Text"
assert ist[k] == '"Heute, " & Text(Today(), "dddd dd.mm.")'
final[k] = '"Heute, " & Text(Coalesce(varHeute, Today()), "dddd dd.mm.")'

fehler = []
end = dict(ist); end.update(final)
gesetzt = {m.group(1) for v in end.values() for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v)}
for k, v in final.items():
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    for x in set(re.findall(r"\b((?:var|col)\w+)\b", A.ausserhalb_strings(v))):
        if x not in gesetzt:
            fehler.append(f"{k}: Variable {x} nirgends gesetzt")
    if "Tischbuchungen" in A.ausserhalb_strings(v) and k != "App.OnStart":
        fehler.append(f"{k}: neue Abfrage")
if "Today()" in final["ddDatum.Items"].replace("Coalesce(varHeute, Today())", ""):
    fehler.append("ddDatum.Items: ungeschütztes Today()")
if "varJetzt" in final["ddDatum.Items"]:
    fehler.append("ddDatum.Items hängt am Minutentakt (Auswahl würde springen)")


def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


out = [dict(control=k.split(".")[0], prop=k.split(".", 1)[1], neu=v, de=A.to_de(v), vorher_de=A.to_de(ist[k]),
            diff=diff(A.to_de(ist[k]), A.to_de(v)), pfad=h.pfad(k.split(".")[0])) for k, v in final.items()]
json.dump(dict(app=out, fehler=fehler, timer_duration=ist.get("tmrJetzt.Duration")), open(os.path.join(ZIEL, "handy_h8_bloecke.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# --- Übergabe-Dokument ---------------------------------------------------------------------------------------------
TXT = """# Handy H8: Tageswechsel bei offener App (08.10.2026)

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

"""
doc = [TXT]
for b in out:
    doc += [f"### `{b['control']}.{b['prop']}`", "", f"Ort: `{b['pfad']}` · **ganze Property ersetzen**", "",
            "Änderung gegenüber dem Export (`-` alt, `+` neu):", "", "```diff", b["diff"], "```", "", "Vollständiger Block:", "", "```", b["de"], "```", ""]
doc += ["""## Test (etwa 3 Minuten)
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
"""]
for b in out:
    doc += [f"**`{b['control']}.{b['prop']}`**", "", "```", b["vorher_de"], "```", ""]
open(os.path.join(ZIEL, "HANDY_H8_Tageswechsel.md"), "w", encoding="utf-8").write("\n".join(doc))
print(f"{len(out)} Properties.", "Prüfung: 0 Fehler" if not fehler else "FEHLER: " + "; ".join(fehler))
sys.exit(1 if fehler else 0)
