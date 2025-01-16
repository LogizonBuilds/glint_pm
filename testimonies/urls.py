from django.urls import path
from .views import TestimonyAPIView


urlpatterns = [
    path("", TestimonyAPIView.as_view(), name="submit-testimony"),
]
