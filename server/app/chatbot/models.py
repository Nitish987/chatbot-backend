from django.db import models


# chatbot model
class Chatbot(models.Model):
    api = models.ForeignKey("apis.Api", on_delete=models.CASCADE)
    config = models.JSONField(default=dict)
    data = models.JSONField(default=dict)
