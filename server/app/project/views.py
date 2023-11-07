from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.debug.log import Log
from common.platform import platform
from common.utils.response import Response
from . import serializers
from .services import ProjectService



# Project
class UserProject(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = serializers.ProjectSerializer(data=request.data)
            if serializer.is_valid():
                ProjectService.create_project(request.user, serializer.validated_data)

                # success response
                return Response.success({'message': 'Project created successfully.'})

            # error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
