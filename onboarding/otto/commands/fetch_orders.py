from django.core.management.base import BaseCommand
from django.utils import timezone
from otto.api import OttoAPIWrapper
from otto.models import Order, PositionItem, Product, ItemValueGrossPrice, OrderLifecycleInformation, Payment, InitialDeliveryFee, DeliveryFeeAmount

class Command(BaseCommand):
    help = 'Fetch orders from OTTO API and save to database'

    def handle(self, *args, **kwargs):
        try:
            otto_api = OttoAPIWrapper()
            orders_data = otto_api.fetch_orders()

            for order_data in orders_data:
                if 'positionItems' in order_data:
                    for item_data in order_data['positionItems']:
                        # Get or create Product
                        product, created = Product.objects.get_or_create(
                            sku=item_data['product']['sku'],
                            defaults={
                                'product_title': item_data['product']['productTitle'],
                                'article_number': item_data['product']['articleNumber'],
                                'vat_rate': item_data['product']['vatRate']
                                # Add more fields as needed
                            }
                        )

                        # Create ItemValueGrossPrice
                        item_value_gross_price = ItemValueGrossPrice.objects.create(
                            amount=item_data['itemValueGrossPrice']['amount'],
                            currency=item_data['itemValueGrossPrice']['currency']
                        )

                        # Create PositionItem
                        position_item = PositionItem.objects.create(
                            order=order,
                            position_item_id=item_data['positionItemId'],
                            fulfillment_status=item_data['fulfillmentStatus'],
                            expected_delivery_date=timezone.datetime.strptime(item_data.get('expectedDeliveryDate', ''), '%Y-%m-%dT%H:%M:%S.%f%z') if 'expectedDeliveryDate' in item_data else None,
                            cancellation_reason=item_data.get('cancellationReason', None),
                            item_value_gross_price=item_value_gross_price,
                            product=product,
                            # Add more fields as needed
                        )

                order_lifecycle_information = OrderLifecycleInformation.objects.create(
                    lifecycle_change_date=timezone.datetime.strptime(order_data['orderLifecycleInformation']['lifecycleChangeDate'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                )
                payment = Payment.objects.create(
                    paymentMethod=order_data['payment']['paymentMethod']
                )

                deliveryFees = [],
                if 'initialDeliveryFees' in order_data:
                    for initial_delivery_fee in order_data['initialDeliveryFees']:
                        delivery_fee_amount, _ =  DeliveryFeeAmount.objects.get_or_create(
                            amount = initial_delivery_fee['deliveryFeeAmount']['amount'],
                            currency = initial_delivery_fee['deliveryFeeAmount']['currency'],
                        )
                        delivery_fee, _ = InitialDeliveryFee.objects.get_or_create(
                            name = initial_delivery_fee['name'],
                            delivery_fee_amount = delivery_fee_amount,
                            vatRate = initial_delivery_fee['vatRate']
                        )
                        product, created = Product.objects.get_or_create(
                            sku=item_data['product']['sku'],
                            defaults={
                                'product_title': item_data['product']['productTitle'],
                                'article_number': item_data['product']['articleNumber'],
                                'vat_rate': item_data['product']['vatRate']
                                # Add more fields as needed
                            }
                        )
                        deliveryFees += delivery_fee

                # Save order to database
                order = Order.objects.create(
                    sales_order_id=order_data['salesOrderId'],
                    order_number=order_data['orderNumber'],
                    order_date=timezone.datetime.strptime(order_data['orderDate'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                    last_modified_date=timezone.datetime.strptime(order_data['lastModifiedDate'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                    order_lifecycle_information=order_lifecycle_information,
                     payment = payment,
                    links=order_data.get('links', {}) ,
                    initial_delivery_fees = deliveryFees,
                )

                

            self.stdout.write(self.style.SUCCESS('Orders fetched and saved successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching or saving orders: {str(e)}'))
