from django.apps import AppConfig

from django.apps import AppConfig



class NetworkConfig(AppConfig):
    name = 'network'

    def ready(self):
        # Run your custom command
        RunTailwindCommand().handle()