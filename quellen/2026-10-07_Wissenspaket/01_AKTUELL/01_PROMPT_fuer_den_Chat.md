# Startprompt für den Chat (zum Einfügen)

> Lies zuerst `00_UEBERGABE_an_Chat_PaketK_2026-10-07.md` vollständig (inkl. Abschnitt 0, Josias’ Feedback zu deiner letzten Analyse), dann `02_GESAMTE_AUFGABEN_Tischbuchung_2026-10-07.md` (alle Aufgaben und Wünsche mit Status und Priorität; prüfe sie auf Fehler und Lücken und ergänze, was du aus dem Projekt kennst) und `UEBERGABE_PaketK_v1.md`. Quelle der Wahrheit ist der Export vom 07.10. (`TischbuchungApp07.10.2026verbesserunganalyse_…zip`), nur lesen, nie zurückpacken.
>
> **Ziel:** Prüfe Paket K unabhängig und kritisch (die unabhängige Prüfung fehlt noch), korrigiere, was falsch ist, und gib mir **eine Übergabedatei im Stil von `UEBERGABE_Grundriss_L2_v0.3.md`** zurück: `UEBERGABE_PaketK_v2.md`. Nicht alles neu schreiben, prüfen, korrigieren, ergänzen.
>
> **Prüfe konkret, mit Belegstellen aus dem Export:**
> 1. Passt jeder Block exakt auf den veröffentlichten Stand? Bleibt die L2-Ladezeile in B1, B3, C1, C2 erhalten? Namen, Klammern, `;` vs. `;;`, Typkonflikte.
> 2. B1/B3 (neues Verlängern): Ist die Kollisionsprüfung gleichwertig zu den Plus-Knöpfen? `varIsLoading` auf jedem Pfad zurückgesetzt? Tab-/Grundriss-Variablen nicht vertauscht? Ist `Date(Year(x); Month(x); Day(x)) + Time(22; 0; 0)` für die 22:00-Grenze plausibel (U-K1)? Gibt es ungenannte Verhaltensänderungen? **B3 wurde von Claude Code nicht einzeln gelesen.**
> 3. A1 (K1): Nebenwirkungen, wenn `varSelectedBuchung` jetzt auch im Tab gesetzt wird (Check-in, Details, `conCheckinDialog.Y`, `btnEinchecken`, `lbl…`-Texte)?
> 4. K5: Setzen alle vier Knöpfe `varIsLoading` auf jedem Pfad zurück, sodass keiner gesperrt bleibt (auch B1/B3 mit den vielen `If`-Zweigen)?
> 5. Stimmt die Begründung, K4.2 zu verwerfen? Ist die Test-Reihenfolge im Dokument stimmig?
> 6. Entscheidungen E1 (22:00 ablehnen), E2 (Mehrfachauswahl drinlassen), E3 (Serie drinlassen): bewerte sie mit den Messdaten aus Abschnitt 4 der Übergabe.
> 7. Fehlt für den Go-Live am 14.10. etwas Wichtiges? Sag es offen, auch wenn es groß ist (Josias: „morgen ist keine Deadline“).
>
> **Regeln:** Josias fügt jede Formel selbst in Studio ein, du bearbeitest keine App. Immer ganze Properties, vollständige Blöcke ohne Platzhalter, deutsche Schreibweise, keine Kommentare in Verhaltensformeln. Kennzeichne jede Aussage als belegt / gemessen / geschlussfolgert / UNSICHER (UNSICHER mit Prüftest). Erzeuge die Blöcke **maschinell** aus dem Export (Skripte `exportiere_props.ps1` und `erzeuge_konzept.ps1` liegen bei, PowerShell; oder dein eigenes Skript) und prüfe sie gegen ihn. Binde das Ergebnis deiner unabhängigen Prüfung als eigenen Abschnitt ein (wie Abschnitt 10 in L2 v0.3). Kurzfassung zuerst, Deutsch mit Umlauten, kurz.
>
> **Liefere:** `UEBERGABE_PaketK_v2.md` (Kurzfassung, Übersicht, Entscheidungen, je Schritt: Steuerelement.Property, Änderung als Diff, vollständiger Block, Test; Rückfall; UNSICHER-Tabelle; unabhängige Prüfung; Anhang Originale). Wenn dir Informationen fehlen, sag es konkret, statt zu raten.
