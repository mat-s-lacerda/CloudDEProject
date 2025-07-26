# CloudDEProject

---

## API to GCS
### Description
This script will get the data from the API and upload it to GCS

### Usage
- Local
    - functions-framework --target=entrypoint --port=8080

    - curl -X POST http://localhost:8080     -H "Content-Type: application/json"     -d '{     "project_id": "de-analytics-meteo-dev",     "bucket_name": "de-analytics-meteo-dev-batch-data-intake",     "run_execution_id": "123456789",     "start_date": "2025-06-01", "modality": "forecast",     "end_date": "2025-06-07",     "latitude": -23.5475,     "longitude": -46.6361,     "timezone": "America/Sao_Paulo" }'

- Cloud Run Function (Remote)
    - curl -X POST https://us-central1-de-analytics-meteo-dev.cloudfunctions.net/analytics-weather-data-forecast-api-extractor-dev -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{     "project_id": "de-analytics-meteo-dev",     "bucket_name": "de-analytics-meteo-dev-batch-data-intake",     "run_execution_id": "123456789",     "start_date": "2025-06-01", "modality": "forecast",     "end_date": "2025-06-07",     "latitude": -23.5475,     "longitude": -46.6361,     "timezone": "America/Sao_Paulo" }'

#### JSON Body
{   
    "project_id": "my-project",
    "modality": "forecast",
    "bucket_name": "my_bucket",
    "run_execution_id": "123456789",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "timezone": "America/Sao_Paulo"
}