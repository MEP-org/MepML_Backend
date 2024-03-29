from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MepML.serializers import ProfessorExerciseSerializer, ExercisePostSerializer
from MepML.models import Exercise, Dataset, Result, CodeSubmission, Metric
from django.core.files import File
from django.core.files.storage import default_storage
from MepML.utils.sandbox import Sandbox
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import uuid


def get_exercise(request, prof_id, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    ranking = Result.objects.filter(exercise=exercise_id).order_by('-score')
    class_ = exercise.students_class
    students = class_.students.all()
    code_submissions = CodeSubmission.objects.filter(exercise=exercise_id)
    serializer = ProfessorExerciseSerializer(instance={
        'exercise': exercise,
        'exercise_class_students': students, 
        'results': ranking,
        'student_codes': code_submissions,
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


def put_exercise(request, prof_id, exercise_id):
    #Verify if the quantity of attempts is a valid value
    if 'quantity_of_attempts' in request.data and request.data['quantity_of_attempts'] <= 0:
        return Response({'error': 'Quantity of attempts must be greater than 0 or unlimited'}, status=status.HTTP_400_BAD_REQUEST)
    
    data_ = request.data.copy()
    data_['created_by'] = prof_id

    if 'test_dataset' in request.FILES:
        x_column_file = open(request.FILES['test_dataset'].name, "w+")
        y_column_file = open(request.FILES['test_dataset'].name[:-4] + "_y.csv", "w+")
        test_line_quant = 0
        reading_header = True
        for line in request.FILES['test_dataset']:
            line = line.decode("utf-8") 
            if reading_header:
                reading_header = False
                continue
            test_line_quant += 1
            x_column_file.write("".join(line.strip().split(",")[:-1]) + "\n")
            y_column_file.write(line.strip().split(",")[-1] + "\n")
        #django_file_x = File(x_column_file)
        #django_file_y = File(y_column_file)
        x_column_file.seek(0)
        y_column_file.seek(0)

        # Create an io.BytesIO object
        bytes_io_x = io.BytesIO()
        bytes_io_x.write(x_column_file.read().encode('utf-8'))
        bytes_io_x.seek(0)

        # Specify the desired filename and content type
        filename = request.FILES['test_dataset'].name
        content_type = 'csv/plain'  # Replace with the appropriate content type

        # Create the InMemoryUploadedFile object
        django_file_xx = InMemoryUploadedFile(
            file=bytes_io_x,
            field_name=None,
            name=filename,
            content_type=content_type,
            size=bytes_io_x.getbuffer().nbytes,
            charset=None
        )

        bytes_io_y = io.BytesIO()
        bytes_io_y.write(y_column_file.read().encode('utf-8'))
        bytes_io_y.seek(0)

        # Create the InMemoryUploadedFile object
        django_file_yy = InMemoryUploadedFile(
            file=bytes_io_y,
            field_name=None,
            name=filename,
            content_type=content_type,
            size=bytes_io_y.getbuffer().nbytes,
            charset=None
        )

        this_uuid = uuid.uuid4()
        request.FILES['train_dataset'].name = str(this_uuid) + request.FILES['train_dataset'].name
        request.FILES['test_dataset'].name = str(this_uuid) + request.FILES['test_dataset'].name
        django_file_xx.name = str(this_uuid) + django_file_xx.name

        dataset = Dataset.objects.create(
            train_name = request.FILES['train_dataset'].name,
            train_dataset = request.FILES['train_dataset'],
            train_size = request.FILES['train_dataset'].size,
            test_name = request.data['test_dataset'].name,
            test_dataset = django_file_xx,
            test_size = django_file_xx.size,
            test_ground_truth_name = django_file_xx.name,
            test_ground_truth_file = django_file_yy,
            test_line_quant = test_line_quant
        )
        x_column_file.close()
        y_column_file.close()
        data_['dataset'] = dataset.id
    else:
        data_['dataset'] = Exercise.objects.get(id=exercise_id).dataset.id
        dataset = Dataset.objects.get(id=data_['dataset'])

    existent_exercise = Exercise.objects.get(id=exercise_id)

    if 'deadline' in data_.keys():
        data_['deadline'] = data_['deadline'] + " 23:59:59"
    serializer = ExercisePostSerializer(existent_exercise, data=data_)

    if serializer.is_valid():
        serializer.save()
        new_metrics = Metric.objects.filter(id__in=data_.getlist('metrics'))
        old_metrics = existent_exercise.metrics.all()
        y_true = dataset.test_ground_truth_file.read().decode("utf-8")

        for metric in new_metrics:
            if metric not in old_metrics:
                src = default_storage.open(metric.metric_file.name).read().decode("utf-8")
                src += f"\nx = score(y_true, y_pred)"
                code_submissions = CodeSubmission.objects.filter(exercise=existent_exercise)
                for code_submission in code_submissions:
                    y_pred = code_submission.result_submission.read().decode("utf-8")
                    score = Sandbox.run(src, y_true, y_pred)
                    Result.objects.create(
                        exercise=existent_exercise,
                        student=code_submission.student,
                        score=score,
                        metric=metric
                    )

        for metric in old_metrics:
            if metric not in new_metrics:
                Result.objects.filter(exercise=existent_exercise, metric=metric).delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    exercise.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated | IsGetRequest])
def handle(request, prof_id, exercise_id):
    try:
        if request.method == 'GET':
            return get_exercise(request, prof_id, exercise_id)
        elif request.method == 'PUT':
            return put_exercise(request, prof_id, exercise_id)
        elif request.method == 'DELETE':
            return delete_exercise(request, exercise_id)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
