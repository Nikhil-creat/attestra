import sys, io, time; sys.path.insert(0, "apps/api")
import os; os.environ["JWT_SECRET"] = "x" * 40
import auth, store

def test_password_and_token():
    h = auth.hash_password("correct horse battery"); assert auth.verify_password("correct horse battery", h)
    assert not auth.verify_password("wrong password!!", h)
    t = auth.make_token("u1", "t1"); assert auth.read_token(t)["tid"] == "t1"
    assert auth.read_token(t[:-2] + "xx") is None and auth.read_token("garbage") is None
    assert auth.read_token(auth.make_token("u", "t", ttl=-5)) is None
    try: auth.check_password("short"); assert False
    except ValueError: pass

def test_memory_store_isolation():
    s = store.MemoryStore()
    a = s.create_account("a@x.com", "h", "A"); b = s.create_account("b@x.com", "h", "B")
    assert a and b and s.create_account("a@x.com", "h", "A") is None
    s.add_doc(a["tid"], "p.md", "We encrypt data with AES-256."); assert s.index(b["tid"]).chunks == []
    rid = s.save_run(a["tid"], b"x", [{"q": 1}]); assert s.get_run(b["tid"], rid) is None and s.get_run(a["tid"], rid)

def test_api_end_to_end():
    try:
        from fastapi.testclient import TestClient
    except Exception:
        return  # fastapi/httpx not installed here
    sys.path.insert(0, "apps/api"); os.chdir("apps/api")
    try:
        import main; from openpyxl import Workbook
        c = TestClient(main.app)
        def reg(e): return {"Authorization": "Bearer " + c.post("/api/auth/register", json={"email": e, "password": "a-long-password"}).json()["token"]}
        ha, hb = reg("a@x.com"), reg("b@x.com")
        assert c.get("/api/audit").status_code == 401
        assert c.post("/api/auth/register", json={"email": "a@x.com", "password": "a-long-password"}).status_code == 409
        assert c.post("/api/documents", headers=ha, files={"file": ("p.md", b"All data is encrypted at rest using AES-256.")}).status_code == 200
        wb = Workbook(); ws = wb.active; ws.append(["Question"]); ws.append(["Do you encrypt customer data at rest?"]); bio = io.BytesIO(); wb.save(bio)
        r = c.post("/api/questionnaires", headers=ha, files={"file": ("q.xlsx", bio.getvalue())}).json(); rid = r["id"]
        assert r["summary"]["auto_passed"] == 1
        assert c.get(f"/api/questionnaires/{rid}", headers=hb).status_code == 404   # other tenant cannot see it
        assert c.post(f"/api/questionnaires/{rid}/items/0/approve", headers=ha).status_code == 200
        assert c.get(f"/api/questionnaires/{rid}/export", headers=ha).status_code == 200
    finally:
        os.chdir("../..")
