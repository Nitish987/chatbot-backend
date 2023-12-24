from django.db import models
from common.platform.products import Product


# emform model
class Emform(models.Model):
    api = models.OneToOneField("apis.Api", on_delete=models.CASCADE)
    type = models.CharField(default='', choices=Product.chatbot.types_model_choices, max_length=20)
    name = models.CharField(default='', max_length=50)
    config = models.JSONField(default=list)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.api.product + " | " + self.api.project.name + " - Configuration"