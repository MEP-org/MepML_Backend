# Generated by Django 4.1.7 on 2023-05-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MepML', '0002_codesubmission_quantity_of_submissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codesubmission',
            name='file_name_code',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='codesubmission',
            name='file_name_result',
            field=models.CharField(max_length=70),
        ),
    ]
