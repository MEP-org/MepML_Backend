from rest_framework import serializers
from MepML.models import Professor, Student, Class, Dataset, Metric, Exercise, User, Result

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
        fields = ['id', "name", "metric_file", "created_by"]

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
        fields = "__all__"

# ------------------------------ Result Serializers ------------------------------
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


class ProfessorExercisesSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)
    classes = ProfessorExercisesClassSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'exercises': data['exercises'],
            'classes': data['classes'],
        }













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
