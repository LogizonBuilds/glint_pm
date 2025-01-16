from django.urls import path
from .views import SignupUserAPIView, ResendOTPAPIView, VerifyOTP


urlpatterns = [
    path("register", SignupUserAPIView.as_view(), name="register"),
    path("resend-otp", ResendOTPAPIView.as_view(), name="resend-otp"),
    path("verify-otp", VerifyOTP.as_view(), name="verify-otp"),
]
