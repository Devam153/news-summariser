import streamlit as st
import requests
import base64

st.title("📰 AI-Powered News Summarizer")

company = st.text_input("Enter a company name to fetch news:")

if st.button("Get News Summary"):
    if company.strip():
        with st.spinner("Fetching news..."):
            response = requests.get(f"http://127.0.0.1:8000/news/{company}")
            news_data = response.json()

        if "Articles" in news_data and news_data["Articles"]:
            st.subheader(f"News Summary for {company}")

            for i, article in enumerate(news_data["Articles"]):
                st.write(f"### {i+1}. {article['title']}")
                st.write(f"📄 **Summary:** {article['summary']}")
                st.write(f"📊 **Sentiment:** {article['sentiment']}")
                st.write(f"📌 **Topics Covered:** {', '.join(article['topics'])}")
                st.write(f"🔗 [Read More]({article['url']})")

                if "audio" in article:
                    st.audio(article["audio"], format="audio/mp3")

            # Display the comparative sentiment analysis in a nicer format
            st.subheader("📊 Comparative Sentiment Analysis")
            sentiment_data = news_data["Comparative Sentiment Score"]["Sentiment Distribution"]
            positive = sentiment_data.get("Positive", 0)
            negative = sentiment_data.get("Negative", 0)
            neutral = sentiment_data.get("Neutral", 0)

            st.markdown("**Sentiment Distribution:**")
            st.write(f"- **Positive:** {positive}")
            st.write(f"- **Negative:** {negative}")
            st.write(f"- **Neutral:** {neutral}")

            st.subheader("📢 Final Sentiment Summary")
            st.write(news_data["Final Sentiment Analysis"])

            if "Audio" in news_data:
                    try:
                        audio_bytes = base64.b64decode(news_data["Audio"]) #Decode the base64 audio.
                        st.audio(audio_bytes, format="audio/mp3")
                    except base64.binascii.Error:
                        st.error("Error decoding audio data.")

        else:
            st.warning("No articles found for this company.")
    else:
        st.warning("Please enter a valid company name.")