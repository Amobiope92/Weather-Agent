"""Weather Time Directions Agent - Production Implementation."""

import logging
from typing import Dict, Any
import opik
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from .config import config
from .weather_service import WeatherService
from .time_service import TimeService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weather(city: str) -> Dict[str, Any]:
    """
    Get weather information for a city.

    Args:
        city: City name to get weather for

    Returns:
        Dictionary with weather information or error message
    """
    logger.info(f"Getting weather for city: {city}")
    return WeatherService.get_weather(city)

def get_current_time(city: str) -> Dict[str, Any]:
    """
    Get current time for a city.

    Args:
        city: City name to get time for

    Returns:
        Dictionary with time information or error message
    """
    logger.info(f"Getting time for city: {city}")
    return TimeService.get_current_time(city)

def create_weather_agent() -> LlmAgent:
    """
    Create and configure the weather agent.

    Returns:
        Configured LlmAgent instance
    """
    # Validate configuration
    missing_config = config.validate_config()
    if missing_config:
        logger.warning(f"Missing configuration: {', '.join(missing_config)}")
        logger.warning("Some features may not work properly")

    # Configure Opik if API key is available
    if config.OPIK_API_KEY and config.OPIK_WORKSPACE:
        opik.configure(
            use_local=False,
            api_key=config.OPIK_API_KEY,
            workspace=config.OPIK_WORKSPACE,
            project_name=config.OPIK_PROJECT_NAME
        )
        opik_tracer = opik.OpikTracer()
        logger.info("Opik monitoring enabled")
    else:
        opik_tracer = None
        logger.warning("Opik monitoring disabled - API key or workspace not configured")

    # Create the agent
    agent = LlmAgent(
        name=config.AGENT_NAME,
        model=config.AGENT_MODEL,
        description=(
            "A helpful assistant that provides weather information, current time, "
            "and directions between cities using real-time data sources."
        ),
        instruction=(
            "You are a helpful assistant. When the user asks about weather or time for a city, "
            "use the appropriate tools to fetch real-time information. For directions between cities, "
            "use the Google Maps integration. Always provide clear, accurate information and "
            "inform the user if any data is unavailable."
        ),
        tools=[
            get_weather,
            get_current_time,
            MCPToolset(
                connection_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-google-maps",
                    ],
                    env={
                        "GOOGLE_MAPS_API_KEY": config.GOOGLE_MAPS_PLATFORM_API_KEY or ""
                    },
                ),
            ),
        ],
    )

    # Add Opik callbacks if configured
    if opik_tracer:
        agent.before_agent_callback = opik_tracer.before_agent_callback
        agent.after_agent_callback = opik_tracer.after_agent_callback
        agent.before_model_callback = opik_tracer.before_model_callback
        agent.after_model_callback = opik_tracer.after_model_callback
        agent.before_tool_callback = opik_tracer.before_tool_callback
        agent.after_tool_callback = opik_tracer.after_tool_callback

    logger.info(f"Created agent: {config.AGENT_NAME}")
    return agent

# Global agent instance
weather_agent = create_weather_agent()
