from django.contrib import admin
from . import models


# Project Admin Panel
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'envtype', 'created_on')

admin.site.register(models.Project, ProjectAdmin)


# Project Api Admin Panel
class ProjectApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'product', 'created_on')

admin.site.register(models.ProjectApi, ProjectApiAdmin)
