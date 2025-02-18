from django.urls import path
from .views import GetAllServices, AllWhatWeDoAPIView


urlpatterns = [
    path("", GetAllServices.as_view(), name="all-services"),
    path("what-we-do", AllWhatWeDoAPIView.as_view(), name="what-we-do"),
]
