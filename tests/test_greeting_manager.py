"""
Test Greeting Manager

Unit tests for the GreetingManager class.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.greeting_manager import GreetingManager
from src.config_manager import ConfigManager


class TestGreetingManager:
    """Test cases for GreetingManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_config = Mock(spec=ConfigManager)
        self.mock_config.get.return_value = {
            'greetings': {
                'default_name': 'World',
                'languages': {
                    'en': 'Hello, {name}!',
                    'es': '¡Hola, {name}!',
                    'fr': 'Bonjour, {name}!'
                },
                'time_based': {
                    'enabled': True,
                    'morning': 'Good morning, {name}!',
                    'afternoon': 'Good afternoon, {name}!',
                    'evening': 'Good evening, {name}!',
                    'night': 'Good night, {name}!'
                }
            }
        }
        
        self.greeting_manager = GreetingManager(self.mock_config)
    
    def test_standard_greeting_with_name(self):
        """Test standard greeting with provided name."""
        self.mock_config.get.return_value = 'World'
        
        result = self.greeting_manager.get_standard_greeting('Alice')
        
        assert result == 'Hello, Alice!'
        assert self.greeting_manager.stats['standard_greetings'] == 1
        assert self.greeting_manager.stats['total_greetings'] == 1
    
    def test_standard_greeting_without_name(self):
        """Test standard greeting with default name."""
        self.mock_config.get.return_value = 'World'
        
        result = self.greeting_manager.get_standard_greeting()
        
        assert result == 'Hello, World!'
        assert self.greeting_manager.stats['standard_greetings'] == 1
    
    def test_multilang_greeting_english(self):
        """Test multi-language greeting in English."""
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.default_name': 'World',
            'greetings.languages': {
                'en': 'Hello, {name}!',
                'es': '¡Hola, {name}!',
                'fr': 'Bonjour, {name}!'
            }
        }.get(key, default)
        
        result = self.greeting_manager.get_multilang_greeting('Bob', 'en')
        
        assert result == 'Hello, Bob!'
        assert self.greeting_manager.stats['multilang_greetings'] == 1
        assert self.greeting_manager.stats['language_usage']['en'] == 1
    
    def test_multilang_greeting_spanish(self):
        """Test multi-language greeting in Spanish."""
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.default_name': 'World',
            'greetings.languages': {
                'en': 'Hello, {name}!',
                'es': '¡Hola, {name}!',
                'fr': 'Bonjour, {name}!'
            }
        }.get(key, default)
        
        result = self.greeting_manager.get_multilang_greeting('Carlos', 'es')
        
        assert result == '¡Hola, Carlos!'
        assert self.greeting_manager.stats['language_usage']['es'] == 1
    
    def test_multilang_greeting_invalid_language(self):
        """Test multi-language greeting with invalid language."""
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.languages': {
                'en': 'Hello, {name}!',
                'es': '¡Hola, {name}!'
            }
        }.get(key, default)
        
        with pytest.raises(ValueError) as exc_info:
            self.greeting_manager.get_multilang_greeting('Alice', 'invalid')
        
        assert 'Language \'invalid\' not supported' in str(exc_info.value)
    
    @patch('src.greeting_manager.datetime')
    def test_time_based_greeting_morning(self, mock_datetime):
        """Test time-based greeting in the morning."""
        mock_datetime.now.return_value.hour = 8
        
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.default_name': 'World',
            'greetings.time_based.enabled': True,
            'greetings.time_based.morning': 'Good morning, {name}!'
        }.get(key, default)
        
        result = self.greeting_manager.get_time_based_greeting('Alice')
        
        assert result == 'Good morning, Alice!'
        assert self.greeting_manager.stats['time_based_greetings'] == 1
    
    @patch('src.greeting_manager.datetime')
    def test_time_based_greeting_afternoon(self, mock_datetime):
        """Test time-based greeting in the afternoon."""
        mock_datetime.now.return_value.hour = 15
        
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.default_name': 'World',
            'greetings.time_based.enabled': True,
            'greetings.time_based.afternoon': 'Good afternoon, {name}!'
        }.get(key, default)
        
        result = self.greeting_manager.get_time_based_greeting('Bob')
        
        assert result == 'Good afternoon, Bob!'
    
    @patch('src.greeting_manager.datetime')
    def test_time_based_greeting_evening(self, mock_datetime):
        """Test time-based greeting in the evening."""
        mock_datetime.now.return_value.hour = 19
        
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.default_name': 'World',
            'greetings.time_based.enabled': True,
            'greetings.time_based.evening': 'Good evening, {name}!'
        }.get(key, default)
        
        result = self.greeting_manager.get_time_based_greeting('Charlie')
        
        assert result == 'Good evening, Charlie!'
    
    @patch('src.greeting_manager.datetime')
    def test_time_based_greeting_night(self, mock_datetime):
        """Test time-based greeting at night."""
        mock_datetime.now.return_value.hour = 23
        
        self.mock_config.get.side_effect = lambda key, default=None: {
            'greetings.default_name': 'World',
            'greetings.time_based.enabled': True,
            'greetings.time_based.night': 'Good night, {name}!'
        }.get(key, default)
        
        result = self.greeting_manager.get_time_based_greeting('Diana')
        
        assert result == 'Good night, Diana!'
    
    def test_process_custom_message(self):
        """Test custom message processing."""
        result = self.greeting_manager.process_custom_message('  Have a great day!  ')
        
        assert result == '✨ Have a great day! ✨'
        assert self.greeting_manager.stats['custom_messages'] == 1
    
    def test_get_available_languages(self):
        """Test getting available languages."""
        self.mock_config.get.return_value = {
            'en': 'Hello, {name}!',
            'es': '¡Hola, {name}!',
            'fr': 'Bonjour, {name}!'
        }
        
        result = self.greeting_manager.get_available_languages()
        
        assert set(result) == {'en', 'es', 'fr'}
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        # Generate some greetings to populate stats
        self.mock_config.get.return_value = 'World'
        self.greeting_manager.get_standard_greeting('Alice')
        self.greeting_manager.process_custom_message('Hello!')
        
        stats = self.greeting_manager.get_statistics()
        
        assert stats['total_greetings'] == 2
        assert stats['standard_greetings'] == 1
        assert stats['custom_messages'] == 1
        assert 'session_duration_minutes' in stats
        assert 'session_start' in stats
    
    def test_greeting_history(self):
        """Test greeting history functionality."""
        self.mock_config.get.return_value = 'World'
        
        # Initially empty history
        history = self.greeting_manager.get_greeting_history()
        assert len(history) == 0
        
        # Add a greeting
        self.greeting_manager.get_standard_greeting('Alice')
        history = self.greeting_manager.get_greeting_history()
        
        assert len(history) == 1
        assert history[0]['greeting'] == 'Hello, Alice!'
        assert history[0]['type'] == 'standard'
        assert history[0]['name'] == 'Alice'
        assert 'timestamp' in history[0]
    
    def test_clear_history(self):
        """Test clearing greeting history."""
        self.mock_config.get.return_value = 'World'
        
        # Add some greetings
        self.greeting_manager.get_standard_greeting('Bob')
        self.greeting_manager.process_custom_message('Test message')
        
        # Verify history has items
        history = self.greeting_manager.get_greeting_history()
        assert len(history) == 2
        
        # Clear history
        self.greeting_manager.clear_history()
        history = self.greeting_manager.get_greeting_history()
        assert len(history) == 0