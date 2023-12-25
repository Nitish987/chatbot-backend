from rest_framework.views import APIView
from common.utils.response import Response
from common.debug.log import Log
from common.auth.permissions import IsExternalAuthenticated
from .services import ExternalExportService



class ExternalExportProject(APIView):
    permission_classes = [IsExternalAuthenticated]

    def get(self, request):
        try: 
            project_id = request.query_params.get('project_id', None)
            if project_id is None:
                return Response.error('Project id not specified.')
            
            project = ExternalExportService.get_project(project_id)
            return Response.success({
                'project': project
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()



class ExternalExportProduct(APIView):
    permission_classes = [IsExternalAuthenticated]

    def get(self, request):
        try: 
            project_id = request.query_params.get('project_id', None)
            api_id = request.query_params.get('api_id', None)

            if project_id is None:
                return Response.error('Project id not specified.')
            if api_id is None:
                return Response.error('Api id not specified')
            
            product = ExternalExportService.get_product(project_id, api_id)
            return Response.success(product)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()



class ExternalExportBillingUpdate(APIView):
    permission_classes = [IsExternalAuthenticated]

    def put(self, request):
        try: 
            project_id = request.query_params.get('project_id', None)
            api_id = request.query_params.get('api_id', None)

            if project_id is None:
                return Response.error('Project id not specified.')
            if api_id is None:
                return Response.error('Api id not specified')
            
            price_to_pay = ExternalExportService.update_billing(project_id, api_id)
            return Response.success({'price_to_pay': price_to_pay})
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
