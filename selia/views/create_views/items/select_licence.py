from irekua_items.models import Licence
from irekua_collections.models import SamplingEvent
from irekua_collections.models import Collection
from irekua_collections.models import Deployment

from selia.views.create_views import SeliaSelectView
from irekua_permissions.items import (
    items as item_permissions)


class SelectItemLicenceView(SeliaSelectView):
    template_name = 'selia/create/items/select_licence.html'
    prefix = 'licence'
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['sampling_event'] = self.sampling_event
        context['collection'] = self.sampling_event.collection
        return context

    def get_list_context_data(self):
        return Licence.objects.all()
