FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# - gcc, g++: For compiling Python packages (psycopg2, etc.)
# - postgresql-client: For database utilities
# - curl: For health checks
# - libgomp1: Required for FAISS CPU operations
# - git: Required for huggingface-hub to download models
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    curl \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
# Use root requirements.txt which has all dependencies
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ /app/backend/

# Copy Quran data files and ML modules from root
COPY quran_retrieval2.py /app/
COPY llm_explainer.py /app/

# Copy Quran data files (JSON and FAISS index)
# Copy from root directory (primary location)
# Note: If files don't exist in root, they should be in backend/ directory
COPY quran_full_formatted.json /app/quran_full_formatted.json
COPY quran_metadata.json /app/quran_metadata.json
COPY quran_texts.json /app/quran_texts.json
COPY quran_faiss.index /app/quran_faiss.index

# Set Python path to include backend directory and root
ENV PYTHONPATH=/app/backend:/app
ENV PYTHONUNBUFFERED=1

# Set default Quran file paths (can be overridden via env vars)
ENV QURAN_JSON_PATH=/app/quran_full_formatted.json
ENV FAISS_INDEX_PATH=/app/quran_faiss.index
ENV QURAN_METADATA_PATH=/app/quran_metadata.json

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
