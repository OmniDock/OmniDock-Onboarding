from django.http import JsonResponse
from otto.api import OttoAPIWrapper

def fetch_orders_view(request):
    otto_api = OttoAPIWrapper()
    try:
        orders = otto_api.fetch_orders()
        return JsonResponse({'orders': orders})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def fetch_shipments_view(request):
    otto_api = OttoAPIWrapper()
    try:
        orders = otto_api.fetch_shipments()
        print("orders", orders)
        return JsonResponse({'shipments': orders})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    