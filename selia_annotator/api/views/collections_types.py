from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from irekua_collections.models import CollectionType
from selia_annotator.api.serializers.data_collection import CollectionTypeSerializer


class CollectionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CollectionTypeSerializer
    queryset = CollectionType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    pagination_class = None
