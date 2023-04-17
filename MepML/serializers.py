from rest_framework import serializers
from MepML.models import CodeSubmission, Professor, Student, Class, Dataset, Metric, Exercise, User, Result

# ------------------------------ User Type Serializers ------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nmec', 'name')


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('id', 'user')


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Professor
        fields = ('id', 'user')


# ------------------------------ Professor Class Serializers ------------------------------
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


# ------------------------------ Student Class Serializers ------------------------------
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


# ------------------------------ Metric Serializers ------------------------------
class MetricSerializer(serializers.ModelSerializer):
    created_by = ProfessorSerializer()
    
    class Meta:
        model = Metric
        fields = ['id', "title", "description", "metric_file", "created_by"]

class MetricOwnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', "title", "description"]

class MetricViewerSerializer(serializers.ModelSerializer):
    created_by = ProfessorSerializer()
    
    class Meta:
        model = Metric
        fields = ['id', "title", "description", "created_by"]

class ProfessorMetricsSerializer(serializers.Serializer):
    my_metrics = MetricOwnSerializer(many=True)
    other_metrics = MetricViewerSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'my_metrics': data['my_metrics'],
            'other_metrics': data['other_metrics'],
        }

# ------------------------------ Dataset Serializers ------------------------------
class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', "train_name", "train_dataset", "train_upload_date", "test_name", "test_dataset", "test_upload_date"]

# ------------------------------ Exercise Serializers ------------------------------
class ExerciseClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', "name"]

class ExerciseSerializer(serializers.ModelSerializer):
    created_by = ProfessorSerializer()
    dataset = DatasetSerializer()
    metrics = MetricSerializer(many=True)
    students_class = ExerciseClassSerializer()
    
    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "description", "evaluation", "publish_date", "deadline", "limit_of_attempts", "visibility", "students_class", "metrics", "dataset", "created_by"]

# ------------------------------ Professor Exercise Serializers ------------------------------
class ProfessorExerciseResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    metric = MetricSerializer()

    class Meta:
        model = Result
        fields = ['id', "score", "date", "student", "metric"]


class ProfessorExerciseSerializer(serializers.Serializer):
    exercise = ExerciseSerializer()
    results = ProfessorExerciseResultSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercise': data['exercise'],
            'results': data['results'],
        }
    

class ProfessorExercisesClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', "name"]

class ProfessorExercisesExerciseSerializer(serializers.ModelSerializer):
    students_class = ProfessorClassesSerializer()
    
    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "deadline", "limit_of_attempts", "visibility", "students_class", "num_answers"]


class ProfessorExercisesSerializer(serializers.Serializer):
    exercises = ProfessorExercisesExerciseSerializer(many=True)
    classes = ProfessorExercisesClassSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercises': data['exercises'],
            'classes': data['classes'],
        }
    

# ------------------------------ Public Exercises ------------------------------
class PublicExercisesProfessorsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.name

    class Meta:
        model = Professor
        fields = ('id', 'name')

class PublicExercisesExerciseTrainingDatasetSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return obj.train_dataset.size

    class Meta:
        model = Dataset
        fields = ["train_dataset", "size"]


class PublicExercisesExerciseSerializer(serializers.ModelSerializer):
    created_by = PublicExercisesProfessorsSerializer()
    dataset = PublicExercisesExerciseTrainingDatasetSerializer()

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "created_by", "dataset"]

class PublicExercisesSerializer(serializers.Serializer):
    exercises = PublicExercisesExerciseSerializer(many=True)
    professors = PublicExercisesProfessorsSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercises': data['exercises'],
            'professors': data['professors'],
        }
    

# ------------------------------ Student Assignment Serializers ------------------------------
class StudentAssignmentExerciseDatasetSerializer(serializers.ModelSerializer):
    train_dataset_size = serializers.SerializerMethodField()
    test_dataset_size = serializers.SerializerMethodField()

    def get_train_dataset_size(self, obj):
        return obj.train_dataset.size
    
    def get_test_dataset_size(self, obj):
        return obj.test_dataset.size
    
    class Meta:
        model = Dataset
        fields = ["train_name", "train_dataset", "train_dataset_size", "train_upload_date", "test_name", "test_dataset", "test_dataset_size", "test_upload_date"]


class StudentAssignmentExerciseOwnResultsSerializer(serializers.ModelSerializer):
    metric = MetricOwnSerializer()

    class Meta:
        model = Result
        fields = ['metric', 'score']


class StudentAssignmentExerciseSerializer(serializers.ModelSerializer):
    dataset = StudentAssignmentExerciseDatasetSerializer()
    metrics = MetricOwnSerializer(many=True)
    students_class = ProfessorExercisesClassSerializer()

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "deadline", "limit_of_attempts", "visibility", "students_class", "metrics", "description", "evaluation", "dataset"]

class StudentAssignmentExerciseAndOwnResultsSerializer(serializers.Serializer):
    exercise = StudentAssignmentExerciseSerializer()
    my_results = StudentAssignmentExerciseOwnResultsSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercise': data['exercise'],
            'my_results': data['my_results'],
        }
    

class StudentAssignmentCodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = ['id', "file_name_result", "result_submission", "result_submission_date", "file_name_code", "code_submission", "code_submission_date"]


class StudentAssignmentSerializer(serializers.Serializer):
    assignment = StudentAssignmentExerciseAndOwnResultsSerializer()
    all_results = ProfessorExerciseResultSerializer(many=True)
    submission = StudentAssignmentCodeSubmissionSerializer()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'assignment': data['assignment'],
            'all_results': data['all_results'],
            'submission': data['submission'],
        }
    
# ------------------------------ Student Assignments Serializers ------------------------------

class StudentAssignmentsClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', "name"]

class StudentAssignmentsExerciseSerializer(serializers.ModelSerializer):
    students_class = StudentAssignmentsClassSerializer()

    class Meta:
        model = Exercise
        fields = ["id", "title", "subtitle", "publish_date", "deadline", "limit_of_attempts", "visibility", "students_class", "num_answers"]

class StudentAssignmentsSerializer(serializers.Serializer):
    exercises = StudentAssignmentsExerciseSerializer(many=True)
    classes = StudentAssignmentsClassSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercises': data['exercises'],
            'classes': data['classes'],
        }
    

# ------------------------------ Student Home Serializers ------------------------------
class StudentHomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["num_exercises", "num_submissions", "next_deadline", "last_ranking"]

















# class ProfessorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Professor
#         fields = ["name", "email"]


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ["nmec", "name", "email"]


# class ClassSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Class
#         fields = ["name", "created_by", "students", "image"]


# class ClassPreviewSerializer(serializers.ModelSerializer):
#     num_students = serializers.SerializerMethodField()

#     def get_num_students(self, obj):
#         return obj.students.count()

#     class Meta:
#         model = Class
#         fields = ["id", "name", "num_students", "image"]


# # Dataset will be serialized in the ExerciseSerializer

# class MetricSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Metric
#         fields = ["name", "path_to_function"]


# class ExerciseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exercise
#         fields = "__all__"
