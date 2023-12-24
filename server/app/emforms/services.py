from .models import Emform
from ..apis.models import Api
from ..apis.services import ApiService
from common.debug.log import Log


class EmformService:
    @staticmethod
    def configure(data: dict):
       api = Api.objects.get(id=data.get('api_id'))
       emform = Emform.objects.create(api=api, type=api.type, **data)
       api.config_id = emform.pk
       api.save()
       return EmformService.to_json(emform)
    
    @staticmethod
    def get_configuration(api_id):
        api = Api.objects.get(id=api_id)
        emform = Emform.objects.get(pk=api.config_id, api=api)
        return EmformService.to_json(emform)

    @staticmethod
    def to_json(emform: Emform):
        return {
            'id': emform.pk,
            'api': ApiService.to_json(emform.api),
            'name': emform.name,
            'config': emform.config,
            'updateon': emform.updated_on,
            'createdon': emform.created_on
        } 