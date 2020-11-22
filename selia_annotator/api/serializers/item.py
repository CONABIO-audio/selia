from rest_framework import serializers

from irekua_collections.models import DeploymentItem
from irekua_items.models import Licence
from irekua_items.models import LicenceType
from irekua_collections.models import DeploymentItemType
from selia_visualizers.models import VisualizerComponentItemType

from selia_annotator.api.serializers.users import UserSerializer
from selia_annotator.api.serializers.data_collection import CollectionSerializer
from selia_annotator.api.serializers.event_type import EventTypeSerializer
from selia_annotator.api.serializers.visualizers import VisualizerComponentItemTypeSerializer


class LicenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenceType
        fields = [
            'id',
            'name',
            'can_view',
            'can_download',
            'can_annotate',
            'years_valid_for'
        ]


class LicenceSerializer(serializers.ModelSerializer):
    licence_type = LicenceTypeSerializer(many=False, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Licence
        fields = [
            'id',
            'is_active',
            'licence_type',
            'created_by',
            'created_on',
            'modified_by',
            'modified_on',
        ]



class ItemTypeSerializer(serializers.ModelSerializer):
    event_types = EventTypeSerializer(many=True, read_only=True)

    class Meta:
        model = ItemType
        fields = [
            'id',
            'name',
            'icon',
            'event_types'
        ]


class ItemSerializer(serializers.ModelSerializer):
    licence = LicenceSerializer(many=False, read_only=True)
    created_by = UserSerializer(read_only=True)
    modified_by = UserSerializer(read_only=True)
    item_type = ItemTypeSerializer(read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='value', read_only=True)
    collection = CollectionSerializer(
        many=False,
        read_only=True,
        source='sampling_event_device.sampling_event.collection')
    visualizer = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id',
            'item_type',
            'licence',
            'item_file',
            'media_info',
            'tags',
            'metadata',
            'captured_on',
            'ready_event_types',
            'collection',
            'created_by',
            'visualizer',
            'modified_by',
            'created_on',
            'modified_on',
        ]

    def get_visualizer(self, obj):
        try:
            visualizer = VisualizerComponentItemType.objects.get(
                is_active=True,
                item_type=obj.item_type)
            serializer = VisualizerComponentItemTypeSerializer(
                visualizer,
                read_only=True)
            return serializer.data
        except VisualizerComponentItemType.DoesNotExist:
            return {}
