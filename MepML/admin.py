from django.contrib import admin
from .models import Professor, Student, Class, Metric, Exercise

# Register your models here.
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Metric)
admin.site.register(Exercise)
