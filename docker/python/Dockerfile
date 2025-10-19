# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory to where Django project will live
WORKDIR /api

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    git \
    vim \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first for better Docker layer caching
COPY api/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files from api/ folder
COPY api/ .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /api

# Add bash alias for the appuser
RUN echo "alias pym='python3 manage.py'" >> /home/appuser/.bashrc

USER appuser
RUN python3 -m textblob.download_corpora

# Expose Django's default port
EXPOSE 8000

# Default command for Django development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
