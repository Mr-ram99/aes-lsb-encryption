from django.db import models

# Create your models here
class AudioModel(models.Model):
    key = models.IntegerField()
    text = models.CharField(max_length=2000)
    audio = models.FileField(upload_to='audios')

    def __str__(self):
        return self.title
    @classmethod
    def create(cls, key, text, audio):
        newtable = cls(key = key, text=text, audio=audio)
        return newtable

class AudioModel2(models.Model):
    key = models.IntegerField()
    audio = models.FileField(upload_to='audios')