from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from .serializers import UserSignupSerializer
from devs.models import ErrorLog
from django.core.cache import cache
from utils.utils import generate_otp
from .models import User
from .tasks import send_email_verification_task

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


class SignupUserAPIView(APIView):
    """Create user api view"""

    serializer_class: UserSignupSerializer = UserSignupSerializer

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post handler to create a new user"""
        serializer: UserSignupSerializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # save the user object
            user: User = serializer.save()
            first_name: str = user.first_name
            email: str = user.email
            # generate otp and for verification and cache
            otp: str = generate_otp()
            # cache the otp
            cache.set(email, otp, 60 * 15)
            # send verification mail asynchronously
            subject = "Email Verification"
            message = f"""
            Your OTP code is {otp},
            Expires in 15mins
            """
            send_email_verification_task.apply_async(
                args=[subject, message, first_name, email]
            )
            return service_response(
                status="success",
                message=f"Registration successful, an email verification as been sent {email}",
                status_code=201,
            )
        raise Exception
