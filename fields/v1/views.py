from django.db.models import F, Value, FloatField, Q
from django.db.models import QuerySet
from django.db.models.functions import Sqrt, Power, Radians, Sin, Cos, ATan2
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from base.v1.views import BaseModelViewSet
from bookings.models import Booking
from fields.filters import FieldsOrdering, FieldsFilter
from fields.models import FootballField
from fields.v1.serializers import FootballFieldSerializer, FootballFieldListSerializer, FootballDetailSerializer
from user.permissions import IsOwnerOrAdmin
from utils.constants import BookingStatus
from utils.response import SuccessResponse
from utils.tools import parse_datetime


class FootballFieldViewSet(BaseModelViewSet):
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        FieldsOrdering,
    )
    filterset_class = FieldsFilter
    search_fields = (
        'name', 'description',
        'address__address_line'
    )

    def get_serializer_class(self):
        if self.action in ['list', 'my_fields']:
            return FootballFieldListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FootballFieldSerializer
        elif self.action == 'retrieve':
            return FootballDetailSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        """
        Returns the permissions required for the current action.
        filters by:
         - distance
         - district
         - availability according to the time range
         orders by:
            - distance
            - name
        """
        if self.action == ['create', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'list':
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == 'my_fields':
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        Optionally filter fields by location, availability, and proximity
        """
        fields = FootballField.objects.active()
        fields = self._annotate_distance(fields)
        return fields.order_by('name')

    def filter_queryset(self, queryset):
        # Filter by date/time availability
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        if start_time and end_time:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)

            # Find fields with conflicting bookings
            booked_fields = Booking.objects.filter(
                Q(start_time__lt=end_time) &
                Q(end_time__gt=start_time) &
                Q(status__in=[BookingStatus.PENDING, BookingStatus.ACCEPTED])
            ).values_list('field_id', flat=True)

            # Exclude booked fields
            queryset = queryset.exclude(id__in=booked_fields)
        return super().filter_queryset(queryset)

    def _annotate_distance(self, fields: QuerySet):
        """
        Annotate fields with distance from a given location
        """
        # Sort by proximity if latitude and longitude provided
        latitude = float(self.request.query_params.get('latitude', 0))
        longitude = float(self.request.query_params.get('longitude', 0))
        # Radius of the Earth in kilometers
        R = 6371

        if not latitude and not longitude:
            # if user's location is not provided, return fields without distance annotation
            return fields.annotate(distance=Value(0, output_field=FloatField()))

        # Implementing the Haversine formula for distance calculation
        fields = fields.annotate(
            distance=R * 2 * ATan2(
                Sqrt(
                    Power(Sin((Radians(Value(latitude)) - Radians(F('address__latitude'))) / 2), 2,
                          output_field=FloatField()) +
                    Cos(Radians(Value(latitude))) * Cos(Radians(F('address__latitude'))) *
                    Power(Sin((Radians(Value(longitude)) - Radians(F('address__longitude'))) / 2), 2,
                          output_field=FloatField())
                ),
                Sqrt(
                    1 - (
                            Power(Sin((Radians(Value(latitude)) - Radians(F('address__latitude'))) / 2), 2,
                                  output_field=FloatField()) +
                            Cos(Radians(Value(latitude))) * Cos(Radians(F('address__latitude'))) *
                            Power(Sin((Radians(Value(longitude)) - Radians(F('address__longitude'))) / 2), 2,
                                  output_field=FloatField())
                    )
                )
            )
        )
        return fields

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_path='my-fields', url_name='my_fields')
    def my_fields(self, request, *args, **kwargs):
        """
        Retrieve fields owned by the authenticated user
        """
        queryset = self.filter_queryset(self.get_queryset().filter(owner=request.user))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return SuccessResponse(**{"data": self.get_paginated_data(serializer.data)})

