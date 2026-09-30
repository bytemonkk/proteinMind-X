import json
from typing import Any


class ProteinExtractor:
    """Extract structured protein information from a JSON document."""

    def extract(self, document: str) -> dict[str, Any]:
        try:
            data = json.loads(document)
        except json.JSONDecodeError as exc:
            raise ValueError("Document is not valid JSON") from exc

        return {
            "accession": data.get("accession"),
            "name": data.get("name"),
            "sequence": data.get("sequence"),
            "organism": data.get("organism"),
            "description": data.get("description"),
            "functions": data.get("functions", []),
            "domains": data.get("domains", []),
            "structures": data.get("structures", []),
            "evidence": data.get("evidence", []),
        }