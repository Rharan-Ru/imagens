from django.db import models

# Create your models here.


class ImagensModel(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='all_images/', blank=True)
