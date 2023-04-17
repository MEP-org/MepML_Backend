from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ExerciseSerializer, StudentSerializer
from MepML.models import Exercise, Class, Result
# from app.security import *


def get_exercise(request, prof_id, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    prof_classes = Class.objects.filter(created_by=prof_id)
    ranking = Result.objects.filter(exercise=exercise_id).order_by('-score')
    response = {
        "exercise": ExerciseSerializer(exercise).data,
        "prof_classes": [{"id": cls.id, "name": cls.name} for cls in prof_classes],
        "ranking": [{"id": result.student.id, "name": result.student.name} for result in ranking]
    }
    return Response(response, status=status.HTTP_200_OK)


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
            return get_exercise(request, prof_id, exercise_id)
        elif request.method == 'PUT':
            return put_exercise(request, exercise_id)
        elif request.method == 'DELETE':
            return delete_exercise(request, exercise_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
