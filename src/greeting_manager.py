"""
Greeting Manager

Handles different types of greetings and greeting statistics.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any
from config_manager import ConfigManager


class GreetingManager:
    """Manages greeting generation and statistics."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the greeting manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.logger = logging.getLogger('hello_world.greetings')
        self.stats = {
            'total_greetings': 0,
            'standard_greetings': 0,
            'multilang_greetings': 0,
            'time_based_greetings': 0,
            'custom_messages': 0,
            'language_usage': {},
            'session_start': datetime.now().isoformat()
        }
        
        self.logger.info("Greeting Manager initialized")
    
    def get_standard_greeting(self, name: str = None) -> str:
        """
        Generate a standard greeting.
        
        Args:
            name: Name to greet (uses default if None or empty)
            
        Returns:
            Formatted greeting string
        """
        if not name:
            name = self.config.get('greetings.default_name', 'World')
        
        greeting = f"Hello, {name}!"
        
        self._update_stats('standard_greetings')
        self.logger.debug(f"Generated standard greeting for: {name}")
        
        return greeting
    
    def get_multilang_greeting(self, name: str = None, language: str = 'en') -> str:
        """
        Generate a multi-language greeting.
        
        Args:
            name: Name to greet (uses default if None or empty)
            language: Language code (en, es, fr, de, it)
            
        Returns:
            Formatted greeting string in specified language
            
        Raises:
            ValueError: If language is not supported
        """
        if not name:
            name = self.config.get('greetings.default_name', 'World')
        
        languages = self.config.get('greetings.languages', {})
        
        if language not in languages:
            available = ', '.join(languages.keys())
            raise ValueError(f"Language '{language}' not supported. Available: {available}")
        
        template = languages[language]
        greeting = template.format(name=name)
        
        self._update_stats('multilang_greetings')
        self._update_language_stats(language)
        self.logger.debug(f"Generated {language} greeting for: {name}")
        
        return greeting
    
    def get_time_based_greeting(self, name: str = None) -> str:
        """
        Generate a time-based greeting.
        
        Args:
            name: Name to greet (uses default if None or empty)
            
        Returns:
            Time-appropriate greeting string
        """
        if not name:
            name = self.config.get('greetings.default_name', 'World')
        
        if not self.config.get('greetings.time_based.enabled', True):
            return self.get_standard_greeting(name)
        
        current_hour = datetime.now().hour
        
        # Determine time of day
        if 5 <= current_hour < 12:
            time_key = 'morning'
        elif 12 <= current_hour < 17:
            time_key = 'afternoon'
        elif 17 <= current_hour < 22:
            time_key = 'evening'
        else:
            time_key = 'night'
        
        template = self.config.get(f'greetings.time_based.{time_key}', 'Hello, {name}!')
        greeting = template.format(name=name)
        
        self._update_stats('time_based_greetings')
        self.logger.debug(f"Generated {time_key} greeting for: {name}")
        
        return greeting
    
    def process_custom_message(self, message: str) -> str:
        """
        Process a custom message.
        
        Args:
            message: Custom message to process
            
        Returns:
            Processed message with decoration
        """
        processed = f"✨ {message.strip()} ✨"
        
        self._update_stats('custom_messages')
        self.logger.debug(f"Processed custom message: {message[:50]}...")
        
        return processed
    
    def get_available_languages(self) -> List[str]:
        """
        Get list of available language codes.
        
        Returns:
            List of supported language codes
        """
        languages = self.config.get('greetings.languages', {})
        return list(languages.keys())
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get greeting statistics.
        
        Returns:
            Dictionary containing usage statistics
        """
        # Calculate session duration
        session_start = datetime.fromisoformat(self.stats['session_start'])
        session_duration = datetime.now() - session_start
        
        stats_copy = self.stats.copy()
        stats_copy['session_duration_minutes'] = round(session_duration.total_seconds() / 60, 2)
        
        return stats_copy
    
    def _update_stats(self, greeting_type: str) -> None:
        """Update greeting statistics."""
        self.stats['total_greetings'] += 1
        if greeting_type in self.stats:
            self.stats[greeting_type] += 1
    
    def _update_language_stats(self, language: str) -> None:
        """Update language usage statistics."""
        if language not in self.stats['language_usage']:
            self.stats['language_usage'][language] = 0
        self.stats['language_usage'][language] += 1