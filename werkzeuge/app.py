# Gemeinsame Bibliothek: Export entpacken, Properties lesen, deutsche Schreibweise, Prüfungen.
# Nur lesen. Nie packen. Aufruf der Werkzeuge mit `python3 -I`.
import io, json, os, re, sys, zipfile
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_DESKTOP = os.path.join(REPO, "quellen/2026-10-07_Wissenspaket/02_EXPORT_UND_TRACES/"
                              "TischbuchungApp07.10.2026verbesserunganalyse_20261007091458.zip")
EXPORT_HANDY = os.path.join(REPO, "quellen/2026-10-07_Wissenspaket/02_EXPORT_UND_TRACES/"
                            "HandyTischbuchung_Export_2026-10-07.zip")
ENTPACKT = os.path.join(REPO, "arbeit/_entpackt")


def entpacke(zip_pfad, name):
    """zip -> *.msapp -> Ordner. Backslash-Pfade im msapp werden zu Ordnern."""
    ziel = os.path.join(ENTPACKT, name)
    if os.path.isdir(os.path.join(ziel, "Src")):
        return ziel
    os.makedirs(ziel, exist_ok=True)
    with zipfile.ZipFile(zip_pfad) as z:
        msapp = [n for n in z.namelist() if n.endswith(".msapp")]
        assert len(msapp) == 1, msapp
        daten = z.read(msapp[0])
    with zipfile.ZipFile(io.BytesIO(daten)) as m:
        for n in m.namelist():
            pfad = os.path.join(ziel, *n.replace("\\", "/").split("/"))
            os.makedirs(os.path.dirname(pfad), exist_ok=True)
            with open(pfad, "wb") as f:
                f.write(m.read(n))
    return ziel


class App:
    """Steuerelemente mit Eltern, Typ und Properties (englische Schreibweise, ohne führendes '=')."""

    def __init__(self, ordner):
        self.props = {}      # "Ctrl.Prop" -> Formel (englisch, ohne '=')
        self.eltern = {}     # Ctrl -> Eltern-Ctrl
        self.typ = {}        # Ctrl -> Control-Typ
        self.reihenfolge = []
        src = os.path.join(ordner, "Src")
        app = yaml.load(open(os.path.join(src, "App.pa.yaml"), encoding="utf-8"), Loader=yaml.BaseLoader)
        self._props("App", app["App"].get("Properties", {}))
        self.typ["App"] = "App"
        for datei in sorted(os.listdir(src)):
            if datei in ("App.pa.yaml", "_EditorState.pa.yaml") or not datei.endswith(".pa.yaml"):
                continue
            d = yaml.load(open(os.path.join(src, datei), encoding="utf-8"), Loader=yaml.BaseLoader)
            for sname, sbody in d["Screens"].items():
                self.typ[sname] = "Screen"
                self.reihenfolge.append(sname)
                self._props(sname, sbody.get("Properties", {}))
                self._walk(sbody.get("Children"), sname)

    def _props(self, ctrl, props):
        for p, v in (props or {}).items():
            assert v.startswith("="), (ctrl, p, v[:40])
            self.props[f"{ctrl}.{p}"] = v[1:]

    def _walk(self, kinder, eltern):
        for k in kinder or []:
            for name, body in k.items():
                self.eltern[name] = eltern
                self.typ[name] = body.get("Control", "?")
                self.reihenfolge.append(name)
                self._props(name, body.get("Properties", {}))
                self._walk(body.get("Children"), name)

    def get(self, ctrl, prop):
        return self.props[f"{ctrl}.{prop}"]

    def pfad(self, ctrl):
        p = [ctrl]
        while p[-1] in self.eltern:
            p.append(self.eltern[p[-1]])
        return " > ".join(reversed(p))

    def suche(self, muster):
        """Alle Properties, deren Formel den regulären Ausdruck enthält."""
        r = re.compile(muster)
        return [k for k, v in self.props.items() if r.search(v)]


def lade_desktop():
    return App(entpacke(EXPORT_DESKTOP, "desktop_2026-10-07"))


def lade_handy():
    return App(entpacke(EXPORT_HANDY, "handy_2026-10-07"))


EXPORT_HANDY_0810 = os.path.join(REPO, "quellen/2026-10-08_HandyExport/handyappAnalyse8.10.26_20261008115132.zip")


def lade_handy_0810():
    return App(entpacke(EXPORT_HANDY_0810, "handy_2026-10-08"))


EXPORT_DESKTOP_FERTIG = os.path.join(REPO, "quellen/2026-10-08_Fertig/PCAppfertig_20261008142626.zip")
EXPORT_HANDY_FERTIG = os.path.join(REPO, "quellen/2026-10-08_Fertig/HandyApp8.10.fertig_20261008142545.zip")


def lade_desktop_fertig():
    return App(entpacke(EXPORT_DESKTOP_FERTIG, "desktop_2026-10-08_fertig"))


def lade_handy_fertig():
    return App(entpacke(EXPORT_HANDY_FERTIG, "handy_2026-10-08_fertig"))


def _string_ende(f, i):
    ch = f[i]
    j = i + 1
    while j < len(f):
        if f[j] == ch:
            if j + 1 < len(f) and f[j + 1] == ch:
                j += 2
                continue
            return j
        j += 1
    raise ValueError("offene Zeichenkette bei %d" % i)


def to_de(f, kommentare=False):
    """Englische -> deutsche Schreibweise. Zeichenketten und '...' bleiben unangetastet.
    kommentare=True: // bis Zeilenende unverändert übernehmen (nur für App.Formulas)."""
    out = []
    i, n = 0, len(f)
    while i < n:
        ch = f[i]
        if ch in "\"'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
            continue
        if f.startswith("//", i):
            if not kommentare:
                raise ValueError("Kommentar in Formel")
            j = f.find("\n", i)
            j = n if j < 0 else j
            out.append(f[i:j])
            i = j
            continue
        if ch == ";":
            out.append(";;")
        elif ch == ",":
            out.append(";")
        elif ch == "." and i > 0 and f[i - 1].isdigit() and i + 1 < n and f[i + 1].isdigit():
            k = i - 1
            while k >= 0 and f[k].isdigit():
                k -= 1
            out.append("," if (k < 0 or not (f[k].isalnum() or f[k] == "_")) else ".")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def from_de(f, kommentare=False):
    """Deutsche -> englische Schreibweise (Gegenstück zu to_de, für Prüfungen)."""
    out = []
    i, n = 0, len(f)
    while i < n:
        ch = f[i]
        if ch in "\"'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
            continue
        if kommentare and f.startswith("//", i):
            j = f.find("\n", i)
            j = n if j < 0 else j
            out.append(f[i:j])
            i = j
            continue
        if f.startswith(";;", i):
            out.append(";")
            i += 2
            continue
        if ch == ";":
            out.append(",")
        elif ch == "," and i > 0 and f[i - 1].isdigit() and i + 1 < n and f[i + 1].isdigit():
            out.append(".")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def ausserhalb_strings(f):
    """Formel mit geleerten Zeichenketten (für Namens- und Klammerprüfungen)."""
    out = []
    i, n = 0, len(f)
    while i < n:
        if f[i] == '"':
            j = _string_ende(f, i)
            out.append('""')
            i = j + 1
        elif f[i] == "'":
            j = _string_ende(f, i)
            out.append(f[i:j + 1])
            i = j + 1
        else:
            out.append(f[i])
            i += 1
    return "".join(out)


def klammern_ok(f):
    s = ausserhalb_strings(f)
    paare = {")": "(", "}": "{", "]": "["}
    stapel = []
    for ch in s:
        if ch in "({[":
            stapel.append(ch)
        elif ch in paare:
            if not stapel or stapel[-1] != paare[ch]:
                return False
            stapel.pop()
    return not stapel


def ws(s):
    return re.sub(r"\s+", "", s)


if __name__ == "__main__":
    a = lade_desktop()
    print(len(a.props), "Properties,", len(a.typ), "Steuerelemente")


EXPORT_DESKTOP_1210 = os.path.join(REPO, "quellen/2026-10-12_Desktop/TischbuchungDesktop12.10.2026Einchecken_20261012072631.zip")


def lade_desktop_1210():
    return App(entpacke(EXPORT_DESKTOP_1210, "desktop_2026-10-12"))


EXPORT_DESKTOP_1210B = os.path.join(REPO, "quellen/2026-10-12_TischZeigen/Tischbuchung12.10.Grundrissemachen_20261012115225.zip")
EXPORT_HANDY_1210 = os.path.join(REPO, "quellen/2026-10-12_TischZeigen/handytischbuchungegrundrisseinbauen12.10._20261012120337.zip")


def lade_desktop_1210b():
    return App(entpacke(EXPORT_DESKTOP_1210B, "desktop_2026-10-12b"))


def lade_handy_1210():
    return App(entpacke(EXPORT_HANDY_1210, "handy_2026-10-12"))


# Achtung: EXPORT_HANDY_1210 („handytischbuchungegrundrisseinbauen“) enthält die Desktop-App (belegt). Echter Handy-Export:
EXPORT_HANDY_1210_ECHT = os.path.join(REPO, "quellen/2026-10-12_TischZeigen/handyecht12.10._20261012120559.zip")


def lade_handy_1210_echt():
    return App(entpacke(EXPORT_HANDY_1210_ECHT, "handy_2026-10-12_echt"))


EXPORT_DESKTOP_1310 = os.path.join(REPO, "quellen/2026-10-13_Desktop/TischbuchungApp13.10.2026959_20261013075948.zip")


def lade_desktop_1310():
    return App(entpacke(EXPORT_DESKTOP_1310, "desktop_2026-10-13"))


EXPORT_DESKTOP_1910 = os.path.join(REPO, "quellen/2026-10-19_HeuteButton/TischbuchungHeutebutton_20261019103505.zip")


def lade_desktop_1910():
    return App(entpacke(EXPORT_DESKTOP_1910, "desktop_2026-10-19"))


EXPORT_DESKTOP_2510 = os.path.join(REPO, "quellen/2026-10-25_Desktop/Tischbuchungsapp25.10.26_20261025200901.zip")


def lade_desktop_2510():
    return App(entpacke(EXPORT_DESKTOP_2510, "desktop_2026-10-25"))
