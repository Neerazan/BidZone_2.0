from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'BidZone Admin'
admin.site.index_title = 'Admin Panel'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auction/', include('auction.urls')),
    path('slider/', include('slider.urls')),
    path('core/', include('core.urls')),
    path('playground/', include('playground.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)