// Setzt die Befunde B1-B11 des Pruef-Subagenten in den YAML-Quellen um.
const fs = require('fs');
const dir = 'C:/tischbuchung_work/MOBIL/yaml/';
function rep(file, alt, neu, anzahl) {
  const p = dir + file;
  let t = fs.readFileSync(p, 'utf8');
  const n = t.split(alt).length - 1;
  if (n !== anzahl) throw new Error(file + ': erwartet ' + anzahl + ', gefunden ' + n + ' fuer: ' + alt.slice(0, 80));
  t = t.split(alt).join(neu);
  fs.writeFileSync(p, t, 'utf8');
  console.log(file, 'ok', n);
}
// Einrueckung des Verlaengern-Mittelteils (beide Knoepfe gleich)
const I = '                  ';
function verl(min) {
  const alt =
I + 'Set(varNeuEnde, DateAdd(varEndeAlt, ' + min + ', TimeUnit.Minutes));\n' +
I + 'Set(varTagesEnde, DateAdd(varBuchung.Startzeit, 22 * 60 - (Hour(varBuchung.Startzeit) * 60 + Minute(varBuchung.Startzeit)), TimeUnit.Minutes));\n' +
I + 'If(\n' +
I + '  varNeuEnde > varTagesEnde,\n' +
I + '  Notify("Eine Buchung kann nicht nach 22:00 Uhr enden.", NotificationType.Warning),\n' +
I + '  If(\n' +
I + '    !IsBlank(LookUp(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID),\n' +
I + '    Notify("Der Tisch ist in dieser Zeit schon belegt.", NotificationType.Warning),\n' +
I + '    IfError(\n' +
I + '      Patch(Tischbuchungen, varBuchung, { Endzeit: varNeuEnde }),\n' +
I + '      Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),\n' +
I + '      If(\n' +
I + '        LookUp(Tischbuchungen, ID = varBuchungID).Endzeit = varNeuEnde,\n' +
I + '        Notify("Buchung verlängert.", NotificationType.Success);\n' +
I + '        Set(varZeigeVerwalten, false),\n' +
I + '        Notify("Die Verlängerung ist nicht angekommen. Bitte aktualisieren.", NotificationType.Warning)\n' +
I + '      )\n' +
I + '    )\n' +
I + '  )\n' +
I + ')\n';
  const neu =
I + 'Set(varNeuEnde, DateAdd(varEndeAlt, ' + min + ', TimeUnit.Minutes));\n' +
I + 'Set(varTagesEnde, DateTime(Year(varBuchung.Startzeit), Month(varBuchung.Startzeit), Day(varBuchung.Startzeit), 22, 0, 0));\n' +
I + 'If(\n' +
I + '  varEndeAlt <= Now(),\n' +
I + '  Notify("Diese Buchung ist bereits beendet.", NotificationType.Information); Set(varZeigeVerwalten, false),\n' +
I + '  varNeuEnde > varTagesEnde,\n' +
I + '  Notify("Eine Buchung kann nicht nach 22:00 Uhr enden.", NotificationType.Warning),\n' +
I + '  !IsBlank(LookUp(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID),\n' +
I + '  Notify("Der Tisch ist in dieser Zeit schon belegt.", NotificationType.Warning),\n' +
I + '  !IsBlank(LookUp(Tischbuchungen, Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID),\n' +
I + '  Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht.", NotificationType.Warning),\n' +
I + '  IfError(\n' +
I + '    Patch(Tischbuchungen, varBuchung, { Endzeit: varNeuEnde }),\n' +
I + '    Notify("Das Verlängern ist fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),\n' +
I + '    ClearCollect(colKollision, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));\n' +
I + '    If(\n' +
I + '      LookUp(colKollision, ID = varBuchungID).Endzeit <> varNeuEnde,\n' +
I + '      Notify("Die Verlängerung ist nicht angekommen. Bitte aktualisieren.", NotificationType.Warning),\n' +
I + '      !IsBlank(LookUp(colKollision, ID <> varBuchungID).ID),\n' +
I + '      IfError(\n' +
I + '        Patch(Tischbuchungen, LookUp(Tischbuchungen, ID = varBuchungID), { Endzeit: varEndeAlt }),\n' +
I + '        Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Bitte deine Buchung prüfen, sie überschneidet sich.", NotificationType.Error),\n' +
I + '        Notify("Jemand hat den Tisch gerade für diese Zeit gebucht. Die Verlängerung wurde zurückgenommen.", NotificationType.Error)\n' +
I + '      ),\n' +
I + '      Notify("Buchung verlängert.", NotificationType.Success);\n' +
I + '      Set(varZeigeVerwalten, false)\n' +
I + '    )\n' +
I + '  )\n' +
I + ')\n';
  rep('dialoge.yaml', alt, neu, 1);
}
verl(60); verl(120);

// B1 + B4: Jetzt beenden
rep('dialoge.yaml',
I + 'If(\n' +
I + '  Now() <= varBuchung.Startzeit,\n' +
I + '  Notify("Diese Buchung hat noch nicht begonnen. Du kannst sie stornieren.", NotificationType.Warning),\n' +
I + '  IfError(\n' +
I + '    Patch(Tischbuchungen, varBuchung, { Endzeit: Now() }),\n',
I + 'If(\n' +
I + '  Now() <= varBuchung.Startzeit,\n' +
I + '  Notify("Diese Buchung hat noch nicht begonnen. Du kannst sie stornieren.", NotificationType.Warning),\n' +
I + '  Now() >= varBuchung.Endzeit,\n' +
I + '  Notify("Diese Buchung ist bereits beendet.", NotificationType.Information); Set(varZeigeVerwalten, false),\n' +
I + '  Set(varNeuEnde, With({ ab: DateTime(Year(Now()), Month(Now()), Day(Now()), Hour(Now()), If(Minute(Now()) >= 30, 30, 0), 0) }, If(ab > varBuchung.Startzeit, ab, Now())));\n' +
I + '  IfError(\n' +
I + '    Patch(Tischbuchungen, varBuchung, { Endzeit: varNeuEnde }),\n', 1);

// B10: Stornieren-Knopf mit Sperre
rep('dialoge.yaml', '            OnSelect: =Set(varZeigeStorno, true)',
  '            OnSelect: =If(!varIsLoading && Now() >= varSperreBis, Set(varZeigeStorno, true))', 1);

// B5 + B8: Einchecken mit eigener Variable und varJetzt
rep('conHeute.yaml', 'Set(varBuchungID, ThisItem.ID);\n                            With(', 'Set(varCheckinID, ThisItem.ID);\n                            With(', 1);
rep('conHeute.yaml', '{ frisch: LookUp(Tischbuchungen, ID = varBuchungID) }', '{ frisch: LookUp(Tischbuchungen, ID = varCheckinID) }', 1);
rep('conHeute.yaml', 'LookUp(Tischbuchungen, ID = varBuchungID).CheckedIn', 'LookUp(Tischbuchungen, ID = varCheckinID).CheckedIn', 1);
rep('conHeute.yaml', 'Now() >= DateAdd(ThisItem.Startzeit, -30, TimeUnit.Minutes) && Now() <= ThisItem.Endzeit,',
  'varJetzt >= DateAdd(ThisItem.Startzeit, -30, TimeUnit.Minutes) && varJetzt <= ThisItem.Endzeit,', 1);
