"""Time service using TimeZoneDB API."""

import requests
import logging
from datetime import datetime
from typing import Dict, Any
from .config import config

logger = logging.getLogger(__name__)

class TimeService:
    """Service for fetching accurate time information."""

    BASE_URL = "https://api.timezonedb.com/v2.1/get-time-zone"

    # Fallback timezone mapping for common cities
    FALLBACK_TIMEZONES = {
        "newyork": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
        "losangeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "mumbai": "Asia/Kolkata",
        "beijing": "Asia/Shanghai",
        "moscow": "Europe/Moscow"
    }

    @staticmethod
    def get_current_time(city: str) -> Dict[str, Any]:
        """
        Get current time for a city.

        Args:
            city: City name

        Returns:
            Dictionary containing time information or error details
        """
        try:
            if not config.TIMEZONEDB_API_KEY:
                logger.warning("TimeZoneDB API key not configured, using fallback timezone data")
                return TimeService._get_fallback_time(city)

            # First get timezone information
            city_normalized = city.lower().replace(" ", "")

            # Try to get timezone from API first
            timezone_data = TimeService._get_timezone_from_api(city)
            if timezone_data and timezone_data.get('status') == 'OK':
                zone_name = timezone_data['zoneName']
            else:
                # Fallback to predefined mapping
                if city_normalized in TimeService.FALLBACK_TIMEZONES:
                    zone_name = TimeService.FALLBACK_TIMEZONES[city_normalized]
                else:
                    return {
                        "status": "error",
                        "error_message": f"Sorry, I don't have timezone information for '{city}'."
                    }

            # Get current time using the timezone
            params = {
                'key': config.TIMEZONEDB_API_KEY,
                'format': 'json',
                'by': 'zone',
                'zone': zone_name
            }

            response = requests.get(TimeService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 'OK':
                # Parse the timestamp
                timestamp = data['timestamp']
                dt = datetime.fromtimestamp(timestamp)

                report = f"The current time in {city} ({zone_name}) is {dt.strftime('%H:%M')} on {dt.strftime('%Y-%m-%d')}."

                return {
                    "status": "success",
                    "report": report,
                    "data": {
                        "city": city,
                        "timezone": zone_name,
                        "timestamp": timestamp,
                        "formatted_time": dt.strftime('%H:%M'),
                        "formatted_date": dt.strftime('%Y-%m-%d')
                    }
                }
            else:
                logger.warning(f"TimeZoneDB API returned error for {city}: {data}")
                return TimeService._get_fallback_time(city)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching time data for {city}: {e}")
            return TimeService._get_fallback_time(city)
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing time data for {city}: {e}")
            return TimeService._get_fallback_time(city)

    @staticmethod
    def _get_timezone_from_api(city: str) -> Dict[str, Any]:
        """Get timezone information from TimeZoneDB API."""
        try:
            params = {
                'key': config.TIMEZONEDB_API_KEY,
                'format': 'json',
                'by': 'position',
                'lat': 0,  # We'll need to implement city coordinate lookup
                'lng': 0
            }
            # Note: This is a simplified implementation
            # In production, you'd need a geocoding service to get coordinates from city name
            return None
        except Exception:
            return None

    @staticmethod
    def _get_fallback_time(city: str) -> Dict[str, Any]:
        """Fallback time data using predefined timezone mapping."""
        from datetime import datetime
        from zoneinfo import ZoneInfo

        city_normalized = city.lower().replace(" ", "")

        if city_normalized in TimeService.FALLBACK_TIMEZONES:
            try:
                timezone = TimeService.FALLBACK_TIMEZONES[city_normalized]
                tz = ZoneInfo(timezone)
                now = datetime.now(tz)
                report = f"The current time in {city} is {now.strftime('%H:%M')}."
                return {
                    "status": "success",
                    "report": report,
                    "data": {
                        "city": city,
                        "timezone": timezone,
                        "formatted_time": now.strftime('%H:%M')
                    }
                }
            except Exception as e:
                logger.error(f"Error getting fallback time for {city}: {e}")

        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for '{city}'."
        }
