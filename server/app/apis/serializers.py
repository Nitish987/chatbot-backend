from rest_framework import serializers
from .models import Api
from common.platform.products import Product
from common.utils import validators
from common.debug.log import Log



# Add Project Api Serializer
class AddApiSerializer(serializers.ModelSerializer):
    host = serializers.CharField()

    class Meta:
        model = Api
        fields = ['product', 'type', 'host']
    
    def validate(self, attrs):
        product = attrs.get('product')
        type = attrs.get('type')
        host = attrs.get('host')

        if product not in Product.products():
            raise serializers.ValidationError({'product': 'Invalid product specified.'})
        
        if type not in Product.product_types():
            raise serializers.ValidationError({'type': 'Invalid product type.'})
        
        if not Product.is_product_type_valid(product, type):
            raise serializers.ValidationError({'product': 'Invalid product or type specified.'})
        
        if host is None:
            raise serializers.ValidationError({'host': 'Invalid host list.'})

        return attrs