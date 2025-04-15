import logging
from django.core.management.base import BaseCommand
from db.connection import initialize_mongodb_connection
from utils.env_validator import validate_env

logger = logging.getLogger('app')


class Command(BaseCommand):
    help = 'Initialize database connection and verify environment variables'

    def handle(self, *args, **options):
        self.stdout.write('Validating environment variables...')
        validate_env()

        self.stdout.write('Establishing database connection...')
        if initialize_mongodb_connection():
            self.stdout.write(self.style.SUCCESS('Successfully connected to MongoDB'))
        else:
            self.stdout.write(self.style.ERROR('Failed to connect to MongoDB'))
            exit(1)