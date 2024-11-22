from rest_framework import viewsets, status

from utils.paginations import DynamicPagination
from utils.response import SuccessResponse


class BaseModelViewSet(DynamicPagination, viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": status.HTTP_201_CREATED,
            "message": "Created successfully.",
            "data": serializer.data
        }
        return SuccessResponse(**data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return SuccessResponse(**{"data": self.get_paginated_data(serializer.data)})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": status.HTTP_200_OK,
            "message": "Updated successfully.",
            "data": serializer.data
        }
        return SuccessResponse(**data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        data = {
            "status": status.HTTP_200_OK,
            "message": "Retrieved successfully.",
            "data": serializer.data
        }
        return SuccessResponse(**data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "status": status.HTTP_200_OK,
            "message": "Updated successfully.",
            "data": serializer.data
        }
        return SuccessResponse(**data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        data = {
            "status": status.HTTP_200_OK,
            "message": "Deleted successfully.",
        }
        return SuccessResponse(**data)
