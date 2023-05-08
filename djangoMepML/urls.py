"""
djangoMepML URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path
from MepML import views
from MepML.webservices import ws_classes, ws_manage_class, ws_metrics, ws_manage_metric,\
    ws_exercises, ws_manage_exercise, ws_metrics_classes, ws_public_exercise, ws_public_exercises, ws_assignments, \
    ws_student_class, ws_home, ws_student_classes, ws_student_assignment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("professors/<int:prof_id>/classes", ws_classes.handle),
    path("professors/<int:prof_id>/classes/<int:class_id>", ws_manage_class.handle),
    path("professors/<int:prof_id>/metrics", ws_metrics.handle),
    path("professors/<int:prof_id>/exercises", ws_exercises.handle),
    path("professors/<int:prof_id>/exercises/<int:exercise_id>", ws_manage_exercise.handle),
    path("professors/<int:prof_id>/metricsclasses", ws_metrics_classes.handle),
    path("publicexercises/", ws_public_exercises.handle),
    path("publicexercises/<int:exercise_id>", ws_public_exercise.handle),
    path("students/<int:student_id>/assignments", ws_assignments.handle),
    path("students/<int:student_id>/assignments/<int:assignment_id>", ws_student_assignment.handle),
    path("students/<int:student_id>/classes", ws_student_classes.handle),
    path("students/<int:student_id>/classes/<int:class_id>", ws_student_class.handle),
    path("students/<int:student_id>/home", ws_home.handle),
    #not to being use by front-end
    path('admin/', admin.site.urls),
    path("professors/<int:prof_id>/metrics/<int:metric_id>", ws_manage_metric.handle),
    path("insertdata/", views.insert_data, name="insert_data"),
    path("getclass/<int:class_id>", views.get_class, name="get_class"),
    path("updateclass/<int:class_id>", views.update_class, name="update_class"),
    path("apitest", views.create_default_metric, name="default_metric"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
