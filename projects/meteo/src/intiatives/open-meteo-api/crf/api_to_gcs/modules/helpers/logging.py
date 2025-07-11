import os, logging
from google.cloud.logging import Client as LogClient

def set_up_cloud_logs(**labels) -> None:
    """
    Set up the logging module to output logs to the console and Stackdriver Logging.

    The log level is set to INFO for non-production environments and WARNING for production environments.
    The log format is set to "%(asctime)s | %(levelname)s - [%(module)s:%(filename)s:%(lineno)d] - %(message)s".
    The log messages are sent to the console and Stackdriver Logging, with the given labels.

    Args:
        **labels: A dictionary of labels to add to the log messages.
    """
    level: int = logging.INFO #if os.environ.get("ENV") != "prd" else logging.WARNING

    logging.basicConfig(
        level=level,
        format=("%(asctime)s | %(levelname)s - [%(module)s:%(filename)s:%(lineno)d] - %(message)s"),
        handlers=[logging.StreamHandler()],
    )
    LogClient().setup_logging(
        log_level=level,
        labels=labels,
    )