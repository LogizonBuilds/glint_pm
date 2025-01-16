from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
import logging
import traceback
from django.db import transaction
from phonenumber_field.modelfields import PhoneNumberField


logger = logging.getLogger(__name__)


# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, email: str, password: str, **extra_fields: any):
        """Create new user method"""
        #    check for email present
        if not email:
            raise ValueError("User must have an email")
        # validate email
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError({"email": _("Please enter a valid email.")})

        # start a singe unit operation
        with transaction.atomic():
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model class
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(
        verbose_name=_("First name"), max_length=30, null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name=_("Last name"), max_length=30, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_pic = models.URLField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    whatsapp_number = PhoneNumberField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"], name="user_email_idx"),
        ]
        verbose_name = _("Client")
        verbose_name = _("Clients")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.save()
