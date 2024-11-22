from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.v1.views import (
    UserProfileAPIView,
    CustomTokenObtainPairView,
    SendOTPAPIView,
    VerifyOTPAPIView
)

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name="user-register-login"),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name="verify-otp"),

    path('me/', UserProfileAPIView.as_view(), name='me'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
