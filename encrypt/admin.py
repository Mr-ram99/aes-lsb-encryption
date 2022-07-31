from django.contrib import admin

# Register your models here.
from .models import ImageModel, ImageModel2
admin.site.register(ImageModel)
admin.site.register(ImageModel2)