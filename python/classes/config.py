import yaml
import os
from typing import Dict, Optional
from classes.singletonMeta import SingletonMeta

class Config(metaclass=SingletonMeta):
    """
    A Singleton class for managing application configuration.
    Provides thread-safe access to configuration data and lazy loading.
    """
    _instance: Optional['Config'] = None
    _config_data: Optional[Dict] = None

    def __new__(cls, config_file: str = 'config.yaml'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config_file = config_file
        return cls._instance

    def __init__(self, config_file: str = 'config.yaml'):
        # Skip initialization if already initialized
        if hasattr(self, '_initialized'):
            return
        self._config_file = config_file
        self._initialized = True

    @property
    def config_data(self) -> Dict:
        """
        Lazy loading of configuration data.
        Returns the configuration dictionary, loading it if not already loaded.
        """
        if self._config_data is None:
            self._config_data = self._load_config()
        return self._config_data

    def _load_config(self) -> Dict:
        """
        Load configuration from a YAML file.
        Raises FileNotFoundError if the config file doesn't exist.
        """
        config_path = self._get_config_path()
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found.")
        
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def _get_config_path(self) -> str:
        """
        Get the absolute path to the config file.
        First checks in the current working directory, then in the script directory.
        """
        if os.path.exists(self._config_file):
            return self._config_file
        
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(script_dir, self._config_file)

    def __getitem__(self, item):
        """
        Get configuration value by key.
        Returns None if the key doesn't exist.
        """
        return self.config_data.get(item)

    def reload(self) -> None:
        """
        Force reload the configuration from the file.
        Useful for updating configuration without restarting the application.
        """
        self._config_data = None