from django.urls import path
from .views import AsyncBlogView, BlogView, RetrieveABlogPost

urlpatterns = [
    path("", AsyncBlogView.as_view(), name=""),
    path("sync/class", BlogView.as_view(), name="sync-class-view"),
    path("<int:id>", RetrieveABlogPost.as_view(), name="retrieve-blog-post"),
]
