#!/usr/bin/env python3
"""Local development runner for the Weather Agent Streamlit application."""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_requirements():
    """Check if required packages are installed."""
    try:
        import streamlit
        import google.adk
        import opik
        logger.info("✅ All required packages are installed")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing required package: {e}")
        logger.info("Run: pip install -r requirements.txt")
        return False

def check_configuration():
    """Check if configuration is valid."""
    missing = config.validate_config()
    if missing:
        logger.warning(f"⚠️ Missing configuration: {', '.join(missing)}")
        logger.info("Copy .env.example to .env and fill in your API keys")
        return False
    else:
        logger.info("✅ Configuration is valid")
        return True

def run_streamlit():
    """Run the Streamlit application."""
    app_path = Path(__file__).parent / "app" / "app.py"

    if not app_path.exists():
        logger.error(f"❌ App file not found: {app_path}")
        return False

    logger.info("Starting Streamlit application...")
    logger.info("Open your browser to: http://localhost:8501")

    try:
        # Run streamlit with the app
        cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)]
        subprocess.run(cmd, cwd=Path(__file__).parent)
        return True
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start Streamlit: {e}")
        return False

def main():
    """Main entry point."""
    print("Weather Agent - Local Development")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        return 1

    # Check configuration
    if not check_configuration():
        print("\n⚠️  You can still run the app, but some features may not work.")

    print("\nStarting application...\n")

    # Run the application
    success = run_streamlit()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
