# Design-Skizzen (10.11.2026): maßstabsgetreue Skizzen der neuen Bedienelemente in den vorhandenen Dialogen.
# Maße aus dem Export 10.11. (echt) und den Blöcken von „Für andere buchen“ v2 / Nachtrag 6 v2. KEIN Studio-Screenshot:
# Schrift ist Liberation Sans statt Open Sans (Breiten weichen um einige Prozent ab), Formelwerte sind von Hand aufgelöst.
# Aufruf: python3 -I werkzeuge/design_skizzen.py -> arbeit/2026-11-10_Abgestimmt/design/*.png
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-11-10_Abgestimmt/design")
os.makedirs(ZIEL, exist_ok=True)
S = 2   # Maßstab
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
BLAU, GRUEN, ROT, NAVY, GRAU = (23, 20, 150), (0, 169, 107), (235, 57, 81), (32, 54, 71), (247, 247, 247)
NEUF = (255, 140, 0)   # Markierung „neu“


def font(px, fett=False):
    return ImageFont.truetype(FB if fett else FR, int(px * S * 1.333))   # Power-Apps-Größe ist in Punkt


class Bild:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.im = Image.new("RGB", (w * S, h * S), bg)
        self.d = ImageDraw.Draw(self.im, "RGBA")

    def rect(self, x, y, w, h, fill=None, outline=None, r=0, bw=1, neu=False):
        box = [x * S, y * S, (x + w) * S, (y + h) * S]
        self.d.rounded_rectangle(box, radius=r * S, fill=fill, outline=outline, width=bw * S)
        if neu:
            self.d.rounded_rectangle([box[0] - 3 * S, box[1] - 3 * S, box[2] + 3 * S, box[3] + 3 * S], radius=r * S + 3 * S, outline=NEUF, width=S)

    def text(self, x, y, t, size=13, color=(0, 0, 0), fett=False, w=None, h=None, mitte=False):
        f = font(size, fett)
        for i, z in enumerate(t.split("\n")):
            tw = self.d.textlength(z, font=f)
            tx = x * S + ((w * S - tw) / 2 if (mitte and w) else 0)
            ty = y * S + (((h * S - len(t.split("\n")) * f.size * 1.2) / 2) if (mitte and h) else 0) + i * f.size * 1.2
            self.d.text((tx, ty), z, font=f, fill=color)

    def knopf(self, x, y, w, h, t, fill, color=(255, 255, 255), size=15, neu=False, rahmen=None):
        self.rect(x, y, w, h, fill=fill, outline=rahmen or tuple(max(0, int(c * 0.85)) for c in fill), r=10, bw=2, neu=neu)
        self.text(x, y, t, size, color, True, w, h, mitte=True)

    def eingabe(self, x, y, w, h, t, size=13, neu=False, hint=False):
        self.rect(x, y, w, h, fill=(255, 255, 255), outline=NAVY, bw=2, neu=neu)
        self.text(x + 8, y + (h - size * 1.6) / 2, t, size, (150, 150, 150) if hint else (0, 0, 0))

    def schalter(self, x, y, w, h, an, t, size=13, neu=False):
        pw = 44
        self.rect(x, y + (h - 22) / 2, pw, 22, fill=GRUEN if an else (200, 200, 200), r=11, neu=neu)
        kx = x + (pw - 18 - 2 if an else 2)
        self.d.ellipse([kx * S, (y + (h - 22) / 2 + 2) * S, (kx + 18) * S, (y + (h - 22) / 2 + 20) * S], fill=(255, 255, 255))
        self.text(x + pw + 8, y + (h - size * 1.6) / 2, t, size)

    def dialog(self, x, y, w, h, fill=(255, 255, 255)):
        self.d.rounded_rectangle([x * S + 3 * S, y * S + 4 * S, (x + w) * S + 3 * S, (y + h) * S + 4 * S], radius=16 * S, fill=(0, 0, 0, 40))
        self.rect(x, y, w, h, fill=fill, outline=(225, 225, 225), r=16)

    def speichern(self, name):
        self.im.save(os.path.join(ZIEL, name), optimize=True)


def beschriftung(b, t, y):
    b.text(10, y, t, 11, (90, 90, 90))


# 1) Buchungsdialog (800 x 350), „Für andere“ aus -> an ---------------------------------------------------------------------------
for an in (False, True):
    b = Bild(840, 400, (225, 225, 228))
    b.dialog(20, 20, 800, 350)
    ox, oy = 20, 20
    b.rect(ox, oy, 245, 278, fill=(236, 238, 242), r=16); b.text(ox + 40, oy + 120, "Tischfoto", 13, (150, 150, 150))
    b.rect(ox + 245, oy, 1, 350, fill=(210, 210, 210))
    b.text(ox + 270, oy + 15, "Matthäus-Merian-Strasse 6 / Lohfelden  MMS Untergeschoss", 13)
    b.text(ox + 270, oy + 50, "UG Desk 5", 20)
    b.eingabe(ox + 448, oy + 60, 328, 40, "30.11.2026")
    b.eingabe(ox + 448, oy + 122, 328, 40, "09:00")
    b.eingabe(ox + 448, oy + 186, 328, 40, "10:00")
    b.rect(ox + 448, oy + 240, 18, 18, outline=NAVY, bw=2); b.text(ox + 474, oy + 238, "Wiederholen", 13)
    b.knopf(ox + 448, oy + 293, 160, 40, "Abbrechen", (0, 0, 0))
    b.knopf(ox + 616, oy + 293, 160, 40, "Speichern", BLAU)
    b.schalter(ox + 270, oy + 128, 165, 28, an, "Für andere" if an else "Für mich", neu=True)
    if an:
        b.eingabe(ox + 270, oy + 186, 165, 40, "Max Mustermann", neu=True)
    beschriftung(b, "Buchungsdialog (800 × 350). Orange = neu. Mittlere Spalte: Schalter in Reihe von „Beginn“, Name in Reihe von „Ende“.", 378)
    b.speichern(f"1_buchungsdialog_{'an' if an else 'aus'}.png")

# 2) Panel „Tisch buchen“ (470 x 678) --------------------------------------------------------------------------------------------------
b = Bild(510, 720, (225, 225, 228))
b.dialog(20, 20, 470, 678, GRAU)
ox, oy = 20, 20
b.text(ox + 75, oy + 45, "Tisch Buchen", 17, (0, 0, 0), True)
b.knopf(ox + 25, oy + 45, 40, 40, "<", BLAU)
b.eingabe(ox + 80, oy + 100, 350, 40, "30.11.2026", 14)
b.eingabe(ox + 80, oy + 160, 240, 40, "09:00"); b.knopf(ox + 350, oy + 160, 80, 40, "5 Std", (150, 220, 190), (0, 0, 0), 15)
b.eingabe(ox + 80, oy + 220, 240, 40, "10:00"); b.knopf(ox + 350, oy + 220, 80, 40, "9 Std", (150, 220, 190), (0, 0, 0), 15)
b.eingabe(ox + 80, oy + 280, 350, 40, "UG Desk 5")
b.rect(ox + 80, oy + 335, 18, 18, outline=NAVY, bw=2); b.text(ox + 106, oy + 333, "Wiederholen", 13)
for i, t in enumerate(["Mo", "Di", "Mi", "Do", "Fr"]):
    b.schalter(ox + 338, oy + 331 + i * 38, 92, 28, i < 2, t)
b.eingabe(ox + 80, oy + 380, 200, 40, "14.12.2026")
b.schalter(ox + 80, oy + 531 + 6, 165, 28, True, "Für andere", neu=True)
b.eingabe(ox + 255, oy + 531, 175, 40, "Max Mustermann", neu=True)
b.knopf(ox + 270, oy + 591, 160, 40, "Speichern", BLAU, neu=False)
beschriftung(b, "Panel (470 × 678, mit „Wiederholen“ an). Neue Zeile unten, „Speichern“ rückt von Y 531 auf Y 591.", 702)
b.speichern("2_panel.png")

# 3) Hinweisdialog (580 x 300) über abgedunkeltem Bildschirm ----------------------------------------------------------------------
b = Bild(1000, 560, (240, 240, 242))
b.rect(20, 20, 470, 520, fill=GRAU, r=16); b.rect(500, 20, 480, 520, fill=(236, 236, 238), r=16)
b.rect(0, 0, 1000, 560, fill=(0, 0, 0, 102))
b.dialog(210, 140, 580, 280)
b.text(230, 160, "Zur selben Zeit schon gebucht", 17, (0, 0, 0), True)
b.text(230, 210, "Du hast zu dieser Zeit schon einen Tisch gebucht. Trotzdem einen\nweiteren Tisch buchen?\n\nFragen: Axel Krägelius (PC-Admin) oder Norman Horn (Admin, NHN IT).", 13, (50, 49, 48))
b.knopf(230, 360, 260, 40, "Abbrechen", (0, 0, 0))
b.knopf(510, 360, 260, 40, "Trotzdem buchen", BLAU)
b.text(10, 540, "Hinweisdialog (580 × 280), Hintergrund wie die Ladeanzeige (Schwarz 40 %), Stil von Details-Popup und Speichern/Abbrechen.", 11, (255, 255, 255))
b.speichern("3_hinweisdialog.png")

# 4) Details-Popup der Kachel (400 x 154) ohne und mit Gast ---------------------------------------------------------------------------
for gast in (False, True):
    b = Bild(440, 200, (225, 225, 228))
    b.dialog(20, 20, 400, 154)
    ox, oy = 20, 20
    b.rect(ox + 256, oy, 144, 154, fill=(236, 238, 242), r=16); b.rect(ox + 256, oy, 1, 154, fill=(210, 210, 210))
    b.text(ox + 25, oy + 10, "Tisch: UG Desk 5", 13, (0, 0, 0))
    b.text(ox + 25, oy + 45, "Gebucht", 13, (255, 165, 0))
    if gast:
        b.text(ox + 25, oy + 71, "Max Mustermann\ngebucht von Josias Semeraf", 11, (0, 0, 0))
        b.text(ox + 25, oy + 118, "09:00 – 10:00", 13)
    else:
        b.text(ox + 25, oy + 71, "Josias Semeraf", 13)
        b.text(ox + 25, oy + 100, "09:00 – 10:00", 13)
    b.knopf(ox + 378, oy + 2, 20, 20, "x", (0, 0, 0), size=10)
    beschriftung(b, "Details-Popup, " + ("mit Gast (Zeitzeile rückt auf Y 118)" if gast else "heute"), 182)
    b.speichern(f"4_popup_{'gast' if gast else 'heute'}.png")

# 5) Dashboard-Karte (470 x 104): normal, mit Gast, „Neu buchen“ bei verfallener Buchung -------------------------------------------------
b = Bild(510, 400, (225, 225, 228))
b.rect(20, 20, 470, 360, fill=GRAU, r=16)
for i, (gast, status, neu_btn) in enumerate([(False, ("Einchecken", (255, 165, 0)), False), (True, ("Eingecheckt", GRUEN), False), (False, None, True)]):
    y0 = 40 + i * 104
    b.rect(35, y0 + 10, 440, 84, fill=(255, 255, 255), outline=(230, 230, 230), r=16)
    b.rect(60, y0 + 30, 50, 50, fill=(236, 238, 242), r=8)
    ty = y0 + (21 if gast else 27)
    b.text(120, ty, "Tisch UG Desk 5", 14, (50, 49, 48))
    b.text(120, ty + 25, "09:00 – 10:00" + ("\nfür Max Mustermann" if gast else ""), 12)
    if status:
        b.text(290, y0 + 43, status[0], 13, status[1])
    if neu_btn:
        b.knopf(290, y0 + 48, 120, 32, "Neu buchen", BLAU, size=12, neu=True)
    b.rect(425, y0 + 30, 40, 40, outline=NAVY, r=8)
beschriftung(b, "Dashboard-Karten (Breite 470): normal · Gast (zweite Zeile) · verfallen mit „Neu buchen“ (Nachtrag 6).", 384)
b.speichern("5_dashboard_karten.png")
print("Skizzen:", sorted(os.listdir(ZIEL)))
