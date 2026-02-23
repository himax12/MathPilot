# --- Stage 1: Build the React Frontend ---
FROM node:20-slim AS frontend-builder

# Accept build arguments for frontend env vars
ARG VITE_GOOGLE_CLIENT_ID
ARG VITE_API_URL=/api

# Set as environment variables for Vite build
ENV VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /app/frontend-react
COPY frontend-react/package*.json ./
RUN npm install
COPY frontend-react/ ./
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    portaudio19-dev \
    python3-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv catalyst tool
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync
RUN uv sync --frozen --no-cache

# Copy the rest of the application
COPY . .

# Copy the built frontend into backend/static for serving
COPY --from=frontend-builder /app/frontend-react/dist ./backend/static

# Deployment environment variables
ENV PORT=8080
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080

# Healthcheck targeting the API
HEALTHCHECK CMD curl --fail http://localhost:8080/api/sessions || exit 1

# Launch the FastAPI app with uvicorn
# Cloud Run sets the PORT env var; we must listen on it.
CMD ["sh", "-c", "uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8080}"]
