from .models import Chatbot
from ..apis.models import Api
from ..apis.services import ApiService
from common.platform.products import Product
from common.debug.log import Log



class ChatbotService:
    @staticmethod
    def configure(data):
        api = Api.objects.get(id=data.get('api_id'))
        chatbot = Chatbot.objects.create(api=api, type=api.type, **data)
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
            'emformConfigId': chatbot.emform_config_id,
            'config': chatbot.config,
            'data': chatbot.data,
            'updateon': chatbot.updated_on,
            'createdon': chatbot.created_on
        }
