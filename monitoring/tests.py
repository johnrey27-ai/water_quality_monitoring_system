from rest_framework.test import APITestCase
from rest_framework import status
from .models import WaterQualityReading


class WaterQualityAPITest(APITestCase):

    def setUp(self):
        """
        Runs before each test
        """
        self.url = '/api/v1/readings/'

        self.valid_data = {
            "temperature": 25,
            "ph": 7,
            "turbidity": 5,
            "light_intensity": 300
        }

    def test_create_reading(self):
        """
        Test creating a water quality reading
        """
        response = self.client.post(self.url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WaterQualityReading.objects.count(), 1)

        reading = WaterQualityReading.objects.first()

        # Check predicted_do is generated
        self.assertIsNotNone(reading.predicted_do)

    def test_get_all_readings(self):
        """
        Test retrieving all readings
        """
        WaterQualityReading.objects.create(**self.valid_data)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_latest_reading_endpoint(self):
        """
        Test latest reading custom endpoint
        """
        WaterQualityReading.objects.create(**self.valid_data)

        response = self.client.get('/api/v1/readings/latest/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predicted_do', response.data)