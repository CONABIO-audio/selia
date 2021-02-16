from django.http import Http404
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Licence
from irekua_items.models import ItemType
from irekua_collections.models import Collection
from irekua_collections.models import CollectionSite
from irekua_collections.models import CollectionDevice
from irekua_collections.models import SamplingEvent
from irekua_collections.models import Deployment

from selia_templates.views.mixins import SeliaPermissionsMixin


def _extract_argument_from_request(request, name, Model, required=False):
    try:
        pk = request.GET[name]
        return Model.objects.get(pk=pk)

    except KeyError:
        if not required:
            return None

        raise Http404(f"No {name} was provided")

    except Model.DoesNotExist:
        raise Http404(f"{name.title()} does not exist")


class UploadAppView(SeliaPermissionsMixin, TemplateView):
    template_name = "selia_uploader/upload.html"

    def dispatch(self, request, *args, **kwargs):
        self.arguments = self.extract_arguments(request)
        return super().dispatch(request, *args, **kwargs)

    def extract_arguments(self, request):
        self.collection = _extract_argument_from_request(
            request,
            "collection",
            Collection,
            required=True,
        )
        self.licence = _extract_argument_from_request(
            request,
            "licence",
            Licence,
            required=True,
        )
        self.item_type = _extract_argument_from_request(
            request,
            "item_type",
            ItemType,
            required=True,
        )
        self.collection_site = _extract_argument_from_request(
            request,
            "collection_site",
            CollectionSite,
        )
        self.collection_device = _extract_argument_from_request(
            request,
            "collection_device",
            CollectionDevice,
        )
        self.sampling_event = _extract_argument_from_request(
            request,
            "sampling_event",
            SamplingEvent,
        )
        self.deployment = _extract_argument_from_request(
            request,
            "deployment",
            Deployment,
        )

    def has_view_permission(self):
        user = self.request.user

        if not user.is_authenticated:
            return False

        return self.collection.can_add_items(user)

    def get_context_data(self, **kwargs):
        items = {
            "collection": [self.collection.pk, str(self.collection)],
            "collection_metadata": self.collection.metadata,
            "item_type": [self.item_type.pk, str(self.item_type)],
            "licence": [self.licence.pk, str(self.licence.licence_type)],
            "mime_types": [
                [mime_type.pk, str(mime_type)]
                for mime_type in self.item_type.mime_types.all()
            ],
        }

        if self.collection_site is not None:
            items["collection_site"] = [
                self.collection_site.pk,
                str(self.collection_site),
            ]

        if self.collection_device is not None:
            items["collection_device"] = [
                self.collection_device.pk,
                str(self.collection_device),
            ]

        if self.sampling_event is not None:
            items["sampling_event"] = [
                self.sampling_event.pk,
                str(self.sampling_event),
            ]

        if self.deployment is not None:
            items["deployment"] = [
                self.deployment.pk,
                str(self.deployment),
            ]

        return {**super().get_context_data(**kwargs), "args": items}