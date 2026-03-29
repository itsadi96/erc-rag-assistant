from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def save_index(chunks, metadatas, output_dir: str = "vectorstore"):
    embeddings = get_embeddings()
    db = FAISS.from_texts(chunks, embeddings, metadatas=metadatas)
    db.save_local(output_dir)
    return db


def load_index(index_dir: str = "vectorstore"):
    embeddings = get_embeddings()
    if not Path(index_dir).exists():
        raise FileNotFoundError("Vector index not found. Run ingestion first.")
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
