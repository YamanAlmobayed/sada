# Generated by Django 4.0.6 on 2023-05-25 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0048_alter_autismquestion_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='wechslerchild',
            name='age',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='autismquestion',
            name='answer',
            field=models.ManyToManyField(blank=True, to='first_app.autismanswer'),
        ),
    ]