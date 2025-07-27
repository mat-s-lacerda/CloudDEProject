# CloudDEProject

---

## GCS to BQ
### Description
This script will get the data (a Json file) from the Storage and will apply a flatten treatment. In sequence, will load it on a table, in the BigQuery. 

### Usage
- Local
    - functions-framework --target=entrypoint --port=8080

    - curl -X POST http://localhost:8080     -H "Content-Type: application/json"     -d '{"run_execution_id": "123456789", "bucket_name": "de-analytics-meteo-dev-batch-data-intake", "file": "forecast/raw/2025-07-26/123456789_2025-06-01 00:00:00_to_2025-06-07 00:00:00.json", "dataset": "db_meteo_forecast", "table": "tbl_stg_meteo_forecast"}'