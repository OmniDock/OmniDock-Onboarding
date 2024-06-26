from django.db import models

# Create your models here.

class OmnidockOrder(models.Model):
    marketplace_order_id = models.CharField(max_length=100)  # Order ID specific to the marketplace
    omnidock_order_id = models.AutoField(primary_key=True)  # Omnidock specific order ID
    order_date = models.DateTimeField()
    fulfillment_status = models.CharField(max_length=100)
    shipping_date = models.DateTimeField(null=True, blank=True)

class OmnidockProduct(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    product_title = models.CharField(max_length=255)
    gross_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    units_sold = models.IntegerField(default=0)

