from django.urls import path
from .views import fetch_data_from_api, AsyncBlogView, BlogView

urlpatterns = [
    path("async", fetch_data_from_api, name="async-view"),
    path("async/class", AsyncBlogView.as_view(), name="async-class-view"),
    path("sync/class", BlogView.as_view(), name="sync-class-view"),
]
