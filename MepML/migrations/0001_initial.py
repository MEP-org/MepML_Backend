# Generated by Django 4.1.7 on 2023-04-15 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='classes_images/')),
            ],
            options={
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=30)),
                ('train_dataset', models.FileField(upload_to='datasets/train/')),
                ('train_upload_date', models.DateTimeField(auto_now_add=True)),
                ('test_name', models.CharField(max_length=30)),
                ('test_dataset', models.FileField(upload_to='datasets/test/')),
                ('test_upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('subtitle', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('evaluation', models.CharField(max_length=100)),
                ('publish_date', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('limit_of_attempts', models.SmallIntegerField()),
                ('visibility', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=300, blank=True)),
                ('source_code', models.FileField(default='', upload_to='metrics/')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nmec', models.CharField(max_length=15, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.exercise')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.metric')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.student')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nmec', models.CharField(max_length=15, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.professor'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.dataset'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='metrics',
            field=models.ManyToManyField(to='MepML.metric'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='students_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.class'),
        ),
        migrations.CreateModel(
            name='CodeSubmission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('result_submission', models.FileField(upload_to='results/')),
                ('code_submission', models.FileField(upload_to='code_submissions/')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('Exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.exercise')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.student')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MepML.professor'),
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(blank=True, to='MepML.student'),
        ),
    ]
