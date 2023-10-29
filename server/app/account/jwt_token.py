import base64
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from jwt import encode, decode
from utils.security import AES256


class Jwt:
    # returns the payload if JWT token is valida
    @staticmethod
    def validate(token):
        payload = {}
        try:
            payload = decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return (True, payload)
        except:
            return (False, payload)
    
    # returns generated JWT token using the given payload type, data and seconds 
    @staticmethod
    def generate(type, data, seconds = None):
        payload = { 'type': type, 'data': data }

        if seconds != None:
            payload['exp'] = timezone.now() + timedelta(seconds=seconds)

        token = encode(payload, settings.JWT_SECRET, algorithm = 'HS256')
        return token
    
