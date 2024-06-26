from django.db import transaction
from .models import Order, ProductDimension, Product, ItemValueGrossPrice, DeliveryFeeAmount, Payment, InitialDeliveryFee, PositionItem
from .api import OttoAPIWrapper
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OrderTask:
    @staticmethod
    def run():
        api = OttoAPIWrapper()
        try:
            orders_data = api.get_orders()
            logger.debug(f"Fetched orders data: {orders_data}")

            if not isinstance(orders_data, list):
                raise ValueError("Expected a list of orders")

            for order_data in orders_data:
                if not isinstance(order_data, dict):
                    logger.error(f"Unexpected order data format: {order_data}")
                    continue

                with transaction.atomic():
                    # Process Payment
                    payment_data = order_data.get('payment', {})
                    payment_method = payment_data.get('paymentMethod')
                    payment_instance, _ = Payment.objects.update_or_create(payment_method=payment_method)

                    # Process InitialDeliveryFees
                    delivery_fees = []
                    for fee in order_data.get('initialDeliveryFees', []):
                        delivery_fee_amount_data = fee.get('deliveryFeeAmount', {})
                        delivery_fee_amount_instance, _ = DeliveryFeeAmount.objects.update_or_create(
                            amount=delivery_fee_amount_data.get('amount'),
                            currency=delivery_fee_amount_data.get('currency')
                        )
                        initial_delivery_fee_instance, _ = InitialDeliveryFee.objects.update_or_create(
                            name=fee.get('name'),
                            delivery_fee_amount=delivery_fee_amount_instance,
                            vat_rate=fee.get('vatRate')
                        )
                        delivery_fees.append(initial_delivery_fee_instance)

                    # Create or update Order
                    order, created = Order.objects.update_or_create(
                        sales_order_id=order_data.get('salesOrderId'),
                        defaults={
                            'order_number': order_data.get('orderNumber'),
                            'order_date': order_data.get('orderDate'),
                            'last_modified_date': order_data.get('lastModifiedDate'),
                            'lifecycle_change_date': order_data.get('orderLifecycleInformation', {}).get('lifecycleChangeDate'),
                            'payment': payment_instance
                        }
                    )

                    # Process PositionItems
                    for position_data in order_data.get('positionItems', []):
                        # Process ItemValueGrossPrice
                        item_value_gross_price_data = position_data.get('itemValueGrossPrice', {})
                        item_value_gross_price_instance, _ = ItemValueGrossPrice.objects.update_or_create(
                            amount=item_value_gross_price_data.get('amount'),
                            currency=item_value_gross_price_data.get('currency')
                        )

                        # Process Product (separately from PositionItem)
                        product_data = position_data.get('product', {})
                        product_instance, _ = Product.objects.update_or_create(
                            sku=product_data.get('sku'),
                            defaults={
                                'product_title': product_data.get('productTitle'),
                                'article_number': product_data.get('articleNumber'),
                                'ean': product_data.get('ean'),
                                'vat_rate': product_data.get('vatRate')
                            }
                        )

                        # Process PositionItem
                        cancellation_date_str = position_data.get('cancellationDate')
                        cancellation_date = datetime.strptime(cancellation_date_str, '%Y-%m-%dT%H:%M:%S.%f%z') if cancellation_date_str else None

                        position_item_instance, _ = PositionItem.objects.update_or_create(
                            position_item_id=position_data.get('positionItemId'),
                            defaults={
                                'fulfillment_status': position_data.get('fulfillmentStatus'),
                                'item_value_gross_price': item_value_gross_price_instance,
                                'cancellation_date': cancellation_date,
                                'cancellation_reason': position_data.get('cancellationReason'),
                            },
                        )

                        position_item_instance.add(product_instance)

                        order.position_items.add(position_item_instance)

                       
                        # Process ProductDimensions
                        for dimension_data in product_data.get('dimensions', []):
                            dimension_instance, _ = ProductDimension.objects.update_or_create(
                                type=dimension_data.get('type'),
                                display_name=dimension_data.get('displayName'),
                                value=dimension_data.get('value')
                            )
                            product_instance.dimensions.add(dimension_instance)

                    # Add InitialDeliveryFees to Order
                    order.initial_delivery_fees.set(delivery_fees)

                    order.save()
                    logger.info(f"Order {'created' if created else 'updated'}: {order.sales_order_id}")

        except Exception as e:
            logger.error(f"Error in OrderTask: {e}", exc_info=True)