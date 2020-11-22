from rest_framework import serializers
from irekua_visualizers import models
from selia_visualizers.api.serializers import VisualizerSerializer



class VisualizerVersionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='selia_visualizers:visualizerversion-detail')

    javascript_file = serializers.SerializerMethodField()
    configuration_schema = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    visualizer = VisualizerSerializer(read_only=True, config=False)

    class Meta:
        model = models.VisualizerVersion
        fields = [
            'url',
            'id',
            'visualizer',
            'version',
            'configuration_schema',
            'javascript_file',
            'is_active'
        ]

    def get_is_active(self, obj):
        try:
            return obj.visualizermodule.is_active
        except:
            return None

    def get_configuration_schema(self, obj):
        if obj.configuration_schema:
            return obj.configuration_schema

        return obj.visualizer.configuration_schema

    def get_javascript_file(self, obj):
        try:
            return obj.visualizermodule.javascript_file.url
        except:
            return None
