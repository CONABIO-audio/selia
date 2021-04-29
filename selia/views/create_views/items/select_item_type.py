from irekua_items.models import ItemType
from irekua_items.models import Licence
from irekua_collections.models import SamplingEvent
from irekua_collections.models import Collection
from irekua_collections.models import Deployment

from selia.views.create_views import SeliaSelectView
from irekua_permissions.items import (
    items as item_permissions)


class SelectItemTypeView(SeliaSelectView):
    template_name = 'selia/create/items/select_item_type.html'
    prefix = 'item_type'
    create_url = 'selia:create_item'

    def has_view_permission(self):
        user = self.request.user
        return item_permissions.create(user,
                collection=self.sampling_event.collection)

    def get_objects(self):
        if not hasattr(self, 'sampling_event'):
            self.sampling_event = SamplingEvent.objects.get(
                pk=self.request.GET['sampling_event'])
        if not hasattr(self, "collection"):
            self.collection = Collection.objects.get(
                pk=self.request.GET["collection"]
            )
        if not hasattr(self, "licence"):
            self.licence = Licence.objects.get(
                pk=self.request.GET["licence"]
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = self.sampling_event
        context['collection'] = self.sampling_event.collection
        context['licence'] = self.licence
        return context

    def get_list_context_data(self):
        return ItemType.objects.all()
