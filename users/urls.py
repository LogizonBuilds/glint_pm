from django.urls import path
from .views import SignupUserAPIView


urlpatterns = [
    path("register", SignupUserAPIView.as_view(), name="register"),
]
