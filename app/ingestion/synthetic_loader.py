import json
import os
from pathlib import Path

from app.schemas.protein import ProteinRecord


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "data" / "synthetic" / "synthetic_protein_001.json"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://proteinmind:proteinmind_dev@localhost:5433/proteinmind",
)


def load_record() -> ProteinRecord:
    return ProteinRecord.model_validate_json(FIXTURE.read_text())


def ingest(record: ProteinRecord) -> None:
    import psycopg

    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO proteins (accession, name, sequence, length, organism, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (accession) DO UPDATE SET
                    name = EXCLUDED.name,
                    sequence = EXCLUDED.sequence,
                    length = EXCLUDED.length,
                    organism = EXCLUDED.organism,
                    description = EXCLUDED.description,
                    updated_at = NOW()
                RETURNING protein_id
                """,
                (record.accession, record.name, record.sequence, record.length,
                 record.organism, record.description),
            )
            protein_id = cur.fetchone()[0]

            for item in record.functions:
                cur.execute(
                    """
                    INSERT INTO protein_functions
                        (protein_id, function_type, function_text, go_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (protein_id, item.function_type, item.function_text, item.go_id),
                )

            for item in record.domains:
                cur.execute(
                    """
                    INSERT INTO protein_domains
                        (protein_id, domain_accession, domain_name,
                         start_position, end_position, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (protein_id, item.domain_accession, item.domain_name,
                     item.start_position, item.end_position, item.source),
                )

            for item in record.structures:
                cur.execute(
                    """
                    INSERT INTO protein_structures
                        (protein_id, structure_type, structure_accession, source, confidence)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (protein_id, item.structure_type, item.structure_accession,
                     item.source, item.confidence),
                )

            for item in record.evidence:
                cur.execute(
                    """
                    INSERT INTO evidence
                        (protein_id, source_type, source_id, source_uri,
                         claim, evidence_text, confidence, extraction_method)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (protein_id, item.source_type, item.source_id, item.source_uri,
                     item.claim, item.evidence_text, item.confidence,
                     item.extraction_method),
                )


def main() -> None:
    record = load_record()
    ingest(record)
    print(f"Ingested {record.accession}: {record.name} ({record.length} aa)")


if __name__ == "__main__":
    main()
