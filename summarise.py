import os
import google.generativeai as genai

def summarise_text(text):
    """Uses Gemini API to summarize a given text."""
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    
    system_instruction = "I will give you a piece of text. I need you to summarise it. Keep it simple, and short and give output in a paragraph format"
    
    response = model.generate_content(
        f"{system_instruction}\n\nText: {text}",
        generation_config={
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
    )
    
    return response.text

def extract_topics(text):
    """Uses Gemini API to extract 2-3 key topics from a given text."""
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")
    
    system_instruction = "I need you to extract the 2-3 most important topics from this news. Give output as a simple comma-separated list."
    
    response = model.generate_content(
        f"{system_instruction}\n\nText: {text}",
        generation_config={
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 100,
        }
    )
    
    topics = response.text.strip()
    return [topic.strip() for topic in topics.split(",")]