from .models import Chatbot
from ..apis.models import Api
from ..apis.services import ApiService
from common.platform.products import Product



class ChatbotService:
    @staticmethod
    def configure(user, data):
        api = Api.objects.get(id=data.get('api_id'), user=user)
        return Chatbot.objects.create(
            api=api,
            config=data.get('config'),
            data=data.get('data')
        )
    
    @staticmethod
    def get_configuration(user, api_id, chatbot_id):
        api = Api.objects.get(id=api_id, user=user)
        chatbot = Chatbot.objects.get(id=chatbot_id, api=api)
        return ChatbotService.to_json(chatbot)
    
    @staticmethod
    def to_json(chatbot: Chatbot):
        return {
            'id': chatbot.pk,
            'api': ApiService.to_json(chatbot.api),
            'config': chatbot.config,
            'data': chatbot.data
        }
