from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ExerciseSerializer
from MepML.models import Exercise
# from app.security import *


def get_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    serializer = ExerciseSerializer
    return Response(serializer.data, status=status.HTTP_200_OK)


def put_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    serializer = ExerciseSerializer(exercise, data=request.data)
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
            return get_exercise(request, exercise_id)
        elif request.method == 'PUT':
            return put_exercise(request, exercise_id)
        elif request.method == 'DELETE':
            return delete_exercise(request, exercise_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
