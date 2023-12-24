from django.urls import path
from . import views


urlpatterns = [
    path('v1/config/', views.EmformConfig.as_view(), name='emform-config'),
]