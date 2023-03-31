from rest_framework import serializers
from MepML.models import *

# this is only a test
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["name", "email"]

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["name", "email"]