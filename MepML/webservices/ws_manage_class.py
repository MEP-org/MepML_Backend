from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorClassSerializer, ProfessorClassPostSerializer
from MepML.models import Class, Student
# from app.security import *


def get_class(request, class_id):
    cls = Class.objects.get(id=class_id)
    serializer = ProfessorClassSerializer(cls)
    return Response(serializer.data, status=status.HTTP_200_OK)


def put_class(request, prof_id, class_id):
    print(request.data)
    request_copy = request.data.copy()
    request_copy['created_by'] = prof_id

    print(request_copy.get('students'))

    students = [int(i) for i in request_copy.get('students').split(',') if i.isdigit()]
    request_copy.pop('students', None)
    
    cls = Class.objects.get(id=class_id)

    serializer = ProfessorClassPostSerializer(cls, data=request_copy)
    if serializer.is_valid():
        serializer.save()

        # Get class object
        class_ = Class.objects.get(id=serializer.data["id"])

        # Add students to class and save
        students = Student.objects.filter(id__in=students)
        class_.students.set(students)
        class_.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_class(request, class_id):
    cls = Class.objects.get(id=class_id)
    cls.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id, class_id):
    try:
        if request.method == 'GET':
            return get_class(request, class_id)
        elif request.method == 'PUT':
            return put_class(request, prof_id, class_id)
        elif request.method == 'DELETE':
            return delete_class(request, class_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
