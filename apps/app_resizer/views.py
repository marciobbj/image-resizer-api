from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from apps.app_resizer.models import Image
from apps.app_resizer.serializers import ImageSerializer


class ImageViewSet(viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    parser_classes = FileUploadParser

    def get_queryset(self):
        return Image.objects.all()

    @action(detail=True, methods=['POST'])
    def create_job(self, request, *args, **kwargs):
        file = request.data.get('file')
        return Response(status=status.HTTP_201_CREATED)
