from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch, Mock


class IntegrationTest(TestCase):

    @patch("integration.views.requests.get")
    def test_environment_summary(self, mock_get):

        client = APIClient()

        mock_country = Mock()
        mock_country.status_code = 200
        mock_country.json.return_value = [
            {
                "capital": ["Manila"],
                "population": 113000000
            }
        ]

        mock_weather = Mock()
        mock_weather.status_code = 200
        mock_weather.json.return_value = {
            "main": {
                "temp": 27,
                "humidity": 60
            },
            "weather": [
                {"main": "Cloudy"}
            ]
        }

        mock_get.side_effect = [mock_country, mock_weather]

        response = client.get(
            "/api/v1/environment-summary/?country=Philippines"
        )

        self.assertEqual(response.status_code, 200)