# Generated by Django 2.2.28 on 2023-03-31 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path_to_train_file', models.CharField(max_length=200)),
                ('path_to_test_file', models.CharField(max_length=200)),
                ('number_of_features', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('is_public', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('path_to_function', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mecanographic_number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number_of_students', models.IntegerField()),
                ('created_by', models.ForeignKey(on_delete=models.CASCADE, to='MepML.Professor')),
                ('studenst', models.ManyToManyField(to='MepML.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Asssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('subtitle', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=30)),
                ('start_date', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('limit_of_attempts', models.SmallIntegerField()),
                ('visibility', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=models.CASCADE, to='MepML.Professor')),
                ('dataset', models.ForeignKey(on_delete=models.CASCADE, to='MepML.Dataset')),
            ],
        ),
    ]
