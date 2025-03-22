# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 8000

# Start both FastAPI and Streamlit using a process manager
CMD uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 7860 --server.enableCORS false
