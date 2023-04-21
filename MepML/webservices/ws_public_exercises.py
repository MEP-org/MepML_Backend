from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from MepML.serializers import PublicExercisesSerializer
from MepML.models import Dataset, Exercise, Professor
# from app.security import *


def get_all_public(request):
    if "order" in request.GET:
        order = None
        if "recent" == request.GET["order"].lower():
            order = "publish_date"
        if "oldest" == request.GET["order"].lower():
            order = "-publish_date"
        if "alphabetic up" == request.GET["order"].lower():
            order = "title"
        if "alphabetic down" == request.GET["order"].lower():
            order = "-title"
        if "size up" == request.GET["order"].lower():
            order = "dataset__train_size"
        if "size down" == request.GET["order"].lower():
            order = "-dataset__train_size"

        exercises = Exercise.objects.all().order_by(order)
    else:
        exercises = Exercise.objects.all()
    professors = Professor.objects.all()

    if "title" in request.GET:
        exercises = exercises.filter(title__icontains = request.GET["title"])

    if "prof" in request.GET:
        exercises = exercises.filter(created_by = request.GET["prof"])

    if "max_size" in request.GET:
        exercises = exercises.filter(dataset__in= Dataset.objects.filter(train_size__lte=request.GET["max_size"]))

    if "min_size" in request.GET:
        exercises = exercises.filter(dataset__in= Dataset.objects.filter(train_size__gte=request.GET["min_size"]))

    paginator = PageNumberPagination()
    paginator.page_size = 6

    exercises_paginados = paginator.paginate_queryset(exercises, request)

    serializer = PublicExercisesSerializer(instance={
        'exercises': exercises_paginados,
        'professors': professors,
    })
    paginated_response = paginator.get_paginated_response(serializer.data)
    return Response(paginated_response.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request):
    try:        
        return get_all_public(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)