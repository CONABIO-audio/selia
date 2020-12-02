from django.urls import path
from selia_uploader.views import UploadAppView


urlpatterns = [
    path("", UploadAppView.as_view(), name="upload_app"),
]
