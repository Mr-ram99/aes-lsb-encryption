from django.db import models

# Create your models here
class AudioModel(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    audio = models.FileField(upload_to='audios')

    def __str__(self):
        return self.title
    @classmethod
    def create(cls, title, text, audio):
        newtable = cls(title = title, text=text, audio=audio)
        return newtable

class AudioModel2(models.Model):
    audio = models.FileField(upload_to='audios')