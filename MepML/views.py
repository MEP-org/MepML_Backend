import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from MepML.models import *
from MepML.serializers import *

# Create your views here.
def invalid_data_dict():
    return {"error": "Invalid data"}


# This is only a test 
# Return all professors
@api_view(["GET"])
def getAll(request):
    todos = Professor.objects.all()
    serializer = ProfessorSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_class(request):
    #Check if all necessary data is present
    if "name" not in request.data or "created_by" not in request.data or "image" not in request.FILES:
        return Response(invalid_data_dict, status=status.HTTP_400_BAD_REQUEST)

    #Check if professor exists
    try:
        professor = Professor.objects.get(id=request.data["created_by"])
    except Professor.DoesNotExist:
        return Response({"error": "Invalid Professor"}, status=status.HTTP_404_NOT_FOUND)

    try:
        Class.objects.create(
            name=request.data["name"],
            created_by=professor,
            image=request.FILES["image"]
        )
    except(KeyError, ValueError, TypeError):
        return Response(invalid_data_dict, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)

@api_view(["GET"])
def get_class(request, class_id):
    try:
        class_ = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return Response({"error": "Invalid Class"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassSerializer(class_)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["PUT"])
def update_class(request, class_id):
    try:
        class_ = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return Response({"error": "Invalid Class"}, status=status.HTTP_404_NOT_FOUND)

    if "name" in request.data:
        class_.name = request.data["name"]
    if "image" in request.FILES:
        class_.image = request.FILES["image"]
    if "students" in request.data:
        for student in request.data["students"]:
            try:
                student = Student.objects.get(nmec=student.nmec)
            except Student.DoesNotExist:
                try:
                    user = User.objects.get(email=student.email)
                except User.DoesNotExist:
                    # if user does not exist, we have to create it
                    ## TODO when idp is implemented, we have to check if student is a valid email from the student
                    user = User.objects.create_user(
                        username=student.email,
                        email=student.email,
                    )
                student = Student.objects.create(
                        user=user,
                        nmec=student.nmec,
                        name=student.name,
                        email=student.email
                    )
            class_.students.add(student)
                
    try:
        class_.save()
    except(KeyError, ValueError, TypeError):
        return Response(invalid_data_dict, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)