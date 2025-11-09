"""
Test Configuration Manager

Unit tests for the ConfigManager class.
"""

import pytest
import tempfile
import os
import yaml
from unittest.mock import patch, mock_open
from src.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_config = {
            'app': {
                'name': 'Test App',
                'version': '1.0.0',
                'debug': True
            },
            'greetings': {
                'default_name': 'TestWorld',
                'languages': {
                    'en': 'Hello, {name}!',
                    'es': '¡Hola, {name}!'
                }
            }
        }
    
    def test_load_config_success(self):
        """Test successful configuration loading."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            loaded_config = config_manager.get_config()
            
            assert loaded_config == self.test_config
            assert config_manager.get('app.name') == 'Test App'
        finally:
            os.unlink(temp_path)
    
    def test_load_config_file_not_found(self):
        """Test handling of missing configuration file."""
        with pytest.raises(FileNotFoundError):
            ConfigManager('nonexistent.yaml')
    
    def test_get_nested_config_value(self):
        """Test retrieving nested configuration values."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            
            assert config_manager.get('app.name') == 'Test App'
            assert config_manager.get('app.version') == '1.0.0'
            assert config_manager.get('greetings.default_name') == 'TestWorld'
            assert config_manager.get('nonexistent.key', 'default') == 'default'
        finally:
            os.unlink(temp_path)
    
    def test_is_debug_enabled(self):
        """Test debug mode detection."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            assert config_manager.is_debug_enabled() is True
        finally:
            os.unlink(temp_path)
    
    def test_get_app_info(self):
        """Test application info retrieval."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            app_info = config_manager.get_app_info()
            
            assert app_info['name'] == 'Test App'
            assert app_info['version'] == '1.0.0'
        finally:
            os.unlink(temp_path)
    
    def test_reload_config(self):
        """Test configuration reloading."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(self.test_config, f)
            temp_path = f.name
        
        try:
            config_manager = ConfigManager(temp_path)
            original_name = config_manager.get('app.name')
            
            # Modify config file
            updated_config = self.test_config.copy()
            updated_config['app']['name'] = 'Updated App'
            
            with open(temp_path, 'w') as f:
                yaml.dump(updated_config, f)
            
            config_manager.reload_config()
            new_name = config_manager.get('app.name')
            
            assert original_name == 'Test App'
            assert new_name == 'Updated App'
        finally:
            os.unlink(temp_path)