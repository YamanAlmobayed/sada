# Generated by Django 4.0.6 on 2023-04-18 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0008_alter_wechslerchild_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='wechslerchild',
            name='date',
            field=models.DateField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]