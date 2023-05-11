from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentAssignmentSerializer, StudentAssignmentCodeSubmissionPostSerializer, \
    StudentResultCodeSubmissionSerializer
from MepML.models import Exercise, Result, Student, CodeSubmission
from django.core.files.storage import default_storage
import pandas as pd
from MepML.utils.sandbox import Sandbox
# from app.security import *


def get_assignment(request, student_id, assignment_id):

    assignment = Exercise.objects.get(id=assignment_id)
    my_results = Result.objects.filter(student__id=student_id).filter(exercise__id=assignment_id)
    all_results = Result.objects.filter(exercise__id=assignment_id)
    # submission = CodeSubmission.objects.filter(student__id=student_id).filter(exercise__id=assignment_id)
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


def post_solution(request, student_id, assignment_id):
    submission_data = request.data
    submission_data["student"] = student_id
    submission_data["exercise"] = assignment_id
    serializer = StudentAssignmentCodeSubmissionPostSerializer(data=submission_data)

    if serializer.is_valid():
        submission = serializer.save()
        metrics = submission.exercise.metrics.all()
        y_pred = pd.read_csv(request.FILES['result_submission'])
        test_dataset_filename = submission.exercise.dataset.test_ground_truth_file.name
        y_true = pd.read_csv(default_storage.open(test_dataset_filename))

        results = []

        for metric in metrics:
            metric_filename = f"metrics/{metric.metric_file.name}.py"
            src = default_storage.open(metric_filename).read().decode("utf-8")
            metric_name = src[src.find("def") + 4:src.find("(")]
            src += f"\nx = {metric_name}(y_true, y_pred)"
            score = Sandbox.run(src, [1, 0, 1], [1, 1, 1])
            results.append({
                "student": student_id,
                "exercise": assignment_id,
                "metric": metric.id,
                "score": score
            })

        serializer = StudentResultCodeSubmissionSerializer(data=results, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, student_id, assignment_id=None):
    try:
        if request.method == 'GET':
            return get_assignment(request, student_id, assignment_id)
        elif request.method == 'POST':
            return post_solution(request, student_id, assignment_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)