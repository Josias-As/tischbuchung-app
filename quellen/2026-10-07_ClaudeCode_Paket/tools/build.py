# Erzeugt aus einem entpackten Export die 20 L2-Formeln (deutsch) inkl. Originale.
# Aufruf: python3 -I tools/build.py <export>/Src out.json   (Src = Ordner mit Screen1.pa.yaml und App.pa.yaml)
import yaml, sys, re, json
SRC = sys.argv[1]
scr = yaml.load(open(SRC + "/Screen1.pa.yaml"), Loader=yaml.BaseLoader)
app = yaml.load(open(SRC + "/App.pa.yaml"), Loader=yaml.BaseLoader)
ctrls = {}
def walk(children):
    for ch in children or []:
        for name, body in ch.items():
            ctrls[name] = body.get("Properties", {}) or {}
            walk(body.get("Children"))
walk(scr["Screens"]["Screen1"]["Children"])
ctrls["App"] = app["App"]["Properties"]

def get(c, p):
    v = ctrls[c][p]
    assert v.startswith("="), (c, p)
    return v[1:]

def to_de(f):
    out = []; i = 0; n = len(f)
    while i < n:
        ch = f[i]
        if ch in "\"'":
            j = i + 1
            while j < n:
                if f[j] == ch:
                    if j + 1 < n and f[j+1] == ch: j += 2; continue
                    break
                j += 1
            out.append(f[i:j+1]); i = j + 1; continue
        if ch == "/" and f[i:i+2] == "//": raise ValueError("comment in formula")
        if ch == ";": out.append(";;")
        elif ch == ",": out.append(";")
        elif ch == "." and i > 0 and f[i-1].isdigit() and i+1 < n and f[i+1].isdigit():
            # only true numeric literal: preceding run of digits must not be part of identifier
            k = i - 1
            while k >= 0 and f[k].isdigit(): k -= 1
            out.append("," if (k < 0 or not (f[k].isalnum() or f[k] in "_")) else ".")
        else: out.append(ch)
        i += 1
    return "".join(out)

def balanced(f):
    depth = {"(":0,"{":0,"[":0}; pairs = {")":"(","}":"{","]":"["}
    i=0;n=len(f)
    while i<n:
        ch=f[i]
        if ch in "\"'":
            j=i+1
            while j<n:
                if f[j]==ch:
                    if j+1<n and f[j+1]==ch: j+=2; continue
                    break
                j+=1
            i=j+1; continue
        if ch in depth: depth[ch]+=1
        elif ch in pairs:
            depth[pairs[ch]]-=1
            if depth[pairs[ch]]<0: return False
        i+=1
    return all(v==0 for v in depth.values())

LADE = ('With({neu: ForAll(Filter(Tischbuchungen, (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(), 60, TimeUnit.Minutes))) As B, '
        '{TischName: B.Tisch.Value, Startzeit: B.Startzeit, Endzeit: B.Endzeit, Eingecheckt: B.CheckedIn, Name: B.Person.DisplayName})}, '
        'If(IsError(neu) || IsError(First(neu)), Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen.", NotificationType.Warning), ClearCollect(colGrundriss, neu)))')

out = []  # (step, control, prop, english, note)
def add(step, c, p, new, note=""):
    assert balanced(new), (c, p)
    out.append((step, c, p, new, note))

def insert_after(c, p, anchor, step, note=""):
    f = get(c, p)
    assert f.count(anchor) == 1, (c, p, f.count(anchor))
    add(step, c, p, f.replace(anchor, anchor + "\n" + LADE + ";"), note)

def append_end(c, p, step, note=""):
    f = get(c, p).rstrip()
    add(step, c, p, f + ";\n" + LADE, note)

# Schritt 1: laden
append_end("App", "OnStart", 1, "Ladezeile ganz ans Ende (Prüfbefund 1)")
f = get("dpAnsichtsDatum", "OnChange"); add(1, "dpAnsichtsDatum", "OnChange", f.rstrip() + ";\n" + LADE)
f = get("ddStockwerk", "OnChange"); add(1, "ddStockwerk", "OnChange", f.rstrip() + ";\n" + LADE, "neu: haelt Fremdbuchungen beim Stockwerkwechsel aktuell wie heute")
for c in ["Icon1", "Icon1_1", "Image6", "btnHitArea_1"]:
    insert_after(c, "OnSelect", "Refresh(Tischbuchungen);", 1)

# Schritt 2: Kacheln
def tile(c, p):
    f = get(c, p)
    n0 = f.count("LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel")
    g = f.replace("LookUp(Tischbuchungen, Tisch.Value = ThisItem.Titel", "LookUp(colGrundriss, TischName = ThisItem.Titel")
    g = g.replace("relevanteBuchung.CheckedIn", "relevanteBuchung.Eingecheckt").replace("relevanteBuchung.Person.DisplayName", "relevanteBuchung.Name")
    assert "Tischbuchungen" not in g and n0 > 0, (c, p)
    add(2, c, p, g, f"{n0} Abfragen auf colGrundriss umgestellt")
tile("Rectangle1", "Fill")
for p in ["BorderColor", "BorderStyle", "Fill"]: tile("Circle1", p)
tile("Label1", "Text")

# Schritt 3: Schreibwege
for c in ["btnSpeichern", "btnSpeichernTischePanel", "btnVerlängern_1", "btnStornieren_1", "btnStornierenKlein"]:
    insert_after(c, "OnSelect", "Refresh(Tischbuchungen);", 3)
for c in ["btnVerlängern", "btnStornieren", "btnEinchecken"]:
    append_end(c, "OnSelect", 3, "hat heute kein Refresh; Ladezeile ans Ende")

res = []
for step, c, p, f, note in out:
    de = to_de(f)
    assert balanced(de)
    res.append({"step": step, "control": c, "prop": p, "de": de, "note": note, "orig_de": to_de(get(c, p))})
json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(len(res), "properties")
for r in res: print(r["step"], r["control"], r["prop"], len(r["de"]), r["note"])
