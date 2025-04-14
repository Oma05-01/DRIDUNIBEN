import time
import logging
from django.conf import settings
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger('app')

MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds


def connect_mongodb():
    """Connect to MongoDB with retry mechanism."""
    retries = MAX_RETRIES

    while retries > 0:
        try:
            client = MongoClient(settings.DATABASES['default']['CLIENT']['host'],
                                 serverSelectionTimeoutMS=settings.DATABASES['default']['CLIENT'][
                                     'serverSelectionTimeoutMS'])

            # Force a connection to verify it works
            client.admin.command('ping')

            db_name = client.get_database().name
            logger.info(f"MongoDB Connected: {client.address[0]}:{client.address[1]}, Database: {db_name}")
            return client

        except (ConnectionFailure, ServerSelectionTimeoutError) as error:
            logger.error(f"MongoDB connection failed. Retries left: {retries - 1}. Error: {str(error)}")
            retries -= 1

            if retries == 0:
                logger.error("All retries exhausted. Exiting...")
                raise Exception("Failed to connect to MongoDB after maximum retries")

            logger.info(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    return None


# This function can be called during Django startup
def initialize_mongodb_connection():
    """Initialize MongoDB connection at Django startup."""
    try:
        client = connect_mongodb()
        if client:
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB connection: {str(e)}")
        return False