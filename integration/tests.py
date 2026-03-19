from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch, Mock


class IntegrationTest(TestCase):

    @patch("integration.views.requests.get")
    def test_environment_summary(self, mock_get):
        client = APIClient()

        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: [
                {"capital": ["Manila"], "population": 113000000}
            ]),
            Mock(status_code=200, json=lambda: {
                "main": {"temp": 27, "humidity": 60},
                "weather": [{"main": "Cloudy"}]
            })
        ]

        response = client.get("/api/v1/environment-summary/?country=Philippines")

        self.assertEqual(response.status_code, 200)