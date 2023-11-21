from django.db import models


# chatbot model
class Chatbot(models.Model):
    api = models.OneToOneField("apis.Api", on_delete=models.CASCADE)
    type = models.CharField(default='', max_length=20)
    config = models.JSONField(default=dict)
    data = models.JSONField(default=dict)
