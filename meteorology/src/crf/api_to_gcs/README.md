# CloudDEProject

---

## API to GCS
### Description
This script will get the data from the API and upload it to GCS

### Usage
- Local
    - functions-framework --target=entrypoint --port=8080

    - curl -X POST http://localhost:8080     -H "Content-Type: application/json"     -d '{     "project_id": "analytics-meteorology-dev",     "bucket_name": "analytics-weather-data-storage-dev",     "run_execution_id": "123456789",     "start_date": "2025-06-01",     "end_date": "2025-06-07",     "latitude": -23.5475,     "longitude": -46.6361,     "timezone": "America/Sao_Paulo" }'

- Cloud Run Function (Remote)
    - curl -X POST https://us-west1-analytics-meteorology-dev.cloudfunctions.net/crf-meteorology-dev \ 
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \ 
    -H "Content-Type: application/json" \
    -d 'JSON body'

#### JSON Body
{   
    "project_id": "my-project",
    "bucket_name": "my_bucket",
    "run_execution_id": "123456789",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "timezone": "America/Sao_Paulo"
}