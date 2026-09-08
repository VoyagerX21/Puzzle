# Multi-platform slim Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Set working directory
WORKDIR /app

# Install system dependencies needed for Pillow and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . /app/

# Ensure media and uploads directories exist with proper permissions
RUN mkdir -p /app/media/uploads /app/staticfiles

# Collect static files during image build
RUN python manage.py collectstatic --noinput

# Expose port 8080
EXPOSE 8080

# Start Gunicorn server binding on port 8080
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 3 --threads 2 --timeout 120 Puzzle.wsgi:application"]
