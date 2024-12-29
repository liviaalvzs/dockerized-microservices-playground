# Base image for building dependencies
FROM python:3.11-slim as builder

# Define working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install PostgreSQL dependencies and Python build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Final image for running the application
FROM python:3.11-slim

# Define working directory
WORKDIR /app

# Copy dependencies and application code
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY app.py .

# Expose port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
