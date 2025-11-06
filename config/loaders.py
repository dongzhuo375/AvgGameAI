import json
import yaml
from typing import Any, Dict, Protocol


class ConfigLoader(Protocol):
    def load(self, file_path: str) -> Dict[str, Any]:
        ...


class JsonConfigLoader:
    def load(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"JSON配置文件不存在: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON配置文件格式错误: {e}")
            return {}
        except Exception as e:
            print(f"JSON配置加载失败: {e}")
            return {}


class YamlConfigLoader:
    def load(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            print(f"YAML配置文件不存在: {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"YAML配置文件格式错误: {e}")
            return {}
        except Exception as e:
            print(f"YAML配置加载失败: {e}")
            return {}
