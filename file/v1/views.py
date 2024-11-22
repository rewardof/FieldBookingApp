from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from file.models import File
from file.v1.serializers import FileSerializer


class FileViewSet(ModelViewSet):
    permission_classes = (AllowAny, )
    serializer_class = FileSerializer
    queryset = File.objects.all()
