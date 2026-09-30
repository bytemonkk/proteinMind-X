from pathlib import Path

from app.ingestion.document_loader import DocumentLoader
from app.ingestion.extractor import ProteinExtractor


def test_protein_extractor_extracts_structured_data():
    loader = DocumentLoader()
    extractor = ProteinExtractor()

    path = Path("data/synthetic/synthetic_protein_001.json")

    document = loader.load(path)
    result = extractor.extract(document)

    assert result["accession"] == "SYN-PROT-001"
    assert result["name"] == "ATPase-X"
    assert result["sequence"]
    assert result["organism"]
    assert result["description"]

    assert isinstance(result["functions"], list)
    assert isinstance(result["domains"], list)
    assert isinstance(result["structures"], list)
    assert isinstance(result["evidence"], list)

    assert len(result["functions"]) == 2
    assert len(result["domains"]) == 1
    assert len(result["structures"]) == 1
    assert len(result["evidence"]) == 1