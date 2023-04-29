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
                                     test_name="test", test_dataset="test_oJHxflz.csv", test_size=1)

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
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def create_default_metric(request):
    Metric.objects.create(id=2, title="Accuracy", description="This is a well known metric", 
                          metric_file="metric_xZojFJp", created_by=None)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_class(request):
    #Check if all necessary data is present
    if "name" not in request.data or "created_by" not in request.data or "image" not in request.FILES:
        return Response(invalid_data_dict, status=status.HTTP_400_BAD_REQUEST)

    #Check if professor exists
    try:
        professor = Professor.objects.get(id=request.data["created_by"])
    except Professor.DoesNotExist:
        return Response({"error": "Invalid Professor"}, status=status.HTTP_404_NOT_FOUND)

    try:
        Class.objects.create(
            name=request.data["name"],
            created_by=professor,
            image=request.FILES["image"]
        )
    except(KeyError, ValueError, TypeError):
        return Response(invalid_data_dict, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_class(request, class_id):
    try:
        class_ = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return Response({"error": "Invalid Class"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassSerializer(class_)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["PUT"])
def update_class(request, class_id):
    try:
        class_ = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return Response({"error": "Invalid Class"}, status=status.HTTP_404_NOT_FOUND)

    if "name" in request.data:
        class_.name = request.data["name"]
    if "image" in request.FILES:
        class_.image = request.FILES["image"]
    if "students" in request.data:
        for student in request.data["students"]:
            try:
                student = Student.objects.get(nmec=student.nmec)
            except Student.DoesNotExist:
                try:
                    user = User.objects.get(email=student.email)
                except User.DoesNotExist:
                    # if user does not exist, we have to create it
                    ## TODO when idp is implemented, we have to check if student is a valid email from the student
                    user = User.objects.create_user(
                        username=student.email,
                        email=student.email,
                    )
                student = Student.objects.create(
                        user=user,
                        nmec=student.nmec,
                        name=student.name,
                        email=student.email
                    )
            class_.students.add(student)
                
    try:
        class_.save()
    except(KeyError, ValueError, TypeError):
        return Response(invalid_data_dict, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
