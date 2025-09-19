# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by PyMuPDF (MuPDF backend)
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to container
COPY . .

# Create input/output folders in the container (in case they don’t exist)
RUN mkdir -p /app/input /app/output

# Default command to run your Python script
CMD ["python", "app.py"]
