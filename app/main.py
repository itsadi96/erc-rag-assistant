import streamlit as st
from src.retrieval.vector_store import load_index
from src.llm.generator import generate_answer

st.set_page_config(
    page_title="ERC RAG Assistant",
    page_icon="📚",
    layout="wide",
)

# ---- GLOBAL STYLE ----
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    .answer-box {
        padding: 1rem 1.25rem;
        border-radius: 0.5rem;
        background-color: #111827;
        border: 1px solid #374151;
        font-size: 0.95rem;
    }
    .evidence-card {
        border-radius: 0.4rem;
        border: 1px solid #374151;
        background-color: #020617;
        padding: 0.6rem 0.8rem;
        font-size: 0.9rem;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
    }
    .small-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .pill-row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        border: 1px solid #374151;
        background-color: #020617;
        color: #9ca3af;
        font-size: 0.78rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- HEADER ----
st.title("📚 ERC RAG Assistant")
st.markdown(
    """
    <div class='pill-row'>
        <div class='pill'>🧠 Mode: RAG</div>
        <div class='pill'>📦 Backend: FAISS + sentence-transformers</div>
        <div class='pill'>📄 Inputs: TXT / CSV / PDF</div>
    </div>
    <p class='subtitle'>Ask questions over your indexed research documents. The assistant retrieves
    relevant chunks and shows you where the answer comes from.</p>
    """,
    unsafe_allow_html=True,
)

# ---- SIDEBAR ----
with st.sidebar:
    st.header("About")
    st.write(
        "This app retrieves relevant chunks from your indexed documents and returns "
        "a grounded answer with sources and evidence."
    )
    st.info("1. Put your files in `data/raw/`\n2. Run the index builder\n3. Ask questions here.")

# ---- INPUT ----
query = st.text_input(
    "Ask a question about the indexed documents",
    placeholder="e.g. What topics does this book cover?",
)

k = st.slider("Top‑K retrieval", min_value=2, max_value=8, value=4)

go = st.button("Search & Answer", type="primary")

# ---- MAIN ----
if go:
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            db = load_index()
            docs = db.similarity_search(query, k=k)
            answer, sources, evidence = generate_answer(query, docs)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("Answer")
                st.markdown(
                    f"<div class='small-label'>Question</div><div class='answer-box'>{query}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<div class='small-label' style='margin-top:0.75rem;'>Grounded answer</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)

            with col2:
                st.subheader("Sources")
                if not sources:
                    st.write("No sources found.")
                else:
                    for src in sources:
                        st.write(f"- `{src}`")

            st.markdown("### Retrieved Evidence")
            if not evidence:
                st.write("No evidence snippets available.")
            else:
                for item in evidence:
                    with st.expander(
                        f"Evidence {item['rank']} · {item['source']}",
                        expanded=(item["rank"] == 1),
                    ):
                        st.markdown(
                            f"<div class='evidence-card'>{item['snippet']}</div>",
                            unsafe_allow_html=True,
                        )

        except Exception as e:
            st.error(str(e))
