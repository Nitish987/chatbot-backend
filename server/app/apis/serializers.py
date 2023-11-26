from rest_framework import serializers
from .models import Api
from common.platform.products import Product



# Add Project Api Serializer
class AddApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = ['product', 'type']
    
    def validate(self, attrs):
        product = attrs.get('product')
        type = attrs.get('type')

        if product not in Product.products():
            raise serializers.ValidationError({'product': 'Invalid product specified.'})
        
        if type not in Product.product_types():
            raise serializers.ValidationError({'type': 'Invalid product type.'})
        
        if not Product.is_product_type_valid(product, type):
            raise serializers.ValidationError({'product': 'Invalid product or type specified.'})

        return attrs