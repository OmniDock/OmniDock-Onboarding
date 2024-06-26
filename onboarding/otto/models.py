from django.db import models

class TrackingInfo(models.Model):
    carrier = models.CharField(max_length=20)
    tracking_number = models.CharField(max_length=50, primary_key=True)

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    product_title = models.CharField(max_length=255)
    article_number = models.CharField(max_length=255, primary_key=True)

class ItemValueGrossPrice(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    class Meta:
        unique_together = ('amount', 'currency')

class Order(models.Model):
    sales_order_id = models.CharField(max_length=100, primary_key=True)
    order_number = models.CharField(max_length=100)
    order_date = models.DateTimeField()


class PositionItem(models.Model):
    position_item_id = models.CharField(max_length=100, primary_key=True)
    fulfillment_status = models.CharField(max_length=100)
    item_value_gross_price = models.ForeignKey(ItemValueGrossPrice,null=True ,on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    

