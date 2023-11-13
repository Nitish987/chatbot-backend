from django.contrib import admin
from . import models



# Product Admin Panel
class ProductAdminPanel(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_on')

admin.site.register(models.Product, ProductAdminPanel)