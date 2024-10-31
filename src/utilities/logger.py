import logging
import os
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.handlers import CloudLoggingHandler

from src.config.constants import ENVIRONMENT, TEST, DEV


def setup_logging():
    """
    Sets up logging for the application based on the environment.

    If the environment is not a test or development environment, it configures
    Google Cloud Logging. Otherwise, it uses console logging with DEBUG level.

    Returns:
        logger: A logging object configured for the application.
    """
    log = logging.getLogger(__name__)
    try:
        # Only setup cloud logging if NOT in a test or dev environment
        if os.getenv(ENVIRONMENT) != TEST and os.getenv(ENVIRONMENT) != DEV:
            client = Client()
            cloud_handler = CloudLoggingHandler(client)

            log.setLevel(logging.INFO)  # Set the default logging level to INFO
            log.addHandler(cloud_handler)  # Add the Cloud Logging handler
            log.info("Cloud logging has been set up.")  # Log successful setup
        else:
            log.setLevel(logging.DEBUG)  # Set to DEBUG or INFO for test logs
            log.addHandler(logging.StreamHandler())  # Output logs to console during tests
            log.debug("Console logging has been set up for testing environment.")  # Log successful setup for tests
    except Exception as e:
        log.error(f"Failed to set up logging: {e}")  # Log error if logging setup fails
    return log

# Initialize logger when needed
logger = setup_logging()
