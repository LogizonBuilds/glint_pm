"""
URL configuration for starter_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import (
    RootAPIView,
    UploadProfileImageAPIView,
    UpdateClientProfile,
    ChangePasswordAPIView,
    SettingsAPIView,
    ServicePaymentAPIView,
    FlutterWebhookAPIView,
)
from django.conf import settings
from django.conf.urls.static import static
from django_editorjs_fields import urls as editorjs_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RootAPIView.as_view(), name="root"),
    path(
        "users/profile/upload",
        UploadProfileImageAPIView.as_view(),
        name="upload-profile-pic",
    ),
    path("settings", SettingsAPIView.as_view(), name="settings"),
    path(
        "users/profile/change-password",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path("payments/webhook", FlutterWebhookAPIView.as_view(), name="webhook"),
    path("users/payments", ServicePaymentAPIView.as_view(), name="service-payment"),
    path("users/profile/update", UpdateClientProfile.as_view(), name="update-profile"),
    path("auth/", include("users.urls")),
    path("services/", include("services.urls")),
    path("testimonies/", include("testimonies.urls")),
    path("editorjs/", include(editorjs_urls)),
    path("portfolio/", include("portfolio.urls")),
    path("blogs/", include("blogs.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
