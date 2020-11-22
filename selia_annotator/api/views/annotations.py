from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from irekua_collections.models import CollectionAnnotation
from selia_annotator.api.serializers.annotation import AnnotationSerializer
from selia_annotator.api.serializers.annotation import CreateAnnotationSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer
    queryset = Annotation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['item']
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateAnnotationSerializer

        return super().get_serializer_class()

    # def options(self, request, *args, **kwargs):
    #     meta = self.metadata_class()
    #     data = meta.determine_metadata(request, self)
    #     data.pop('description')
    #     return data
