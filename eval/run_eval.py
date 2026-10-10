"""Golden-set eval: python eval/run_eval.py  (fails below 90%). Designed and developed by NIKHIL CHARY SRIRAMOJU."""
import json, sys
sys.path.insert(0, "apps/api")
from core import Index, answer_question
idx = Index(); idx.add("policy.md", open("samples/security-policy.md").read())
gold = json.load(open("eval/golden.json")); ok = 0
for g in gold:
    r = answer_question(idx, g["q"]); hit = g["must"].lower() in r["answer"].lower() and r["verdict"] == "pass" and bool(r["citations"])
    ok += hit; print("PASS" if hit else "FAIL", g["q"])
score = ok / len(gold); print(f"accuracy {score:.0%}"); sys.exit(0 if score >= 0.9 else 1)
