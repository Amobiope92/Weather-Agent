"""Weather service using OpenWeatherMap API."""

import requests
import logging
from typing import Dict, Optional, Any
from .config import config

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching real weather data."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(city: str) -> Dict[str, Any]:
        """
        Get weather information for a city.

        Args:
            city: City name

        Returns:
            Dictionary containing weather information or error details
        """
        try:
            if not config.OPENWEATHER_API_KEY:
                logger.warning("OpenWeatherMap API key not configured, using mock data")
                return WeatherService._get_mock_weather(city)

            params = {
                'q': city,
                'appid': config.OPENWEATHER_API_KEY,
                'units': 'imperial'  # Use Fahrenheit for consistency
            }

            response = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract relevant weather information
            weather_info = {
                "status": "success",
                "city": data['name'],
                "country": data['sys']['country'],
                "temperature": data['main']['temp'],
                "description": data['weather'][0]['description'].capitalize(),
                "humidity": data['main']['humidity'],
                "wind_speed": data['wind']['speed'],
                "pressure": data['main']['pressure']
            }

            report = (
                f"The weather in {weather_info['city']}, {weather_info['country']} is "
                f"{weather_info['description']} with a temperature of {weather_info['temperature']}°F. "
                f"Humidity: {weather_info['humidity']}%, Wind: {weather_info['wind_speed']} mph, "
                f"Pressure: {weather_info['pressure']} hPa."
            )

            return {
                "status": "success",
                "report": report,
                "data": weather_info
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for {city}: {e}")
            return {
                "status": "error",
                "error_message": f"Unable to fetch weather data for '{city}'. Please check the city name and try again."
            }
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing weather data for {city}: {e}")
            return {
                "status": "error",
                "error_message": f"Received invalid weather data for '{city}'."
            }

    @staticmethod
    def _get_mock_weather(city: str) -> Dict[str, Any]:
        """Fallback mock weather data when API is not available."""
        city_normalized = city.lower().replace(" ", "")

        mock_weather = {
            "newyork": {
                "status": "success",
                "report": "The weather in New York is sunny with a temperature of 45°F.",
            },
            "london": {
                "status": "success",
                "report": "It's cloudy in London with a temperature of 55°F.",
            },
            "tokyo": {
                "status": "success",
                "report": "Tokyo is experiencing light rain and a temperature of 72°F.",
            },
        }

        if city_normalized in mock_weather:
            return mock_weather[city_normalized]
        else:
            return {
                "status": "error",
                "error_message": f"Sorry, I don't have weather information for '{city}'.",
            }
