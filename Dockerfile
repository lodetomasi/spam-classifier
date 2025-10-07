# Multi-Agent Spam Classifier - Docker Image
# For deployment and containerized execution

FROM python:3.10-slim

LABEL maintainer="spam-classifier"
LABEL description="Multi-Agent Spam Email Classifier using Claude AI"
LABEL version="2.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY .claude/ .claude/
COPY src/ src/
COPY data/ data/
COPY examples/ examples/
COPY *.md ./

# Create results directory
RUN mkdir -p results

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import json; json.load(open('data/pattern_catalog.json'))" || exit 1

# Default command
CMD ["python", "src/batch_test.py"]

# Usage:
# Build: docker build -t spam-classifier .
# Run:   docker run -v $(pwd)/results:/app/results spam-classifier
