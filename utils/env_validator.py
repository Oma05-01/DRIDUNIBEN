
import os
import sys
import logging

logger = logging.getLogger('app')

REQUIRED_ENV_VARS = [
    'MONGODB_URI',
    'SECRET_KEY',
]


def validate_env():
    """
    Validates that all required environment variables are set.
    Exits the application if any required variable is missing.
    """
    missing_vars = []

    for var in REQUIRED_ENV_VARS:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        for var in missing_vars:
            logger.error(f"Missing required environment variable: {var}")
        logger.error("Application cannot start. Missing required environment variables.")
        sys.exit(1)

    logger.info("All required environment variables are set")
    return True
