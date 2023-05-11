from datetime import timezone
from django.utils.timezone import make_aware
import datetime
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nmec, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not nmec:
            raise ValueError('Users must have an nmec')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            email=self.normalize_email(email),
            nmec=nmec,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nmec, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            nmec=nmec,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    nmec = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nmec', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def num_exercises(self):
        # Number of exercises that the student has to do in which the deadline has not passed
        return Exercise.objects.filter(students_class__students=self, deadline__gt=datetime.datetime.now(timezone.utc)).count()

    @property
    def num_submissions(self):
        # Number of submissions that the student has delivered
        return CodeSubmission.objects.filter(student=self).count()

    @property
    def next_deadline(self):
        # Next deadline in which the deadline has not passed
        next_deadline = Exercise.objects.filter(students_class__students=self, deadline__gt=datetime.datetime.now(timezone.utc)).order_by('deadline').first()
        if next_deadline is None:
            return None
        return next_deadline.deadline

    @property
    def next_deadline_title(self):
        # Next deadline in which the deadline has not passed
        next_deadline = Exercise.objects.filter(students_class__students=self, deadline__gt=datetime.datetime.now(timezone.utc)).order_by('deadline').first()
        if next_deadline is None:
            return None
        return next_deadline.title

    @property
    def last_ranking(self):
        # Last exercise that the student has done
        last_submission = CodeSubmission.objects.filter(student=self).order_by('-result_submission_date').first()

        if last_submission is None:
            return None

        exercise_class = last_submission.exercise.students_class

        # Get the results of the class for the same exercise
        class_results = Result.objects.filter(exercise=last_submission.exercise, student__in=exercise_class.students.all()).order_by('-score')

        # Get my position in the ranking of the class
        my_position = 0
        for result in class_results:
            if result.student == self:
                break
            my_position += 1

        return my_position + 1


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='classes_images/', blank=True)
    # relationships
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

    class Meta:
        verbose_name_plural = "Classes"


class Dataset(models.Model):
    id = models.AutoField(primary_key=True)

    train_name = models.CharField(max_length=30)
    train_dataset = models.FileField(upload_to='datasets/train/')
    train_upload_date = models.DateTimeField(auto_now_add=True)
    train_size = models.IntegerField() #size in bytes
    
    test_name = models.CharField(max_length=30)
    test_dataset = models.FileField(upload_to='datasets/test/')
    test_upload_date = models.DateTimeField(auto_now_add=True)
    test_size = models.IntegerField() #size in bytes


class Metric(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=300, blank=True)
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    metric_file = models.FileField(upload_to='metrics/')


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    evaluation = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    limit_of_attempts = models.SmallIntegerField()
    visibility = models.BooleanField()

    # relationships
    students_class = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    metrics = models.ManyToManyField(Metric)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE)

    @property # for using in serializer
    def num_answers(self):
        return CodeSubmission.objects.filter(exercise=self).count()


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
    file_name_result = models.CharField(max_length=30)
    result_submission = models.FileField(upload_to='results/')
    result_submission_date = models.DateTimeField(auto_now_add=True)
    code_submission = models.FileField(upload_to='code_submissions/')
    file_name_code = models.CharField(max_length=30)
    code_submission_date = models.DateTimeField(auto_now_add=True)

    # relationships
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)