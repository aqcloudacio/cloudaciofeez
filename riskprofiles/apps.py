from django.apps import AppConfig


class RiskProfilesConfig(AppConfig):
    name = 'riskprofiles'

    def ready(self):
        import riskprofiles.signals
