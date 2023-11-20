from rest_framework import serializers
from .models import Chatbot
from common.utils import validators
from common.debug.log import Log
from ..apis.models import Api
from common.platform.products import Product



# Add Chatbot Configuration Serializer
class AddChatbotConfigSerializer(serializers.ModelSerializer):
    api_id = serializers.IntegerField()
    config = serializers.CharField()
    data = serializers.CharField()

    class Meta:
        model = Chatbot
        fields = ['api_id', 'config', 'data']
    
    def validate(self, attrs):
        api_id = attrs.get('api_id')
        config = attrs.get('config')
        data = attrs.get('data')
        user = self.context.get('user')

        if not Api.objects.filter(id=api_id, user=user).exists():
            raise serializers.ValidationError({'api': 'Permission denied.'})
        
        if Api.objects.get(id=api_id, user=user).product != Product.chatbot.name:
            raise serializers.ValidationError({'api': 'Invalid api for product.'})

        if config is None:
            raise serializers.ValidationError({'config': 'Invalid configuration.'})
        
        if data is None:
            raise serializers.ValidationError({'data': 'Invalid data.'})

        return attrs