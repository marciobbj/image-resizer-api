from __future__ import absolute_import, unicode_literals

import os

import cv2
from celery import Celery, shared_task

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image.settings')
app = Celery('image', broker='pyamqp://guest@rabbitmq//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@shared_task()
def resize_job(file_id: int, resize_to: dict) -> bool:
    from apps.app_resizer.models import Image
    from django.conf import settings
    from django.core.files import File

    height = resize_to['height']
    width = resize_to['width']
    image_object = Image.objects.get(id=int(file_id))

    # Read image and transform it to a np array
    img = cv2.imread(image_object.file.path)

    # Resize the image
    img_resized = cv2.resize(img, (width, height))

    # Save the output in the media folder
    out_file_path = os.path.join(settings.BASE_DIR, 'media', f'{image_object.name}-OUT.jpg')

    # Write the image file
    cv2.imwrite(out_file_path, img_resized)

    # Save it to the db
    image_object.resized_image = File(file=open(out_file_path, mode='rb'), name=f'{image_object.name}-OUT.jpg')
    image_object.job_done = True
    image_object.save()

    # Remove the file created and just
    # keep the "File" object.
    os.remove(out_file_path)

    return True
