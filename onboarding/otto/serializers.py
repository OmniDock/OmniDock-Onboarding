from rest_framework import serializers
from .models import Product, ItemValueGrossPrice, PositionItem, Order



class TrackingInfo:
    def __init__(self, carrier, tracking_number):
        self.carrier = carrier,
        self.tracking_number = tracking_number,

class Product:
    def __init__(self, sku, product_title, article_number):
        self.sku = sku
        self.product_title = product_title
        self.article_number = article_number

class ItemValueGrossPrice:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

class Order:
    def __init__(self, sales_order_id, order_number, order_date):
        self.sales_order_id = sales_order_id
        self.order_number = order_number
        self.order_date = order_date

class PositionItem:
    def __init__(self, position_item_id, fulfillment_status, item_value_gross_price, product, order):
        self.position_item_id = position_item_id
        self.fulfillment_status = fulfillment_status
        self.item_value_gross_price = item_value_gross_price
        self.product = product
        self.order = order

class TrackingInfoSerializer(serializers.Serializer):
    carrier = serializers.CharField(max_length=20)
    tracking_number = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return TrackingInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.carrier = validated_data.get('carrier', instance.carrier)
        instance.tracking_number = validated_data.get('trackingNumber', instance.tracking_number)
        instance.save()
        return instance
    
class ProductSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=100)
    product_title = serializers.CharField(max_length=255)
    article_number = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sku = validated_data.get('sku', instance.sku)
        instance.product_title = validated_data.get('productTitle', instance.product_title)
        instance.article_number = validated_data.get('articleNumber', instance.article_number)
        instance.save()
        return instance

class ItemValueGrossPriceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=10)

    def create(self, validated_data):
        return ItemValueGrossPrice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.save()
        return instance

class OrderSerializer(serializers.Serializer):
    sales_order_id = serializers.CharField(max_length=100)
    order_number = serializers.CharField(max_length=100)
    order_date = serializers.DateTimeField()

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sales_order_id = validated_data.get('salesOrderId', instance.sales_order_id)
        instance.order_number = validated_data.get('orderNumber', instance.order_number)
        instance.order_date = validated_data.get('orderDate', instance.order_date)
        instance.save()
        return instance

class PositionItemSerializer(serializers.Serializer):
    position_item_id = serializers.CharField(max_length=100)
    fulfillment_status = serializers.CharField(max_length=100)
    item_value_gross_price = ItemValueGrossPriceSerializer(required=False)
    product = ProductSerializer()
    order = OrderSerializer()

    def create(self, validated_data):
        item_value_gross_price_data = validated_data.pop('item_value_gross_price', None)
        product_data = validated_data.pop('product')
        order_data = validated_data.pop('order')
        
        item_value_gross_price = None
        if item_value_gross_price_data:
            item_value_gross_price = ItemValueGrossPrice.objects.create(**item_value_gross_price_data)
        
        product = Product.objects.create(**product_data)
        order = Order.objects.create(**order_data)
        
        return PositionItem.objects.create(
            item_value_gross_price=item_value_gross_price,
            product=product,
            order=order,
            **validated_data
        )

    def update(self, instance, validated_data):
        item_value_gross_price_data = validated_data.pop('item_value_gross_price', None)
        product_data = validated_data.pop('product', None)
        order_data = validated_data.pop('order', None)

        if item_value_gross_price_data:
            item_value_gross_price = instance.item_value_gross_price
            if item_value_gross_price:
                item_value_gross_price.amount = item_value_gross_price_data.get('amount', item_value_gross_price.amount)
                item_value_gross_price.currency = item_value_gross_price_data.get('currency', item_value_gross_price.currency)
                item_value_gross_price.save()
            else:
                item_value_gross_price = ItemValueGrossPrice.objects.create(**item_value_gross_price_data)
                instance.item_value_gross_price = item_value_gross_price

        if product_data:
            product = instance.product
            product.sku = product_data.get('sku', product.sku)
            product.product_title = product_data.get('product_title', product.product_title)
            product.article_number = product_data.get('article_number', product.article_number)
            product.save()

        if order_data:
            order = instance.order
            order.sales_order_id = order_data.get('sales_order_id', order.sales_order_id)
            order.order_number = order_data.get('order_number', order.order_number)
            order.order_date = order_data.get('order_date', order.order_date)
            order.save()

        instance.position_item_id = validated_data.get('position_item_id', instance.position_item_id)
        instance.fulfillment_status = validated_data.get('fulfillment_status', instance.fulfillment_status)
        instance.save()
        return instance