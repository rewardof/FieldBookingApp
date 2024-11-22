from django.apps import apps
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

from utils.constants import UserTypes


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsAuthenticatedUserOrAdmin(BasePermission):
    required_groups = [UserTypes.ADMIN, UserTypes.CUSTOMER]

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        if self.required_groups is None:
            return False
        return obj == request.user or has_group_permission


class IsStaffUser(BasePermission):
    """
    Allows access only to staff users
    """
    required_groups = [UserTypes.ADMIN]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsCustomer(BasePermission):
    required_groups = [UserTypes.CUSTOMER]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsOwnerOrAdmin(BasePermission):
    required_groups = [UserTypes.ADMIN, UserTypes.FIELD_OWNER]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


def create_groups():
    Group = apps.get_model('auth', 'Group')
    groups = UserTypes.LIST
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
