from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import Dataset, AnalysisRun
from .serializers import DatasetSerializer, AnalysisRunSerializer

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all().order_by("-uploaded_at")
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class AnalysisRunViewSet(viewsets.ModelViewSet):
    queryset = AnalysisRun.objects.all().order_by("-created_at")
    serializer_class = AnalysisRunSerializer
    permission_classes = [IsAuthenticated]
