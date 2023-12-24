from rest_framework import serializers
from .models import Emform
from common.utils import validators
from common.debug.log import Log
from ..apis.models import Api
from common.platform.products import Product



# Add Emform Configuration Serializer
class AddEmformConfigSerializer(serializers.ModelSerializer):
    api_id = serializers.IntegerField()

    class Meta:
        model = Emform
        fields = ['api_id', 'name', 'config']
    
    def validate(self, attrs):
        api_id = attrs.get('api_id')
        name = attrs.get('name')
        config = attrs.get('config')
        user = self.context.get('user')

        if not Api.objects.filter(id=api_id).exists():
            raise serializers.ValidationError({'api': 'No API found.'})
        
        api = Api.objects.get(id=api_id)
        if api.project.user != user or api.product != Product.emforms.name:
            raise serializers.ValidationError({'api': 'Invalid api for product.'})
        
        if not validators.atleast_length(name, 3) or not validators.atmost_length(name, 20):
            raise serializers.ValidationError({'name': 'Name must be atleast of 3 characters and atmost 20 characters.'})

        if config is None or not isinstance(config, list):
            raise serializers.ValidationError({'config': 'Invalid configuration.'})

        return attrs