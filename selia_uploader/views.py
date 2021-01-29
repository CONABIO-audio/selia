import json
from django.views.generic import TemplateView
from django.shortcuts import render


class UploadAppView(TemplateView):
    template_name = "selia_uploader/upload.html"
    def get(self, request):
        return render(request, self.template_name, {"args": json.dumps(request.GET)})
