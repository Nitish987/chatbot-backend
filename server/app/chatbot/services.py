from .models import Chatbot
from ..apis.models import Api
from ..apis.services import ApiService
from ..emforms.models import Emform
from ..emforms.services import EmformService
from common.platform.products import Product
from common.debug.log import Log



class ChatbotService:
    @staticmethod
    def configure(data):
        api = Api.objects.get(id=data.get('api_id'))
        if data.get('use_emform'):
            emform = Emform.objects.get(pk=data.get('emform_config_id'))
        else:
            emform = None
        del data['emform_config_id']
        chatbot = Chatbot.objects.create(api=api, type=api.type, emform=emform, **data)
        api.config_id = chatbot.pk
        api.save()
        return ChatbotService.to_json(chatbot)
    
    @staticmethod
    def get_configuration(api_id):
        api = Api.objects.get(id=api_id)
        chatbot = Chatbot.objects.get(pk=api.config_id, api=api)
        return ChatbotService.to_json(chatbot)
    
    @staticmethod
    def to_json(chatbot: Chatbot):
        return {
            'id': chatbot.pk,
            'api': ApiService.to_json(chatbot.api),
            'name': chatbot.name,
            'photo': chatbot.photo.url,
            'greeting': chatbot.greeting,
            'engine': chatbot.engine,
            'model': chatbot.model,
            'sysprompt': chatbot.sys_prompt,
            'knowledge': chatbot.knowledge,
            'useEmform': chatbot.use_emform,
            'whenEmform': chatbot.when_emform,
            'emform': EmformService.to_json(chatbot.emform) if chatbot.use_emform else None,
            'config': chatbot.config,
            'data': chatbot.data,
            'updateon': chatbot.updated_on,
            'createdon': chatbot.created_on
        }
