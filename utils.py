import requests
from bs4 import BeautifulSoup
import os
from summarise import summarise_text, extract_topics
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
from deep_translator import GoogleTranslator
import base64

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text (summary) and returns 
    Positive, Negative, or Neutral based on the compound score.
    """
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def fetch_article_content(url):
    """
    Fetches the title and summary from a news article URL using BeautifulSoup.
    Summarizes the full text via Gemini API, extracts key topics, and analyzes sentiment.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        paragraphs = soup.find_all('p')
        full_text = " ".join([p.get_text(strip=True) for p in paragraphs])

        summarized_text = summarise_text(full_text)
        topics = extract_topics(summarized_text)

        sentiment = analyze_sentiment(summarized_text)

        return {
            "title": title,
            "summary": summarized_text,
            "topics": topics,
            "sentiment": sentiment,
            "url": url
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def generate_hindi_audio(text): 
    """
    Translates the given text to Hindi and converts it into Hindi speech.
    Returns the base64 encoded audio data.
    """
    if text.strip():
        translated_text = GoogleTranslator(source="auto", target="hi").translate(text)
        tts = gTTS(text=translated_text, lang="hi")
        tts.save("output.mp3")
        with open("output.mp3", "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
        os.remove("output.mp3")
        return audio_base64 
    return None

def extract_news(company_name):
    """
    Fetches 10 news articles using NewsAPI and scrapes their content.
    Aggregates sentiment counts and generates a final overall sentiment analysis.
    Generates a Hindi audio file for the final sentiment analysis.
    """
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = []
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for i,item in enumerate(data["articles"][:10]): 
            article_url = item["url"]
            article_content = fetch_article_content(article_url) 
            if article_content:
                articles.append(article_content)
                sentiment_counts[article_content["sentiment"]] += 1

        comparative_analysis = {
            "Sentiment Distribution": sentiment_counts
        }

        if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
            final_analysis = f"{company_name}’s latest news coverage is mostly positive. Potential stock growth expected."
        elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
            final_analysis = f"{company_name}'s latest news coverage is mostly negative. Negative perception is dominant."
        else:
            final_analysis = f"Mixed coverage for {company_name}. Some positive and some negative."

        final_audio_base64 = generate_hindi_audio(final_analysis) 

        return {
            "Company": company_name,
            "Articles": articles,
            "Comparative Sentiment Score": comparative_analysis,
            "Final Sentiment Analysis": final_analysis,
            "Audio": final_audio_base64 
        }

    except Exception as e:
        print(f"Error fetching news for {company_name}: {e}")
        return {"Company": company_name, "Articles": []}