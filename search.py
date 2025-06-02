import os
from typing import TypedDict, List
from dotenv import load_dotenv

from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader

# === Load environment variables ===
load_dotenv()
import trafilatura
from transformers import pipeline

# Load summarization pipeline (you can also load this once globally)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_and_summarize(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        clean_text = trafilatura.extract(downloaded)
        if clean_text:
            # Summarize the text (trimming to max 1024 tokens)
            summary = summarizer(clean_text[:3000], max_length=150, min_length=50, do_sample=False)
            return summary[0]['summary_text']
    return "Failed to extract or summarize content."

# === Define State ===
class ResearchState(TypedDict):
    query: str
    notes: List  # List of Documents

# === Search Tool Setup ===
search_tool = TavilySearchResults(k=5)

# === Research Agent ===
def research_agent(state: ResearchState) -> ResearchState:
    query = state["query"]
    search_results = search_tool.run(query)
    documents = []

    for result in search_results:
        url = result.get("url")
        if url:
            try:
                summary_text = fetch_and_summarize(url)
                if summary_text:
                    documents.append({
                        "summary": summary_text,
                        "source": url
                    })
            except Exception as e:
                print(f"Failed to summarize {url}: {e}")

    return {"query": query, "notes": documents}

# === Run It ===
if __name__ == "__main__":
    query = "Risks of using AI-generated passwords in secure systems"
    research_output = research_agent({"query": query, "notes": []})

    print("\n=== Retrieved Documents ===\n")
    for idx, doc in enumerate(research_output["notes"]):
        print(f"\n--- Document {idx + 1} ---")
        print(f"Source: {doc.get('source', 'N/A')}")
        print(f"Summary: {doc.get('summary', 'No summary available.')}")

