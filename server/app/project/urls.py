from django.urls import path
from . import views


urlpatterns = [
    path('v1/project/', views.UserProject.as_view(), name='project'),
    path('v1/project-api/', views.UserProjectApi.as_view(), name='project-api'),
]