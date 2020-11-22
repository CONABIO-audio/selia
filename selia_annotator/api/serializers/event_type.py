from rest_framework import serializers

from irekua_database.models import EventType
from selia_annotator.api.serializers.terms import TermTypeSerializer
from selia_annotator.api.serializers.terms import TermSerializer


class EventTypeSerializer(serializers.ModelSerializer):
    term_types = TermTypeSerializer(many=True, read_only=True)
    should_imply = TermSerializer(many=True, read_only=True)

    class Meta:
        model = EventType
        fields = [
            'id',
            'name',
            'description',
            'icon',
            'term_types',
            'should_imply',
        ]
