"""Tests for configuration module."""

import pytest
from unittest.mock import patch, MagicMock
from src.config import Config, config


class TestConfig:
    """Test cases for Config class."""

    def test_validate_config_missing_all(self):
        """Test validation when all required config is missing."""
        with patch.dict('os.environ', {}, clear=True):
            config = Config()
            missing = config.validate_config()
            expected_missing = ["GOOGLE_API_KEY", "GOOGLE_MAPS_PLATFORM_API_KEY", "OPIK_API_KEY", "OPIK_WORKSPACE"]
            assert set(missing) == set(expected_missing)

    def test_validate_config_all_present(self):
        """Test validation when all required config is present."""
        env_vars = {
            "GOOGLE_API_KEY": "test_key",
            "GOOGLE_MAPS_PLATFORM_API_KEY": "test_maps_key",
            "OPIK_API_KEY": "test_opik_key",
            "OPIK_WORKSPACE": "test_workspace"
        }
        with patch.dict('os.environ', env_vars):
            config = Config()
            missing = config.validate_config()
            assert missing == []

    def test_is_production_ready_true(self):
        """Test production ready check when config is complete."""
        env_vars = {
            "GOOGLE_API_KEY": "test_key",
            "GOOGLE_MAPS_PLATFORM_API_KEY": "test_maps_key",
            "OPIK_API_KEY": "test_opik_key",
            "OPIK_WORKSPACE": "test_workspace"
        }
        with patch.dict('os.environ', env_vars):
            config = Config()
            assert config.is_production_ready() is True

    def test_is_production_ready_false(self):
        """Test production ready check when config is incomplete."""
        with patch.dict('os.environ', {}, clear=True):
            config = Config()
            assert config.is_production_ready() is False

    def test_config_attributes(self):
        """Test that config attributes are set correctly."""
        env_vars = {
            "GOOGLE_API_KEY": "test_google_key",
            "GOOGLE_MAPS_PLATFORM_API_KEY": "test_maps_key",
            "OPIK_API_KEY": "test_opik_key",
            "OPIK_WORKSPACE": "test_workspace",
            "OPENWEATHER_API_KEY": "test_weather_key",
            "TIMEZONEDB_API_KEY": "test_time_key"
        }
        with patch.dict('os.environ', env_vars):
            config = Config()
            assert config.GOOGLE_API_KEY == "test_google_key"
            assert config.GOOGLE_MAPS_PLATFORM_API_KEY == "test_maps_key"
            assert config.OPIK_API_KEY == "test_opik_key"
            assert config.OPIK_WORKSPACE == "test_workspace"
            assert config.OPENWEATHER_API_KEY == "test_weather_key"
            assert config.TIMEZONEDB_API_KEY == "test_time_key"
            assert config.AGENT_MODEL == "gemini-2.0-flash"
            assert config.AGENT_NAME == "weather_time_city_agent"
