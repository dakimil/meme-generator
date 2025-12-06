# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Install system dependencies for Pillow (Image processing)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libjpeg-dev \
        libpng-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libtiff-dev \
        libwebp-dev \
        tcl-dev \
        tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static/uploads

# Set proper permissions
RUN chmod -R 755 static/uploads

# Expose port
EXPOSE ${PORT}

# Command to run the application
CMD ["python", "app.py"]