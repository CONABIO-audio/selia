from rest_framework import serializers

from irekua_collections.models import CollectionType
from irekua_collections.models import Collection
from selia_annotator.models import AnnotationToolComponent
from selia_annotator.api.serializers.event_type import EventTypeSerializer
from selia_annotator.api.serializers.annotation import AnnotationToolComponentSerializer


class CollectionTypeSerializer(serializers.ModelSerializer):
    event_types = EventTypeSerializer(many=True, read_only=True)
    annotation_tools = serializers.SerializerMethodField()

    class Meta:
        model = CollectionType
        fields = [
            'id',
            'name',
            'description',
            'restrict_annotation_types',
            'restrict_event_types',
            'annotation_tools',
            'event_types',
        ]

    def get_annotation_tools(self, obj):
        if obj.restrict_annotation_types:
            queryset = AnnotationToolComponent.objects.filter(
                is_active=True,
                annotation_tool__annotation_type__in=obj.annotation_types.all())
        else:
            queryset = AnnotationToolComponent.objects.filter(is_active=True)

        serializer = AnnotationToolComponentSerializer(
            queryset,
            many=True,
            read_only=True)
        return serializer.data


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            'id',
            'name',
            'collection_type',
        ]
