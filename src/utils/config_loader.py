"""
Configuration loader utility.
"""

import yaml
from pathlib import Path


class ConfigLoader:
    """Load and manage configuration."""
    
    @staticmethod
    def load_config():
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
