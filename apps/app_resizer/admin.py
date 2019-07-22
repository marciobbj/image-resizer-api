from django.contrib import admin

# Register your models here.
from apps.app_resizer.models import Image

admin.site.register(Image)