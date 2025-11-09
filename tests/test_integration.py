"""
Integration Tests

End-to-end integration tests for the Hello World application.
"""

import pytest
import tempfile
import os
import yaml
from unittest.mock import patch, Mock
from src.config_manager import ConfigManager
from src.greeting_manager import GreetingManager


class TestIntegration:
    """Integration test cases."""
    
    def setup_method(self):
        """Set up test fixtures with real configuration."""
        self.test_config = {
            'app': {
                'name': 'Hello World Advanced',
                'version': '1.0.0',
                'debug': False
            },
            'greetings': {
                'default_name': 'World',
                'languages': {
                    'en': 'Hello, {name}!',
                    'es': '¡Hola, {name}!',
                    'fr': 'Bonjour, {name}!',
                    'de': 'Hallo, {name}!',
                    'it': 'Ciao, {name}!'
                },
                'time_based': {
                    'enabled': True,
                    'morning': 'Good morning, {name}!',
                    'afternoon': 'Good afternoon, {name}!',
                    'evening': 'Good evening, {name}!',
                    'night': 'Good night, {name}!'
                }
            },
            'output': {
                'color_enabled': True,
                'save_to_file': True,
                'output_file': 'logs/greetings.log'
            }
        }
    
    def test_full_workflow_standard_greeting(self):
        """Test complete workflow for standard greeting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            # Initialize managers
            config_manager = ConfigManager(temp_path)
            greeting_manager = GreetingManager(config_manager)
            
            # Test standard greeting
            result = greeting_manager.get_standard_greeting('Integration Test')
            
            assert result == 'Hello, Integration Test!'
            
            # Check statistics
            stats = greeting_manager.get_statistics()
            assert stats['total_greetings'] == 1
            assert stats['standard_greetings'] == 1
            
        finally:
            os.unlink(temp_path)
    
    def test_full_workflow_multilang_greetings(self):
        """Test complete workflow for multiple language greetings."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            greeting_manager = GreetingManager(config_manager)
            
            # Test multiple languages
            languages = ['en', 'es', 'fr', 'de', 'it']
            expected_greetings = [
                'Hello, MultiLang!',
                '¡Hola, MultiLang!',
                'Bonjour, MultiLang!',
                'Hallo, MultiLang!',
                'Ciao, MultiLang!'
            ]
            
            results = []
            for lang in languages:
                result = greeting_manager.get_multilang_greeting('MultiLang', lang)
                results.append(result)
            
            assert results == expected_greetings
            
            # Check statistics
            stats = greeting_manager.get_statistics()
            assert stats['total_greetings'] == 5
            assert stats['multilang_greetings'] == 5
            
            # Check language usage
            for lang in languages:
                assert stats['language_usage'][lang] == 1
                
        finally:
            os.unlink(temp_path)
    
    @patch('src.greeting_manager.datetime')
    def test_full_workflow_time_based_greetings(self, mock_datetime):
        """Test complete workflow for time-based greetings throughout the day."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            greeting_manager = GreetingManager(config_manager)
            
            # Test different times of day
            test_cases = [
                (8, 'Good morning, TimeTest!'),
                (14, 'Good afternoon, TimeTest!'),
                (19, 'Good evening, TimeTest!'),
                (2, 'Good night, TimeTest!')
            ]
            
            for hour, expected in test_cases:
                mock_datetime.now.return_value.hour = hour
                result = greeting_manager.get_time_based_greeting('TimeTest')
                assert result == expected
            
            # Check statistics
            stats = greeting_manager.get_statistics()
            assert stats['total_greetings'] == 4
            assert stats['time_based_greetings'] == 4
            
        finally:
            os.unlink(temp_path)
    
    def test_configuration_reload_affects_greetings(self):
        """Test that configuration changes affect greeting behavior."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            greeting_manager = GreetingManager(config_manager)
            
            # Initial greeting
            result1 = greeting_manager.get_standard_greeting()
            assert result1 == 'Hello, World!'
            
            # Modify configuration
            modified_config = self.test_config.copy()
            modified_config['greetings']['default_name'] = 'Universe'
            
            with open(temp_path, 'w') as f:
                yaml.dump(modified_config, f)
            
            # Reload configuration
            config_manager.reload_config()
            
            # Create new greeting manager with updated config
            greeting_manager_new = GreetingManager(config_manager)
            result2 = greeting_manager_new.get_standard_greeting()
            
            assert result2 == 'Hello, Universe!'
            
        finally:
            os.unlink(temp_path)
    
    def test_error_handling_invalid_language(self):
        """Test error handling for invalid language codes."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            greeting_manager = GreetingManager(config_manager)
            
            # Test invalid language
            with pytest.raises(ValueError) as exc_info:
                greeting_manager.get_multilang_greeting('Test', 'invalid')
            
            assert 'not supported' in str(exc_info.value)
            
            # Statistics should not be affected by failed operations
            stats = greeting_manager.get_statistics()
            assert stats['total_greetings'] == 0
            assert stats['multilang_greetings'] == 0
            
        finally:
            os.unlink(temp_path)