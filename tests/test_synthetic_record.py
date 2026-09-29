from app.ingestion.synthetic_loader import load_record


def test_synthetic_fixture_has_required_identity():
    record = load_record()
    assert record.accession == "SYN-PROT-001"
    assert record.name == "ATPase-X"
    assert record.length == len(record.sequence)


def test_synthetic_fixture_contains_provenance():
    record = load_record()
    assert record.evidence
    assert record.evidence[0].source_type == "synthetic_document"
    assert record.evidence[0].source_id == "synthetic_protein_001.json"


def test_synthetic_fixture_contains_multiple_biological_views():
    record = load_record()
    assert {item.function_type for item in record.functions} == {
        "molecular_function",
        "biological_process",
    }
    assert record.domains
    assert record.structures
