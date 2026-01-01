# Weather Time Directions Agent

A production-ready Streamlit application featuring an intelligent agent that provides real-time weather information, accurate time data, and directions between cities using Google's Gemini AI and external APIs.

## Features

- **Real-time Weather**: Get current weather conditions for any city worldwide
- **Accurate Time**: Display current time with proper timezone handling
- **City Directions**: Get route planning and navigation between cities
- **AI-Powered**: Uses Google's Gemini 2.0 Flash for intelligent conversations
- **Monitoring**: Full observability with Opik integration
- **Production Ready**: Deployable to Streamlit Cloud Community

## Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd weather-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   # Create a .env file and add your API keys
   ```

4. **Run locally**:
   ```bash
   python run_local.py
   ```

### Streamlit Cloud Deployment

1. **Fork this repository** on GitHub

2. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Set main file path to: `app/app.py`
   - Add secrets in the advanced settings

3. **Configure secrets** in Streamlit Cloud:
   ```toml
   GOOGLE_API_KEY = "your_google_api_key"
   GOOGLE_MAPS_PLATFORM_API_KEY = "your_google_maps_key"
   OPIK_API_KEY = "your_opik_api_key"
   OPIK_WORKSPACE = "your_opik_workspace"
   OPIK_PROJECT_NAME = "weather-agent"
   ```

## Configuration

### Required API Keys

| Service | Environment Variable | Where to Get |
|---------|---------------------|--------------|
| Google AI | `GOOGLE_API_KEY` | [Google AI Studio](https://aistudio.google.com/) |
| Google Maps | `GOOGLE_MAPS_PLATFORM_API_KEY` | [Google Cloud Console](https://console.cloud.google.com/) |
| Opik | `OPIK_API_KEY` | [Opik Dashboard](https://app.comet.com/) |
| OpenWeatherMap | `OPENWEATHER_API_KEY` | [OpenWeatherMap](https://openweathermap.org/api) |
| TimeZoneDB | `TIMEZONEDB_API_KEY` | [TimeZoneDB](https://timezonedb.com/) |

### Optional Configuration

- `OPIK_WORKSPACE`: Your Opik workspace name
- `OPIK_PROJECT_NAME`: Project name for tracking (default: "weather-agent")

## Project Structure

```
weather-agent/
├── app/                          # Streamlit application
│   └── app.py                   # Main Streamlit app
├── src/                         # Core application code
│   ├── __init__.py
│   ├── agent.py                 # Agent implementation
│   ├── config.py                # Configuration management
│   ├── weather_service.py       # Weather API integration
│   └── time_service.py          # Time API integration
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_config.py           # Configuration tests
├── docs/                        # Documentation
├── .streamlit/                  # Streamlit configuration
│   └── config.toml
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── run_local.py                 # Local development runner
└── README.md                    # This file
```

## Testing

Run the test suite:

```bash
pip install -r requirements-dev.txt
pytest
```

## API Documentation

### Weather Service

Get real-time weather information:

```python
from src.weather_service import WeatherService

result = WeatherService.get_weather("New York")
print(result["report"])
```

### Time Service

Get accurate time information:

```python
from src.time_service import TimeService

result = TimeService.get_current_time("London")
print(result["report"])
```

### Agent Integration

Use the full agent:

```python
from src.agent import weather_agent

response = weather_agent.run("What's the weather in Tokyo?")
print(response)
```

## Deployment Options

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Deploy via [share.streamlit.io](https://share.streamlit.io)
3. Configure secrets in the dashboard
4. App is live instantly!

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python run_local.py
```

### Docker (Advanced)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app/app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google ADK](https://github.com/google/agent-dev-kit) - Agent Development Kit
- [Opik](https://github.com/comet-ml/opik) - AI Observability Platform
- [Streamlit](https://streamlit.io/) - Web app framework
- [OpenWeatherMap](https://openweathermap.org/) - Weather data API
- [TimeZoneDB](https://timezonedb.com/) - Timezone database
