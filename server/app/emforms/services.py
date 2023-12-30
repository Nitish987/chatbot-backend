from .models import Emform
from ..apis.models import Api
from ..apis.services import ApiService
from common.debug.log import Log
from firebase_admin import firestore


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


# Emform content generation service
class EmformContentService:
    @staticmethod
    def get_content(emform_id):
        content = {
            'keys': [],
            'data': []
        }
        collection = f'emform_{emform_id}'
        db = firestore.client()
        docs = db.collection(collection).get()
        for doc in docs:
            content['data'].append(doc.to_dict())
        if len(content['data']) > 0:
            content['keys'] = content['data'][0].keys()
        return content