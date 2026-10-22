# Сводка `hyperframes check --json`: печатает все находки, кроме info
import sys, json
s = open(sys.argv[1]).read(); d = json.loads(s[s.index('{'):])
print("ok:", d.get("ok"))
for sec in ("lint", "runtime", "layout", "craft", "media", "audio"):
    v = d.get(sec)
    if not isinstance(v, dict): continue
    for f in v.get("findings", []):
        if f.get("severity") == "info": continue
        print(f"[{sec}] {f['severity']} {f['code']} t={f.get('time')} {f.get('selector','')} :: {f['message'][:230]}")
for k, v in d.items():
    if k not in ("lint","runtime","layout","craft","media","audio","ok","strict","browserSkipped") : print(k, str(v)[:300])
