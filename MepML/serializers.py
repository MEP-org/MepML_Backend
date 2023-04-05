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
        fields = ["name", "number_of_students", "created_by", "students"]


# Dataset will be serialized in the ExerciseSerializer

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ["name", "path_to_function"]


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"
