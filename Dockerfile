# Use Python 3.10 slim image for a smaller footprint
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for some Python packages like sentencepiece)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port (Railway will provide $PORT, but we default to 8000)
ENV PORT=8000
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
