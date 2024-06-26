from .api import OttoAPIWrapper
import logging
from .serializers import OrderSerializer

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
                print(order_data)
                if not isinstance(order_data, dict):
                    logger.error(f"Unexpected order data format: {order_data}")
                    continue
                serializer = OrderSerializer(data=order_data)
                if serializer.is_valid():
                    order = serializer.save()
                    print(order)
                else:
                    print("Error")
                
        except Exception as e:
            logger.error(f"Error in OrderTask: {e}", exc_info=True)