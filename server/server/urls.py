from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    
    # WEB
    path('', include('app.index.urls')),

    # API
    path('api/account/', include('app.account.urls')),
]
