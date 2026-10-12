from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, AnalysisRunViewSet

router = DefaultRouter()
router.register("datasets", DatasetViewSet, basename="dataset")
router.register("analysis-runs", AnalysisRunViewSet, basename="analysis-run")

urlpatterns = router.urls
