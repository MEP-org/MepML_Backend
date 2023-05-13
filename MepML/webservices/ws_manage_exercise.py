from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorExerciseSerializer, ExercisePostSerializer
from MepML.models import Exercise, Dataset, Result, Class, Professor
from django.core.files import File
# from app.security import *
import requests


def get_exercise(request, prof_id, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    ranking = Result.objects.filter(exercise=exercise_id).order_by('-score')
    class_ = exercise.students_class
    students = class_.students.all()
    serializer = ProfessorExerciseSerializer(instance={
        'exercise': exercise,
        'exercise_class_students': students, 
        'results': ranking
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


def put_exercise(request, prof_id, exercise_id):
    data_ = request.data.copy()
    data_['created_by'] = prof_id

    if 'test_dataset' in request.FILES:
        x_column_file = open(request.FILES['test_dataset'].name, "w+")
        y_column_file = open(request.FILES['test_dataset'].name[:-4] + "_y.csv", "w+")
        reading_header = True
        for line in request.FILES['test_dataset']:
            line = line.decode("utf-8") 
            if reading_header:
                reading_header = False
                continue
            x_column_file.write("".join(line.strip().split(",")[:-1]) + "\n")
            y_column_file.write(line.strip().split(",")[-1] + "\n")
        django_file_x = File(x_column_file)
        django_file_y = File(y_column_file)

        dataset = Dataset.objects.create(
            train_name = request.FILES['train_dataset'].name,
            train_dataset = request.FILES['train_dataset'],
            train_size = request.FILES['train_dataset'].size,
            test_name = request.data['test_dataset'].name,
            test_dataset = django_file_x,
            test_size = django_file_x.size,
            test_ground_truth_name = django_file_x.name,
            test_ground_truth_file = django_file_y
        )
        x_column_file.close()
        y_column_file.close()
        data_['dataset'] = dataset.id
    else:
        data_['dataset'] = Exercise.objects.get(id=exercise_id).dataset.id

    existent_exercise = Exercise.objects.get(id=exercise_id)
    serializer = ExercisePostSerializer(existent_exercise, data=data_)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    exercise.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id, exercise_id):
    try:
        if request.method == 'GET':
            return get_exercise(request, prof_id, exercise_id)
        elif request.method == 'PUT':
            return put_exercise(request, prof_id, exercise_id)
        elif request.method == 'DELETE':
            return delete_exercise(request, exercise_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
