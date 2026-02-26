from rest_framework.test import APITestCase
from rest_framework import status
from .models import WaterQualityReading


class WaterQualityAPITest(APITestCase):

    def test_create_reading(self):
        url = '/api/v1/readings/'
        data = {
            "temperature": 25,
            "ph": 7,
            "turbidity": 5,
            "light_intensity": 300
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WaterQualityReading.objects.count(), 1)

        reading = WaterQualityReading.objects.first()
        self.assertIsNotNone(reading.predicted_do)