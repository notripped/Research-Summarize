import streamlit as st
import requests

st.set_page_config(page_title="AI Research Summarizer", layout="centered")

st.title("🔍 AI Research Summarizer")
query = st.text_input("Enter your research query:")

if st.button("Search & Summarize") and query:
    with st.spinner("Fetching summaries..."):
        try:
            response = requests.post(
                "http://localhost:8000/api/research",
                json={"query": query},
                timeout=600
            )
            response.raise_for_status()
            data = response.json()
            for idx, item in enumerate(data.get("results", [])):
                st.subheader(f"🔗 Source {idx + 1}")
                st.markdown(f"[{item['source']}]({item['source']})")
                st.write(item["summary"])
        except Exception as e:
            st.error(f"Error: {e}")
