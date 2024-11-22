from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_("Personal Info"), {
            "fields": ("full_name", "email", "phone_number", "gender", "date_of_birth", "language", "address"),
        }),
        (_("Authentication Info"), {
            "fields": ("username", "auth_method", "password"),
        }),
        (_("Roles and Permissions"), {
            "fields": ("user_type", "is_staff", "is_superuser", "is_active", "is_verified"),
        }),
        (_("Important Dates"), {
            "fields": ("date_joined",),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone_number", "password1", "password2"),
        }),
    )

    list_display = (
        "username", "full_name", "email", "phone_number", "user_type",
        "is_staff", "is_active", "is_verified", "date_joined"
    )
    list_filter = (
        "is_staff", "is_active", "is_verified", "user_type", "gender", "language",
    )
    search_fields = ("username", "full_name", "email", "phone_number")
    ordering = ("-date_joined",)
    filter_horizontal = ("groups", "user_permissions",)
    readonly_fields = ("date_joined",)