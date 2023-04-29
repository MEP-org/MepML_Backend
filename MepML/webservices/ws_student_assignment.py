from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentAssignmentSerializer
from MepML.models import Exercise, Result, CodeSubmission
# from app.security import *


def get_assignment(request, student_id, assignment_id):
    
    assignment = Exercise.objects.get(id=assignment_id)
    my_results = Result.objects.filter(student__id=student_id).filter(exercise__id=assignment_id)
    all_results = Result.objects.filter(exercise__id=assignment_id)
    #submission = CodeSubmission.objects.filter(student__id=student_id).filter(exercise__id=assignment_id)
    submission = CodeSubmission.objects.get(id=1)

    print(assignment, my_results, all_results, submission)

    serializer = StudentAssignmentSerializer(instance={
        'assignment': {
            'exercise': assignment,
            'my_results': my_results,
        },
        'all_results': all_results,
        'submission': submission,
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, student_id, assignment_id=None):
    try:        
        return get_assignment(request, student_id, assignment_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)