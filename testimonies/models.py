from django.db import models
from django.utils import timezone


# Create your models here.


class Testimony(models.Model):
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, null=True, blank=True)
    testimony = models.TextField(null=True, blank=True)
    show = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} Testimony"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimony"
        verbose_name_plural = "Testimonies"
        db_table = "testimonies"
        indexes = [
            models.Index(fields=["show"], name="testimony_show_idx"),
        ]
