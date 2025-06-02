from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import research_and_summarize

app = FastAPI()
def read_root():
    return {"message": "App is live!"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://streamlit-frontend.onrender.com"]
,  # allow frontend (like Streamlit) to call this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class QueryRequest(BaseModel):
    query: str

@app.post("/api/research")
async def get_summary(request: QueryRequest):
    results = research_and_summarize(request.query)
    return {"results": results}

import os

port = int(os.environ.get("PORT", 8000))  # fallback to 8000 if PORT is not set

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)