from textwrap import shorten


def generate_answer(query: str, docs):
    if not docs:
        return "I couldn't find relevant context in the indexed dataset.", [], []

    evidence = []
    sources = []
    answer_points = []

    for idx, doc in enumerate(docs[:4], start=1):
        content = (doc.page_content or "").strip()
        if not content:
            continue
        src = doc.metadata.get("source", "unknown")
        if src not in sources:
            sources.append(src)
        snippet = shorten(content.replace("\n", " "), width=280, placeholder="...")
        evidence.append({"rank": idx, "source": src, "snippet": snippet})
        answer_points.append(f"- Evidence {idx}: {snippet}")

    if not answer_points:
        return "Relevant documents were retrieved, but no readable evidence was found.", sources, evidence

    answer = (
        f"Question: {query}\n\n"
        "Grounded answer based on retrieved context:\n"
        + "\n".join(answer_points)
        + "\n\nStarter behavior: this version is extractive and source-grounded. "
          "You can later replace this module with an LLM call for better synthesis and citations."
    )
    return answer, sources, evidence
