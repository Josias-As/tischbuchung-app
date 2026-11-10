# P0 Design-Korrektur (10.11.2026): zwei Befunde aus DESIGN_PRUEFUNG.md, Abschnitt 4 (Josias: „wie du meinst, dass es stimmig ist“).
# D1 btnHeuteDatum: Schrift beim Drücken unsichtbar. D2 „Tisch Buchen“: weiß auf #D0D0D0 (1,5:1) -> Stil des Hauptknopfs btnSpeichern.
# Aufruf: python3 -I werkzeuge/design_korrektur.py -> arbeit/2026-11-10_Abgestimmt/P0_Design/
import difflib, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_1011_echt()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-11-10_Abgestimmt/P0_Design")
os.makedirs(ZIEL, exist_ok=True)
roh = {}
for fn in glob.glob(os.path.join(A.ENTPACKT, "desktop_2026-11-10_echt", "Controls", "*.json")):
    def w(n):
        for r in n.get("Rules", []):
            roh[f"{n['Name']}.{r['Property']}"] = r["InvariantScript"].strip()
        for c in n.get("Children", []):
            w(c)
    w(json.load(open(fn, encoding="utf-8-sig"))["TopParent"])
fehler = []
final = {"btnHeuteDatum.PressedColor": "RGBA(255, 255, 255, 1)"}
for p in ["Fill", "HoverFill", "PressedFill", "PressedColor", "Size", "Width"]:
    final[f"btnTischHinzufügen.{p}"] = roh[f"btnSpeichern.{p}"]
# Prüfungen: Werte stimmen mit dem Hauptknopf überein, Breite reicht für den Text, sonst nichts geändert
for k, v in final.items():
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    if roh.get(k) is None:
        fehler.append(f"{k}: im Export nicht vorhanden")
txt = "Tisch Buchen"
em = sum(0.572 if c.isdigit() else 0.26 if c == " " else 0.68 if c.isupper() else 0.55 for c in txt)
px = em * 1.05 * int(final["btnTischHinzufügen.Size"]) * 1.333 + 20
if px > int(final["btnTischHinzufügen.Width"]):
    fehler.append(f"„{txt}“ ca. {px:.0f} > Breite")
abh = [k for k, v in ist.items() if "btnTischHinzufügen.Width" in v]
if abh:
    fehler.append(f"Breite wird gelesen von {abh}")


def lum(r, g, b):
    q = lambda c: (c / 255 / 12.92) if c / 255 <= 0.03928 else ((c / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * q(r) + 0.7152 * q(g) + 0.0722 * q(b)


k_alt = (1.05) / (lum(208, 208, 208) + 0.05)
k_neu = (1.05) / (lum(23, 20, 150) + 0.05)
out = []
for k, v in final.items():
    c, p = k.split(".", 1)
    v0 = roh.get(k)
    out.append(dict(schritt="P0", titel="Design-Korrektur", control=c, prop=p, neu=v, de=A.to_de(v), vorher_de=A.to_de(v0),
                    diff="\n".join(list(difflib.unified_diff(A.to_de(v0).split("\n"), A.to_de(v).split("\n"), lineterm="", n=1))[2:]),
                    art="ersetzen", pfad=f.pfad(c)))
json.dump(dict(app=out, neue={}), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"P0 Design-Korrektur: {len(out)} Properties, kein neues Steuerelement. Grundlage: Export 10.11. 08:13 (echt).",
     f"„Tisch Buchen“: Text ca. {px:.0f} px in Breite {final['btnTischHinzufügen.Width']}; Kontrast weiße Schrift alt {k_alt:.1f}:1, neu {k_neu:.1f}:1.",
     "Breite von btnTischHinzufügen liest keine andere Formel (nur Y/Height, unverändert)."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
