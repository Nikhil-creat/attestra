# Security
Report vulnerabilities privately via GitHub Security Advisories on the repository. Do not open public issues for them.
Current limits: in-memory storage, header-based tenant selection (demo only, no auth). Do not expose publicly or load
real customer data until auth, Postgres RLS (db/schema.sql) and zero-retention LLM settings are in place.
