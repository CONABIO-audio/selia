from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets
from django_filters import rest_framework as filters

from irekua_collections.models import DeploymentItemType

from irekua_visualizers import models
from selia_visualizers.api import serializers


class VisualizerVersionFilter(filters.FilterSet):
    has_module = filters.BooleanFilter(
        label=_('Has module'),
        help_text=_('Indicates whether this version has a javascript module.'),
        field_name='visualizermodule',
        method='filter_has_module')

    is_active = filters.BooleanFilter(
        label=_('Is active'),
        help_text=_('Indicates whether this version is the default version.'),
        field_name='visualizermodule',
        method='filter_is_active')

    item_type = filters.ModelChoiceFilter(
        queryset=ItemType.objects.all(),
        label=_('Item type'),
        help_text=_('Get the versions of the default visualizer for this item type.'),
        field_name='itemtype',
        method='filter_item_type')

    def filter_has_module(self, queryset, name, value):
        return queryset.filter(visualizermodule__isnull=not value)

    def filter_is_active(self, queryset, name, value):
        return (
            queryset.filter(
                visualizermodule__isnull=False,
                visualizermodule__is_active=value))

    def filter_item_type(self, queryset, name, value):
        q = models.VisualizerItemType.objects.filter(
            item_type=value,
            is_active=True)
        return queryset.filter(visualizer__visualizeritemtype__in=q)

    class Meta:
        model = models.VisualizerVersion
        fields = {
            'visualizer': ['exact'],
            'visualizer__name': ['icontains'],
            'visualizer__item_types': ['exact'],
            'version': ['exact', 'lt', 'gt', 'lte', 'gte', 'icontains'],
        }


class VisualizerVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.VisualizerVersion.objects.all()
    serializer_class = serializers.VisualizerVersionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VisualizerVersionFilter
