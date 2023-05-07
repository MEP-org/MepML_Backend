from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentClassSerializer
from MepML.models import Class
# from app.security import *


def get_class_info(request, student_id, class_id):
    classes = Class.objects.filter(id = class_id)
    serializer = StudentClassSerializer(classes)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, student_id, class_id=None):
    try:        
        return get_class_info(request, student_id, class_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
