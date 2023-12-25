from django.urls import path
from . import views

urlpatterns = [
    path('v1/billings/', views.BillingDashboard.as_view(), name='billings'),
    path('v1/billing/<str:project_id>/', views.BillingDashboardByProject.as_view(), name='billing-by-project')
]
