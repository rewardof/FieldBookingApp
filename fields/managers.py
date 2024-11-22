from django.db import models


class FootballFieldManager(models.Manager):

    def active(self, *args, **kwargs):
        """
        Return all active football fields.
        """
        return self.get_queryset().filter(is_active=True, *args, **kwargs)
