from django.conf import settings
from django.db import models


class Album(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Album name", max_length=80)
    is_public = models.BooleanField(verbose_name="Public?")
    date_created = models.DateField()

    class Meta:
        ordering = ["date_created"]
