from rest_framework import serializers
from .models import Project, ProjectApi
from ..product.models import Product
from common.utils import validators
from common.debug.log import Log



# Add Project Serializer
class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'envtype']
    
    def validate(self, attrs):
        name = attrs.get('name')
        description = attrs.get('description')
        envtype = attrs.get('envtype')

        if not validators.atleast_length(name, 5) or validators.contains_script(name):
            raise serializers.ValidationError({'name': 'Name must be of 5 character atleast.'})
        
        if not validators.atleast_length(description, 20) or validators.contains_script(description):
            raise serializers.ValidationError({'desc': 'Description must be of 20 character atleast.'})
        
        if envtype not in ['DEVELOPMENT', 'PRODUCTION']:
            raise serializers.ValidationError({'envtype': 'Invalid Environment Type.'})

        return attrs




# Project Serializer
class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['description', 'envtype']
    
    def validate(self, attrs):
        description = attrs.get('description')
        envtype = attrs.get('envtype')
        
        if not validators.atleast_length(description, 20) or validators.contains_script(description):
            raise serializers.ValidationError({'desc': 'Description must be of 20 character atleast.'})
        
        if envtype not in ['DEVELOPMENT', 'PRODUCTION']:
            raise serializers.ValidationError({'envtype': 'Invalid Environment Type.'})

        return attrs





# Add Project Api Serializer
class AddProjectApiSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    host = serializers.CharField()

    class Meta:
        model = ProjectApi
        fields = ['product_id', 'host']
    
    def validate(self, attrs):
        product_id = attrs.get('product_id')
        host = attrs.get('host')

        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError({'ids': 'Invalid product specified.'})
        
        if host is None:
            raise serializers.ValidationError({'host': 'Invalid host list.'})

        return attrs