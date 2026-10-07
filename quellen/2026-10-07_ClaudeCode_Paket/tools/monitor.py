"""Livemonitor-Export auswerten: python3 -I monitor.py <PowerAppsTraceEvents.json>
Hinweis: 'time' = ENDE der Antwort (= response.endTime). getRowsCount-Eintraege ohne status sind Begleiteintraege."""
import json, sys, collections, urllib.parse as up
d = json.load(open(sys.argv[1])); M = d["Messages"]; t0 = M[0]["time"]
T = lambda m: (m["time"] - t0) / 1000
net = [m for m in M if m["category"] == "Network" and (m.get("data") or {}).get("response", {}).get("status")]
ent = lambda m: (m["data"]["context"].get("entityName") or "?") + "." + (m["data"]["context"].get("propertyName") or "?")
ds = lambda m: ((m["data"]["context"].get("diagnosticContext") or {}).get("dataOperation") or {}).get("dataSource")
acts = [m for m in M if m["category"] == "UserAction" and m["name"] == "Select"]
cuts = [0.0] + [T(a) for a in acts] + [1e9]
names = ["Start"] + [ent(a) for a in acts]
for i, n in enumerate(names):
    sel = [m for m in net if cuts[i] <= T(m) < cuts[i + 1]]
    if not sel: continue
    starts = [T(m) - m["data"]["response"]["duration"] / 1000 for m in sel]
    print(f"== {cuts[i]:7.2f}s {n}: {len(sel)} Anfragen, letzte Antwort {max(T(m) for m in sel) - cuts[i]:.1f}s nach Aktion, "
          f"Status {dict(collections.Counter(m['data']['response']['status'] for m in sel))}")
    print("   Quellen:", dict(collections.Counter(ds(m) for m in sel)))
    print("   Top:", collections.Counter(ent(m) for m in sel).most_common(8))
