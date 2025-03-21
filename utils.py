import requests
from bs4 import BeautifulSoup
import os 
from summarise import summarise_text
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyzes the sentiment of a given text (summary) and returns Positive, Negative, or Neutral."""
    sentiment_score = sia.polarity_scores(text)["compound"]  # Compound score

    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def fetch_article_content(url):
    """Fetches the title and summary from a news article URL using BeautifulSoup."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.find('h1')
        title = title.get_text(strip=True) if title else "No title found"

        # Extract summary (first 3 paragraphs)
        paragraphs = soup.find_all('p')
        full_text = " ".join([p.get_text(strip=True) for p in paragraphs])

        summarized_text = summarise_text(full_text)

        sentiment = analyze_sentiment(summarized_text)

        return {"title": title, "summary": summarized_text, "sentiment": sentiment, "url": url}

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def extract_news(company_name):
    """Fetches 10 news articles using NewsAPI and scrapes their content."""
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = []
        for item in data["articles"][:10]:  # Get 10 articles
            article_url = item["url"]
            article_content = fetch_article_content(article_url)  # Scrape the article page
            if article_content:
                articles.append(article_content)

        return {"Company": company_name, "Articles": articles}

    except Exception as e:
        print(f"Error fetching news for {company_name}: {e}")
        return {"Company": company_name, "Articles": []}