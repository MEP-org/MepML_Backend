from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorExerciseSerializer, ExercisePostSerializer
from MepML.models import Exercise, Dataset, Result
# from app.security import *


def get_exercise(request, prof_id, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    ranking = Result.objects.filter(exercise=exercise_id).order_by('-score')
    serializer = ProfessorExerciseSerializer(instance={
        'exercise': exercise,
        'results': ranking
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


def put_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    dataset = Dataset.objects.create(
        train_name = request.FILES['train_dataset'].name,
        train_dataset = request.FILES['train_dataset'],
        test_name = request.data['test_dataset'].name,
        test_dataset = request.FILES['test_dataset']
    )
    data_ = request.data
    data_['dataset'] = dataset.id
    serializer = ExercisePostSerializer(exercise, data=data_)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
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
            return put_exercise(request, exercise_id)
        elif request.method == 'DELETE':
            return delete_exercise(request, exercise_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
