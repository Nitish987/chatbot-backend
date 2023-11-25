from django.db import models
from django.conf import settings
from common.utils import generator


# Project Model
class Project(models.Model):
    id = models.CharField(default=generator.generate_identity, max_length=10, primary_key=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=50)
    description = models.CharField(default='', max_length=200)
    envtype = models.CharField(default='DEVELOPMENT', choices=(('DEVELOPMENT', 'Development'), ('PRODUCTION', 'Production')), max_length=20)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name
    