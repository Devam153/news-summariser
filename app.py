import streamlit as st
import requests

st.title("📰 AI-Powered News Summarizer")

company = st.text_input("Enter a company name to fetch news:")

if st.button("Get News Summary"):
    if company.strip():
        with st.spinner("Fetching news..."):
            # Call the API instead of running extract_news directly
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

            st.subheader("📊 Comparative Sentiment Analysis")
            st.write(news_data["Comparative Sentiment Score"])

            st.subheader("📢 Final Sentiment Summary")
            st.write(news_data["Final Sentiment Analysis"])

            if "Audio" in news_data:
                st.audio(news_data["Audio"], format="audio/mp3")

        else:
            st.warning("No articles found for this company.")
    else:
        st.warning("Please enter a valid company name.")