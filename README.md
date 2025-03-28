News Summariser is an AI-powered tool designed to generate concise and accurate summaries of news articles. Built using FastAPI and Google Generative AI, it efficiently processes large amounts of text, extracting key information while preserving the original meaning. The application is ideal for users who want quick, digestible insights without reading entire articles. Whether you're keeping up with daily news or conducting research, News Summariser helps streamline information consumption by delivering essential points in a clear and structured format.

Hugging face space link - https://huggingface.co/spaces/devam153/news-summariser

So originally this used Google's Gemini API, but in Hugging Face Spaces I kept hitting rate limits and permission errors (turns out cloud APIs can be fussy about where they're called from).
Tried using Transformers too, but Spaces got grumpy about cache paths (`/.cache permission denied, bruh).

So now I'm keeping it simple with:

Sumy - For decent summaries without API keys

YAKE - For topic extraction that runs locally

NLTK - Just the basics for text processing

No external services = no rate limits 
Might not be as smart as Gemini, but it always works!

This Hugging Face Spaces version uses a simplified tech stack (Sumy + YAKE) to avoid cloud API limits and permission issues. 

For the full-powered Gemini API version with FastAPI backend, check out the main GitHub repository - perfect for local development and more advanced use cases! 
