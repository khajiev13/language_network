from django.core.management.base import BaseCommand
from subprocess import run

class Command(BaseCommand):
    help = 'Run Tailwind CSS build process'

    def handle(self, *args, **options):
        run(['python', 'manage.py', 'tailwind', 'start'])
