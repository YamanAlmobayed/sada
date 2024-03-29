# Generated by Django 3.2 on 2023-04-17 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wechslerchild',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='wechslerchild',
            name='name',
        ),
        migrations.AddField(
            model_name='wechslerchild',
            name='child',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='Wechsler_test', to='first_app.childpersonalinfo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='childpersonalinfo',
            name='Lddrs_diagnose_listening_difficulties',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='childpersonalinfo',
            name='Lddrs_diagnose_writing_difficulties',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
