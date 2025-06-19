import streamlit as st
import tempfile
from utils import extract_text, chunk_text, embed_chunks, load_models, search, answer_query

st.set_page_config(page_title="SmartDocsAI", layout="wide")
st.title("📄 SmartDocAI - Chat with Your Documents!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None
if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "embedder" not in st.session_state or "rag_pipeline" not in st.session_state:
    st.session_state.embedder, st.session_state.rag_pipeline = load_models()

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Processing file..."):
        raw_text = extract_text(uploaded_file)
        chunks = chunk_text(raw_text)
        embeddings = embed_chunks(chunks, st.session_state.embedder)

        # Store chunks and embeddings
        st.session_state.chunks = chunks
        st.session_state.embeddings = embeddings

    st.success("✅ File processed. You can now ask questions below.")

if st.session_state.chunks:
    st.markdown("---")
    st.subheader("🧠 Ask something about the document:")

    with st.form("chat_form", clear_on_submit=True):
        user_query = st.text_input("Your question:", key="user_query")
        submitted = st.form_submit_button("Ask", use_container_width=False,)

        if submitted and user_query:
            with st.spinner("Thinking..."):
                top_chunks = search(user_query, st.session_state.chunks, st.session_state.embeddings, st.session_state.embedder)
                response = answer_query(user_query, top_chunks, st.session_state.rag_pipeline)
                st.session_state.chat_history.append((user_query, response))

    # --- Display Chat ---
    chat_container = st.container()
    with chat_container:
        for q, a in st.session_state.chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**SmartDocAI:** {a}")
else:
    st.info("📂 Please upload a file to begin.")