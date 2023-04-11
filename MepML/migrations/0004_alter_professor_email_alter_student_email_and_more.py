# Generated by Django 4.1.7 on 2023-04-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MepML", "0003_alter_class_students"),
    ]

    operations = [
        migrations.AlterField(
            model_name="professor",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="nmec",
            field=models.IntegerField(unique=True),
        ),
    ]
