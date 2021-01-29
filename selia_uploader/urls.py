from django.urls import path, re_path
from selia_uploader.views import UploadAppView


urlpatterns = [
    re_path(r"^$", UploadAppView.as_view(), name="upload_app"),
]
