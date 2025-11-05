from config.config_loader import ConfigLoader
from typing import Any

class GlobalConfig:
    _instance = None
    _data = {}
    _initialized = False

    def __new__(cls, loader: ConfigLoader = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 注入加载器
            cls._instance._loader = loader
        return cls._instance

    def initialize(self, config_file: str):
        if self._initialized:
            print("全局配置已初始化，跳过重复初始化")
            return

        if not self._loader:
            print("错误: 未设置配置加载器")
            return

        try:
            self._data = self._loader.load(config_file)
            self._initialized = True
            print(f"全局配置初始化: {config_file}")
        except Exception as e:
            print(f"全局配置初始化失败: {e}")

    def inject_loader(self, loader: ConfigLoader):
        self._loader = loader
        print("全局配置加载器已注入")

    def get(self, key: str, default: Any = None) -> Any:
        if not self._initialized:
            print("警告: 全局配置未初始化")
            return default

        keys = key.split('.')
        value = self._data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def is_initialized(self) -> bool:
        return self._initialized


class StoryConfig:
    _instance = None
    _data = {}
    _current_file = None

    def __new__(cls, loader: ConfigLoader = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 注入加载器
            cls._instance._loader = loader
        return cls._instance

    def inject_loader(self, loader: ConfigLoader):
        self._loader = loader
        print("运行时配置加载器已注入")

    def load(self, config_file: str) -> bool:
        if not self._loader:
            print("错误: 未设置配置加载器")
            return False

        self._current_file = config_file
        return self.reload()

    def reload(self) -> bool:
        if not self._current_file or not self._loader:
            return False

        try:
            self._data = self._loader.load(self._current_file)
            print(f"运行时配置加载: {self._current_file}")
            return True
        except Exception as e:
            print(f"运行时配置加载失败: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def current_file(self) -> str:
        return self._current_file