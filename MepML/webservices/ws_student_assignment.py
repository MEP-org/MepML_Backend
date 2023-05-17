from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import StudentAssignmentSerializer, StudentAssignmentCodeSubmissionPostSerializer, \
    StudentResultCodeSubmissionSerializer
from MepML.models import Exercise, Result, Student, CodeSubmission
from django.core.files.storage import default_storage
import pandas as pd
from MepML.utils.sandbox import Sandbox
from django.utils import timezone
# from app.security import *


def get_assignment(request, student_id, assignment_id):
    assignment = Exercise.objects.get(id=assignment_id)
    my_results = Result.objects.filter(student__id=student_id, exercise__id=assignment_id)
    all_results = Result.objects.filter(exercise__id=assignment_id)
    submission = CodeSubmission.objects.filter(student__id=student_id, exercise__id=assignment_id).last()

    #Get all students from the class
    class_ = assignment.students_class
    assignment_class_students = class_.students.all()

    serializer = StudentAssignmentSerializer(instance={
        'assignment': {
            'exercise': assignment,
            'my_results': my_results,
        },
        'assignment_class_students': assignment_class_students,
        'all_results': all_results,
        'submission': submission,
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


def post_solution(request, student_id, assignment_id):
    submission_data = request.data
    submission_data["student"] = student_id
    submission_data["exercise"] = assignment_id
    submission = CodeSubmission.objects.filter(student__id=student_id, exercise__id=assignment_id).first()
    if not submission:
        submission_serializer = StudentAssignmentCodeSubmissionPostSerializer(data=submission_data)
    else:
        if "result_submission" in request.FILES:
            submission_data["result_submission_date"] = timezone.now()
        if "code_submission" in request.FILES:
            submission_data["code_submission_date"] = timezone.now()
        submission_data["quantity_of_submissions"] = submission.quantity_of_submissions + 1
        submission_serializer = StudentAssignmentCodeSubmissionPostSerializer(submission, data=submission_data)

    if submission_serializer.is_valid():
        assignment = Exercise.objects.get(id=assignment_id)
        # Check if the deadline has passed
        if assignment.deadline < timezone.now():
            return Response({"error": "The deadline has passed"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the student has reached the limit of attempts
        if submission and assignment.limit_of_attempts and assignment.limit_of_attempts < submission_data["quantity_of_submissions"]:
            return Response({"error": "You have reached the limit of attempts"}, status=status.HTTP_400_BAD_REQUEST)
        
        metrics = assignment.metrics.all()
        test_dataset_filename = assignment.dataset.test_ground_truth_file.name
        y_true = pd.read_csv(default_storage.open(test_dataset_filename), header=None)
        y_pred = pd.read_csv(request.FILES['result_submission'], header=None)

        if y_true.shape != y_pred.shape:
            return Response({"error": "Invalid submission => y_true and y_pred must have the same shape"},
                            status=status.HTTP_400_BAD_REQUEST)

        results_data = []
        scores = {}

        for metric in metrics:
            src = default_storage.open(metric.metric_file.name).read().decode("utf-8")
            src += f"\nx = score(y_true, y_pred)"
            score = Sandbox.run(src, y_true, y_pred)
            result = Result.objects\
                .filter(student__id=student_id, exercise__id=assignment_id, metric__id=metric.id)\
                .first()
            result_data = {
                "student": student_id,
                "exercise": assignment_id,
                "metric": metric.id,
                "score": score
            }
            scores[metric.title] = score

            if result:
                result_serializer = StudentResultCodeSubmissionSerializer(result, data=result_data)
                if not result_serializer.is_valid():
                    return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                result_serializer.save()
                continue

            results_data.append(result_data)

        results = StudentResultCodeSubmissionSerializer(data=results_data, many=True)
        if not results.is_valid():
            return Response(results.errors, status=status.HTTP_400_BAD_REQUEST)
        submission_serializer.save()
        results.save()
        return Response(scores, status=status.HTTP_201_CREATED)

    return Response(submission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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