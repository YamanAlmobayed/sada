# Generated by Django 3.2 on 2023-05-11 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0034_rename_age_childpersonalinfo_age_years'),
    ]

    operations = [
        migrations.RenameField(
            model_name='childpersonalinfo',
            old_name='age_years',
            new_name='age_in_years',
        ),
    ]