import json

from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from irekua_items.models import Licence
from irekua_items.models import ItemType
from irekua_collections.models import Collection
from irekua_collections.models import CollectionSite
from irekua_collections.models import CollectionDevice
from irekua_collections.models import SamplingEvent
from irekua_collections.models import Deployment


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


class UploadAppView(TemplateView):
    template_name = "selia_uploader/upload.html"

    def dispatch(self, request, *args, **kwargs):
        self.arguments = self.extract_arguments(request)
        return super().dispatch(request, *args, **kwargs)

    def extract_arguments(self, request):
        return {
            "collection": _extract_argument_from_request(
                request,
                "collection",
                Collection,
                required=True,
            ),
            "licence": _extract_argument_from_request(
                request,
                "licence",
                Licence,
                required=True,
            ),
            "item_type": _extract_argument_from_request(
                request,
                "item_type",
                ItemType,
                required=True,
            ),
            "collection_site": _extract_argument_from_request(
                request,
                "collection_site",
                CollectionSite,
            ),
            "collection_device": _extract_argument_from_request(
                request,
                "collection_device",
                CollectionDevice,
            ),
            "sampling_event": _extract_argument_from_request(
                request,
                "sampling_event",
                SamplingEvent,
            ),
            "deployment": _extract_argument_from_request(
                request,
                "deployment",
                Deployment,
            ),
        }

    def get(self, request):
        items = {}
        for i in request.GET:
            if "deployment" in i:
                dep = Deployment.objects.get(id=request.GET[i])
                items["deployment"] = [dep.pk, dep.deployment_type.name]
                items["collection_metadata"] = dep.collection_metadata
                items["sampling_event"] = [
                    dep.sampling_event.pk,
                    dep.sampling_event.sampling_event_type.name,
                ]
                items["collection_site"] = [
                    dep.sampling_event.collection_site.pk,
                    dep.sampling_event.collection_site.collection_name,
                ]
                items["collection_device"] = [
                    dep.collection_device.pk,
                    dep.collection_device.collection_metadata["Nombres originales"],
                ]
                items["collection"] = [
                    dep.collection_device.collection.pk,
                    dep.collection_device.collection.name,
                ]
            elif "licence" in i:
                lic = Licence.objects.get(id=request.GET[i])
                items["licence"] = [lic.pk, lic.licence_type.name]
            elif "item_type" in i:
                mime = ItemType.objects.get(id=request.GET[i])
                items["item_type"] = [mime.pk, mime.name]
                items["mime_type"] = [
                    mime.mime_types.all()[0].pk,
                    mime.mime_types.all()[0].mime_type,
                ]
        return render(request, self.template_name, {"args": json.dumps(items)})