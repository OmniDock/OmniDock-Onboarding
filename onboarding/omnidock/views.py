from django.db.models import Sum, Count, F
from rest_framework import generics
from rest_framework.response import Response
from .models import Order, Product, PositionItem
from .serializers import ProductSalesSerializer, OrderFulfillmentSerializer

# class ProductSalesListView(generics.ListAPIView):
#     serializer_class = ProductSalesSerializer

#     def get_queryset(self):
#         return Product.objects.annotate(
#             total_sales=Count('positionitem'),
#             total_revenue=Sum('positionitem__item_value_gross_price__amount')
#         )
# 
# class OrderFulfillmentListView(generics.ListAPIView):
#     serializer_class = OrderFulfillmentSerializer

#     def get_queryset(self):
#         return Order.objects.annotate(
#             order_status=F('positionitem__fulfillment_status')
#         ).filter(
#             positionitem__fulfillment_status__in=['Ready to Fulfill', 'Fulfilled']
#         ).distinct()
