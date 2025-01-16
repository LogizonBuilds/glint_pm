from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from .serializers import UserSignupSerializer, VerifyOTPSerializer
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


class ResendOTPAPIView(APIView):
    """Resends OTP"""

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post Handler to resend otp"""
        email: str = request.data.get("email")
        user: User = User.objects.get(email__iexact=email)
        first_name = user.first_name
        otp: str = generate_otp()
        # cache the otp
        cache.set(email, otp, 60 * 15)
        subject = "Email Verification"
        message = f"""
        Your OTP code is {otp},
        Expires in 15mins
        """
        send_email_verification_task.delay(subject, message, first_name, email)
        return service_response(
            status="success", message="OTP Resent Successfully", status_code=200
        )


class VerifyOTP(APIView):
    """Verify the otp sent to the user email"""

    serializer_class: VerifyOTPSerializer = VerifyOTPSerializer

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post Handler to handle verifing user email"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data.get("email")
        otp: str = serializer.validated_data.get("otp")
        # get otp from cache
        cached_otp: str = cache.get(email)
        print("This is the cached code: ", cached_otp)
        if not cached_otp:
            return service_response(
                status="error", message="OTP Expired!", status_code=400
            )
        if str(otp) != str(cached_otp):
            return service_response(
                status="error", message="Invalid OTP!", status_code=400
            )

        # get the user
        user: User = User.objects.get(email__iexact=email)
        user.email_verified = True
        user.save()
        return service_response(
            status="success", message="Email Successfully Verified!", status_code=200
        )
