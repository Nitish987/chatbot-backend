from django.contrib import admin
from . import models

# emform admin panel
class EmformAdmin(admin.ModelAdmin):
    list_display = ('id', 'api', 'name', 'created_on')

admin.site.register(models.Emform, EmformAdmin)
