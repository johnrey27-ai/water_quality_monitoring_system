from rest_framework.routers import DefaultRouter
from .views import WaterQualityViewSet

router = DefaultRouter()
router.register(r'readings', WaterQualityViewSet)

urlpatterns = router.urls