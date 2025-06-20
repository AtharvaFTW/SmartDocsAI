# SmartDocsAI

SmartDocsAI is an intelligent document Q&A assistant that allows users to upload PDFs or text files and ask questions based on their contents. It leverages MiniLM embeddings for semantic understanding and uses Google's FLAN-T5 model to generate answers grounded in the provided document context.

---

## 🚀 Features

- 📄 Upload `.pdf` or `.txt` files
- 🧠 Chunk and embed document content with `MiniLM`
- 🔍 Retrieve relevant chunks using `FAISS`
- 🤖 Generate context-aware answers using `FLAN-T5`
- 🖥️ Streamlit-powered interactive web UI

---

## 🔧 Tech Stack

- **Frontend/UI**: Streamlit
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: `google/flan-t5-base`
- **Vector Store**: FAISS
- **OCR**: pdfplumber (for PDF text extraction)

---

## 🛠️ Installation

> Ensure Python 3.10 is installed (not 3.11+ due to some package compatibility)

```bash
# Clone the repo
git clone https://github.com/AtharvaFTW/SmartDocsAI.git
cd SmartDocsAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 📦Major Dependencies

```txt
streamlit>=1.26.0
pdfplumber
scikit-learn
sentence-transformers==2.2.2
transformers==4.24.0
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Once the app launches:

1. Upload a `.pdf` or `.txt` document.
2. Enter your question in the input box.
3. View generated answers along with document context.

---

## 📁 Project Structure

```
SmartDocsAI/
├── app.py                 # Main Streamlit app
├── utils.py               # Core logic: embedding, FAISS, RAG
├── requirements.txt       # Project dependencies
└── README.md              # You're here
```

---

## 🧠 How It Works

1. **Text Extraction**: Extracts raw text from uploaded PDFs using `pdfplumber`.
2. **Chunking**: Breaks down the text into manageable chunks (100 words each).
3. **Embedding**: Each chunk is embedded via `MiniLM`.
4. **Indexing**: Chunks are indexed in a FAISS vector store.
5. **Search**: Query is embedded and top relevant chunks are retrieved.
6. **Answer Generation**: A prompt is created using those chunks and passed to `FLAN-T5` to generate a final answer.

---

## 🧪 Example Prompt

```text
Answer the question based on the context below.

Context:
<retrieved document chunks>

Question: <your question>
Answer:
```

---

## 📌 Notes

- For best performance, avoid uploading scanned images — pdfplumber works with actual text.
- All processing is local. No cloud APIs are involved.
- Currently supports only `.pdf` and `.txt` files.

---

## 📜 License

MIT License. See `LICENSE` file.

---

## 🤝 Contributions

Feel free to open issues or submit PRs. Ideas welcome!

