from functions_framework import http
from flask import Request
import logging
from modules.helpers.logging import set_up_logger

@http
def entrypoint(request: Request) -> tuple[str, int, dict[str, str]]:
    """
    Cloud Function entrypoint
    Usage:
        functions-framework --target=entrypoint --port=8080

        curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{"message":"Hello"}'
        curl -X POST https://us-west1-analytics-meteorology-dev.cloudfunctions.net/crf-meteorology-dev  -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -d '{"message":"Hello"}'
        curl -o output.json "https://api.open-meteo.com/v1/forecast?latitude=-23.5475&longitude=-46.6361&hourly=temperature_2m,rain,wind_speed_10m&timezone=America%2FSao_Paulo&past_days=1"    """
    logger: logging.Logger = set_up_logger()

    logger.info("Hello from GCP Logging!")
    try:
        json_input: dict = request.get_json()
        logger.info(f"JSON received: {json_input}")
        logger.info(f"Message: {json_input['message']}")
    except Exception as e:
        logger.warning(f"No JSON payload: {e}")

    return ("Hello, World!", 200, {"Content-Type": "text/plain"})