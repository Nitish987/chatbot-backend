from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, Throttled
from ..utils.response import get_default_response_json

def ExceptionHandler(exc, context):
    response = exception_handler(exc, context)

    try:
        res = get_default_response_json()

        if isinstance(exc, NotAuthenticated):
            res['errors'] ={
                'account': ['Invalid Credentials or Credentials not provided.']
            }
            response.data = res
            response.status_code = 401

        if isinstance(exc, Throttled):
            res['errors'] = {
                'server': ['Your Limit Exceeded. Please try again after some time.']
            }
            response.data = res
            response.status_code = 429
    except:
        res['errors'] = {
            'server': ['Something went wrong.']
        }
        response.data = res
        response.status_code = 403

    return response