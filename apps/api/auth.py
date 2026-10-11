"""Passwords (scrypt) and signed expiring tokens, stdlib only.
Designed and developed by NIKHIL CHARY SRIRAMOJU."""
import base64, hashlib, hmac, json, os, secrets, time

_SECRET = None


def secret() -> bytes:
    global _SECRET
    if _SECRET is None:
        s = os.getenv("JWT_SECRET")
        if not s:
            print("WARNING: JWT_SECRET not set; using a random key (tokens reset on restart). Set it in production.")
            s = secrets.token_hex(32)
        elif len(s) < 32:
            raise RuntimeError("JWT_SECRET must be at least 32 characters")
        _SECRET = s.encode()
    return _SECRET


def _b(x: bytes) -> str: return base64.urlsafe_b64encode(x).decode().rstrip("=")
def _u(x: str) -> bytes: return base64.urlsafe_b64decode(x + "=" * (-len(x) % 4))


def check_password(pw: str):
    if len(pw) < 10 or len(pw) > 200: raise ValueError("password must be 10-200 characters")


def hash_password(pw: str) -> str:
    salt = os.urandom(16)
    return f"scrypt${_b(salt)}${_b(hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32))}"


def verify_password(pw: str, stored: str) -> bool:
    try:
        _, salt, h = stored.split("$")
        got = hashlib.scrypt(pw.encode(), salt=_u(salt), n=2**14, r=8, p=1, dklen=32)
        return hmac.compare_digest(got, _u(h))
    except Exception:
        return False


DUMMY = hash_password("not-a-real-password")  # equalises timing when the email is unknown


def make_token(uid: str, tid: str, ttl: int = 12 * 3600) -> str:
    body = _b(json.dumps({"uid": uid, "tid": tid, "exp": int(time.time()) + ttl}).encode())
    return body + "." + _b(hmac.new(secret(), body.encode(), hashlib.sha256).digest())


def read_token(tok: str):
    try:
        body, sig = tok.split(".")
        if not hmac.compare_digest(_u(sig), hmac.new(secret(), body.encode(), hashlib.sha256).digest()): return None
        d = json.loads(_u(body))
        return d if d["exp"] > time.time() else None
    except Exception:
        return None
