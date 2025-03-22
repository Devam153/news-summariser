import streamlit as st
from utils import extract_news
import os

# App title
st.title("📰 AI-Powered News Summarizer")

# Input field for company name
company = st.text_input("Enter a company name to fetch news:")

if st.button("Get News Summary"):
    if company.strip():
        # Fetch news
        with st.spinner("Fetching news..."):
            news_data = extract_news(company)
        
        if news_data["Articles"]:
            st.subheader(f"News Summary for {company}")

            # Display news articles
            for i, article in enumerate(news_data["Articles"]):
                st.write(f"### {i+1}. {article['title']}")
                st.write(f"📄 **Summary:** {article['summary']}")
                st.write(f"📊 **Sentiment:** {article['sentiment']}")
                st.write(f"📌 **Topics Covered:** {', '.join(article['topics'])}")
                st.write(f"🔗 [Read More]({article['url']})")

                # Audio player for Hindi TTS
                if "audio" in article and os.path.exists(article["audio"]):
                    st.audio(article["audio"], format="audio/mp3")

            # Show final comparative sentiment analysis
            st.subheader("📊 Comparative Sentiment Analysis")
            st.write(news_data["Comparative Sentiment Score"])

            # Show final sentiment analysis
            st.subheader("📢 Final Sentiment Summary")
            st.write(news_data["Final Sentiment Analysis"])

            # Final audio analysis in Hindi
            if "Audio" in news_data and os.path.exists(news_data["Audio"]):
                st.audio(news_data["Audio"], format="audio/mp3")

        else:
            st.warning("No articles found for this company.")
    else:
        st.warning("Please enter a valid company name.")