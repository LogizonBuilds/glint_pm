from django.urls import path
from .views import SignupUserAPIView, ResendOTPAPIView


urlpatterns = [
    path("register", SignupUserAPIView.as_view(), name="register"),
    path("resend-otp", ResendOTPAPIView.as_view(), name="resend-otp"),
]
