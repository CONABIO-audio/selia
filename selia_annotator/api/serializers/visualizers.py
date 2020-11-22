from rest_framework import serializers

from irekua_database.models import Visualizer
from selia_visualizers.models import VisualizerComponent
from selia_visualizers.models import VisualizerComponentItemType


class VisualizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualizer
        fields = [
            'id',
            'name',
            'version',
            'website',
            'configuration_schema',
        ]


class VisualizerComponentSerializer(serializers.ModelSerializer):
    visualizer = VisualizerSerializer(many=False, read_only=True)

    class Meta:
        model = VisualizerComponent
        fields = [
            'id',
            'visualizer',
            'javascript_file',
        ]


class VisualizerComponentItemTypeSerializer(serializers.ModelSerializer):
    visualizer_component = VisualizerComponentSerializer(many=False, read_only=True)

    class Meta:
        model = VisualizerComponentItemType
        fields = [
            'id',
            'is_active',
            'visualizer_component',
            'item_type',
        ]
