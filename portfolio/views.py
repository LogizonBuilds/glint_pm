from rest_framework.views import APIView
from .models import Portfolio, AboutUs
from .serializers import PortfolioSerializer, AboutUsSerializer
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from devs.models import ErrorLog


# Create your views here.


class PortfolioAPIView(APIView):
    """Portfolio List APIView"""

    @exception_advice(model_object=ErrorLog)
    def get(self, request, *args, **kwargs):
        """Get Handler for Portfolio"""
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return service_response(
            status="success",
            message="Portfolios fetched successfully",
            data=serializer.data,
            status_code=200,
        )


class AboutUsAPIView(APIView):

    @exception_advice(model_object=ErrorLog)
    def get(self, request, *args, **kwargs):
        """Get handler for about us list lage"""
        all_aboutus = AboutUs.objects.all()[:3]
        serializer = AboutUsSerializer(all_aboutus, many=True)
        return service_response(
            status="success",
            message="About us fetched successfully",
            data=serializer.data,
            status_code=200,
        )
