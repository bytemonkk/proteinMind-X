# from pathlib import Path

# from app.db.repository import ProteinRepository
# from app.ingestion.document_loader import DocumentLoader
# from app.ingestion.extractor import ProteinExtractor
# from app.ingestion.validator import ProteinValidator


# def test_protein_repository_persists_and_retrieves_complete_record():
#     loader = DocumentLoader()
#     extractor = ProteinExtractor()
#     validator = ProteinValidator()
#     repository = ProteinRepository()

#     path = Path("data/synthetic/synthetic_protein_001.json")

#     document = loader.load(path)
#     extracted = extractor.extract(document)
#     record = validator.validate(extracted)

#     protein_id = repository.save(record)

#     assert protein_id

#     retrieved = repository.get_by_accession("SYN-PROT-001")

#     assert retrieved is not None

#     # Core identity
#     assert retrieved.accession == record.accession
#     assert retrieved.name == record.name
#     assert retrieved.sequence == record.sequence
#     assert retrieved.organism == record.organism
#     assert retrieved.description == record.description
#     assert retrieved.length == record.length

#     # Functions
#     # Functions
#     assert len(retrieved.functions) == 2

#     function_map = {
#         item.function_type: item.function_text
#         for item in retrieved.functions
#     }

#     assert function_map["molecular_function"] == "ATP binding"
#     assert function_map["biological_process"] == "membrane transport"

#     # Domains
#     assert len(retrieved.domains) == 1
#     assert retrieved.domains[0].domain_accession == "SYN-DOM-001"
#     assert retrieved.domains[0].domain_name == "Synthetic ABC-type ATPase domain"
#     assert retrieved.domains[0].start_position == 18
#     assert retrieved.domains[0].end_position == 58

#     # Structures
#     assert len(retrieved.structures) == 1
#     assert retrieved.structures[0].structure_accession == "SYN-STRUCT-001"
#     assert retrieved.structures[0].confidence == 1.0

#     # Evidence / provenance
#     assert len(retrieved.evidence) == 1
#     assert retrieved.evidence[0].source_type == "synthetic_document"
#     assert retrieved.evidence[0].source_id == "synthetic_protein_001.json"
#     assert retrieved.evidence[0].confidence == 1.0
#     assert retrieved.evidence[0].extraction_method == "synthetic_fixture"
    


from pathlib import Path

from app.db.repository import ProteinRepository
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.extractor import ProteinExtractor
from app.ingestion.validator import ProteinValidator


def test_protein_repository_persists_and_retrieves_complete_record():
    loader = DocumentLoader()
    extractor = ProteinExtractor()
    validator = ProteinValidator()
    repository = ProteinRepository()

    path = Path("data/synthetic/synthetic_protein_001.json")

    document = loader.load(path)
    extracted = extractor.extract(document)
    record = validator.validate(extracted)

    protein_id = repository.save(record)

    assert protein_id

    retrieved = repository.get_by_accession("SYN-PROT-001")

    assert retrieved is not None

    # Core identity
    assert retrieved.accession == record.accession
    assert retrieved.name == record.name
    assert retrieved.sequence == record.sequence
    assert retrieved.organism == record.organism
    assert retrieved.description == record.description
    assert retrieved.length == record.length

    # Functions
    assert len(retrieved.functions) == 2

    function_map = {
        item.function_type: item.function_text
        for item in retrieved.functions
    }

    assert function_map["molecular_function"] == "ATP binding"
    assert function_map["biological_process"] == "membrane transport"

    # Domains
    assert len(retrieved.domains) == 1
    assert retrieved.domains[0].domain_accession == "SYN-DOM-001"
    assert retrieved.domains[0].domain_name == "Synthetic ABC-type ATPase domain"
    assert retrieved.domains[0].start_position == 18
    assert retrieved.domains[0].end_position == 58

    # Structures
    assert len(retrieved.structures) == 1
    assert retrieved.structures[0].structure_accession == "SYN-STRUCT-001"
    assert retrieved.structures[0].confidence == 1.0

    # Evidence / provenance
    assert len(retrieved.evidence) == 1
    assert retrieved.evidence[0].source_type == "synthetic_document"
    assert retrieved.evidence[0].source_id == "synthetic_protein_001.json"
    assert retrieved.evidence[0].confidence == 1.0
    assert retrieved.evidence[0].extraction_method == "synthetic_fixture"


def test_protein_repository_is_idempotent():
    loader = DocumentLoader()
    extractor = ProteinExtractor()
    validator = ProteinValidator()
    repository = ProteinRepository()

    path = Path("data/synthetic/synthetic_protein_001.json")

    document = loader.load(path)
    extracted = extractor.extract(document)
    record = validator.validate(extracted)

    # Simulate repeated ingestion / job retries.
    repository.save(record)
    repository.save(record)
    repository.save(record)

    retrieved = repository.get_by_accession("SYN-PROT-001")

    assert retrieved is not None

    # The same protein should still exist only once logically.
    assert retrieved.accession == "SYN-PROT-001"

    # Repeated saves must not create duplicate annotations.
    assert len(retrieved.functions) == 2
    assert len(retrieved.domains) == 1
    assert len(retrieved.structures) == 1
    assert len(retrieved.evidence) == 1