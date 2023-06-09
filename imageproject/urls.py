from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.urls.conf import include
from django.conf.urls.static import static
urlpatterns = [
    path('admin/',  admin.site.urls),
    path('', include('encrypt.urls'), name='index'),
    path('', include('audio_encrypt.urls'), name='index')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
