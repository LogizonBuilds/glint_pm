from django.urls import path
from .views import GetAllServices


urlpatterns = [
    path("", GetAllServices.as_view(), name="all-services"),
]
