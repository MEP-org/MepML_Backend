from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorExercisesSerializer, ExercisePostSerializer
from MepML.models import Exercise, Class, Exercise, Dataset, Professor
from django.core.files import File
# from app.security import *

#Make post request to slack
import requests


def get_exercises(request, prof_id):
    exercises = Exercise.objects.filter(created_by=prof_id)
    prof_classes = Class.objects.filter(created_by=prof_id)
    serializer = ProfessorExercisesSerializer(instance={
        'exercises': exercises,
        'classes': prof_classes
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_exercise(request, prof_id):
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
    data_ = request.data
    data_['dataset'] = dataset.id
    data_['created_by'] = prof_id
    serializer = ExercisePostSerializer(data=data_)
    if serializer.is_valid():
        serializer.save()

        # Get exercise
        exercise = Exercise.objects.get(id=serializer.data['id'])

        # Get class name
        class_ = Class.objects.get(id=serializer.data['students_class'])

        # Get professor name
        professor = Professor.objects.get(id=serializer.data['created_by'])

        # Send message on slack
        slack_message = {
            'channel': 'bot-test',
            'message': f"*New Assignment to:* {class_.name}\n*Title:* {request.data['title']}\n{request.data['subtitle']}\n\n*ByProf:* {professor.user.name} *, due to* {exercise.deadline.strftime('%d/%m/%Y')}",
        }

        response = requests.post("http://127.0.0.1:8000/notify", json=slack_message , headers={'Content-Type': 'application/json'})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id=None):
    #try:
    if request.method == 'GET':
        return get_exercises(request, prof_id)
    elif request.method == 'POST':
        return post_exercise(request, prof_id)
    #except Exception as e:
    #    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
