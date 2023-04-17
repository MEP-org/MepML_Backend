from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ExerciseSerializer, ExercisePreviewSerializer
from MepML.models import Exercise, Class, CodeSubmission
# from app.security import *


def get_exercises(request, prof_id):
    prof_exercises = Exercise.objects.filter(created_by=prof_id)
    prof_classes = Class.objects.filter(created_by=prof_id)
    response = {"exercises": [], "prof_classes": [{"id": cls.id, "name": cls.name} for cls in prof_classes]}
    serializer_data = ExercisePreviewSerializer(prof_exercises, many=True).data
    for ex in serializer_data:
        ex["num_answers"] = CodeSubmission.objects.filter(exercise=ex["id"]).count()
        response["exercises"].append(ex)
    return Response(response, status=status.HTTP_200_OK)


def post_exercise(request):
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id=None):
    try:
        if request.method == 'GET':
            return get_exercises(request, prof_id)
        elif request.method == 'POST':
            return post_exercise(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
