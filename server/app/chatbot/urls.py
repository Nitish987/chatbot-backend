from django.urls import path
from . import views


urlpatterns = [
    path('v1/config/', views.ChatbotConfig.as_view(), name='chatbot-config'),
]