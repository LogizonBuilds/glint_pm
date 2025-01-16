from rest_framework.views import APIView
from sparky_utils.advice import exception_advice
from devs.models import ErrorLog
from .models import Service
from .serializers import ServiceSerializer
from sparky_utils.response import service_response


# Create your views here.


class GetAllServices(APIView):
    """Get All Available services"""

    @exception_advice(model_object=ErrorLog)
    def get(self, request, *args, **kwargs):
        """Get handler to handle getting all available services"""
        # get filter query
        filter_query = request.GET.get("service_type")
        # get all services
        services = Service.objects.all()
        if filter_query:
            services = services.filter(service_type=filter_query)
        # serialize the services
        serializer = ServiceSerializer(instance=services, many=True)
        data = serializer.data
        return service_response(
            status="success",
            message="Services fetched successfully",
            data=data,
            status_code=200,
        )
