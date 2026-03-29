from pathlib import Path
from src.ingestion.document_loader import load_document
from src.ingestion.chunker import chunk_text
from src.retrieval.vector_store import save_index

RAW_DIR = Path("data/raw")


def main():
    chunks = []
    metadatas = []

    files = list(RAW_DIR.glob("**/*"))
    files = [f for f in files if f.is_file()]

    if not files:
        print("No files found in data/raw")
        return

    for file in files:
        text = load_document(file)
        if not text.strip():
            continue
        text_chunks = chunk_text(text)
        chunks.extend(text_chunks)
        metadatas.extend([{"source": str(file)} for _ in text_chunks])
        print(f"Processed: {file} -> {len(text_chunks)} chunks")

    if not chunks:
        print("No chunks created.")
        return

    save_index(chunks, metadatas)
    print(f"Saved index with {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
