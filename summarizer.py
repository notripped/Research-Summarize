import os
from dotenv import load_dotenv
from typing import List, Dict

from langchain_community.tools.tavily_search.tool import TavilySearchResults
import trafilatura
from transformers import pipeline

# Load environment variables
load_dotenv()

# Initialize summarizer once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Tavily search tool (top 5 results)
search_tool = TavilySearchResults(k=5)

def fetch_and_summarize(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            clean_text = trafilatura.extract(downloaded)
            if clean_text:
                summary = summarizer(clean_text[:3000], max_length=150, min_length=50, do_sample=False)
                return summary[0]['summary_text']
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    return "Failed to extract or summarize content."

def research_and_summarize(query: str) -> List[Dict[str, str]]:
    search_results = search_tool.run(query)
    summaries = []

    for result in search_results:
        url = result.get("url")
        if url:
            summary_text = fetch_and_summarize(url)
            summaries.append({
                "source": url,
                "summary": summary_text
            })

    return summaries
