import base64
import os
from google import genai
from google.genai import types

def summarise_text(text):
    """Uses Gemini API to summarize a given text."""
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),  # Pass the actual text
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="I will give you a text of text. I need you to summarise it. Keep it simple, and short and give output in a paragraph format"),
        ],
    )

    # Generate and return summary
    summary = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        summary += chunk.text

    return summary

def extract_topics(text):
    """Uses Gemini API to extract 2-3 key topics from a given text."""
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),  # Pass the actual text
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="Extract the 2-3 most important topics from this news. Give output as a simple comma-separated list."),
        ],
    )

    topics = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        topics += chunk.text

    return [topic.strip() for topic in topics.split(",")] 