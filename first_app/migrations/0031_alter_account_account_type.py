# Generated by Django 4.0.6 on 2023-05-10 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0030_alter_childpersonalinfo_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(blank=True, choices=[('Expert', 'Expert'), ('Parent', 'Parent')], default='Expert', max_length=10, null=True),
        ),
    ]
