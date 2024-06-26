from rest_framework import serializers
from .models import ProductDimension, Product, ItemValueGrossPrice, PositionItem, DeliveryFeeAmount, InitialDeliveryFee, Payment, Order

class ProductDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDimension
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    dimensions = ProductDimensionSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        dimensions_data = validated_data.pop('dimensions')
        product = Product.objects.create(**validated_data)
        for dimension_data in dimensions_data:
            dimension, created = ProductDimension.objects.get_or_create(**dimension_data)
            product.dimensions.add(dimension)
        return product

class ItemValueGrossPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemValueGrossPrice
        fields = '__all__'

class PositionItemSerializer(serializers.ModelSerializer):
    item_value_gross_price = ItemValueGrossPriceSerializer()
    product = ProductSerializer()

    class Meta:
        model = PositionItem
        fields = '__all__'

    def create(self, validated_data):
        item_value_gross_price_data = validated_data.pop('item_value_gross_price')
        product_data = validated_data.pop('product')
        item_value_gross_price = ItemValueGrossPrice.objects.create(**item_value_gross_price_data)
        product_serializer = ProductSerializer(data=product_data)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()
        position_item = PositionItem.objects.create(
            item_value_gross_price=item_value_gross_price,
            product=product,
            **validated_data
        )
        return position_item

class DeliveryFeeAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFeeAmount
        fields = '__all__'

class InitialDeliveryFeeSerializer(serializers.ModelSerializer):
    delivery_fee_amount = DeliveryFeeAmountSerializer()
    position_items = PositionItemSerializer(many=True)

    class Meta:
        model = InitialDeliveryFee
        fields = '__all__'

    def create(self, validated_data):
        delivery_fee_amount_data = validated_data.pop('delivery_fee_amount')
        position_items_data = validated_data.pop('position_items')
        delivery_fee_amount = DeliveryFeeAmount.objects.create(**delivery_fee_amount_data)
        initial_delivery_fee = InitialDeliveryFee.objects.create(
            delivery_fee_amount=delivery_fee_amount,
            **validated_data
        )
        for position_item_data in position_items_data:
            position_item_serializer = PositionItemSerializer(data=position_item_data)
            position_item_serializer.is_valid(raise_exception=True)
            position_item = position_item_serializer.save()
            initial_delivery_fee.position_items.add(position_item)
        return initial_delivery_fee

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    position_items = PositionItemSerializer(many=True)
    initial_delivery_fees = InitialDeliveryFeeSerializer(many=True)
    payment = PaymentSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        position_items_data = validated_data.pop('position_items')
        initial_delivery_fees_data = validated_data.pop('initial_delivery_fees')
        payment_data = validated_data.pop('payment')
        payment = Payment.objects.create(**payment_data)
        order = Order.objects.create(payment=payment, **validated_data)

        for position_item_data in position_items_data:
            position_item_serializer = PositionItemSerializer(data=position_item_data)
            position_item_serializer.is_valid(raise_exception=True)
            position_item = position_item_serializer.save()
            order.position_items.add(position_item)

        for initial_delivery_fee_data in initial_delivery_fees_data:
            initial_delivery_fee_serializer = InitialDeliveryFeeSerializer(data=initial_delivery_fee_data)
            initial_delivery_fee_serializer.is_valid(raise_exception=True)
            initial_delivery_fee = initial_delivery_fee_serializer.save()
            order.initial_delivery_fees.add(initial_delivery_fee)

        return order
