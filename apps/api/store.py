"""Storage backends: MemoryStore (dev/tests) and PgStore (Postgres + row-level security).
Tenant id always comes from the verified token, never from client input.
Designed and developed by NIKHIL CHARY SRIRAMOJU."""
import datetime, os, uuid
from contextlib import contextmanager
from core import Index


def _now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()


class MemoryStore:
    def __init__(s): s.users, s.t = {}, {}

    def create_account(s, email, pw_hash, org):
        if email in s.users: return None
        tid, uid = str(uuid.uuid4()), str(uuid.uuid4())
        s.users[email] = {"uid": uid, "tid": tid, "pw_hash": pw_hash, "email": email}
        s.t[tid] = {"idx": Index(), "runs": {}, "lib": [], "audit": [], "org": org}
        return {"uid": uid, "tid": tid}

    def user_by_email(s, email): return s.users.get(email)

    def add_doc(s, tid, name, text):
        i = s.t[tid]["idx"]; b = len(i.chunks); i.add(name, text); return len(i.chunks) - b

    def index(s, tid): return s.t[tid]["idx"]

    def save_run(s, tid, src, items):
        rid = uuid.uuid4().hex; s.t[tid]["runs"][rid] = {"src": src, "items": items}; return rid

    def get_run(s, tid, rid): return s.t[tid]["runs"].get(rid)
    def set_items(s, tid, rid, items): s.t[tid]["runs"][rid]["items"] = items
    def lib(s, tid): return s.t[tid]["lib"]
    def add_lib(s, tid, e): s.t[tid]["lib"].append(e)
    def audit(s, tid, event, **kw): s.t[tid]["audit"].append({"ts": _now(), "event": event, **kw})
    def audit_list(s, tid): return s.t[tid]["audit"]


class PgStore:
    """Every tenant query runs in a transaction with SET LOCAL app.tenant_id (see db/schema.sql)."""

    def __init__(s, url):
        import psycopg  # noqa: F401  (imported lazily so memory mode needs no driver)
        s.url = url

    @contextmanager
    def tx(s, tid=None):
        import psycopg
        from psycopg.rows import dict_row
        with psycopg.connect(s.url, row_factory=dict_row) as c:  # commits on success, rolls back on error
            if tid: c.execute("select set_config('app.tenant_id', %s, true)", (str(tid),))
            yield c

    def create_account(s, email, pw_hash, org):
        import psycopg
        try:
            with s.tx() as c:
                tid = c.execute("insert into tenants(name) values (%s) returning id::text", (org,)).fetchone()["id"]
                uid = c.execute("insert into users(tenant_id,email,pw_hash) values (%s,%s,%s) returning id::text",
                                (tid, email, pw_hash)).fetchone()["id"]
            return {"uid": uid, "tid": tid}
        except psycopg.errors.UniqueViolation:
            return None

    def user_by_email(s, email):
        with s.tx() as c:
            r = c.execute("select id::text as uid, tenant_id::text as tid, pw_hash, email from users where email=%s", (email,)).fetchone()
        return r

    def add_doc(s, tid, name, text):
        with s.tx(tid) as c:
            c.execute("insert into documents(tenant_id,doc_type,title,text) values (%s,'policy',%s,%s)", (tid, name, text))
        i = Index(); i.add(name, text); return len(i.chunks)

    def index(s, tid):
        i = Index()
        with s.tx(tid) as c:
            for r in c.execute("select title,text from documents where tenant_id=%s order by created_at", (tid,)).fetchall():
                i.add(r["title"], r["text"])
        return i

    def save_run(s, tid, src, items):
        from psycopg.types.json import Jsonb
        with s.tx(tid) as c:
            return c.execute("insert into runs(tenant_id,src,items) values (%s,%s,%s) returning id::text",
                             (tid, src, Jsonb(items))).fetchone()["id"]

    def get_run(s, tid, rid):
        try: uuid.UUID(rid)
        except ValueError: return None
        with s.tx(tid) as c:
            r = c.execute("select src,items from runs where id=%s and tenant_id=%s", (rid, tid)).fetchone()
        return {"src": bytes(r["src"]), "items": r["items"]} if r else None

    def set_items(s, tid, rid, items):
        from psycopg.types.json import Jsonb
        with s.tx(tid) as c:
            c.execute("update runs set items=%s where id=%s and tenant_id=%s", (Jsonb(items), rid, tid))

    def lib(s, tid):
        with s.tx(tid) as c:
            rows = c.execute("select question_text,answer,source_ids from approved_answers where tenant_id=%s", (tid,)).fetchall()
        return [{"question": r["question_text"], "answer": r["answer"], "citations": r["source_ids"]} for r in rows]

    def add_lib(s, tid, e):
        from psycopg.types.json import Jsonb
        with s.tx(tid) as c:
            c.execute("insert into approved_answers(tenant_id,question_text,answer,source_ids) values (%s,%s,%s,%s)",
                      (tid, e["question"], e["answer"], Jsonb(e["citations"])))

    def audit(s, tid, event, **kw):
        from psycopg.types.json import Jsonb
        with s.tx(tid) as c:
            c.execute("insert into audit(tenant_id,event,data) values (%s,%s,%s)", (tid, event, Jsonb(kw)))

    def audit_list(s, tid):
        with s.tx(tid) as c:
            rows = c.execute("select ts,event,data from audit where tenant_id=%s order by ts", (tid,)).fetchall()
        return [{"ts": r["ts"].isoformat(), "event": r["event"], **r["data"]} for r in rows]


def get_store():
    url = os.getenv("DATABASE_URL")
    return PgStore(url) if url else MemoryStore()
