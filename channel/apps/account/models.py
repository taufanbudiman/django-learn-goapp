import uuid

from django.db import models


# Create your models here.
class MarketplaceProduct(models.Model):
    MARKETPLACE = (
        ('tokopedia', 'Tokopedia'),
        ('shopee', 'Shopee'),
    )
    identifier = models.CharField(max_length=255, choices=MARKETPLACE)
    sku = models.CharField(max_length=255, help_text='sku of product')
    name = models.CharField(max_length=255, help_text='name of product')
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text='price of product')
    stock = models.PositiveIntegerField(default=0, help_text='stock of product')

    class Meta:
        ordering = ('identifier',)
        unique_together = (('identifier', 'sku'),)
        verbose_name = 'Marketplace Product'

