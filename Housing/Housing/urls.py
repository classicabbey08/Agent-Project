from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import home view from your Main app
from Main.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    # Landing page (root URL)
    path('', home, name='home'),

    # Include all URLs from your Main app
    path('', include('Main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)