from rest_framework import serializers

from apps.app_resizer.models import Image


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

    valid_file_types = ['png', 'jpeg', 'jpg']

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
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