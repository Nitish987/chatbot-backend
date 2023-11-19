from django.urls import path
from . import views


urlpatterns = [
    path('v1/project-api/<str:project_id>/', views.UserProjectApi.as_view(), name='project-api'),
    path('v1/project-api/<str:project_id>/view/', views.UserProjectApiView.as_view(), name='project-api-view'),
]