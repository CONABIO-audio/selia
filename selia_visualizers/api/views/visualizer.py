from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from rest_framework import pagination
from django_filters import rest_framework as filters


from irekua_visualizers import models
from selia_visualizers.api import serializers


class VisualizerFilter(filters.FilterSet):
    has_modules = filters.BooleanFilter(
        label=_('Has module'),
        help_text=_(
            'Indicates whether the visualizer has version with a '
            'javascript module.'),
        method='filter_has_modules')

    is_active = filters.BooleanFilter(
        label=_('Is active'),
        help_text=_(
            'Indicates whether the visualizer is used the default '
            'visualizer for some item type.'),
        method='filter_is_active')

    def filter_has_modules(self, queryset, name, value):
        queryset = queryset.annotate(
            modules=Count(
                'visualizerversion',
                filter=Q(visualizerversion__visualizermodule__isnull=False),
            )
        )

        if value:
            return queryset.filter(modules__gt=0)
        return queryset.filter(modules=0)

    def filter_is_active(self, queryset, name, value):
        queryset = queryset.annotate(
            active_item_types=Count(
                'visualizeritemtype',
                filter=Q(visualizeritemtype__is_active=True),
            )
        )

        if value:
            return queryset.filter(active_item_types__gt=0)
        return queryset.filter(active_item_types=0)

    class Meta:
        model = models.Visualizer
        fields = {
            'name': ['exact', 'icontains'],
            'item_types': ['exact'],
            'item_types__name': ['exact', 'icontains'],
        }


class VisualizerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Visualizer.objects.all()

    pagination_class = pagination.PageNumberPagination
    page_size = 2

    serializer_class = serializers.VisualizerSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisualizerFilter
