from django.db import models

# Create your models here
class ImageModel(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title
    @classmethod
    def create(cls, title, text, image):
        newtable = cls(title = title, text=text, image=image)
        return newtable

class ImageModel2(models.Model):
    image = models.ImageField(upload_to='images')