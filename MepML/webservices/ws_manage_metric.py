from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorMetricPostSerializer
from MepML.models import Metric
# from app.security import *


def get_metric(request, metric_id):
    metric = Metric.objects.get(id=metric_id)
    serializer = ProfessorMetricPostSerializer(metric)
    return Response(serializer.data, status=status.HTTP_200_OK)


def put_metric(request, metric_id):
    metric = Metric.objects.get(id=metric_id)
    serializer = ProfessorMetricPostSerializer(metric, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_metric(request, metric_id):
    metric = Metric.objects.get(id=metric_id)
    metric.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id, metric_id):
    try:
        if request.method == 'GET':
            return get_metric(request, metric_id)
        elif request.method == 'PUT':
            return put_metric(request, metric_id)
        elif request.method == 'DELETE':
            return delete_metric(request, metric_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
