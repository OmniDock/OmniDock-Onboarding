from rest_framework import serializers
from .models import Order, Product, PositionItem, ItemValueGrossPrice, TrackingInfo

class ItemValueGrossPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemValueGrossPrice
        fields = ['amount', 'currency']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['sku', 'product_title', 'omnidock_article_number']


class TrackingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingInfo
        fields = ['carrier', 'tracking_number']

class PositionItemSerializer(serializers.ModelSerializer):
    item_value_gross_price = ItemValueGrossPriceSerializer()
    product = ProductSerializer()
    tracking_info = TrackingInfoSerializer()

    class Meta:
        model = PositionItem
        fields = ['position_item_id', 'fulfillment_status', 'sentDate', 'item_value_gross_price', 'product', 'tracking_info']


class OrderSerializer(serializers.ModelSerializer):
    position_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['marketplace_order_id', 'omnidock_order_id', 'order_date', 'shipping_date', 'position_items']

    def get_position_items(self, obj):
        # Fetching only the fulfilled position items
        fulfilled_items = PositionItem.objects.filter(order=obj, fulfillment_status='fulfilled')
        return PositionItemSerializer(fulfilled_items, many=True).data

class ProductSalesSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=100)
    product_title = serializers.CharField(max_length=255)
    sold_count = serializers.IntegerField()
    gross_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)