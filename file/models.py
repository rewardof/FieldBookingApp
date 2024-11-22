from django.db import models
from base.models import BaseModel
from django.core.files.storage import storages
from file import get_upload_path
from django.utils.translation import gettext_lazy as _


class File(BaseModel):
    file = models.FileField(
        upload_to=get_upload_path,
        storage=storages['default'],
        verbose_name=_('file')
    )
