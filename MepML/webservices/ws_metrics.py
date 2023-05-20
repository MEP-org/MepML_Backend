from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorMetricsSerializer, ProfessorMetricPostSerializer
from MepML.models import Metric
from MepML.utils.sandbox import Sandbox
# from app.security import *


def get_metrics(request, prof_id):
    my_metrics = Metric.objects.filter(created_by=prof_id)
    other_metrics = Metric.objects.filter(created_by=None)
    serializer = ProfessorMetricsSerializer(instance={
        'my_metrics': my_metrics,
        'other_metrics': other_metrics
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_metric(request, prof_id):
    #prevent creation of default metrics
    if request.data["title"] in ["Accuracy", "Precision", "Recall", "F1", "MCC", "MAE", "MSE", "R2"]:
        return Response({"error": "metric cannot have that title"}, status=status.HTTP_400_BAD_REQUEST)
    data_ = request.data.copy()
    data_['created_by'] = prof_id

    serializer = ProfessorMetricPostSerializer(data=data_)
    if serializer.is_valid():
        source = request.FILES["metric_file"].read().decode("utf-8")
        try:
            Sandbox.run(source, [1, 0, 1], [1, 1, 1])
        except Exception as e:
            return Response({"error": "Invalid metric => " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id=None):
    try:
        if request.method == 'GET':
            return get_metrics(request, prof_id)
        elif request.method == 'POST':
            return post_metric(request, prof_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
