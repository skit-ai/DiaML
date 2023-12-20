import yaml
from typing import List, Dict

class APIConfig:
    def __init__(self, config_path):
        loaded_data = yaml.safe_load(config_path)
        self.api_map: Dict[str, Dict[str, str]] = loaded_data["API_OVERRIDES"]
        self.allowed_apis: List[str] = list(self.api_map.keys())
