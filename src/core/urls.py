from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
]

# SWAGGER SCHEMES
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.unregister(Group)
admin.site.site_header = 'Botly ADMIN'
admin.site.site_title = 'Botly'
admin.site.index_title = 'ADMIN'
