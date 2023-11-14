from django.db import models

# Product Model
class Product(models.Model):
    name = models.CharField(default='', max_length=100)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
