from os import stat
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('yotech/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('account/', include('account.urls', namespace='account')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
