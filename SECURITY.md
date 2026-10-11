# Security
Report vulnerabilities privately via GitHub Security Advisories or the Contact page. Do not open public issues for them.

## Implemented (v1.4.0)
- Email/password accounts: scrypt hashing, 10+ character passwords, signed 12-hour tokens, login rate limiting.
- Tenant id comes only from the verified token. In Postgres mode every query runs under row-level security
  (`SET LOCAL app.tenant_id`), and the app connects as a non-owner role with FORCE RLS.
- PII masking before LLM calls, audit log, file size limits, per-client rate limits.

## Before real customer data
- Have the tenant-isolation tests run against a real Postgres and reviewed independently.
- Set a strong `JWT_SECRET`, change the `qai_app` password, put the API behind HTTPS, set `ALLOW_REGISTER=0`.
- Add SSO, password reset, email verification, and a connection pool. Use zero-retention LLM settings.
