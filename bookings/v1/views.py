from django.db.models import Case, When, Value, IntegerField
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from base.v1.views import BaseModelViewSet
from bookings.models import Booking
from bookings.v1.serializers import BookingSerializer
from user.permissions import IsOwnerOrAdmin
from utils.constants import BookingStatus
from utils.response import SuccessResponse


class BookingViewSet(BaseModelViewSet):
    queryset = Booking.objects.all()
    filterset_fields = (
        'field', 'user',
        'status'
    )
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == ['list', 'change_status', 'destroy']:
            return [IsOwnerOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            raise NotImplementedError("Booking update is not allowed")
        return []

    def get_queryset(self):
        field_id = self.kwargs.get('field_pk')
        status_order = {
            BookingStatus.PENDING: 1,
            BookingStatus.ACCEPTED: 2,
            BookingStatus.COMPLETED: 3,
            BookingStatus.CANCELLED: 4,
            BookingStatus.REJECTED: 5
        }
        queryset = Booking.objects.filter(field_id=field_id)
        return queryset.order_by(
            Case(
                *[When(status=status, then=Value(priority)) for status, priority in status_order.items()],
                output_field=IntegerField()
            ),
            'start_time'
        )

    def list(self, request, *args, **kwargs):
        """
        to get list of bookings for a field owner
        """
        return super().list(request, *args, **kwargs)

    @action(
        detail=True, methods=['post'],
        url_path='change-status', url_name='change_status'
    )
    def change_status(self, request, *args, **kwargs):
        """
        to change the status of a booking
        - rejecting a booking
        - accepting a booking
        - cancelling a booking
        reject or cancelling booking may be considered as booking deletion
        """
        from bookings.services import BookingService

        booking = self.get_object()
        BookingService().change_booking_status(booking, request.data.get('status'))
        data = {
            "status": status.HTTP_200_OK,
            "message": "Booking status changed",
            "data": BookingSerializer(booking).data
        }
        return SuccessResponse(**data)