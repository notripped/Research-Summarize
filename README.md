# Research-Summarize
# AI Research Summarizer Agent

An intelligent research assistant that fetches top search results for your query, extracts and summarizes relevant content from webpages, and presents concise summaries in an easy-to-use web interface.

---

## Features

- Uses **Tavily Search API** to retrieve relevant URLs for research queries.
- Extracts main textual content from URLs using **trafilatura** to avoid unnecessary page elements like sidebars or ads.
- Summarizes extracted content with a transformer-based model (`facebook/bart-large-cnn`) via Hugging Face's **transformers** pipeline.
- FastAPI backend exposes a REST API for querying and summarizing.
- Streamlit frontend provides a clean, responsive user interface.
- CORS middleware enabled for cross-origin requests between frontend and backend.

---

## Demo

[Optional: Add a link or screenshot of your deployed app]

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/installation/)
- (Optional) Create and activate a virtual environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # Linux/macOS
  .venv\Scripts\activate     # Windows
