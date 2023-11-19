from django.contrib import admin
from . import models

# Project Api Admin Panel
class ProjectApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'product', 'created_on')

admin.site.register(models.ProjectApi, ProjectApiAdmin)