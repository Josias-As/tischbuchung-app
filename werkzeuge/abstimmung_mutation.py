# Mutationstest für werkzeuge/abstimmung.py: baut je einen Fehler absichtlich ein und erwartet, dass die Abstimmung ihn meldet.
# Aufruf: python3 -I werkzeuge/abstimmung_mutation.py   (die Blöcke unten werden von abstimmung.py per ABST_MUT eingelesen)
import os, subprocess, sys

if __name__ == "__main__":
    namen = [z.split()[1] for z in open(__file__, encoding="utf-8").read().split("\n") if z.startswith("#MUT ")]
    ok, zeilen = 0, []
    for n in namen:
        r = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "abstimmung.py")],
                           env=dict(os.environ, ABST_MUT=n), capture_output=True, text=True)
        zeile = [z for z in r.stdout.split("\n") if z.startswith("MUTATION")]
        zeilen.append(zeile[0] if zeile else f"MUTATION {n} ABBRUCH {r.stderr.strip().splitlines()[-1:]}")
        print(zeilen[-1])
        ok += bool(zeile) and "NICHT" not in zeile[0] or (not zeile and r.returncode != 0)
    zeilen.append(f"{ok} von {len(namen)} erkannt")
    print(zeilen[-1])
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arbeit", "2026-11-10_Abgestimmt", "ABSTIMMUNG_mutation.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
    sys.exit(0 if ok == len(namen) else 1)

#MUT ohne_L5
OHNE_L5 = True
#ENDE
#MUT neu_buchen_ohne_gastreset
b = [x for x in P3["app"] if x["control"] == "btnNeuBuchenHeute" and x["prop"] == "OnSelect"][0]
b["neu"] = b["neu"].replace("Reset(tglFuerAndere);", "", 1)
#ENDE
#MUT n5_vorher_anders
P2["app"][0]["vorher_de"] = P2["app"][0]["vorher_de"].replace(";;", ";; ", 1)
#ENDE
#MUT speichern_ohne_sperre
b = [x for x in P1["app"] if x["control"] == "btnSpeichern" and x["prop"] == "OnSelect"][0]
b["neu"] = b["neu"].replace("varSperreBis", "varSperreX")
#ENDE
#MUT colneuich_ohne_gastname
b = [x for x in P1["app"] if x["control"] == "btnSpeichern" and x["prop"] == "OnSelect"][0]
b["neu"] = b["neu"].replace(", GastName: B.GastName}", "}")
#ENDE
#MUT ladezeile_abweichend
b = [x for x in P1["app"] if x["control"] == "btnSpeichernTischePanel" and x["prop"] == "OnSelect"][0]
i = b["neu"].find("With({neu: ForAll(Filter(Tischbuchungen, (Endzeit > varAnsichtsDatum")
b["neu"] = b["neu"][:i] + b["neu"][i:].replace(", Erstellt: B.Erstellt", "", 1)
#ENDE
#MUT panel_feld_fehlt
b = [x for x in P1["app"] if x["control"] == "btnSpeichernTischePanel" and x["prop"] == "OnSelect"][0]
b["neu"] = b["neu"].replace("ddTischePanel.Selected.ID", "ddTischePanel.Selected.Nummer", 1)
#ENDE
#MUT doppelter_name
P3["neue"] = {"tglFuerAndere": P3["neue"]["btnNeuBuchenHeute"]}
#ENDE
#MUT positionen_noch_sammlung
b = [x for x in G1["app"] if x["schritt"] == "L1"][0]
b["neu"] = ist["App.OnStart"]
#ENDE
#MUT freigabe_60
b = [x for x in P2["app"] if x["control"] == "Timer1"][0]
b["neu"] = b["neu"].replace("varFreigabeMinuten, 30", "varFreigabeMinuten, 60", 1)
#ENDE
#MUT buchung_aus_sammlung
b = [x for x in P2["app"] if x["control"] == "btnVerwalten" and x["prop"] == "OnSelect"][0]
b["neu"] = b["neu"].replace("Set(varSelectedBuchung, ThisItem)", "Set(varSelectedBuchung, First(colGrundriss))", 1)
#ENDE
