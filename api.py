from fastapi import FastAPI
from utils import extract_news

app = FastAPI()

@app.get("/")
def home():
    return {"message": "News Summarizer API is running!"}

@app.get("/news/{company_name}")
def get_news(company_name: str):
    """Fetch news, summarize, analyze sentiment, and return JSON response."""
    news_data = extract_news(company_name)
    return news_data
