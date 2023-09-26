from .serializers import UploadedImageSerializer
from rest_framework import (
    # views,
    generics,
    response,
    authentication,
    permissions,
)
from core.models import UploadedImage


class UploadImageView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadedImageSerializer

    def post(self, request):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Process image based on user's account tier and return links
            # ... (resize logic using Pillow and generate links)
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
