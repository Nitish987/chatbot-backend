from django.db import models
from common.platform.products import Product


# Apis Model
class Api(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    product = models.CharField(default='', choices=Product.products_model_choices(), max_length=20)
    type = models.CharField(default='', choices=Product.product_types_model_choices(), max_length=20)
    config_id = models.IntegerField(default=0)
    api_key = models.CharField(default='', max_length=256)
    hits_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.product + " | " + self.project.name + " - API"
