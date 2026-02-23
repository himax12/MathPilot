# Math Mentor Deployment Script
$PROJECT_ID = "firstproject-c5ac2"
$REGION = "us-central1"
$SERVICE_NAME = "math-mentor"

Write-Host "Deploying MathPilot to Cloud Run" -ForegroundColor Cyan

# Check for gcloud
if (-not (Get-Command "gcloud" -ErrorAction SilentlyContinue)) {
    Write-Error "Google Cloud CLI (gcloud) is not installed."
    exit 1
}

# Login & Project Setup
gcloud auth login
gcloud config set project $PROJECT_ID

# Load environment variables from .env
$envVars = @{}
if (Test-Path ".env") {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^#=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"')
            $envVars[$key] = $value
        }
    }
}

# Prompt for missing required vars
if (-not $envVars["GEMINI_API_KEY"]) {
    $envVars["GEMINI_API_KEY"] = Read-Host "Please enter your GEMINI_API_KEY"
}
if (-not $envVars["GOOGLE_CLIENT_ID"] -or $envVars["GOOGLE_CLIENT_ID"] -eq "your_google_oauth_client_id_here") {
    Write-Host "WARNING: GOOGLE_CLIENT_ID not found in .env" -ForegroundColor Yellow
    Write-Host "Get it from: https://console.cloud.google.com/apis/credentials?project=$PROJECT_ID" -ForegroundColor Yellow
    $envVars["GOOGLE_CLIENT_ID"] = Read-Host "Please enter your GOOGLE_CLIENT_ID"
}

# Build substitutions string for Cloud Build
$substitutions = ($envVars.GetEnumerator() | ForEach-Object { 
    "_$($_.Key.ToUpper())=$($_.Value)" 
}) -join ","

Write-Host "Deploying with configuration:" -ForegroundColor Cyan
$envVars.Keys | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }

# Deploy using Cloud Build with substitutions
Write-Host "Starting Cloud Build deployment..." -ForegroundColor Cyan
gcloud builds submit `
    --config=cloudbuild.yaml `
    --substitutions="$substitutions" `
    --region=$REGION

Write-Host "Deployment Complete" -ForegroundColor Green
