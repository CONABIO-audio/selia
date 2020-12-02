from django.views.generic import TemplateView


class UploadAppView(TemplateView):
    template_name = "selia_uploader/upload.html"
