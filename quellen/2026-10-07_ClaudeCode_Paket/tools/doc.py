# Erzeugt aus out.json die Übergabe UEBERGABE_Grundriss_L2_v0.3.md. Aufruf im Ordner mit out.json: python3 -I tools/doc.py
import json
R=json.load(open("out.json"))
A=[r for r in R if r["step"] in (1,3)]
B=[r for r in R if r["step"]==2]
LADE=[r for r in R if r["control"]=="dpAnsichtsDatum"][0]["de"].split(";;\n",1)[1]
def block(r, orig=False):
    return f"**`{r['control']}.{r['prop']}`**" + (f" – {r['note']}" if r['note'] and not orig and r['step']==2 else "") + "\n\n```\n" + (r["orig_de"] if orig else r["de"]) + "\n```\n"
o=[]
w=o.append
w("""# ÜBERGABE Tischbuchung: Grundriss-Performance (L2)
**Entwurf v0.3 · 06.10.2026 · online gegengeprüft (Abschnitt 9) · unabhängig geprüft, Befunde eingearbeitet (Abschnitt 10) · noch nichts davon eingefügt**

## 0. Auftrag (für den Claude, der das übernimmt)
Die Tischbuchungs-App ist beim Speichern langsam; bei Serienbuchungen hängt sie minutenlang. Ursache ist **gemessen**: Die Grundriss-Kacheln fragen SharePoint je Tisch 6× einzeln ab und tun das nach **jedem** Schreibvorgang neu. Lösung L2: Die Kacheln lesen aus einer Collection `colGrundriss`, die an 15 festen Stellen mit **einer** Abfrage geladen wird. Josias fügt jede Formel selbst in Power Apps Studio ein (deutsche Schreibweise). Alle Formeln unten sind **vollständige Properties**, maschinell aus seinem Export vom 06.10.2026 erzeugt (App „Tischbuchung“, Stand 05.10. 11:58 UTC).

**Entscheidungen (vorläufig, Josias bestätigt noch):**
- Kein Timer für Live-Farben (Verhalten wie heute).
- Alle vorhandenen `Refresh(Tischbuchungen)` bleiben; die Ladezeile kommt **dazu** (kleinste Änderung).
- L3, L4, K1 und das Entfernen der Mehrfachauswahl sind **nicht** Teil dieser Übergabe (Abschnitt 8).

**Voraussetzung:** Die Formeln basieren auf dem **veröffentlichten** Stand vom 05.10.2026, 13:58 Uhr. Wurde seitdem in Studio etwas gespeichert, würden diese Änderungen beim Ersetzen der ganzen Property still überschrieben. Dann zuerst einen neuen Export erstellen und die Formeln neu erzeugen lassen.

## 1. Messbefunde (Livemonitor, veröffentlichte App, ein Nutzer, OG mit 16 Tischen)
| Vorgang | Abfragen | Dauer | Quelle |
|---|---|---|---|
| App-Start | ~150 (davon ~102 Grundriss, 36 Raumcode) | Netz ruhig nach 2,5–3,4 s | Messung 1 + 2 |
| Aktualisieren-Knopf | 103 (1 Grundriss-Welle) | 1,7 s | Messung 1 |
| Einzelbuchung (Tische-Panel) | 190 (2 Grundriss-Wellen) | 2,6–4,6 s | Messung 1 |
| Serie 11 Termine (Grundriss-Dialog, Sammel-Patch) | 1.020 (12 Wellen = 11 Schreibvorgänge + 1 Refresh) | **~101 s** vom Klick bis zur letzten Antwort; Antwortzeit Median 31 s, max 97 s; 95 % der Abfragen nach 3,7 s abgeschickt, danach Stau; kein 429 | Messung 2 |

Hinweis zur Auswertung: Im Monitor-JSON ist `time` das **Ende** einer Antwort (`time` = `response.endTime`), nicht der Beginn.

- Das Speichern selbst ist schnell: Kollisionsabfrage 0,2–1,7 s, `createRow` 0,25–0,47 s; Serie: 11 `createRow` zusammen ca. 1,6 s, gestaffelt. **gemessen**
- Je Kachel 6 Abfragen: `Rectangle1.Fill`, `Circle1.Fill`, `Circle1.BorderColor`, `Label1.Text` (4× **dieselbe** Bedingung) + 2× `Circle1.BorderStyle`. `Now()` steht in jeder URL, deshalb wird nichts wiederverwendet. **Code + gemessen**
- Jeder einzelne Schreibvorgang löst eine volle Grundriss-Welle aus, auch beim Sammel-Patch. **gemessen** (jede Kachel-Property genau 12× bei 11 Terminen)

## 2. Korrekturen am bisherigen Briefing (belegt)
| Briefing sagte | Tatsächlich | Beleg |
|---|---|---|
| `ddEndeTischePanel` | heißt **`ddEndTischePanel`** | Export |
| Sammel-Patch braucht evtl. `'@odata.type'` für Person/Tisch | **nicht nötig**: alle 11 Datensätze mit korrekter Person und Tisch angelegt | SharePoint-Antworten in Messung 2 |
| Sammel-Patch spart keine Aufrufe / ist ein Aufruf | **11 einzelne `createRow`**, gestaffelt und überlappend (höchstens 5 gleichzeitig; IDs in anderer Reihenfolge als die Daten), zusammen ca. 1,6 s | Messung 2 |
| Serie max. 14 Termine | Fenster ist Start + 14 Tage = **15 Tage** (06.–20.10. ergab 11 Werktage) | Messung 2 |
| Raumcode ist tot | ist unsichtbar, **lädt aber beim Start 36× `Raumbuchungen`**. Unsichtbar heißt nicht „nicht berechnet“ | Messung 1 |
| `btnVerwalten_2` (K1) offen | weiterhin **nicht** eingebaut, B0 aktiv | Export |
| keine Kommentare in Formeln | gilt für Verhaltensformeln; `App.Formulas` enthält `//` und läuft | Export |
| – | Unsichtbarer Grundriss-Verwalten-Dialog (`btnPlus3Std`) lädt bei leerer `varSelectedBuchung` die **ganze Liste** (249–251 Zeilen, 286 KB) je Aktualisierung | Messung 1 |

## 3. Lösung L2: Prinzip und Abgrenzung
- Neue Collection **`colGrundriss`** mit flachen Spalten `TischName`, `Startzeit`, `Endzeit`, `Eingecheckt`, `Name`. Inhalt, **beide Stockwerke**: alle Buchungen, die den angezeigten Tag (`varAnsichtsDatum`) überlappen, **oder** die von jetzt bis +60 min laufen. Der zweite Teil ist nötig, weil `Circle1.BorderColor` immer „jetzt“ prüft, auch wenn ein anderer Tag angezeigt wird, und weil sonst heute zwischen 23 und 24 Uhr Buchungen nach Mitternacht fehlen. Durch `Now()` ist außerdem jede Abfrage-URL eindeutig, ein Zwischenspeicher kann also keine veralteten Daten liefern. Eine delegierte Abfrage (`and`, `or`, `gt`, `lt` delegierbar laut Spaltenmetadaten).
- Die 5 Kachel-Properties lesen aus `colGrundriss`, die Bedingungen bleiben **1:1** gleich.
- **Bleibt bewusst an SharePoint, NICHT ändern:**
  - `btnHitArea.OnSelect` (Klick auf Kachel): entscheidet mit frischen Serverdaten und liefert den echten Datensatz für `varSelectedBuchung` (Patch-Regel, Typ-Regel).
  - Kollisionsprüfungen in beiden Speichern-Knöpfen.
  - Listen `galTischbuchungenHeute`, `galAlleTischbuchungen`.
  - Alle `Refresh(Tischbuchungen)`.
- Folge: Eine veraltete Kachelfarbe kann **keine** Doppelbuchung verursachen. Klick und Speichern prüfen am Server.

**Die Ladezeile** (an allen 15 Stellen identisch). Sie lädt erst in einen Zwischenwert `neu` und ersetzt `colGrundriss` **nur bei Erfolg**. Hintergrund: Bei einem fehlgeschlagenen Laden kann Power Apps einen Fehlerdatensatz in die Collection schreiben (Abschnitt 9). So bleibt bei Netzfehlern der alte Stand stehen, und es kommt ein Hinweis statt einer rohen Fehlermeldung.
```
""" + LADE + """
```

## 4. Einbau
Vorher Versionsverlauf prüfen (siehe Voraussetzung in Abschnitt 0) und `.msapp` exportieren. In **Studio** testen (Livemonitor aus Studio, nicht über make.powerapps.com, sonst muss veröffentlicht werden). Erst nach Schritt B veröffentlichen.

### Schritt A: 15 Ladestellen (unsichtbar, harmlos)
Der Grundriss liest danach noch aus SharePoint. Die App verhält sich gleich, es kommt nur 1 Abfrage pro Anlass dazu.

In `App.OnStart` steht die Ladezeile **ganz am Ende**, damit Stockwerk und Tischpositionen nicht auf die Abfrage warten.

| Anlass | Steuerelement.Property |
|---|---|
""")
LAB={"App":"App-Start","dpAnsichtsDatum":"Datum wechseln","ddStockwerk":"Stockwerk wechseln (neu, hält Fremdbuchungen aktuell wie heute)",
"Icon1":"Aktualisieren (hinter Refresh)","Icon1_1":"Aktualisieren (hinter Refresh)","Image6":"Logo-Klick = Aktualisieren (hinter Refresh)","btnHitArea_1":"Aktualisieren (hinter Refresh)",
"btnSpeichern":"Buchen, Grundriss-Dialog (hinter Refresh)","btnSpeichernTischePanel":"Buchen, Tische-Panel (hinter Refresh)","btnVerlängern_1":"Verlängern, Tab (hinter Refresh)",
"btnStornieren_1":"Stornieren, Tab (hinter Refresh)","btnStornierenKlein":"Stornieren, Mehrfachauswahl (hinter Refresh)","btnVerlängern":"Verlängern, Grundriss (ans Ende, hat kein Refresh)",
"btnStornieren":"Stornieren, Grundriss (ans Ende, hat kein Refresh)","btnEinchecken":"Ein-/Auschecken (ans Ende, hat kein Refresh)"}
for r in A: w(f"| {LAB[r['control']]} | `{r['control']}.{r['prop']}` |\n")
w("\n")
for r in A: w(block(r))
w("""
**Test A**
1. App-Prüfung: keine neuen Fehler.
2. In Studio `OnStart` einmal ausführen (Strukturansicht → App → … → „OnStart ausführen“), denn die Vorschau startet `OnStart` nicht neu. Dann Variablen-Ansicht (links: Variablen → Collections → `colGrundriss`): enthält die Buchungen von heute aus **beiden** Stockwerken.
3. Datum wechseln: `colGrundriss` zeigt den neuen Tag.
4. Livemonitor: genau **1** Abfrage auf `Tischbuchungen` mit `$filter` aus `Endzeit`/`Startzeit` und `or`, ausgelöst von `App.OnStart`. Ein gelbes Delegationsdreieck an `ForAll` in Studio ist kein Beweis für ein Problem; entscheidend ist die URL im Monitor. Vorher den Stand der App-Prüfung notieren, damit neue Fehler erkennbar sind.
5. Einzelbuchung, Verlängern (Grundriss und Tab), Stornieren (Grundriss, Tab, mehrfach), Einchecken je einmal: alles wie vorher, keine Warnung „Grundriss konnte nicht…“.

### Schritt B: Kacheln umstellen (die eigentliche Änderung)
""")
for r in B: w(block(r))
w("""
**Test B** (heute, dann ein anderer Tag, dann UG)
0. In Studio `OnStart` ausführen (wie Test A2), sonst sind die Kacheln grün.
1. Farben und Kürzel identisch mit vorher: grün frei, orange gebucht, rot eingecheckt; Kreisrand bei besetzt/bald besetzt.
2. Einzelbuchung → Kachel wechselt **sofort** die Farbe.
3. Verlängern, Stornieren, Einchecken (Grundriss und Tab) → Kachel stimmt danach.
4. Zweiter Nutzer/Tab bucht → erscheint nach Aktualisieren, Datum- oder Stockwerkwechsel (wie heute).
5. Livemonitor, Erwartung (geschlussfolgert, zu messen):

| Vorgang | heute | erwartet |
|---|---|---|
| App-Start Grundriss | ~102 | 1 (App-Start gesamt ~49, davon 36 Raumcode bis L4) |
| Aktualisieren | 103 | ~8 |
| Einzelbuchung | 190 | ~15 |
| Serie 11 Termine | 1.020 | ~45 |

## 5. Rückfall
- Schritt B rückgängig: die 5 Kachel-Properties durch die Originale in Anhang 1 ersetzen. Die Ladestellen aus Schritt A dürfen bleiben (harmlos).
- Komplett: letzten `.msapp`-Export importieren oder Versionsverlauf der App.

## 6. UNSICHER (mit Prüftest)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U1 | Ob die Prüfung `IsError(neu) || IsError(First(neu))` einen Netzfehler zuverlässig erkennt (Fehler kann als ganzer Wert oder als Fehlerdatensatz kommen) | Grundriss zeigt alten Stand oder Fehler; Klick/Speichern prüfen trotzdem am Server | WLAN aus, Aktualisieren tippen: erwartet Hinweis „Grundriss konnte nicht…“, Farben bleiben |
| U2 | Ob die Filterbedingung wirklich als **eine** delegierte Abfrage rausgeht | sonst gelbes Delegationsdreieck und lokale Filterung (bis Datenzeilenlimit) | Test A4 im Monitor |
| U3 | `usenonblockingonstartrule` ist an: Grundriss kann beim Start kurz grün zeigen, bis `colGrundriss` geladen ist | kosmetisch | App-Start beobachten |
| U4 | Ob `If(…; Notify(…); ClearCollect(…))` (unterschiedliche Rückgabetypen in den Zweigen) bei `powerfxv1 = false` ohne Fehler akzeptiert wird. Die App mischt das schon heute (z. B. `btnStornierenKlein`) | rote Formel beim Einfügen | App-Prüfung nach Schritt A |
| U7 | Nach der Ladezeile zeigen die 4 Aktualisieren-Knöpfe „Aktualisiert.“; das könnte die Warnung „Grundriss konnte nicht…“ überdecken | Warnung übersehen | bei Test U1 auf beide Meldungen achten |
| U8 | Bei sehr schnellem Datumswechsel können zwei Ladezeilen gleichzeitig laufen; die zuletzt fertige gewinnt | Grundriss zeigt kurz den falschen Tag; Klick/Speichern prüfen am Server; Aktualisieren behebt es | hinnehmen für Go-Live |
| U9 | Datenzeilenlimit 1000 oder 2000 (Abfragen gehen mit `$top=1000` raus) | unkritisch, ein Tag hat ≪ 1000 Buchungen | – |
| U5 | UG nicht gemessen (18 Tische lt. `TischNrUG`) | – | Test B im UG |
| U6 | Mehrere Nutzer gleichzeitig nicht gemessen | – | nach Go-Live beobachten |

## 7. Regeln (aus dem Projekt)
Deutsche Schreibweise (`;` trennt, `;;` verkettet). Keine Kommentare in Verhaltensformeln. Immer die ganze Property ersetzen. Die zwei Speichern-Knöpfe sind nicht wortgleich: jeden einzeln einfügen. Nur ein Studio-Fenster.

## 8. Danach (nicht Teil dieser Übergabe)
- **L3** Versteckte Dialoge nur rechnen lassen, wenn offen (beseitigt das Laden der ganzen Liste durch `btnPlus3Std` und die `eq null`-Abfragen).
- **L4** Raumcode stilllegen (Start −36 Abfragen, darunter die langsamsten).
- **K1** `Set(varSelectedBuchung; ThisItem)` in `btnVerwalten_2` (stille Doppelbuchung B0).
- Mehrfachauswahl zum Go-Live ausblenden (Josias’ Idee, zu bestätigen).
- Serienbuchung: Nachlese über `SerienID` (bisher nicht geschrieben) für ehrliche Meldungen; Panel-Knopf noch auf alter Schleife.

## 9. Online-Prüfung der tragenden Annahmen
| Annahme | Status | Quelle |
|---|---|---|
| Eine `LookUp` in einer Galerie-Vorlage erzeugt einen eigenen Konnektor-Aufruf **pro Zeile** | **belegt** (Fachblog) + **gemessen** (6 je Kachel) | Devaney, Performance Guidelines |
| Daten in Collections zwischenspeichern ist ein empfohlenes Muster; „alles in Collections“ ist ein Anti-Muster | **belegt** | Microsoft Learn, Performance-Übersicht |
| `Now()` wird nur neu berechnet, wenn sich in derselben Formel etwas anderes ändert | **belegt**: deshalb ändert L2 nichts an der Aktualität der „jetzt“-Farben | Microsoft Learn, Now/Today |
| Nicht blockierendes `OnStart` (bei dir an) läuft parallel zu den Bildschirm-Formeln | **belegt**: Grundriss kann beim Start kurz grün sein (U3) | Microsoft Learn, App-Objekt |
| SharePoint: 600 Aufrufe pro **Verbindung** pro 60 s; die Verbindung ist **pro Nutzer** | **belegt** | Microsoft Learn, SharePoint-Konnektor |
| `Startzeit`/`Endzeit` mit `<`/`>` sind an SharePoint delegierbar | **belegt** + Spaltenmetadaten im Export | Microsoft Learn, SharePoint-Verbindung |
| `ClearCollect` selbst ist nicht delegierbar, holt höchstens das Datenzeilenlimit | **belegt**; unkritisch, ein Tag hat ≪ 2000 Buchungen | Microsoft Learn, Clear/Collect |
| Fehlgeschlagenes Laden kann einen **Fehlerdatensatz in die Collection** schreiben | **belegt** (Microsoft-Mitarbeiter in der Community), Verhalten evtl. inzwischen geändert | Power Apps Community, Error Handling |
| Fehler beim Lesen können als einzelne Fehlerdatensätze in einer Tabelle stehen | **belegt** | Microsoft Learn, Error handling |
| Unsichtbare Steuerelemente werden trotzdem berechnet und fragen Daten ab | **gemessen** (Raumcode, `btnPlus3Std`); keine offizielle Doku gefunden | Messung 1 |
| Jeder Schreibvorgang löst eine Neuberechnung aller abhängigen Formeln aus | **gemessen**; keine offizielle Doku gefunden | Messung 2 |

**Geprüfte und verworfene Alternative: benannte Formel statt Collection** (`App.Formulas`, z. B. `GrundrissTag = ForAll(Filter(Tischbuchungen; …); …)`).
- Vorteil: keine 15 Ladestellen, aktualisiert sich laut Microsoft selbst, wenn sich die Daten ändern.
- Verworfen für den Go-Live, weil: Es gibt ein bekanntes, von Microsoft bestätigtes Problem, dass der Zwischenspeicher nicht aktualisiert wird, wenn sich abhängige Variablen ändern (hier `varAnsichtsDatum`); ob es behoben ist, ist nicht dokumentiert. Außerdem ist nicht steuerbar, wann sie neu abfragt (vermutlich nach **jedem** Schreibvorgang, bei der Serie also 11-mal). Kandidat für nach dem Go-Live.

## 10. Unabhängige Prüfung (v0.2) und Umsetzung
Geprüft von einem separaten Agenten ohne Kenntnis der Herleitung, gegen Export, beide Messdateien und Briefing. Urteil: einfügebereit nach Korrekturen; kein blockierender Fehler. Geprüft und ok: Vollständigkeit der Ladestellen (alle 8 Schreibstellen, alle 9 Refresh, alle Datums- und Stockwerkwechsel; `Gallery1` ist die einzige Grundriss-Galerie), deutsche Umwandlung, Klammerung, Steuerelementnamen, Anhang = Original, `CheckedIn`/`Checkedin`, keine Typkonflikte mit `varSelectedBuchung`.
| Befund | Umsetzung in v0.3 |
|---|---|
| 1 Ladezeile mitten in `OnStart` blockiert Stockwerk und Tischpositionen | ans Ende von `OnStart` verschoben |
| 2 Dauern doppelt gezählt (`time` = Antwortende) | Abschnitt 1 und 2 korrigiert (selbst nachgeprüft) |
| 3 `Circle1.BorderColor` prüft immer „jetzt“; Lücke 23–24 Uhr | Ladefilter um „jetzt bis +60 min“ erweitert (`or`, delegierbar, selbst nachgeprüft) |
| 4 Gleiche URL bei Datums-/Stockwerkwechsel evtl. aus Zwischenspeicher | durch `Now()` im Filter erledigt |
| 5 Export ist der veröffentlichte Stand | Voraussetzung in Abschnitt 0 |
| 6 Studio-Vorschau führt `OnStart` nicht neu aus; Delegationsdreieck an `ForAll` | Tests A2, A4, B0 ergänzt |
| 7 Zahlen/Erwartungen | Abschnitt 1 und Test B angepasst |
| 8–10 Meldungen überdecken, Wettlauf, Feldname `Name` | U7, U8 ergänzt; `Name` ohne Konflikt, bleibt |

## Anhang 1: Originale der 5 Kachel-Properties (für den Rückfall)
""")
for r in B: w(block(r, orig=True))
open("UEBERGABE_Grundriss_L2_v0.3.md","w").write("".join(o))
print(len("".join(o)))
