from django.db import models
from datetime import datetime
from constants.constants import Severity
from django.utils import timezone

# Create your models here.


class ErrorLog(models.Model):
    """
    ErrorLog model class
    """

    error = models.TextField()
    traceback = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    app_name = models.CharField(max_length=100, null=True, blank=True)
    severity = models.CharField(
        max_length=10, choices=Severity.choices(), default=Severity.ERROR.value
    )

    def __str__(self):
        return self.error
