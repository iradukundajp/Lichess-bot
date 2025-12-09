# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir inside the container
WORKDIR /app

# Install system dependencies (compiler etc. for some Python packages)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better Docker cache)
# Make sure requirements.txt is in the repo root
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Make sure our start script is executable
# (start.sh must be in the repo root)
RUN chmod +x start.sh

# Start the bot (start.sh will inject LICHESS_TOKEN into config.yml, then run lichess-bot.py)
CMD ["./start.sh"]
