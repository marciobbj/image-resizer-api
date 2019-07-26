from io import BytesIO
from unittest import TestCase
from unittest.mock import patch

from django.core.files import File
from rest_framework.test import APITestCase


class ImageTestCase(APITestCase):

    """
    É importante mockar os testes pois isso
    isola o ambiente de testes do FileSystem
    de Django, se por ventura a aplicação
    utilizar um Bucket da Amazon ou algo do
    genero, os testes não irão interferir
    nesse ambiente.
    """
    @patch('apps.app_resizer.serializers.Image.save')
    @patch('apps.app_resizer.serializers.resize_job.delay')
    def test_users_can_upload_image(self, resize_job_mock, saving_mock):
        saving_mock.return_value = True
        img = File(file=BytesIO(b'ImageMock'), name='test.jpg')
        request_payload = {
            'file': img,
            'name': img.name,
            'width': 100,
            'height': 200
        }
        response = self.client.post('/images/', request_payload, follow=True)
        self.assertEqual(response.status_code, 201)
        saving_mock.assert_called_once()
        resize_job_mock.assert_called_once()

    def test_user_cannot_upload_not_image_files(self):
        img = File(file=BytesIO(b'ImageMock'), name='test.pdf')
        request_payload = {
            'file': img,
            'name': img.name,
            'width': 100,
            'height': 200
        }
        response = self.client.post('/images/', request_payload, follow=True)
        self.assertEqual(response.status_code, 400)
