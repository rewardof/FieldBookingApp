from django.conf import settings
from rest_framework import serializers

from file.models import File


class FileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = (
            'id',
            'file',
            'url'
        )

    def get_url(self, obj):
        return f"{settings.API_HOST}{obj.file.url}"
