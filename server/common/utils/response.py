from rest_framework.response import Response as Resp


# default response json
def get_default_response_json():
    response = {
        "success": False,
        "data": {},
        "errors": {}
    }
    return response


class Response:
    # success response
    @staticmethod
    def success(data):
        response = get_default_response_json()
        response['success'] = True
        response['data'] = data
        return Resp(response, status=200)

    # permission denied response
    @staticmethod
    def permission_denied():
        response = get_default_response_json()
        response['errors'] = {
            "server": ['Permission Denied.']
        }
        return Resp(response, status=200)

    # try again response
    @staticmethod
    def try_again(minutes):
        response = get_default_response_json()
        response['errors'] = {
            "server": [f'Please, Try again in {minutes}']
        }
        return Resp(response, status=200)

    # error response
    @staticmethod
    def error(error = "Something went wrong"):
        response = get_default_response_json()
        response['errors'] = {
            "server": [error]
        }
        return Resp(response, status=200)
    
    # errors response
    @staticmethod
    def errors(errors):
        response = get_default_response_json()
        response['errors'] = errors
        return Resp(response, status=200)
    
    # something went wrong response
    @staticmethod
    def something_went_wrong():
        response = get_default_response_json()
        response['errors'] = {
            "server": ["Something went wrong"]
        }
        return Resp(response, status=200)
