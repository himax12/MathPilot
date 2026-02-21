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
# Note: we use pyproject.toml and uv.lock as the source of truth
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync
# This creates a virtual environment at /app/.venv
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . .

# Expose the port
ENV PORT=8080
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the app
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
