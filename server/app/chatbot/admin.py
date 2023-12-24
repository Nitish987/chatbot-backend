from django.contrib import admin
from . import models

# chatbot admin panel
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('id', 'api', 'name', 'engine', 'model', 'created_on')

admin.site.register(models.Chatbot, ChatbotAdmin)