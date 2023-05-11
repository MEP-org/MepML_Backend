from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import LoginUserSerializer
from MepML.models import Student, Professor, User


def singup(request):
    firebase_id = request.POST["token"]
    try:
        User.objects.get(firebase_uuid=firebase_id)
    except:
        print("No student")

    user = User.objects.create(
        nmec=request.POST["nmec"], 
        name=request.POST["name"], 
        email=request.POST["email"],
        firebase_uuid=firebase_id
    )
    if request.POST["user_type"] == "professor":
        Professor.objects.create(user=user)
        professor = Professor.objects.get(user__firebase_uuid=firebase_id)    
        LoginUserSerializer.Meta.model = Professor
        serializer = LoginUserSerializer(professor)
    if request.POST["user_type"] == "student":
        Student.objects.create(user=user)
        student = Student.objects.get(user__firebase_uuid=firebase_id)    
        LoginUserSerializer.Meta.model = Student
        serializer = LoginUserSerializer(student)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def handle(request):
    try:        
        return singup(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)