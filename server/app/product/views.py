from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.debug.log import Log
from common.platform import platform
from common.utils.response import Response
from common.auth.throttling import AuthenticatedUserThrottling
from .services import ProductService




# App Product
class AppProduct(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def get(self, request):
        try:
            products = ProductService.list_products()

            # succcess response
            return Response.success({
                'message': 'Product List',
                'products': products
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()

