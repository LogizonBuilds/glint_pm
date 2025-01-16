from rest_framework.views import APIView
from sparky_utils.advice import exception_advice
from devs.models import ErrorLog
from .models import Testimony
from sparky_utils.response import service_response
from .serializers import TestimonySerializer


# Create your views here.


class TestimonyAPIView(APIView):
    """Testimony Apiview"""

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Submit Testimony Post handler"""
        serializer = TestimonySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return service_response(
            status="success",
            message="Testimony submitted successfully",
            status_code=201,
        )

    @exception_advice(model_object=ErrorLog)
    def get(self, request, *args, **kwargs):
        """Get handler for getting all visible testimonies"""
        testimonies = Testimony.objects.filter(show=True)
        serializer = TestimonySerializer(instance=testimonies, many=True)
        data = serializer.data
        return service_response(
            status="success",
            message="Testimonies fetched successfully",
            data=data,
            status_code=200,
        )
