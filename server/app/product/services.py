from .models import Product



class ProductService:
    '''Product Service for listing and parsing products'''

    @staticmethod
    def list_products():
        return [ProductService.to_json(p) for p in Product.objects.all()]

    @staticmethod
    def to_json(product: Product):
        return {
            'id': product.pk,
            'name': product.name,
            'createdon': product.created_on
        }