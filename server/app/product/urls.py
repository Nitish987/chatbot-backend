from django.urls import path
from . import views


urlpatterns = [
    path('v1/products/', views.AppProduct.as_view(), name='products')
]