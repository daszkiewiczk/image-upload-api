from django.urls import path, include

from .views import UploadImageView, ListUserImagesView

urlpatterns = [
    path("upload/", UploadImageView.as_view(), name="upload-image"),
    path("list/", ListUserImagesView.as_view(), name="list-images"),
]
