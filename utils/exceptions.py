from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class UserNotVerified(APIException):
    default_detail = _('User not verified')


class UserAlreadyExists(APIException):
    default_detail = _('User already exists')