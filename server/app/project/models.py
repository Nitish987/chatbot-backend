from django.db import models
from django.conf import settings
from common.utils import generator
from constants.products import Product


# Project Model
class Project(models.Model):
    id = models.CharField(default=generator.generate_identity, max_length=10, primary_key=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=50)
    description = models.CharField(default='', max_length=200)
    envtype = models.CharField(default='DEVELOPMENT', choices=(('DEVELOPMENT', 'Development'), ('PRODUCTION', 'Production')), max_length=20)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name



# Project Apis Model
class ProjectApi(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    product = models.CharField(default=Product.CHATBOT, choices=Product.products_model_choices(), max_length=20)
    api_key = models.CharField(default='', max_length=50)
    host = models.JSONField(default=dict)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.name + " | " + self.project.name + " - API"
    