from rest_framework.views import APIView
from common.utils.response import Response
from common.debug.log import Log
from common.auth.permissions import IsExternalAuthenticated
from .services import ExternalExportService



# External Api Server data Validation API
class ExternalExport(APIView):
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
