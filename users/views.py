from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice

# Create your views here.


class RootAPIView(APIView):
    """Root API View"""

    def get(self, request, *args, **kwargs):
        """Get method"""
        return service_response(
            message="Welcome to Glint PM API",
            data={},
            status_code=200,
            status="success",
        )
