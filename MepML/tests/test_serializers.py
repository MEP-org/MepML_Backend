from datetime import date, timezone
import datetime
from unittest import skip, skipIf, skipUnless
from unittest import mock
from rest_framework.test import APIRequestFactory, APITestCase

from rest_framework import status

from MepML.models import CodeSubmission, Dataset, Exercise, Professor, Result, User, Student, Class, Metric
from MepML.serializers import DatasetSerializer, ExerciseSerializer, MetricOwnSerializer, MetricViewerSerializer, ProfessorExerciseSerializer, ProfessorExercisesExerciseSerializer, ProfessorExercisesSerializer, ProfessorMetricsSerializer, PublicExercisesExerciseSerializer, PublicExercisesExerciseTrainingDatasetSerializer, PublicExercisesProfessorsSerializer, PublicExercisesSerializer, StudentAssignmentCodeSubmissionSerializer, StudentAssignmentExerciseAndOwnResultsSerializer, StudentAssignmentExerciseDatasetSerializer, StudentAssignmentExerciseOwnResultsSerializer, StudentAssignmentExerciseSerializer, StudentAssignmentSerializer, StudentAssignmentsSerializer, StudentHomeSerializer, UserSerializer, StudentSerializer, ProfessorClassSerializer, ProfessorClassesSerializer, StudentClassSerializer, StudentClassesSerializer, MetricSerializer, ProfessorExerciseResultSerializer, ProfessorExercisesClassSerializer

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


class TestMetricsSerializers(APITestCase):

    def setUp(self):
         # Create Professor
        self.user1 = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        self.professor1 = Professor.objects.create(user=self.user1)

        self.user2 = User.objects.create(nmec=102934, name="Violeta Rodrigues", email="vr@ua.pt")
        self.professor2 = Professor.objects.create(user=self.user2)

        # Create Metric
        self.metric1 = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=self.professor1)
        self.metric2 = Metric.objects.create(id=2, title="Metric 2", description="Metric Description 2", metric_file="metrica2", created_by=self.professor2)
    
    def test_metric_serializer(self):
        # Serialize Metric
        serializer = MetricSerializer(self.metric1)

        # Create expected data
        expected_data = {
            'id': 1,
            'title': 'Metric 1',
            'description': 'Metric Description 1',
            'metric_file': '/media/metrica1',
            'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_metric_own_serializer(self):
        # Serialize Metric
        serializer = MetricOwnSerializer(self.metric1)

        # Create expected data
        expected_data = {
            'id': 1,
            'title': 'Metric 1',
            'description': 'Metric Description 1',
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_metric_viewer_serializer(self):
        # Serialize Metric
        serializer = MetricViewerSerializer(self.metric1)

        # Create expected data
        expected_data = {
            'id': 1,
            'title': 'Metric 1',
            'description': 'Metric Description 1',
            'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_professor_metrics_serializer(self):
        # Serialize Metrics
        serializer = ProfessorMetricsSerializer(instance={
            'my_metrics': [self.metric1],
            'other_metrics': [self.metric2],
        })

        # Create expected data
        expected_data = {
            'my_metrics': [
                {
                    'id': 1,
                    'title': 'Metric 1',
                    'description': 'Metric Description 1',
                },
            ],
            'other_metrics': [
                {
                    'id': 2,
                    'title': 'Metric 2',
                    'description': 'Metric Description 2',
                    'created_by': {'id': 2, 'user': {'email': 'vr@ua.pt', 'nmec': 102934, 'name': 'Violeta Rodrigues'}},
                },
            ],
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
        metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=professor)

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
                {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}}
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
        metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=professor)

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
            'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
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
        metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=professor)

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
                    {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}}
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
                    'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                },
                {
                    'id': 2,
                    'student': {'id': 2, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
                    'score': 0.6,
                    'date': result2.date.isoformat()[:-6]+'Z',
                    'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                },
                {
                    'id': 3,
                    'student': {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                    'score': 0.7,
                    'date': result3.date.isoformat()[:-6]+'Z',
                    'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestProfessorExercisesSerializer(APITestCase):

    def setUp(self):
        # Create Professor
        self.user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        self.professor = Professor.objects.create(user=self.user)

        # Create Students
        self.user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        self.student1 = Student.objects.create(user=self.user1)

        self.user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        self.student2 = Student.objects.create(user=self.user2)

        # Create class
        self.class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=self.professor)
        self.class_.students.add(self.student1)
        self.class_.students.add(self.student2)

        # Create Metric
        self.metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=self.professor)

        # Create Dataset
        self.dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        self.exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=self.class_,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        self.exercise.metrics.add(self.metric)

        # Create CodeSubmission
        self.code_submission1 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student1)
        self.code_submission2 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student2)

    def test_professor_exercises_class_serializer(self):
        # Serialize
        serializer = ProfessorExercisesClassSerializer([self.class_], many=True)
        
        # Create expected data
        expected_data = [
            {
                'id': 1,
                'name': 'Class 1',
            }
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_professor_exercises_exercise_serializer(self):
        # Serialize
        serializer = ProfessorExercisesExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': 1,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
            'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
            'limit_of_attempts': 3,
            'visibility': False,
            'students_class': {'id': 1, 'name': 'Class 1', 'num_students': 2, 'image': '/media/image.png'},
            'num_answers': 2,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    
    def test_professor_exercises_serializer(self):
        # Serialize
        serializer = ProfessorExercisesSerializer(instance={
            'exercises': [self.exercise],
            'classes': [self.class_]
        })
        
        # Create expected data
        expected_data = {
            'exercises': [
                {
                    'id': 1,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
                    'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
                    'limit_of_attempts': 3,
                    'visibility': False,
                    'students_class': {'id': 1, 'name': 'Class 1', 'num_students': 2, 'image': '/media/image.png'},
                    'num_answers': 2,
                }
            ],
            'classes': [
                {
                    'id': 1,
                    'name': 'Class 1',
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestPublicExercisesSerializer(APITestCase):

    def setUp(self):
        # Create Professor
        self.user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        self.professor = Professor.objects.create(user=self.user)

        # Create Dataset
        self.dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        self.exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=True,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        
    def test_public_exercises_professors_serializer(self):
        # Serialize
        serializer = PublicExercisesProfessorsSerializer(self.professor)
        
        # Create expected data
        expected_data = {
            'id': 1,
            'name': 'Pedro Dias',
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    #Since we are working with files names and not files in this tests, we can't get the size of the files so we mock the function
    @mock.patch('MepML.serializers.PublicExercisesExerciseTrainingDatasetSerializer.get_size')
    def test_public_exercises_exercise_training_dataset_serializer(self, mock_get_size):
        # Mock get_size return value
        mock_get_size.return_value = 0

        # Serialize
        serializer = PublicExercisesExerciseTrainingDatasetSerializer(self.dataset)
        
        # Create expected data
        expected_data = {
            'train_dataset': '/media/train_dataset',
            'size': 0,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    #Since we are working with files names and not files in this tests, we can't get the size of the files so we mock the function
    @mock.patch('MepML.serializers.PublicExercisesExerciseTrainingDatasetSerializer.get_size')
    def test_public_exercises_exercise_serializer(self, mock_get_size):
        # Mock get_size return value
        mock_get_size.return_value = 0

        # Serialize
        serializer = PublicExercisesExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': 1,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
            'created_by': {'id': 1, 'name': 'Pedro Dias'},
            'dataset': {'train_dataset': '/media/train_dataset', 'size': 0},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    #Since we are working with files names and not files in this tests, we can't get the size of the files so we mock the function
    @mock.patch('MepML.serializers.PublicExercisesExerciseTrainingDatasetSerializer.get_size')
    def test_public_exercises_serializer(self, mock_get_size):
        # Mock get_size return value
        mock_get_size.return_value = 0

        # Serialize
        serializer = PublicExercisesSerializer(instance={
            'exercises': [self.exercise],
            'professors': [self.professor]
        })
        
        # Create expected data
        expected_data = {
            'exercises': [
                {
                    'id': 1,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
                    'created_by': {'id': 1, 'name': 'Pedro Dias'},
                    'dataset': {'train_dataset': '/media/train_dataset', 'size': 0},
                }
            ],
            'professors': [
                {
                    'id': 1,
                    'name': 'Pedro Dias',
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestStudentAssignmentSerializer(APITestCase):

    def setUp(self):
        # Create Professor
        self.user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        self.professor = Professor.objects.create(user=self.user)

        # Create Students
        self.user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        self.student1 = Student.objects.create(user=self.user1)

        self.user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        self.student2 = Student.objects.create(user=self.user2)

        # Create class
        self.class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=self.professor)
        self.class_.students.add(self.student1)
        self.class_.students.add(self.student2)

        # Create Metric
        self.metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=self.professor)

        # Create Dataset
        self.dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        self.exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=self.class_,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        self.exercise.metrics.add(self.metric)

        # Create Result
        self.result1 = Result.objects.create(id=1, score=0.5, student=self.student1, exercise=self.exercise, metric=self.metric)

        # Create CodeSubmission
        self.code_submission1 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student1)
        self.code_submission2 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student2)

    #Since we are working with files names and not files in this tests, we can't get the size of the files so we mock the function
    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_train_dataset_size')
    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_test_dataset_size')
    def test_student_assignment_exercise_dataset_serializer(self, mock_get_train_dataset_size, mock_get_test_dataset_size):
        # Mock get_size return value
        mock_get_train_dataset_size.return_value = 0
        mock_get_test_dataset_size.return_value = 0
        
        # Serialize
        serializer = StudentAssignmentExerciseDatasetSerializer(self.dataset)
        
        # Create expected data
        expected_data = {
            'train_name': 'train',
            'train_dataset': '/media/train_dataset',
            'train_dataset_size': 0,
            'train_upload_date': self.dataset.train_upload_date.isoformat()[:-6]+'Z',

            'test_name': 'test',
            'test_dataset': '/media/test_dataset',
            'test_dataset_size': 0,
            'test_upload_date': self.dataset.test_upload_date.isoformat()[:-6]+'Z',
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_student_assignment_exercise_own_results_serializer(self):
        # Serialize
        serializer = StudentAssignmentExerciseOwnResultsSerializer(self.result1)
        
        # Create expected data
        expected_data = {
            'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1'},
            'score': 0.5,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_train_dataset_size')
    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_test_dataset_size')
    def test_student_assignment_exercise_serializer(self, mock_get_train_dataset_size, mock_get_test_dataset_size):
        # Mock get_size return value
        mock_get_train_dataset_size.return_value = 0
        mock_get_test_dataset_size.return_value = 0

        # Serialize
        serializer = StudentAssignmentExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': 1,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
            'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
            'limit_of_attempts': 3,
            'visibility': False,
            'students_class': {'id': 1, 'name': 'Class 1'},
            'metrics': [{'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1'}],
            'description': 'DescriptionMD 1',
            'evaluation': 'EvaluationMD 1',
            'dataset': {
                'train_name': 'train',
                'train_dataset': '/media/train_dataset',
                'train_dataset_size': 0,
                'train_upload_date': self.dataset.train_upload_date.isoformat()[:-6]+'Z',
                'test_name': 'test',
                'test_dataset': '/media/test_dataset',
                'test_dataset_size': 0,
                'test_upload_date': self.dataset.test_upload_date.isoformat()[:-6]+'Z',
            },
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_train_dataset_size')
    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_test_dataset_size')
    def test_student_assignment_exercise_and_own_results_serializer(self, mock_get_train_dataset_size, mock_get_test_dataset_size):
        # Mock get_size return value
        mock_get_train_dataset_size.return_value = 0
        mock_get_test_dataset_size.return_value = 0

        # Serialize
        serializer = StudentAssignmentExerciseAndOwnResultsSerializer(instance={
            'exercise': self.exercise,
            'my_results': [self.result1]
        })
        
        # Create expected data
        expected_data = {
            'exercise': {
                'id': 1,
                'title': 'Exercise 1',
                'subtitle': 'Subtitle 1',
                'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
                'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
                'limit_of_attempts': 3,
                'visibility': False,
                'students_class': {'id': 1, 'name': 'Class 1'},
                'metrics': [{'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1'}],
                'description': 'DescriptionMD 1',
                'evaluation': 'EvaluationMD 1',
                'dataset': {
                    'train_name': 'train',
                    'train_dataset': '/media/train_dataset',
                    'train_dataset_size': 0,
                    'train_upload_date': self.dataset.train_upload_date.isoformat()[:-6]+'Z',
                    'test_name': 'test',
                    'test_dataset': '/media/test_dataset',
                    'test_dataset_size': 0,
                    'test_upload_date': self.dataset.test_upload_date.isoformat()[:-6]+'Z',
                },
            },
            'my_results': [
                {
                    'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1'},
                    'score': 0.5,
                }
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    def test_student_assignment_code_submission_serializer(self):
        # Serialize
        serializer = StudentAssignmentCodeSubmissionSerializer(self.code_submission1)
        
        # Create expected data
        expected_data = {
            'id': 1,
            'file_name_result': 'result.py',
            'result_submission': '/media/result.py',
            'result_submission_date': self.code_submission1.result_submission_date.isoformat()[:-6]+'Z',
            'file_name_code': 'code.py',
            'code_submission': '/media/code.py',
            'code_submission_date': self.code_submission1.code_submission_date.isoformat()[:-6]+'Z',
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_train_dataset_size')
    @mock.patch('MepML.serializers.StudentAssignmentExerciseDatasetSerializer.get_test_dataset_size')
    def test_student_assignment_serializer(self, mock_get_train_dataset_size, mock_get_test_dataset_size):
        # Mock get_size return value
        mock_get_train_dataset_size.return_value = 0
        mock_get_test_dataset_size.return_value = 0
        
        # Serialize
        serializer = StudentAssignmentSerializer(instance={
            'assignment': {
                'exercise': self.exercise,
                'my_results': [self.result1],
            },
            'all_results': [self.result1],
            'submission': self.code_submission1,
        })
        
        # Create expected data
        expected_data = {
            'assignment': {
                'exercise': {
                    'id': 1,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
                    'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
                    'limit_of_attempts': 3,
                    'visibility': False,
                    'students_class': {'id': 1, 'name': 'Class 1'},
                    'metrics': [{'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1'}],
                    'description': 'DescriptionMD 1',
                    'evaluation': 'EvaluationMD 1',
                    'dataset': {
                        'train_name': 'train',
                        'train_dataset': '/media/train_dataset',
                        'train_dataset_size': 0,
                        'train_upload_date': self.dataset.train_upload_date.isoformat()[:-6]+'Z',
                        'test_name': 'test',
                        'test_dataset': '/media/test_dataset',
                        'test_dataset_size': 0,
                        'test_upload_date': self.dataset.test_upload_date.isoformat()[:-6]+'Z',
                        },
                },
                'my_results': [
                    {
                        'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1'},
                        'score': 0.5,
                    }
                ],
            },
            'all_results': [
                {
                    'id': 1,
                    'student': {'id': 1, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                    'score': 0.5,
                    'date': self.result1.date.isoformat()[:-6]+'Z',
                    'metric': {'id': 1, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': 1, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                },
            ],
            'submission': {
                'id': 1,
                'file_name_result': 'result.py',
                'result_submission': '/media/result.py',
                'result_submission_date': self.code_submission1.result_submission_date.isoformat()[:-6]+'Z',
                'file_name_code': 'code.py',
                'code_submission': '/media/code.py',
                'code_submission_date': self.code_submission1.code_submission_date.isoformat()[:-6]+'Z',
            },
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestStudentAssignmentsSerializer(APITestCase):

    def setUp(self):
        # Create Professor
        self.user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        self.professor = Professor.objects.create(user=self.user)

        # Create Students
        self.user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        self.student1 = Student.objects.create(user=self.user1)

        self.user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        self.student2 = Student.objects.create(user=self.user2)

        # Create class
        self.class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=self.professor)
        self.class_.students.add(self.student1)
        self.class_.students.add(self.student2)

        # Create Metric
        self.metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=self.professor)

        # Create Dataset
        self.dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        self.exercise = Exercise.objects.create(
                                        id=1,
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=self.class_,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        self.exercise.metrics.add(self.metric)

        # Create CodeSubmission
        self.code_submission1 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student1)
        self.code_submission2 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student2)


    def test_student_assignments_serializer(self):
        # Arrange
        serializer = StudentAssignmentsSerializer(instance={
            'exercises': [self.exercise],
            'classes': [self.class_],
        })

        # Serialize
        expected_data = {
            'exercises': [
                {
                    'id': 1,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.isoformat()[:-6]+'Z',
                    'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
                    'limit_of_attempts': 3,
                    'visibility': False,
                    'students_class': {
                        'id': 1,
                        'name': 'Class 1',
                    },
                    'num_answers': 2,
                },
            ],
            'classes': [
                {
                    'id': 1,
                    'name': 'Class 1',
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


class TestStudentHomeSerializer(APITestCase):

    def setUp(self):
        # Create Professor
        self.user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
        self.professor = Professor.objects.create(user=self.user)

        # Create Students
        self.user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
        self.student1 = Student.objects.create(user=self.user1)

        self.user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
        self.student2 = Student.objects.create(user=self.user2)

        # Create class
        self.class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=self.professor)
        self.class_.students.add(self.student1)
        self.class_.students.add(self.student2)

        # Create Metric
        self.metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=self.professor)

        # Create Dataset
        self.dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", test_name="test", test_dataset="test_dataset")

        # Create Exercise
        self.exercise = Exercise.objects.create(
                                        title="Exercise 1",
                                        subtitle="Subtitle 1",
                                        description="DescriptionMD 1",
                                        evaluation="EvaluationMD 1",
                                        deadline= make_aware(datetime.datetime(2099, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=self.class_,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        self.exercise.metrics.add(self.metric)

        # Create Exercise
        self.exercise2 = Exercise.objects.create(
                                        title="Exercise 2",
                                        subtitle="Subtitle 2",
                                        description="DescriptionMD 2",
                                        evaluation="EvaluationMD 2",
                                        deadline= make_aware(datetime.datetime(2098, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=self.class_,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        self.exercise2.metrics.add(self.metric)

        # Create Exercise
        self.exercise3 = Exercise.objects.create(
                                        title="Exercise 3",
                                        subtitle="Subtitle 3",
                                        description="DescriptionMD 3",
                                        evaluation="EvaluationMD 3",
                                        deadline= make_aware(datetime.datetime(1994, 12, 10, 12, 0, 0)),
                                        limit_of_attempts=3,
                                        visibility=False,
                                        students_class=self.class_,
                                        dataset=self.dataset,
                                        created_by=self.professor
                                        )
        self.exercise3.metrics.add(self.metric)
            
        # Create CodeSubmission
        self.code_submission1 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student1)
        self.code_submission2 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student2)
        self.code_submission3 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise2, student=self.student1)
        self.code_submission4 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise3, student=self.student1)

        # Create Result
        self.result1 = Result.objects.create(score=0.5, student=self.student1, exercise=self.exercise, metric=self.metric)
        self.result2 = Result.objects.create(score=0.6, student=self.student1, exercise=self.exercise2, metric=self.metric)
        self.result3 = Result.objects.create(score=0.7, student=self.student1, exercise=self.exercise3, metric=self.metric)
        self.result10 = Result.objects.create(score=0.9, student=self.student2, exercise=self.exercise, metric=self.metric)

    def test_student_home_serializer(self):
        # Serialize
        serializer = StudentHomeSerializer(self.student1)

        # Expected Data
        expected_data = {
            'num_exercises': 2,
            'num_submissions': 3,
            'next_deadline': datetime.datetime(2098, 12, 10, 12, 0, tzinfo=datetime.timezone.utc),
            'last_ranking': 1,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)



        