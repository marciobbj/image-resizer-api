# Generated by Django 2.2.3 on 2019-07-23 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_resizer', '0002_auto_20190723_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
