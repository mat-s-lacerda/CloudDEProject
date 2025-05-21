import functions_framework
from flask import Request
import logging
from modules.helpers.logging import set_up_logger

@functions_framework.http
def entrypoint(request: Request) -> tuple[str, int, dict[str, str]]:
    """
    Cloud Function entrypoint
    Usage:
        functions-framework --target=entrypoint --port=8080

        curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{"message":"Hello"}'
    """
    logger: logging.Logger = set_up_logger()

    logger.info("Hello from GCP Logging!")
    try:
        json_input: dict = request.get_json()
        logger.info(f"JSON received: {json_input}")
        logger.info(f"Message: {json_input['message']}")
    except Exception as e:
        logger.warning(f"No JSON payload: {e}")

    return ("Hello, World!", 200, {"Content-Type": "text/plain"})