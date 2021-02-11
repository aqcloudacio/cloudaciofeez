from django.apps import AppConfig


class PlatformsConfig(AppConfig):
    name = 'platforms'

    def ready(self):
        import platforms.signals
