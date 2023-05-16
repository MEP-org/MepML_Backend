from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import LoginUserSerializer
from MepML.models import Student, Professor, User
from djangoMepML import authentication

def singin(request):
    fire_state, pyromancer_id = authentication.fire_in(
            request.POST["email"], 
            request.POST["password"]
            )
    print(fire_state)
    try:
        user = User.objects.get(firebase_uuid=pyromancer_id)
    except:
        print("No such User")
        return Response(status=status.HTTP_404_NOT_FOUND)

    # may be a student or a professor
    try:
        person = Student.objects.get(user__firebase_uuid=pyromancer_id)
        LoginUserSerializer.Meta.model = Student
    except:
        print("It's not a student")  
    try:
        person = Professor.objects.get(user__firebase_uuid=pyromancer_id)
        LoginUserSerializer.Meta.model = Professor
    except:
        print("It's not a professor")  
    
    #print(person)
    serializer = LoginUserSerializer(person)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def handle(request):
    try:        
        return singin(request)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)