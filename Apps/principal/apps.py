from django.apps import AppConfig


class PrincipalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apps.principal'
    verbose_name = "Biken" # Nombre que se mostrara en las vistas de Admin

    def ready(self):
        import Apps.principal.signals
