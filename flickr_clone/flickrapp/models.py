from django.conf import settings
from django.db import models


class Album(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Album name", max_length=80)
    is_public = models.BooleanField(verbose_name="Public?")
    date_created = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["date_created"]


class Image(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Photo title", max_length=80)
    location = models.CharField(max_length=120)
    date_uploaded = models.DateField()

    class Meta:
        ordering = ['date_uploaded']
