from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.debug.log import Log
from common.utils.response import Response
from common.auth.throttling import AuthenticatedUserThrottling
from . import serializers
from .services import EmformService



# Emform Config
class EmformConfig(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthenticatedUserThrottling]

    def post(self, request):
        try:
            Log.info(request.data)
            serializer = serializers.AddEmformConfigSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                config = EmformService.configure(serializer.validated_data)

                # success response
                return Response.success({
                    'message': 'Emform Configured.', 
                    'config': config
                })

            # error response
            return Response.errors(serializer.errors)
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
    
    def get(self, request):
        try:
            config = EmformService.get_configuration(
                api_id=request.query_params.get('api_id'),
                emform_id=request.query_params.get('emform_id')
            )

            # success response
            return Response.success({
                'message': 'Emform Configured.', 
                'config': config
            })
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()