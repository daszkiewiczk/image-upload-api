from .serializers import UploadedImageSerializer
from rest_framework import (
    generics,
    response,
    authentication,
    permissions,
)
from django.core.files.base import ContentFile
from PIL import Image
from core.models import UploadedImage, ImageLink
from io import BytesIO
from django.core.files.storage import default_storage


def resize_image(image, height):
    img = Image.open(image)
    width = int((height / img.height) * img.width)
    img_resized = img.resize((width, height), Image.ANTIALIAS)

    img_byte_array = BytesIO()
    img_resized.save(img_byte_array, format="JPEG")
    return ContentFile(img_byte_array.getvalue())


class UploadImageView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadedImageSerializer

    def post(self, request):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            user_tier = request.user.tier
            print(user_tier.thumbnail_sizes.all())
            print(user_tier.name)

            for size in user_tier.thumbnail_sizes.all():
                resized_image_content = resize_image(
                    serializer.instance.image, size.height
                )
                resized_image_name = (
                    f"{serializer.instance.image.name}_thumbnail_{size.height}.jpg"
                )
                path = default_storage.save(resized_image_name, resized_image_content)
                ImageLink.objects.create(
                    uploaded_image=serializer.instance, link=default_storage.url(path)
                )

            return response.Response(serializer.data, status=201)
        return response.Response(serializer.errors, status=400)


class ListUserImagesView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadedImageSerializer

    def get(self, request):
        images = UploadedImage.objects.filter(user=request.user)
        serializer = UploadedImageSerializer(images, many=True)
        return response.Response(serializer.data)
