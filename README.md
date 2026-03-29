
<img width="2344" height="1463" alt="Screenshot 2026-03-29 132552" src="https://github.com/user-attachments/assets/f26618dd-abc0-4fbf-a0d6-2e8a84148a04" />
 
Built a small RAG system called ERC RAG Assistant aimed at research-style datasets. The idea is that you can drop documents like PDFs, CSVs or text files into a folder, and the app will clean them, chunk them, embed them with sentence-transformers, and index them in a FAISS vector store.

When a user asks a question, the system runs a semantic search over the index, pulls back the most relevant chunks and then generates a grounded answer that’s basically a structured summary of those chunks. The Streamlit UI shows three things: the answer, the list of source files, and expandable evidence cards with the actual retrieved snippets. That makes it easy to see where the answer came from and to debug retrieval quality.

I wrote the ingestion, chunking, retrieval and answer modules as separate components and added some smoke tests so I can safely change embedding models or chunking parameters later. It’s not a full LLM fine-tune yet, but it demonstrates that I can put together a working RAG pipeline over real documents end-to-end

1. Clone the repository
git clone https://github.com/itsadi96/erc-rag-assistant.git
cd erc-rag-assistant
2. Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
If pip is missing inside the venv:
python -m ensurepip --upgrade
3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
4. Add your dataPlace documents inside:
data/raw/
Supported types:
  • .txt
  • .md
  • .csv
  • .pdf
There is also a sample file:
data/raw/sample_research.txt
5. Build the FAISS index
$env:PYTHONPATH="."
python src/ingestion/build_index.py
You should see logs like:
  • Processed: data/raw/your_file.ext -> N chunks
  • Saved index with N chunks.
6. Run the Streamlit app
$env:PYTHONPATH="."
python -m streamlit run app/main.py
Streamlit will print a local URL, for example:
Local URL: http://localhost:8501
Open that in your browser, ask a question about your documents, and the app will:
  • retrieve relevant chunks via FAISS
  • generate a grounded answer
  • show sources and evidence snippetste a grounded answer
  • show sources and evidence snippets
