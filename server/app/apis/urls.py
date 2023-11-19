from django.urls import path
from . import views


urlpatterns = [
    path('v1/project-api/<str:project_id>/', views.ProjectApi.as_view(), name='project-api'),
    path('v1/project-api/<str:project_id>/view/', views.ProjectApiView.as_view(), name='project-api-view'),
]