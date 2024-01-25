# Generated by Django 3.2 on 2023-04-17 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChildInfoBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ChildPersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('birthdate', models.DateField()),
                ('age', models.IntegerField(editable=False)),
                ('child_class', models.CharField(max_length=20)),
                ('current_school', models.CharField(max_length=70)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=20)),
                ('transferring_party', models.CharField(blank=True, max_length=50, null=True)),
                ('supervised_doctor', models.CharField(blank=True, max_length=50, null=True)),
                ('father_name', models.CharField(max_length=50)),
                ('mother_name', models.CharField(max_length=50)),
                ('father_education', models.TextField()),
                ('mother_education', models.TextField()),
                ('father_work', models.TextField()),
                ('mother_work', models.TextField()),
                ('Lddrs_diagnose_writing_difficulties', models.CharField(max_length=50, null=True)),
                ('Lddrs_diagnose_listening_difficulties', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'الاختبارات العامة',
            },
        ),
        migrations.CreateModel(
            name='LddrsTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('option', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ParentsBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_range', models.CharField(max_length=50)),
                ('age', models.IntegerField(editable=False)),
            ],
            options={
                'ordering': ['-age'],
            },
        ),
        migrations.CreateModel(
            name='PortageBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basal_age', models.IntegerField()),
            ],
            options={
                'ordering': ['-basal_age'],
            },
        ),
        migrations.CreateModel(
            name='WechslerChild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('gender', models.TextField()),
                ('age', models.CharField(choices=[('7-4/7-7', '7-4/7-7'), ('5-1/5-5', '5-2/5-5')], max_length=20)),
                ('address', models.TextField()),
                ('father_name', models.TextField()),
                ('vrebal_scal', models.IntegerField(default=0)),
                ('practical_scale', models.IntegerField(default=0)),
                ('IQ', models.IntegerField(default=0)),
                ('diagnose', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WechslerScaledScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.TextField()),
                ('scaled_score', models.IntegerField()),
                ('info_test', models.IntegerField(blank=True, null=True)),
                ('compare_test', models.IntegerField(blank=True, null=True)),
                ('math_test', models.IntegerField(blank=True, null=True)),
                ('similarity_test', models.IntegerField(blank=True, null=True)),
                ('understanding_test', models.IntegerField(blank=True, null=True)),
                ('complete_photo', models.IntegerField(blank=True, null=True)),
                ('order_photo', models.IntegerField(blank=True, null=True)),
                ('block_test', models.IntegerField(blank=True, null=True)),
                ('collect_things', models.IntegerField(blank=True, null=True)),
                ('maze_test', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WechslerTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('errors_allowed', models.IntegerField(blank=True, null=True)),
                ('general_test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wechsler_general_test', to='first_app.generaltest')),
            ],
            options={
                'verbose_name_plural': 'اختبارات ويكسلر',
            },
        ),
        migrations.CreateModel(
            name='WechslerQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('score', models.CharField(max_length=10)),
                ('hint', models.TextField(blank=True, null=True)),
                ('time', models.IntegerField(blank=True, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wechsler_qustions', to='first_app.wechslertest')),
            ],
            options={
                'verbose_name_plural': 'أسئلة ويكسلر',
            },
        ),
        migrations.CreateModel(
            name='PortageTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('general_test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='protage_general_test', to='first_app.generaltest')),
            ],
            options={
                'verbose_name_plural': 'اختبارات بورتيج',
            },
        ),
        migrations.CreateModel(
            name='PortageQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('score', models.CharField(max_length=10)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portage_qustions', to='first_app.portageblock')),
            ],
            options={
                'verbose_name_plural': 'أسئلة بورتيج',
            },
        ),
        migrations.CreateModel(
            name='PortageChildTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('level', models.TextField(blank=True, null=True)),
                ('child_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portage_results', to='first_app.childpersonalinfo')),
                ('portage_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portage_test', to='first_app.portagetest')),
            ],
            options={
                'verbose_name_plural': 'نتائج اختبارات بورتيج',
            },
        ),
        migrations.AddField(
            model_name='portageblock',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='first_app.portagetest'),
        ),
        migrations.CreateModel(
            name='ParentsTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('general_test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents_general_test', to='first_app.generaltest')),
            ],
            options={
                'verbose_name_plural': 'اختبارات الأهل',
            },
        ),
        migrations.CreateModel(
            name='ParentsQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('score', models.CharField(max_length=10)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents_qustions', to='first_app.parentsblock')),
            ],
            options={
                'verbose_name_plural': 'أسئلة الأهل',
            },
        ),
        migrations.AddField(
            model_name='parentsblock',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='first_app.parentstest'),
        ),
        migrations.CreateModel(
            name='LddrsQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('score', models.CharField(max_length=20)),
                ('general_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.lddrstest')),
            ],
        ),
        migrations.CreateModel(
            name='LddrsChild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=50)),
                ('diagnose', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_app.childpersonalinfo')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ChildInfoQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qustion', models.TextField()),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block_qustions', to='first_app.childinfoblock')),
            ],
        ),
        migrations.CreateModel(
            name='ChildInfoAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True)),
                ('child_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_id', to='first_app.childpersonalinfo')),
                ('qustion_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='qustion_id', to='first_app.childinfoquestion')),
            ],
        ),
    ]
