from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.debug.log import Log
from common.utils.response import Response
from common.auth.throttling import AuthenticatedUserThrottling
from . import serializers
from .services import ProjectService, ProjectApiService



# User Project
class UserProject(APIView):
    permission_classes = [IsAuthenticated]
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






# User Project Api
class UserProjectApi(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request, project_id):
        try:
            serializer = serializers.AddProjectApiSerializer(data=request.data)
            if serializer.is_valid():
                project_api = ProjectApiService.create_project_api(request.user, project_id, serializer.validated_data)

                # success response
                return Response.success({
                    'message': 'Project api created successfully.', 
                    'projectapi': project_api
                })

            # error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
        
    def get(self, request, project_id):
        try:
            project_apis = ProjectApiService.list_project_apis(request.user, project_id)

            # succcess response
            return Response.success({
                'message': 'Project Api List',
                'projectapis': project_apis
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
    
    def delete(self, request, project_id):
        try:
            id = request.query_params.get('id')
            if id is None:
                return Response.error('Project API Id required.')

            ProjectApiService.delete_project_api(request.user, project_id, id)

            # success response
            return Response.success({'message': 'Project deleted successfully.'})
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()




# User Project Api View
class UserProjectApiView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def get(self, request, project_id):
        try:
            id = request.query_params.get('id')
            if id is None:
                return Response.error('Project API Id required.')

            api_key = ProjectApiService.view_project_api(request.user, project_id, id)

            # success response
            return Response.success({
                'message': 'Project view successfully.',
                'apikey': api_key
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()