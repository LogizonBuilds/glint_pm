from django.db import models
from sparky_utils.decorators import str_meta
from cloudinary.models import CloudinaryField

# Create your models here.


@str_meta
class Portfolio(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField("image")
    project_link = models.URLField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
