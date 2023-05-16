from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import LoginUserSerializer
from MepML.models import Student, Professor, User

def token(request):
    person = None
    try:
        person = Student.objects.get(user__firebase_uuid=request.POST["token"])
        LoginUserSerializer.Meta.model = Student

    except:
        print("It's not a student")  
    try:
        person = Professor.objects.get(user__firebase_uuid=request.POST["token"])
        LoginUserSerializer.Meta.model = Professor
    except:
        print("It's not a professor")  
    
    if not person:
        return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = LoginUserSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def handle(request):
    try:        
        return token(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)