import json
from django.views.generic import TemplateView
from django.shortcuts import render

from irekua_items.models import ItemType, Licence, MimeType
from irekua_collections.models import *


class UploadAppView(TemplateView):
    template_name = "selia_uploader/upload.html"
    def get(self, request):
        items = {}
        for i in request.GET:
            if "deployment" in i:
                dep = Deployment.objects.get(id=request.GET[i])
                items["deployment"] = [dep.pk,dep.deployment_type.name]
                items["collection_metadata"] = dep.collection_metadata
                items["sampling_event"] = [dep.sampling_event.pk,dep.sampling_event.sampling_event_type.name]
                items["collection_site"] = [dep.sampling_event.collection_site.pk,dep.sampling_event.collection_site.collection_name]
                items["collection_device"] = [dep.collection_device.pk,dep.collection_device.collection_metadata["Nombres originales"]]
                items["collection"] = [dep.collection_device.collection.pk,dep.collection_device.collection.name]
            elif "licence" in i:
                lic = Licence.objects.get(id=request.GET[i])
                items["licence"] = [lic.pk,lic.licence_type.name]
            elif "item_type" in i:
                mime = ItemType.objects.get(id=request.GET[i])
                items["item_type"] = [mime.pk,mime.name]
                items["mime_type"] = [mime.mime_types.all()[0].pk,mime.mime_types.all()[0].mime_type]
        return render(request, self.template_name, {"args": json.dumps(items)})
