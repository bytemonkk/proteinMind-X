from pathlib import Path


class DocumentLoader:
    """Loads a protein document from disk."""

    def load(self, path: str | Path) -> str:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        return file_path.read_text(encoding="utf-8")