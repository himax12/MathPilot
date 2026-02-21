# Start with a lightweight Python image
FROM python:3.11-slim

# Install system dependencies for OpenCV and Audio
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    portaudio19-dev \
    python3-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv compiler tool
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
# Note: we use pyproject.toml and uv.lock as the source of truth if available, otherwise requirements.txt
COPY requirements.txt pyproject.toml uv.lock* ./

# Install dependencies using uv
# --system ensures it installs to the container's global python env
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port
ENV PORT=8080
ENV PYTHONPATH=/app
EXPOSE 8080

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the app
CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
