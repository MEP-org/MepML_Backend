from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from MepML.models import User, Professor, Student, Class, Metric


class Command(BaseCommand):
    help = "Initialize built-in metrics"
    base_src = "def score(y_true, y_pred):\n"

    metrics = [
        # Classification
        {
            "title": "Accuracy",
            "description": "(True positives + True negatives) / Total number of samples",
            "src": base_src + "\treturn sklearn.metrics.accuracy_score(y_true, y_pred)\n"
        },
        {
            "title": "Precision",
            "description": "True positives / (True positives + False positives)",
            "src": base_src + "\tif len(set(y_true.flatten())) > 2:\n" +
            "\t\treturn sklearn.metrics.precision_score(y_true, y_pred, average=\"weighted\", zero_division=0)\n" +
            "\telse:\n" +
            "\t\treturn sklearn.metrics.precision_score(y_true, y_pred)\n"
        },
        {
            "title": "Recall",
            "description": "True positives / (True positives + False negatives)",
            "src": base_src + "\tif len(set(y_true.flatten())) > 2:\n" +
            "\t\treturn sklearn.metrics.recall_score(y_true, y_pred, average=\"weighted\", zero_division=0)\n" +
            "\telse:\n" +
            "\t\treturn sklearn.metrics.recall_score(y_true, y_pred)\n"
        },
        {
            "title": "F1",
            "description": "2 * (Precision * Recall) / (Precision + Recall)",
            "src": base_src + "\tif len(set(y_true.flatten())) > 2:\n" +
            "\t\treturn sklearn.metrics.f1_score(y_true, y_pred, average=\"weighted\", zero_division=0)\n" +
            "\telse:\n" +
            "\t\treturn sklearn.metrics.f1_score(y_true, y_pred)\n"
        },
        {
            "title": "MCC",
            "description": "Matthews Correlation Coefficient",
            "src": base_src + "\treturn sklearn.metrics.matthews_corrcoef(y_true, y_pred)\n"
        },

        # Regression
        {
            "title": "MAE",
            "description": "Mean absolute error",
            "src": base_src + "\treturn sklearn.metrics.mean_absolute_error(y_true, y_pred)\n"
        },
        {
            "title": "MSE",
            "description": "Mean squared error",
            "src": base_src + "\treturn sklearn.metrics.mean_squared_error(y_true, y_pred)\n"
        },
        {
            "title": "R2",
            "description": "Coefficient of determination - proportion of the variance " +
            "in the dependent variable that is predictable from the independent variable(s)",
            "src": base_src + "\treturn sklearn.metrics.r2_score(y_true, y_pred)\n"
        },
    ]

    def handle(self, *args, **options):
        # Delete all built-in metrics from the database
        Metric.objects.filter(created_by=None).delete()

        # Create Professor
        user = User.objects.create_user(nmec=102534, name="Rafael Gonçalves", email="rfg@ua.pt")
        professor = Professor.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS(f"Professor {user.name} created"))

        # Create Students
        user1 = User.objects.create_user(nmec=654321, name="João Mário", email="jm@ua.pt")
        student1 = Student.objects.create(user=user1)
        self.stdout.write(self.style.SUCCESS(f"Student {user1.name} created"))

        user2 = User.objects.create_user(nmec=987654, name="Rafa Silva", email="rs@ua.pt")
        student2 = Student.objects.create(user=user2)
        self.stdout.write(self.style.SUCCESS(f"Student {user2.name} created"))

        # Create class
        class_ = Class.objects.create(id=1, name="Class 1", image="image.png", created_by=professor)
        class_.students.add(student1)
        class_.students.add(student2)

        for metric in self.metrics:
            filename = f"metrics/{metric['title'].lower()}.py"
            content = ContentFile(metric["src"])
            if default_storage.exists(filename):
                default_storage.delete(filename)
            default_storage.save(filename, content)
            self.stdout.write(self.style.SUCCESS(f"Metric {metric['title']} created"))
            Metric.objects.create(
                title=metric["title"],
                description=metric["description"],
                metric_file=filename
            )
