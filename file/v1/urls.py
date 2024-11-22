from django.urls import path, include
from rest_framework import routers

from file.v1.views import FileViewSet

router = routers.SimpleRouter()
router.register('', FileViewSet, 'file')
app_name = 'file'

urlpatterns = [
    path('', include(router.urls))
]