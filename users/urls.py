from django.urls import path
from .views import (
    SignupUserAPIView,
    ResendOTPAPIView,
    VerifyOTP,
    SocialAuth,
    UserDetailsAPIView,
    PasswordResetView,
    ChangePasswordAPIViewNOAuth,
    LoginAPIView,
)


urlpatterns = [
    path("register", SignupUserAPIView.as_view(), name="register"),
    path("resend-otp", ResendOTPAPIView.as_view(), name="resend-otp"),
    path("verify-otp", VerifyOTP.as_view(), name="verify-otp"),
    path("social-login", SocialAuth.as_view(), name="social-login"),
    path("details", UserDetailsAPIView.as_view(), name="user-details"),
    path("reset-password", PasswordResetView.as_view(), name="reset-password"),
    path(
        "reset-password/change",
        ChangePasswordAPIViewNOAuth.as_view(),
        name="reset-password-change",
    ),
    path("login", LoginAPIView.as_view(), name="login"),
]
