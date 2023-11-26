from django.urls import path
from . import views


urlpatterns = [
    path('v1/import/project/', views.ExternalExport.as_view(), name='external-export-project'),
]
