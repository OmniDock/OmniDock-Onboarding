from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=50)
    product_title = models.CharField(max_length=255)
    article_number = models.CharField(max_length=50)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.product_title
    
class ItemValueGrossPrice(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.amount} {self.currency}"
    
class DeliveryFeeAmount(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3) 

class PositionItem(models.Model):
    position_item_id = models.CharField(max_length=50)
    fulfillment_status = models.CharField(max_length=50)
    expected_delivery_date = models.DateTimeField(null=True)
    cancellation_reason = models.CharField(max_length=100, blank=True, null=True)
    item_value_gross_price = models.OneToOneField(ItemValueGrossPrice, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.product_title} - {self.fulfillment_status}"

class OrderLifecycleInformation(models.Model):
    lifecycle_change_date = models.DateTimeField()

    def __str__(self):
        return str(self.lifecycle_change_date)

class Payment(models.Model):
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_method

class InitialDeliveryFee(models.Model):
    name = models.CharField(max_length=50)
    delivery_fee_amount = models.OneToOneField(DeliveryFeeAmount, null=True, on_delete=models.SET_NULL)
    position_item_ids = models.ManyToManyField(PositionItem)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    

class Address(models.Model):
    salutation = models.CharField(max_length=10, null=True)
    title = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=255)
    addition = models.CharField(max_length=100, null=True)
    house_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=3, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.street}, {self.zip_code} {self.city}, {self.country_code}"

class Order(models.Model):
    sales_order_id = models.CharField(max_length=50)
    order_number = models.CharField(max_length=50)
    order_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    order_lifecycle_information = models.OneToOneField(OrderLifecycleInformation, null=True, on_delete=models.SET_NULL)
    payment = models.OneToOneField(Payment, null=True, on_delete=models.SET_NULL)
    delivery_address = models.OneToOneField(Address, related_name='order_delivery_address', on_delete=models.CASCADE)
    invoice_address = models.OneToOneField(Address, related_name='order_invoice_address', on_delete=models.CASCADE)
    initial_delivery_fees = models.ManyToManyField(InitialDeliveryFee)
    links = models.JSONField()  

    def __str__(self):
        return self.order_number
    


class Shipment(models.Model):
    creation_date = models.DateTimeField()
    shipment_id = models.CharField(max_length=20)
    carrier = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50)
    occurred_on = models.DateTimeField()
    ship_from_adress = models.OneToOneField(Address, null=True, related_name='ship_from_adress', on_delete=models.SET_NULL)

    def __str__(self):
        return f"Shipment {self.shipment_id}"

