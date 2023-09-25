from rest_framework import serializers
from core.models import UploadedImage


class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ("id", "image", "upload_time")
        # read_only_fields = ('id', 'upload_time')
