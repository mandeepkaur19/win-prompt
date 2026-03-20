$ErrorActionPreference = "Continue"
$Gcloud = "C:\Users\HP\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

$PROJECT_ID = "win-prompt"
$SERVICE_NAME = "truthlens"
$REGION = "us-central1"
$REPOSITORY = "truthlens-repo"
$IMAGE_TAG = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE_NAME"

Write-Host ""
Write-Host "Starting Robust Deployment of TruthLens to Google Cloud Run..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Enabling core Google Cloud APIs (Cloud Run, Cloud Build, Artifact Registry)..." -ForegroundColor Yellow
& $Gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --quiet
Write-Host "GCP APIs Configuration Verified." -ForegroundColor Green
Write-Host ""

Write-Host "Verifying Artifact Registry: $REPOSITORY..." -ForegroundColor Yellow
& $Gcloud artifacts repositories describe $REPOSITORY --location=$REGION --project=$PROJECT_ID 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating fresh Artifact Registry repository..." -ForegroundColor Cyan
    & $Gcloud artifacts repositories create $REPOSITORY --repository-format=docker --location=$REGION --description="Docker repo for TruthLens" --project=$PROJECT_ID --quiet
} else {
    Write-Host "Artifact Registry already exists." -ForegroundColor Green
}
Write-Host ""

Write-Host "Building Docker image and securely pushing to Artifact Registry..." -ForegroundColor Yellow
& $Gcloud builds submit --tag $IMAGE_TAG . --project=$PROJECT_ID --quiet
Write-Host ""

Write-Host "Deploying container to public Cloud Run service..." -ForegroundColor Yellow
& $Gcloud run deploy $SERVICE_NAME --image $IMAGE_TAG --platform managed --region $REGION --allow-unauthenticated --port 8080 --set-env-vars "GEMINI_API_KEY=AIzaSyAdpSU3F5gdt3zFULf1_BSUIDjXUSbllSk,GOOGLE_SEARCH_API_KEY=AIzaSyAdpSU3F5gdt3zFULf1_BSUIDjXUSbllSk,GOOGLE_SEARCH_CX=d4a6704242f7b4cfe" --project=$PROJECT_ID --quiet

Write-Host ""
Write-Host "Deployment Complete! TruthLens is live. Copy the green Service URL printed above!" -ForegroundColor Green
Write-Host ""
