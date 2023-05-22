from rest_framework import serializers
from MepML.models import CodeSubmission, Professor, Student, Class, Dataset, Metric, Exercise, User, Result


# ------------------------------ User Serializers ------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nmec', 'name')

# ------------------------------ Authentication Serializers ------------------------------
class LoginUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    nmec = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    def get_user_type(self, obj):
        if isinstance(obj, Student):
            return "student"
        elif isinstance(obj, Professor):
            return "professor"
        else:
            return str(type(obj))

    def get_token(self, obj):
        return obj.user.firebase_uuid
        
    def get_email(self, obj):
        return obj.user.email
    
    def get_nmec(self, obj):
        return obj.user.nmec
    
    def get_name(self, obj):
        return obj.user.name

    class Meta:
        model = None
        fields = ('id', 'token', 'user_type', 'name', 'email', 'nmec')

# ------------------------------ Student Serializers ------------------------------
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('id', 'user')


class StudentHomeSerializer(serializers.ModelSerializer):
    next_deadline = serializers.SerializerMethodField()

    #format date
    def get_next_deadline(self, obj):
        if obj.next_deadline == None:
            return None
        return obj.next_deadline.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Student
        fields = ["num_exercises", "num_submissions", "next_deadline", "next_deadline_title"]

# ------------------------------ Professor Serializers ------------------------------
class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Professor
        fields = ('id', 'user')


class PublicExercisesProfessorsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.name

    class Meta:
        model = Professor
        fields = ('id', 'name')


# ------------------------------ Class Serializers ------------------------------
class ProfessorClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Class
        fields = ('id', 'name', 'image', 'students')


class ProfessorClassesSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()

    def get_num_students(self, obj):
        return obj.students.count()

    class Meta:
        model = Class
        fields = ["id", "name", "num_students", "image"]


class ProfessorClassPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"


class StudentClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    created_by = ProfessorSerializer()

    class Meta:
        model = Class
        fields = ('id', 'name', 'created_by', 'image', 'students')


class StudentClassesSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()
    created_by = ProfessorSerializer()

    def get_num_students(self, obj):
        return obj.students.count()

    class Meta:
        model = Class
        fields = ["id", "name", "num_students", "image", "created_by"]


class SimpleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', "name"]


# ------------------------------ Metric Serializers ------------------------------
class MetricSerializer(serializers.ModelSerializer):
    created_by = ProfessorSerializer()

    class Meta:
        model = Metric
        fields = ['id', "title", "description", "created_by", "metric_file"]


class MetricOwnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', "title", "description"]


class MetricViewerSerializer(serializers.ModelSerializer):
    created_by = ProfessorSerializer()

    class Meta:
        model = Metric
        fields = ['id', "title", "description", "created_by"]


class ProfessorMetricPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = "__all__"


# ------------------------------ Dataset Serializers ------------------------------
class DatasetSerializer(serializers.ModelSerializer):
    train_upload_date = serializers.SerializerMethodField()
    test_upload_date = serializers.SerializerMethodField()
    train_name = serializers.SerializerMethodField()
    test_name = serializers.SerializerMethodField()

    #format date
    def get_train_upload_date(self, obj):
        return obj.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_test_upload_date(self, obj):
        return obj.test_upload_date.strftime("%d/%m/%Y %H:%M:%S")
    
    #format file name (36 is the size of uuid) 
    def get_train_name(self, obj):
        return obj.train_name[36:]
    
    def get_test_name(self, obj):
        return obj.test_name[36:]
    
    class Meta:
        model = Dataset
        fields = ['id', "train_name", "train_dataset", "train_upload_date", "train_size", 
                  "test_name", "test_dataset", "test_upload_date", "test_size", "test_line_quant"]


class PublicExercisesExerciseTrainingDatasetSerializer(serializers.ModelSerializer):
    train_upload_date = serializers.SerializerMethodField()
    train_name = serializers.SerializerMethodField()

    #format date
    def get_train_upload_date(self, obj):
        return obj.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")
    
    #format file name (36 is the size of uuid) 
    def get_train_name(self, obj):
        return obj.train_name[36:]
    
    class Meta:
        model = Dataset
        fields = ["train_name", "train_dataset", "train_size", "train_upload_date"]


class StudentAssignmentExerciseDatasetSerializer(serializers.ModelSerializer):
    train_upload_date = serializers.SerializerMethodField()
    test_upload_date = serializers.SerializerMethodField()
    train_name = serializers.SerializerMethodField()
    test_name = serializers.SerializerMethodField()

    #format date
    def get_train_upload_date(self, obj):
        return obj.train_upload_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_test_upload_date(self, obj):
        return obj.test_upload_date.strftime("%d/%m/%Y %H:%M:%S")
    
    #format file name (36 is the size of uuid) 
    def get_train_name(self, obj):
        return obj.train_name[36:]
    
    def get_test_name(self, obj):
        return obj.test_name[36:]

    class Meta:
        model = Dataset
        fields = ["train_name", "train_dataset", "train_size", "train_upload_date",
                  "test_name", "test_dataset", "test_size", "test_upload_date", "test_line_quant"]
        

# ------------------------------ Exercise Serializers ------------------------------
class ExerciseSerializer(serializers.ModelSerializer):
    created_by = ProfessorSerializer()
    dataset = DatasetSerializer()
    metrics = MetricSerializer(many=True)
    students_class = SimpleClassSerializer()
    publish_date = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    #format date
    def get_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_deadline(self, obj):
        return obj.deadline.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "description", "evaluation", "publish_date", "deadline", "limit_of_attempts", "visibility", "students_class", "metrics", "dataset", "created_by"]


class ExercisePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class ProfessorExercisesExerciseSerializer(serializers.ModelSerializer):
    students_class = ProfessorClassesSerializer()
    publish_date = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    #format date
    def get_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_deadline(self, obj):
        return obj.deadline.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "deadline", "limit_of_attempts", "visibility", "students_class", "num_answers"]


class PublicExercisesExerciseSerializer(serializers.ModelSerializer):
    created_by = PublicExercisesProfessorsSerializer()
    dataset = PublicExercisesExerciseTrainingDatasetSerializer()
    publish_date = serializers.SerializerMethodField()

    #format date
    def get_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "created_by", "dataset"]


class StudentAssignmentExerciseSerializer(serializers.ModelSerializer):
    dataset = StudentAssignmentExerciseDatasetSerializer()
    metrics = MetricOwnSerializer(many=True)
    students_class = SimpleClassSerializer()
    publish_date = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    #format date
    def get_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_deadline(self, obj):
        return obj.deadline.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "deadline", "limit_of_attempts", "visibility", 
                  "students_class", "metrics", "description", "evaluation", "dataset"]
        

class StudentAssignmentsExerciseSerializer(serializers.ModelSerializer):
    students_class = SimpleClassSerializer()
    publish_date = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()

    #format date
    def get_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_deadline(self, obj):
        return obj.deadline.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "deadline", "limit_of_attempts", 
                  "visibility", "students_class", "num_answers"]
        

class PublicExerciseSerializer(serializers.ModelSerializer):
    dataset = PublicExercisesExerciseTrainingDatasetSerializer()
    publish_date = serializers.SerializerMethodField()

    #format date
    def get_publish_date(self, obj):
        return obj.publish_date.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "description", "publish_date", "visibility", "dataset"]

        


# ------------------------------ Result Serializers ------------------------------
class ProfessorExerciseResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    metric = MetricSerializer()
    date = serializers.SerializerMethodField()

    #format date
    def get_date(self, obj):
        return obj.date.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Result
        fields = ['id', "score", "date", "student", "metric"]


class StudentAssignmentExerciseOwnResultsSerializer(serializers.ModelSerializer):
    metric = MetricOwnSerializer()

    class Meta:
        model = Result
        fields = ['metric', 'score']


class StudentResultCodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

# ------------------------------ CodeSubmission Serializers ------------------------------
class StudentAssignmentCodeSubmissionSerializer(serializers.ModelSerializer):
    result_submission_date = serializers.SerializerMethodField()
    code_submission_date = serializers.SerializerMethodField()
    result_submission_size = serializers.SerializerMethodField()
    code_submission_size = serializers.SerializerMethodField()
    file_name_result = serializers.SerializerMethodField()
    file_name_code = serializers.SerializerMethodField()

    #format date
    def get_result_submission_date(self, obj):
        return obj.result_submission_date.strftime("%d/%m/%Y %H:%M:%S")

    #format date
    def get_code_submission_date(self, obj):
        return obj.code_submission_date.strftime("%d/%m/%Y %H:%M:%S")
    
    #Get file size
    def get_result_submission_size(self, obj):
        return obj.result_submission.size
    
    #Get file size
    def get_code_submission_size(self, obj):
        return obj.code_submission.size
    
    #Get file size
    def get_file_name_result(self, obj):
        return obj.file_name_result[36:]
    
    #Get file size
    def get_file_name_code(self, obj):
        return obj.file_name_code[36:]
    
    class Meta:
        model = CodeSubmission
        fields = ['id', "file_name_result", "result_submission", "result_submission_size", "result_submission_date", "file_name_code", 
                  "code_submission", "code_submission_size", "code_submission_date", "quantity_of_submissions"]


class StudentAssignmentCodeSubmissionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = '__all__'




class ProfessorExerciseStudentCodeSubmissionSerializer(serializers.ModelSerializer):
    code_submission_date = serializers.SerializerMethodField()

    #format date
    def get_code_submission_date(self, obj):
        return obj.code_submission_date.strftime("%d/%m/%Y %H:%M:%S")
    
    class Meta:
        model = CodeSubmission
        fields = ["student", "file_name_code", "code_submission", "code_submission_date", "quantity_of_submissions"]


# ------------------------------ Other Serializers ------------------------------

class ProfessorMetricsSerializer(serializers.Serializer):
    my_metrics = MetricViewerSerializer(many=True)
    other_metrics = MetricViewerSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'my_metrics': data['my_metrics'],
            'other_metrics': data['other_metrics'],
        }



class ProfessorExerciseSerializer(serializers.Serializer):
    exercise = ExerciseSerializer()
    exercise_class_students = StudentSerializer(many=True)
    results = ProfessorExerciseResultSerializer(many=True)
    student_codes = ProfessorExerciseStudentCodeSubmissionSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        results = []

        #Obtain all students in the exercise class
        for student in data['exercise_class_students']:
            # Get all results from the student in the exercise
            student_results = [i for i in data['results'] if i['student'] == student and i['metric'] in data['exercise']['metrics']] # results of the student in the exercise

            # Order based on the metric order in the exercise
            student_results = sorted(student_results, key=lambda k: data['exercise']['metrics'].index(k['metric']))

            # Get the student code
            student_code = None
            for i in data['student_codes']:
                if i['student'] == student['id']:
                    student_code = data['student_codes'].pop(data['student_codes'].index(i))
                    student_code.pop("student", None)
                    break
            

            results.append({
                'student': student,
                'results': [
                    {
                    'date': i['date'],
                    'score': i['score'],
                    }
                    for i in student_results
                ],
                'code': student_code
            })

        for i in data["exercise"]["metrics"]:
            i.pop("metric_file", None)


        return {
            'exercise': data['exercise'],
            'results': results,
        }


class ProfessorExercisesSerializer(serializers.Serializer):
    exercises = ProfessorExercisesExerciseSerializer(many=True)
    classes = SimpleClassSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercises': data['exercises'],
            'classes': data['classes'],
        }


class PublicExercisesSerializer(serializers.Serializer):
    exercises = PublicExercisesExerciseSerializer(many=True)
    professors = PublicExercisesProfessorsSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercises': data['exercises'],
            'professors': data['professors'],
        }


class StudentAssignmentExerciseAndOwnResultsSerializer(serializers.Serializer):
    exercise = StudentAssignmentExerciseSerializer()
    my_results = StudentAssignmentExerciseOwnResultsSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Order based on the metric order in the exercise
        data['my_results'] = sorted(data['my_results'], key=lambda k: data['exercise']['metrics'].index(k['metric']))
        
        return {
            'exercise': data['exercise'],
            'my_results': data['my_results'],
        }

class StudentAssignmentSerializer(serializers.Serializer):
    assignment = StudentAssignmentExerciseAndOwnResultsSerializer()
    assignment_class_students = StudentSerializer(many=True)
    all_results = ProfessorExerciseResultSerializer(many=True)
    submission = StudentAssignmentCodeSubmissionSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        results = []

        metrics_id = [i['id'] for i in data['assignment']['exercise']['metrics']]

        #Obtain all students in the exercise class
        for student in data['assignment_class_students']:
            # Get all results from the student in the exercise
            student_results = [i for i in data['all_results'] if i['student'] == student and i['metric']['id'] in metrics_id] # results of the student in the exercise

            # Order based on the metric order in the exercise
            student_results = sorted(student_results, key=lambda k: metrics_id.index(k['metric']['id']))

            results.append({
                'student': student,
                'results': [
                    {
                    'date': i['date'],
                    'score': i['score'],
                    }
                    for i in student_results
                ]
            })

        for i in data["assignment"]['exercise']["metrics"]:
            i.pop("metric_file", None)


        return {
            'assignment': data['assignment'],
            'all_results': results,
            'submission': data['submission'],
        }

class StudentAssignmentsSerializer(serializers.Serializer):
    exercises = StudentAssignmentsExerciseSerializer(many=True)
    classes = SimpleClassSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'assignments': data['exercises'],
            'classes': data['classes'],
        }
    

class ProfessorCreateExerciseGETSerializer(serializers.Serializer):
    metrics = MetricOwnSerializer(many=True)
    classes = SimpleClassSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'metrics': data['metrics'],
            'classes': data['classes'],
        }