import sys, io; sys.path.insert(0, "apps/api")
from openpyxl import Workbook
from core import Index, answer_question, parse_questions, export_xlsx

DOC = open("samples/security-policy.md").read()

def idx():
    i = Index(); i.add("policy.md", DOC); return i

def test_cited_answer_passes():
    r = answer_question(idx(), "Do you encrypt customer data at rest?")
    assert r["citations"] and "AES-256" in r["answer"] and r["verdict"] == "pass"

def test_unknown_question_escalates():
    r = answer_question(idx(), "Do you operate a quantum datacenter on the moon?")
    assert r["verdict"] == "escalate"

def test_sensitive_topic_escalates():
    r = answer_question(idx(), "Describe your breach notification process and encryption of data")
    assert r["verdict"] == "escalate"

def test_xlsx_roundtrip():
    wb = Workbook(); ws = wb.active; ws.append(["Question"]); ws.append(["Do you encrypt customer data at rest?"])
    b = io.BytesIO(); wb.save(b)
    qs = parse_questions(b.getvalue()); assert len(qs) == 1
    items = [{**q, **answer_question(idx(), q["text"])} for q in qs]
    assert export_xlsx(b.getvalue(), items)

def test_pii_masking():
    from core import mask_pii
    t = mask_pii("mail a.b@corp.com or call +1 415 555 0100 from 10.0.0.1")
    assert "@" not in t and "[EMAIL]" in t and "[IP]" in t and "[PHONE]" in t

def test_library_reuse():
    from core import answer_question
    lib = [{"question": "Do you encrypt customer data at rest?", "answer": "Yes, AES-256.", "citations": ["policy.md#1"]}]
    r = answer_question(idx(), "Do you encrypt customer data at rest?", lib)
    assert r["status"] == "reused" and r["verdict"] == "pass"

def test_stale_and_gaps():
    import datetime
    from core import stale_docs, gap_analysis
    i = Index(); i.add("old.md", "Last reviewed: 2020-01-01\n\nWe encrypt data.")
    assert stale_docs(i, 365, datetime.date(2026, 10, 10))
    assert gap_analysis([{"verdict": "escalate", "reason": "weak support", "question": "q"}])["escalated"] == 1
