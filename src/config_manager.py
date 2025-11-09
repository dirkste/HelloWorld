"""
Configuration Manager

Handles loading and managing application configuration from YAML files.
"""

import logging
import yaml
import os
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration loading and access."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration YAML file
        """
        self.config_path = config_path
        self.logger = logging.getLogger('hello_world.config')
        self._config = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            if not os.path.exists(self.config_path):
                self.logger.error(f"Configuration file not found: {self.config_path}")
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
            
            self.logger.info(f"Configuration loaded from {self.config_path}")
            
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML configuration: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the full configuration dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        if self._config is None:
            self._load_config()
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'app.name', 'greetings.default_name')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        try:
            config = self.get_config()
            keys = key.split('.')
            value = config
            
            for k in keys:
                value = value[k]
            
            self.logger.debug(f"Retrieved config value for '{key}': {value}")
            return value
            
        except (KeyError, TypeError):
            self.logger.warning(f"Configuration key '{key}' not found, using default: {default}")
            return default
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self.logger.info("Reloading configuration")
        self._config = None
        self._load_config()
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get('app.debug', False)
    
    def get_app_info(self) -> Dict[str, str]:
        """Get application name and version."""
        return {
            'name': self.get('app.name', 'Hello World'),
            'version': self.get('app.version', '1.0.0')
        }