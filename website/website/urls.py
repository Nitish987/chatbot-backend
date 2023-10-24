from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.index.urls')),
    path('account/', include('app.account.urls')),
]
