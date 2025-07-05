from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self):
        # Prevent double start from Django's autoreloader
        if os.environ.get('RUN_MAIN') == 'true':
            from .runner import start_scheduler
            start_scheduler()
