# Generated by Django 4.0.6 on 2023-05-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0032_alter_account_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('Parent', 'Parent'), ('Expert', 'Expert')], default='Parent', max_length=6),
        ),
    ]
