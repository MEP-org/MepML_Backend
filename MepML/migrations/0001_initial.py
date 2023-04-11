# Generated by Django 4.1.7 on 2023-04-11 12:34

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
            name="Dataset",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("path_to_train_file", models.CharField(max_length=200)),
                ("path_to_test_file", models.CharField(max_length=200)),
                ("number_of_features", models.IntegerField()),
                ("description", models.CharField(max_length=100)),
                ("is_public", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Metric",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=20)),
                ("path_to_function", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nmec", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Professor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                ("subtitle", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=30)),
                ("start_date", models.DateTimeField()),
                ("deadline", models.DateTimeField()),
                ("limit_of_attempts", models.SmallIntegerField()),
                ("visibility", models.BooleanField()),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MepML.professor",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="MepML.dataset"
                    ),
                ),
                ("metrics", models.ManyToManyField(to="MepML.metric")),
            ],
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("number_of_students", models.IntegerField()),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MepML.professor",
                    ),
                ),
                ("students", models.ManyToManyField(to="MepML.student")),
            ],
            options={
                "verbose_name_plural": "Classes",
            },
        ),
    ]
