from rest_framework import serializers
from irekua_visualizers import models


class VisualizerItemTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VisualizerItemType
        fields = [
            'item_type',
            'is_active',
        ]


class VisualizerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='selia_visualizers:visualizer-detail')
    item_types = VisualizerItemTypesSerializer(
        many=True,
        read_only=True,
        source='visualizeritemtype_set')

    class Meta:
        model = models.Visualizer
        fields = [
            'url',
            'id',
            'name',
            'description',
            'website',
            'configuration_schema',
            'item_types',
        ]

    def __init__(self, *args, **kwargs):
        config = kwargs.pop('config', True)

        super().__init__(*args, **kwargs)

        if not config:
            self.fields.pop('configuration_schema')
