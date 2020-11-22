from rest_framework import serializers
from irekua_database.models import Term
from irekua_database.models import TermType



class TermTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermType
        fields = [
            'id',
            'name',
            'description',
            'icon',
            'is_categorical',
        ]


class TermSerializer(serializers.ModelSerializer):
    term_type_name = serializers.SlugRelatedField(
        slug_field='name',
        source='term_type',
        read_only=True)

    class Meta:
        model = Term
        fields = [
            'id',
            'value',
            'term_type',
            'term_type_name',
        ]
