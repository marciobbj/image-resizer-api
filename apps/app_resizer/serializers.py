from rest_framework import serializers

from apps.app_resizer.models import Image
from image.celery import resize_job


class ImageSerializer(serializers.ModelSerializer):

    valid_file_types = ['png', 'jpeg', 'jpg']

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        resize_to = {
            'width': validated_data.get('width'),
            'height': validated_data.get('height')
        }
        image = Image.objects.create(**validated_data)

        resize_job.delay(file_id=image.id, resize_to=resize_to)
        return image

    def validate_file(self, file):
        valid_format = [
            acceptable_format in file.name
            for acceptable_format
            in self.valid_file_types
        ]
        if any(valid_format):
            return file
        raise serializers.ValidationError('Incompatible file format')