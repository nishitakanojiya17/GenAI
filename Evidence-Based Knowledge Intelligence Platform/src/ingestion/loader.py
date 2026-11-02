from pathlib import Path

from pypdf import PdfReader


def load_documents(folder_path: str | Path) -> list[dict]:
    folder = Path(folder_path)
    documents = []

    if not folder.exists():
        raise FileNotFoundError(f"Document folder not found: {folder}")

    for file_path in sorted(folder.rglob("*")):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            reader = PdfReader(str(file_path))

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""

                if text.strip():
                    documents.append({
                        "text": text,
                        "source": str(file_path.relative_to(folder)),
                        "page": page_number,
                    })

        elif suffix == ".txt":
            text = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            if text.strip():
                documents.append({
                    "text": text,
                    "source": str(file_path.relative_to(folder)),
                    "page": 1,
                })

    return documents