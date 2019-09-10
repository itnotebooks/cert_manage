from django.apps import AppConfig


class CertsConfig(AppConfig):
    name = 'certs'

    def ready(self):
        from . import signals_handler
        super().ready()
