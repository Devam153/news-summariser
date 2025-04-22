import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv
from gtts import gTTS
import json

# Load environment variables
load_dotenv()

# Get API URL from environment variable or use default for local development
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("📰 AI-Powered News Summarizer")

company = st.text_input("Enter a company name to fetch news:")

if st.button("Get News Summary"):
    if company.strip():
        with st.spinner("Fetching news..."):
            response = requests.get(f"{API_URL}/news/{company}")
            if response.status_code == 200:
                news_data = response.json()
                
                if not news_data:
                    st.warning(f"No news found for {company}.")
                else:
                    for i, article in enumerate(news_data):
                        with st.expander(f"{i+1}. {article['title']}"):
                            st.write(f"**Source:** {article['source']} | **Published:** {article['time']}")
                            st.write("**Summary:**")
                            st.write(article['summary'])
                            
                            if 'topics' in article and article['topics']:
                                st.write("**Topics:**")
                                topics_html = ' '.join([f'<span style="background-color:#e6f2ff; padding:3px 8px; margin-right:5px; border-radius:10px;">{topic}</span>' for topic in article['topics']])
                                st.markdown(topics_html, unsafe_allow_html=True)
                            
                            st.markdown(f"[Read full article]({article['url']})")
                            
                            # Generate and display audio summary
                            if st.button(f"Listen to Summary #{i+1}"):
                                summary_text = article['summary']
                                tts = gTTS(text=summary_text, lang='en', slow=False)
                                tts.save("summary.mp3")
                                
                                with open("summary.mp3", "rb") as audio_file:
                                    audio_bytes = audio_file.read()
                                    
                                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error(f"Error fetching news: {response.text}")
    else:
        st.warning("Please enter a valid company name.")

# Add footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and AI")