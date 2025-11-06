from typing import Optional

from config.base import BaseConfig
from config.loaders import ConfigLoader, JsonConfigLoader, YamlConfigLoader


class GlobalConfig(BaseConfig):
    """
    全局配置
    """

    _instance = None
    _initialized = False

    def __new__(cls, loader: ConfigLoader = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            BaseConfig.__init__(cls._instance, loader or JsonConfigLoader())
        return cls._instance

    def __init__(self, loader: ConfigLoader = None):
        pass

    def load(self, file_path: str) -> bool:
        """加载全局配置（只能加载一次）"""
        if self._initialized:
            print("全局配置已初始化，跳过重复加载")
            return True

        success = super().load(file_path)
        if success:
            self._initialized = True
        return success

    def reload(self) -> bool:
        """全局配置不支持重新加载"""
        if self._initialized:
            print("全局配置不支持重新加载")
            return False
        else:
            # 首次加载时调用父类的reload方法
            return super().reload()

    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._initialized

    def reset(self):
        """重置全局配置（主要用于测试）"""
        self._data = {}
        self._current_file = None
        self._initialized = False


class StoryConfig(BaseConfig):
    """
    故事配置
    """

    _instance = None

    def __new__(cls, loader: ConfigLoader = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            BaseConfig.__init__(cls._instance, loader or YamlConfigLoader())
        return cls._instance

    def __init__(self, loader: ConfigLoader = None):
        pass

    def reload(self) -> bool:
        """重新加载故事配置"""
        if not self._current_file:
            print("故事配置文件未设置")
            return False

        print("重新加载故事配置...")
        return super().reload()

    def reset(self):
        """重置故事配置（主要用于测试）"""
        self._data = {}
        self._current_file = None