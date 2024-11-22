import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from base.models import BaseModel
from user.managers import UserManager
from utils.constants import (
    Languages,
    UserTypes,
    Gender, CodeType, AuthMethod, BookingStatus
)
from utils.validators import phone_number_validator


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    1. for customer, phone_number or email is required. Other fields are optional.
    2. for admin and field owner full_name, phone_number, email, password are required.
    """
    username = models.CharField(
        _("username"), max_length=512,
        unique=True,
        db_index=True,
    )
    full_name = models.CharField(
        _("full name"),
        max_length=150,
    )
    email = models.EmailField(
        _("email address"), max_length=128,
        blank=True, null=True
    )
    phone_number = models.CharField(
        _('phone number'),
        validators=[phone_number_validator()],
        max_length=17, null=True
    )
    language = models.CharField(
        verbose_name=_("preferred language"),
        choices=Languages.CHOICES,
        default=Languages.UZBEK,
        null=True,
    )
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    gender = models.CharField(
        _("gender"), max_length=16,
        choices=Gender.CHOICES,
        null=True
    )
    user_type = models.CharField(
        _("user type"),
        max_length=15,
        choices=UserTypes.CHOICES,
        default=UserTypes.CUSTOMER,
    )
    auth_method = models.CharField(
        _("auth method"),
        choices=AuthMethod.CHOICES,
        max_length=10, null=True
    )
    address = models.ForeignKey(
        'base.Address',
        verbose_name=_("address"),
        on_delete=models.SET_NULL,
        null=True
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions"
            " without explicitly assigning them."
        )
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user is verified.")
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        null=True,
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now
    )

    objects = UserManager()
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.full_name

    def verify(self):
        self.is_verified = True
        self.save(update_fields=['is_verified'])

    def get_pair_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def get_active_bookings(self):
        """
        Get all active bookings of the user
        """
        from bookings.models import Booking
        return Booking.objects.filter(user=self, status=BookingStatus.ACCEPTED)


class VerificationCode(BaseModel):
    """
    This model handles the verification process for actions such as registration and password reset.

    Workflow:
    1. User initiates an action requiring verification and receives a verification code.
    2. User submits the verification code to the backend for validation.
    3. Upon successful verification, user is verified
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()  # number which will be sent to the user
    code_type = models.CharField(
        max_length=20, choices=CodeType.CHOICES,
    )
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(
                seconds=int(settings.OTP_SETTINGS['OTP_EXPIRE_TIME'])
            )
        super().save(*args, **kwargs)

    @classmethod
    def create_code(cls, user: User, code_type: str):
        code = cls.generate_code()
        cls.objects.create(
            user=user, code=code,
            code_type=code_type
        )
        return code

    @classmethod
    def generate_code(cls):
        length = int(settings.OTP_SETTINGS['OTP_LENGTH'])
        return random.randint(10 ** (length - 1), 10 ** length - 1)

    @classmethod
    def send_code(cls, user: User, code_type: str):
        from utils.services import send_confirmation_sms

        if cls.already_sent_code(user, code_type):
            raise ValidationError("Confirmation code already sent, please use that one.")

        cls.delete_old_codes(user, code_type)

        code = cls.create_code(user=user, code_type=code_type)
        if user.auth_method == AuthMethod.EMAIL:
            if code_type == CodeType.REGISTER:
                raise NotImplementedError
            elif code_type == CodeType.FORGOT_PASSWORD:
                raise NotImplementedError
        elif user.auth_method == AuthMethod.PHONE:
            if code_type in [CodeType.REGISTER, CodeType.LOGIN]:
                send_confirmation_sms(user, code)
            elif code_type == CodeType.FORGOT_PASSWORD:
                raise NotImplementedError

    @classmethod
    def already_sent_code(cls, user: User, code_type: str):
        """
        Check if the user has already sent the code
        """
        verification_code = cls.objects.filter(user=user, code_type=code_type).last()
        if verification_code and not verification_code.is_expired():
            return True
        return False

    def is_expired(self):
        expired = self.expires_at < timezone.now()
        return expired

    @classmethod
    def check_code(cls, user: User, code: int, code_type: str) -> 'VerificationCode':
        verification_code: VerificationCode = cls.objects.filter(
            user=user, code=code, code_type=code_type
        ).last()
        if not verification_code:
            raise ValidationError({"code": _("Invalid code")})
        if verification_code.is_expired():
            raise ValidationError({"code": _("Code is expired")})

        # delete all other codes of this type
        cls.delete_old_codes(user, code_type)
        return verification_code

    @classmethod
    def delete_old_codes(cls, user: User, code_type: str, exclude_id=None):
        codes = cls.objects.filter(user=user, code_type=code_type)
        if exclude_id:
            codes = codes.exclude(id=exclude_id)

        codes.delete()
