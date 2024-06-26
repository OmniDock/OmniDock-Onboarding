from django.db import models

class ProductDimension(models.Model):
    type = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    class Meta:
        unique_together = ('type', 'display_name', 'value')


class ItemValueGrossPrice(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    class Meta:
        unique_together = ('amount', 'currency')

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True, primary_key=True)
    product_title = models.CharField(max_length=255)
    article_number = models.CharField(max_length=100)
    ean = models.CharField(max_length=100)
    vat_rate = models.FloatField()
    dimensions = models.ManyToManyField(ProductDimension, related_name='products', blank=True)

class PositionItem(models.Model):
    position_item_id = models.CharField(max_length=100, unique=True, primary_key=True)
    fulfillment_status = models.CharField(max_length=100)
    item_value_gross_price = models.ForeignKey(ItemValueGrossPrice, on_delete=models.CASCADE)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='position_items')

class DeliveryFeeAmount(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    class Meta:
        unique_together = ('amount', 'currency')

class InitialDeliveryFee(models.Model):
    name = models.CharField(max_length=100)
    delivery_fee_amount = models.ForeignKey(DeliveryFeeAmount, on_delete=models.CASCADE)
    position_items = models.ManyToManyField(PositionItem, related_name='delivery_fees')
    vat_rate = models.FloatField()
    class Meta:
        unique_together = ('name', 'vat_rate')

class Payment(models.Model):
    payment_method = models.CharField(max_length=100, primary_key=True)

class Order(models.Model):
    sales_order_id = models.CharField(max_length=100, unique=True, primary_key=True)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    position_items = models.ManyToManyField(PositionItem, related_name='orders')
    lifecycle_change_date = models.DateTimeField(null=True, blank=True)
    initial_delivery_fees = models.ManyToManyField(InitialDeliveryFee, related_name='orders')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


