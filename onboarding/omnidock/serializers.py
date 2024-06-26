from rest_framework import serializers
from .models import Order, Product, PositionItem

class ProductSalesSerializer(serializers.ModelSerializer):
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ['sku', 'product_title', 'total_sales', 'total_revenue']

class OrderFulfillmentSerializer(serializers.ModelSerializer):
    shipping_date = serializers.DateTimeField()
    order_status = serializers.CharField()
    
    class Meta:
        model = Order
        fields = ['marketplace_order_id', 'omnidock_order_id', 'order_date', 'shipping_date', 'order_status']
