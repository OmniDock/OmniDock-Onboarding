from django.db.models import Sum, Count, F
from rest_framework import generics
from .models import Order, Product, PositionItem
from .serializers import OrderSerializer, ProductSalesSerializer 

class ProductSalesListView(generics.ListAPIView):
    serializer_class = ProductSalesSerializer

    def get_queryset(self):
        queryset = (
            Product.objects
            .annotate(
                sold_count=Count('positionitem'),
                gross_revenue=Sum(F('positionitem__item_value_gross_price__amount'))
            )
            .values('sku', 'product_title', 'sold_count', 'gross_revenue')
        )
        return queryset

class FullFilledOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        queryset = (
            Order.objects
            .filter(positionitem__fulfillment_status='fulfilled')
            .values('omnidock_order_id', 'order_date', 'shipping_date')
            .distinct()
        )
        return queryset
