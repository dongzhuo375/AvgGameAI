from typing import Any, Optional

from config.configs import StoryConfig, GlobalConfig
from config.loaders import ConfigLoader, JsonConfigLoader, YamlConfigLoader


class ConfigManager:
    """
    配置管理器
    """

    def __init__(self):
        # 创建加载器实例
        self.json_loader = JsonConfigLoader()
        self.yaml_loader = YamlConfigLoader()

        # 创建配置实例
        self.global_config = GlobalConfig(self.json_loader)
        self.story_config = StoryConfig(self.yaml_loader)

    def setup_global_config(self, file_path: str, loader: Optional[ConfigLoader] = None) -> bool:
        """设置全局配置"""
        if loader:
            self.global_config.set_loader(loader)
        return self.global_config.load(file_path)

    def setup_story_config(self, file_path: str, loader: Optional[ConfigLoader] = None) -> bool:
        """设置故事配置"""
        if loader:
            self.story_config.set_loader(loader)
        return self.story_config.load(file_path)

    def reload_story_config(self) -> bool:
        """重新加载故事配置"""
        return self.story_config.reload()

    def get_global_value(self, key: str, default: Any = None) -> Any:
        """获取全局配置值"""
        return self.global_config.get_value(key, default)

    def get_story_value(self, key: str, default: Any = None) -> Any:
        """获取故事配置值"""
        return self.story_config.get_value(key, default)

    def switch_global_loader(self, loader: ConfigLoader):
        """切换全局配置加载器"""
        self.global_config.set_loader(loader)

    def switch_story_loader(self, loader: ConfigLoader):
        """切换故事配置加载器"""
        self.story_config.set_loader(loader)

    def get_global_int(self, key: str, default: int = 0) -> int:
        """获取全局整型配置值"""
        return self.global_config.get_int(key, default)

    def get_story_int(self, key: str, default: int = 0) -> int:
        """获取故事整型配置值"""
        return self.story_config.get_int(key, default)

    def get_global_bool(self, key: str, default: bool = False) -> bool:
        """获取全局布尔型配置值"""
        return self.global_config.get_bool(key, default)

    def get_story_bool(self, key: str, default: bool = False) -> bool:
        """获取故事布尔型配置值"""
        return self.story_config.get_bool(key, default)

    def get_global_float(self, key: str, default: float = 0.0) -> float:
        """获取全局浮点型配置值"""
        return self.global_config.get_float(key, default)

    def get_story_float(self, key: str, default: float = 0.0) -> float:
        """获取故事浮点型配置值"""
        return self.story_config.get_float(key, default)

    def is_global_initialized(self) -> bool:
        """检查全局配置是否已初始化"""
        return self.global_config.is_initialized()

    def get_status(self) -> dict:
        """获取配置管理器状态"""
        return {
            "global_config": {
                "initialized": self.global_config.is_initialized(),
                "file": self.global_config.current_file(),
                "keys_count": len(self.global_config.get_all_data())
            },
            "story_config": {
                "file": self.story_config.current_file(),
                "keys_count": len(self.story_config.get_all_data())
            }
        }