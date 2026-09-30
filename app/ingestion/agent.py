from pathlib import Path

from pydantic import BaseModel

from app.db.repository import ProteinRepository
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.extractor import ProteinExtractor
from app.ingestion.validator import ProteinValidator


class ConstructionResult(BaseModel):
    """Summary of a completed protein knowledge-construction operation."""

    protein_id: str
    accession: str
    functions_count: int
    domains_count: int
    structures_count: int
    evidence_count: int


class KnowledgeConstructionAgent:
    """Orchestrates the protein knowledge-construction pipeline."""

    def __init__(
        self,
        loader: DocumentLoader | None = None,
        extractor: ProteinExtractor | None = None,
        validator: ProteinValidator | None = None,
        repository: ProteinRepository | None = None,
    ):
        self.loader = loader or DocumentLoader()
        self.extractor = extractor or ProteinExtractor()
        self.validator = validator or ProteinValidator()
        self.repository = repository or ProteinRepository()

    def process(self, path: str | Path) -> ConstructionResult:
        """Load, extract, validate, persist, and report a protein."""

        # 1. Load the raw document.
        document = self.loader.load(path)

        # 2. Extract structured protein data.
        extracted = self.extractor.extract(document)

        # 3. Validate against the canonical ProteinRecord schema.
        record = self.validator.validate(extracted)

        # 4. Persist the validated record.
        protein_id = self.repository.save(record)

        # 5. Return a structured construction summary.
        return ConstructionResult(
            protein_id=protein_id,
            accession=record.accession,
            functions_count=len(record.functions),
            domains_count=len(record.domains),
            structures_count=len(record.structures),
            evidence_count=len(record.evidence),
        )