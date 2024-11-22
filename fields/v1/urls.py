from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from fields.v1.views import FootballFieldViewSet
from bookings.v1.views import BookingViewSet

router = routers.SimpleRouter()
router.register('', FootballFieldViewSet, 'fields')
review_nested_router = NestedDefaultRouter(router, '', lookup='field')
review_nested_router.register('bookings', BookingViewSet, basename='field-booking')

app_name = 'fields'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_nested_router.urls)),
]