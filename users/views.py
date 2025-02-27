from django.shortcuts import render
from rest_framework.views import APIView
from sparky_utils.response import service_response
from sparky_utils.advice import exception_advice
from .serializers import (
    SettingsSerializer,
    UserSignupSerializer,
    VerifyOTPSerializer,
    UserDetailsSerializers,
    ChangePasswordUnAuthenticatedSerializer,
    LoginSerializer,
    UpdateUserSerializer,
)
from devs.models import ErrorLog
from django.core.cache import cache
from utils.utils import generate_otp, generate_ref, upload_to_cloudinary, FlutterSDK
from .models import User, Setting
from .tasks import send_email_verification_task
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from typing import Union
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ChangePasswordAuthenticatedSerializer

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
        # TODO Update the send_email_verification_task to accept dynamic template name
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


class SocialAuth(APIView):
    """Social Auth View"""

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """
        Post Handler to handle social auth login and register
        """
        data = request.data
        user, created = User.objects.get_or_create(**data)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        refresh_token = str(tokens)
        user_data = {
            "name": user.first_name,
            "email": user.email,
            "profile_pic": user.profile_pic,
        }
        token_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": tokens.access_token.lifetime.total_seconds(),
            "user": user_data,
        }
        user.last_login = datetime.now()
        user.email_verified = True
        user.save()
        return service_response(
            status="success",
            message="Login Successful",
            data=token_data,
            status_code=200,
        )


class UserDetailsAPIView(APIView):
    """Get User's details"""

    permission_classes = [IsAuthenticated]

    @exception_advice(model_object=ErrorLog)
    def get(self, request, *args, **kwargs):
        """HTTP Get handler that returns users details"""
        user = request.user
        # serialize the user instance
        serializer = UserDetailsSerializers(instance=user)
        data = serializer.data
        return service_response(
            status="success",
            message="User details successfully fetched!",
            data=data,
            status_code=200,
        )


class PasswordResetView(APIView):
    """Sends Reset password token to a user"""

    @exception_advice(model_object=ErrorLog)
    def get(self, request, *args, **kwargs):
        email: Union[str, None] = request.GET.get("email")
        if not email:
            return service_response(
                status="error", message="Email is required", status_code=400
            )

        user: User = User.objects.get(email__iexact=email)
        otp: str = generate_otp()
        # cache otp
        cache.set(email, otp, 60 * 15)
        first_name = user.first_name
        subject = "Password Reset Token"
        message = f"""
        Your Password reset token is {otp}
        """
        send_email_verification_task.delay(subject, message, first_name, email)
        return service_response(
            status="success", message="OTP sent successfully", status_code=200
        )


class ChangePasswordAPIViewNOAuth(APIView):
    """Changes User password with reset token"""

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post Handler that handles changing of password - Unauthenticated"""

        serializer = ChangePasswordUnAuthenticatedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")
        password = serializer.validated_data.get("password1")
        # get opt from cache
        cached_otp = cache.get(email)
        if not cached_otp:
            return service_response(
                status="error", message="OTP Expired", status_code=400
            )
        if str(cached_otp) != str(otp):
            return service_response(
                status="error", message="Invalid OTP", status_code=400
            )
        user = User.objects.get(email__iexact=email)
        user.set_password(password)
        user.save()
        return service_response(
            status="success", message="Password Changed Successfully", status_code=200
        )


class LoginAPIView(APIView):
    """Logs client in"""

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post Handler to handle login"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        refresh_token = str(tokens)
        user_data = {
            "name": user.first_name,
            "email": user.email,
            "profile_pic": user.profile_pic,
        }

        token_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": tokens.access_token.lifetime.total_seconds(),
            "user": user_data,
        }
        user.last_login = datetime.now()
        user.save()

        return service_response(
            status="success",
            message="Login Successful",
            data=token_data,
            status_code=200,
        )


class UploadProfileImageAPIView(APIView):
    """API View that handles client profile image upload"""

    parser_classes = (MultiPartParser, FormParser)

    permission_classes = [IsAuthenticated]

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post handler"""
        profile_image = request.FILES.get("profile_image")
        profile_url = upload_to_cloudinary(profile_image, "profile_pics")
        user = request.user
        # set user profile image
        user.profile_pic = profile_url
        user.save()

        data = {"profile_pic": profile_url}
        return service_response(
            status="success",
            message="Image Uploaded Successfully",
            data=data,
            status_code=200,
        )


class UpdateClientProfile(APIView):
    """Update client APIView"""

    permission_classes = [IsAuthenticated]

    @exception_advice(model_object=ErrorLog)
    def patch(self, request, *args, **kwargs):
        """Handles update for user profile"""
        _id = request.user.id
        user = User.objects.get(id=_id)
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_data = serializer.validated_data
        print("This is the update data: ", update_data)
        for k, v in update_data.items():
            setattr(user, k, v)
        user.save()
        return service_response(
            status="success", message="Profile Updated Successfully", status_code=200
        )


class ChangePasswordAPIView(APIView):
    """Changes User Password Authenticated"""

    permission_classes = [IsAuthenticated]

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post Handler that handles changing of password - Authenticated"""

        serializer = ChangePasswordAuthenticatedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data.get("old_password")
        password1 = serializer.validated_data.get("new_password")

        if not user.check_password(old_password):
            return service_response(
                status="error", message="Old Password is incorrect", status_code=400
            )
        user.set_password(password1)
        user.save()
        return service_response(
            status="success", message="Password Changed Successfully", status_code=200
        )


class SettingsAPIView(APIView):

    @exception_advice(model_object=ErrorLog)
    def get(self, request):
        #  get settings object instance
        settings = Setting.objects.first()
        # serialize the settings instance
        serializer = SettingsSerializer(instance=settings)
        return service_response(
            status="success",
            data=serializer.data,
            message="Settings Fetched Successfully",
            status_code=200,
        )


class ServicePaymentAPIView(APIView):
    """Service Payment API View"""

    permission_classes = [IsAuthenticated]

    @exception_advice(model_object=ErrorLog)
    def post(self, request, *args, **kwargs):
        """Post Handler"""
        # get amount from request
        amount = request.data.get("amount")
        if not amount:
            return service_response(
                status="error", message="Amount is required", status_code=400
            )
        # get currency
        # currency = request.data.get("currency", "NGN")
        user: User = request.user
        # get user details
        customer_email = user.email
        customer_name = user.full_name
        customer_phone = user.whatsapp_number
        # create flutter sdk instance
        flutter = FlutterSDK(
            amount=amount,
            customer_email=customer_email,
            customer_name=customer_name,
            customer_phone=customer_phone,
        )
        # generate checkout url
        checkout_url = flutter.generate_checkout_url()
        return service_response(
            status="success",
            message="Checkout URL Generated Successfully",
            data={"checkout_url": checkout_url},
            status_code=200,
        )
