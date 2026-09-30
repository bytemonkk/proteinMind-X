from pathlib import Path

import pytest
from pydantic import ValidationError

from app.ingestion.document_loader import DocumentLoader
from app.ingestion.extractor import ProteinExtractor
from app.ingestion.validator import ProteinValidator


def test_protein_validator_returns_protein_record():
    loader = DocumentLoader()
    extractor = ProteinExtractor()
    validator = ProteinValidator()

    path = Path("data/synthetic/synthetic_protein_001.json")

    document = loader.load(path)
    extracted = extractor.extract(document)
    record = validator.validate(extracted)

    assert record.accession == "SYN-PROT-001"
    assert record.name == "ATPase-X"
    assert record.sequence
    assert record.length == len(record.sequence)

    assert len(record.functions) == 2
    assert len(record.domains) == 1
    assert len(record.structures) == 1
    assert len(record.evidence) == 1


def test_protein_validator_rejects_invalid_protein():
    validator = ProteinValidator()

    invalid_data = {
        "accession": "INVALID-001",
        "name": "Invalid Protein",
        "sequence": "",
    }

    with pytest.raises(ValidationError):
        validator.validate(invalid_data)