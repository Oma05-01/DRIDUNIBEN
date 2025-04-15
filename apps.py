import os
import logging
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger('app')


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Code to run when Django starts.
        Note: This will run twice when using the development server with auto-reload.
        """
        # Only run in main process (not in the reloader process)
        if os.environ.get('RUN_MAIN', None) != 'true':
            # Create upload directories if they don't exist
            upload_dir = settings.PROFILE_UPLOAD_DIR
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir, exist_ok=True)
                logger.info(f"Upload directory created: {upload_dir}")

            # The database connection is handled by Djongo when Django starts
            # but we could manually check it here if needed
            logger.info(f"Server running in {os.environ.get('DJANGO_SETTINGS_MODULE', 'unknown')} mode")