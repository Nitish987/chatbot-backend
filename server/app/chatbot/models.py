from django.db import models
from common.platform.products import Product


# chatbot model
class Chatbot(models.Model):
    api = models.OneToOneField("apis.Api", on_delete=models.CASCADE)
    type = models.CharField(default='', choices=Product.chatbot.types_model_choices, max_length=20)
    name = models.CharField(default='', max_length=20)
    photo = models.ImageField(upload_to='chatbot/photo', blank=True)
    greeting = models.CharField(default='Hello, how may I help you.', max_length=200)
    engine = models.CharField(default='', choices=Product.chatbot.engines_model_choices, max_length=20)
    model = models.CharField(default='', choices=Product.chatbot.models_model_choices, max_length=20)
    sys_prompt = models.CharField(default='', max_length=200)
    knowledge = models.TextField(default='')
    use_emform = models.BooleanField(default=False)
    when_emform = models.CharField(default='', max_length=200)
    emform = models.ForeignKey("emforms.Emform", null=True, on_delete=models.SET_NULL)
    config = models.JSONField(default=dict)
    data = models.JSONField(default=dict)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.api.product + " | " + self.api.project.name + " - Configuration"
