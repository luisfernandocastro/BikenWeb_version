from django.apps import AppConfig


class PrincipalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.principal'
    verbose_name = "Biken"

    def ready(self):
        import Apps.principal.signals
