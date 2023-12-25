from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from common.utils import generator



def _next_pricing_date():
    return timezone.now() + timedelta(days=30)

# Project Model
class Project(models.Model):
    id = models.CharField(default=generator.generate_identity, max_length=10, primary_key=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=50)
    description = models.CharField(default='', max_length=200)
    envtype = models.CharField(default='DEVELOPMENT', choices=(('DEVELOPMENT', 'Development'), ('PRODUCTION', 'Production')), max_length=20)
    host = models.JSONField(default=dict)
    next_pricing_date = models.DateTimeField(default=_next_pricing_date)
    price_to_pay = models.FloatField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def can_make_request(self) -> bool:
        return self.next_pricing_date > timezone.now()
    