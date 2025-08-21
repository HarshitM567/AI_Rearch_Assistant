import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Research Companion", layout="wide")
st.title("🧠 AI Research Companion")

with st.sidebar:
    st.header("Ingest Paper")
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if st.button("Ingest PDF", use_container_width=True) and pdf:
        files = {"file": (pdf.name, pdf.getvalue(), "application/pdf")}
        with st.spinner("Indexing…"):
            r = requests.post(f"{BACKEND_URL}/ingest/pdf", files=files)
        if r.ok:
            data = r.json()
            st.success(f"Indexed {data['chunks_indexed']} chunks. Doc ID: {data['doc_id']}")
            st.session_state.setdefault("doc_id", data["doc_id"])
        else:
            st.error(r.text)

    st.divider()
    st.text_input("Doc ID (optional)", key="doc_id")
    top_k = st.slider("Top-K Context", 1, 10, 5)

st.subheader("Ask a question about your papers")
q = st.text_input("Your question", placeholder="What is the main contribution?")

if st.button("Ask") and q:
    with st.spinner("Thinking…"):
        r = requests.post(f"{BACKEND_URL}/query", json={
            "query": q,
            "top_k": top_k,
            "doc_id": st.session_state.get("doc_id") or None,
        })
    if r.ok:
        data = r.json()
        st.markdown("### Answer")
        st.write(data["answer"]) 
        st.markdown("### Sources")
        for s in data["sources"]:
            with st.expander(f"{s['doc_id']} — {s['chunk_id']} (p.{s['page']}) | score: {s['score']:.3f}"):
                st.write(s["text"]) 
    else:
        st.error(r.text)
