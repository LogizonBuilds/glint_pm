import httpx
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio
from .models import Post
from .serializers import PostSerializers
from asgiref.sync import sync_to_async

count = 0


class AsyncDispatchMixin:
    async def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(),
                          self.http_method_not_allowed)
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
    def get(self, request):
        global count
        count += 1
        blogs = Post.objects.all()
        serializer = PostSerializers(blogs, many=True)
        print(f"Hit Count: {count}")
        return Response(serializer.data, status=200)
