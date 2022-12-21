from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'final_project.web'

    def ready(self):
        import final_project.web.signals
