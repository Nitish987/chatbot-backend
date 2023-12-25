from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.utils.response import Response
from common.debug.log import Log
from .services import BillingService



class BillingDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try: 
            billings = BillingService.get_billing(request.user)
            return Response.success({
                'billings': billings
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()




class BillingDashboardByProject(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try: 
            billing = BillingService.get_billing_By_project(request.user, project_id)
            return Response.success({
                'billing': billing
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()