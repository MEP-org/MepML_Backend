from datetime import date, timezone
import datetime
from unittest import skip, skipIf, skipUnless
from unittest import mock
from rest_framework.test import APIRequestFactory, APITestCase

from rest_framework import status

from MepML.models import CodeSubmission, Dataset, Exercise, Professor, Result, User, Student, Class, Metric
from MepML.serializers import DatasetSerializer, ExercisePostSerializer, ExerciseSerializer, MetricOwnSerializer, MetricSerializer, \
    MetricViewerSerializer, ProfessorClassPostSerializer, ProfessorClassSerializer, ProfessorClassesSerializer, ProfessorCreateExerciseGETSerializer, ProfessorExerciseResultSerializer, ProfessorExerciseSerializer, ProfessorExercisesExerciseSerializer, ProfessorExercisesSerializer, ProfessorMetricPostSerializer, ProfessorMetricsSerializer, ProfessorSerializer, PublicExerciseSerializer, PublicExercisesExerciseSerializer, PublicExercisesExerciseTrainingDatasetSerializer, PublicExercisesProfessorsSerializer, PublicExercisesSerializer, SimpleClassSerializer, StudentAssignmentCodeSubmissionSerializer, StudentAssignmentExerciseAndOwnResultsSerializer, StudentAssignmentExerciseDatasetSerializer, StudentAssignmentExerciseOwnResultsSerializer, StudentAssignmentExerciseSerializer, StudentAssignmentSerializer, StudentAssignmentsExerciseSerializer, StudentAssignmentsSerializer, StudentClassSerializer, StudentClassesSerializer, StudentHomeSerializer, UserSerializer, StudentSerializer


from django.utils.timezone import make_aware

# https://www.20tab.com/en/blog/test-python-mocking/
# https://www.django-rest-framework.org/api-guide/testing/
# Create your tests here.

def fill_db(self):
    # Create Professor
    self.user = User.objects.create(nmec=102931, name="Pedro Dias", email="pd@ua.pt")
    self.professor = Professor.objects.create(user=self.user)

    # Create Students
    self.user1 = User.objects.create(nmec=102932, name="João Mário", email="jm@ua.pt")
    self.student1 = Student.objects.create(user=self.user1)

    self.user2 = User.objects.create(nmec=102933, name="Rafa Silva", email="rs@ua.pt")
    self.student2 = Student.objects.create(user=self.user2)

    # Create classes
    self.class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=self.professor)
    self.class_.students.add(self.student1)
    self.class_.students.add(self.student2)

    self.class2 = Class.objects.create(id=2, name="Class 2", image="image2.png", created_by=self.professor)
    self.class2.students.add(self.student1)

    # Create Metric
    self.metric1 = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metrica1", created_by=self.professor)
    self.metric2 = Metric.objects.create(id=2, title="Metric 2", description="Metric Description 2", metric_file="metrica2", created_by=self.professor)

    # Create Dataset
    self.dataset = Dataset.objects.create(train_name="train", train_dataset="train_dataset", train_size=0, test_name="test", test_dataset="test_dataset", test_size=0)

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
    self.exercise.metrics.add(self.metric1)

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
    self.exercise2.metrics.add(self.metric1)

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
    self.exercise3.metrics.add(self.metric1)
        
    # Create CodeSubmission
    self.code_submission1 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student1)
    self.code_submission2 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise, student=self.student2)
    self.code_submission3 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise2, student=self.student1)
    self.code_submission4 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=self.exercise3, student=self.student1)

    # Create Result
    self.result1 = Result.objects.create(score=0.5, student=self.student1, exercise=self.exercise, metric=self.metric1)
    self.result2 = Result.objects.create(score=0.6, student=self.student1, exercise=self.exercise2, metric=self.metric1)
    self.result3 = Result.objects.create(score=0.7, student=self.student1, exercise=self.exercise3, metric=self.metric1)
    self.result10 = Result.objects.create(score=0.9, student=self.student2, exercise=self.exercise, metric=self.metric1)

# ------------------------------ Test User Serializers ------------------------------
class TestUserSerializer(APITestCase):

    def setUp(self):
        # Create User
        self.user = User(nmec=102932, name="João Mário", email="jm@ua.pt")

    def test_user_serializer(self):
        # Serialize User
        serializer = UserSerializer(self.user)

        # Create expected data
        expected_data = {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Student Serializers ------------------------------
class TestStudentSerializer(APITestCase):

    def setUp(self):
        fill_db(self)


    def test_student_serializer(self):
        # Serialize Student
        serializer = StudentSerializer(self.student1)

        # Create expected data
        expected_data = {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}}

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_multiple_student_serializer(self):
        # Serialize Students
        serializer = StudentSerializer([self.student1, self.student2], many=True)

        # Create expected data
        expected_data = [
            {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
            {'id': self.student2.id, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_student_home_serializer(self):

        # 2098-12-10 12:00:00+00:00
        # 10/12/2098 12:00:00
        # Serialize
        serializer = StudentHomeSerializer(self.student1)

        # Expected Data
        expected_data = {
            'num_exercises': 2,
            'num_submissions': 3,
            'next_deadline': datetime.datetime(2098, 12, 10, 12, 0, tzinfo=datetime.timezone.utc).strftime("%d/%m/%Y %H:%M:%S"),
            'next_deadline_title': 'Exercise 2',
            'last_ranking': 1,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Professor Serializers ------------------------------
class TestProfessorSerializer(APITestCase):

    def setUp(self):
        fill_db(self)
    
    
    def test_professor_serializer(self):
        # Serialize Professor
        serializer = ProfessorSerializer(self.professor)

        # Create expected data
        expected_data = {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_public_exercises_professors_serializer(self):
        # Serialize
        serializer = PublicExercisesProfessorsSerializer(self.professor)
        
        # Create expected data
        expected_data = {
            'id': self.professor.id,
            'name': 'Pedro Dias',
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Class Serializers ------------------------------
class TestClassSerializer(APITestCase):
    
    def setUp(self):
        fill_db(self)

    
    def test_professor_class_serializer(self):
        # Serialize Class
        serializer = ProfessorClassSerializer(self.class_)

        # Create expected data
        expected_data = {
            'id': self.class_.id,
            'name': 'Class 1',
            'image': '/media/image.png',
            'students': [
                {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                {'id': self.student2.id, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_professor_classes_serializer(self):
        # Serialize Classes
        serializer = ProfessorClassesSerializer([self.class_, self.class2], many=True)

        # Create expected data
        expected_data = [
            {
                'id': self.class_.id,
                'name': 'Class 1',
                'num_students': 2,
                'image': '/media/image.png',
            },
            {
                'id': self.class2.id,
                'name': 'Class 2',
                'num_students': 1,
                'image': '/media/image2.png',
            },
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_professor_class_post_serializer(self):
        # Serialize Class
        serializer = ProfessorClassPostSerializer(self.class_)

        # Create expected data
        expected_data = {
            'id': self.class_.id,
            'name': 'Class 1',
            'image': '/media/image.png',
            'created_by': 1,
            'students': [1, 2],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    
    def test_student_class_serializer(self):
        # Serialize Class
        serializer = StudentClassSerializer(self.class_)

        # Create expected data
        expected_data = {
            'id': self.class_.id,
            'name': 'Class 1',
            'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            'image': '/media/image.png',
            'students': [
                {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                {'id': self.student2.id, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_student_classes_serializer(self):
        # Serialize Classes
        serializer = StudentClassesSerializer([self.class_, self.class2], many=True)

        # Create expected data
        expected_data = [
            {
                'id': self.class_.id,
                'name': 'Class 1',
                'num_students': 2,
                'image': '/media/image.png',
                'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            },
            {
                'id': self.class2.id,
                'name': 'Class 2',
                'num_students': 1,
                'image': '/media/image2.png',
                'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            },
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_simple_class_serializer(self):
        # Serialize
        serializer = SimpleClassSerializer([self.class_], many=True)
        
        # Create expected data
        expected_data = [
            {
                'id': self.class_.id,
                'name': 'Class 1',
            }
        ]

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Metric Serializers ------------------------------
class TestMetricSerializer(APITestCase):

    def setUp(self):
        fill_db(self)

    def test_metric_serializer(self):
        # Serialize Metric
        serializer = MetricSerializer(self.metric1)

        # Create expected data
        expected_data = {
            'id': self.metric1.id,
            'title': 'Metric 1',
            'description': 'Metric Description 1',
            'metric_file': '/media/metrica1',
            'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_metric_own_serializer(self):
        # Serialize Metric
        serializer = MetricOwnSerializer(self.metric1)

        # Create expected data
        expected_data = {
            'id': self.metric1.id,
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
            'id': self.metric1.id,
            'title': 'Metric 1',
            'description': 'Metric Description 1',
            'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_professor_metric_post_serializer(self):
        # Serialize Metric
        serializer = ProfessorMetricPostSerializer(self.metric1)

        # Create expected data
        expected_data = {
            'id': self.metric1.id,
            'title': 'Metric 1',
            'description': 'Metric Description 1',
            'metric_file': '/media/metrica1',
            'created_by': self.professor.id,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Dataset Serializers ------------------------------
class TestDatasetSerializer(APITestCase):

    def setUp(self):
        fill_db(self)
    

    def test_dataset_serializer(self):
        # Serialize Dataset
        serializer = DatasetSerializer(self.dataset)

        # Create expected data
        expected_data = {
            'id': self.dataset.id,
            'train_name': 'train',
            'train_dataset': '/media/train_dataset',
            'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
            'train_size': 0,
            'test_name': 'test',
            'test_dataset': '/media/test_dataset',
            'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
            'test_size': 0,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_public_exercises_exercise_training_dataset_serializer(self):
        # Serialize
        serializer = PublicExercisesExerciseTrainingDatasetSerializer(self.dataset)
        
        # Create expected data
        expected_data = {
            'train_name': 'train',
            'train_dataset': '/media/train_dataset',
            'train_size': 0,
            'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_student_assignment_exercise_dataset_serializer(self):
        # Serialize
        serializer = StudentAssignmentExerciseDatasetSerializer(self.dataset)
        
        # Create expected data
        expected_data = {
            'train_name': 'train',
            'train_dataset': '/media/train_dataset',
            'train_size': 0,
            'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),

            'test_name': 'test',
            'test_dataset': '/media/test_dataset',
            'test_size': 0,
            'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Exercise Serializers ------------------------------
class TestExerciseSerializer(APITestCase):
    
    def setUp(self):
        fill_db(self)
    
    def test_exercise_serializer(self):

        # Serialize Exercise
        serializer = ExerciseSerializer(self.exercise)

        # Create expected data

        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'description': 'DescriptionMD 1',
            'evaluation': 'EvaluationMD 1',
            'publish_date' : self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
            'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
            'limit_of_attempts': 3,
            'visibility': False,
            'metrics': [
                {'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}}
            ],
            'students_class': {
                'id': self.class_.id,
                'name': 'Class 1',
            },
            'dataset': {
                'id': self.dataset.id,
                'train_name': 'train',
                'train_dataset': '/media/train_dataset',
                'train_size': 0,
                'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                'test_name': 'test',
                'test_dataset': '/media/test_dataset',
                'test_size': 0,
                'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
            },
            'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_exercise_post_serializer(self):
        # Serialize Exercise
        serializer = ExercisePostSerializer(self.exercise)

        # Create expected data
        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'description': 'DescriptionMD 1',
            'evaluation': 'EvaluationMD 1',
            'publish_date' : self.exercise.publish_date.isoformat()[:-6]+'Z',
            'deadline': self.exercise.deadline.isoformat()[:-6]+'Z',
            'limit_of_attempts': 3,
            'visibility': False,
            'metrics': [self.metric1.id],
            'students_class': self.class_.id,
            'dataset': self.dataset.id,
            'created_by': self.professor.id,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_professor_exercises_exercise_serializer(self):
        # Serialize
        serializer = ProfessorExercisesExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
            'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
            'limit_of_attempts': 3,
            'visibility': False,
            'students_class': {'id': self.class_.id, 'name': 'Class 1', 'num_students': 2, 'image': '/media/image.png'},
            'num_answers': 2,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_public_exercises_exercise_serializer(self):
        # Serialize
        serializer = PublicExercisesExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
            'created_by': {'id': self.professor.id, 'name': 'Pedro Dias'},
            'dataset': {
                'train_name': 'train',
                'train_dataset': '/media/train_dataset',
                'train_size': 0,
                'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")
                },
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    
    def test_student_assignment_exercise_serializer(self):
        # Serialize
        serializer = StudentAssignmentExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
            'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
            'limit_of_attempts': 3,
            'visibility': False,
            'students_class': {'id': self.class_.id, 'name': 'Class 1'},
            'metrics': [{'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1'}],
            'description': 'DescriptionMD 1',
            'evaluation': 'EvaluationMD 1',
            'dataset': {
                'train_name': 'train',
                'train_dataset': '/media/train_dataset',
                'train_size': 0,
                'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                'test_name': 'test',
                'test_dataset': '/media/test_dataset',
                'test_size': 0,
                'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
            },
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_student_assignments_exercise_serializer(self):
        # Serialize
        serializer = StudentAssignmentsExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
            'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
            'limit_of_attempts': 3,
            'visibility': False,
            'students_class': {'id': self.class_.id, 'name': 'Class 1'},
            'num_answers': 2,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
    

    def test_public_exercise_serializer(self):
        # Serialize
        serializer = PublicExerciseSerializer(self.exercise)
        
        # Create expected data
        expected_data = {
            'id': self.exercise.id,
            'title': 'Exercise 1',
            'subtitle': 'Subtitle 1',
            'description': 'DescriptionMD 1',
            'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
            'visibility': False,
            'dataset': {
                'train_name': 'train',
                'train_dataset': '/media/train_dataset',
                'train_size': 0,
                'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")
                },
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test Result Serializers ------------------------------
class TestResultSerializers(APITestCase):

    def setUp(self):
        fill_db(self)

    
    def test_professor_exercise_result_serializer(self):
        # Serialize Result
        serializer = ProfessorExerciseResultSerializer(self.result1)

        # Create expected data
        expected_data = {
            'id': self.result1.id,
            'student': {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
            'score': 0.5,
            'date': self.result1.date.strftime("%d/%m/%Y %H:%M:%S"),
            'metric': {'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1', 'metric_file': '/media/metrica1', 'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    
    def test_student_assignment_exercise_own_results_serializer(self):
        # Serialize
        serializer = StudentAssignmentExerciseOwnResultsSerializer(self.result1)
        
        # Create expected data
        expected_data = {
            'metric': {'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1'},
            'score': 0.5,
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


# ------------------------------ Test CodeSubmission Serializers ------------------------------
class TestCodeSubmissionSerializers(APITestCase):

    def setUp(self):
        fill_db(self)

    @mock.patch('MepML.serializers.StudentAssignmentCodeSubmissionSerializer.get_result_submission_size')
    @mock.patch('MepML.serializers.StudentAssignmentCodeSubmissionSerializer.get_code_submission_size')
    def test_student_assignment_code_submission_serializer(self, mock_get_code_submission_size, mock_get_result_submission_size):
        # Mock
        mock_get_code_submission_size.return_value = 0
        mock_get_result_submission_size.return_value = 0
        
        # Serialize
        serializer = StudentAssignmentCodeSubmissionSerializer(self.code_submission1)
        
        # Create expected data
        expected_data = {
            'id': self.code_submission1.id,
            'file_name_result': 'result.py',
            'result_submission': '/media/result.py',
            'result_submission_size': 0,
            'result_submission_date': self.code_submission1.result_submission_date.strftime("%d/%m/%Y %H:%M:%S"),
            'file_name_code': 'code.py',
            'code_submission': '/media/code.py',
            'code_submission_size': 0,
            'code_submission_date': self.code_submission1.code_submission_date.strftime("%d/%m/%Y %H:%M:%S"),
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    
# ------------------------------ Test Other Serializers ------------------------------
class TestOtherSerializers(APITestCase):

    def setUp(self):
        fill_db(self)
    

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
                    'id': self.metric1.id,
                    'title': 'Metric 1',
                    'description': 'Metric Description 1',
                    'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
                },
            ],
            'other_metrics': [
                {
                    'id': self.metric2.id,
                    'title': 'Metric 2',
                    'description': 'Metric Description 2',
                    'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
                },
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_professor_exercise_serializer(self):
        # Serialize Exercise
        serializer = ProfessorExerciseSerializer(instance={
            'exercise': self.exercise,
            'exercise_class_students': [self.student1, self.student2],
            'results': [self.result10, self.result1]  # This test uses unsorted results to check if it is sorted inside the serializer
        }
        )

        # Create expected data
        expected_data = {
            'exercise': {
                'id': self.exercise.id,
                'title': 'Exercise 1',
                'subtitle': 'Subtitle 1',
                'description': 'DescriptionMD 1',
                'evaluation': 'EvaluationMD 1',
                'publish_date' : self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
                'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
                'limit_of_attempts': 3,
                'visibility': False,
                'metrics': [
                    {'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1', 'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}}},
                ],
                'students_class': {
                    'id': self.class_.id,
                    'name': 'Class 1',
                },
                'dataset': {
                    'id': self.dataset.id,
                    'train_name': 'train',
                    'train_dataset': '/media/train_dataset',
                    'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'train_size': 0,
                    'test_name': 'test',
                    'test_dataset': '/media/test_dataset',
                    'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'test_size':0,
                },
                'created_by': {'id': self.professor.id, 'user': {'email': 'pd@ua.pt', 'nmec': 102931, 'name': 'Pedro Dias'}},
            },
            'results': [
                {
                    'student': {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                    'results': [
                        {'date': self.result1.date.strftime("%d/%m/%Y %H:%M:%S"), 'score': 0.5},
                                ],
                },
                {
                    'student': {'id': self.student2.id, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
                    'results': [
                        {'date': self.result10.date.strftime("%d/%m/%Y %H:%M:%S"), 'score': 0.9},
                    ],
                }
            ]
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
                    'id': self.exercise.id,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
                    'limit_of_attempts': 3,
                    'visibility': False,
                    'students_class': {'id': self.class_.id, 'name': 'Class 1', 'num_students': 2, 'image': '/media/image.png'},
                    'num_answers': 2,
                }
            ],
            'classes': [
                {
                    'id': self.class_.id,
                    'name': 'Class 1',
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_public_exercises_serializer(self):
        # Serialize
        serializer = PublicExercisesSerializer(instance={
            'exercises': [self.exercise],
            'professors': [self.professor]
        })
        
        # Create expected data
        expected_data = {
            'exercises': [
                {
                    'id': self.exercise.id,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'created_by': {'id': self.professor.id, 'name': 'Pedro Dias'},
                    'dataset': {
                        'train_name': 'train',
                        'train_dataset': '/media/train_dataset',
                        'train_size': 0,
                        'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")
                        },
                }
            ],
            'professors': [
                {
                    'id': self.professor.id,
                    'name': 'Pedro Dias',
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_student_assignment_exercise_and_own_results_serializer(self):
        # Serialize
        serializer = StudentAssignmentExerciseAndOwnResultsSerializer(instance={
            'exercise': self.exercise,
            'my_results': [self.result1]
        })
        
        # Create expected data
        expected_data = {
            'exercise': {
                'id': self.exercise.id,
                'title': 'Exercise 1',
                'subtitle': 'Subtitle 1',
                'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
                'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
                'limit_of_attempts': 3,
                'visibility': False,
                'students_class': {'id': self.class_.id, 'name': 'Class 1'},
                'metrics': [{'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1'}],
                'description': 'DescriptionMD 1',
                'evaluation': 'EvaluationMD 1',
                'dataset': {
                    'train_name': 'train',
                    'train_dataset': '/media/train_dataset',
                    'train_size': 0,
                    'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'test_name': 'test',
                    'test_dataset': '/media/test_dataset',
                    'test_size': 0,
                    'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                },
            },
            'my_results': [
                {
                    'metric': {'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1'},
                    'score': 0.5,
                }
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    @mock.patch('MepML.serializers.StudentAssignmentCodeSubmissionSerializer.get_result_submission_size')
    @mock.patch('MepML.serializers.StudentAssignmentCodeSubmissionSerializer.get_code_submission_size')
    def test_student_assignment_serializer(self, mock_get_code_submission_size, mock_get_result_submission_size):
        # Mock
        mock_get_code_submission_size.return_value = 0
        mock_get_result_submission_size.return_value = 0

        # Serialize
        serializer = StudentAssignmentSerializer(instance={
            'assignment': {
                'exercise': self.exercise,
                'my_results': [self.result1],
            },
            'assignment_class_students': [self.student1, self.student2],
            'all_results': [self.result1],
            'submission': self.code_submission1,
        })

        
        # Create expected data
        expected_data = {
            'assignment': {
                'exercise': {
                    'id': self.exercise.id,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
                    'limit_of_attempts': 3,
                    'visibility': False,
                    'students_class': {'id': self.class_.id, 'name': 'Class 1'},
                    'metrics': [{'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1'}],
                    'description': 'DescriptionMD 1',
                    'evaluation': 'EvaluationMD 1',
                    'dataset': {
                        'train_name': 'train',
                        'train_dataset': '/media/train_dataset',
                        'train_size': 0,
                        'train_upload_date': self.dataset.train_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                        'test_name': 'test',
                        'test_dataset': '/media/test_dataset',
                        'test_size': 0,
                        'test_upload_date': self.dataset.test_upload_date.strftime("%d/%m/%Y %H:%M:%S"),
                        },
                },
                'my_results': [
                    {
                        'metric': {'id': self.metric1.id, 'title': 'Metric 1', 'description': 'Metric Description 1'},
                        'score': 0.5,
                    }
                ],
            },
            'all_results': [
                {
                    'student': {'id': self.student1.id, 'user': {'email': 'jm@ua.pt', 'nmec': 102932, 'name': 'João Mário'}},
                    'results': [
                                    {
                                        'date': self.result1.date.strftime("%d/%m/%Y %H:%M:%S"),
                                        'score': 0.5
                                    },
                                ],
                },
                {
                    'student': {'id': self.student2.id, 'user': {'email': 'rs@ua.pt', 'nmec': 102933, 'name': 'Rafa Silva'}},
                    'results': [

                                ],
                },
            ],
            'submission': {
                'id': self.code_submission1.id,
                'file_name_result': 'result.py',
                'result_submission': '/media/result.py',
                'result_submission_size': 0,
                'result_submission_date': self.code_submission1.result_submission_date.strftime("%d/%m/%Y %H:%M:%S"),
                'file_name_code': 'code.py',
                'code_submission': '/media/code.py',
                'code_submission_size': 0,
                'code_submission_date': self.code_submission1.code_submission_date.strftime("%d/%m/%Y %H:%M:%S"),
            },
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)


    def test_student_assignments_serializer(self):
        # Serialize
        serializer = StudentAssignmentsSerializer(instance={
            'exercises': [self.exercise],
            'classes': [self.class_],
        })

        # Create expected data
        expected_data = {
            'assignments': [
                {
                    'id': self.exercise.id,
                    'title': 'Exercise 1',
                    'subtitle': 'Subtitle 1',
                    'publish_date': self.exercise.publish_date.strftime("%d/%m/%Y %H:%M:%S"),
                    'deadline': self.exercise.deadline.strftime("%d/%m/%Y %H:%M:%S"),
                    'limit_of_attempts': 3,
                    'visibility': False,
                    'students_class': {
                        'id': self.class_.id,
                        'name': 'Class 1',
                    },
                    'num_answers': 2,
                },
            ],
            'classes': [
                {
                    'id': self.class_.id,
                    'name': 'Class 1',
                }
            ]
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)

    
    def test_professor_create_exercise_get_serializer(self):
        # Serialize
        serializer = ProfessorCreateExerciseGETSerializer(instance={
            'metrics': [self.metric1, self.metric2],
            'classes': [self.class_, self.class2],
        })

        # Create expected data
        expected_data = {
            'metrics': [
                {
                    'id': self.metric1.id,
                    'title': 'Metric 1',
                    'description': 'Metric Description 1',
                },
                {
                    'id': self.metric2.id,
                    'title': 'Metric 2',
                    'description': 'Metric Description 2',
                },
            ],
            'classes': [
                {
                    'id': self.class_.id,
                    'name': 'Class 1',
                },
                {
                    'id': self.class2.id,
                    'name': 'Class 2',
                },
            ],
        }

        # Assert
        self.assertEqual(serializer.data, expected_data)
        







