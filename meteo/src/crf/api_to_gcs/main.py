from functions_framework import http
from flask import Request
import logging
from datetime import datetime
from modules.helpers.logging import set_up_logger
from modules.meteorology.general import ForecastAPIHandler
from modules.helpers.storage import GCSHandler
import json

@http
def entrypoint(request: Request) -> tuple[str, int, dict[str, str]]:
    """
    Cloud Run Function entrypoint
    Consult the README.md file in the current directory for more information
    curl -o output.json "https://api.open-meteo.com/v1/forecast?latitude=-23.5475&longitude=-46.6361&hourly=temperature_2m,rain,wind_speed_10m&timezone=America%2FSao_Paulo&start_date=2025-05-02&end_date=2025-06-02"    """

    logger: logging.Logger = set_up_logger()

    current_date: datetime = datetime.now().date()

    logger.info("Hello from GCP Logging!")
    json_input: dict = request.get_json()
    logger.info(f"JSON received: {json_input}")

    project_id: str = json_input["project_id"]

    run_execution_id: str = json_input["run_execution_id"]
    latitude: float = json_input["latitude"]
    longitude: float = json_input["longitude"]
    start_date: datetime = datetime.strptime(json_input["start_date"], "%Y-%m-%d")
    end_date: datetime = datetime.strptime(json_input["end_date"], "%Y-%m-%d")
    timezone: str = json_input["timezone"]

    modality: str = json_input["modality"]
    match modality:
        case "forecast":
            weather_api_handler: ForecastAPIHandler = ForecastAPIHandler(latitude, longitude, timezone)
            data: dict = weather_api_handler.get_forecast(start_date=start_date, end_date=end_date)
        case _:
            raise ValueError(f"Modality {modality} not supported")

    bucket_name: str = json_input["bucket_name"]
    dest_dir_path: str = f"forecast/raw/{current_date}"
    dest_file_name: str = f"{run_execution_id}_{start_date}_to_{end_date}.json"
    destination_blob_name: str = f"{dest_dir_path}/{dest_file_name}"
    gcs_handler: GCSHandler = GCSHandler(project_id=project_id, bucket_name=bucket_name)
    gcs_handler.upload_bytes(
        data=json.dumps(data).encode("utf-8"), 
        destination_blob_name=destination_blob_name
    )

    logger.info(f"Data uploaded to GCS: {bucket_name}/{destination_blob_name}")



    return ("Hello, World!", 200, {"Content-Type": "text/plain"})
        