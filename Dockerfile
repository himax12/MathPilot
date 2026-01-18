# Start with a lightweight Python image
FROM python:3.10-slim

# Install system dependencies for OpenCV and Audio
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (The extremely fast Python package installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency definition files first
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen: strict sync from uv.lock
# --no-install-project: only install dependencies (we copy code later)
RUN uv sync --frozen --no-install-project

# Add the virtual environment to PATH
# uv creates the venv in .venv by default
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the application
COPY . .

# Expose the port
ENV PORT=8080
EXPOSE 8080

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch the app using the venv's python/streamlit
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
