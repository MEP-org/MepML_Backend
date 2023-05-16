from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import PublicExerciseSerializer
from MepML.models import Exercise, Class, Exercise
# from app.security import *


def get_assignment_info(request, exercise_id):
    exercise = Exercise.objects.get(id = exercise_id)

    if exercise.visibility == False:
        return Response({'error': 'Exercise is not public'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = PublicExerciseSerializer(exercise)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, exercise_id=None):
    try:
        return get_assignment_info(request, exercise_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)