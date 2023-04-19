from django.db import models

# Create your models here
class ImageModel(models.Model):
    key = models.IntegerField()
    text = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title
    @classmethod
    def create(cls, key, text, image):
        newtable = cls(key = key, text=text, image=image)
        return newtable

class ImageModel2(models.Model):
    key = models.IntegerField()
    image = models.ImageField(upload_to='images')