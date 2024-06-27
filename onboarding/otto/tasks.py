from .api import OttoAPIWrapper
import logging
from .serializers import OrderSerializer, PositionItemSerializer, ProductSerializer, ItemValueGrossPriceSerializer

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
                position_items = order_data.get('positionItems')
                for position_item_data in position_items:
                    price_data = position_item_data.get('itemValueGrossPrice')
                    price_serializer = ItemValueGrossPriceSerializer(data=price_data)
                    if price_serializer.is_valid():
                        price_item = price_serializer.save()
                        print(price_item)
                    else:
                        print("Error")

                    pos_item_serializer = PositionItemSerializer(data=position_item_data)
                    if pos_item_serializer.is_valid():
                        position_item = pos_item_serializer.save()
                        print(position_item)
                    else:
                        print("Error")
                # print(order_data)
                order_serializer = OrderSerializer(data=order_data)
                if order_serializer.is_valid():
                    order = order_serializer.save()
                    print(order)
                else:
                    print("Error")
                
        except Exception as e:
            logger.error(f"Error in OrderTask: {e}", exc_info=True)