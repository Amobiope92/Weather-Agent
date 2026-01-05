"""Streamlit Weather Agent Application."""

import streamlit as st
import logging
from typing import Optional

# Configure page first
st.set_page_config(
    page_title="Weather Time Directions Agent",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for required packages
MISSING_PACKAGES = []

try:
    from src.config import config
except ImportError as e:
    MISSING_PACKAGES.append(f"Configuration module: {e}")

try:
    from src.agent import weather_agent
except ImportError as e:
    MISSING_PACKAGES.append(f"Agent module: {e}")
    weather_agent = None

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False

def check_configuration() -> Optional[str]:
    """Check if required configuration is available."""
    missing = config.validate_config()
    if missing:
        return f"Missing required configuration: {', '.join(missing)}. Please check your .env file."
    return None

def display_sidebar():
    """Display sidebar with information and controls."""
    with st.sidebar:
        st.title("🌤️ Weather Agent")
        st.markdown("---")

        # Configuration status
        config_error = check_configuration()
        if config_error:
            st.error(f"⚠️ Configuration Issue: {config_error}")
        else:
            st.success("✅ Configuration OK")

        st.markdown("---")

        # Agent capabilities
        st.subheader("Capabilities")
        st.markdown("""
        - 🌡️ **Weather Information**: Real-time weather data
        - 🕐 **Current Time**: Accurate time for any city
        - 🗺️ **Directions**: Route planning between cities
        """)

        st.markdown("---")

        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()

        # About section
        st.markdown("---")
        st.subheader("About")
        st.markdown("""
        This agent uses Google's Gemini AI with real-time data sources
        for accurate weather, time, and navigation information.
        """)

def display_chat_interface():
    """Display the main chat interface."""
    st.title("Weather Time Directions Assistant")
    st.markdown("Ask me about weather, time, or directions between cities!")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about weather, time, or directions..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = weather_agent.run_live(prompt)
                    # Extract the response text
                    if hasattr(response, 'text'):
                        response_text = response.text
                    elif isinstance(response, str):
                        response_text = response
                    else:
                        response_text = str(response)

                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    logger.error(f"Agent error: {e}")

def display_error_page():
    """Display error page for missing packages."""
    st.title("❌ Setup Required")
    st.error("Some required packages are missing. Please install the dependencies:")

    st.code("pip install -r requirements.txt", language="bash")

    st.markdown("### Missing Components:")
    for error in MISSING_PACKAGES:
        st.error(f"• {error}")

    st.markdown("### Quick Fix:")
    st.info("Run the following command in your terminal:")
    st.code("pip install streamlit python-dotenv requests pytz", language="bash")

    if st.button("🔄 Try Again"):
        st.rerun()

def main():
    """Main application function."""
    # Check for missing packages first
    if MISSING_PACKAGES:
        display_error_page()
        return

    initialize_session_state()
    display_sidebar()
    display_chat_interface()

if __name__ == "__main__":
    main()
