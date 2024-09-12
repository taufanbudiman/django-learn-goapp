from itertools import product
from django.db import models


# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    sku = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'


class Orders(models.Model):
    order_number = models.CharField(
        max_length=100, help_text="aka Invoice Number")
    order_id = models.CharField(
        max_length=100,
        help_text="Order ID on Marketplace",
        blank=True,
        null=True,
    )
    marketplace = models.CharField(
        max_length=100,
        help_text="Marketplace Name eg: Tokopedia, Shopee etc",
        blank=True,
        null=True,
    )
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.FloatField()

    def __str__(self):
        return self.order_number

    class Meta:
        ordering = ('order_number',)
        verbose_name = 'Orders'


class OrderDetails(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return f'{self.order.order_number} - {self.product.name}'

    def save(self, *args, **kwargs):
        # only on new data
        if not self.pk:
            self.price = self.product.price

        self.total_price = self.price * self.quantity
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Order Details'


class Channels(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Channel'


class BulkProducts(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    DONE = 'done'
    STATUS_CHOICES = {
        PENDING: 'Pending',
        PROCESSING: 'Processing',
        DONE: 'Done'
    }
    file = models.FileField(upload_to='main/products')
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending',
                              choices=STATUS_CHOICES)
    progress = models.IntegerField(default=0)

    def mark_done(self):
        self.status = 'done'
        self.save()

    def mark_processing(self):
        self.status = 'processing'
        self.save()

    def save(self, *args, **kwargs):
        from .tasks import upload_process_job
        upload_process_job.delay()
        return super().save(*args, **kwargs)
