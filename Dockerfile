# Start with a lightweight Python image
FROM python:3.11-slim

# Install system dependencies for OpenCV and Audio
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    portaudio19-dev \
    python3-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies using standard pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
ENV PORT=8080
EXPOSE 8080

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the app
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
