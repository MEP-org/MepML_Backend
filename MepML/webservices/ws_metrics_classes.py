from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorCreateExerciseGETSerializer
from MepML.models import Class, Metric
# from app.security import *


def get_metrics_classes(request, prof_id):

    all_metrics = Metric.objects.all()
    classes = Class.objects.filter(created_by__id = prof_id)

    serializer = ProfessorCreateExerciseGETSerializer(instance={
        'metrics': all_metrics,
        'classes': classes
    })

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id=None):
    try:
        return get_metrics_classes(request, prof_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)