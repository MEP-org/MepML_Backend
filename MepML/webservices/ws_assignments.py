from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentAssignmentsSerializer
from MepML.models import Exercise, Class, Exercise
# from app.security import *


def get_assignments(request, student_id):
    classes = Class.objects.filter(students__id = student_id)
    exercises = Exercise.objects.filter(students_class__in = classes)
    serializer = StudentAssignmentsSerializer(instance={
        'exercises': exercises,
        'classes': classes
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, student_id=None):
    try:
        return get_assignments(request, student_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)