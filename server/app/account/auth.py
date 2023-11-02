from rest_framework import authentication
from rest_framework import exceptions
from .models import User
from .jwt_token import Jwt
from constants.tokens import TokenType
from constants.headers import Header


# User Authentication
class WebUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            # getting validation success and payload from authentication token
            bearer_token = request.COOKIES.get('HTTP_AUTHORIZATION').split(' ')[1]
            success, payload = Jwt.validate(bearer_token)
            payload_data = payload['data']
        
            # validating authentication token
            if not success or payload['type'] != TokenType.LOGIN or payload_data['uid'] != request.META.get(Header.USER_ID):
                return None

            try:
                # fetching user from database
                user = User.objects.get(uid=payload_data['uid'])
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such Account found.')

            return (user, None)
        except:
            return None

