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

# 2. Check Login Status
$auth = gcloud auth list --filter=status:ACTIVE --format="value(account)"
if (-not $auth) {
    Write-Host "⚠️  You are not logged in." -ForegroundColor Yellow
    Write-Host "Opening login window..."
    gcloud auth login
}

# 3. Project Setup
$projectId = Read-Host "Enter a unique Project ID (or press Enter for 'math-mentor-demo-01')"
if (-not $projectId) { $projectId = "math-mentor-demo-01" }

Write-Host "Creating/Selecting Project '$projectId'..." -ForegroundColor Green
# Try create, ignore if exists
gcloud projects create $projectId --name="Math Mentor" 2>$null
gcloud config set project $projectId

# 4. Enable APIs
Write-Host "Enabling Cloud Run & Build APIs (this may take a minute)..." -ForegroundColor Green
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# 5. Get API Key
$apiKey = $env:GOOGLE_API_KEY
if (-not $apiKey) {
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -match "GOOGLE_API_KEY=(.*)") { $apiKey = $matches[1] }
        }
    }
}
if (-not $apiKey) {
    $apiKey = Read-Host "Enter your Google Gemini API Key"
}

# 6. Deploy
Write-Host "Building and Deploying to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy math-mentor `
    --source . `
    --region us-central1 `
    --allow-unauthenticated `
    --set-env-vars="GOOGLE_API_KEY=$apiKey"

Write-Host "`n✅ Deployment Complete!" -ForegroundColor Green
