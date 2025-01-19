from django.urls import path
from .views import AsyncBlogView, BlogView

urlpatterns = [
    path("", AsyncBlogView.as_view(), name=""),
    path("sync/class", BlogView.as_view(), name="sync-class-view"),
]
