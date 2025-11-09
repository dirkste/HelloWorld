"""
Advanced Hello World Application

A more sophisticated greeting application with:
- Logging configuration
- Multiple greeting languages and modes
- Time-based greetings
- Configuration management
- Error handling
"""

import logging
import logging.config
import yaml
import os
import sys
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from greeting_manager import GreetingManager
from config_manager import ConfigManager


def setup_logging(config_path: str = "config/logging.yaml") -> None:
    """Set up logging configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Ensure log directory exists
        os.makedirs('logs', exist_ok=True)
        
        logging.config.dictConfig(config)
        logger = logging.getLogger('hello_world')
        logger.info("Logging configuration loaded successfully")
        
    except FileNotFoundError:
        # Fallback to basic logging if config file not found
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('logs/hello_world.log')
            ]
        )
        logger = logging.getLogger('hello_world')
        logger.warning(f"Could not load logging config from {config_path}, using basic config")
    except Exception as e:
        print(f"Error setting up logging: {e}")
        sys.exit(1)


def main():
    """Main application entry point."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger('hello_world')
    
    try:
        logger.info("Starting Hello World Advanced Application")
        
        # Load configuration
        config_manager = ConfigManager("config/settings.yaml")
        app_config = config_manager.get_config()
        
        logger.info(f"Loaded configuration for {app_config['app']['name']} v{app_config['app']['version']}")
        
        # Initialize greeting manager
        greeting_manager = GreetingManager(config_manager)
        
        # Interactive mode
        print(f"\n🌟 Welcome to {app_config['app']['name']} v{app_config['app']['version']} 🌟\n")
        
        while True:
            print("\nChoose an option:")
            print("1. Standard greeting")
            print("2. Multi-language greeting") 
            print("3. Time-based greeting")
            print("4. Custom message")
            print("5. Show greeting statistics")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            logger.debug(f"User selected option: {choice}")
            
            if choice == "1":
                handle_standard_greeting(greeting_manager, logger)
            elif choice == "2":
                handle_multilang_greeting(greeting_manager, logger)
            elif choice == "3":
                handle_time_greeting(greeting_manager, logger)
            elif choice == "4":
                handle_custom_message(greeting_manager, logger)
            elif choice == "5":
                handle_statistics(greeting_manager, logger)
            elif choice == "6":
                logger.info("Application shutting down by user request")
                print("\nGoodbye! 👋")
                break
            else:
                logger.warning(f"Invalid menu choice: {choice}")
                print("❌ Invalid choice. Please try again.")
                
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
        print("\n\nApplication interrupted. Goodbye! 👋")
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}", exc_info=True)
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)


def handle_standard_greeting(greeting_manager: GreetingManager, logger: logging.Logger):
    """Handle standard greeting interaction."""
    try:
        name = input("Enter your name (or press Enter for default): ").strip()
        greeting = greeting_manager.get_standard_greeting(name)
        logger.info(f"Generated standard greeting for: {name or 'default'}")
        print(f"\n✨ {greeting}")
    except Exception as e:
        logger.error(f"Error in standard greeting: {str(e)}")
        print("❌ Error generating greeting")


def handle_multilang_greeting(greeting_manager: GreetingManager, logger: logging.Logger):
    """Handle multi-language greeting interaction."""
    try:
        languages = greeting_manager.get_available_languages()
        print(f"\nAvailable languages: {', '.join(languages)}")
        
        lang = input("Enter language code: ").strip().lower()
        name = input("Enter your name (or press Enter for default): ").strip()
        
        greeting = greeting_manager.get_multilang_greeting(name, lang)
        logger.info(f"Generated {lang} greeting for: {name or 'default'}")
        print(f"\n✨ {greeting}")
    except ValueError as e:
        logger.warning(f"Invalid language selection: {str(e)}")
        print(f"❌ {e}")
    except Exception as e:
        logger.error(f"Error in multilang greeting: {str(e)}")
        print("❌ Error generating greeting")


def handle_time_greeting(greeting_manager: GreetingManager, logger: logging.Logger):
    """Handle time-based greeting interaction."""
    try:
        name = input("Enter your name (or press Enter for default): ").strip()
        greeting = greeting_manager.get_time_based_greeting(name)
        logger.info(f"Generated time-based greeting for: {name or 'default'}")
        print(f"\n✨ {greeting}")
    except Exception as e:
        logger.error(f"Error in time-based greeting: {str(e)}")
        print("❌ Error generating greeting")


def handle_custom_message(greeting_manager: GreetingManager, logger: logging.Logger):
    """Handle custom message interaction."""
    try:
        message = input("Enter your custom message: ").strip()
        if message:
            result = greeting_manager.process_custom_message(message)
            logger.info(f"Processed custom message: {message[:50]}...")
            print(f"\n✨ {result}")
        else:
            print("❌ Message cannot be empty")
    except Exception as e:
        logger.error(f"Error in custom message: {str(e)}")
        print("❌ Error processing message")


def handle_statistics(greeting_manager: GreetingManager, logger: logging.Logger):
    """Handle statistics display."""
    try:
        stats = greeting_manager.get_statistics()
        logger.debug("Displayed greeting statistics")
        print("\n📊 Greeting Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        print("❌ Error retrieving statistics")


if __name__ == "__main__":
    main()