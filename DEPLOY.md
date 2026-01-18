# Deploying Math Mentor to Google Cloud Run

This guide explains how to deploy the application using the **Cloud Run** service.
The project is configured to use **uv**, a high-performance Python package manager, ensuring fast and deterministic builds.

## 1. Prerequisites
Ensure you have the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and initialized.

```bash
# Verify installation
gcloud --version
```

## 2. One-Time Setup
Run these commands in your terminal (from the project root) to configure the environment:

```bash
# 1. Login to Google Cloud
gcloud auth login

# 2. Create the project (or skip if you have one)
# Replace 'math-mentor-prod' with your unique project ID
gcloud projects create math-mentor-prod --name="Math Mentor"
gcloud config set project math-mentor-prod

# 3. Enable necessary Google Cloud APIs
gcloud services enable run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com
```

## 3. Deploy
Execute this single command to build and launch the application.

```bash
gcloud run deploy math-mentor \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_API_KEY=your_actual_api_key_here"
```

**Configuration Details**:
*   `--source .`: Uses the local `Dockerfile` (which leverages `uv sync`).
*   `--allow-unauthenticated`: Makes the application accessible via public URL.
*   `--set-env-vars`: Securely injects your API key.

## 4. Verification
Upon success, the terminal will display a Service URL:
`https://math-mentor-abc123xyz.a.run.app`

Click the link to verify your deployed Math Mentor!
