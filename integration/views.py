import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def environment_summary(request):

    country = request.GET.get("country")

    if not country:
        return Response(
            {"error": "Country parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        # API 1: Country information
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

        # API 2: Weather information
        api_key = "deadef5fec5c9d9754342c1bf104f358"

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

        # DATA TRANSFORMATION
        result = {
            "country": country,
            "capital": capital,
            "population": population,
            "temperature_celsius": temperature,
            "weather_condition": condition,
            "humidity_level": humidity
        }

        return Response(result)

    except Exception:
        return Response(
            {"error": "External API failure"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )