from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import PublicExercisesSerializer
from MepML.models import Exercise, Professor
# from app.security import *


def get_all_public(request):
    exercises = Exercise.objects.filter(created_by=3)
    professors = Professor.objects.all()
    serializer = PublicExercisesSerializer(instance={
        'exercises': exercises,
        'professors': professors,
    })
    print("h3", serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request):
    try:        
        return get_all_public(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)