from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.urls.conf import include
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home , name='home'),
    path('audio-encrypt/', views.audio_upload_view_encrypt, name="encrypt-audio"),
    path('audio-decrypt/', views.audio_upload_view_decrypt, name="decrypt-audio"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
