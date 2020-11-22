from rest_framework import serializers

from irekua_collections.models import CollectionAnnotation
from irekua_collections.models import CollectionAnnotationType
from irekua_collections.models import CollectionAnnotationTool
from selia_annotator.models import AnnotationToolComponent
from selia_annotator.api.serializers.users import UserSerializer
from selia_annotator.api.serializers.terms import TermSerializer
from selia_annotator.api.serializers.visualizers import VisualizerSerializer


class AnnotationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationType
        fields = [
            'id',
            'name',
            'description',
            'icon',
            'annotation_schema',
        ]


class AnnotationToolSerializer(serializers.ModelSerializer):
    annotation_type = AnnotationTypeSerializer(many=False, read_only=True)

    class Meta:
        model = AnnotationTool
        fields = [
            'id',
            'annotation_type',
            'name',
            'version',
            'logo',
            'website',
        ]


class AnnotationToolComponentSerializer(serializers.ModelSerializer):
    annotation_tool = AnnotationToolSerializer(read_only=True)

    class Meta:
        model = AnnotationToolComponent
        fields = [
            'id',
            'is_active',
            'annotation_tool',
            'javascript_file',
        ]


class AnnotationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    modified_by = UserSerializer(read_only=True)
    labels = TermSerializer(many=True, read_only=True)

    class Meta:
        model = Annotation
        fields = [
            'id',
            'item',
            'annotation_type',
            'event_type',
            'annotation',
            'labels',
            'annotation_tool',
            'visualizer',
            'visualizer_configuration',
            'certainty',
            'quality',
            'commentaries',
            'created_by',
            'created_on',
            'modified_by',
            'modified_on',
        ]


class CreateAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = [
            'item',
            'annotation_type',
            'event_type',
            'annotation',
            'labels',
            'annotation_tool',
            'visualizer',
            'visualizer_configuration',
            'certainty',
            'quality',
            'commentaries',
        ]
