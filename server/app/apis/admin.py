from django.contrib import admin
from . import models

# Api Admin Panel
class ApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'product', 'updated_on', 'created_on')

admin.site.register(models.Api, ApiAdmin)