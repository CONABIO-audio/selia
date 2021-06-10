from django.views.generic import TemplateView
from django.shortcuts import render

from irekua_items.models import ItemType, Licence, MimeType
from irekua_collections.models import *


class CollectionItemAnnotatorView(TemplateView):
    template_name = "selia_annotator/annotator.html"
    def get(self, request):
        return render(request, self.template_name)
      