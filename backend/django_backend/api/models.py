from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, blank=True)
    rows = models.PositiveIntegerField(default=0)
    columns = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AnalysisRun(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="runs")
    algorithm = models.CharField(max_length=100)
    accuracy = models.FloatField(null=True, blank=True)
    result_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
