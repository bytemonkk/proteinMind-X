from typing import Any

from app.schemas.protein import ProteinRecord


class ProteinValidator:
    """Validate extracted protein data against the canonical ProteinRecord schema."""

    def validate(self, data: dict[str, Any]) -> ProteinRecord:
        return ProteinRecord.model_validate(data)