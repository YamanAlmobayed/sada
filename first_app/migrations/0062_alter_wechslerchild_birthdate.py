# Generated by Django 4.0.6 on 2023-05-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0061_dyslexiaquestion_hint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechslerchild',
            name='birthdate',
            field=models.DateField(null=True),
        ),
    ]
