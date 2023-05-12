from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MepML.models import Student
from MepML.serializers import StudentSerializer



def get_users_by_nmec(request):
    # students = Student.objects.filter(user_nmec__in=users_nmec.split(','))
    nmecs = request.GET.get("nmecs", "").split(",")
    nmecs = [int(nmec.strip()) for nmec in nmecs]

    students = Student.objects.filter(user__nmec__in=nmecs)

    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request):
    try:        
        return get_users_by_nmec(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)