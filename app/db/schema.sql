CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS proteins (
    protein_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    accession TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    sequence TEXT NOT NULL,
    length INTEGER NOT NULL CHECK (length > 0),
    organism TEXT,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS protein_functions (
    function_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protein_id UUID NOT NULL REFERENCES proteins(protein_id) ON DELETE CASCADE,
    function_type TEXT NOT NULL,
    function_text TEXT NOT NULL,
    go_id TEXT,
    evidence_id UUID,
    UNIQUE NULLS NOT DISTINCT (protein_id, function_type, function_text, go_id)
);

CREATE TABLE IF NOT EXISTS protein_domains (
    domain_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protein_id UUID NOT NULL REFERENCES proteins(protein_id) ON DELETE CASCADE,
    domain_accession TEXT,
    domain_name TEXT NOT NULL,
    start_position INTEGER,
    end_position INTEGER,
    source TEXT NOT NULL,
    UNIQUE (protein_id, domain_accession, domain_name, start_position, end_position)
);

CREATE TABLE IF NOT EXISTS protein_structures (
    structure_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protein_id UUID NOT NULL REFERENCES proteins(protein_id) ON DELETE CASCADE,
    structure_type TEXT NOT NULL,
    structure_accession TEXT NOT NULL,
    source TEXT NOT NULL,
    confidence REAL,
    UNIQUE (protein_id, structure_type, structure_accession, source)
);

CREATE TABLE IF NOT EXISTS literature (
    literature_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protein_id UUID NOT NULL REFERENCES proteins(protein_id) ON DELETE CASCADE,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    title TEXT,
    abstract TEXT,
    published_at DATE,
    UNIQUE (protein_id, source, source_id)
);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protein_id UUID NOT NULL REFERENCES proteins(protein_id) ON DELETE CASCADE,
    source_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_uri TEXT,
    claim TEXT NOT NULL,
    evidence_text TEXT,
    confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    extraction_method TEXT NOT NULL,
    retrieved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (protein_id, source_type, source_id, claim)
);

CREATE INDEX IF NOT EXISTS idx_evidence_protein_id ON evidence(protein_id);
CREATE INDEX IF NOT EXISTS idx_evidence_source ON evidence(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_functions_protein_id ON protein_functions(protein_id);
CREATE INDEX IF NOT EXISTS idx_domains_protein_id ON protein_domains(protein_id);
CREATE INDEX IF NOT EXISTS idx_literature_protein_id ON literature(protein_id);
