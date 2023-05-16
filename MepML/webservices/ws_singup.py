from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import LoginUserSerializer
from MepML.models import Student, Professor, User
from djangoMepML import authentication


def singup(request):
    try:
        User.objects.get(nmec=request.POST["nmec"])
        return Response({"error": "nmec exist"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        print("nmec exist")

    try:
        User.objects.get(email=request.POST["email"])
        return Response({"error": "email exist"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        print("email exists")

    fire_state, pyromancer_id = authentication.crate_new_pyromancer(
                                request.POST["email"], 
                                request.POST["password"]
    )
    print(fire_state)
    try:
        User.objects.get(firebase_uuid=pyromancer_id)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        print("No student")

    user = User.objects.create(
        nmec=request.POST["nmec"], 
        name=request.POST["name"], 
        email=request.POST["email"],
        firebase_uuid=pyromancer_id
    )
    if request.POST["user_type"] == "professor":
        Professor.objects.create(user=user)
        professor = Professor.objects.get(user__firebase_uuid=pyromancer_id)    
        LoginUserSerializer.Meta.model = Professor
        serializer = LoginUserSerializer(professor)
    if request.POST["user_type"] == "student":
        Student.objects.create(user=user)
        student = Student.objects.get(user__firebase_uuid=pyromancer_id)    
        LoginUserSerializer.Meta.model = Student
        serializer = LoginUserSerializer(student)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def handle(request):
    try:        
        return singup(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
