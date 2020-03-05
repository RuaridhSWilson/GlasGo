from django.apps import AppConfig


class GlasgoConfig(AppConfig):
    name = "glasgo"

    def ready(self):
        import glasgo.signals
