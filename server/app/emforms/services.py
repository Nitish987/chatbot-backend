from .models import Emform
from ..apis.models import Api
from ..apis.services import ApiService


class EmformService:
    @staticmethod
    def configure(data: dict):
       api = Api.objects.get(id=data.get('api_id'))
       emform = Emform.objects.create(api=api, type=api.type, **data)
       return EmformService.to_json(emform)
    
    @staticmethod
    def get_configuration(api_id, emform_id):
        api = Api.objects.get(id=api_id)
        emform = Emform.objects.get(id=emform_id, api=api)
        return EmformService.to_json(emform)

    @staticmethod
    def to_json(emform: Emform):
        return {
            'id': emform.pk,
            'api': ApiService.to_json(emform.api),
            'config': emform.config,
            'updateon': emform.updated_on,
            'createdon': emform.created_on
        } 