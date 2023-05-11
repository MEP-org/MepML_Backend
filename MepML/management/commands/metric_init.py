from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from MepML.models import Metric


class Command(BaseCommand):
    help = "Initialize built-in metrics"
    base_src = "def score(y_true, y_pred):\n"

    metrics = [
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
        }
    ]

    def handle(self, *args, **options):
        # delete all built-in metrics from the database
        Metric.objects.filter(created_by=None).delete()

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
