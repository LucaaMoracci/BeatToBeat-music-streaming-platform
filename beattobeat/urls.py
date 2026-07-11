from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('music/', include('music.urls')),
]

# Serviamo i file media (audio dei brani) anche in produzione, così il player
# funziona sul sito deployato; WhiteNoise gestisce solo i file statici.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
