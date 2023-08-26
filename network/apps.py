from django.apps import AppConfig

from django.apps import AppConfig
from myapp.management.commands.run_tailwind import Command as RunTailwindCommand



class NetworkConfig(AppConfig):
    name = 'network'

    def ready(self):
        # Run your custom command
        RunTailwindCommand().handle()