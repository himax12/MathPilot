<#
.SYNOPSIS
    Automated Deployment Script for Math Mentor
.DESCRIPTION
    Deploys the Streamlit application to Google Cloud Run using the gcloud CLI.
    Handles project creation, API enabling, and container deployment.
#>

Write-Host "🚀 Math Mentor - Automated Deployment" -ForegroundColor Cyan
Write-Host "======================================"

# 1. Check for gcloud
if (-not (Get-Command "gcloud" -ErrorAction SilentlyContinue)) {
    Write-Error "Google Cloud CLI (gcloud) is not installed."
    Write-Host "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
}

# Math Mentor unified deployment script
$PROJECT_ID = "firstproject-c5ac2"
$REGION = "us-central1"
$SERVICE_NAME = "math-mentor"

Write-Host "--- Deploying MathPilot (Unified Stack) to Cloud Run ---" -ForegroundColor Cyan

# 1. Login & Project Setup
gcloud auth login
gcloud config set project $PROJECT_ID

# 2. Get GEMINI_API_KEY if not in env
if (-not $env:GEMINI_API_KEY) {
    if (Test-Path ".env") {
        $env:GEMINI_API_KEY = (Get-Content .env | Select-String "GEMINI_API_KEY=").ToString().Split("=")[1].Trim()
    }
    if (-not $env:GEMINI_API_KEY) {
        $env:GEMINI_API_KEY = Read-Host "Please enter your GEMINI_API_KEY"
    }
}

# 3. Deploy
gcloud run deploy $SERVICE_NAME `
    --source . `
    --region $REGION `
    --allow-unauthenticated `
    --set-env-vars="GEMINI_API_KEY=$($env:GEMINI_API_KEY)"

Write-Host "--- Deployment Complete ---" -ForegroundColor Green
