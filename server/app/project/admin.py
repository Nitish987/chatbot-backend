from django.contrib import admin
from . import models


# Project Admin Panel
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'envtype', 'updated_on', 'created_on')

admin.site.register(models.Project, ProjectAdmin)
