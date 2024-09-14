from django.apps import AppConfig


class RequestorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'requestor'
    def ready(self):
        import requestor.signals






