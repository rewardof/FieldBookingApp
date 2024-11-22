from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from user.permissions import (
    IsAuthenticatedUserOrAdmin,
)
from user.v1.serializers import (
    UserSerializer,
    StaffUserSerializer, SendOTPSerializer, VerifyOTPSerializer
)
from utils.constants import UserTypes
from utils.response import SuccessResponse, FailResponse


class SendOTPAPIView(views.APIView):
    """
    Send OTP to user's phone or email
    """

    def post(self, request, *args, **kwargs):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(
            message=_("Confirmation code has been sent to your phone number")
        )


class VerifyOTPAPIView(views.APIView):
    """
    Verify OTP and authenticate user
    """

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        request.user = user
        data = {
            "message": _("User successfully logged in"),
            "data": {
                "token": user.get_pair_token(),
                "user": UserSerializer(user).data
            }
        }
        return SuccessResponse(**data)


class UserProfileAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedUserOrAdmin,)

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        """
        only full_name, address, longitude, latitude, language can be updated
        """
        user = self.get_object()
        user_serializer = self.get_serializer(user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return SuccessResponse(**{"data": user_serializer.data})


class CustomTokenObtainPairView(TokenObtainPairView):

    def get_serializer_class(self):
        return TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        only admin and field owner can login with password
        customers can login with confirmation code
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.user.user_type not in UserTypes.STAFFS:
            kwargs = {
                "code": "not_allowed",
                "message": _("You are not allowed to login"),
                'status': 403,
            }
            return FailResponse(**kwargs)

        serializer.is_valid(raise_exception=True)
        data = {
            "message": _("User successfully logged in"),
            "data": {
                "token": serializer.validated_data,
                "user": StaffUserSerializer(serializer.user).data
            }
        }
        return SuccessResponse(**data)
