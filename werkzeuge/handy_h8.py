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
print(f"{len(out)} Properties.", "Prüfung: 0 Fehler" if not fehler else "FEHLER: " + "; ".join(fehler))
sys.exit(1 if fehler else 0)
