from datetime import date, timezone
import datetime
from unittest import skip, skipIf, skipUnless
from unittest import mock
from rest_framework.test import APIRequestFactory, APITestCase

from rest_framework import status

from MepML.models import Dataset, Exercise, Professor, Result, User, Student, Class, Metric
from MepML.serializers import DatasetSerializer, ExerciseSerializer, ProfessorExerciseSerializer, UserSerializer, StudentSerializer, ProfessorClassSerializer, ProfessorClassesSerializer, StudentClassSerializer, StudentClassesSerializer, MetricSerializer, ProfessorExerciseResultSerializer

from django.utils.timezone import make_aware

# https://www.20tab.com/en/blog/test-python-mocking/
# https://www.django-rest-framework.org/api-guide/testing/
# Create your tests here.

class TestUserSerializer(APITestCase):

    def test_user_serializer(self):
        # Create User
        user = User(nmec=102932, name="João Mário", email="jm@ua.pt")

        # Serialize User
        serializer = UserSerializer(user)

        # Create expected data
        expected_data = {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestStudentSerializer(APITestCase):

    def test_student_serializer(self):
        # Create Student
        user = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student = Student.objects.create(user=user)

        # Serialize Student
        serializer = StudentSerializer(student)

        # Create expected data
        expected_data = {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}}

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_multiple_student_serializer(self):
        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Serialize Students
        serializer = StudentSerializer([student1, student2], many=True)

        # Create expected data
        expected_data = [
            {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
            {'id': 2, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestProfessorClassSerializer(APITestCase):
    
    def test_professor_class_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create Class
        class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class_.students.add(student1)
        class_.students.add(student2)

        # Serialize Class
        serializer = ProfessorClassSerializer(class_)

        # Create expected data
        expected_data = {
            'id': 1,
            'name': 'Class 1',
            'image': '/media/image.png',
            'students': [
                {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                {'id': 2, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestProfessorClassesSerializer(APITestCase):
    
    def test_professor_classes_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create Classes
        class1 = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class1.students.add(student1)
        class1.students.add(student2)

        class2 = Class.objects.create(id=2, name="Class 2", image="image2.png", created_by=professor)
        class2.students.add(student1)
        
        # Serialize Classes
        serializer = ProfessorClassesSerializer([class1, class2], many=True)

        # Create expected data
        expected_data = [
            {
                'id': 1,
                'name': 'Class 1',
                'num_students': 2,
                'image': '/media/image.png',
            },
            {
                'id': 2,
                'name': 'Class 2',
                'num_students': 1,
                'image': '/media/image2.png',
            },
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)

class TestStudentClassSerializer(APITestCase):
    
    def test_student_class_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create Class

        class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class_.students.add(student1)
        class_.students.add(student2)

        # Serialize Class
        serializer = StudentClassSerializer(class_)

        # Create expected data
        expected_data = {
            'id': 1,
            'name': 'Class 1',
            'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            'image': '/media/image.png',
            'students': [
                {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                {'id': 2, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
            

class TestStudentClassesSerializer(APITestCase):
        
    def test_student_classes_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create Classes
        class1 = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class1.students.add(student1)
        class1.students.add(student2)

        class2 = Class.objects.create(id=2, name="Class 2", image="image2.png", created_by=professor)
        class2.students.add(student1)

        # Serialize Classes
        serializer = StudentClassesSerializer([class1, class2], many=True)

        # Create expected data
        expected_data = [
            {
                'id': 1,
                'name': 'Class 1',
                'num_students': 2,
                'image': '/media/image.png',
                'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            },
            {
                'id': 2,
                'name': 'Class 2',
                'num_students': 1,
                'image': '/media/image2.png',
                'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            },
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestMetricSerializer(APITestCase):
    
    def test_metrics_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Metric
        metric = Metric.objects.create(id=1, name="Metric 1", metric_file="metrica1", created_by=professor)

        # Serialize Metric
        serializer = MetricSerializer(metric)

        # Create expected data
        expected_data = {
            'id': 1,
            'name': 'Metric 1',
            'metric_file': '/media/metrica1',
            'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestDatasetSerializer(APITestCase):
        
    def test_dataset_serializer(self):
        # Create Dataset
        dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Serialize Dataset
        serializer = DatasetSerializer(dataset)

        # Create expected data
        expected_data = {
            'id': 1,
            'train_name': 'train',
            'train_dataset': '/media/train_dataset',
            'train_upload_date': dataset.train_upload_date.isoformat()[:-6]+'Z',
            'test_name': 'test',
            'test_dataset': '/media/test_dataset',
            'test_upload_date': dataset.test_upload_date.isoformat()[:-6]+'Z',
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestExerciseSerializer(APITestCase):
        
    def test_exercise_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create class
        class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class_.students.add(student1)
        class_.students.add(student2)

        # Create Metric
        metric = Metric.objects.create(id=1, name="Metric 1", metric_file="metrica1", created_by=professor)

        # Create Dataset
        dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=class_,
                                        dataset=dataset,
                                        created_by=professor
                                        )
        exercise.metrics.add(metric)

        # Serialize Exercise
        serializer = ExerciseSerializer(exercise)

        # Create expected data

        expected_data = {
            'id': 1,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'description': 'DescriptionMD 1',
            'evaluation': 'EvaluationMD 1',
            'publish_date' : exercise.publish_date.isoformat()[:-6]+'Z',
            'deadline': '2099-12-10T12:00:00Z',
            'limit_of_attempts': 3,
            'visibility': False,
            'metrics': [
                {'id': 1, 'name': 'Metric 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}}
            ],
            'students_class': {
                'id': 1,
                'name': 'Class 1',
            },
            'dataset': {
                'id': 1,
                'train_name': 'train',
                'train_dataset': '/media/train_dataset',
                'train_upload_date': dataset.train_upload_date.isoformat()[:-6]+'Z',
                'test_name': 'test',
                'test_dataset': '/media/test_dataset',
                'test_upload_date': dataset.test_upload_date.isoformat()[:-6]+'Z',
            },
            'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

        
class ResultSerializer(APITestCase):
        
    def test_result_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create class
        class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class_.students.add(student1)
        class_.students.add(student2)

        # Create Metric
        metric = Metric.objects.create(id=1, name="Metric 1", metric_file="metrica1", created_by=professor)

        # Create Dataset
        dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")
        
        # Create Exercise
        exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=class_,
                                        dataset=dataset,
                                        created_by=professor
                                        )
        exercise.metrics.add(metric)

        # Create Result
        result = Result.objects.create(id=1, student=student1, exercise=exercise, score=0.5, date=make_aware(datetime.datetime(2020, 12, 10, 12, 0, 0)), metric=metric)

        # Serialize Result
        serializer = ProfessorExerciseResultSerializer(result)

        # Create expected data
        expected_data = {
            'id': 1,
            'student': {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
            'score': 0.5,
            'date': result.date.isoformat()[:-6]+'Z',
            'metric': {'id': 1, 'name': 'Metric 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestProfessorExerciseSerializer(APITestCase):

    def test_professor_exercise_serializer(self):
        # Create Professor
        user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        professor = Professor.objects.create(user=user)

        # Create Students
        user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)

        user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)

        # Create class
        class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class_.students.add(student1)
        class_.students.add(student2)

        # Create Metric
        metric = Metric.objects.create(id=1, name="Metric 1", metric_file="metrica1", created_by=professor)

        # Create Dataset
        dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=class_,
                                        dataset=dataset,
                                        created_by=professor
                                        )
        exercise.metrics.add(metric)

        # Create Result
        result1 = Result.objects.create(id=1, student=student1, exercise=exercise, score=0.5, date=make_aware(datetime.datetime(2020, 12, 10, 12, 0, 0)), metric=metric)
        result2 = Result.objects.create(id=2, student=student2, exercise=exercise, score=0.6, date=make_aware(datetime.datetime(2020, 12, 10, 12, 0, 0)), metric=metric)
        result3 = Result.objects.create(id=3, student=student1, exercise=exercise, score=0.7, date=make_aware(datetime.datetime(2020, 12, 10, 12, 0, 0)), metric=metric)
        
        # Serialize Exercise
        serializer = ProfessorExerciseSerializer(instance={
            'exercise': exercise,
            'results': [result1, result2, result3]
        }
        )
        # Create expected data

        expected_data = {
            'exercise': {
                'id': 1,
                'title': 'Exercise 1',
                'subtitle': 'Subtitle 1',
                'description': 'DescriptionMD 1',
                'evaluation': 'EvaluationMD 1',
                'publish_date' : exercise.publish_date.isoformat()[:-6]+'Z',
                'deadline': '2099-12-10T12:00:00Z',
                'limit_of_attempts': 3,
                'visibility': False,
                'metrics': [
                    {'id': 1, 'name': 'Metric 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}}
                ],
                'students_class': {
                    'id': 1,
                    'name': 'Class 1',
                },
                'dataset': {
                    'id': 1,
                    'train_name': 'train',
                    'train_dataset': '/media/train_dataset',
                    'train_upload_date': dataset.train_upload_date.isoformat()[:-6]+'Z',
                    'test_name': 'test',
                    'test_dataset': '/media/test_dataset',
                    'test_upload_date': dataset.test_upload_date.isoformat()[:-6]+'Z',
                },
                'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            },
            'results': [
                {
                    'id': 1,
                    'student': {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                    'score': 0.5,
                    'date': result1.date.isoformat()[:-6]+'Z',
                    'metric': {'id': 1, 'name': 'Metric 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                },
                {
                    'id': 2,
                    'student': {'id': 2, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
                    'score': 0.6,
                    'date': result2.date.isoformat()[:-6]+'Z',
                    'metric': {'id': 1, 'name': 'Metric 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                },
                {
                    'id': 3,
                    'student': {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                    'score': 0.7,
                    'date': result3.date.isoformat()[:-6]+'Z',
                    'metric': {'id': 1, 'name': 'Metric 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    


