from django.apps import AppConfig


class PractictionerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "practitioner"

    def ready(self):
        import practitioner.signals
