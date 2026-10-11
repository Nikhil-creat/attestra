"""Attestra API. Designed and developed by NIKHIL CHARY SRIRAMOJU."""
import io, os, time, collections
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Request
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pypdf import PdfReader
from docx import Document as Docx
import auth
from core import answer_question, parse_questions, export_xlsx, stale_docs, gap_analysis
from store import get_store

AUTHOR = {"name": "NIKHIL CHARY SRIRAMOJU", "github": "https://github.com/Nikhil-creat",
          "linkedin": "https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a"}
app = FastAPI(title="Attestra", version="1.4.0",
              description="Cited AI answers for security questionnaires. Designed and developed by NIKHIL CHARY SRIRAMOJU.")
S = get_store()
MAX_BYTES = 10 * 1024 * 1024
HITS = collections.defaultdict(list)


@app.middleware("http")
async def limits(request: Request, call_next):
    p = request.url.path
    if p.startswith("/api"):
        bucket = "auth" if p.startswith("/api/auth") else "api"
        lim = 10 if bucket == "auth" else int(os.getenv("RATE_LIMIT", "120"))
        k, now = (request.client.host if request.client else "?", bucket), time.time()
        HITS[k] = [t for t in HITS[k] if now - t < 60]
        if len(HITS[k]) >= lim: return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)
        HITS[k].append(now)
    return await call_next(request)


class Cred(BaseModel):
    email: str
    password: str
    org: str | None = None


def me(request: Request):
    h = request.headers.get("authorization", "")
    t = auth.read_token(h[7:] if h.lower().startswith("bearer ") else "")
    if not t: raise HTTPException(401, "login required")
    return t


@app.get("/health")
def health(): return {"status": "ok"}


@app.get("/api/about")
def about(): return AUTHOR


@app.post("/api/auth/register")
def register(c: Cred):
    if os.getenv("ALLOW_REGISTER", "1") != "1": raise HTTPException(403, "registration is closed")
    email = c.email.strip().lower()
    if "@" not in email or len(email) > 254: raise HTTPException(422, "invalid email")
    try: auth.check_password(c.password)
    except ValueError as e: raise HTTPException(422, str(e))
    a = S.create_account(email, auth.hash_password(c.password), (c.org or email.split("@")[0])[:80])
    if not a: raise HTTPException(409, "email already registered")
    S.audit(a["tid"], "account_created", email=email)
    return {"token": auth.make_token(a["uid"], a["tid"])}


@app.post("/api/auth/login")
def login(c: Cred):
    u = S.user_by_email(c.email.strip().lower())
    ok = auth.verify_password(c.password, u["pw_hash"] if u else auth.DUMMY)
    if not (u and ok): raise HTTPException(401, "invalid email or password")
    return {"token": auth.make_token(u["uid"], u["tid"])}


@app.get("/api/auth/me")
def whoami(u=Depends(me)): return {"user_id": u["uid"], "tenant_id": u["tid"]}


async def read(f: UploadFile):
    data = await f.read()
    if len(data) > MAX_BYTES: raise HTTPException(413, "file too large (10MB max)")
    return data


@app.post("/api/documents")
async def add_document(file: UploadFile = File(...), u=Depends(me)):
    data, name = await read(file), file.filename or "doc"
    low = name.lower()
    if low.endswith(".pdf"): text = "\n\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    elif low.endswith(".docx"): text = "\n\n".join(p.text for p in Docx(io.BytesIO(data)).paragraphs)
    elif low.endswith((".txt", ".md")): text = data.decode("utf-8", "ignore")
    else: raise HTTPException(400, "supported: pdf, docx, txt, md")
    n = S.add_doc(u["tid"], name, text); S.audit(u["tid"], "document_added", document=name, by=u["uid"])
    return {"document": name, "chunks_added": n}


def summary(items):
    n = len(items); p = sum(i["verdict"] == "pass" for i in items)
    return {"total": n, "auto_passed": p, "escalated": n - p}


def run_or_404(u, rid):
    r = S.get_run(u["tid"], rid)
    if not r: raise HTTPException(404, "not found")
    return r


@app.post("/api/questionnaires")
async def run_questionnaire(file: UploadFile = File(...), u=Depends(me)):
    data, tid = await read(file), u["tid"]
    idx = S.index(tid)
    if not idx.chunks: raise HTTPException(400, "upload policy documents first")
    try: qs = parse_questions(data)
    except Exception: raise HTTPException(400, "could not read xlsx file")
    lib = S.lib(tid)
    items = [{**q, **answer_question(idx, q["text"], lib)} for q in qs]
    rid = S.save_run(tid, data, items); S.audit(tid, "questionnaire_run", id=rid, questions=len(items), by=u["uid"])
    return {"id": rid, "items": items, "summary": summary(items)}


@app.get("/api/questionnaires/{rid}")
def get_q(rid: str, u=Depends(me)):
    r = run_or_404(u, rid); return {"id": rid, "items": r["items"], "summary": summary(r["items"])}


@app.post("/api/questionnaires/{rid}/items/{n}/approve")
def approve(rid: str, n: int, body: dict | None = None, u=Depends(me)):
    r = run_or_404(u, rid)
    if not 0 <= n < len(r["items"]): raise HTTPException(404, "item not found")
    it = r["items"][n]
    if body and body.get("answer"): it["answer"] = str(body["answer"])[:5000]
    it["status"] = "approved"
    S.set_items(u["tid"], rid, r["items"])
    S.add_lib(u["tid"], {"question": it["question"], "answer": it["answer"], "citations": it["citations"]})
    S.audit(u["tid"], "answer_approved", run=rid, item=n, by=u["uid"])
    return it


@app.get("/api/questionnaires/{rid}/export")
def export(rid: str, u=Depends(me)):
    r = run_or_404(u, rid)
    return Response(export_xlsx(r["src"], r["items"]),
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": f"attachment; filename=answers-{rid[:8]}.xlsx"})


@app.get("/api/questionnaires/{rid}/gaps")
def gaps(rid: str, u=Depends(me)): return gap_analysis(run_or_404(u, rid)["items"])


@app.get("/api/stale-documents")
def stale(days: int = 365, u=Depends(me)): return stale_docs(S.index(u["tid"]), days)


@app.get("/api/audit")
def audit(u=Depends(me)): return S.audit_list(u["tid"])


app.mount("/", StaticFiles(directory="static", html=True), name="static")
