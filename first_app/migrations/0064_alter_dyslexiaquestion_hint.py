# Generated by Django 3.2 on 2023-06-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0063_ravngroup_ravnquestion_ravnquestionimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dyslexiaquestion',
            name='hint',
            field=models.CharField(max_length=20),
        ),
    ]
