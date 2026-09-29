# ProteinMind-X

**Evidence-Augmented Protein Intelligence System**

ProteinMind-X is a research and engineering project for automated protein knowledge construction and evidence-grounded protein-function prediction.

## Current milestone: v0.1 — Knowledge Base Foundation

This milestone establishes:

- PostgreSQL as the source of truth for structured protein knowledge.
- Provenance-aware evidence records.
- A synthetic protein sandbox for controlled ingestion tests.
- A clean separation between structured knowledge and future vector retrieval.

### Planned architecture

```text
Biological APIs / Documents
          |
          v
   Agentic Ingestion
          |
   Extract -> Validate
          |
          v
  PostgreSQL Knowledge Base
          |
          +----> Embeddings / Vector Store
          |
          v
      Evidence RAG
          |
          v
 Protein Foundation Model
      + LoRA / QLoRA
          |
          v
 Function Prediction
```

## Repository layout

```text
proteinmind-x/
├── app/
│   ├── db/
│   │   └── schema.sql
│   ├── ingestion/
│   │   └── synthetic_loader.py
│   └── schemas/
│       └── protein.py
├── data/
│   └── synthetic/
│       └── synthetic_protein_001.json
├── scripts/
│   └── reset_db.sql
├── tests/
│   └── test_synthetic_record.py
├── docker-compose.yml
├── .env.example
├── .gitignore
└── pyproject.toml
```

## Run the database

```bash
docker compose up -d postgres
```

Check:

```bash
docker compose ps
```

## Initialize the schema

```bash
docker compose exec -T postgres psql -U proteinmind -d proteinmind < app/db/schema.sql
```

## Load the synthetic protein

```bash
python -m app.ingestion.synthetic_loader
```

The loader is intentionally deterministic and idempotent: running it more than once should not create duplicate protein/evidence records.

## Verify

```bash
docker compose exec postgres psql -U proteinmind -d proteinmind
```

Then:

```sql
SELECT protein_id, accession, name FROM proteins;
SELECT protein_id, source_type, source_id, claim FROM evidence;
```

## Important research principle

The synthetic record is **not biological evidence**. It exists only to validate the knowledge-construction and grounding workflow before connecting real sources such as UniProt, InterPro, Gene Ontology, RCSB PDB, AlphaFold DB, and Europe PMC/PubMed.

Every future biological claim should retain provenance: source, source identifier, retrieval timestamp, and the extracted claim.
