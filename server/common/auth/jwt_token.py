from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from jwt import encode, decode


class Jwt:
    ACCESS = 0
    REFRESH = 1

    @staticmethod
    def validate(token, category: int = ACCESS):
        '''returns the payload if JWT token is valid'''
        payload = {}
        try:
            if category == Jwt.ACCESS:
                payload = decode(token, settings.JWT_ACCESS_SECRET, algorithms=["HS256"])
            else:
                payload = decode(token, settings.JWT_REFRESH_SECRET, algorithms=["HS256"])
            return (True, payload)
        except:
            return (False, payload)
    
    @staticmethod
    def generate(type: str, sub: str | None = None, data: dict | None = None, category: int = ACCESS, seconds: int | None = None):
        '''returns generated JWT token using the given payload type (token for type), data, t_type (token type, can be ACCESS or REFRESH) and seconds''' 
        payload = { 'type': type }

        if sub != None:
            payload['sub'] = sub
        
        if data != None:
            payload['data'] = data

        if seconds != None:
            payload['exp'] = timezone.now() + timedelta(seconds=seconds)

        if category == Jwt.ACCESS:
            token = encode(payload, settings.JWT_ACCESS_SECRET, algorithm = 'HS256')
        else:
            token = encode(payload, settings.JWT_REFRESH_SECRET, algorithm = 'HS256')
        return token
    
