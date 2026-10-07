# So startest du den Bau der Handy-App

Kurzfassung: Gleiche Claude-Code-Sitzung wie bei der Analyse öffnen, Auto-Modus an, den Text aus `GOAL.txt` einfügen, erreichbar bleiben. Alles Weitere macht Claude Code und schreibt es in diesen Ordner.

## Vorher (5 Minuten)
1. Chrome öffnen und bei https://make.powerapps.com angemeldet sein (Umgebung „Personal Productivity").
2. Claude in Chrome ist aktiv, falls Claude Code den Browser steuern soll.
3. Energieeinstellungen: Laptop darf während der Arbeit nicht in den Ruhezustand gehen, Deckel offen lassen.
4. Die produktive App „Tischbuchung" bitte währenddessen nicht im Studio bearbeiten und speichern lassen, wenn Claude Code gerade darin liest.

## Start
5. Eingabeaufforderung/PowerShell in `C:\tischbuchung_work` öffnen.
6. **Dieselbe Sitzung** fortsetzen, in der Claude Code die App analysiert hat, damit sein Wissen erhalten bleibt:
   `claude --continue --chrome`
   (oder `claude --resume` und die Sitzung auswählen; falls `--chrome` nicht geht: ohne starten und im Gespräch `/chrome` eingeben)
7. Mit `Umschalt+Tab` in den **Auto-Modus** wechseln (Statuszeile zeigt „auto mode").
8. Den kompletten Inhalt von `GOAL.txt` als eine Nachricht einfügen und abschicken.

## Während der Arbeit
- Claude Code fragt dich ggf. nach Anmeldung/MFA im Browser oder nach dem Studio-Link der neuen App. Das steht dann auch oben in `FRAGEN_AN_JOSIAS.md`.
- Wenn Claude Code dich bittet, einen Studio-Tab offen zu lassen: nicht schließen (Co-Authoring hängt daran).
- Stand ansehen: `/goal` (ohne Text) oder `FORTSCHRITT.md` öffnen.
- Anhalten: `Esc` (unterbrechen) oder `/goal clear` (Ziel beenden). Weitermachen: GOAL.txt erneut einfügen.
- Du kannst parallel an anderen Dingen arbeiten, aber die Handy-App selbst nicht im Studio anfassen, solange Claude Code daran baut.

## Am Ende
- `ABNAHME.md` und `ANLEITUNG_JOSIAS.md` lesen.
- Checkliste J1–J3 abarbeiten (echte Handys, Testgruppe, Entscheidungen).
