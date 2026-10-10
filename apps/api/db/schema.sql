CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- App role: NOT the table owner, so RLS always applies.
CREATE ROLE qai_app LOGIN PASSWORD 'qai_app';

CREATE TABLE tenants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  plan text NOT NULL DEFAULT 'starter',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  doc_type text NOT NULL,            -- policy | evidence | past_answers
  title text,
  effective_date date,
  storage_path text,
  approved boolean DEFAULT true,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  text text NOT NULL,
  section_path text,
  metadata jsonb DEFAULT '{}',
  embedding vector(1536),            -- match your embedding model's dimension
  tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', text)) STORED
);
CREATE INDEX chunks_embedding_idx ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX chunks_tsv_idx ON chunks USING gin (tsv);

CREATE TABLE questionnaires (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  source_file text,
  status text DEFAULT 'uploaded',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  questionnaire_id uuid NOT NULL REFERENCES questionnaires(id) ON DELETE CASCADE,
  text text NOT NULL,
  category text,
  row_ref text                       -- e.g. sheet/row for export
);

CREATE TABLE answers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  question_id uuid NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
  draft text,
  confidence real,
  status text DEFAULT 'drafted',     -- drafted | escalated | approved | rejected
  citations jsonb DEFAULT '[]',
  reviewed_by text,
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE approved_answers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  question_text text NOT NULL,
  question_embedding vector(1536),
  answer text NOT NULL,
  source_ids jsonb DEFAULT '[]'
);
CREATE INDEX approved_embedding_idx ON approved_answers USING hnsw (question_embedding vector_cosine_ops);

CREATE TABLE agent_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  question_id uuid REFERENCES questions(id) ON DELETE CASCADE,
  tokens_in int, tokens_out int, cost_usd numeric(10,4),
  latency_ms int, revisions int, trace jsonb,
  created_at timestamptz DEFAULT now()
);

-- Row-level security on every tenant table
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['documents','chunks','questionnaires','questions',
                           'answers','approved_answers','agent_runs']
  LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', t);
    EXECUTE format(
      'CREATE POLICY tenant_isolation ON %I
         USING (tenant_id = current_setting(''app.tenant_id'', true)::uuid)
         WITH CHECK (tenant_id = current_setting(''app.tenant_id'', true)::uuid)', t);
  END LOOP;
END $$;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO qai_app;
-- Per request, the API runs:  SET LOCAL app.tenant_id = '<tenant uuid>';
