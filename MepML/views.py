from django.utils.timezone import make_aware
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from MepML.models import *
from MepML.serializers import *

# Create your views here.
def invalid_data_dict():
    return {"error": "Invalid data"}


# This is only a test 
# Return all professors
@api_view(["GET"])
def insert_data(request):
    # Create Professor
    user = User.objects.create_user(nmec=102534, name="Rafael Gonçalves", email="rfg@ua.pt")

    professor = Professor.objects.create(user=user)

    # Create Students
    user1 = User.objects.create_user(nmec=654321, name="João Mário", email="jm@ua.pt")
    student1 = Student.objects.create(user=user1)

    user2 = User.objects.create_user(nmec=987654, name="Rafa Silva", email="rs@ua.pt")
    student2 = Student.objects.create(user=user2)

    # Create class
    class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
    class_.students.add(student1)
    class_.students.add(student2)

    # Create Metric
    metric = Metric.objects.create(id=1, title="Metric 1", description="Metric Description 1", metric_file="metric_OOUSUjUM", created_by=professor)

    # Create Dataset
    dataset = Dataset.objects.create(train_name="train", train_dataset="train_MGArrll.csv", train_size=1, 
                                     test_name="test", test_dataset="test_oJHxflz.csv", test_size=1,
                                     test_ground_truth_name="test_y", test_ground_truth_file="test_oJHxflz.csv")

    # Create Exercise
    exercise = Exercise.objects.create(
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

    # Create Exercise
    exercise2 = Exercise.objects.create(
        title="Exercise 2",
        subtitle="Subtitle 2",
        description="DescriptionMD 2",
        evaluation="EvaluationMD 2",
        deadline= make_aware(datetime.datetime(2098, 12, 10, 12, 0, 0)),
        limit_of_attempts=3,
        visibility=True,
        students_class=class_,
        dataset=dataset,
        created_by=professor
    )
    exercise2.metrics.add(metric)

    # Create Exercise
    exercise3 = Exercise.objects.create(
        title="Exercise 3",
        subtitle="Subtitle 3",
        description="DescriptionMD 3",
        evaluation="EvaluationMD 3",
        deadline= make_aware(datetime.datetime(1994, 12, 10, 12, 0, 0)),
        limit_of_attempts=3,
        visibility=True,
        students_class=class_,
        dataset=dataset,
        created_by=professor
    )
    exercise3.metrics.add(metric)

    # Create CodeSubmission
    code_submission1 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=exercise, student=student1)
    code_submission2 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=exercise, student=student2)
    code_submission3 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=exercise2, student=student1)
    code_submission4 = CodeSubmission.objects.create(file_name_result="result.py", result_submission="result.py", file_name_code="code.py", code_submission="code.py", exercise=exercise3, student=student1)

    # Create Result
    result1 = Result.objects.create(score=0.5, student=student1, exercise=exercise, metric=metric)
    result2 = Result.objects.create(score=0.6, student=student1, exercise=exercise2, metric=metric)
    result3 = Result.objects.create(score=0.7, student=student1, exercise=exercise3, metric=metric)
    result10 = Result.objects.create(score=0.9, student=student2, exercise=exercise, metric=metric)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def apitest(request):
    #usefull for testing
    return Response(status=status.HTTP_200_OK)
