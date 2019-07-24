from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.app_resizer.models import Image
from apps.app_resizer.serializers import ImageSerializer


class ImageViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ImageSerializer
    parser_classes = MultiPartParser,

    def get_queryset(self):
        return Image.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)