from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WaterQualityReading
from .serializers import WaterQualitySerializer


class WaterQualityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing water quality readings.
    Provides full CRUD operations.
    """

    queryset = WaterQualityReading.objects.all().order_by('-created_at')
    serializer_class = WaterQualitySerializer

    # Enable search and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ph']  # You can change to other fields if needed
    ordering_fields = ['created_at', 'temperature', 'predicted_do']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Returns the most recent water quality reading.
        """
        latest_reading = self.queryset.first()

        if not latest_reading:
            return Response({"message": "No readings available."})

        serializer = self.get_serializer(latest_reading)
        return Response(serializer.data)