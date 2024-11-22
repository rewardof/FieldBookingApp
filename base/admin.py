from django.contrib import admin

from base.models import Country, Region, District, Address


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing countries.
    """
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)
    list_per_page = 25


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing regions.
    """
    list_display = ('id', 'name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)
    ordering = ('country', 'name')
    list_per_page = 25


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """
    Admin interface for managing districts.
    """
    list_display = ('id', 'name', 'region', 'get_country')
    search_fields = ('name', 'region__name', 'region__country__name')
    list_filter = ('region__country', 'region')
    ordering = ('region__country', 'region', 'name')
    list_per_page = 25

    def get_country(self, obj):
        """
        Displays the country of the related region in the list view.
        """
        return obj.region.country.name

    get_country.short_description = 'Country'
    get_country.admin_order_field = 'region__country__name'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Basic admin interface for managing addresses.
    """
    list_display = ('id', "address_line", "district", "zipcode", "longitude", "latitude")
    search_fields = ("address_line", "district__name", "zipcode")
    list_filter = ("district",)
