from django.apps import AppConfig


class ClinicAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_app'

    def ready(self):
        import clinic_app.signals
