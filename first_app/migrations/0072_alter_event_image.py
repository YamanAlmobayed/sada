# Generated by Django 3.2 on 2023-06-04 10:21

from django.db import migrations, models
import first_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0071_auto_20230604_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=first_app.models.upload_to),
        ),
    ]
