from django.db import models
from sparky_utils.decorators import str_meta
from constants.constants import ServiceType
from cloudinary.models import CloudinaryField
from django.utils import timezone


# Create your models here.


@str_meta
class Service(models.Model):
    name = models.CharField(max_length=300)
    service_type = models.CharField(
        max_length=200, choices=ServiceType.choices(), default=ServiceType.TECH.value
    )
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField("image")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


@str_meta
class WhatWeDo(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField("image")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
