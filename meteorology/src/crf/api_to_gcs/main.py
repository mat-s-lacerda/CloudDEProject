from functions_framework import http
from flask import Request
import logging
from datetime import datetime
from modules.helpers.logging import set_up_logger
from modules.meteorology.general import ForecastAPIHandler

@http
def entrypoint(request: Request) -> tuple[str, int, dict[str, str]]:
    """
    Cloud Run Function entrypoint
    Consult the README.md file in the current directory for more information
    curl -o output.json "https://api.open-meteo.com/v1/forecast?latitude=-23.5475&longitude=-46.6361&hourly=temperature_2m,rain,wind_speed_10m&timezone=America%2FSao_Paulo&start_date=2025-05-02&end_date=2025-06-02"    """

    logger: logging.Logger = set_up_logger()

    logger.info("Hello from GCP Logging!")
    json_input: dict = request.get_json()
    logger.info(f"JSON received: {json_input}")

    latitude: float = json_input["latitude"]
    longitude: float = json_input["longitude"]
    start_date: datetime = datetime.strptime(json_input["start_date"], "%Y-%m-%d")
    end_date: datetime = datetime.strptime(json_input["end_date"], "%Y-%m-%d")
    timezone: str = json_input["timezone"]

    forecast_api_handler: ForecastAPIHandler = ForecastAPIHandler(latitude, longitude, start_date, end_date, timezone)
    json: dict = forecast_api_handler.get_forecast()
    logger.info(f"Forecast: {json}")

    return ("Hello, World!", 200, {"Content-Type": "text/plain"})
        