from pathlib import Path

from app.ingestion.document_loader import DocumentLoader


def test_document_loader_reads_protein_document():
    loader = DocumentLoader()

    path = Path("data/synthetic/synthetic_protein_001.json")

    document = loader.load(path)

    assert document
    assert "SYN-PROT-001" in document