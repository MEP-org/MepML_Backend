from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentClassesSerializer
from MepML.models import Class
# from app.security import *


def get_classes(request, student_id):
    classes = Class.objects.filter(students__id=student_id)
    serializer = StudentClassesSerializer(classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, student_id):
    try:        
        return get_classes(request, student_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)