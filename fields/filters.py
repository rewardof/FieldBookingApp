from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from fields.models import FootballField


class FieldsOrdering(OrderingFilter):
    """
    Custom ordering filter for fields.

    This filter enables custom ordering of querysets based on specific fields,
    primarily `distance` and `name`. It retrieves the ordering criteria from the
    request's query parameters and applies the ordering accordingly.

    Example Query:
        - `?ordering=distance` (Ascending by distance)
        - `?ordering=-distance` (Descending by distance)
        - `?ordering=name` (Ascending by name)
        - `?ordering=-name` (Descending by name)
    """
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        return queryset.order_by(*ordering) if ordering else queryset

    def get_ordering(self, request, queryset, view):
        ordering = request.query_params.get(self.ordering_param, 'distance')
        if not ordering:
            return ('name',)
        asc = not ordering.startswith('-')
        order_by = ordering.lstrip('-')

        return (f"{'' if asc else '-'}{order_by}", 'name') if order_by in ['distance', 'name'] else (ordering,)


class FieldsFilter(filters.FilterSet):
    distance = filters.NumberFilter(method='filter_by_distance')
    district = filters.NumberFilter(field_name='address__district', lookup_expr='exact')

    class Meta:
        model = FootballField
        fields = (
            'district',
            'distance'
        )

    def filter_by_distance(self, queryset, name, value):
        return queryset.filter(distance__lte=value)

