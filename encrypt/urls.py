from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.urls.conf import include
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home , name='home'),
    path('encrypt/', views.image_upload_view_encrypt, name="encrypt"),
    path('decrypt/', views.image_upload_view_decrypt, name="decrypt"),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
