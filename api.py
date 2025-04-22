
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import os
from summarise import summarise_text, extract_topics
from typing import List, Dict, Any, Optional
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def extract_news(company: str, num_articles: int = 5) -> List[Dict[str, Any]]:
    """
    Extracts news articles about a specific company from Google News.
    
    Args:
        company: The company name to search for
        num_articles: Number of articles to extract (default: 5)
        
    Returns:
        List of dictionaries containing article information
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = f"https://news.google.com/search?q={company}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_='MQsxIb')
        
        news_data = []
        for i, article in enumerate(articles[:num_articles]):
            if i >= num_articles:
                break
                
            # Extract title
            title_tag = article.find('h3', class_='ipQwMb')
            title = title_tag.text if title_tag else "No title found"
            
            # Extract URL
            link_tag = article.find('a')
            article_url = ""
            if link_tag and 'href' in link_tag.attrs:
                article_url = "https://news.google.com" + link_tag['href'][1:]
                
            # Extract source and time
            source_time = article.find('div', class_='SVJrMe')
            source = source_time.find('a').text if source_time and source_time.find('a') else "Unknown"
            time = source_time.find('time').text if source_time and source_time.find('time') else "Unknown"
            
            # Extract snippet
            snippet_tag = article.find('div', class_='GI74Re')
            snippet = snippet_tag.text if snippet_tag else "No snippet available"
            
            # Get full article content
            full_content = ""
            try:
                if article_url:
                    article_response = requests.get(article_url, headers=headers, timeout=5)
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    paragraphs = article_soup.find_all('p')
                    full_content = ' '.join([p.text for p in paragraphs])
            except:
                full_content = snippet
            
            # Summarize content
            summary = summarise_text(full_content if full_content else snippet)
            
            # Extract topics
            topics = extract_topics(full_content if full_content else snippet)
            
            news_data.append({
                "title": title,
                "source": source,
                "time": time,
                "snippet": snippet,
                "url": article_url,
                "summary": summary,
                "topics": topics
            })
            
        return news_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting news: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "News Summarizer API", "version": "1.0"}

@app.get("/news/{company}")
def get_news(company: str, num_articles: int = 5):
    try:
        news = extract_news(company, num_articles)
        return news
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For testing locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
