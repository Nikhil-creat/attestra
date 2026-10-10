"""Questionnaire answering graph: classify -> retrieve -> draft -> critic.
Replace the stub functions (llm_*, hybrid_search, rerank) with real implementations."""
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

MAX_REVISIONS = 2


class State(TypedDict):
    tenant_id: str
    question: str
    category: Optional[str]
    approved_match: Optional[dict]
    retrieved: List[dict]        # [{id, text, source}]
    draft: Optional[str]
    citations: List[str]
    verdict: Optional[str]       # pass | revise | fail
    feedback: Optional[str]
    confidence: float
    revisions: int


# ---- stubs: wire these to your LLM / DB ---------------------------------
def llm_classify(q: str) -> str: ...
def lookup_approved_answer(tenant_id: str, q: str) -> Optional[dict]: ...
def hybrid_search(tenant_id: str, q: str, category: str, k: int = 30) -> List[dict]: ...
def rerank(q: str, chunks: List[dict], k: int = 5) -> List[dict]: ...
def llm_draft(q: str, chunks: List[dict], feedback: Optional[str]) -> dict:
    """Return {'answer': str, 'citations': [chunk ids]} or 'Insufficient evidence'."""
def llm_critic(q: str, draft: str, chunks: List[dict]) -> dict:
    """Return {'verdict': 'pass|revise|fail', 'confidence': float, 'feedback': str}.
    Fail any claim not supported by a cited chunk."""
# --------------------------------------------------------------------------


def classify(s: State):
    cat = llm_classify(s["question"])
    return {"category": cat, "approved_match": lookup_approved_answer(s["tenant_id"], s["question"])}


def retrieve(s: State):
    if s.get("approved_match"):
        m = s["approved_match"]
        return {"retrieved": [{"id": m["id"], "text": m["answer"], "source": "approved_answer"}]}
    hits = hybrid_search(s["tenant_id"], s["question"], s["category"])
    return {"retrieved": rerank(s["question"], hits)}


def draft(s: State):
    out = llm_draft(s["question"], s["retrieved"], s.get("feedback"))
    return {"draft": out["answer"], "citations": out["citations"],
            "revisions": s.get("revisions", 0) + (1 if s.get("feedback") else 0)}


def critic(s: State):
    if not s["citations"] or s["draft"].startswith("Insufficient evidence"):
        return {"verdict": "fail", "confidence": 0.0, "feedback": "no supporting evidence"}
    r = llm_critic(s["question"], s["draft"], s["retrieved"])
    return {"verdict": r["verdict"], "confidence": r["confidence"], "feedback": r["feedback"]}


def route(s: State):
    if s["verdict"] == "pass":
        return "save"
    if s["verdict"] == "revise" and s["revisions"] < MAX_REVISIONS:
        return "draft"
    return "escalate"


def save(s: State):      # persist answer with status='drafted' + citations, log agent_run
    return {}


def escalate(s: State):  # persist with status='escalated' for human review
    return {}


g = StateGraph(State)
for name, fn in [("classify", classify), ("retrieve", retrieve), ("draft", draft),
                 ("critic", critic), ("save", save), ("escalate", escalate)]:
    g.add_node(name, fn)
g.set_entry_point("classify")
g.add_edge("classify", "retrieve")
g.add_edge("retrieve", "draft")
g.add_edge("draft", "critic")
g.add_conditional_edges("critic", route, {"save": "save", "draft": "draft", "escalate": "escalate"})
g.add_edge("save", END)
g.add_edge("escalate", END)

# Compile with a Postgres checkpointer in production so jobs resume after a crash:
# graph = g.compile(checkpointer=PostgresSaver(conn))
graph = g.compile()
