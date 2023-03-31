from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from MepML.models import *
from MepML.serializers import *

# Create your views here.


# This is only a test 
# Return all professors
@api_view(["GET"])
def getAll(request):
    todos = Professor.objects.all()
    serializer = ProfessorSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)