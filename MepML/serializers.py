from rest_framework import serializers
from MepML.models import Professor, Student, Class, Dataset, Metric, Exercise


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["name", "email"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["nmec", "name", "email"]


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["name", "created_by", "students", "image"]


class ClassPreviewSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()

    def get_num_students(self, obj):
        return obj.students.count()

    class Meta:
        model = Class
        fields = ["id", "name", "num_students", "image"]


# Dataset will be serialized in the ExerciseSerializer

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ["name", "description", "created_by", "source_code"]


class MetricPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ["id", "name", "description"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"
