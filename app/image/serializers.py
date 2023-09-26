from rest_framework import serializers
from core.models import UploadedImage, ImageLink


class ImageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLink
        fields = ("id", "uploaded_image", "link", "expiration_time")
        read_only_fields = ("id", "uploaded_image", "expiration_time")


class UploadedImageSerializer(serializers.ModelSerializer):
    links = ImageLinkSerializer(many=True, read_only=True)

    class Meta:
        model = UploadedImage
        fields = ("id", "image", "upload_time", "links")
        read_only_fields = ("id", "upload_time", "links")
        extra_kwargs = {"image": {"required": {"required": True}}}
