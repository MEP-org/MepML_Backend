from django.db import models
from django.contrib.auth.models import User


user_id = models.IntegerField(default=0)

class Professor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)


class Student(models.Model):
    mecanographic_number = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)


class Class(models.Model):
    name = models.CharField(max_length=50)
    number_of_students = models.IntegerField()
    # relationships
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)


class Dataset(models.Model):
    path_to_train_file = models.CharField(max_length=200)
    path_to_test_file = models.CharField(max_length=200)
    number_of_features = models.IntegerField()
    description = models.CharField(max_length=100)
    is_public = models.BooleanField()


class Metric(models.Model):
    name = models.CharField(max_length=20)
    path_to_function = models.CharField(max_length=200)


class Asssignment(models.Model):
    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()
    limit_of_attempts = models.SmallIntegerField()
    visibility = models.BooleanField()
    # relationships
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    # metrics = models.ManyToManyRel(Metric)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
