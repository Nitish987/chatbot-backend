from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.debug.log import Log
from common.platform import platform
from common.utils.response import Response
from common.auth.throttling import AuthenticatedUserThrottling
from . import serializers
from .services import ProjectService



# User Project
class UserProject(APIView):
    permission_class = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            serializer = serializers.AddProjectSerializer(data=request.data)
            if serializer.is_valid():
                project = ProjectService.create_project(request.user, serializer.validated_data)

                # success response
                return Response.success({
                    'message': 'Project created successfully.', 
                    'project': project
                })

            # error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
        
    def get(self, request):
        try:
            projects = ProjectService.list_project(request.user)

            # succcess response
            return Response.success({
                'message': 'Project List',
                'projects': projects
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()

    def put(self, request):
        try:
            id = request.query_params.get('id')
            if id is None:
                return Response.error('Project Id required.')
            
            serializer = serializers.UpdateProjectSerializer(data=request.data)
            if serializer.is_valid():
                project = ProjectService.update_project(id, serializer.validated_data)

                # success response
                return Response.success({
                    'message': 'Project updated successfully.',
                    'project': project
                })

            # error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
    
    def delete(self, request):
        try:
            id = request.query_params.get('id')
            if id is None:
                return Response.error('Project Id required.')

            ProjectService.delete_project(id)

            # success response
            return Response.success({'message': 'Project deleted successfully.'})
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()