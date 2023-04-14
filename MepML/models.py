from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    nmec = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nmec', 'name']

    def __str__(self):
        return self.name


class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Class_images/', blank=True)
    # relationships
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

    class Meta:
        verbose_name_plural = "Classes"


class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    
    train_name = models.CharField(max_length=30)
    train_dataset = models.FileField(upload_to='Datasets/Train/')
    train_upload_date = models.DateTimeField(auto_now_add=True)

    test_name = models.CharField(max_length=30)
    test_dataset = models.FileField(upload_to='Datasets/Test/')
    test_upload_date = models.DateTimeField(auto_now_add=True)
    

class Metric(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    path_to_function = models.CharField(max_length=200)


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    evaluation = models.CharField(max_length=100)
    publish_date = models.DateTimeField()
    deadline = models.DateTimeField()
    limit_of_attempts = models.SmallIntegerField()
    visibility = models.BooleanField()

    # relationships
    students_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    metrics = models.ManyToManyField(Metric)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    # relationships
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)


class CodeSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    result_submission = models.FileField(upload_to='results/')
    code_submission = models.FileField(upload_to='code_submissions/')
    submission_date = models.DateTimeField(auto_now_add=True)

    # relationships
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
