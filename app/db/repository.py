import os

import psycopg

from app.schemas.protein import ProteinRecord

from app.config import DATABASE_URL


class ProteinRepository:
    """Persistence layer for ProteinRecord objects."""

    def __init__(self, database_url: str = DATABASE_URL):
        self.database_url = database_url

    def save(self, record: ProteinRecord) -> str:
        """Persist a complete ProteinRecord and return its database ID."""

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:

                # 1. Store the core protein entity.
                cur.execute(
                    """
                    INSERT INTO proteins (
                        accession,
                        name,
                        sequence,
                        length,
                        organism,
                        description
                    )
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
                    (
                        record.accession,
                        record.name,
                        record.sequence,
                        record.length,
                        record.organism,
                        record.description,
                    ),
                )

                protein_id = cur.fetchone()[0]

                # 2. Store function annotations.
                for item in record.functions:
                    cur.execute(
                        """
                        INSERT INTO protein_functions (
                            protein_id,
                            function_type,
                            function_text,
                            go_id
                        )
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            protein_id,
                            item.function_type,
                            item.function_text,
                            item.go_id,
                        ),
                    )

                # 3. Store domain annotations.
                for item in record.domains:
                    cur.execute(
                        """
                        INSERT INTO protein_domains (
                            protein_id,
                            domain_accession,
                            domain_name,
                            start_position,
                            end_position,
                            source
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            protein_id,
                            item.domain_accession,
                            item.domain_name,
                            item.start_position,
                            item.end_position,
                            item.source,
                        ),
                    )

                # 4. Store structure annotations.
                for item in record.structures:
                    cur.execute(
                        """
                        INSERT INTO protein_structures (
                            protein_id,
                            structure_type,
                            structure_accession,
                            source,
                            confidence
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            protein_id,
                            item.structure_type,
                            item.structure_accession,
                            item.source,
                            item.confidence,
                        ),
                    )

                # 5. Store evidence/provenance.
                for item in record.evidence:
                    cur.execute(
                        """
                        INSERT INTO evidence (
                            protein_id,
                            source_type,
                            source_id,
                            source_uri,
                            claim,
                            evidence_text,
                            confidence,
                            extraction_method
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            protein_id,
                            item.source_type,
                            item.source_id,
                            item.source_uri,
                            item.claim,
                            item.evidence_text,
                            item.confidence,
                            item.extraction_method,
                        ),
                    )

                return str(protein_id)
    
    def get_by_accession(self, accession: str) -> ProteinRecord | None:
        """Retrieve a complete ProteinRecord by accession."""

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cur:

                # 1. Retrieve the core protein.
                cur.execute(
                    """
                    SELECT
                        protein_id,
                        accession,
                        name,
                        sequence,
                        organism,
                        description
                    FROM proteins
                    WHERE accession = %s
                    """,
                    (accession,),
                )

                protein = cur.fetchone()

                if protein is None:
                    return None

                (
                    protein_id,
                    accession,
                    name,
                    sequence,
                    organism,
                    description,
                ) = protein

                # 2. Retrieve function annotations.
                cur.execute(
                    """
                    SELECT
                        function_type,
                        function_text,
                        go_id
                    FROM protein_functions
                    WHERE protein_id = %s
                    ORDER BY function_id
                    """,
                    (protein_id,),
                )

                functions = [
                    {
                        "function_type": row[0],
                        "function_text": row[1],
                        "go_id": row[2],
                    }
                    for row in cur.fetchall()
                ]

                # 3. Retrieve domain annotations.
                cur.execute(
                    """
                    SELECT
                        domain_accession,
                        domain_name,
                        start_position,
                        end_position,
                        source
                    FROM protein_domains
                    WHERE protein_id = %s
                    ORDER BY domain_id
                    """,
                    (protein_id,),
                )

                domains = [
                    {
                        "domain_accession": row[0],
                        "domain_name": row[1],
                        "start_position": row[2],
                        "end_position": row[3],
                        "source": row[4],
                    }
                    for row in cur.fetchall()
                ]

                # 4. Retrieve structure annotations.
                cur.execute(
                    """
                    SELECT
                        structure_type,
                        structure_accession,
                        source,
                        confidence
                    FROM protein_structures
                    WHERE protein_id = %s
                    ORDER BY structure_id
                    """,
                    (protein_id,),
                )

                structures = [
                    {
                        "structure_type": row[0],
                        "structure_accession": row[1],
                        "source": row[2],
                        "confidence": row[3],
                    }
                    for row in cur.fetchall()
                ]

                # 5. Retrieve evidence/provenance.
                cur.execute(
                    """
                    SELECT
                        source_type,
                        source_id,
                        source_uri,
                        claim,
                        evidence_text,
                        confidence,
                        extraction_method
                    FROM evidence
                    WHERE protein_id = %s
                    ORDER BY evidence_id
                    """,
                    (protein_id,),
                )

                evidence = [
                    {
                        "source_type": row[0],
                        "source_id": row[1],
                        "source_uri": row[2],
                        "claim": row[3],
                        "evidence_text": row[4],
                        "confidence": row[5],
                        "extraction_method": row[6],
                    }
                    for row in cur.fetchall()
                ]

                return ProteinRecord(
                    accession=accession,
                    name=name,
                    sequence=sequence,
                    organism=organism,
                    description=description,
                    functions=functions,
                    domains=domains,
                    structures=structures,
                    evidence=evidence,
                )