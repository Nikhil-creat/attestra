"""Attestra - API. Designed and developed by NIKHIL CHARY SRIRAMOJU."""
import io, os, time, uuid, hmac, collections
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from docx import Document as Docx
import datetime
from core import Index, answer_question, parse_questions, export_xlsx, stale_docs, gap_analysis

AUTHOR = {"name": "NIKHIL CHARY SRIRAMOJU", "github": "https://github.com/Nikhil-creat",
          "linkedin": "https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a"}
app = FastAPI(title="Attestra", version="1.0.0",
              description="Cited AI answers for security questionnaires. Designed and developed by NIKHIL CHARY SRIRAMOJU.")
HITS = collections.defaultdict(list)


@app.middleware("http")
async def guard(request: Request, call_next):
    if request.url.path.startswith("/api"):
        key = os.getenv("API_KEY")
        if key and not hmac.compare_digest(request.headers.get("x-api-key", ""), key):
            return JSONResponse({"detail": "invalid API key"}, status_code=401)
        who, now, lim = request.client.host if request.client else "?", time.time(), int(os.getenv("RATE_LIMIT", "60"))
        HITS[who] = [t for t in HITS[who] if now - t < 60]
        if len(HITS[who]) >= lim:
            return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)
        HITS[who].append(now)
    return await call_next(request)


STORE = {}  # tenant -> {"index": Index, "runs": {id: {...}}}  (swap for Postgres, see schema.sql)
MAX_BYTES = 10 * 1024 * 1024


def tenant(t): return STORE.setdefault(t, {"index": Index(), "runs": {}, "lib": [], "audit": []})


def log(t, event, **kw): t["audit"].append({"ts": datetime.datetime.utcnow().isoformat() + "Z", "event": event, **kw})


async def read(f: UploadFile):
    data = await f.read()
    if len(data) > MAX_BYTES: raise HTTPException(413, "file too large (10MB max)")
    return data


@app.get("/health")
def health(): return {"status": "ok"}


@app.get("/api/about")
def about(): return AUTHOR


@app.post("/api/documents")
async def add_document(file: UploadFile = File(...), x_tenant: str = Header("demo")):
    data, name = await read(file), file.filename or "doc"
    low = name.lower()
    if low.endswith(".pdf"): text = "\n\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    elif low.endswith(".docx"): text = "\n\n".join(p.text for p in Docx(io.BytesIO(data)).paragraphs)
    elif low.endswith((".txt", ".md")): text = data.decode("utf-8", "ignore")
    else: raise HTTPException(400, "supported: pdf, docx, txt, md")
    t = tenant(x_tenant); before = len(t["index"].chunks)
    t["index"].add(name, text); log(t, "document_added", document=name)
    return {"document": name, "chunks_added": len(t["index"].chunks) - before}


@app.post("/api/questionnaires")
async def run_questionnaire(file: UploadFile = File(...), x_tenant: str = Header("demo")):
    data = await read(file); t = tenant(x_tenant)
    if not t["index"].chunks: raise HTTPException(400, "upload policy documents first")
    try: qs = parse_questions(data)
    except Exception: raise HTTPException(400, "could not read xlsx file")
    items = [{**q, **answer_question(t["index"], q["text"], t["lib"])} for q in qs]
    rid = uuid.uuid4().hex[:8]; t["runs"][rid] = {"src": data, "items": items}; log(t, "questionnaire_run", id=rid, questions=len(items))
    return {"id": rid, "items": items, "summary": summary(items)}


def summary(items):
    n = len(items); p = sum(i["verdict"] == "pass" for i in items)
    return {"total": n, "auto_passed": p, "escalated": n - p}


def get_run(rid, x_tenant):
    r = tenant(x_tenant)["runs"].get(rid)
    if not r: raise HTTPException(404, "not found")
    return r


@app.get("/api/questionnaires/{rid}")
def get_q(rid: str, x_tenant: str = Header("demo")):
    r = get_run(rid, x_tenant); return {"id": rid, "items": r["items"], "summary": summary(r["items"])}


@app.post("/api/questionnaires/{rid}/items/{n}/approve")
def approve(rid: str, n: int, body: dict | None = None, x_tenant: str = Header("demo")):
    r = get_run(rid, x_tenant)
    if not 0 <= n < len(r["items"]): raise HTTPException(404, "item not found")
    it = r["items"][n]
    if body and body.get("answer"): it["answer"] = body["answer"]
    it["status"] = "approved"
    t = tenant(x_tenant)
    t["lib"].append({"question": it["question"], "answer": it["answer"], "citations": it["citations"]})
    log(t, "answer_approved", run=rid, item=n)
    return it


@app.get("/api/questionnaires/{rid}/export")
def export(rid: str, x_tenant: str = Header("demo")):
    r = get_run(rid, x_tenant)
    return Response(export_xlsx(r["src"], r["items"]),
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": f"attachment; filename=answers-{rid}.xlsx"})


@app.get("/api/audit")
def audit(x_tenant: str = Header("demo")): return tenant(x_tenant)["audit"]


@app.get("/api/stale-documents")
def stale(days: int = 365, x_tenant: str = Header("demo")): return stale_docs(tenant(x_tenant)["index"], days)


@app.get("/api/questionnaires/{rid}/gaps")
def gaps(rid: str, x_tenant: str = Header("demo")): return gap_analysis(get_run(rid, x_tenant)["items"])


app.mount("/", StaticFiles(directory="static", html=True), name="static")
