from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorClassesSerializer, ProfessorClassPostSerializer
from MepML.models import Class, Student
# from app.security import *


def get_classes(request, prof_id):
    classes = Class.objects.filter(created_by=prof_id)
    serializer = ProfessorClassesSerializer(classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_class(request, prof_id):
    request_copy = request.data.copy()
    request_copy['created_by'] = prof_id

    students = [int(i) for i in request_copy['students'].split(",") if i.isdigit()]
    request_copy.pop('students', None)

    serializer = ProfessorClassPostSerializer(data=request_copy)
    if serializer.is_valid():
        serializer.save()

        # Get class object
        class_ = Class.objects.get(id=serializer.data["id"])

        # Add students to class and save
        students = Student.objects.filter(id__in=students)
        class_.students.set(students)
        class_.save()

        return Response({"Success": "Class Successfully Created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id=None):
    try:
        if request.method == 'GET':
            return get_classes(request, prof_id)
        elif request.method == 'POST':
            return post_class(request, prof_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
