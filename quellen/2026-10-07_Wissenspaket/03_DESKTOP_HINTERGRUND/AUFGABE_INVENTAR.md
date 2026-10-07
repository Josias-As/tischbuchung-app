# Aufgabe: Inventar des App-Quellcodes

Durchsuche `./src` vollständig. Die App ist in `KONTEXT.md` beschrieben, die Korrekturen dazu in `KORREKTUR.md` — **`KORREKTUR.md` sticht `KONTEXT.md`.**

Meine bisherige Dokumentation ist nachweislich an mehreren Stellen veraltet, und Abschnitt 2 von `KONTEXT.md` stammt aus einer **anderen App**. Verlass dich ausschließlich auf den Quellcode. Wo Quellcode und Notiz sich widersprechen, gilt der Quellcode, und du schreibst den Widerspruch ausdrücklich hin.

Schreibe `INVENTAR.md` mit diesen elf Abschnitten. **Kein Abschnitt bleibt leer** — wenn es keine Treffer gibt, schreibst du „keine Treffer" hin.

---

## 1. MASTER-BEDINGUNG

Alle Vorkommen der `LookUp`-Formel auf `Tischbuchungen` mit `Tisch.Value` und `Now()` — die Bedingung, die entscheidet, ob eine Grundriss-Kachel frei, ausstehend oder belegt ist.

Pro Fund: Datei, Steuerelement, Property, **vollständig zitierte Formel**.

Meine Notizen sagen „sechs Stellen". Prüf das — ich vermute, es sind mehr.

## 2. REFRESH

Jedes Vorkommen von `Refresh(`.

Markiere ausdrücklich, welche davon **innerhalb einer `ForAll`-Schleife** stehen. Das ist mein Hauptverdacht für die sehr langsame Serienbuchung: `Refresh` lädt die komplette Liste neu, und in einer Schleife passiert das pro Durchlauf.

## 3. DELEGATION

Alle `Filter(` und `LookUp(` auf `Tischbuchungen`.

Pro Formel eine Einschätzung: delegierbar oder nicht, und **woran genau** es scheitert. Kandidaten für Nicht-Delegierbarkeit sind Lookup-Spalten wie `Tisch`, sowie `Now()`, `Today()` und `DateAdd()` direkt in der Formel.

## 4. CHECK-IN-SPALTE

Jedes Vorkommen von `CheckedIn` **und** von `Checkedin` — Groß-/Kleinschreibung unterschieden.

Ein falsch geschriebener Feldname wird von SharePoint **still ignoriert**, ohne Fehlermeldung. Wenn beide Schreibweisen vorkommen, ist das ein latenter Bug. Wenn du nicht sicher sagen kannst, welche die richtige ist, schreib `UNSICHER`.

## 5. TOTER CODE

Alle Referenzen auf: `Raum`, `Räume`, `Raumbuchungen`, `varZeigeRaum`, `varAusgewählt`, sowie `varZoom`, `varPanX`, `varPanY`.

Raumbuchungen sind aus dem Scope gestrichen. Gib pro Fund an, **was ihn noch referenziert** — das entscheidet, ob er gefahrlos löschbar ist.

## 6. APP.FORMULAS

Vollständiger Inhalt der Named Formulas, unverändert zitiert.

## 7. SPINNER

Alles zu `varIsLoading`, `varSpinnerWinkel`, `conLadeOverlay`, `imgSpinner`.

Existiert irgendwo ein **Timer-Steuerelement**? Gemeldeter Bug: Das Ladesymbol erscheint an manchen Stellen doppelt.

## 8. MEHRFACHAUSWAHL

Alle Formeln rund um `colAusgewaehlteBuchungen`, `varMehrfachAuswahlModus`, `varAuswahlModusAktiv` — besonders **Speichern** und **Stornieren**.

Das ist der wichtigste Performance-Punkt der App. Zitiere hier besonders vollständig; auf diesen Formeln baut die anschließende Entwurfsarbeit auf.

## 9. FARBEN

Alle Farbliterale mit Fundort (`#00A96B`, `#4DC398`, `#EB3951`, `#FFA500`, `#171496` und alle weiteren).

## 10. UMFANG

Steuerelementanzahl pro Container. Dazu eine Liste der Steuerelemente, die **nirgends referenziert** werden.

Hintergrund: Jedes Steuerelement kostet Speicher beim Laden des Screens. Das ist ein direkter Ladezeit-Faktor.

## 11. ABWEICHUNGEN ZU KONTEXT.md

Jede Stelle, an der der echte Quellcode von Abschnitt 2 in `KONTEXT.md` abweicht — Container, Variablen, `App.OnStart`-Inhalt, toter Code.

Das ist **erwartbar**, weil Abschnitt 2 aus einer anderen App stammt. Abweichungen sind hier das Ergebnis, nicht der Fehler.

---

## FAZIT

Maximal 10 Sätze. Was hat dich am meisten überrascht? Wo siehst du das größte Problem?

Sei kritisch, keine Beschönigung.
