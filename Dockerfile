# Use Python 3.10 slim bullseye image (Debian 11) where execstack is available
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies AND execstack to fix Railway security policies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    execstack \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FIX: Clear the executable stack flag from ctranslate2 shared libraries
# Railway blocks libraries that request executable stack memory for security reasons.
RUN find /usr/local/lib/python3.10/site-packages/ctranslate2 -name "*.so*" -exec execstack -c {} \;

# Copy the application code
COPY . .

# Expose port
ENV PORT=8000
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
