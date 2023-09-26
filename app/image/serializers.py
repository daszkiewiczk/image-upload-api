from rest_framework import serializers
from core.models import UploadedImage, ImageLink


class ImageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageLink
        fields = ("link", "type")
        read_only_fields = ("link", "type")


class ExpiringImageLinkSerializer(ImageLinkSerializer):
    uploaded_image_id = serializers.IntegerField(write_only=True)
    expire_in = serializers.IntegerField(write_only=True)

    class Meta(ImageLinkSerializer.Meta):
        model = ImageLink
        fields = ImageLinkSerializer.Meta.fields + ("expire_in", "uploaded_image_id")


class UploadedImageSerializer(serializers.ModelSerializer):
    links = ImageLinkSerializer(many=True, read_only=True)

    class Meta:
        model = UploadedImage
        fields = (
            "id",
            "image",
            "links",
        )
        read_only_fields = ("links", "id")
        extra_kwargs = {"image": {"write_only": True}}
