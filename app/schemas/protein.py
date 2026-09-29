from pydantic import BaseModel, Field


class FunctionAnnotation(BaseModel):
    function_type: str
    function_text: str
    go_id: str | None = None


class DomainAnnotation(BaseModel):
    domain_accession: str | None = None
    domain_name: str
    start_position: int | None = Field(default=None, ge=1)
    end_position: int | None = Field(default=None, ge=1)
    source: str


class StructureAnnotation(BaseModel):
    structure_type: str
    structure_accession: str
    source: str
    confidence: float | None = Field(default=None, ge=0, le=1)


class EvidenceAnnotation(BaseModel):
    source_type: str
    source_id: str
    source_uri: str | None = None
    claim: str
    evidence_text: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    extraction_method: str


class ProteinRecord(BaseModel):
    accession: str
    name: str
    sequence: str = Field(min_length=1)
    organism: str | None = None
    description: str | None = None
    functions: list[FunctionAnnotation] = Field(default_factory=list)
    domains: list[DomainAnnotation] = Field(default_factory=list)
    structures: list[StructureAnnotation] = Field(default_factory=list)
    evidence: list[EvidenceAnnotation] = Field(default_factory=list)

    @property
    def length(self) -> int:
        return len(self.sequence)
