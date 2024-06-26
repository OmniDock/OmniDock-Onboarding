from rest_framework import serializers, viewsets
from .models import OmnidockProduct, OmnidockOrder

class OmnidockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OmnidockProduct
        fields = ('sku', 'product_title', 'gross_income', 'units_sold')

class ProductSalesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OmnidockProduct.objects.all()
    serializer_class = OmnidockProductSerializer


class OmnidockOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OmnidockOrder
        fields = ('marketplace_order_id', 'omnidock_order_id', 'order_date', 'fulfillment_status', 'shipping_date')

class FulfilledOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OmnidockOrder.objects.filter(fulfillment_status='Fulfilled')
    serializer_class = OmnidockOrderSerializer
