# Roadmap: from MVP to production
Designed and developed by NIKHIL CHARY SRIRAMOJU

## Stage 1: Make it real (weeks 1-3)
1. **Auth + tenants (done in 1.4.0: email/password; SSO still to do):** Clerk/Auth0 JWT; derive tenant from the token, never from a header.
2. **Postgres + RLS (done in 1.4.0; needs independent testing):** apply `apps/api/db/schema.sql`; `SET LOCAL app.tenant_id` per request; replace `STORE`.
3. **Embeddings + hybrid search:** pgvector + Postgres full-text, reciprocal rank fusion, cross-encoder rerank.
4. **LangGraph:** wire `agents/graph.py` to the real functions; Postgres checkpointer for resumable jobs.
5. **Async jobs:** Celery/ARQ + progress via SSE; limits per tenant.
6. **Answer library:** save approved answers; reuse before retrieval.

## Stage 2: Trust and compliance (weeks 3-8)
- PII masking before LLM calls; zero-retention provider settings; audit log of approvals.
- Prompt-injection defenses: questionnaire text is data, never instructions.
- Eval suite (Ragas/Phoenix) with a golden set; CI blocks releases that lower faithfulness.
- Trust page; start SOC 2 only after paying customers justify it.

## Stage 3: Advanced features
| Feature | What it adds | Approach |
|---|---|---|
| Integrations | Evidence from Drata, Vanta, Drive, Notion, Confluence | Connectors that sync docs into the index |
| Evidence freshness | Warns when policies are stale | `effective_date` + review-cycle rules |
| Multi-format export | Portals (OneTrust, Whistic), Word, PDF | Format adapters behind one interface |
| Confidence calibration | Fewer unnecessary escalations | Learn from reviewer approve/edit data |
| Contradiction detection | Catches answers that conflict across questionnaires | Compare new drafts against approved library |
| Browser agent | Fills buyer portals directly | Computer-use agent plus mandatory human sign-off |
| Voice/Slack review | Approve from chat | Slack app posting escalations |
| Gap analysis | "Controls you lack that buyers keep asking about" | Aggregate escalation reasons |
| Local/private models | Customers who forbid cloud LLMs | Self-hosted open model behind the same interface |
| Verifiable audit trail | Tamper-evident approvals | Hash-chained log, optional signed exports |

## Stage 4: Business layer
Stripe billing per questionnaire, usage dashboard, admin panel, trust center, referral program for auditors.

## Research ideas (stand out technically)
Provenance-aware answers (sentence-level citations), self-consistency checks, active learning from edits,
privacy-preserving cross-tenant benchmarks (aggregate only, opt-in).
