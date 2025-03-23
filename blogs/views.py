import httpx
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio
from .models import Post
from .serializers import PostSerializers
from asgiref.sync import sync_to_async
from sparky_utils.advice import exception_advice
from devs.models import ErrorLog

count = 0


class AsyncDispatchMixin:
    async def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        if asyncio.iscoroutinefunction(handler):
            return await handler(request, *args, **kwargs)
        return handler(request, *args, **kwargs)


class AsyncBlogView(AsyncDispatchMixin, APIView):
    async def get(self, request):
        blogs = blogs = await sync_to_async(list)(Post.objects.all())
        serializer = PostSerializers(blogs, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)


class BlogView(APIView):

    @exception_advice(model_object=ErrorLog)
    def get(self, request):
        latest = request.GET.get("query", None)
        if latest:
            blogs = Post.objects.all().order_by("-date_created")[:3]
            serializer = PostSerializers(blogs, many=True)
            print(f"Hit Count: {count}")
            return Response(serializer.data, status=200)
        else:
            blogs = Post.objects.all()
            serializer = PostSerializers(blogs, many=True)
            print(f"Hit Count: {count}")
            return Response(serializer.data, status=200)


class RetrieveABlogPost(APIView):

    @exception_advice(model_object=ErrorLog)
    def get(self, request, id):
        blog = Post.objects.get(id=id)
        serializer = PostSerializers(blog)
        return Response(serializer.data, status=200)
