# Generated by Django 3.2 on 2023-05-11 21:09

from django.db import migrations, models
import first_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0037_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to=first_app.models.upload_to),
        ),
    ]
