import json
import yaml
from typing import Any, Dict, Protocol

class ConfigLoader(Protocol):
    """配置加载"""
    def load(self, file_path: str) -> Dict[str, Any]:
        ...

class JsonConfigLoader:
    def load(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"JSON配置加载失败: {e}")
            return {}

class YamlConfigLoader:
    def load(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except Exception as e:
            print(f"YAML配置加载失败: {e}")
            return {}
