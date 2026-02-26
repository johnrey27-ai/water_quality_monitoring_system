from rest_framework import viewsets
from .models import WaterQualityReading
from .serializers import WaterQualitySerializer

class WaterQualityViewSet(viewsets.ModelViewSet):
    queryset = WaterQualityReading.objects.all().order_by('-created_at')
    serializer_class = WaterQualitySerializer