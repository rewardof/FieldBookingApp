from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from user.signals import create_groups_signal
        # Connect the signal to the function that creates groups
        post_migrate.connect(create_groups_signal, sender=self)
