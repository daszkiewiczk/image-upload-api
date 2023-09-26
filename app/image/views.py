from .serializers import (
    UploadedImageSerializer,
    ImageLinkSerializer,
    ExpiringImageLinkSerializer,
)
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
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseForbidden, FileResponse
from django.conf import settings
from django.http import HttpResponseForbidden, FileResponse


def expiring_link_view(request, link_id):
    try:
        image_link = ImageLink.objects.get(id=link_id)
    except ImageLink.DoesNotExist:
        return HttpResponseForbidden("Invalid link")

    print(image_link.expiration_time - timezone.now())

    if image_link.expiration_time and timezone.now() > image_link.expiration_time:
        return HttpResponseForbidden("Link has expired")

    # Serve the image content directly
    response = FileResponse(image_link.uploaded_image.image)
    return response


def generate_expiring_link(image, expiration_seconds=60):
    expiration_date = timezone.now() + timedelta(seconds=expiration_seconds)
    image_link = ImageLink.objects.create(
        uploaded_image=image,
        link=reverse("expiring-link", args=[image.id]),
        expiration_time=expiration_date,
        type=ImageLink.LinkType.EXPIRING,
    )
    return image_link


def resize_image(image, height):
    img = Image.open(image)
    width = int((height / img.height) * img.width)
    img_resized = img.resize((width, height), Image.ANTIALIAS)

    img_byte_array = BytesIO()
    img_resized.save(img_byte_array, format="JPEG")
    return ContentFile(img_byte_array.getvalue())


class ImageView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadedImageSerializer

    def get(self, request):
        images = UploadedImage.objects.filter(user=request.user)
        serializer = UploadedImageSerializer(images, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            user_tier = request.user.tier
            print(user_tier.thumbnail_sizes.all())
            print(user_tier.name)

            if user_tier.original_link:
                ImageLink.objects.create(
                    uploaded_image=serializer.instance,
                    link=serializer.instance.image.url,
                    type=ImageLink.LinkType.ORIGINAL,
                )

            for size in user_tier.thumbnail_sizes.all():
                resized_image_content = resize_image(
                    serializer.instance.image, size.height
                )
                resized_image_name = (
                    f"{serializer.instance.image.name}_thumbnail_{size.height}.jpg"
                )
                path = default_storage.save(resized_image_name, resized_image_content)
                ImageLink.objects.create(
                    uploaded_image=serializer.instance,
                    link=default_storage.url(path),
                    type=ImageLink.LinkType.THUMBNAIL,
                )
            return response.Response(serializer.data, status=201)
        return response.Response(serializer.errors, status=400)


class CreateExpiringImageLinkView(generics.CreateAPIView):
    serializer_class = ExpiringImageLinkSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            uploaded_image = UploadedImage.objects.get(
                id=request.data.get("uploaded_image_id"),
                user=request.user,
            )
            expiration_time = int(request.data.get("expire_in"))
            if (
                expiration_time < settings.MIN_LINK_EXPIRATION_TIME
                or expiration_time > settings.MAX_LINK_EXPIRATION_TIME
            ):
                return response.Response(
                    {
                        f"detail": "Expiration time be between {MIN_LINK_EXPIRATION_TIME} and {MAX_LINK_EXPIRATION_TIME}"
                    },
                    status=400,
                )
            image_link = generate_expiring_link(uploaded_image, expiration_time)
        except UploadedImage.DoesNotExist:
            return response.Response({"detail": "Invalid image id"}, status=400)
        except ValueError:
            return response.Response({"detail": "Invalid expiration time"}, status=400)

        return response.Response(ImageLinkSerializer(image_link).data, status=201)
