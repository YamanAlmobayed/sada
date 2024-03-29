# Generated by Django 3.2 on 2023-05-09 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0024_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_expert',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_parent',
        ),
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Expert', 'Expert'), ('Parent', 'Parent')], default=None, max_length=10),
            preserve_default=False,
        ),
    ]
