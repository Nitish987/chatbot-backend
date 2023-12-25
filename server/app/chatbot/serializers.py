from rest_framework import serializers
from .models import Chatbot
from common.utils import validators
from common.debug.log import Log
from ..apis.models import Api
from ..emforms.models import Emform
from common.platform.products import Product



# Add Chatbot Configuration Serializer
class AddChatbotConfigSerializer(serializers.ModelSerializer):
    api_id = serializers.IntegerField()
    emform_config_id = serializers.IntegerField()

    class Meta:
        model = Chatbot
        fields = ['api_id', 'name', 'photo', 'greeting', 'engine', 'model',  'sys_prompt', 'knowledge', 'use_emform', 'when_emform', 'emform_config_id', 'config', 'data']
    
    def validate(self, attrs):
        api_id = attrs.get('api_id')
        name = attrs.get('name')
        photo = attrs.get('photo')
        greeting = attrs.get('greeting')
        engine = attrs.get('engine')
        model = attrs.get('model')
        sys_prompt = attrs.get('sys_prompt')
        knowledge = attrs.get('knowledge')
        use_emform = attrs.get('use_emform')
        when_emform = attrs.get('when_emform')
        emform_config_id = attrs.get('emform_config_id')
        config = attrs.get('config')
        data = attrs.get('data')
        user = self.context.get('user')

        if not Api.objects.filter(id=api_id).exists():
            raise serializers.ValidationError({'api': 'No API found.'})
        
        api = Api.objects.get(id=api_id)
        if api.project.user != user or api.product != Product.chatbot.name:
            raise serializers.ValidationError({'api': 'Invalid api for product.'})
        
        if not validators.atleast_length(name, 3) or not validators.atmost_length(name, 20):
            raise serializers.ValidationError({'name': 'Name must be atleast of 3 characters and atmost 20 characters.'})
        
        if photo is None:
            raise serializers.ValidationError({'photo': 'No Bot profile pic provided.'})
        
        if not validators.atleast_length(greeting, 2) or not validators.atmost_length(greeting, 200):
            raise serializers.ValidationError({'greeting': 'Greeting must be atleast of 2 characters and atmost 200 characters.'})
        
        if engine not in Product.chatbot.engines:
            raise serializers.ValidationError({'engine': 'Engine must be specified.'})
        
        if api.type == Product.chatbot.types[1]:
            if model not in Product.chatbot.models_list:
                raise serializers.ValidationError({'model': 'Model must be specified.'})
            
            if not validators.atleast_length(sys_prompt, 2) or not validators.atmost_length(sys_prompt, 200) or validators.contains_script(sys_prompt):
                raise serializers.ValidationError({'greeting': 'System Prompt must be atleast of 2 characters and atmost 200 characters.'})
        
            if validators.contains_script(knowledge):
                raise serializers.ValidationError({'greeting': 'Knowledge must specified.'})

        if use_emform is None or not isinstance(use_emform, bool):
            raise serializers.ValidationError({'emfrom': 'Invalid emform specification.'})
        
        if when_emform is None:
            raise serializers.ValidationError({'emform': 'Invalid emform specification.'})
        
        if use_emform and not Emform.objects.filter(pk=emform_config_id).exists():
            raise serializers.ValidationError({'api': 'No Emform found.'})

        if config is None or not isinstance(config, dict):
            raise serializers.ValidationError({'config': 'Invalid configuration.'})
        
        if data is None or not isinstance(data, dict):
            raise serializers.ValidationError({'data': 'Invalid data.'})

        return attrs