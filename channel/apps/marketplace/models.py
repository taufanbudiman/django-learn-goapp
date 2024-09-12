from django.db import models


# Create your models here.
class Tokopedia(models.Model):
    client_id = models.CharField(max_length=255, unique=True)
    client_secret = models.CharField(max_length=255, unique=True)
    app_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Tokopedia'