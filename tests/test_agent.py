from pathlib import Path

from app.db.repository import ProteinRepository
from app.ingestion.agent import KnowledgeConstructionAgent


def test_knowledge_construction_agent_processes_protein():
    repository = ProteinRepository()
    agent = KnowledgeConstructionAgent(repository=repository)

    path = Path("data/synthetic/synthetic_protein_001.json")

    result = agent.process(path)

    assert result.protein_id
    assert result.accession == "SYN-PROT-001"
    assert result.functions_count == 2
    assert result.domains_count == 1
    assert result.structures_count == 1
    assert result.evidence_count == 1

    retrieved = repository.get_by_accession("SYN-PROT-001")

    assert retrieved is not None
    assert retrieved.accession == "SYN-PROT-001"
    assert retrieved.name == "ATPase-X"
    assert retrieved.sequence
    assert retrieved.organism == "Synthetic benchmark organism"

    assert len(retrieved.functions) == 2
    assert len(retrieved.domains) == 1
    assert len(retrieved.structures) == 1
    assert len(retrieved.evidence) == 1