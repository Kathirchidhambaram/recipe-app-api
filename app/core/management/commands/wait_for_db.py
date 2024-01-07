"""
    Django management command to wait for db activation
"""

import time
from typing import Any

from psycopg2 import OperationalError as psycopg2Error
from django.db.utils import OperationalError
from django.core.management import BaseCommand

class Command(BaseCommand):
    """Django command to wait for database to be available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database Connection...')
        is_db_connected = False 

        while is_db_connected == False:
            try:
                self.check(databases=['default'])
                is_db_connected = True 
            except (psycopg2Error, OperationalError):
                self.stdout.write('Database not available yet, waiting for 1 sec...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database active and connected!'))