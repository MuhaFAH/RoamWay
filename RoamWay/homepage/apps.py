from django.apps import AppConfig
from django.db.models.signals import post_delete

__all__ = []


class HomepageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"

    def ready(self):
        import homepage.signals

        post_delete.connect(homepage.signals.delete_related_files)
