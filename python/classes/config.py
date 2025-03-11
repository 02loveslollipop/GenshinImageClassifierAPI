import yaml
import os
from typing import Dict
from classes.singletonMeta import SingletonMeta

class Config(metaclass=SingletonMeta):
    """
    A Singleton class for managing application configuration.
    """

    def __init__(self, config_file: str = 'config.yaml'):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load configuration from a YAML file.
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)
        
    def __getattr__(self, item):
        """
        Get configuration value by key.
        """
        return self.config_data.get(item, None)
    
    