param (
    [Parameter(Mandatory=$true)]
    [string]$ProjectId
)

$ImageName = "gcr.io/$ProjectId/truthlens-api"

Write-Host "🚀 Building Docker Image and uploading to Google Container Registry..." -ForegroundColor Cyan
gcloud builds submit --tag $ImageName

Write-Host "🌐 Deploying TruthLens API to Google Cloud Run..." -ForegroundColor Cyan
# Note: You will need to manually update the environment variables in the Cloud Run console 
# or add them here before running this script for security!
gcloud run deploy truthlens-api `
  --image $ImageName `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated 

Write-Host "✅ Deployment Complete! Grab the URL provided above and paste it into your frontend/main.js file!" -ForegroundColor Green
