import logging
import sys
from google.cloud.logging import Client as LogClient
from google.cloud.logging.handlers import CloudLoggingHandler

def set_up_logger() -> logging.Logger:
    """
    Set up a logger for use in Cloud Functions.

    The logger returned by this function is configured to log at the INFO level
    and logs to both the Cloud Logging service and the console.

    If the logger has already been configured (i.e. it already has handlers), this
    function does nothing and returns the existing logger.

    This function is intended to be called once per module, and the logger it
    returns should be used throughout the module.

    Returns:
        A configured Logger.
    """
    client: LogClient = LogClient()

    cloud_handler: CloudLoggingHandler = CloudLoggingHandler(client)
    stream_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout) 

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(cloud_handler)
        logger.addHandler(stream_handler)
    
    return logger