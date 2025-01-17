from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from cloudinary.models import CloudinaryField

from django_editorjs_fields import EditorJsJSONField

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=500)
    body = RichTextField()
    date_created = models.DateField(default=timezone.now)
    author_name = models.CharField(max_length=200, null=True, blank=True)
    image = CloudinaryField("image")
    content = EditorJsJSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"
