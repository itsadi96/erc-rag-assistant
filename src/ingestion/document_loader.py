from pathlib import Path
import pandas as pd
from pypdf import PdfReader


def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def load_csv(path: Path) -> str:
    df = pd.read_csv(path)
    return df.to_string(index=False)


def load_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return load_txt(path)
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix == ".csv":
        return load_csv(path)
    return "" 
