from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    
    # WEB
    path('', include('app.index.urls')),

    # API
    path('api/account/', include('app.account.urls')),
    path('api/project/', include('app.project.urls')),
    path('api/apis/', include('app.apis.urls')),
    path('api/chatbot/', include('app.chatbot.urls')),
    path('api/emforms/', include('app.emforms.urls')),
    path('api/external/', include('app.external.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)