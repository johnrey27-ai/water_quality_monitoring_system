import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'country',
            openapi.IN_PATH,
            description="Country name (e.g., USA, France, Japan)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@api_view(['GET'])
def environment_summary(request, country):
    try:
        # 🌍 Get country data
        country_url = f"https://restcountries.com/v3.1/name/{country}"
        country_response = requests.get(country_url)

        if country_response.status_code != 200:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        country_data = country_response.json()[0]

        capital = country_data.get("capital", ["Unknown"])[0]
        population = country_data.get("population", "Unknown")

        # 🌦 Get weather data
        api_key = "YOUR_API_KEY_HERE"  # ⚠️ Replace this

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)

        if weather_response.status_code != 200:
            return Response(
                {"error": "Weather service unavailable"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        weather_data = weather_response.json()

        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        condition = weather_data["weather"][0]["main"]

        # 📊 Final result
        result = {
            "country": country,
            "capital": capital,
            "population": population,
            "temperature_celsius": temperature,
            "weather_condition": condition,
            "humidity_level": humidity
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )