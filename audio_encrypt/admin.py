from django.contrib import admin

# Register your models here.
from .models import AudioModel, AudioModel2
admin.site.register(AudioModel)
admin.site.register(AudioModel2)