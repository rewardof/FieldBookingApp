from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True

    objects = Manager()


class Country(BaseModel):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name


class Region(BaseModel):
    name = models.CharField(max_length=256)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        related_name="regions"
    )

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=256)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        related_name="districts"
    )

    def __str__(self):
        return self.name


class Address(BaseModel):
    address_line = models.CharField(max_length=256, blank=True)
    district = models.ForeignKey(
        District, on_delete=models.PROTECT,
        null=True, blank=True
    )
    zipcode = models.CharField(max_length=120, blank=True)
    longitude = models.FloatField(
        blank=True, null=True
    )
    latitude = models.FloatField(
        blank=True, null=True
    )
