from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('chatbots/', views.ChatbotsView.as_view(), name='chatbots'),
    path('emforms/', views.EmFormsView.as_view(), name='emforms'),
    path('docs/', views.DocsView.as_view(), name='docs'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
]