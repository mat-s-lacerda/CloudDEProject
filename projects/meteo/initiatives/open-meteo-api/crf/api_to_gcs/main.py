from functions_framework import http
from flask import Request
import logging
from datetime import datetime
from modules.helpers.logging import set_up_cloud_logs
from modules.meteorology.general import ForecastAPIHandler
from modules.helpers.storage import GCSHandler
import json

@http
def entrypoint(request: Request) -> tuple[str, int, dict[str, str]]:
    """
    Cloud Run Function entrypoint
    Consult the README.md file in the current directory for more information
    curl -o output.json "https://api.open-meteo.com/v1/forecast?latitude=-23.5475&longitude=-46.6361&hourly=temperature_2m,rain,wind_speed_10m&timezone=America%2FSao_Paulo&start_date=2025-05-02&end_date=2025-06-02"    """

    set_up_cloud_logs()

    current_date: datetime = datetime.now().date()

    parsed_req: dict = request.get_json()
    logging.info(f"JSON received: {parsed_req}")

    project_id: str = parsed_req["project_id"]

    run_execution_id: str = parsed_req["run_execution_id"]
    latitude: float = parsed_req["latitude"]
    longitude: float = parsed_req["longitude"]
    start_date: datetime = datetime.strptime(parsed_req["start_date"], "%Y-%m-%d")
    end_date: datetime = datetime.strptime(parsed_req["end_date"], "%Y-%m-%d")
    timezone: str = parsed_req["timezone"]

    modality: str = parsed_req["modality"]
    match modality:
        case "forecast":
            weather_api_handler: ForecastAPIHandler = ForecastAPIHandler(latitude, longitude, timezone)
            data: dict = weather_api_handler.get_forecast(start_date=start_date, end_date=end_date)
        case _:
            raise ValueError(f"Modality {modality} not supported")

    bucket_name: str = parsed_req["bucket_name"]
    dest_dir_path: str = f"forecast/raw/{current_date}"
    dest_file_name: str = f"{run_execution_id}_{start_date}_to_{end_date}.json"
    destination_blob_name: str = f"{dest_dir_path}/{dest_file_name}"
    gcs_handler: GCSHandler = GCSHandler(project_id=project_id, bucket_name=bucket_name)
    gcs_handler.upload_bytes(
        data=json.dumps(data).encode("utf-8"), 
        destination_blob_name=destination_blob_name
    )

    logging.info(f"Data uploaded to GCS: {bucket_name}/{destination_blob_name}")



    return json.dumps({"success": True, "data": "Data extraction finished"}), 200, {"Content-Type": "text/plain"}

