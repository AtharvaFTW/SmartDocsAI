import os
import pdfplumber
from sklearn.neighbors import NearestNeigbors
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,pipeline

EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL="google/flan-t5-base"


def extract_text(file):
    file_name=file.name.lower()
    if file_name.endswith("pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() or '' for page in pdf.pages])
    elif file_name.endswith("txt"):
        return file.read().decode("utf-8")
    else:
        return ""
    

def chunk_text(text,max_words=100):
    words=text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0,len(words),max_words)]

def embed_chunks(chunks,model):
    return model.encode(chunks,convert_to_tensor=False)

def build_knn_index(embeddings):
    knn=NearestNeighbors(n_neighbors=3,metric="cosine")
    knn.fit(embeddings)
    return knn

def search(query,chunks,embeddings,embedder,top_k=3):
    query_vec=embedder.encode([query])
    knn=build_knn_index(embeddings)
    _,I= index.search(query_vec, top_k)
    return [chunks[i]for i in I[0]]

def generate_prompt(context,query):
    return f"Answer the question based on the context below. \n\n Context:\n{context}\n\n Question: {query} \nAnswer:"

def answer_query(query,top_chunks,rag_pipeline):
    context="\n".join(top_chunks)
    prompt=generate_prompt(context,query)
    response=rag_pipeline(prompt,max_new_tokens=300,do_sample=False)[0]['generated_text']
    return response.strip()

def load_models():
    embedder=SentenceTransformer(EMBEDDING_MODEL)
    tokenizer=AutoTokenizer.from_pretrained(LLM_MODEL)
    model=AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)
    rag_pipeline=pipeline("text2text-generation",model=model,tokenizer=tokenizer)
    return embedder, rag_pipeline