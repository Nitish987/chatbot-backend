from django.db import models
from common.platform.products import Product


# Apis Model
class Api(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    product = models.CharField(default=Product.chatbot.name, choices=Product.products_model_choices(), max_length=20)
    type = models.CharField(default=Product.chatbot.types[0], choices=Product.product_types_model_choices(), max_length=20)
    api_key = models.CharField(default='', max_length=256)
    host = models.JSONField(default=dict)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product + " | " + self.project.name + " - API"
