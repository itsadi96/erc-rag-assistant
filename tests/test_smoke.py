from src.ingestion.chunker import chunk_text
from src.llm.generator import generate_answer


class DummyDoc:
    def __init__(self, text, source):
        self.page_content = text
        self.metadata = {"source": source}


def test_chunker_returns_chunks():
    text = "This is a sample document. " * 100
    chunks = chunk_text(text, chunk_size=120, chunk_overlap=20)
    assert len(chunks) > 1


def test_generator_returns_sources_and_evidence():
    docs = [
        DummyDoc("ERC grants support frontier research in multiple domains.", "sample.txt"),
        DummyDoc("Datasets may include abstracts, funding notes, and metadata.", "meta.txt"),
    ]
    answer, sources, evidence = generate_answer("What does the dataset contain?", docs)
    assert "Grounded answer" in answer
    assert len(sources) == 2
    assert len(evidence) >= 1
