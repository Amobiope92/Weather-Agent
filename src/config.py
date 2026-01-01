"""Configuration management for the Weather Agent application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""

    # Google AI API
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")

    # Google Maps Platform API
    GOOGLE_MAPS_PLATFORM_API_KEY: Optional[str] = os.getenv("GOOGLE_MAPS_PLATFORM_API_KEY")

    # Opik Monitoring
    OPIK_API_KEY: Optional[str] = os.getenv("OPIK_API_KEY")
    OPIK_WORKSPACE: Optional[str] = os.getenv("OPIK_WORKSPACE")
    OPIK_PROJECT_NAME: Optional[str] = os.getenv("OPIK_PROJECT_NAME", "weather-agent")

    # Real API Keys (for production use)
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    TIMEZONEDB_API_KEY: Optional[str] = os.getenv("TIMEZONEDB_API_KEY")

    # Agent Configuration
    AGENT_MODEL: str = "gemini-2.0-flash"
    AGENT_NAME: str = "weather_time_city_agent"

    @classmethod
    def validate_config(cls) -> list[str]:
        """Validate required configuration and return list of missing items."""
        missing = []

        if not cls.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY")

        if not cls.GOOGLE_MAPS_PLATFORM_API_KEY:
            missing.append("GOOGLE_MAPS_PLATFORM_API_KEY")

        if not cls.OPIK_API_KEY:
            missing.append("OPIK_API_KEY")

        if not cls.OPIK_WORKSPACE:
            missing.append("OPIK_WORKSPACE")

        return missing

    @classmethod
    def is_production_ready(cls) -> bool:
        """Check if configuration is ready for production."""
        return len(cls.validate_config()) == 0

# Global config instance
config = Config()
