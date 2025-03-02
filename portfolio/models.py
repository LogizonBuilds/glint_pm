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


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField("image")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About Us"
        verbose_name = "About Us"
