<p align="center"><img src="site/assets/logo.svg" width="110" alt="Attestra logo"></p>

# Attestra

AI agents that draft **cited** answers to customer security questionnaires (SOC 2, SIG, custom spreadsheets) from your own
policies. A critic checks every answer against its sources, anything weak or sensitive goes to a human, and approved
answers export back into the original XLSX.

> **Designed and developed by NIKHIL CHARY SRIRAMOJU**
> [GitHub](https://github.com/Nikhil-creat) · [LinkedIn](https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a)

**Website:** https://nikhil-creat.github.io/questionnaire-ai/ · **Live demo:** https://nikhil-creat.github.io/questionnaire-ai/demo.html

## Quickstart
```bash
python samples/make_questionnaire.py        # already included: samples/questionnaire.xlsx
make run                                    # http://localhost:8000
```
1. Upload `samples/security-policy.md` (or your own pdf/docx/txt/md).
2. Upload `samples/questionnaire.xlsx` and click **Draft answers**.
3. Review, approve, and **Export XLSX**.

Docker: `cp .env.example .env && make docker`. Tests: `make test`.
Set `ANTHROPIC_API_KEY` in `.env` for LLM drafting. Without it, the app runs offline in extractive mode.

## Features
- Cited drafting (LLM or offline), critic with escalation rules, human approval, XLSX in/out
- Answer library: approved answers are reused for repeat questions
- PII masking before any LLM call, audit log, stale-policy warnings, gap analysis
- Golden-set eval in CI, in-browser demo for GitHub Pages
- Company website: pricing, docs, security, about, contact form, ROI calculator, legal pages
- Optional `API_KEY` auth and per-client rate limiting
- API extras: `/api/audit`, `/api/stale-documents`, `/api/questionnaires/{id}/gaps`

## How it works
`chunk -> retrieve (TF-IDF) -> draft (LLM or extractive) -> critic -> approve -> export`
- **Critic rules:** no citation = escalate; citation outside retrieved context = escalate; low source support = escalate;
  sensitive topics (breach, certifications, legal) always need human approval.

## Repo map
| Path | Purpose |
|---|---|
| `apps/api/core.py` | Pipeline: chunking, retrieval, drafting, critic, XLSX parse/export |
| `apps/api/main.py` | FastAPI endpoints and static UI |
| `apps/api/static/index.html` | Single-page review UI |
| `apps/api/agents/graph.py` | LangGraph skeleton (production path) |
| `apps/api/db/schema.sql` | Postgres + pgvector schema with row-level security (production path) |
| `site/` | Company website + live demo (GitHub Pages); regenerate with `python tools/build_site.py` |
| `eval/` | Golden-set evaluation |
| `docs/ROADMAP.md` | Advanced feature guide |
| `docs/DEPLOY_GITHUB_PAGES.md` | Pages deployment guide |
| `tests/` | Pipeline tests, run in CI |

## Status and limits
MVP: in-memory storage, no auth, TF-IDF retrieval. Not for real customer data until the production path in
`docs/ROADMAP.md` (auth, Postgres RLS, embeddings, zero-retention LLM) is done. See `SECURITY.md`.

## License
MIT (c) 2026 NIKHIL CHARY SRIRAMOJU
