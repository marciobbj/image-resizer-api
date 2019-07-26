from django.db import models

# Create your models here.

class Image(models.Model):

    name = models.CharField(max_length=255)
    file = models.FileField()
    width = models.IntegerField()
    height = models.IntegerField()
    job_done = models.BooleanField(default=False)
    resized_image = models.FileField(null=True)

    def __str__(self):
        return self.file.name

