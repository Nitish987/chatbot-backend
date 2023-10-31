import user_agents
from rest_framework import authentication
from rest_framework import exceptions
from .models import User
from .services import LoginStateTokenService
from .jwt_token import Jwt


# User Authentication
class WebUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            # getting validation success and payload from authentication token
            success, payload = Jwt.validate(request.COOKIES.get('HTTP_AUTHORIZATION'))
            payload_data = payload['data']
        
            # validating authentication token
            if not success or payload['type'] != 'LI' or payload_data['uid'] != request.META.get("HTTP_UID"):
                return None

            try:
                # fetching user from database
                user = User.objects.get(uid=payload_data['uid'])
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such Account found.')

            try:
                login_state = LoginStateTokenService.get(user=user)

                if login_state['login_token'] != request.META['HTTP_LST']:
                    return None

                # passing user agent data
                ua = user_agents.parse(request.META['HTTP_USER_AGENT'])

                # validing login state token data with user agent
                if login_state['browser'] != ua.browser.family or login_state['device'] != ua.device.family or login_state['os'] != ua.os.family:
                    return None
            except:
                raise exceptions.AuthenticationFailed('No Login user found.')

            return (user, None)
        except:
            return None

