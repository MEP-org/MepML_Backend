from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentHomeSerializer
from MepML.models import Student
# from app.security import *


def home(request, student_id):
    print("Here")
    student = Student.objects.get(id=student_id)
    print(student)
    serializer = StudentHomeSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, student_id):
    try:        
        return home(request, student_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)