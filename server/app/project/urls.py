from django.urls import path
from . import views


urlpatterns = [
    path('v1/project/', views.UserProject.as_view(), name='project'),
]