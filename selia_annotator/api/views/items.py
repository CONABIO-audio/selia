from django.db.models import Q
from rest_framework import viewsets

from irekua_collections.models import DeploymentItem
from selia_annotator.api.serializers.item import ItemSerializer


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        user = self.request.user

        is_open = (
            Q(licence__licence_type__can_view=True) |
            Q(licence__is_active=False)
        )

        if not user.is_authenticated:
            return Item.objects.filter(is_open)

        if user.is_special:
            return Item.objects.all()

        is_own = Q(created_by=user)

        collections_with_permissions = user.collections_with_permissions('view_collection_annotations').only('id')
        managed_collections = user.managed_collections.only('id')
        admin_collections = user.admin_collections.only('id')

        collection_queryset = collections_with_permissions.union(
            managed_collections,
            admin_collections)
        is_in_allowed_collection = Q(
            sampling_event_device__sampling_event__collection__in=collection_queryset)

        return Item.objects.filter(
            is_open
            | is_own
            | is_in_allowed_collection
        ).select_related(
            'sampling_event_device',
            'sampling_event_device__sampling_event',
            'sampling_event_device__sampling_event__collection').distinct()
